from rest_framework import viewsets, status
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
        # 如果要排除 BUTTON 类型：
        menus = Menu.objects.filter(visible=True).exclude(type='BUTTON').order_by('sort', 'id')
        menus_with_children = Menu.objects.filter(id__in=[m.id for m in menus]).prefetch_related('children')
        menu_list = list(menus_with_children)
        tree = build_tree(menu_list)
        data = [MenuRouteSerializer(node, context={'request': request}).data for node in tree]
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

    def get_queryset(self):
        """可选：重写 get_queryset 以支持过滤"""
        queryset = super().get_queryset()
        return queryset

    def list(self, request, *args, **kwargs):
        """重写 list，返回树形结构"""
        queryset = self.filter_queryset(self.get_queryset())
        # 预加载 children 以优化性能并供 build_tree 使用
        queryset_with_children = queryset.prefetch_related('children')
        menu_list = list(queryset_with_children)
        tree = build_tree(menu_list)
        data = MenuTreeSerializer(tree, many=True, context={'request': request}).data
        return Response({"code": "200", "msg": "一切ok", "data": data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            menu = serializer.save()
            return Response({
                "code": "200",
                "msg": f"新增菜单{menu.name}成功",
                "data": None
            }, status=status.HTTP_201_CREATED) # 成功创建应返回 201
        return Response({"code": "500", "msg": "请求参数异常", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) # 返回错误详情

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
        return Response({"code": "500", "msg": "请求参数异常", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        menu_id = instance.id
        try:
            instance.delete()
            return Response({
                "code": "200",
                "msg": f"删除菜单{menu_id}成功",
                "data": None
            })
        except Exception as e:
            return Response({"code": "500", "msg": f"删除失败: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MenuOptionsView(APIView):
    """GET /menus/options —— 下拉树选项"""
    def get(self, request):
        # 过滤可见菜单
        menus = Menu.objects.filter(visible=True).order_by('sort', 'id')
        # 预加载 children
        menus_with_children = menus.prefetch_related('children')
        menu_list = list(menus_with_children)
        tree = build_tree(menu_list)
        data = MenuOptionSerializer(tree, many=True, context={'request': request}).data
        return Response({"code": "200", "msg": "一切ok", "data": data})


class MenuFormView(APIView):
    """GET /menus/{id}/form"""
    def get(self, request, id):
        menu = get_object_or_404(Menu, id=id)
        data = MenuFormSerializer(menu, context={'request': request}).data
        return Response({"code": "200", "msg": "一切ok", "data": data})

