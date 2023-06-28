from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .paginations import CustomPageNumberPagination

from .models import Exhibition
from reviews.models import Review
from accompanies.models import Accompany
from accompanies.serializers import AccompanySerializer
from reviews.serializers import ReviewSerializer
from .serializers import (
    ExhibitionSerializer,
    ExhibitionDetailSerializer,
)

from .recommend_ml import recommendation
from django.db.models.query_utils import Q
import datetime


class ExhibitionView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증된 사용자, 인증되지 않은 사용자 모두 읽기 가능

    def get(self, request):  # 전시회 목록 불러오기
        q = Q()
        today = datetime.date.today()
        # 카테고리 정보 가져오기
        category = request.query_params.get("category", None)
        if category:
            q.add(Q(category__icontains=category), q.OR)
        # 현재 날짜 기준으로 예약 가능한 전시회만 보여주기
        q.add(Q(start_date__lte=today), q.AND)
        q.add(Q(end_date__gte=today), q.AND)
        q.add(Q(svstatus="접수중"), q.AND)
        exhibitions = Exhibition.objects.filter(q).order_by("end_date")
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
                    {"message": "게시글이 등록되었습니다.", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
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
        recommend = [
            get_object_or_404(Exhibition, id=id) for id in recommendation(exhibition_id)
        ]
        # query_params를 serializer로 전달
        serializer = ExhibitionDetailSerializer(
            exhibition,
            context={
                "select": request.query_params.get("select", None),
                "request": request,
                "recommend": ExhibitionSerializer(recommend, many=True).data,
            },
        )
        return Response(serializer.data)

    def put(self, request, exhibition_id):
        exhibition = get_object_or_404(Exhibition, id=exhibition_id)
        serializer = ExhibitionSerializer(
            exhibition,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "게시글이 수정되었습니다.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
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
            return Response(
                {"message": "좋아요", "likes": exhibition.likes.count()},
                status=status.HTTP_201_CREATED,
            )
        else:
            exhibition.likes.remove(request.user)
            return Response(
                {"message": "좋아요 취소", "likes": exhibition.likes.count()},
                status=status.HTTP_200_OK,
            )


class ExhibitionSearchView(APIView):
    def get(self, request):
        search = request.query_params.get("search", None)
        pagination = CustomPageNumberPagination()
        # 키워드가 있는 경우
        if search:
            # 내용, 제목, 장소 기준으로 검색
            exhibitions = Exhibition.objects.filter(
                Q(content__icontains=search)
                | Q(info_name__icontains=search)
                | Q(location__icontains=search)
            ).order_by("-created_at")
        else:
            exhibitions = Exhibition.objects.all().order_by("-created_at")
        paginated_exhibitions = pagination.paginate_queryset(exhibitions, request)
        serializer = ExhibitionSerializer(paginated_exhibitions, many=True)
        return Response(
            pagination.get_paginated_response(serializer.data),
            status=status.HTTP_200_OK,
        )
