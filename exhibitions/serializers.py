from rest_framework import serializers

from .models import Exhibition
from reviews.serializers import ReviewSerializer
from accompanies.serializers import AccompanySerializer


class TopFiveExhibitionSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Exhibition
        fields = ["id", "info_name", "likes"]

    def get_likes(self, obj):
        return obj.likes.count()


class ExhibitionSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Exhibition
        fields = [
            "id",
            "user_id",
            "info_name",
            "location",
            "image",
            "created_at",
            "updated_at",
            "category",
            "start_date",
            "end_date",
            "svstatus",
            "longitude",
            "latitude",
            "likes",
            "direct_url",
            "content",
        ]
        extra_kwargs = {
            "content": {
                "write_only": True,
            },
        }

    def get_likes(self, obj):
        return obj.likes.count()


class ExhibitionDetailSerializer(serializers.ModelSerializer):
    """전시회 상세보기"""

    likes = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    accompany_count = serializers.SerializerMethodField()

    # 읽기 전용 직렬화
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["recommend"] = self.context["recommend"]
        # query_params
        select = self.context["select"]
        # select에 따라 field 추가
        if select == "accompanies":
            accompany = instance.accompanies.all().order_by("-updated_at")
            data["accompanies"] = AccompanySerializer(accompany, many=True).data
        else:
            reviews = instance.exhibition_reviews.all().order_by("-updated_at")
            data["reviews"] = ReviewSerializer(reviews, many=True).data
        return data

    class Meta:
        model = Exhibition
        exclude = []

    def get_likes(self, obj):
        return obj.likes.count()

    def get_review_count(self, obj):
        return obj.exhibition_reviews.count()

    def get_accompany_count(self, obj):
        return obj.accompanies.count()
