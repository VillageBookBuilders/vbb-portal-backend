from rest_framework import serializers

from vbb.language.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = [
            "id",
            "english_display_name",
            "name_in_native_alphabet",
        ]
