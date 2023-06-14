from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from json.decoder import JSONDecodeError
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import get_object_or_404
import os
from django.shortcuts import redirect

from users.models import User
from users.serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    UserMypageSerializer,
)


class UserView(APIView):
    def post(self, request):
        """회원 가입을 실행합니다."""
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


class CustomTokenObtainPairView(TokenObtainPairView):  # 토큰 부여하는 코드 = 로그인
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailView(APIView):
    def patch(self, request):
        """회원 정보를 수정합니다."""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "회원 정보가 수정되었습니다."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        """회원 계정을 비활성화합니다."""
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "탈퇴되었습니다."})


# 마이페이지
class UserMypageView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserMypageSerializer(user)

        return Response(serializer.data)


# 구글 소셜로그인 변수 설정
state = os.environ.get("STATE")
# 복습
BASE_URL = "http://localhost:8000/"
GOOGLE_CALLBACK_URI = BASE_URL + "api/users/google/callback/"


@api_view(["GET", "POST"])
def google_login(request):
    """
    인가 코드 요청
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )


@api_view(["GET", "POST"])
def google_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get("code")
    """
    액세스 토큰 요청
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    print(access_token)

    """
    우선 구글로 로그인된 사용자의 이메일 요청
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )
    email_req_json = email_req.json()
    email = email_req_json.get("email")
    print("내 이메일", email)
    """
    이메일을 가지고 우리 사이트에 로그인 시키거나 회원가입
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "google":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 Google로 가입된 유저
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}api/users/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        # https://www.googleapis.com/oauth2/v2/userinfo

        # data = {"access_token": access_token, "code": code}
        # accept = requests.post(f"{BASE_URL}api/users/google/login/finish/", data=data)
        # headers={"Authorization": f"Bearer {access_token}"}

        accept = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        accept = accept.json()
        print(accept)
        data = {
            "profile_image": accept.get("picture"),
            "email": accept.get("email"),
            # "username": accept.get("name"),
            "login_type": "google",
        }
        new_user = User.objects.create(**data)
        # pw는 사용불가로 지정
        new_user.set_unusable_password()
        new_user.save()
        # 이후 토큰 발급해서 프론트로
        refresh = RefreshToken.for_user(new_user)
        access_token = CustomTokenObtainPairSerializer.get_token(new_user)
        return Response(
            {"refresh": str(refresh), "access": str(access_token.access_token)},
            status=status.HTTP_200_OK,
        )


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
