from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# ---------------------------회원가입 테스트------------------------
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
