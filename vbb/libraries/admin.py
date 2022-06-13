from django.contrib import admin
from .models import Library, Computer, LibraryComputerSlots, UserPreferenceSlot, ComputerReservation, Announcement

# Register your models here.
admin.site.register(Library)
admin.site.register(Computer)
admin.site.register(LibraryComputerSlots)
admin.site.register(UserPreferenceSlot)
admin.site.register(ComputerReservation)
admin.site.register(Announcement)
