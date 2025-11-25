
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    authentication_classes = []  # 不需要认证
    permission_classes = []      # 允许任何人访问

    def post(self, request):
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        if not username or not password:
            return Response({
                "code": "A0001",
                "msg": "用户名或密码不能为空",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                "code": "A0002",
                "msg": "用户名或密码错误",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)

        # 生成 token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "code": "A0000",
            "msg": "登录成功",
            "data": {
                "tokenType": "Bearer",
                "accessToken": access_token,
                "refreshToken": refresh_token,
                "expiresIn": 1800  # 30分钟，单位秒
            }
        }, status=status.HTTP_200_OK)

