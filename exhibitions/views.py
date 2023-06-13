from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Exhibition
from reviews.models import Review
from accompanies.models import Accompany
from accompanies.serializers import AccompanySerializer
from reviews.serializers import ReviewSerializer
from .serializers import (
    ExhibitionSerializer,
    ExhibitionDetailSerializer,
)


class ExhibitionView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증된 사용자, 인증되지 않은 사용자 모두 읽기 가능

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
        if request.user.is_staff:  # 관리자만 작성 가능
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
        else:
            return Response(
                {"message": "관리자만 글을 작성할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )


class ExhibitionDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request, exhibition_id):
        exhibition = get_object_or_404(Exhibition, id=exhibition_id)
        # query_params를 serializer로 전달
        serializer = ExhibitionDetailSerializer(
            exhibition,
            context={
                "select": request.query_params.get("select", None),
                "request": request,
            },
        )
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


class ExhibitionSearchView(APIView):
    def get(self, request):
        search = request.query_params.get("search", None)
        # 키워드가 있는 경우
        if search:
            # 전시회 내용 or 제목으로 검색
            exhibitions = Exhibition.objects.filter(
                content__icontains=search
            ) | Exhibition.objects.filter(info_name__icontains=search).order_by(
                "-created_at"
            )
            reviews = Review.objects.filter(content__icontains=search).order_by(
                "-created_at"
            )
            accompanies = Accompany.objects.filter(content__icontains=search).order_by(
                "-created_at"
            )
        else:
            exhibitions = Exhibition.objects.all().order_by("-created_at")
            reviews = Review.objects.all().order_by("-created_at")
            accompanies = Accompany.objects.all().order_by("-created_at")
        results = (
            ExhibitionSerializer(exhibitions, many=True),
            ReviewSerializer(reviews, many=True),
            AccompanySerializer(accompanies, many=True),
        )
        # serializer.data의 리스트를 Response로 보내주기
        return Response([result.data for result in results], status=status.HTTP_200_OK)
