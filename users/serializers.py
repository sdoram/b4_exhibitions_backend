from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User
from rest_framework.generics import get_object_or_404
from exhibitions.serializers import ExhibitionSerializer
from exhibitions.models import Exhibition
from datetime import datetime, date
from django.db.models import Count


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["is_active"]

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # patch를 사용 하기 위에 값이 들어 오지 않으면 원래 상태, 아니면 수정된 데이터 저장
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)  # 비밀번호 암호화
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["is_admin"] = user.is_admin

        return token


class UserMypageSerializer(serializers.ModelSerializer):
    since_together = serializers.SerializerMethodField()
    exhibition_likes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "nickname",
            "bio",
            "created_at",
            "since_together",
            "profile_image",
            "gender",
            "exhibition_likes",
        )

    def get_since_together(self, request_user):
        calculate = date.today() - request_user.created_at.date()
        return calculate.days + 1

    def get_exhibition_likes(self, obj):
        # 유저가 좋아요 누른 전시회 id 가져오기
        exhibition_likes_list = [value["id"] for value in obj.exhibition_likes.values()]

        return [
            # 가져온 id를 바탕으로 serializer 진행
            ExhibitionSerializer(get_object_or_404(Exhibition, id=exhibition_id)).data
            for exhibition_id in exhibition_likes_list
        ]
