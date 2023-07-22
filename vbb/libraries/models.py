from django.db import models
import uuid
from django.utils import timezone
from django.conf import settings

DAYS = ((0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'))
STATUS =  ((0, 'Upcoming'), (1, 'In Session'), (2, 'Completed'), (3, 'Cancelled'), (4, 'Other'))
LIB_STATUS =  ((0, 'active'), (1, 'inactive'), (2, 'closed'))


class Library(models.Model):
    """
    Library site under VBB
    """
    uniqueID = models.UUIDField(max_length=1024, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    #announcements = models.CharField(max_length=255)  #nix
    is_accepting_new_mentors = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    library_code = models.CharField(max_length=255, unique=True, null=True)
    status = models.IntegerField(choices=LIB_STATUS, null=False, default=0)
    address_1 = models.CharField(max_length=255, null=True, blank=True)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state_province = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    poBoxNumber = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    """
    Announcements under VBB
    """
    uniqueID = models.UUIDField(max_length=1024, default=uuid.uuid4, editable=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    display_start = models.DateTimeField(default=None, blank=True, null=True)
    display_end = models.DateTimeField(default=None, blank=True, null=True)
    library = models.ForeignKey(Library, null=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text

class Computer(models.Model):
    """
    Computer model under VBB
    """
    uniqueID = models.UUIDField(max_length=1024, default=uuid.uuid4, editable=False)
    library = models.ForeignKey(Library, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=1024)
    mac_address = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    is_reserved = models.BooleanField(default=False)
    is_down = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

class LibraryComputerSlots(models.Model):
    uniqueID = models.UUIDField(max_length=1024, default=uuid.uuid4, editable=False)
    library = models.ForeignKey(Library, null=True, on_delete=models.SET_NULL)
    day = models.IntegerField(choices=DAYS, null=False, default=0)
    start_time = models.DateTimeField(default=None, blank=True, null=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)
    start_recurring = models.DateTimeField(default=None, blank=True, null=True)
    end_recurring = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        #return str(self.uniqueID) + str(self.day) + str(self.id)
        return "%s %s %s" % (self.library.name, DAYS[self.day][1], self.start_time)

    class Meta:
        verbose_name = "Library Computer Slots"

class UserPreferenceSlot(models.Model):
    uniqueID = models.UUIDField(max_length=1024, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,  blank=True, on_delete=models.SET_NULL, related_name='preference_student')
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,  blank=True, on_delete=models.SET_NULL, related_name='preference_mentor')
    computer_slot = models.ForeignKey(LibraryComputerSlots, null=True, on_delete=models.SET_NULL, related_name='preference_slot')
    start_time = models.DateTimeField(default=None, blank=True, null=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)
    start_recurring = models.DateTimeField(default=None, blank=True, null=True)
    end_recurring = models.DateTimeField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    conference_type = models.CharField(max_length=1024, null=True, blank=True, default="google")

    def __str__(self):
        return str(self.uniqueID)

    class Meta:
        verbose_name = "Preference Slots"

#Day OF mODEL
class ComputerReservation(models.Model):
    uniqueID = models.UUIDField(max_length=1024, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    reserved_slot = models.ForeignKey(UserPreferenceSlot, on_delete=models.CASCADE)
    reserved_date = models.DateTimeField(auto_now_add=True)
    reserve_status = models.IntegerField(choices=STATUS, null=True, default=0)
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,  blank=True, on_delete=models.SET_NULL, related_name='reservation_mentor')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,  blank=True, on_delete=models.SET_NULL, related_name='reservation_student')
    computer = models.ForeignKey(Computer, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
    start_time = models.DateTimeField(default=None, blank=True, null=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    student_attended = models.BooleanField(default=False)
    student_attended_time = models.DateTimeField(default=None, blank=True, null=True)
    mentor_attended = models.BooleanField(default=False)
    mentor_attended_time = models.DateTimeField(default=None, blank=True, null=True)

    #start_recurring = models.DateTimeField(default=None, blank=True, null=True)
    #end_recurring = models.DateTimeField(default=None, blank=True, null=True)
    transcript_file = models.CharField(max_length=255,  null=True, blank=True)
    meetingID = models.CharField(max_length=255, null=True, blank=True)
    conferenceURL = models.CharField(max_length=1024, null=True, blank=True)


    class Meta:
        verbose_name = "ComputerReservation"

    def save(self, *args, **kwargs):
        if not self.mentor_attended_time and self.mentor_attended:
            self.mentor_attended_time = timezone.now()
        if not self.student_attended_time and self.student_attended:
            self.student_attended_time = timezone.now()

        super(ComputerReservation, self).save(*args, **kwargs)
