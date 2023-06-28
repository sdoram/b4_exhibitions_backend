from rest_framework import serializers
from accompanies.models import Accompany, Apply


class ApplySerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    accompany = serializers.SerializerMethodField()

    class Meta:
        model = Apply
        fields = "__all__"

    def get_nickname(self, obj):
        return obj.user.nickname

    def get_user(self, obj):
        return obj.user.id

    def get_accompany(self, obj):
        return obj.accompany.id


0


class AccompanyCreateSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Accompany
        fields = (
            "id",
            "user",
            "nickname",
            "content",
            "personnel",
            "start_time",
            "end_time",
            "updated_at",
        )

    read_only_fields = (
        "nickname",
        "updated_at",
    )

    def validate(self, data):
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError("종료시간은 시작시간보다 빠를 수 없습니다.")
        if data["personnel"] == 0:
            raise serializers.ValidationError("목표인원을 1명 이상 선택하십시오.")
        return data

    def get_nickname(self, obj):
        return obj.user.nickname

    def get_user(self, obj):
        return obj.user.id


class AccompanySerializer(serializers.ModelSerializer):
    applies = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Accompany
        fields = "__all__"

    def get_nickname(self, obj):
        return obj.user.nickname

    def get_applies(self, obj):
        applies = obj.applies.all().order_by("-updated_at")
        return ApplySerializer(applies, many=True).data
