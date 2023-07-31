import os
import requests

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    UserMypageSerializer,
)


class UserView(APIView):
    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [AllowAny()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request, user_id):  # 마이페이지 조회
        user = get_object_or_404(User, id=user_id)
        serializer = UserMypageSerializer(user)
        return Response(serializer.data)

    def post(self, request):  # 회원가입
        password = request.data["password"]
        password_check = request.data["password_check"]
        serializer = UserSerializer(data=request.data)
        if password != password_check:
            return Response(
                {"message": "재확인 비밀번호가 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):  # 회원 정보 수정
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "회원 정보가 수정되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):  # 회원탈퇴 -> 계정 비활성화
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "탈퇴되었습니다."})


class CustomTokenObtainPairView(TokenObtainPairView):  # 토큰 부여하는 코드 = 로그인
    serializer_class = CustomTokenObtainPairSerializer


class GoogleSignin(APIView):  # 구글 소셜 로그인
    def get(self, request):
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        return Response(GOOGLE_API_KEY, status=status.HTTP_200_OK)

    def post(self, request):
        access_token = request.data["access_token"]
        user_data = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_data.json()
        data = {
            "profile_image": user_data.get("picture"),
            "email": user_data.get("email"),
            "nickname": user_data.get("name"),
            "signin_type": "google",
        }
        return SocialSignin(**data)


def SocialSignin(**kwargs):  # 소셜 로그인/회원가입
    # 소셜 로그인에서 유저 정보를 받아오고 None인 값들은 빼줌
    data = {k: v for k, v in kwargs.items() if v is not None}
    email = data.get("email")
    signin_type = data.get("signin_type")
    if not email:
        # email이 없으면 회원가입이 불가능하므로 프론트에 error메시지와 http status를 보냄
        return Response(
            {"error": "해당 계정에 email정보가 없습니다."}, status=status.HTTP_400_BAD_REQUEST
        )

    user, created = User.objects.get_or_create(email=email, defaults=data)

    if created:
        user.set_unusable_password()
        user.save()
        # 회원가입 후 토큰 발급해서 프론트로 보냄
        refresh_token = RefreshToken.for_user(user)
        access_token = CustomTokenObtainPairSerializer.get_token(user)
        return Response(
            {
                "refresh": str(refresh_token),
                "access": str(access_token.access_token),
            },
            status=status.HTTP_200_OK,
        )
    else:
        # DB에서 찾은 사용자와 로그인 타입이 일치하는 경우
        if user.signin_type == signin_type:
            if user.is_active == 0:
                return Response(
                    {"message": "탈퇴한 계정입니다."}, status=status.HTTP_403_FORBIDDEN
                )
            refresh_token = RefreshToken.for_user(user)
            access_token = CustomTokenObtainPairSerializer.get_token(user)
            return Response(
                {
                    "refresh": str(refresh_token),
                    "access": str(access_token.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": f"{user.signin_type}로 이미 가입된 계정이 있습니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
