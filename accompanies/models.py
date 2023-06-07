from django.db import models
from django.contrib.auth.models import User
from exhibitions.models import Exhibition


class Accompany(models.Model):
    user = models.ManyToManyField(
        User,
        related_name="get_accompanies",
        verbose_name="동행구하기 작성자",
    )
    info_name = models.ManyToManyField(
        Exhibition,
        related_name="accompanies",
        verbose_name="전시회 정보",
    )
    content = models.TextField("동행구하기 내용")
    personnel = models.PositiveIntegerField("동행인원")
    start_time = models.DateTimeField("모임시작시간", blank=True, null=True)
    end_time = models.DateTimeField("모임종료시간", blank=True, null=True)
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return str(self.content)


class Apply(models.Model):
    user = models.ManyToManyField(
        User,
        related_name="get_applies",
        verbose_name="동행신청하기 작성자",
    )
    accompany = models.ManyToManyField(
        Accompany,
        related_name="applies",
        verbose_name="동행구하기 댓글",
    )
    content = models.TextField("동행신청하기 내용")
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return str(self.content)
