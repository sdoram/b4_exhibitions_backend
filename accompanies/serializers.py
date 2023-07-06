from rest_framework import serializers
from accompanies.models import Accompany, Apply


class ApplySerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Apply
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "nickname",
            "accompany",
            "created_at",
            "updated_at",
        )

    def get_nickname(self, obj):
        return obj.user.nickname


class AccompanySerializer(serializers.ModelSerializer):
    applies = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    picks_count = serializers.SerializerMethodField()

    class Meta:
        model = Accompany
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "nickname",
            "exhibition",
            "applies",
            "created_at",
            "updated_at",
        )

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        personnel = data.get("personnel")

        if start_time and end_time and start_time > end_time:
            raise serializers.ValidationError("종료시간은 시작시간보다 빠를 수 없습니다.")
        if personnel and personnel == 0:
            raise serializers.ValidationError("목표인원을 1명 이상 선택하십시오.")
        return data

    def get_applies(self, obj):
        applies = obj.applies.all().order_by("-updated_at")
        return ApplySerializer(applies, many=True).data

    def get_nickname(self, obj):
        return obj.user.nickname

    def get_picks_count(self, obj):
        return obj.picks.count()
