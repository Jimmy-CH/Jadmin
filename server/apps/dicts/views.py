
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Dict
from .serializers import DictSerializer
from .filters import DictFilter


class DictViewSet(viewsets.ModelViewSet):
    """
    字典管理：增删改查
    """
    queryset = Dict.objects.all()
    serializer_class = DictSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DictFilter
    search_fields = ['name', 'dict_code']  # 支持全局搜索
    ordering_fields = ['id', 'created_at']

    # 可选：自定义成功响应格式（根据你的 ResultObject）
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "code": "200",
            "msg": "操作成功",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "code": "200",
            "msg": "操作成功",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "code": "200",
            "msg": "删除成功",
            "data": {}
        })


