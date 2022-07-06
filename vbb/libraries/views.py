from typing import Optional

from rest_framework import permissions, status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from vbb.users.models import User

from vbb.libraries.models import Library, LibraryComputerSlots, UserPreferenceSlot, Computer, ComputerReservation
from vbb.libraries.serializers import LibrarySerializer, LibraryWithComputersSerializer
from vbb.utils.custom_csrf import CsrfHTTPOnlySessionAuthentication
from vbb.libraries import serializers
import uuid
from datetime import datetime, timedelta

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

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = serializers.RetieveAnnouncementSerializer(data=request.data)
        library = serializer.validated_data["library"]

        if library == "" or library == None:
                return Response({"error": "Provided library ID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        libraryObj = {}

        try:
            libraryObj = Library.objects.get(text=text)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        allAnnouncements = Announcement.objects.get(library=libraryObj.pk)

        if allAnnouncements == None:
            return Response({"error": "Server error occurred."}, status=status.HTTP_400_BAD_REQUEST)

        announcmentSerializer = serializers.AnnouncementSerializer(allAnnouncements, many=True)
        return Response(announcmentSerializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request) -> Response:
            serializer = serializers.CreateAnnouncementSerializer(data=request.data)
            if serializer.is_valid():
                text = serializer.validated_data["text"]
                display_start = serializer.validated_data["display_start"]
                display_end = serializer.validated_data["display_end"]
                library = serializer.validated_data["library"]
                notes = serializer.validated_data["notes"]

                announcment = {}
                try:
                    announcment = Announcement.objects.get(text=text)
                except Announcement.DoesNotExist:
                    announcment = Announcement.objects.create(**serializer.validated_data)
                    announcment.save()

                    announcmentSerializer = serializers.AnnouncementSerializer(announcment, many=False)
                    return Response(announcmentSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request) -> Response:
            serializer = serializers.UpdateAnnouncementSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
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

    def delete(self, request: Request) -> Response:
            serializer = serializers.UpdateAnnouncementSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                try:
                    announcment = Announcement.objects.get(uniqueID=uniqueID)
                except Announcement.DoesNotExist:
                    return Response({"error": "Announcement with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                announcment.delete()
                return Response({"msg":"Announcement deleted successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComputerViews(APIView):
    """All Computer Related Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = serializers.RetieveComputersSerializer(data=request.data)
        uniqueID = serializer.validated_data["uniqueID"]

        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided library uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        computerObjs = None
        library = None

        try:
            library = Library.objects.get(uniqueID=uniqueID)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            computerObjs = Computer.objects.get(library=library.pk)
        except Computer.DoesNotExist:
            return Response({"error": "No computers with that library could be found."}, status=status.HTTP_400_BAD_REQUEST)

        computerSerializer = serializers.ComputerSerializer(computerObjs, many=True)
        return Response(computerSerializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request) -> Response:
            serializer = serializers.CreateComputerSerializer(data=request.data)
            if serializer.is_valid():
                name = serializer.validated_data["name"]
                key = serializer.validated_data["key"]
                mac_address = serializer.validated_data["mac_address"]
                ip_address = serializer.validated_data["ip_address"]
                library = serializer.validated_data["library"]
                notes = serializer.validated_data["notes"]

                try:
                    library = Library.objects.get(pk=library)
                except Library.DoesNotExist:
                    return Response({"error": "Library with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                computer = {}

                computer = Computer.objects.create(**serializer.validated_data)
                computer.save()
                computerSerializer = serializers.ComputerSerializer(computer, many=False)
                return Response(computerSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request) -> Response:
            serializer = serializers.UpdateComputerSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                name = serializer.validated_data["name"]
                key = serializer.validated_data["key"]
                mac_address = serializer.validated_data["mac_address"]
                ip_address = serializer.validated_data["ip_address"]
                library = serializer.validated_data["library"]
                notes = serializer.validated_data["notes"]

                computer = {}

                try:
                    computer = Computer.objects.get(uniqueID=uniqueID)
                except Computer.DoesNotExist:
                    return Response({"error": "Computer with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                computer.name = name
                computer.key = key
                computer.mac_address = mac_address
                computer.ip_address = ip_address
                computer.library = library
                computer.notes = notes
                computer.save()

                computerSerializer = serializers.ComputerSerializer(computer, many=False)
                return Response(computerSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
            serializer = serializers.UpdateComputerSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                computer = {}

                try:
                    computer = Computer.objects.get(uniqueID=uniqueID)
                except Computer.DoesNotExist:
                    return Response({"error": "Computer with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                computer.delete()
                return Response({"msg":"Computer deleted successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibraryComputerSlotViews(APIView):
    """All Computer Related Views"""
    # add admin permission levels
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
                start_time = serializer.validated_data["start_time"]
                end_time = serializer.validated_data["end_time"]
                start_recurring = serializer.validated_data["start_recurring"]
                end_recurring = serializer.validated_data["end_recurring"]
                day = serializer.validated_data["day"]
                library = serializer.validated_data["library"]

                try:
                    library = Library.objects.get(pk=library)
                except Library.DoesNotExist:
                    return Response({"error": "Library with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                #Add existting time range slot exception

                libSlot = {}

                libSlot = LibraryComputerSlots.objects.create(**serializer.validated_data)
                libSlot.save()
                libSlotSerializer = serializers.LibrarySlotSerializer(libSlot, many=False)
                return Response(libSlotSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request) -> Response:
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

    def delete(self, request: Request) -> Response:
            serializer = serializers.UpdateLibrarySlotSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                libSlot = {}

                try:
                    libSlot = LibraryComputerSlots.objects.get(uniqueID=uniqueID)
                except LibraryComputerSlots.DoesNotExist:
                    return Response({"error": "Library Slot with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                libSlot.delete()
                return Response({"msg":"Library Slot deleted successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveLibraryStudentPreferencesViews(APIView):
    """All User Preference Slot Views"""

    #authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
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
                    userSlots = UserPreferenceSlot.objects.filter(computer_slot__in=libSlotIDs)
                except UserPreferenceSlot.DoesNotExist:
                    return Response({"error": "User Preference Slots with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                userSlotsSerializer = serializers.UserPreferenceSlotSerializer(userSlots, many=True)
                return Response(userSlotsSerializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Library uniqueID needs to be provided."}, status=status.HTTP_400_BAD_REQUEST)


class UserPreferenceSlotViews(APIView):
    """All User Preference Slot Views"""

    #authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
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


                studentObj = None

                try:
                    studentObj = User.objects.get(pk=int(student))
                except User.DoesNotExist:
                    return Response({"error": "User with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)


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
                except Computers.DoesNotExist:
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
                    return Response({"error": "ComputerReservation with that provided Computer Slot could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                print(allComputersID)
                print(allComputersReservations)


                #Add existting time range slot exception
                userSlot = None
                userSlotSerializer = {}

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

                        userSlot = UserPreferenceSlot.objects.create(start_time=start_time, end_time=end_time, start_recurring=start_recurring, end_recurring=end_recurring, computer_slot=availableSlot, student=studentObj)
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

    def patch(self, request: Request) -> Response:
            serializer = serializers.UpdateUserPreferenceSlotSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                student = serializer.validated_data["student"]
                mentor = serializer.validated_data["mentor"]
                lib_computer_slot = serializer.validated_data["lib_computer_slot"]
                start_time = serializer.validated_data["start_time"]
                end_time = serializer.validated_data["end_time"]
                start_recurring = serializer.validated_data["start_recurring"]
                end_recurring = serializer.validated_data["end_recurring"]

                userSlot = {}

                try:
                    userSlot = UserPreferenceSlot.objects.get(pk=computer_slot)
                except UserPreferenceSlot.DoesNotExist:
                    return Response({"error": "UserPreferenceSlot with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                userSlot.student = student
                userSlot.mentor = mentor
                userSlot.lib_computer_slot = lib_computer_slot
                userSlot.start_time = start_time
                userSlot.end_time = end_time
                userSlot.start_recurring = start_recurring
                userSlot.end_recurring = end_recurring

                userSlot.save()

                userSlotSerializer = serializers.UserPreferenceSlotSerializer(userSlot, many=False)
                return Response(userSlotSerializer.data, status=status.HTTP_200_OK)
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





class ComputerReservationViews(APIView):
    """All Computer Reservations Views"""

    #authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
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
            serializer = serializers.UpdateUserPreferenceSlotSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                student = serializer.validated_data["student"]
                mentor = serializer.validated_data["mentor"]
                reserved_slot = serializer.validated_data["reserved_slot"]
                start_time = serializer.validated_data["start_time"]
                end_time = serializer.validated_data["end_time"]
                start_recurring = serializer.validated_data["start_recurring"]
                end_recurring = serializer.validated_data["end_recurring"]
                is_recurring = serializer.validated_data["is_recurring"]
                transcript_file = serializer.validated_data["transcript_file"]

                meetingID = serializer.validated_data["meetingID"]
                conferenceURL = serializer.validated_data["conferenceURL"]
                reserve_status = serializer.validated_data["reserve_status"]
                mentor_attended = serializer.validated_data["mentor_attended"]
                student_attended = serializer.validated_data["student_attended"]

                computerReservation = {}

                try:
                    computerReservation = ComputerReservation.objects.get(pk=computer_slot)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "ComputerReservation with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                computerReservation.student = student
                computerReservation.mentor = mentor
                computerReservation.reserved_slot = reserved_slot
                computerReservation.computer = computer
                computerReservation.start_time = start_time
                computerReservation.end_time = end_time
                computerReservation.start_recurring = start_recurring
                computerReservation.end_recurring = end_recurring
                computerReservation.is_recurring = is_recurring
                computerReservation.transcript_file = transcript_file
                computerReservation.meetingID = meetingID
                computerReservation.conferenceURL = conferenceURL
                computerReservation.reserve_status = reserve_status
                computerReservation.mentor_attended = mentor_attended
                computerReservation.student_attended = student_attended

                computerReservation.save()

                computerSlotSerializer = serializers.ComputerReservationSerializer(computerReservation, many=False)
                return Response(computerSlotSerializer.data, status=status.HTTP_200_OK)
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

    #authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
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
                    userPreferenceSlot = UserPreferenceSlot.objects.get(uniqueID=uniqueID)
                except ComputerReservation.DoesNotExist:
                    return Response({"error": "UserPreferenceSlot with that provided uniqueID could not be found."}, status=status.HTTP_400_BAD_REQUEST)


                userPreferenceSlot.mentor = mentorUser
                userPreferenceSlot.save()

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


                for reserve in activeComputerReservations:
                    reserve.mentor = mentorUser
                    reserve.save()

                #Generate Meeting URLS
                #computerReservation.meetingID = meetingID
                #computerReservation.conferenceURL = conferenceURL
                #computerReservation.reserve_status = reserve_status


                computerSlotSerializer = serializers.ComputerReservationWithUserSerializer(activeComputerReservations, many=True)
                return Response(computerSlotSerializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
