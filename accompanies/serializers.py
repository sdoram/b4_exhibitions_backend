from rest_framework import serializers
from accompanies.models import Accompany, Apply


class ApplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = ("content",)


class ApplySerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Apply
        fields = "__all__"

    def get_nickname(self, obj):
        return obj.user.nickname


class AccompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accompany
        fields = ("content", "personnel", "start_time", "end_time")


class AccompanySerializer(serializers.ModelSerializer):
    applies = ApplySerializer(many=True)
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Accompany
        fields = "__all__"

    def get_nickname(self, obj):
        return obj.user.nickname
