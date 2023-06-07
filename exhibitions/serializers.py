from rest_framework import serializers
from .models import Exhibition


class ExhibitionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    info_name = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    period = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return str(obj.user_id)

    def get_info_name(self, obj):
        return obj.info_name.upper() if obj.info_name else obj.info_name

    def get_period(self, obj):
        return f"{obj.period} 동안 전시"

    def get_location(self, obj):
        return f"장소: {obj.location}"

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y년 %m월 %d일 %p:%M:%S")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y년 %m월 %d일 %p:%M:%S")

    def get_likes(self, obj):
        return obj.likes.count()

    def get_total_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = Exhibition
        fields = [
            "id",
            "user_id",
            "info_name",
            "content",
            "period",
            "location",
            "image",
            "created_at",
            "updated_at",
        ]
