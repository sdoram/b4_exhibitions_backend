from rest_framework import serializers

from .models import Exhibition
from reviews.serializers import ReviewSerializer
from accompanies.serializers import AccompanySerializer


class ExhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibition
        fields = [
            "id",
            "user_id",
            "info_name",
            "content",
            "location",
            "image",
            "created_at",
            "updated_at",
            "category",
            "start_date",
            "end_date",
        ]

    def get_likes(self, obj):
        return obj.likes.count()

    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None


class ExhibitionDetailSerializer(serializers.ModelSerializer):
    """전시회 상세보기"""

    # 읽기 전용 직렬화
    def to_representation(self, instance):
        # serializer.data
        data = super().to_representation(instance)
        # query_params
        select = self.context["select"]
        # select에 따라 filed 추가
        if select == "accompanies":
            accompany = instance.accompanies.all()
            serializer = AccompanySerializer(accompany, many=True)
            data["accompanies"] = serializer.data
        else:
            # related_name 설정 필요
            reviews = instance.review_set.all()
            serializer = ReviewSerializer(reviews, many=True)
            data["reviews"] = serializer.data
        return data

    class Meta:
        model = Exhibition
        exclude = []
