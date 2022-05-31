from datetime import timedelta

from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
)

from vbb.meetings.api.serializers.computer import ComputerSerializer
from vbb.meetings.models import Computer, Slot


class SlotSerializer(ModelSerializer):

    computer = PrimaryKeyRelatedField(queryset=Computer.objects.all(), required=True)
    computer_object = ComputerSerializer(source="computer", read_only=True)

    start_day_of_the_week = IntegerField(required=True)
    end_day_of_the_week = IntegerField(required=True)
    start_hour = IntegerField(required=True)
    end_hour = IntegerField(required=True)
    start_minute = IntegerField(required=True)
    end_minute = IntegerField(required=True)

    def validate(self, attrs):
        self.start_time = Slot.DEAFULT_INIT_DATE + timedelta(
            days=attrs.pop("start_day_of_the_week"),
            hours=attrs.pop("start_hour"),
            minutes=attrs.pop("start_minute"),
        )
        self.end_time = Slot.DEAFULT_INIT_DATE + timedelta(
            days=attrs.pop("end_day_of_the_week"),
            hours=attrs.pop("end_hour"),
            minutes=attrs.pop("end_minute"),
        )
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["schedule_start"] = self.start_time
        validated_data["schedule_end"] = self.end_time

        return super().create(validated_data)

    class Meta:
        model = Slot
        exclude = ["schedule_start", "schedule_end"]
