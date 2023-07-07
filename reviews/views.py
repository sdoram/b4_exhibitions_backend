from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, exhibition_id):  # 리뷰 작성하기
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, exhibition_id=exhibition_id)
        return Response(
            {"message": "리뷰가 등록되었습니다.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, review_id):  # 리뷰 수정하기
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "리뷰가 수정되었습니다.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, review_id):  # 리뷰 삭제하기
        review = get_object_or_404(Review, id=review_id)

        if request.user == review.user:
            review.delete()
            return Response(
                {"message": "리뷰가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
