from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer


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
