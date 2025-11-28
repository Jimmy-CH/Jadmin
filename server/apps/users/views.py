from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers import CurrentUserDTOSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .filters import UserFilter


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


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理视图集
    - list: 获取用户列表（支持过滤）
    - create: 新增用户
    - retrieve: 获取用户详情
    - update / partial_update: 更新用户
    - destroy: 删除用户
    """
    queryset = (
        User.objects
        .select_related('profile__dept')
        .prefetch_related('profile__roles')
        .order_by('-id')
    )
    serializer_class = UserSerializer
    filterset_class = UserFilter
    ordering = ['-id']

    def get_serializer_context(self):
        # 如有需要可传递额外上下文
        return super().get_serializer_context()

    @action(detail=True, methods=['get'],  url_path='form')
    def form(self, request, pk=None):
        """获取用户表单数据（用于编辑）"""
        user = self.get_object()
        serializer = UserSerializer(user, context=self.get_serializer_context())
        return Response({
            "code": "200",
            "msg": "success",
            "data": serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # 使用完整序列化器返回数据（含 profile）
        output_serializer = UserSerializer(user, context=self.get_serializer_context())
        return Response({
            "code": "200",
            "msg": "新增用户成功",
            "data": output_serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        output_serializer = UserSerializer(user, context=self.get_serializer_context())
        return Response({
            "code": "200",
            "msg": "更新用户成功",
            "data": output_serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "code": "200",
            "msg": "删除成功",
            "data": {}
        }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "code": "200",
                "msg": "查询成功",
                "data": serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": "200",
            "msg": "查询成功",
            "data": serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "code": "200",
            "msg": "查询成功",
            "data": serializer.data
        })
