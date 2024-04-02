from care_scribe.models.scribe import Scribe
from rest_framework import serializers
from care_scribe.models.scribe_file import ScribeFile
from rest_framework import serializers
from config.serializers import ChoiceField
from rest_framework.exceptions import ValidationError
from django.conf import settings
from care.users.api.serializers.user import UserBaseMinimumSerializer

def check_permissions(file_type, associating_id, user):
    if file_type == ScribeFile.FileType.SCRIBE:
        scribe_obj = Scribe.objects.filter(external_id=associating_id).first()
        if scribe_obj and scribe_obj.requested_by != user:
            raise ValidationError({"detail": "Permission Denied"})
        return associating_id

class ScribeFileUploadCreateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    file_type = ChoiceField(choices=ScribeFile.FileTypeChoices)
    file_category = ChoiceField(choices=ScribeFile.FileCategoryChoices, required=False)

    signed_url = serializers.CharField(read_only=True)
    associating_id = serializers.CharField(write_only=True)
    internal_name = serializers.CharField(read_only=True)
    original_name = serializers.CharField(write_only=True)
    mime_type = serializers.CharField(write_only=True)

    class Meta:
        model = ScribeFile
        fields = (
            "id",
            "file_type",
            "file_category",
            "name",
            "associating_id",
            "signed_url",
            "internal_name",
            "original_name",
            "mime_type",
        )
        write_only_fields = ("associating_id",)

    def create(self, validated_data):
        user = self.context["request"].user
        mime_type = validated_data.pop("mime_type")

        if mime_type not in settings.ALLOWED_MIME_TYPES:
            raise ValidationError({"detail": "Invalid File Type"})

        internal_id = check_permissions(
            validated_data["file_type"], validated_data["associating_id"], user
        )
        validated_data["associating_id"] = internal_id
        validated_data["uploaded_by"] = user
        validated_data["internal_name"] = validated_data["original_name"]
        del validated_data["original_name"]
        file_upload: ScribeFile = super().create(validated_data)
        file_upload.signed_url = file_upload.signed_url(mime_type=mime_type)
        return file_upload

class ScribeFileUploadUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    class Meta:
        model = ScribeFile
        fields = (
            "id",
            "name",
            "upload_completed",
        )