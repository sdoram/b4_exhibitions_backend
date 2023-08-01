from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    nickname = serializers.StringRelatedField(source="user.nickname")

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "nickname",
            "exhibition",
            "created_at",
            "updated_at",
        )
