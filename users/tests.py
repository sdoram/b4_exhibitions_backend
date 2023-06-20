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


# ------------------------유저 테스트------------------------
class UserViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            nickname="test",
            password="123",
        )
        self.user.save()

    # ------------------------로그인 테스트------------------------
    def test_login(self):
        url = reverse("users:user-signin")
        login_data = {"email": "test@test.com", "password": "123"}
        response = self.client.post(url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
