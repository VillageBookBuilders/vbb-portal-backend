from rest_framework import serializers

from vbb.announcements.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            "text",
            "id",
            "start_date",
            "end_date",
        ]
