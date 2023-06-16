import tempfile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from exhibitions.models import Exhibition
from PIL import Image


# -----------------------------------이미지 생성 함수----------------------------------
def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, "png")
    return temp_file


# -----------------------------------전시회 CRUD 테스트----------------------------------
class ExhibitionViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "nickname": "test", "password": "123"}
        cls.user = User.objects.create_superuser("admin@admin.com", "admin", "123")
        cls.exhibition_data = {
            "info_name": "Test Info_name",
            "content": "Test Exhibition Content",
            "location": "Test Location",
            "category": "Test Category",
            "start_date": "2023-01-01",
            "end_date": "2023-02-01",
        }
        cls.user = User.objects.create_superuser(**cls.user_data)

    def setUp(self):
        admin_data = {"email": "admin@admin.com", "password": "123"}
        response = self.client.post(reverse("users:user-signin"), admin_data)
        self.access_token = response.data["access"]
        self.is_admin = self.user.is_staff
        Exhibition.objects.all().delete()

    def tearDown(self):
        for exhibition in Exhibition.objects.all():
            exhibition.image.delete()
            exhibition.delete()

    # -------------------------------전시회(게시글)작성 테스트(관리자만 작성 가능)----------------------------------
    def test_create_exhibition(self):
        if not self.is_admin:
            self.skipTest("Skipped test_exhibition_detail_update_admin")

        response = self.client.post(
            path=reverse("exhibitions:exhibition"),
            data=self.exhibition_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exhibition.objects.count(), 1)
        self.assertEqual(Exhibition.objects.get().info_name, "Test Info_name")

    # ------------------------------------이미지와 함께 전시회(게시글) 작성 테스트-----------------------------
    def test_create_exhibition_with_image(self):
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        self.exhibition_data["image"] = image_file
        response = self.client.post(
            path=reverse("exhibitions:exhibition"),
            data=self.exhibition_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exhibition.objects.count(), 1)
        self.assertEqual(Exhibition.objects.get().info_name, "Test Info_name")
        self.assertEqual(bool(Exhibition.objects.get().image), True)

    # ------------------------------------전시회(게시글) 리스트를 불러옴------------------------------------
    def test_get_exhibition_list(self):
        response = self.client.get(path=reverse("exhibitions:exhibition"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    # ------------------------------------전체 전시회(게시글) 리스트를 불러옴--------------------------------
    def test_get_exhibition_list(self):
        Exhibition.objects.all().delete()
        exhibitions = []
        for _ in range(4):
            exhibitions.append(Exhibition.objects.create(**self.exhibition_data, user=self.user))
        response = self.client.get(path=reverse("exhibitions:exhibition"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


# --------------------------------------전시회 상세페이지 테스트----------------------------------
class ExhibitionDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "nickname": "test", "password": "123"}
        cls.user = User.objects.create_superuser("admin@admin.com", "admin", "123")
        cls.exhibition_data = [
            {"info_name": "test Title1", "content": "test content1"},
            {"info_name": "test Title2", "content": "test content2"},
            {"info_name": "test Title3", "content": "test content3"},
            {"info_name": "test Title4", "content": "test content4"},
            {"info_name": "test Title5", "content": "test content5"},
        ]
        cls.exhibitions = []
        for i in range(5):
            cls.exhibitions.append(
                Exhibition.objects.create(**cls.exhibition_data[i], user=cls.user)
            )

    def setUp(self):
        admin_data = {"email": "admin@admin.com", "password": "123"}
        response = self.client.post(reverse("users:user-signin"), admin_data)
        self.access_token = response.data["access"]
        self.is_admin = self.user.is_staff

    # ------------------------------------전시회 상세페이지를 불러옴--------------------------------
    def test_exhibition_detail(self):
        response = self.client.get(
            path=reverse("exhibitions:exhibition-detail", kwargs={"exhibition_id": 2}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "test content2")

    # ------------------------------------전시회 상세페이지를 수정(관리자만 수정 가능)--------------------------------
    def test_exhibition_detail_update_admin(self):
        if not self.is_admin:
            self.skipTest("Skipped test_exhibition_detail_update_admin")

        data = {"content": "updated test content"}
        response = self.client.put(
            path=reverse("exhibitions:exhibition-detail", kwargs={"exhibition_id": 2}),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

    # ------------------------------------전시회 상세페이지를 삭제(관리자만 삭제 가능)--------------------------------
    def test_exhibition_detail_delete_admin(self):
        if not self.is_admin:
            self.skipTest("Skipped test_exhibition_detail_delete_admin")

        response = self.client.delete(
            path=reverse("exhibitions:exhibition-detail", kwargs={"exhibition_id": 5}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exhibition.objects.count(), 4)
        self.assertFalse(Exhibition.objects.filter(id=5).exists())


# --------------------------------------전시회 좋아요 테스트----------------------------------
class ExhibitionLikeViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "admin@admin.com", "nickname": "admin", "password": "123"}
        cls.exhibition_data = {"info_name": "test Title", "content": "test content"}
        cls.user = User.objects.create_user(**cls.user_data)
        cls.exhibition = Exhibition.objects.create(**cls.exhibition_data, user=cls.user)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    # ------------------------------------전시회 좋아요--------------------------------
    def test_like_exhibition(self):
        response = self.client.post(
            reverse("exhibitions:exhibition-like", kwargs={"exhibition_id": self.exhibition.id})
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"message": "좋아요"})
        self.assertIn(self.user, self.exhibition.likes.all())

    # ------------------------------------전시회 좋아요 취소--------------------------------
    def test_cancel_like_exhibition(self):
        self.exhibition.likes.add(self.user)
        response = self.client.post(
            reverse("exhibitions:exhibition-like", kwargs={"exhibition_id": self.exhibition.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "좋아요 취소"})
        self.assertNotIn(self.user, self.exhibition.likes.all())
