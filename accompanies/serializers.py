from rest_framework import serializers
from accompanies.models import Accompany


class AccompanyCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Accompany
        fields = ("content", "personnel", "start_time", "end_time")
