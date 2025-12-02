from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Menu
from .serializers import (
    MenuRouteSerializer,
    MenuTreeSerializer,
    MenuOptionSerializer,
    MenuFormSerializer
)
from .filters import MenuFilter
from .utils import build_tree


class MenuRouteView(APIView):
    """GET /menus/routes —— 前端路由结构"""
    def get(self, request):
        menus = Menu.objects.filter(visible=1).exclude(type=4).order_by('sort', 'id')
        tree = build_tree(list(menus))
        data = [MenuRouteSerializer(node).data for node in tree]
        return Response({"code": "200", "msg": "一切ok", "data": data})


class MenuViewSet(viewsets.ModelViewSet):
    """
    菜单管理视图集
    - list: GET /menus/ → 树形表格（含按钮）
    - create: POST /menus/
    - retrieve: GET /menus/{id}/ → 一般不用，但可保留
    - update: PUT /menus/{id}/
    - destroy: DELETE /menus/{id}/
    """
    queryset = Menu.objects.all().order_by('sort', 'id')
    serializer_class = MenuFormSerializer  # 默认用于 create/update
    filterset_class = MenuFilter

    def list(self, request, *args, **kwargs):
        """重写 list，返回树形结构"""
        queryset = self.filter_queryset(self.get_queryset())
        tree = build_tree(list(queryset))
        data = MenuTreeSerializer(tree, many=True).data
        return Response({"code": "200", "msg": "一切ok", "data": data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            menu = serializer.save()
            return Response({
                "code": "200",
                "msg": f"新增菜单{menu.name}成功",
                "data": None
            })
        return Response({"code": "500", "msg": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            updated = serializer.save()
            return Response({
                "code": "200",
                "msg": f"修改菜单{updated.name}成功",
                "data": None
            })
        return Response({"code": "500", "msg": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        menu_id = instance.id
        instance.delete()
        return Response({
            "code": "200",
            "msg": f"删除菜单{menu_id}成功",
            "data": None
        })


class MenuOptionsView(APIView):
    """GET /menus/options —— 下拉树选项"""
    def get(self, request):
        menus = Menu.objects.filter(visible=1).order_by('sort', 'id')
        tree = build_tree(list(menus))
        data = MenuOptionSerializer(tree, many=True).data
        return Response({"code": "200", "msg": "一切ok", "data": data})


class MenuFormView(APIView):
    """GET /menus/{id}/form"""
    def get(self, request, id):
        menu = get_object_or_404(Menu, id=id)
        data = MenuFormSerializer(menu).data
        return Response({"code": "200", "msg": "一切ok", "data": data})

