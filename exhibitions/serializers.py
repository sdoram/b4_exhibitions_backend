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

    accompanies = AccompanySerializer(many=True)
    reviews = ReviewSerializer(source="review_set", many=True)

    # 읽기 전용 직렬화
    # serializer.data에서 select가 안된 다른 필드 값을 ''으로 변경
    def to_representation(self, instance):
        # serializer.data
        data = super().to_representation(instance)
        # query_params
        select = self.context["select"]
        # 데이터 값 빈값으로 교체
        if select == "accompanies":
            data["reviews"] = ""
        else:
            data["accompanies"] = ""
        return data

    class Meta:
        model = Exhibition
        exclude = []
