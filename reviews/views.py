from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Review
from .serializers import ReviewSerializer


class ReviewView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

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

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(exhibition_id=exhibition_id, user=request.user)
            return Response(
                {"message": "리뷰가 등록되었습니다.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "요청이 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
        )


class ReviewDetailView(APIView):
    # 리뷰 수정
    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {"message": "리뷰가 수정되었습니다.", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 삭제
    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        if request.user == review.user:
            review.delete()
            return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
