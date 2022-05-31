import enum
from datetime import datetime, timedelta, timezone

import pytz
from django.db import models
from rest_framework.exceptions import ValidationError

from vbb.utils.models.base import BaseUUIDModel


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


# NOTE this should be a relationship to the Language Model list
class LanguageEnum(enum.Enum):
    ENGLISH = "ENGLISH"
    SPANISH = "SPANISH"
    VIETNAMESE = "VIETNAMSE"
    TAGALOG = "TAGALOG"
    HINDI = "HINDI"


# NOTE this should be a relationship to the Language Model list
LanguageChoices = [(e.value, e.name) for e in LanguageEnum]


# NOTE The concept of a Program has been replaced by Library.
# This model fields may need to be transferred to the Library or deleted entirely
class Program(BaseUUIDModel):
    """
    This model represents a VBB village mentoring program
    Users that have foreign keys back to Program:
        ??? Program Director ???
        Student (through School)
    Teacher (through School)
        Mentor (through Slot)
        Mentor Advisor (many to many through a relation table)
    Models that have foreign keys back to Program:
        Slot (through Computer?)
        School
        Library
        Computer (?)
    """

    # primary information
    name = models.CharField(max_length=40, blank=False)
    time_zone = models.CharField(max_length=32, choices=TIMEZONES)
    # todo add field type = models.ForeignKey(ContentType)
    # types include excellent, good, poor, gov/low-fee, special status
    latitude = models.DecimalField(max_digits=8, decimal_places=3)
    longitude = models.DecimalField(max_digits=8, decimal_places=3)
    program_director = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True
    )
    # headmasters = models.ManyToManyField("users.User", through="HeadmastersProgramAssociation")
    # teachers = models.ManyToManyField("users.User", through="TeachersProgramAssociation")
    # managers = models.ManyToManyField("users.User", through="ManagersProgramAssociation")
    # todo add access control for 54-56
    program_inception_date = models.DateTimeField(
        null=True, blank=True
    )  # offical start date
    program_renewal_date = models.DateTimeField(
        null=True, blank=True
    )  # yearly program renual before trips should be made
    # NOTE this should likely be mentoring lanaguage although this
    # responsability has been moved to the student and then mentor languages
    required_languages = models.CharField(
        max_length=254, choices=LanguageChoices, default=None, null=True
    )
    secondary_languages = models.CharField(
        max_length=254, choices=LanguageChoices, default=None, null=True
    )

    # calender key for scheduling
    googe_calendar_id = models.CharField(max_length=254, null=True)

    # communication tools
    facebook_group = models.CharField(max_length=254, null=True, blank=True)
    whatsapp_group = models.CharField(max_length=254, null=True)
    mentor_announcements = models.CharField(max_length=254, null=True, blank=True)
    mentor_collaboration = models.CharField(max_length=254, null=True, blank=True)
    students_group = models.CharField(max_length=254, null=True, blank=True)
    parents_group = models.CharField(max_length=254, null=True, blank=True)

    # program specific resources
    notion_url = models.URLField(
        max_length=500, null=True, blank=True, help_text="url link"
    )
    googleDrive_url = models.URLField(
        max_length=500, null=True, blank=True, help_text="url link"
    )
    googleClassroom_url = models.URLField(
        max_length=500, null=True, blank=True, help_text="url link"
    )
    workplace_resources = models.URLField(
        max_length=500, null=True, blank=True, help_text="url link"
    )
    program_googlePhotos = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text="url link to google drive program photo folder",
    )

    # local village culture information
    program_googlePhotos = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text="url link to google drive program photo folder",
    )
    # todo figure out a better way to store, cache, or link, different types of photos
    village_info_link = models.CharField(max_length=500, null=True, blank=True)
    village_chief = models.CharField(max_length=254, null=True, blank=True)
    chief_contact = models.CharField(max_length=254, null=True, blank=True)
    ministry_education_contact = models.TextField(null=True, blank=True)
    notes = models.TextField(
        help_text="comments, suggestions, notes, events, open-house dates,\
            mentor program break dates, internet connectivity, power avalibility,\
            state of infrastructure, etc",
        null=True,
        blank=True,
    )


class Computer(BaseUUIDModel):
    """
    This Model Represents a Computer in a VBB Mentor Program that can host mentoring slots
    """

    # NOTE 'Program' has been replaced by 'Library'
    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
    )
    computer_number = models.IntegerField(null=True)
    computer_email = models.EmailField(max_length=70, null=True)
    room_id = models.CharField(max_length=100, null=True)
    notes = models.TextField(null=True, blank=True)

    computer_model = models.CharField(max_length=100, null=True, blank=True)
    manufactured_date = models.TextField(null=True, blank=True)
    mp_start_date = models.TextField(null=True, blank=True)
    # estimate renewal date
    harward_specifications = models.TextField(null=True, blank=True)
    computer_issues = models.TextField(null=True, blank=True)
    has_headphones = models.BooleanField(default=False)
    headphone_specs = models.TextField(null=True, blank=True)
    wifi_connectivityInfo = models.TextField(null=True, blank=True)
    software_Notes = models.TextField(null=True, blank=True)

    """"
    connection to andriodx86, etc, remote control etc, add as needed.
    ? again not sure what sure what information should we stored and what should just be static ?
    """

    def __str__(self):
        return (
            f"{str(self.program)} {str(self.computer_number)} + ({self.computer_email})"
        )


class Slot(BaseUUIDModel):
    """
    This Model Represents a slot that the mentor program decides to have with one of its computers,
    **eg , a slot can be for a Computer A for firday 10AM to friday 12AM**
    The slot is not editable, once the slot is to be updated the model object has to be deleted and recreated
    The slot object has no starting time or ending time, slots made are run throughout the year,
    to cancel a slot the slot has to be deleted
    The slot can be of any duration less than 24 hours
    the slot start and end refer to the start and end of a session in the slot,
    we are only concerned with the day of the week and the time , so month and year does not make a difference
    the slot will be assigned to a mentor, which connects the mentor app and the program app
    """

    # Default Min date not used as this can cause issues in some databases and systems
    DEAFULT_INIT_DATE = datetime.fromisoformat(
        "2000-01-03 00:00:00"
    )  # First Monday of the year 2000
    # DO NOT CHANGE THE DEFAULT INIT DATE | USED FOR EASE OF USE
    slot_number = models.IntegerField(null=True, blank=True)
    # ? should we have a way to ID the slots across computers or programs? like an index to help admins find slots?
    # todo remove computer model as in the apis we can make implicit associations exlicit in apis
    # is the following implicitly stored
    computer = models.ForeignKey(
        Computer,
        on_delete=models.PROTECT,
        null=True,
    )
    # NOTE Language is now part of the User object.
    language = models.CharField(max_length=254, choices=LanguageChoices)
    schedule_start = models.DateTimeField(
        null=False, blank=False
    )  # All Date Times in UTC
    schedule_end = models.DateTimeField(
        null=False, blank=False
    )  # All Date Times are in UTC
    start_date = models.DateField(auto_now=True)  # When the slot becomes active
    end_date = models.DateField(null=True, blank=True)  # if and when the slot ends
    event_id = models.CharField(max_length=60, null=True, blank=True)
    meeting_link = models.CharField(max_length=60, null=True, blank=True)
    max_students = models.IntegerField(default=1)
    assigned_students = models.IntegerField(
        default=0
    )  # Storing to avoid recalculation each time
    is_mentor_assigned = models.BooleanField(default=False)
    is_student_assigned = models.BooleanField(default=False)

    students = models.ManyToManyField(
        "users.User", through="StudentSlotAssociation", related_name="slot_mentors"
    )
    # NOTE current understanding is that a SLOT can only have one mentor and one
    # student at any given time
    mentors = models.ManyToManyField(
        "users.User", through="MentorSlotAssociation", related_name="slot_students"
    )

    @staticmethod
    def get_slot_time(day, hour, minute):
        slot_time = Slot.DEAFULT_INIT_DATE + timedelta(
            days=int(day), hours=int(hour), minutes=int(minute)
        )
        return slot_time.replace(tzinfo=timezone.utc)

    def save(self, *args, **kwargs):

        if Slot.objects.filter(
            computer=self.computer,
            schedule_end__gt=self.schedule_start,
            schedule_start__lt=self.schedule_end,
        ).exists():
            raise ValidationError({"schedule": "Conflict Found"})

        return super().save(*args, **kwargs)

    def start_day_of_the_week(self):
        return self.schedule_start.date().weekday()

    def end_day_of_the_week(self):
        return self.schedule_end.date().weekday()

    def start_hour(self):
        return self.schedule_start.hour

    def end_hour(self):
        return self.schedule_end.hour

    def start_minute(self):
        return self.schedule_start.minute

    def end_minute(self):
        return self.schedule_end.minute


class StudentSlotAssociation(BaseUUIDModel):
    """
    This connects the student user object with a Slot Object
    """

    student = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="student_slot",
    )
    slot = models.ForeignKey(
        Slot, on_delete=models.SET_NULL, null=True, related_name="slot_student"
    )
    priority = models.IntegerField(default=0)  # 0 is the highest priority

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "slot"],
                condition=models.Q(deleted=False),
                name="unique_student_slot_pair",
            ),
        ]


class MentorSlotAssociation(BaseUUIDModel):
    """
    This connects the student user object with a Slot Object
    """

    mentor = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="mentor_slot"
    )
    slot = models.ForeignKey(
        Slot, on_delete=models.SET_NULL, null=True, related_name="slot_mentor"
    )
    priority = models.IntegerField(default=0)  # 0 is the highest priority
    is_confirmed = models.BooleanField(
        default=False
    )  # This is only editable by the program director or above

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mentor", "slot"],
                condition=models.Q(deleted=False),
                name="unique_mentor_slot_pair",
            ),
        ]


class Session(BaseUUIDModel):
    """
    This Model represents the sessions history and the next upcoming session for mentors.
    An Asyncronous task will populate the required sessions from the SessionRule
    """

    slot = models.ForeignKey(
        Slot, on_delete=models.SET_NULL, null=True
    )  # Represents the Connected Slot

    computer = models.ForeignKey(Computer, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField()  # All Date Times in UTC
    end = models.DateTimeField()  # All Date Times in UTC
    students = models.ManyToManyField(
        "users.User",
        through="StudentSessionAssociation",
        related_name="session_students",
    )
    mentors = models.ManyToManyField(
        "users.User", through="MentorSessionAssociation", related_name="session_mentors"
    )

    isHappening = models.BooleanField(default=False)

    infrastructure_notes = models.TextField(
        default=None, help_text="Power, wifi, audio quality?", null=True, blank=True
    )
    mentorAdvisor_notes = models.TextField(default=None, null=True, blank=True)
    headmaster_notes = models.TextField(default=None, null=True, blank=True)
    teacher_notes = models.TextField(default=None, null=True, blank=True)
    parent_notes = models.TextField(default=None, null=True, blank=True)
    student_notes = models.TextField(default=None, null=True, blank=True)
    mentee_notes = models.TextField(default=None, null=True, blank=True)
    otherNotes = models.TextField(default=None, null=True, blank=True)
    # @varun we need to know which user can edit which fields

    agenda = models.TextField(default=None, null=True, blank=True)
    # figure out the ideal mentor mentee format and use of notion + journaling, if mentoring was a
    # therapy intervetion, what are different formats? how does that play into the resources we are using?

    def save(self, *args, **kwargs):
        # TODO Need to ensure that only one session exists per day
        pass


class StudentSessionAssociation(BaseUUIDModel):
    """
    This connects the student user object with a Session Object
    """

    student = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="student_session",
    )
    session = models.ForeignKey(
        Session, on_delete=models.SET_NULL, null=True, related_name="session_student"
    )
    attended = models.BooleanField(default=False)
    mentoring_notes = models.TextField(default=None, null=True, blank=True)
    # todo subject/class field and a computer field stating which computer the session is part of

    delay_notes = models.BooleanField(default=False)
    # warnings, risks, complexities etc. make this a type variable? issue_warning
    # need to figure out user workflow + story for session warning + communication @sarthak
    # if its easy for people to communicate over email or slack, there should be a simple way
    # for mentors & mentees to communicate wether or not they are coming, the answer could be attendance,
    # phones, parents, librian, idk but people should not need to wait
    # alert 30 minutes if mentee does not show, for mentors to leave, if problem repeats for 3 times in
    # a row with power/internet/issues, then alert libraian and figure out a way to keep mentor engaged
    # in the process sarthak, we need to figure this out soon
    warnings = models.TextField(default=None, null=True, blank=True)
    issues = models.TextField(default=None, null=True, blank=True)
    feedback = models.TextField(default=None, null=True, blank=True)


class MentorSessionAssociation(BaseUUIDModel):
    """
    This connects the student user object with a Session Object
    """

    mentor = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="mentor_session",
    )
    session = models.ForeignKey(
        Session, on_delete=models.SET_NULL, null=True, related_name="session_mentor"
    )
    attended = models.BooleanField(default=False)
    mentoring_notes = models.TextField(default=None, null=True, blank=True)
    # todo subject/class field and a computer field stating which computer the session is part of

    delay_notes = models.BooleanField(default=False)
    # warnings, risks, complexities etc. make this a type variable? issue_warning
    # need to figure out user workflow + story for session warning + communication @sarthak
    # if its easy for people to communicate over email or slack, there should be a simple
    # way for mentors & mentees to communicate wether or not they are coming, the answer
    # could be attendance, phones, parents, librian, idk but people should not need to wait
    # alert 30 minutes if mentee does not show, for mentors to leave, if problem repeats for
    # 3 times in a row with power/internet/issues, then alert libraian and figure out a way
    # to keep mentor engaged in the process sarthak, we need to figure this out soon
    warnings = models.TextField(default=None, null=True, blank=True)
    issues = models.TextField(default=None, null=True, blank=True)
    feedback = models.TextField(default=None, null=True, blank=True)
