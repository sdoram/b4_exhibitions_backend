from rest_framework import serializers

from .models import Exhibition
from reviews.serializers import ReviewSerializer
from accompanies.serializers import AccompanySerializer
from .paginations import CustomPageNumberPagination


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
        pagination = CustomPageNumberPagination()
        # query_params
        select = self.context["select"]
        # select에 따라 field 추가
        if select == "accompanies":
            accompany = instance.accompanies.all()
            paginated_accompanies = pagination.paginate_queryset(
                accompany, self.context["request"]
            )
            serializer = AccompanySerializer(paginated_accompanies, many=True)
            data["accompanies"] = pagination.get_paginated_response(serializer.data)
        else:
            reviews = instance.exhibition_reviews.all()
            paginated_reviews = pagination.paginate_queryset(
                reviews, self.context["request"]
            )
            serializer = ReviewSerializer(paginated_reviews, many=True)
            data["reviews"] = pagination.get_paginated_response(serializer.data)
        return data

    class Meta:
        model = Exhibition
        exclude = []
