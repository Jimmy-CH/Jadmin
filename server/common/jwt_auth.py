
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache


class BlacklistJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        # 检查是否在黑名单中
        token_str = raw_token.decode('utf-8')
        if cache.get(f"blacklisted_token:{token_str}"):
            raise AuthenticationFailed('Token 已注销')

        validated_token = self.get_validated_token(raw_token)
        return (self.get_user(validated_token), validated_token)


