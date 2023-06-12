from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from accompanies.models import Accompany, Apply
from exhibitions.models import Exhibition


# ---------------------------동행 구하기 댓글 CRUD 테스트------------------------
class AccompanyViewTest(APITestCase):
    # ----------------유저, 전시회, 동행 구하기 댓글 데이터 생성---------------
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
        cls.accompany_data = {
            "content": "Test Accompany Content",
            "personnel": 3,
            "start_time": "2023-06-13 11:00",
            "end_time": "2023-06-13 15:00",
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.exhibition = Exhibition.objects.create(**cls.exhibition_data, user=cls.user)

    def setUp(self):
        self.access_token = self.client.post(
            reverse("users:user-signin"), self.user_data
        ).data["access"]

    # --------------동행 구하기 댓글 작성 테스트------------------------
    def test_create_accompany(self):
        response = self.client.post(
            path=reverse(
                "accompanies:accompany-view",
                kwargs={"exhibition_id": self.exhibition.id},
            ),
            data=self.accompany_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Accompany.objects.count(), 1)
        self.assertEqual(
            Accompany.objects.get().content, self.accompany_data["content"]
        )

    # --------------동행 구하기 댓글 조회 테스트------------------------
    def test_accompany_list(self):
        self.accompanies = []
        for _ in range(5):
            self.accompanies.append(
                Accompany.objects.create(
                    content="Test Accompany Content",
                    personnel=3,
                    start_time="2023-06-13 11:00",
                    end_time="2023-06-13 15:00",
                    exhibition=self.exhibition,
                    user=self.user,
                )
            )
        response = self.client.get(
            path=reverse(
                "accompanies:accompany-view",
                kwargs={"exhibition_id": self.exhibition.id},
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Accompany.objects.count(), 5)
        self.assertEqual(len(response.data["data"]), 5)
        self.assertEqual(response.data["data"][0]["content"], "Test Accompany Content")

    # --------------동행 구하기 댓글 수정 테스트------------------------
    def test_accompany_detail_update(self):
        self.accompany = Accompany.objects.create(
            **self.accompany_data, user=self.user, exhibition=self.exhibition
        )
        self.accompany_updated_data = {
            "content": "Updated Test Content",
            "personnel": 4,
            "start_time": "2023-06-15 10:00",
            "end_time": "2023-06-15 12:00",
        }

        response = self.client.put(
            path=reverse("accompanies:accompany-view", kwargs={"accompany_id": 1}),
            data=self.accompany_updated_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Accompany.objects.count(), 1)
        self.assertEqual(response.data["data"]["content"], "Updated Test Content")
        self.assertEqual(response.data["data"]["personnel"], 4)
        self.assertEqual(response.data["data"]["start_time"], "2023-06-15T10:00:00")
        self.assertEqual(response.data["data"]["end_time"], "2023-06-15T12:00:00")

    # --------------동행 구하기 댓글 삭제 테스트------------------------
    def test_accompany_detail_delete(self):
        self.accompany = Accompany.objects.create(
            **self.accompany_data, user=self.user, exhibition=self.exhibition
        )

        response = self.client.delete(
            path=reverse("accompanies:accompany-view", kwargs={"accompany_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Accompany.objects.count(), 0)
        self.assertEqual(response.data, {"message": "동행 구하기 글이 삭제되었습니다."})


# ---------------------------동행 신청하기 댓글 CRUD 테스트------------------------
class ApplyViewTest(APITestCase):
    # ----------------유저, 동행 구하기/신청하기 댓글 데이터 생성---------------
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
        cls.accompany_data = {
            "content": "Test Accompany Content",
            "personnel": 3,
            "start_time": "2023-06-13 11:00",
            "end_time": "2023-06-13 15:00",
        }
        cls.apply_data = {
            "content": "Test Accompany Content",
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.exhibition = Exhibition.objects.create(**cls.exhibition_data, user=cls.user)
        cls.accompany = Accompany.objects.create(
            **cls.accompany_data, user=cls.user, exhibition=cls.exhibition
        )

    def setUp(self):
        self.access_token = self.client.post(
            reverse("users:user-signin"), self.user_data
        ).data["access"]

    # --------------동행 신청하기 댓글 작성 테스트------------------------
    def test_create_apply(self):
        response = self.client.post(
            path=reverse(
                "accompanies:apply-view",
                kwargs={"accompany_id": self.accompany.id},
            ),
            data=self.apply_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Apply.objects.count(), 1)
        self.assertEqual(Apply.objects.get().content, self.accompany_data["content"])

    # --------------동행 신청하기 댓글 수정 테스트------------------------
    def test_apply_detail_update(self):
        self.apply = Apply.objects.create(
            **self.apply_data, user=self.user, accompany=self.accompany
        )
        self.apply_updated_data = {"content": "Updated Test Content"}

        response = self.client.put(
            path=reverse("accompanies:apply-view", kwargs={"apply_id": 1}),
            data=self.apply_updated_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Accompany.objects.count(), 1)
        self.assertEqual(response.data["data"]["content"], "Updated Test Content")

    # --------------동행 신청하기 댓글 삭제 테스트------------------------
    def test_apply_detail_delete(self):
        self.apply = Apply.objects.create(
            **self.apply_data, user=self.user, accompany=self.accompany
        )

        response = self.client.delete(
            path=reverse("accompanies:apply-view", kwargs={"apply_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Apply.objects.count(), 0)
        self.assertEqual(response.data, {"message": "동행 신청하기 댓글이 삭제되었습니다."})
