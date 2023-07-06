from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from accompanies.models import Accompany, Apply
from accompanies.serializers import AccompanySerializer, ApplySerializer


class AccompanyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, exhibition_id):  # 동행 구하기 댓글 작성하기
        serializer = AccompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, exhibition_id=exhibition_id)
        return Response(
            {"message": "동행 구하기 글이 등록되었습니다.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, accompany_id):  # 동행 구하기 댓글 수정하기
        accompany = get_object_or_404(Accompany, id=accompany_id)
        if request.user == accompany.user:
            serializer = AccompanySerializer(accompany, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "동행 구하기 글이 수정되었습니다.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, accompany_id):  # 동행 구하기 댓글 삭제하기
        accompany = get_object_or_404(Accompany, id=accompany_id)
        if request.user == accompany.user:
            accompany.delete()
            return Response(
                {"message": "동행 구하기 글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class ApplyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, accompany_id):  # 동행 신청하기 댓글 작성하기
        serializer = ApplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, accompany_id=accompany_id)
        return Response(
            {"message": "동행 신청하기 댓글이 등록되었습니다.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, apply_id):  # 동행 신청하기 댓글 수정하기
        apply = get_object_or_404(Apply, id=apply_id)
        if request.user == apply.user:
            serializer = ApplySerializer(apply, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "동행 신청하기 댓글이 수정되었습니다.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, apply_id):  # 동행 신청하기 댓글 삭제하기
        apply = get_object_or_404(Apply, id=apply_id)
        if request.user == apply.user:
            apply.delete()
            return Response(
                {"message": "동행 신청하기 댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class AccompanyPickView(APIView):  # 동행 채택하기 기능
    def post(self, request, accompany_id, apply_id):
        accompany = get_object_or_404(Accompany, id=accompany_id)
        apply = get_object_or_404(Apply, id=apply_id)
        if request.user == accompany.user:
            if apply.user not in accompany.picks.all():
                if accompany.picks.count() < accompany.personnel:
                    accompany.picks.add(apply.user)
                    return Response(
                        {
                            "message": "채택 완료",
                            "personnel": accompany.personnel,
                            "picks_count": accompany.picks.count(),
                        },
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"message": "목표 인원을 이미 채웠습니다. 인원을 수정하거나 다른 유저와의 동행을 취소하세요."},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                accompany.picks.remove(apply.user)
                return Response(
                    {
                        "message": "채택 취소",
                        "personnel": accompany.personnel,
                        "picks_count": accompany.picks.count(),
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
