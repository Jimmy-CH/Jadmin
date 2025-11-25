
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers import CurrentUserDTOSerializer


class CurrentUserView(APIView):
    """获取当前登录用户信息"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CurrentUserDTOSerializer(user)
        return Response({
            "code": "200",
            "msg": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
