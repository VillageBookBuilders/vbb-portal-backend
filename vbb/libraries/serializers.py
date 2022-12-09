from rest_framework import serializers

from vbb.libraries.models import Library, Computer, LibraryComputerSlots, UserPreferenceSlot, ComputerReservation, Announcement
from vbb.users.models import User
#
#
class ReservationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["first_name", "last_name", "profileImage", "id", "username", "email", "is_student", "is_mentor"]

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields="__all__"
        # fields = [
        #     "announcements",
        #     "id",
        #     "is_accepting_new_mentors",
        #     "name",
        # ]


class LibraryWithComputersSerializer(serializers.ModelSerializer):
    """Should also include all of the slot and session data"""

    class Meta:
        model = Library
        fields="__all__"
        # fields = [
        #     "announcements",
        #     "id",
        #     "is_accepting_new_mentors",
        #     "name",
        # ]

class LibraryWithComputersSerializer(serializers.ModelSerializer):
    """Should also include all of the slot and session data"""

    class Meta:
        model = Library
        fields="__all__"


class CreateLibrarySerializer(serializers.Serializer):
    is_accepting_new_mentors = serializers.BooleanField(required=False)
    name = serializers.CharField(required=True, max_length=2048)
    library_code = serializers.CharField(required=True, max_length=2048)
    address_1 = serializers.CharField(required=False, max_length=2048)
    address_2 = serializers.CharField(required=False, max_length=1024)
    city = serializers.CharField(required=False, max_length=1024)
    state_province = serializers.CharField(required=False, max_length=1024)
    postal_code = serializers.CharField(required=False, max_length=1024)
    poBoxNumber = serializers.CharField(required=False, max_length=1024)
    country = serializers.CharField(required=False, max_length=1024)
    notes = serializers.CharField(required=False, max_length=1024)


class UpdateLibrarySerializer(serializers.Serializer):
    uniqueID = serializers.CharField(required=True, max_length=1024)
    is_accepting_new_mentors = serializers.BooleanField(required=False)
    name = serializers.CharField(required=False, max_length=2048)
    library_code = serializers.CharField(required=False, max_length=2048)
    address_1 = serializers.CharField(required=False, max_length=2048)
    address_2 = serializers.CharField(required=False, max_length=1024)
    city = serializers.CharField(required=False, max_length=1024)
    state_province = serializers.CharField(required=False, max_length=1024)
    postal_code = serializers.CharField(required=False, max_length=1024)
    poBoxNumber = serializers.CharField(required=False, max_length=1024)
    country = serializers.CharField(required=False, max_length=1024)
    notes = serializers.CharField(required=False, max_length=1024)

'''
Announcment Serializers
'''

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields="__all__"

        # fields = [
        #     "announcements",
        #     "id",
        #     "is_accepting_new_mentors",
        #     "name",
        # ]

class RetieveAnnouncementSerializer(serializers.Serializer):
    """Get all announcements given library"""
    library = serializers.IntegerField(required=True)

class CreateAnnouncementSerializer(serializers.Serializer):
    display_start = serializers.CharField(required=True, max_length=1024)
    display_end = serializers.CharField(required=True, max_length=1024)
    library = serializers.CharField(required=True)
    text = serializers.CharField(required=True, max_length=2048)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=2048)

class UpdateAnnouncementSerializer(serializers.Serializer):
    display_start = serializers.CharField(required=False, max_length=1024)
    display_end = serializers.CharField(required=False, max_length=1024)
    text = serializers.CharField(required=False, max_length=2048)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=2048)

'''
Computer Serializers
'''

class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields="__all__"
        # fields = [
        #     "announcements",
        #     "id",
        #     "is_accepting_new_mentors",
        #     "name",
        # ]

class RetieveComputersSerializer(serializers.Serializer):
    """Get all computers given library"""
    uniqueID = serializers.CharField(required=True, max_length=2048)

class CreateComputerSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=2048)
    key = serializers.CharField(required=False, allow_blank=True, max_length=2048)
    email = serializers.CharField(required=False, allow_blank=True, max_length=2048)
    mac_address = serializers.CharField(required=False, allow_blank=True, max_length=2048)
    ip_address = serializers.CharField(required=False, allow_blank=True, max_length=1024)
    library = serializers.IntegerField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=2048)

class UpdateComputerSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=2048)
    key = serializers.CharField(required=False, max_length=2048)
    email = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=2048)
    mac_address = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=2048)
    ip_address = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=1024)
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=2048)
    is_down = serializers.BooleanField(required=False)

'''
Library Slot Serializers
'''
class LibrarySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryComputerSlots
        fields = '__all__'
        # fields = [
        #     "announcements",
        #     "id",
        #     "is_accepting_new_mentors",
        #     "name",
        # ]
class RetieveLibrarySlotSerializer(serializers.Serializer):
    """Get a particular library slot given library"""
    uniqueID = serializers.CharField(required=True, max_length=2048)

class CreateLibrarySlotSerializer(serializers.Serializer):
    start_time = serializers.CharField(required=True, max_length=1024)
    end_time = serializers.CharField(required=True, max_length=1024)
    start_recurring = serializers.CharField(required=False, max_length=1024)
    end_recurring = serializers.CharField(required=False, max_length=1024)
    day = serializers.IntegerField(required=True)
    library = serializers.CharField(required=False, max_length=1024)

class UpdateLibrarySlotSerializer(serializers.Serializer):
    uniqueID = serializers.CharField(required=True, max_length=1024)
    start_time = serializers.CharField(required=False, max_length=1024)
    end_time = serializers.CharField(required=False, max_length=1024)
    start_recurring = serializers.CharField(required=False, max_length=1024)
    end_recurring = serializers.CharField(required=False, max_length=1024)
    day = serializers.IntegerField(required=False)
    library = serializers.IntegerField(required=False)

'''
UserPreferenceSlot Serializers
'''
class UserPreferenceSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferenceSlot
        fields = '__all__'
        # fields = [
        #     "announcements",
        #     "id",
        #     "is_accepting_new_mentors",
        #     "name",
        # ]

class UserPreferenceSlotWithUsersSerializer(serializers.ModelSerializer):

    student = ReservationUserSerializer(many=False)
    mentor = ReservationUserSerializer(many=False)

    class Meta:
        model = UserPreferenceSlot
        fields = '__all__'
        # fields = [
        #     "announcements",
        #     "id",
        #     "is_accepting_new_mentors",
        #     "name",
        # ]

class RetieveUserPreferenceSlotSerializer(serializers.Serializer):
    """Get a list user preference slots given userId"""
    userId = serializers.IntegerField(required=True)


class CreateUserPreferenceSlotSerializer(serializers.Serializer):
    student = serializers.IntegerField(required=False)
    mentor = serializers.IntegerField(required=False)
    lib_computer_slot = serializers.CharField(required=True)
    conference_type = serializers.CharField(required=True)
    start_time = serializers.CharField(required=True, max_length=1024)
    end_time = serializers.CharField(required=True, max_length=1024)
    start_recurring = serializers.CharField(required=False, max_length=1024)
    end_recurring = serializers.CharField(required=False, max_length=1024)
    is_recurring = serializers.CharField(required=False, max_length=1024)


class UpdateUserPreferenceSlotSerializer(serializers.Serializer):
    student = serializers.IntegerField(required=False, allow_null=True)
    mentor = serializers.IntegerField(required=False, allow_null=True)
    lib_computer_slot = serializers.CharField(required=False)
    start_time = serializers.CharField(required=False, max_length=1024)
    end_time = serializers.CharField(required=False, max_length=1024)
    start_recurring = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=1024)
    end_recurring = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=1024)
    conference_type = serializers.CharField(required=False, max_length=1024, allow_null=True, allow_blank=True)


'''
ComputerReservation Serializers
'''
class ComputerReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerReservation
        fields = '__all__'
        # fields = [
        #     "announcements",
        #     "id",
        #     "is_accepting_new_mentors",
        #     "name",
        # ]

class ComputerReservationWithUserSerializer(serializers.ModelSerializer):

    student = ReservationUserSerializer(many=False)
    mentor = ReservationUserSerializer(many=False)
    computer = ComputerSerializer(many=False)

    class Meta:
        model = ComputerReservation
        fields = '__all__'

class CreateComputerReservationSerializer(serializers.Serializer):
    student = serializers.IntegerField(required=True)
    mentor = serializers.IntegerField(required=True)
    reserved_slot = serializers.IntegerField(required=True)
    computer = serializers.IntegerField(required=True)
    start_time = serializers.CharField(required=True, max_length=1024)
    end_time = serializers.CharField(required=True, max_length=1024)
    start_recurring = serializers.CharField(required=False, max_length=1024)
    end_recurring = serializers.CharField(required=False, max_length=1024)
    transaction_id = serializers.CharField(required=False, max_length=1024)
    is_recurring = serializers.BooleanField(required=True)
    transcript_file = serializers.CharField(required=False, max_length=1024)


class UpdateComputerReservationSerializer(serializers.Serializer):
    unique_id = serializers.CharField(required=False, max_length=1024)
    student = serializers.IntegerField(required=False, allow_null=True)
    mentor = serializers.IntegerField(required=False, allow_null=True)
    computer = serializers.IntegerField(required=False, allow_null=True)
    start_time = serializers.CharField(required=False, max_length=1024)
    end_time = serializers.CharField(required=False, max_length=1024)
    transaction_id = serializers.CharField(required=False, max_length=1024, allow_null=True)
    student_attended = serializers.BooleanField(required=False)
    mentor_attended = serializers.BooleanField(required=False)
    reserve_status = serializers.IntegerField(required=False)
    transcript_file = serializers.CharField(required=False, max_length=1024, allow_null=True, allow_blank=True)
    meetingID = serializers.CharField(required=False, max_length=1024, allow_null=True, allow_blank=True)
    conferenceURL = serializers.CharField(required=False, max_length=1024, allow_null=True, allow_blank=True)
    conference_type = serializers.CharField(required=False, max_length=1024, allow_null=True, allow_blank=True)
    #notes = serializers.CharField(required=False, max_length=1024)
