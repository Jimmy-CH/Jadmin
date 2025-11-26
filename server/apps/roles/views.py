
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Role
from .serializers import RoleFormSerializer, RoleListSerializer
from .filters import RoleFilter


class RoleViewSet(viewsets.ModelViewSet):
    """
    角色管理：增删改查
    """
    queryset = Role.objects.all().order_by('sort', '-create_time')
    filterset_class = RoleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RoleListSerializer
        return RoleFormSerializer

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()
        return Response({
            "code": "200",
            "msg": "新增角色成功",
            "data": {}
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "code": "200",
            "msg": "更新角色成功",
            "data": {}
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "code": "200",
            "msg": "删除成功",
            "data": {}
        })

