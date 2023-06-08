from rest_framework import serializers
from accompanies.models import Accompany, Apply


class ApplyCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = ("content",)


class AccompanyCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Accompany
        fields = ("content", "personnel", "start_time", "end_time")


class AccompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Accompany
        fields = "__all__"
