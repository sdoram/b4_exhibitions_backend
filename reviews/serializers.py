from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "nickname",
            "exhibition_id",
            "content",
            "rating",
            "image",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "nickname",
            "exhibition_id",
            "created_at",
            "updated_at",
        )

    def get_nickname(self, obj):
        return obj.user.nickname
