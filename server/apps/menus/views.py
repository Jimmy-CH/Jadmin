
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Menu
from .serializers import MenuFormSerializer, MenuTreeSerializer
from .filters import MenuFilter


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    filterset_class = MenuFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return MenuTreeSerializer
        return MenuFormSerializer

    def get_queryset(self):
        if self.action == 'list':
            # 只返回根节点，由序列化器递归构建树
            return Menu.objects.filter(parent__isnull=True).order_by('sort')
        return Menu.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": "200",
            "msg": "查询成功",
            "data": serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu = serializer.save()
        return Response({
            "code": "200",
            "msg": "新增菜单成功",
            "data": {}
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "code": "200",
            "msg": "更新菜单成功",
            "data": {}
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()  # CASCADE 会自动删子菜单
        return Response({
            "code": "200",
            "msg": "删除成功",
            "data": {}
        })


