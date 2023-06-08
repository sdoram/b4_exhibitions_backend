from rest_framework import serializers
from accompanies.models import Accompany, Apply


class ApplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = ("content",)


class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = "__all__"


class AccompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accompany
        fields = ("content", "personnel", "start_time", "end_time")


class AccompanySerializer(serializers.ModelSerializer):
    applies = ApplySerializer(many=True)

    class Meta:
        model = Accompany
        fields = "__all__"
