from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "nickname",
            "exhibition_id",
            "content",
            "rating",
            "image",
            "created_at",
            "updated_at",
        ]

    def get_nickname(self, obj):
        return obj.user.nickname


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["content", "rating", "image"]
