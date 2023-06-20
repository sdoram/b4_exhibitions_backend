from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


# ------------------------회원가입 테스트------------------------
class SignupViewTest(APITestCase):
    def test_signup(self):
        url = reverse("users:user-signup")
        data = {
            "email": "test@test.com",
            "nickname": "test",
            "password": "123",
            "password_check": "123",
            "gender": "여성",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# ------------------------로그인 테스트------------------------
class SigninViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            nickname="test",
            password="123",
        )
        self.user.save()

    def test_login(self):
        url = reverse("users:user-signin")
        login_data = {"email": "test@test.com", "password": "123"}
        response = self.client.post(url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ------------------------유저 테스트------------------------
class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "test@test.com",
            "nickname": "testuser",
            "password": "123",
        }
        cls.user = User.objects.create_user(**cls.user_data)

    def setUp(self):
        self.access_token = self.client.post(
            reverse("users:user-signin"), self.user_data
        ).data["access"]

    # ------------------------마이페이지 테스트------------------------
    def test_mypage(self):
        user_id = self.user.id
        url = reverse("users:user-mypage", kwargs={"user_id": user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ------------------------회원수정 테스트------------------------
    def test_user_update(self):
        update_data = {"nickname": "goodman", "bio": "안녕하세요 테스트 중입니다"}
        response = self.client.patch(
            path=reverse("users:user-update-and-delete"),
            data=update_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
