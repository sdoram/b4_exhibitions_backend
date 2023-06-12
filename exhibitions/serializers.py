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

    select = serializers.SerializerMethodField()
    # query_params에 따라서 필드 변경
    if select == "accompanies":
        accompanies = AccompanySerializer(many=True)
    else:
        reviews = ReviewSerializer(source="review_set", many=True)

    def get_select(self, obj):
        return self.context["select"]

    class Meta:
        model = Exhibition
        exclude = []
