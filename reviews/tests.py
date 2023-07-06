from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from reviews.models import Review
from exhibitions.models import Exhibition


# ---------------------------리뷰 CUD 테스트---------------------------
class ReviewViewTest(APITestCase):
    # ----------------유저, 전시회, 리뷰 데이터 생성----------------
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
            "content": "Test Review Content",
            "rating": 5,
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.exhibition = Exhibition.objects.create(**cls.exhibition_data, user=cls.user)

    def setUp(self):
        super().setUp()

        self.access_token = self.client.post(
            reverse("users:user-signin"), self.user_data
        ).data["access"]

        self.review = Review.objects.create(
            content="Test Review Content",
            rating=5,
            exhibition=self.exhibition,
            user=self.user,
        )

    # ------------------------리뷰 작성 테스트------------------------
    def test_create_review(self):
        response = self.client.post(
            path=reverse(
                "reviews:review",
                kwargs={"exhibition_id": self.exhibition.id},
            ),
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(
            Review.objects.get(id=self.review.id).content, self.review_data["content"]
        )

    # ------------------------리뷰 수정 테스트------------------------
    def test_review_detail_update(self):
        self.review_updated_data = {
            "content": "Updated Test Content",
            "rating": 4,
        }

        response = self.client.put(
            path=reverse("reviews:review-detail", kwargs={"review_id": self.review.id}),
            data=self.review_updated_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(response.data["data"]["content"], "Updated Test Content")
        self.assertEqual(response.data["data"]["rating"], 4)

    # ------------------------리뷰 삭제 테스트------------------------
    def test_review_detail_delete(self):
        response = self.client.delete(
            path=reverse("reviews:review-detail", kwargs={"review_id": self.review.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
        self.assertEqual(response.data, {"message": "리뷰가 삭제되었습니다."})
