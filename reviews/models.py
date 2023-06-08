from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    content = models.TextField("내용")
    rating = models.IntegerField("별점", default=0)
    exhibition = models.ForeignKey("exhibitions.Exhibition", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField("사진", blank=True, null=True)
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)
