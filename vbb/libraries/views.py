from typing import Optional

from rest_framework import permissions, status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vbb.libraries.models import Library
from vbb.libraries.serializers import LibrarySerializer, LibraryWithComputersSerializer
from vbb.utils.custom_csrf import CsrfHTTPOnlySessionAuthentication

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

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = serializers.RetieveLibrarySlotSerializer(data=request.data)
        uniqueID = serializer.validated_data["uniqueID"]

        if uniqueID == "" or uniqueID == None:
                return Response({"error": "Provided library uniqueID cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        librarySlots = None
        library = None

        try:
            library = Library.objects.get(uniqueID=uniqueID)
        except Computer.DoesNotExist:
            return Response({"error": "Library with that provided uniuqeID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            librarySlots = LibraryComputerSlots.objects.get(library=library.pk)
        except LibraryComputerSlots.DoesNotExist:
            return Response({"error": "No computer slots with this library could be found."}, status=status.HTTP_400_BAD_REQUEST)

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

class UserPreferenceSlotViews(APIView):
    """All User Preference Slot Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = serializers.RetieveUserPreferenceSlotSerializer(data=request.data)
        userId = serializer.validated_data["userId"]

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
                userSlots = UserPreferenceSlot.objects.get(student=user.pk)
            elif user.is_mentor == True:
                userSlots = UserPreferenceSlot.objects.get(mentor=user.pk)
            else:
                return Response({"error": "User must be a mentor or student to make a preference slot."}, status=status.HTTP_400_BAD_REQUEST)

        except UserPreferenceSlot.DoesNotExist:
            return Response({"error": "No user slots with this userId could be found."}, status=status.HTTP_400_BAD_REQUEST)

        userSlotsSerializer = serializers.UserPreferenceSlotSerializer(userSlots, many=True)
        return Response(userSlotsSerializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request) -> Response:
            serializer = serializers.CreateUserPreferenceSlotSerializer(data=request.data)
            if serializer.is_valid():
                student = serializer.validated_data["student"]
                mentor = serializer.validated_data["mentor"]
                computer_slot = serializer.validated_data["computer_slot"]
                start_time = serializer.validated_data["start_time"]
                end_time = serializer.validated_data["end_time"]
                start_recurring = serializer.validated_data["start_recurring"]
                end_recurring = serializer.validated_data["end_recurring"]

                availableSlot = {}

                try:
                    availableSlot = LibraryComputerSlots.objects.get(pk=computer_slot)
                except LibraryComputerSlots.DoesNotExist:
                    return Response({"error": "LibraryComputerSlot with that provided id could not be found."}, status=status.HTTP_400_BAD_REQUEST)

                #Add existting time range slot exception
                userSlot = UserPreferenceSlot.objects.create(**serializer.validated_data)
                userSlot.save()
                userSlotSerializer = serializers.UserPreferenceSlotSerializer(userSlot, many=False)
                return Response(userSlotSerializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request) -> Response:
            serializer = serializers.UpdateUserPreferenceSlotSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                student = serializer.validated_data["student"]
                mentor = serializer.validated_data["mentor"]
                computer_slot = serializer.validated_data["computer_slot"]
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
                userSlot.computer_slot = computer_slot
                userSlot.start_time = start_time
                userSlot.end_time = end_time
                userSlot.start_recurring = start_recurring
                userSlot.end_recurring = end_recurring

                userSlot.save()

                userSlotSerializer = serializers.UserPreferenceSlotSerializer(userSlot, many=False)
                return Response(userSlotSerializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
            serializer = serializers.UpdateUserPreferenceSlotSerializer(data=request.data)
            if serializer.is_valid():
                uniqueID = serializer.validated_data["uniqueID"]
                userSlot = {}

                try:
                    userSlot = UserPreferenceSlot.objects.get(uniqueID=uniqueID)
                except UserPreferenceSlot.DoesNotExist:
                    return Response({"error": "User Preference Slot with that provided uniqueID could not be found."}, status=status.HTTP_404_NOT_FOUND)

                userSlot.delete()
                return Response({"msg":"User Preference Slot deleted successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComputerReservationViews(APIView):
    """All Computer Reservations Views"""

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
    # add admin permission levels
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = serializers.RetieveUserPreferenceSlotSerializer(data=request.data)
        userId = serializer.validated_data["userId"]

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
                userSlots = UserPreferenceSlot.objects.get(student=user.pk)
            elif user.is_mentor == True:
                userSlots = UserPreferenceSlot.objects.get(mentor=user.pk)
            else:
                return Response({"error": "User must be a mentor or student to make a preference slot."}, status=status.HTTP_400_BAD_REQUEST)

        except UserPreferenceSlot.DoesNotExist:
            return Response({"error": "No user slots with this userId could be found."}, status=status.HTTP_400_BAD_REQUEST)

        userSlotsSerializer = serializers.UserPreferenceSlotSerializer(userSlots, many=True)
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
                computer = serializer.validated_data["computer"]
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
