from django.db import models
from users.models import User
from exhibitions.models import Exhibition


class Accompany(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="get_accompanies",
        verbose_name="작성자",
    )
    exhibition = models.ForeignKey(
        Exhibition,
        on_delete=models.CASCADE,
        related_name="accompanies",
        verbose_name="전시회 정보",
    )
    content = models.TextField("내용")
    personnel = models.PositiveIntegerField("동행 인원")
    start_time = models.DateTimeField("모임 시작시간")
    end_time = models.DateTimeField("모임 종료시간")
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return str(self.content)


class Apply(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="get_applies",
        verbose_name="작성자",
    )
    accompany = models.ForeignKey(
        Accompany,
        on_delete=models.CASCADE,
        related_name="applies",
        verbose_name="동행 구하는 댓글",
    )
    content = models.TextField("내용")
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return str(self.content)
