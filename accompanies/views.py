from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accompanies.models import Accompany, Apply
from accompanies.serializers import (
    AccompanySerializer,
    AccompanyCreateSerializer,
    ApplySerializer,
)
from exhibitions.models import Exhibition


class AccompanyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, exhibition_id):
        """동행 구하기 댓글 작성하기\n
        Args:
            request.data["content"] (char): 동행 구하기 내용\n
            request.data["personnel"] (int): 동행 목표 인원\n
            request.data["start_time"] (datetime): 모임 시작 시간\n
            request.data["end_time"] (datetime): 모임 종료 시간\n
            exhibition_id (int): 해당 댓글이 등록될 전시회 게시글의 pk값\n
        Returns:
            HTTP_201_CREATED : 댓글 등록 완료\n
            HTTP_400_BAD_REQUEST : 값이 제대로 입력되지 않음\n
            HTTP_401_UNAUTHORIZED : 로그인 하지 않은 사용자
        """
        serializer = AccompanyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(exhibition_id=exhibition_id, user=request.user)
        return Response(
            {"message": "동행 구하기 글이 등록되었습니다.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, accompany_id):
        """동행 구하기 댓글 수정하기\n
        Args:
            request.data["content"] (char): 동행 구하기 내용\n
            request.data["personnel"] (int): 동행 목표 인원\n
            request.data["start_time"] (datetime): 모임 시작 시간\n
            request.data["end_time"] (datetime): 모임 종료 시간\n
            accompany_id (int): 해당 동행 구하기 댓글의 pk값\n
        Returns:
            HTTP_200_OK : 댓글 수정 완료\n
            HTTP_400_BAD_REQUEST : 값이 제대로 입력되지 않음\n
            HTTP_401_UNAUTHORIZED : 로그인 하지 않은 사용자\n
            HTTP_403_FORBIDDEN : 권한이 없는 사용자
        """
        accompany = get_object_or_404(Accompany, id=accompany_id)
        if request.user == accompany.user:
            serializer = AccompanyCreateSerializer(
                accompany, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "동행 구하기 글이 수정되었습니다.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def delete(self, request, accompany_id):
        """동행 구하기 댓글 삭제하기\n
        Args:
            accompany_id (int): 해당 동행 구하기 댓글의 pk값\n
        Returns:
            HTTP_204_NO_CONTENT : 댓글 삭제 완료\n
            HTTP_401_UNAUTHORIZED : 로그인 하지 않은 사용자\n
            HTTP_403_FORBIDDEN : 권한이 없는 사용자
        """
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

    def post(self, request, accompany_id):
        """동행 신청하기 댓글 작성하기\n
        Args:
            request.data["content"] (char): 동행 신청하기 내용\n
            accompany_id (int): 해당 댓글이 등록될 동행 구하기 댓글의 pk값\n
        Returns:
            HTTP_201_CREATED : 댓글 등록 완료\n
            HTTP_400_BAD_REQUEST : 값이 제대로 입력되지 않음\n
            HTTP_401_UNAUTHORIZED : 로그인 하지 않은 사용자
        """
        serializer = ApplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, accompany_id=accompany_id)
        return Response(
            {"message": "동행 신청하기 댓글이 등록되었습니다.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, apply_id):
        """동행 신청하기 댓글 수정하기\n
        Args:
            request.data["content"] (char): 동행 신청하기 내용\n
            apply_id (int): 해당 동행 신청하기 댓글의 pk값\n
        Returns:
            HTTP_200_OK : 댓글 수정 완료\n
            HTTP_400_BAD_REQUEST : 값이 제대로 입력되지 않음\n
            HTTP_401_UNAUTHORIZED : 로그인 하지 않은 사용자\n
            HTTP_403_FORBIDDEN : 권한이 없는 사용자
        """
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
            return Response(
                {"message": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def delete(self, request, apply_id):
        """동행 신청하기 댓글 삭제하기\n
        Args:
            apply_id (int): 해당 동행 신청하기 댓글의 pk값\n
        Returns:
            HTTP_204_NO_CONTENT : 댓글 삭제 완료\n
            HTTP_401_UNAUTHORIZED : 로그인 하지 않은 사용자\n
            HTTP_403_FORBIDDEN : 권한이 없는 사용자
        """
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
                        {
                            "message": "목표 인원을 이미 채웠습니다. 인원을 수정하거나 다른 유저와의 동행을 취소하세요.",
                            "picks_count": accompany.picks.count(),
                        },
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
