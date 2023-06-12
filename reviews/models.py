from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    content = models.TextField("내용")
    rating = models.PositiveIntegerField(
        "별점", validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    exhibition = models.ForeignKey("exhibitions.Exhibition", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField("사진", blank=True, null=True, upload_to="reviews/%Y/%m/")
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return str(self.content)
