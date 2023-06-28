from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from reviews.models import Review
from exhibitions.models import Exhibition


class ReviewViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "test@test.com",
            "nickname": "testuser",
            "password": "123",
        }
        cls.exhibition_data = {
            "info_name": "Test Info_name",
            "content": "Test Exhibition Content",
            "location": "Test Location",
            "category": "Test Category",
            "start_date": "2022-06-04",
            "end_date": "2022-06-10",
        }
        cls.review_data = {
            "title": "Test Review Title",
            "content": "Test Review Content",
            "rating": 5,
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.exhibition = Exhibition.objects.create(**cls.exhibition_data, user=cls.user)

    def setUp(self):
        self.access_token = self.client.post(
            reverse("users:user-signin"), self.user_data
        ).data["access"]

    def test_create_review(self):
        response = self.client.post(
            path=reverse(
                "reviews:review-list",
                kwargs={"exhibition_id": self.exhibition.id},
            ),
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().title, self.review_data["title"])

    def test_review_list(self):
        self.reviews = []
        for _ in range(5):
            self.reviews.append(
                Review.objects.create(
                    title="Test Review Title",
                    content="Test Review Content",
                    rating=5,
                    exhibition=self.exhibition,
                    user=self.user,
                )
            )

        response = self.client.get(
            path=reverse(
                "reviews:review-list",
                kwargs={"exhibition_id": self.exhibition.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 5)
        self.assertEqual(len(response.data["data"]), 5)
        self.assertEqual(response.data["data"][0]["title"], "Test Review Title")

    def test_review_detail_update(self):
        self.review = Review.objects.create(
            title="Test Review Title",
            content="Test Review Content",
            rating=5,
            exhibition=self.exhibition,
            user=self.user,
        )
        self.review_updated_data = {
            "title": "Updated Test Title",
            "content": "Updated Test Content",
            "rating": 4,
        }

        response = self.client.put(
            path=reverse("reviews:review-detail", kwargs={"review_id": 1}),
            data=self.review_updated_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(response.data["data"]["title"], "Updated Test Title")
        self.assertEqual(response.data["data"]["content"], "Updated Test Content")
        self.assertEqual(response.data["data"]["rating"], 4)
