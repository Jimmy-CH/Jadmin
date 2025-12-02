
import uuid
import time
from django.core.cache import cache
from apps.authentication.utils import generate_captcha
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    authentication_classes = []  # 不需要认证
    permission_classes = []      # 允许任何人访问

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                "code": "400",
                "msg": "用户名或密码不能为空",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                "code": "401",
                "msg": "用户名或密码错误",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)

        # 生成 token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "code": "200",
            "msg": "登录成功",
            "data": {
                "tokenType": "Bearer",
                "accessToken": access_token,
                "refreshToken": refresh_token,
                "expiresIn": 1800  # 30分钟，单位秒
            }
        }, status=status.HTTP_200_OK)


class CaptchaView(APIView):
    """获取登录验证码"""
    authentication_classes = []  # 无需认证
    permission_classes = []      # 无需权限

    def get(self, request):
        # 生成验证码内容和图片
        captcha_text, captcha_base64 = generate_captcha()

        # 生成唯一 key
        captcha_key = str(uuid.uuid4())

        # 存入缓存，5 分钟有效
        cache.set(f"captcha:{captcha_key}", captcha_text, timeout=300)

        return Response({
            "code": "200",
            "msg": "success",
            "data": {
                "captchaKey": captcha_key,
                "captchaBase64": f"data:image/png;base64,{captcha_base64}"
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    注销登录：将当前 Access Token 对应的 Refresh Token 加入黑名单
    （假设前端在登录时保存了 refresh token；若只传 access token，则无法直接黑名单）

    但注意：SimpleJWT 默认只能黑名单 refresh token。

    方案一（推荐）：前端在 logout 时同时传 refresh token（放在 body 或 header）
    方案二：仅使当前 access token 在应用层“视为无效”（需自定义缓存机制）

    由于本接口只接收 Authorization header（access token），我们采用方案二：
    —— 将 access token 加入短期黑名单（使用缓存）
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        # 获取当前 access token（从 request.auth）
        # request.auth 是 UntypedToken 实例（已验证过的 payload）
        token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')

        if not token:
            return Response({
                "code": "400",
                "msg": "缺少 Authorization 头",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

        # 获取 token 过期时间（从已解析的 token payload）
        payload = request.auth  # 已验证的 token payload
        exp = payload.get('exp')
        now = int(time.time())
        ttl = exp - now  # 剩余有效时间（秒）

        if ttl > 0:
            # 将 token 加入缓存黑名单，有效期为剩余时间
            cache.set(f"blacklisted_token:{token}", True, timeout=ttl)

        return Response({
            "code": "200",
            "msg": "注销成功",
            "data": {}
        }, status=status.HTTP_200_OK)
