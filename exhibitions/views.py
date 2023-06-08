from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Exhibition
from .serializers import ExhibitionSerializer


class ExhibitionView(APIView):
    def get(self, request):  # 전시회 목록 불러오기
        # 카테고리 정보 가져오기
        category = request.query_params.get("category", None)
        # 카테고리 정보 존재 시
        if category:
            exhibitions = Exhibition.objects.filter(
                # category에 params value가 포함된 전시회 정보
                category__icontains=category
            ).order_by("-created_at")
        else:
            exhibitions = Exhibition.objects.order_by("-created_at")
        # 페이지네이션 class 객체 생성
        pagination = PageNumberPagination()
        # 페이지네이션 진행
        paginated_exhibitions = pagination.paginate_queryset(exhibitions, request)
        # 추후 일부 정보만 보여줘야 한다면 serializer 정의 필요
        serializer = ExhibitionSerializer(paginated_exhibitions, many=True)
        return pagination.get_paginated_response(serializer.data)

    def post(self, request):  # 전시회 작성
        serializer = ExhibitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "게시글이 등록되었습니다."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "요청이 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
            )


class ExhibitionDetailView(APIView):
    def get(self, request, exhibition_id):
        exhibition = get_object_or_404(Exhibition, id=exhibition_id)
        serializer = ExhibitionSerializer(exhibition)
        return Response(serializer.data)

    def put(self, request, exhibition_id):
        exhibition = get_object_or_404(Exhibition, id=exhibition_id)
        serializer = ExhibitionSerializer(exhibition, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "게시글이 수정되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, exhibition_id):
        exhibition = get_object_or_404(Exhibition, id=exhibition_id)
        exhibition.delete()
        return Response({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


class ExhibitionLikeView(APIView):  # 좋아요 기능
    def post(self, request, exhibition_id):
        exhibition = get_object_or_404(Exhibition, id=exhibition_id)
        if request.user not in exhibition.likes.all():
            exhibition.likes.add(request.user)
            return Response({"message": "좋아요"}, status=status.HTTP_201_CREATED)
        else:
            exhibition.likes.remove(request.user)
            return Response({"message": "좋아요 취소"}, status=status.HTTP_204_NO_CONTENT)
