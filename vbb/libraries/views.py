from typing import Optional

from rest_framework import permissions, status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from vbb.users.models import User
from vbb.profiles.models import MentorProfile, StudentProfile

from vbb.libraries.models import Announcement, Library, LibraryComputerSlots, UserPreferenceSlot, Computer, ComputerReservation
from vbb.libraries.serializers import LibrarySerializer, LibraryWithComputersSerializer
from vbb.utils.custom_csrf import CsrfHTTPOnlySessionAuthentication
from vbb.libraries import serializers
from vbb.profiles import serializers as profileSerializers
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from vbb.meetings.api import generateCalendarEvent



class LibraryViews(viewsets.ViewSet):
    """All non-admin level Library Views

    Currently only a View Set with a get '/' and detail '/<id>'
    """

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Library.objects.all()

    def list(self, request: Request) -> Response:
        """Returns list of all libraries in the system with limited fields."""
        serialized_libraries = LibrarySerializer(
            self.queryset, context={"request": request}, many=True
        )
        return Response(data=serialized_libraries.data)

    def retrieve(self, request: Request, pk: Optional[int] = None) -> Response:
        """Returns a library detail with slots."""
        try:
            serialized_library = LibraryWithComputersSerializer(
                self.queryset.get(id=pk), context={"request": request}
            )
            return Response(data=serialized_library.data)
        except Library.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class LibraryDetailViews(APIView):
    """All non-admin level Library Views
    Currently only a View Set with detail '/<uniqueID>'
    """

    #authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request: Request, uniqueID) -> Response:
        #serializer = serializers.RetieveLibrarySlotSerializer(data=request.data)
        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided library uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        library = None

        try:
            library = Library.objects.get(uniqueID=uniqueID)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided uniuqeID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        librarySerializer = serializers.LibrarySerializer(library, many=False)
        return Response(librarySerializer.data, status=status.HTTP_200_OK)



class AdminLibraryViews(APIView):
    """All Admin level Library Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Returns a list of all Libraries including codes"""
        return Response(data="Not implemented yet")

class AnnouncementViews(APIView):
    """All Announcement level Library Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uniqueID) -> Response:

        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided library ID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        libraryObj = {}

        try:
            libraryObj = Library.objects.get(uniqueID=uniqueID)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        allAnnouncements = Announcement.objects.filter(library=libraryObj.pk)

        if allAnnouncements == None:
            return Response({"error": "Server error occurred."}, status=status.HTTP_400_BAD_REQUEST)

        announcmentSerializer = serializers.AnnouncementSerializer(allAnnouncements, many=True)
        return Response(announcmentSerializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request) -> Response:
            serializer = serializers.CreateAnnouncementSerializer(data=request.data)
            lib = {}
            if serializer.is_valid():
                text = serializer.validated_data["text"]
                display_start = serializer.validated_data["display_start"]
                display_end = serializer.validated_data["display_end"]
                library = serializer.validated_data["library"]
                notes = serializer.validated_data["notes"]

                announcment = {}

                try:
                    lib = Library.objects.get(uniqueID=library)
                except Announcement.DoesNotExist:
                    return Response({"error": "Library with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    announcment = Announcement.objects.get(text=text)
                except Announcement.DoesNotExist:
                    announcment = Announcement.objects.create(text=text, display_start=display_start, display_end=display_end, library=lib, notes=notes)
                    announcment.save()

                    announcmentSerializer = serializers.AnnouncementSerializer(announcment, many=False)
                    return Response(announcmentSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, uniqueID) -> Response:

            if uniqueID == "" or uniqueID == None:
                    return Response({"error": "Provided uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = serializers.UpdateAnnouncementSerializer(data=request.data)
            if serializer.is_valid():
                text = serializer.validated_data["text"]
                display_start = serializer.validated_data["display_start"]
                display_end = serializer.validated_data["display_end"]
                #library = serializer.validated_data["library"]
                notes = serializer.validated_data["notes"]

                announcment = {}

                try:
                    announcment = Announcement.objects.get(uniqueID=uniqueID)
                except Announcement.DoesNotExist:
                    return Response({"error": "Announcement with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                announcment.text = text
                announcment.display_start = display_start
                announcment.display_end = display_end
                announcment.notes = notes
                announcment.save()

                announcmentSerializer = serializers.AnnouncementSerializer(announcment, many=False)
                return Response(announcmentSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, uniqueID) -> Response:
        print(uniqueID)
        if uniqueID == "" or uniqueID == None:
            return Response({"error": "Provided Announcement ID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            announcment = Announcement.objects.get(uniqueID=uniqueID)
        except Announcement.DoesNotExist:
            return Response({"error": "Announcement with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

        announcment.delete()
        return Response({"msg":"Announcement deleted successfully."}, status=status.HTTP_200_OK)


class RetrieveLibraryMentorsViews(APIView):
    """All Computer Related Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uniqueID) -> Response:
        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided library ID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        library = {}
        mentors = None

        try:
            library = Library.objects.get(uniqueID=uniqueID)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mentors = MentorProfile.objects.filter(assigned_library=library.pk)
        except MentorProfile.DoesNotExist:
            return Response({"error": "No mentor with that library could be found."}, status=status.HTTP_400_BAD_REQUEST)

        mentorSerializer = profileSerializers.MentorProfileWithUserSerializer(mentors, many=True)
        return Response(mentorSerializer.data, status=status.HTTP_200_OK)

class RetrieveLibraryStudentsViews(APIView):
    """All Computer Related Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uniqueID) -> Response:
        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided library ID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        library = {}
        students = None

        try:
            library = Library.objects.get(uniqueID=uniqueID)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            students = StudentProfile.objects.filter(assigned_library=library.pk)
        except StudentProfile.DoesNotExist:
            return Response({"error": "No students with that library could be found."}, status=status.HTTP_400_BAD_REQUEST)

        studentSerializer = profileSerializers.StudentProfileWithUserSerializer(students, many=True)
        return Response(studentSerializer.data, status=status.HTTP_200_OK)

class RetrieveLibraryComputerViews(APIView):
    """All Computer Related Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uniqueID) -> Response:
        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided library ID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        library = {}
        computerObjs = None

        try:
            library = Library.objects.get(uniqueID=uniqueID)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            computerObjs = Computer.objects.filter(library=library.pk)
        except Computer.DoesNotExist:
            return Response({"error": "No computers with that library could be found."}, status=status.HTTP_400_BAD_REQUEST)

        computerSerializer = serializers.ComputerSerializer(computerObjs, many=True)
        return Response(computerSerializer.data, status=status.HTTP_200_OK)


class LibraryComputerSlotViews(APIView):
    """All Computer Related Views"""
    # add admin permission levels
    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uniqueID) -> Response:
        #serializer = serializers.RetieveLibrarySlotSerializer(data=request.data)

        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided library uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        librarySlots = None
        library = None

        try:
            library = Library.objects.get(uniqueID=uniqueID)
        except Computer.DoesNotExist:
            return Response({"error": "Library with that provided uniuqeID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            librarySlots = LibraryComputerSlots.objects.filter(library=library.pk)
        except LibraryComputerSlots.DoesNotExist:
            return Response({"error": "No computer slots with this library could be found."}, status=status.HTTP_400_BAD_REQUEST)
        print(librarySlots)

        librarySlotsSerializer = serializers.LibrarySlotSerializer(librarySlots, many=True)
        return Response(librarySlotsSerializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request) -> Response:
            serializer = serializers.CreateLibrarySlotSerializer(data=request.data)
            if serializer.is_valid():
                # start_time = serializer.validated_data["start_time"]
                # end_time = serializer.validated_data["end_time"]
                # start_recurring = serializer.validated_data["start_recurring"]
                # end_recurring = serializer.validated_data["end_recurring"]
                # day = serializer.validated_data["day"]
                library = serializer.validated_data["library"]

                try:
                    library = Library.objects.get(uniqueID=library)
                except Library.DoesNotExist:
                    return Response({"error": "Library with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                serializer.validated_data["library"] = library
                #Add existting time range slot exception

                libSlot = {}

                libSlot = LibraryComputerSlots.objects.create(**serializer.validated_data)
                libSlot.save()
                libSlotSerializer = serializers.LibrarySlotSerializer(libSlot, many=False)
                return Response(libSlotSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, uniqueID) -> Response:
            serializer = serializers.UpdateLibrarySlotSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                start_time = serializer.validated_data["start_time"]
                end_time = serializer.validated_data["end_time"]
                start_recurring = serializer.validated_data["start_recurring"]
                end_recurring = serializer.validated_data["end_recurring"]
                day = serializer.validated_data["day"]
                library = serializer.validated_data["library"]

                libSlot = {}

                try:
                    libSlot = LibraryComputerSlots.objects.get(uniqueID=uniqueID)
                except Computer.DoesNotExist:
                    return Response({"error": "Library Slot with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                libSlot.start_time = start_time
                libSlot.end_time = end_time
                libSlot.start_recurring = start_recurring
                libSlot.end_recurring = end_recurring
                libSlot.day = day
                libSlot.library = library
                libSlot.save()

                libSlotSerializer = serializers.LibrarySlotSerializer(libSlot, many=False)
                return Response(libSlotSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, uniqueID) -> Response:
            if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                libSlot = LibraryComputerSlots.objects.get(uniqueID=uniqueID)
            except LibraryComputerSlots.DoesNotExist:
                return Response({"error": "Library Slot with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

            libSlot.delete()
            return Response({"msg":"Library Slot deleted successfully."}, status=status.HTTP_200_OK)


class RetrieveLibraryStudentPreferencesViews(APIView):
    """All User Preference Slot Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uniqueID) -> Response:
            if uniqueID:
                userSlots = {}
                libSlotIDs = []

                try:
                    library = Library.objects.get(uniqueID=uniqueID)
                except Library.DoesNotExist:
                    return Response({"error": "Library with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                try:
                    allLibrarySlots = LibraryComputerSlots.objects.filter(library=library.pk)
                except LibraryComputerSlots.DoesNotExist:
                    return Response({"error": "Library with that provided id could not be found."}, status=status.HTTP_404_NOT_FOUND)

                for lib in allLibrarySlots:
                    libSlotIDs.append(lib.pk)

                print(libSlotIDs)

                try:
                    userSlots = UserPreferenceSlot.objects.filter(computer_slot__in=libSlotIDs, mentor=None)
                except UserPreferenceSlot.DoesNotExist:
                    return Response({"error": "User Preference Slots with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                userSlotsSerializer = serializers.UserPreferenceSlotSerializer(userSlots, many=True)
                return Response(userSlotsSerializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Library uniqueID needs to be provided."}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUserPreferenceSlotViews(APIView):
    """All User Preference Slot Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uniqueID) -> Response:
        # serializer = serializers.RetieveUserPreferenceSlotSerializer(data=request.data)
        # userId = serializer.validated_data["userId"]

        userId = request.user.pk

        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        userSlots = None
        lib = None
        hours = None

        try:
            lib = Library.objects.get(uniqueID=uniqueID)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hours = LibraryComputerSlots.objects.filter(library=lib)
        except LibraryComputerSlots.DoesNotExist:
            return Response({"error": "Library slots could not be found with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        slotList = []

        for hr in hours:
            slotList.append(hr.pk)

        try:
            userSlots = UserPreferenceSlot.objects.filter(computer_slot__in=slotList)

        except UserPreferenceSlot.DoesNotExist:
            return Response({"error": "No user slots with this userId could be found."}, status=status.HTTP_400_BAD_REQUEST)

        userSlotsSerializer = serializers.UserPreferenceSlotWithUsersSerializer(userSlots, many=True)
        return Response(userSlotsSerializer.data, status=status.HTTP_200_OK)


class RetrieveComputerReservationViews(APIView):
    """All User Preference Slot Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uniqueID) -> Response:
        # serializer = serializers.RetieveUserPreferenceSlotSerializer(data=request.data)
        # userId = serializer.validated_data["userId"]

        userId = request.user.pk

        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        userSlots = None
        lib = None
        hours = None
        computerReservations = None
        try:
            lib = Library.objects.get(uniqueID=uniqueID)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hours = LibraryComputerSlots.objects.filter(library=lib)
        except LibraryComputerSlots.DoesNotExist:
            return Response({"error": "Library slots could not be found with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        slotList = []

        for hr in hours:
            slotList.append(hr.pk)

        try:
            userSlots = UserPreferenceSlot.objects.filter(computer_slot__in=slotList)

        except UserPreferenceSlot.DoesNotExist:
            return Response({"error": "No user slots with this userId could be found."}, status=status.HTTP_400_BAD_REQUEST)


        userSlotList = []

        for slot in userSlots:
            userSlotList.append(slot.pk)


        try:
            computerReservations = ComputerReservation.objects.filter(reserved_slot__in=userSlotList)

        except ComputerReservation.DoesNotExist:
            return Response({"error": "No computer reservations could be found."}, status=status.HTTP_400_BAD_REQUEST)


        reservationSerializer = serializers.ComputerReservationWithUserSerializer(computerReservations, many=True)
        return Response(reservationSerializer.data, status=status.HTTP_200_OK)


class UserPreferenceSlotViews(APIView):
    """All User Preference Slot Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        # serializer = serializers.RetieveUserPreferenceSlotSerializer(data=request.data)
        # userId = serializer.validated_data["userId"]

        userId = request.user.pk

        if userId == "" or userId == None:
                return Response({"error": "Provided userId cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        userSlots = None
        user = None

        try:
            user = User.objects.get(pk=userId)
        except User.DoesNotExist:
            return Response({"error": "User with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            if user.is_student == True:
                userSlots = UserPreferenceSlot.objects.filter(student=user.pk)
            elif user.is_mentor == True:
                userSlots = UserPreferenceSlot.objects.filter(mentor=user.pk)
            else:
                return Response({"error": "User must be a mentor or student to make a preference slot."}, status=status.HTTP_400_BAD_REQUEST)

        except UserPreferenceSlot.DoesNotExist:
            return Response({"error": "No user slots with this userId could be found."}, status=status.HTTP_400_BAD_REQUEST)

        userSlotsSerializer = serializers.UserPreferenceSlotSerializer(userSlots, many=True)
        return Response(userSlotsSerializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request) -> Response:
            serializer = serializers.CreateUserPreferenceSlotSerializer(data=request.data)
            if serializer.is_valid():


                print(serializer.validated_data)
                student = serializer.validated_data["student"]
                # mentor = serializer.validated_data["mentor"]
                lib_computer_slot = serializer.validated_data["lib_computer_slot"]
                start_time = serializer.validated_data["start_time"]
                end_time = serializer.validated_data["end_time"]
                start_recurring = None
                end_recurring = None

                try:
                    start_recurring = serializer.validated_data["start_recurring"]
                    end_recurring = serializer.validated_data["end_recurring"]
                except KeyError:
                    start_recurring = None
                    end_recurring = None

                availableSlot = {}


                studentProfileObj = None

                try:
                    studentObj = User.objects.get(pk=int(student))
                except User.DoesNotExist:
                    return Response({"error": "User with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)


                try:
                    studentProfileObj = StudentProfile.objects.get(user=studentObj)
                except StudentProfile.DoesNotExist:
                    return Response({"error": "StudentProfile with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)



                if studentProfileObj.approval_status != "Approved":
                    return Response({"error": "You are not approved yet."}, status=status.HTTP_400_BAD_REQUEST)


                try:
                    availableSlot = LibraryComputerSlots.objects.get(uniqueID=lib_computer_slot)
                except LibraryComputerSlots.DoesNotExist:
                    return Response({"error": "LibraryComputerSlot with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    reservedSlots = UserPreferenceSlot.objects.filter(computer_slot=availableSlot, start_time__contains=start_time, end_time__contains=end_time)
                except UserPreferenceSlot.DoesNotExist:
                    return Response({"error": "UserPreferenceSlot with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)


                try:
                    availableComputers = Computer.objects.filter(library=availableSlot.library)
                except Computer.DoesNotExist:
                    return Response({"error": "Computers with that provided Computer Slot could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                if len(availableComputers) == 0:
                    return Response({"error": "No Computers available to reserve."}, status=status.HTTP_400_BAD_REQUEST)

                allComputersID = []

                for computer in availableComputers:
                    allComputersID.append(computer.pk)

                #Determine if exsiting reservation at time can be found in list of computers.
                try:
                    allComputersReservations = ComputerReservation.objects.filter(start_time=start_time, end_time=end_time, computer__in=allComputersID)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "ComputerReservation with that provided timeslot taken already."}, status=status.HTTP_400_BAD_REQUEST)

                print(allComputersID)
                print(allComputersReservations)


                #Add existting time range slot exception
                userSlot = None
                userSlotSerializer = {}


                #Generate Conference URLS

                if len(allComputersReservations) == 0:
                    #Create Multiple  Computer Reservations if Reccurring
                    if start_recurring != None and end_recurring != None:

                        startSplit = start_time
                        startTz = start_time.split('T')[1]

                        endSplit = end_time
                        endTz = end_time.split('T')[1]

                        startRecSplit = start_recurring.split('T')[0]
                        startRecTz = start_recurring.split('T')[1]

                        endRecSplit = end_recurring.split('T')[0]
                        endRecTz = end_recurring.split('T')[1]

                        startRecurFormatted = datetime.strptime(startRecSplit, '%Y-%m-%d')
                        endRecurFormatted = datetime.strptime(endRecSplit, '%Y-%m-%d')

                        startFormatted = datetime.strptime(startSplit, '%Y-%m-%dT%H:%M:%S.%fZ')
                        endFormatted = datetime.strptime(endSplit, '%Y-%m-%dT%H:%M:%S.%fZ')

                        print(startFormatted)
                        print(endFormatted)

                        #Find Recurring Date Difference
                        recurr_diff = endRecurFormatted - startRecurFormatted
                        numberOfWeeks = recurr_diff.days // 7

                        #Find Recurring Date Difference
                        hour_diff = endFormatted - startFormatted
                        numOfSessionHours = hour_diff
                        print(numOfSessionHours)

                        userSlot = UserPreferenceSlot.objects.create(start_time=start_time, end_time=end_time, start_recurring=start_recurring, end_recurring=end_recurring, computer_slot=availableSlot, student=studentObj, is_recurring=True)
                        userSlot.save()
                        userSlotSerializer = serializers.UserPreferenceSlotSerializer(userSlot, many=False)


                        computerReservationsList = []
                        #Make Reccurring Object Creation Logic
                        #Create the inital day of reservation
                        newComputerReserve = ComputerReservation.objects.create(start_time=start_time, end_time=end_time, reserved_slot=userSlot, student=studentObj, computer=availableComputers[0], transaction_id=uuid.uuid4())
                        newComputerReserve.save()
                        computerReservationsList.append(newComputerReserve)

                        #Create the temporary computer reservation objects
                        date_tmp = startRecurFormatted
                        for week in range(0, numberOfWeeks):
                            print("Computer Reservation Created")
                            new_start_date = date_tmp + timedelta(days=7)
                            date_tmp = new_start_date
                            new_start_date_object = datetime(new_start_date.year, new_start_date.month, new_start_date.day, startFormatted.hour, startFormatted.minute)
                            new_end_date_object = datetime(new_start_date.year, new_start_date.month, new_start_date.day, endFormatted.hour, endFormatted.minute)
                            print(new_start_date_object)
                            print(new_end_date_object)
                            formattedStartDate =  new_start_date_object.strftime('%Y/%m/%d')
                            formattedEndDate = new_end_date_object.strftime('%Y/%m/%d')
                            print(formattedStartDate)
                            print(formattedEndDate)

                            newComputerReserve = ComputerReservation.objects.create(start_time=new_start_date_object, end_time=new_end_date_object, reserved_slot=userSlot, student=studentObj, computer=availableComputers[0], transaction_id=uuid.uuid4())
                            newComputerReserve.save()
                            computerReservationsList.append(newComputerReserve)


                        computerReserveSerializer = serializers.ComputerReservationSerializer(computerReservationsList, many=True)
                        print(computerReserveSerializer.data)

                    else:
                        #Create Single Reservation Object
                        userSlot = UserPreferenceSlot.objects.create(start_time=start_time, end_time=end_time, computer_slot=availableSlot, student=studentObj)
                        userSlot.save()
                        userSlotSerializer = serializers.UserPreferenceSlotSerializer(userSlot, many=False)
                        newComputerReserve = ComputerReservation.objects.create(start_time=start_time, end_time=end_time, reserved_slot=userSlot, student=studentObj, computer=availableComputers[0], transaction_id=uuid.uuid4())
                        newComputerReserve.save()
                        computerReserveSerializer = serializers.ComputerReservationSerializer(newComputerReserve, many=False)
                        print(computerReserveSerializer.data)

                else:
                    reservedComputers = []
                    freeComputers = []

                    for computer in allComputersReservations:
                        reservedComputers.append(computer.computer.pk)
                    print(reservedComputers)

                    for comp in allComputersID:
                        if comp not in reservedComputers:
                            freeComputers.append(comp)

                    print(freeComputers)
                    print("Reservations with computers found at this time")

                    if len(freeComputers) <= 0:
                        return Response({"error": "No free computers at this time."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        selectedComputer = Computer.objects.get(pk=freeComputers[0])
                        if start_recurring != None and end_recurring != None:

                            startSplit = start_time
                            startTz = start_time.split('T')[1]

                            endSplit = end_time
                            endTz = end_time.split('T')[1]

                            startRecSplit = start_recurring.split('T')[0]
                            startRecTz = start_recurring.split('T')[1]

                            endRecSplit = end_recurring.split('T')[0]
                            endRecTz = end_recurring.split('T')[1]

                            startRecurFormatted = datetime.strptime(startRecSplit, '%Y-%m-%d')
                            endRecurFormatted = datetime.strptime(endRecSplit, '%Y-%m-%d')

                            startFormatted = datetime.strptime(startSplit, '%Y-%m-%dT%H:%M:%S.%fZ')
                            endFormatted = datetime.strptime(endSplit, '%Y-%m-%dT%H:%M:%S.%fZ')

                            print(startFormatted)
                            print(endFormatted)

                            #Find Recurring Date Difference
                            recurr_diff = endRecurFormatted - startRecurFormatted
                            numberOfWeeks = recurr_diff.days // 7

                            #Find Recurring Date Difference
                            hour_diff = endFormatted - startFormatted
                            numOfSessionHours = hour_diff
                            print(numOfSessionHours)



                            userSlot = UserPreferenceSlot.objects.create(start_time=start_time, end_time=end_time, start_recurring=start_recurring, end_recurring=end_recurring, computer_slot=availableSlot, student=studentObj)
                            userSlot.save()
                            userSlotSerializer = serializers.UserPreferenceSlotSerializer(userSlot, many=False)


                            computerReservationsList = []
                            #Make Reccurring Object Creation Logic
                            #Create the inital day of reservation
                            newComputerReserve = ComputerReservation.objects.create(start_time=start_time, end_time=end_time, reserved_slot=userSlot, student=studentObj, computer=selectedComputer, transaction_id=uuid.uuid4())
                            newComputerReserve.save()
                            computerReservationsList.append(newComputerReserve)

                            #Create the temporary computer reservation objects
                            date_tmp = startRecurFormatted
                            for week in range(0, numberOfWeeks):
                                print("Computer Reservation Created")
                                new_start_date = date_tmp + timedelta(days=7)
                                date_tmp = new_start_date
                                new_start_date_object = datetime(new_start_date.year, new_start_date.month, new_start_date.day, startFormatted.hour, startFormatted.minute)
                                new_end_date_object = datetime(new_start_date.year, new_start_date.month, new_start_date.day, endFormatted.hour, endFormatted.minute)
                                print(new_start_date_object)
                                print(new_end_date_object)
                                formattedStartDate =  new_start_date_object.strftime('%Y/%m/%d')
                                formattedEndDate = new_end_date_object.strftime('%Y/%m/%d')
                                print(formattedStartDate)
                                print(formattedEndDate)

                                newComputerReserve = ComputerReservation.objects.create(start_time=new_start_date_object, end_time=new_end_date_object, reserved_slot=userSlot, student=studentObj, computer=selectedComputer, transaction_id=uuid.uuid4())
                                newComputerReserve.save()
                                computerReservationsList.append(newComputerReserve)


                            computerReserveSerializer = serializers.ComputerReservationSerializer(computerReservationsList, many=True)
                            print(computerReserveSerializer.data)

                        else:
                            userSlot = UserPreferenceSlot.objects.create(start_time=start_time, end_time=end_time, computer_slot=availableSlot, student=studentObj)
                            userSlot.save()
                            userSlotSerializer = serializers.UserPreferenceSlotSerializer(userSlot, many=False)

                            newComputerReserve = ComputerReservation.objects.create(start_time=start_time, end_time=end_time, reserved_slot=userSlot, student=studentObj, computer=selectedComputer, transaction_id=uuid.uuid4())
                            newComputerReserve.save()
                            computerReserveSerializer = serializers.ComputerReservationSerializer(newComputerReserve, many=False)
                            print(computerReserveSerializer.data)


                return Response(userSlotSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, uniqueID) -> Response:
            serializer = serializers.UpdateUserPreferenceSlotSerializer(data=request.data)
            userSlot = {}
            reservations = []
            if uniqueID == "" or uniqueID == None:
                    return Response({"error": "Provided uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    userSlot = UserPreferenceSlot.objects.get(uniqueID=uniqueID)
                except UserPreferenceSlot.DoesNotExist:
                    return Response({"error": "UserPreferenceSlot with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    print(userSlot.computer_slot)
                    availableSlot = LibraryComputerSlots.objects.get(pk=userSlot.computer_slot.pk)
                except LibraryComputerSlots.DoesNotExist:
                    return Response({"error": "LibraryComputerSlot with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)


                try:
                    reservations = ComputerReservation.objects.filter(reserved_slot=userSlot.pk)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "ComputerReservation with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                if serializer.is_valid():
                    student = serializer.validated_data["student"]
                    mentor = serializer.validated_data["mentor"]
                    start_time = serializer.validated_data["start_time"]
                    end_time = serializer.validated_data["end_time"]
                    start_recurring = serializer.validated_data["start_recurring"]
                    end_recurring = serializer.validated_data["end_recurring"]

                    student = None
                    mentor = None
                    start_recurring = None
                    end_recurring = None

                    try:
                        start_time = serializer.validated_data["start_time"]
                        end_time = serializer.validated_data["end_time"]
                        userSlot.start_time = start_time
                        userSlot.end_time = end_time
                    except KeyError:
                        start_time = None
                        end_time = None


                    try:
                        start_recurring = serializer.validated_data["start_recurring"]
                        end_recurring = serializer.validated_data["end_recurring"]
                    except KeyError:
                        start_recurring = None
                        end_recurring = None


                    try:
                        student = serializer.validated_data["student"]
                    except KeyError:
                        student = None

                    try:
                        mentor = serializer.validated_data["mentor"]
                    except KeyError:
                        mentor = None


                    if student:
                        student = User.objects.get(pk=student)
                        userSlot.student = student

                    if mentor:
                        mentor = User.objects.get(pk=mentor)
                        userSlot.mentor = mentor

                        if len(reservations) == 0:
                            print('No reservations or mentor')

                            try:
                                studentObj = student
                            except User.DoesNotExist:
                                return Response({"error": "User with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)


                            try:
                                availableComputers = Computer.objects.filter(library=availableSlot.library)
                            except Computer.DoesNotExist:
                                return Response({"error": "Computers with that provided Computer Slot could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                            if len(availableComputers) == 0:
                                return Response({"error": "No Computers available to reserve."}, status=status.HTTP_400_BAD_REQUEST)

                            allComputersID = []

                            for computer in availableComputers:
                                allComputersID.append(computer.pk)

                            try:
                                allComputersReservations = ComputerReservation.objects.filter(start_time=start_time, end_time=end_time, computer__in=allComputersID)
                            except ComputerReservation.DoesNotExist:
                                return Response({"error": "ComputerReservations with that provided timeslot taken already."}, status=status.HTTP_400_BAD_REQUEST)

                            #userSlot = None
                            userSlotSerializer = {}

                            directorEmail = 'mentor@villagebookbuilders.org'
                            username = studentObj.first_name + ' ' + studentObj.last_name


                            start = userSlot.start_time.strftime('%Y-%m-%dT%H:%M:%S')
                            end = userSlot.end_time.strftime('%Y-%m-%dT%H:%M:%S')
                            conferenceLink = generateCalendarEvent(username, mentor.email, directorEmail, start, end, mentor.email)
                            print(conferenceLink)

                            link = conferenceLink["link"]
                            id = conferenceLink["id"]

                            if len(allComputersReservations) == 0:
                                #Create Multiple  Computer Reservations if Reccurring
                                if start_recurring != None and end_recurring != None:

                                    startSplit = start_time
                                    startTz = start_time.split('T')[1]

                                    endSplit = end_time
                                    endTz = end_time.split('T')[1]

                                    startRecSplit = start_recurring.split('T')[0]
                                    startRecTz = start_recurring.split('T')[1]

                                    endRecSplit = end_recurring.split('T')[0]
                                    endRecTz = end_recurring.split('T')[1]

                                    startRecurFormatted = datetime.strptime(startRecSplit, '%Y-%m-%d')
                                    endRecurFormatted = datetime.strptime(endRecSplit, '%Y-%m-%d')

                                    startFormatted = datetime.strptime(startSplit, '%Y-%m-%dT%H:%M:%S%fZ')
                                    endFormatted = datetime.strptime(endSplit, '%Y-%m-%dT%H:%M:%S%fZ')

                                    print(startFormatted)
                                    print(endFormatted)

                                    #Find Recurring Date Difference
                                    recurr_diff = endRecurFormatted - startRecurFormatted
                                    numberOfWeeks = recurr_diff.days // 7

                                    #Find Recurring Date Difference
                                    hour_diff = endFormatted - startFormatted
                                    numOfSessionHours = hour_diff
                                    print(numOfSessionHours)

                                    computerReservationsList = []
                                    #Make Reccurring Object Creation Logic
                                    #Create the inital day of reservation
                                    newComputerReserve = ComputerReservation.objects.create(start_time=start_time, end_time=end_time, reserved_slot=userSlot, student=studentObj, mentor=mentor, computer=availableComputers[0], transaction_id=uuid.uuid4(), conferenceURL=link, meetingID=id)
                                    newComputerReserve.save()
                                    computerReservationsList.append(newComputerReserve)

                                    #Create the temporary computer reservation objects
                                    date_tmp = startRecurFormatted
                                    for week in range(0, numberOfWeeks):
                                        print("Computer Reservation Created")
                                        new_start_date = date_tmp + timedelta(days=7)
                                        date_tmp = new_start_date
                                        new_start_date_object = datetime(new_start_date.year, new_start_date.month, new_start_date.day, startFormatted.hour, startFormatted.minute)
                                        new_end_date_object = datetime(new_start_date.year, new_start_date.month, new_start_date.day, endFormatted.hour, endFormatted.minute)
                                        print(new_start_date_object)
                                        print(new_end_date_object)
                                        formattedStartDate =  new_start_date_object.strftime('%Y/%m/%d')
                                        formattedEndDate = new_end_date_object.strftime('%Y/%m/%d')
                                        print(formattedStartDate)
                                        print(formattedEndDate)

                                        newComputerReserve = ComputerReservation.objects.create(start_time=new_start_date_object, end_time=new_end_date_object, reserved_slot=userSlot, student=studentObj, mentor=mentor, computer=availableComputers[0], transaction_id=uuid.uuid4(), conferenceURL=link, meetingID=id)
                                        newComputerReserve.save()
                                        computerReservationsList.append(newComputerReserve)


                                    computerReserveSerializer = serializers.ComputerReservationSerializer(computerReservationsList, many=True)
                                    print(computerReserveSerializer.data)

                                else:
                                    #Create Single Reservation Object
                                    newComputerReserve = ComputerReservation.objects.create(start_time=start_time, end_time=end_time, reserved_slot=userSlot, student=studentObj, mentor=mentor, computer=availableComputers[0], transaction_id=uuid.uuid4(), conferenceURL=link, meetingID=id)
                                    newComputerReserve.save()
                                    computerReserveSerializer = serializers.ComputerReservationSerializer(newComputerReserve, many=False)
                                    print(computerReserveSerializer.data)
                            else:
                                reservedComputers = []
                                freeComputers = []

                                for computer in allComputersReservations:
                                    reservedComputers.append(computer.computer.pk)
                                print(reservedComputers)

                                for comp in allComputersID:
                                    if comp not in reservedComputers:
                                        freeComputers.append(comp)

                                print(freeComputers)
                                print("Reservations with computers found at this time")

                                if len(freeComputers) <= 0:
                                    return Response({"error": "No free computers at this time."}, status=status.HTTP_400_BAD_REQUEST)
                                else:
                                    selectedComputer = Computer.objects.get(pk=freeComputers[0])
                                    if start_recurring != None and end_recurring != None:

                                        startSplit = start_time
                                        startTz = start_time.split('T')[1]

                                        endSplit = end_time
                                        endTz = end_time.split('T')[1]

                                        startRecSplit = start_recurring.split('T')[0]
                                        startRecTz = start_recurring.split('T')[1]

                                        endRecSplit = end_recurring.split('T')[0]
                                        endRecTz = end_recurring.split('T')[1]

                                        startRecurFormatted = datetime.strptime(startRecSplit, '%Y-%m-%d')
                                        endRecurFormatted = datetime.strptime(endRecSplit, '%Y-%m-%d')

                                        startFormatted = datetime.strptime(startSplit, '%Y-%m-%dT%H:%M:%S%fZ')
                                        endFormatted = datetime.strptime(endSplit, '%Y-%m-%dT%H:%M:%S%fZ')

                                        print(startFormatted)
                                        print(endFormatted)

                                        #Find Recurring Date Difference
                                        recurr_diff = endRecurFormatted - startRecurFormatted
                                        numberOfWeeks = recurr_diff.days // 7

                                        #Find Recurring Date Difference
                                        hour_diff = endFormatted - startFormatted
                                        numOfSessionHours = hour_diff
                                        print(numOfSessionHours)

                                        computerReservationsList = []
                                        #Make Reccurring Object Creation Logic
                                        #Create the inital day of reservation
                                        newComputerReserve = ComputerReservation.objects.create(start_time=start_time, end_time=end_time, reserved_slot=userSlot, mentor=mentor, student=studentObj, computer=selectedComputer, transaction_id=uuid.uuid4(), conferenceURL=link, meetingID=id)
                                        newComputerReserve.save()
                                        computerReservationsList.append(newComputerReserve)

                                        #Create the temporary computer reservation objects
                                        date_tmp = startRecurFormatted
                                        for week in range(0, numberOfWeeks):
                                            print("Computer Reservation Created")
                                            new_start_date = date_tmp + timedelta(days=7)
                                            date_tmp = new_start_date
                                            new_start_date_object = datetime(new_start_date.year, new_start_date.month, new_start_date.day, startFormatted.hour, startFormatted.minute)
                                            new_end_date_object = datetime(new_start_date.year, new_start_date.month, new_start_date.day, endFormatted.hour, endFormatted.minute)
                                            print(new_start_date_object)
                                            print(new_end_date_object)
                                            formattedStartDate =  new_start_date_object.strftime('%Y/%m/%d')
                                            formattedEndDate = new_end_date_object.strftime('%Y/%m/%d')
                                            print(formattedStartDate)
                                            print(formattedEndDate)

                                            newComputerReserve = ComputerReservation.objects.create(start_time=new_start_date_object, end_time=new_end_date_object, reserved_slot=userSlot, student=studentObj, mentor=mentor, computer=selectedComputer, transaction_id=uuid.uuid4(), conferenceURL=link, meetingID=id)
                                            newComputerReserve.save()
                                            computerReservationsList.append(newComputerReserve)


                                        computerReserveSerializer = serializers.ComputerReservationSerializer(computerReservationsList, many=True)
                                        print(computerReserveSerializer.data)

                                    else:
                                        newComputerReserve = ComputerReservation.objects.create(start_time=start_time, end_time=end_time, reserved_slot=userSlot, student=studentObj, mentor=mentor, computer=selectedComputer, transaction_id=uuid.uuid4(), conferenceURL=link, meetingID=id)
                                        newComputerReserve.save()
                                        computerReserveSerializer = serializers.ComputerReservationSerializer(newComputerReserve, many=False)
                                        print(computerReserveSerializer.data)


                    if start_time:
                        userSlot.start_time = start_time

                    if end_time:
                        userSlot.end_time = end_time

                    if start_recurring:
                        userSlot.start_recurring = start_recurring

                    if end_recurring:
                        userSlot.end_recurring = end_recurring


                    userSlot.save()

                    if mentor:
                        for resev in reservations:
                            resev.mentor = mentor
                            resev.save()
                            print(resev)

                    userSlotSerializer = serializers.UserPreferenceSlotSerializer(userSlot, many=False)
                    return Response(userSlotSerializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, uniqueID) -> Response:
            if uniqueID:
                userSlot = {}
                try:
                    userSlot = UserPreferenceSlot.objects.get(uniqueID=uniqueID)
                except UserPreferenceSlot.DoesNotExist:
                    return Response({"error": "User Preference Slot with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                #Delete Computer Reservation
                try:
                    reservations = ComputerReservation.objects.filter(reserved_slot=userSlot.pk)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "ComputerReservation with that provided slot could not be found."}, status=status.HTTP_404_NOT_FOUND)

                reservations.delete()
                userSlot.delete()

                return Response({"msg":"User Preference Slot deleted successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "User Preference Slot uniqueID needs to be provided."}, status=status.HTTP_400_BAD_REQUEST)


class ComputerViews(APIView):
    """All Computer Reservations Views"""
    #
    # authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # # add admin permission levels
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
            serializer = serializers.CreateComputerSerializer(data=request.data)
            lib = None
            if serializer.is_valid():
                library = serializer.validated_data["library"]
                name = serializer.validated_data["name"]
                key = serializer.validated_data["key"]
                ip_address = serializer.validated_data["ip_address"]
                notes = serializer.validated_data["notes"]

                try:
                    lib = Library.objects.get(pk=library)
                except User.DoesNotExist:
                    return Response({"error": "User with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                computer = Computer.objects.create(library=lib, name=name, key=key, ip_address=ip_address, notes=notes)
                computer.save()
                computerSerializer = serializers.ComputerSerializer(computer, many=False)
                return Response(computerSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, uniqueID) -> Response:
            serializer = serializers.UpdateComputerSerializer(data=request.data)
            computer = {}
            reservations = []
            if uniqueID == "" or uniqueID == None:
                    return Response({"error": "Provided uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    computer = Computer.objects.get(uniqueID=uniqueID)
                except UserPreferenceSlot.DoesNotExist:
                    return Response({"error": "Computer with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                if serializer.is_valid():
                    name = serializer.validated_data["name"]
                    key = serializer.validated_data["key"]
                    ip_address = serializer.validated_data["ip_address"]
                    notes = serializer.validated_data["notes"]
                    is_down = serializer.validated_data["is_down"]
                    email = serializer.validated_data["email"]

                    name = None
                    key = None
                    ip_address = None
                    notes = None
                    is_down = None
                    email = None

                    try:
                        name = serializer.validated_data["name"]
                    except KeyError:
                        name = None

                    try:
                        key = serializer.validated_data["key"]
                    except KeyError:
                        key = None

                    try:
                        email = serializer.validated_data["email"]
                    except KeyError:
                        email = None

                    try:
                        ip_address = serializer.validated_data["ip_address"]
                    except KeyError:
                        ip_address = None

                    try:
                        notes = serializer.validated_data["notes"]
                    except KeyError:
                        notes = None

                    try:
                        is_down = serializer.validated_data["is_down"]
                    except KeyError:
                        is_down = None



                    if name:
                        computer.name = name

                    if key:
                        computer.key = key

                    if ip_address:
                        computer.ip_address = ip_address

                    if notes:
                        computer.notes = notes

                    if is_down:
                        computer.is_down = is_down

                    if email:
                        computer.email = email

                    computer.save()


                    compSerializer = serializers.ComputerSerializer(computer, many=False)
                    return Response(compSerializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, uniqueID) -> Response:
            if uniqueID:
                computer = {}
                try:
                    computer = Computer.objects.get(uniqueID=uniqueID)
                except Computer.DoesNotExist:
                    return Response({"error": "Computer with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                computer.delete()

                return Response({"msg":"Computer deleted successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Computer uniqueID needs to be provided."}, status=status.HTTP_400_BAD_REQUEST)


class ComputerReservationViews(APIView):
    """All Computer Reservations Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        userId = request.user.pk

        if userId == "" or userId == None:
                return Response({"error": "Provided userId cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        userSlots = None
        user = None

        try:
            user = User.objects.get(pk=userId)
        except User.DoesNotExist:
            return Response({"error": "User with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            if user.is_student == True:
                userSlots = ComputerReservation.objects.filter(student=user.pk)
            elif user.is_mentor == True:
                userSlots = ComputerReservation.objects.filter(mentor=user.pk)
            else:
                return Response({"error": "User must be a mentor or student to make a reservation slot."}, status=status.HTTP_400_BAD_REQUEST)

        except ComputerReservation.DoesNotExist:
            return Response({"error": "No reservation slots with this userId could be found."}, status=status.HTTP_400_BAD_REQUEST)

        userSlotsSerializer = serializers.ComputerReservationWithUserSerializer(userSlots, many=True)
        return Response(userSlotsSerializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request) -> Response:
            serializer = serializers.CreateComputerReservationSerializer(data=request.data)
            if serializer.is_valid():
                student = serializer.validated_data["student"]
                mentor = serializer.validated_data["mentor"]
                reserved_slot = serializer.validated_data["reserved_slot"]
                computer = serializer.validated_data["computer"]
                start_time = serializer.validated_data["start_time"]
                end_time = serializer.validated_data["end_time"]
                start_recurring = serializer.validated_data["start_recurring"]
                end_recurring = serializer.validated_data["end_recurring"]
                is_recurring = serializer.validated_data["is_recurring"]
                transcript_file = serializer.validated_data["transcript_file"]
                existingSlot = {}

                try:
                    existingSlot = ComputerReservation.objects.get(start_time=start_time, end_time=end_time, computer=computer)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "ComputerReservation with this timeslot and computer already exists."}, status=status.HTTP_400_BAD_REQUEST)

                computerReservation = ComputerReservation.objects.create(**serializer.validated_data)
                computerReservation.save()
                computerReservationSerializer = serializers.ComputerReservationSerializer(computerReservation, many=False)
                return Response(computerReservationSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request) -> Response:
            serializer = serializers.UpdateComputerReservationSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["unique_id"]

                try:
                    computerReservation = ComputerReservation.objects.get(uniqueID=uniqueID)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "ComputerReservation with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                computerSlotSerializer = serializers.ComputerReservationSerializer(computerReservation, data=request.data, partial=True)
                if computerSlotSerializer.is_valid():
                    student_attended = serializer.validated_data.get('student_attended')
                    mentor_attended = serializer.validated_data.get('mentor_attended')
                    start_time = computerReservation.start_time
                    current_date = timezone.now()
                    #print(start_time)
                    #print(current_date)
                    time_diff = start_time - current_date
                    #print(time_diff)
                    if student_attended or mentor_attended:
                        if time_diff < timedelta(hours=1):
                            print("time_diff < 1 hour")
                            computerSlotSerializer.save()
                            return Response(computerSlotSerializer.data, status=status.HTTP_200_OK)
                        else:
                            print("time_diff > 1 hour")
                            return Response({"message": "ComputerReservation attendence could not be updated."}, status=status.HTTP_200_OK)
                    else:
                        computerSlotSerializer.save()
                        return Response(computerSlotSerializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "ComputerReservation could not be updated."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
            serializer = serializers.UpdateComputerReservationSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                computerReservation = {}

                try:
                    computerReservation = ComputerReservation.objects.get(uniqueID=uniqueID)
                except ComputerReservation .DoesNotExist:
                    return Response({"error": "ComputerReservation with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                computerReservation.delete()
                return Response({"msg":"ComputerReservation deleted successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BookComputerReservationViews(APIView):
    """All Computer Reservations Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
            print(request.data)
            serializer = serializers.UpdateComputerReservationSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["unique_id"]
                mentor = serializer.validated_data["mentor"]
                conferenceType = serializer.validated_data["conference_type"]
                start_time = serializer.validated_data["start_time"]
                end_time = serializer.validated_data["end_time"]

                #notes = serializer.validated_data["notes"]

                # meetingID = serializer.validated_data["meetingID"]
                # conferenceURL = serializer.validated_data["conferenceURL"]
                # reserve_status = serializer.validated_data["reserve_status"]
                # mentor_attended = serializer.validated_data["mentor_attended"]
                # student_attended = serializer.validated_data["student_attended"]

                computerReservation = {}


                try:
                    mentorUser = User.objects.get(pk=mentor)
                except User.DoesNotExist:
                    return Response({"error": "User with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)


                try:
                    mentorProfile = MentorProfile.objects.get(user=mentorUser.pk)
                except MentorProfile.DoesNotExist:
                    return Response({"error": "Mentor Profile with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                if mentorProfile.approval_status != "Approved":
                    return Response({"error": "You have not been approved to book sessions. Please wait unil we've approved your profile."}, status=status.HTTP_400_BAD_REQUEST)


                try:
                    userPreferenceSlot = UserPreferenceSlot.objects.get(uniqueID=uniqueID)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "UserPreferenceSlot with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)


                userPreferenceSlot.mentor = mentorUser
                userPreferenceSlot.save()

                studentUser = userPreferenceSlot.student

                try:
                    existingComputerReservation = ComputerReservation.objects.filter(start_time=start_time, end_time=end_time, mentor=mentor)

                    if existingComputerReservation:
                        return Response({"error": "This mentor already has a booked session at this time."}, status=status.HTTP_400_BAD_REQUEST)

                except Exception:
                    return Response({"error": "Server error occured"}, status=status.HTTP_400_BAD_REQUEST)


                try:
                    activeComputerReservations = ComputerReservation.objects.filter(reserved_slot=userPreferenceSlot.pk)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "ComputerReservation for this prefence slot could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                directorEmail = 'mentor@villagebookbuilders.org'
                username = studentUser.first_name + ' ' + studentUser.last_name


                start = userPreferenceSlot.start_time.strftime('%Y-%m-%dT%H:%M:%S')
                end = userPreferenceSlot.end_time.strftime('%Y-%m-%dT%H:%M:%S')
                conferenceLink = generateCalendarEvent(username, mentorUser.email, directorEmail, start, end, mentorUser.email)
                print(conferenceLink)

                link = conferenceLink["link"]
                id = conferenceLink["id"]

                for reserve in activeComputerReservations:
                    reserve.mentor = mentorUser
                    reserve.conferenceURL = link
                    reserve.meetingID = id
                    reserve.save()

                #Generate Meeting URLS
                #computerReservation.meetingID = meetingID
                #computerReservation.conferenceURL = conferenceURL
                #computerReservation.reserve_status = reserve_status


                computerSlotSerializer = serializers.ComputerReservationWithUserSerializer(activeComputerReservations, many=True)
                return Response(computerSlotSerializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LibraryMentorViews(APIView):
    """All Computer Reservations Views"""
    #
    # authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # # add admin permission levels
    # permission_classes = [permissions.IsAuthenticated]

    # def patch(self, request: Request, uniqueID) -> Response:
    #         serializer = serializers.UpdateComputerSerializer(data=request.data)
    #         computer = {}
    #         reservations = []
    #         if uniqueID == "" or uniqueID == None:
    #                 return Response({"error": "Provided uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             try:
    #                 computer = Computer.objects.get(uniqueID=uniqueID)
    #             except UserPreferenceSlot.DoesNotExist:
    #                 return Response({"error": "Computer with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #             if serializer.is_valid():
    #                 name = serializer.validated_data["name"]
    #                 key = serializer.validated_data["key"]
    #                 ip_address = serializer.validated_data["ip_address"]
    #                 notes = serializer.validated_data["notes"]
    #                 is_down = serializer.validated_data["is_down"]
    #                 email = serializer.validated_data["email"]
    #
    #                 name = None
    #                 key = None
    #                 ip_address = None
    #                 notes = None
    #                 is_down = None
    #                 email = None
    #
    #                 try:
    #                     name = serializer.validated_data["name"]
    #                 except KeyError:
    #                     name = None
    #
    #                 try:
    #                     key = serializer.validated_data["key"]
    #                 except KeyError:
    #                     key = None
    #
    #                 try:
    #                     email = serializer.validated_data["email"]
    #                 except KeyError:
    #                     email = None
    #
    #                 try:
    #                     ip_address = serializer.validated_data["ip_address"]
    #                 except KeyError:
    #                     ip_address = None
    #
    #                 try:
    #                     notes = serializer.validated_data["notes"]
    #                 except KeyError:
    #                     notes = None
    #
    #                 try:
    #                     is_down = serializer.validated_data["is_down"]
    #                 except KeyError:
    #                     is_down = None
    #
    #
    #
    #                 if name:
    #                     computer.name = name
    #
    #                 if key:
    #                     computer.key = key
    #
    #                 if ip_address:
    #                     computer.ip_address = ip_address
    #
    #                 if notes:
    #                     computer.notes = notes
    #
    #                 if is_down:
    #                     computer.is_down = is_down
    #
    #                 if email:
    #                     computer.email = email
    #
    #                 computer.save()
    #
    #
    #                 compSerializer = serializers.ComputerSerializer(computer, many=False)
    #                 return Response(compSerializer.data, status=status.HTTP_200_OK)
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id) -> Response:
            if id:
                user = {}
                prof = {}
                try:
                    user = User.objects.get(pk=id)
                except User.DoesNotExist:
                    return Response({"error": "User with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                try:
                    prof = MentorProfile.objects.get(user=user)
                except MentorProfile.DoesNotExist:
                    return Response({"error": "MentorProfile with that provided id could not be found."}, status=status.HTTP_404_NOT_FOUND)

                user.delete()
                prof.delete()

                return Response({"msg":"User removed successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "User ID needs to be provided."}, status=status.HTTP_400_BAD_REQUEST)


class LibraryStudentViews(APIView):
    """All Computer Reservations Views"""
    #
    # authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # # add admin permission levels
    # permission_classes = [permissions.IsAuthenticated]

    # def patch(self, request: Request, uniqueID) -> Response:
    #         serializer = serializers.UpdateComputerSerializer(data=request.data)
    #         computer = {}
    #         reservations = []
    #         if uniqueID == "" or uniqueID == None:
    #                 return Response({"error": "Provided uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             try:
    #                 computer = Computer.objects.get(uniqueID=uniqueID)
    #             except UserPreferenceSlot.DoesNotExist:
    #                 return Response({"error": "Computer with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #             if serializer.is_valid():
    #                 name = serializer.validated_data["name"]
    #                 key = serializer.validated_data["key"]
    #                 ip_address = serializer.validated_data["ip_address"]
    #                 notes = serializer.validated_data["notes"]
    #                 is_down = serializer.validated_data["is_down"]
    #                 email = serializer.validated_data["email"]
    #
    #                 name = None
    #                 key = None
    #                 ip_address = None
    #                 notes = None
    #                 is_down = None
    #                 email = None
    #
    #                 try:
    #                     name = serializer.validated_data["name"]
    #                 except KeyError:
    #                     name = None
    #
    #                 try:
    #                     key = serializer.validated_data["key"]
    #                 except KeyError:
    #                     key = None
    #
    #                 try:
    #                     email = serializer.validated_data["email"]
    #                 except KeyError:
    #                     email = None
    #
    #                 try:
    #                     ip_address = serializer.validated_data["ip_address"]
    #                 except KeyError:
    #                     ip_address = None
    #
    #                 try:
    #                     notes = serializer.validated_data["notes"]
    #                 except KeyError:
    #                     notes = None
    #
    #                 try:
    #                     is_down = serializer.validated_data["is_down"]
    #                 except KeyError:
    #                     is_down = None
    #
    #
    #
    #                 if name:
    #                     computer.name = name
    #
    #                 if key:
    #                     computer.key = key
    #
    #                 if ip_address:
    #                     computer.ip_address = ip_address
    #
    #                 if notes:
    #                     computer.notes = notes
    #
    #                 if is_down:
    #                     computer.is_down = is_down
    #
    #                 if email:
    #                     computer.email = email
    #
    #                 computer.save()
    #
    #
    #                 compSerializer = serializers.ComputerSerializer(computer, many=False)
    #                 return Response(compSerializer.data, status=status.HTTP_200_OK)
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id) -> Response:
            if id:
                user = {}
                prof = {}
                try:
                    user = User.objects.get(pk=id)
                except User.DoesNotExist:
                    return Response({"error": "User with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                try:
                    prof = StudentProfile.objects.get(user=user)
                except StudentProfile.DoesNotExist:
                    return Response({"error": "StudentProfile with that provided id could not be found."}, status=status.HTTP_404_NOT_FOUND)

                user.delete()
                prof.delete()

                return Response({"msg":"User removed successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "User ID needs to be provided."}, status=status.HTTP_400_BAD_REQUEST)


class LibraryComputerReservationViews(APIView):
    """All Computer Reservations Views"""
    #
    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication, JWTAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request: Request, uniqueID) -> Response:
            serializer = serializers.UpdateComputerReservationSerializer(data=request.data)
            reservation = {}
            if uniqueID == "" or uniqueID == None:
                    return Response({"error": "Provided uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    reservation = ComputerReservation.objects.get(uniqueID=uniqueID)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "ComputerReservation with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                if serializer.is_valid():
                    # name = serializer.validated_data["name"]
                    # mentor = serializer.validated_data["mentor"]
                    # computer = serializer.validated_data["computer"]
                    # start_time = serializer.validated_data["start_time"]
                    # end_time = serializer.validated_data["end_time"]
                    # conferenceURL = serializer.validated_data["conferenceURL"]
                    #
                    # name = None
                    mentor = None
                    computer = None
                    start_time = None
                    end_time = None
                    conferenceURL = None

                    # try:
                    #     name = serializer.validated_data["name"]
                    # except KeyError:
                    #     name = None
                    #
                    try:
                        mentor = serializer.validated_data["mentor"]
                    except KeyError:
                        mentor = None

                    try:
                        computer = serializer.validated_data["computer"]
                    except KeyError:
                        computer = None

                    try:
                        start_time = serializer.validated_data["start_time"]
                        end_time = serializer.validated_data["end_time"]
                    except KeyError:
                        start_time = None
                        end_time = None

                    try:
                        conferenceURL = serializer.validated_data["conferenceURL"]
                    except KeyError:
                        conferenceURL = None



                    # if name:
                    #     computer.name = name

                    if mentor:

                        try:
                            mentorUser = User.objects.get(pk=mentor)
                        except User.DoesNotExist:
                            return Response({"error": "User with that provided id could not be found."}, status=status.HTTP_404_NOT_FOUND)

                        reservation.mentor = mentorUser

                    if computer:


                        try:
                            computerAssigned = Computer.objects.get(pk=computer)
                        except User.DoesNotExist:
                            return Response({"error": "Computer with that provided id could not be found."}, status=status.HTTP_404_NOT_FOUND)

                        reservation.computer = computerAssigned

                    if start_time:
                        reservation.start_time = start_time

                    if end_time:
                        reservation.end_time = end_time

                    if conferenceURL:
                        reservation.conferenceURL = conferenceURL

                    reservation.save()


                    compReserveSerializer = serializers.ComputerReservationWithUserSerializer(reservation, many=False)
                    return Response(compReserveSerializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, uniqueID) -> Response:
            if uniqueID:
                reservation = {}
                try:
                    reservation = ComputerReservation.objects.get(uniqueID=uniqueID)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "ComputerReservation with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                reservation.delete()

                return Response({"msg":"ComputerReservation removed successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "UniqueID of computer reservation needs to be provided."}, status=status.HTTP_400_BAD_REQUEST)
