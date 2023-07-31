import datetime

from django.db.models import Count
from django.db.models.query_utils import Q

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from exhibitions.models import Exhibition
from exhibitions.recommend_ml import recommendation, set_data_updated
from exhibitions.serializers import (
    ExhibitionSerializer,
    ExhibitionDetailSerializer,
    TopFiveExhibitionSerializer,
)


class ExhibitionView(APIView):
    def get_permissions(self):  # 권한 설정
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

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
        serializer = ExhibitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            set_data_updated()
            return Response(
                {"message": "게시글이 등록되었습니다.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "요청이 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
            )


class ExhibitionDetailView(APIView):
    def get_permissions(self):  # 권한 설정
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAdminUser()]

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
    permission_classes = [IsAuthenticated]  # 권한 설정

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
    def get(self, request):  # 전시 검색 기능
        search = request.query_params.get("search", None)
        pagination = PageNumberPagination()
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
        return pagination.get_paginated_response(serializer.data)


class PopularExhibitionView(APIView):
    def get(self, request):  # 전시 좋아요 탑5 인기랭킹 조회
        q = Q()
        today = datetime.date.today()
        # 현재 날짜 기준으로 예약 가능한 전시회만 보여주기
        q.add(Q(start_date__lte=today), q.AND)
        q.add(Q(end_date__gte=today), q.AND)
        q.add(Q(svstatus="접수중"), q.AND)
        exhibitions = (
            Exhibition.objects.filter(q)
            .annotate(total_likes=Count("likes"))
            .order_by("-total_likes")[:5]
        )
        serializer = TopFiveExhibitionSerializer(exhibitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
