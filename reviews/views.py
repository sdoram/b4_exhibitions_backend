from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewView(APIView):
    # 리뷰 보기
    def get(self, request, exhibition_id):
        reviews = Review.objects.filter(exhibition_id=exhibition_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 리뷰 작성
    def post(self, request, exhibition_id):
        # 로그인
        if not request.user.is_authenticated:
            return Response(
                {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(exhibition_id=exhibition_id, user=request.user)
            return Response({"message": "리뷰가 등록되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(
            {"message": "요청이 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
