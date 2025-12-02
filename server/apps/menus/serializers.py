
from rest_framework import serializers
from .models import Menu


class MenuTreeSerializer(serializers.ModelSerializer):
    """用于 /menus 和 /menus/options 的递归序列化"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            'id', 'name', 'parent', 'type', 'route_name', 'route_path',
            'component', 'perm', 'visible', 'sort', 'icon', 'redirect',
            'keep_alive', 'always_show', 'params', 'children'
        ]

    def get_children(self, obj):
        if hasattr(obj, 'children'):
            return MenuTreeSerializer(obj.children, many=True, context=self.context).data
        return []


class MenuRouteSerializer(serializers.ModelSerializer):
    """专用于 /menus/routes，输出前端路由所需结构"""
    class Meta:
        model = Menu
        fields = []  # 不直接使用字段，手动构建

    def to_representation(self, instance):
        meta = {
            "title": instance.name,
            "icon": instance.icon or "",
            "hidden": not bool(instance.visible),
            "keepAlive": bool(instance.keep_alive),
            "alwaysShow": bool(instance.always_show),
            "params": instance.params or None,
        }

        route = {
            "path": instance.route_path,
            "name": instance.route_name or instance.name,
            "meta": meta,
        }

        if instance.component:
            route["component"] = instance.component

        if instance.redirect:
            route["redirect"] = instance.redirect

        if hasattr(instance, 'children') and instance.children:
            route["children"] = [
                self.__class__(child).data for child in instance.children
            ]

        return route


class MenuOptionSerializer(serializers.ModelSerializer):
    """用于 /menus/options 下拉树"""
    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name')
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['value', 'label', 'children']

    def get_children(self, obj):
        if hasattr(obj, 'children'):
            return MenuOptionSerializer(obj.children, many=True, context=self.context).data
        return []


class MenuFormSerializer(serializers.ModelSerializer):
    """用于表单编辑/新增"""
    class Meta:
        model = Menu
        fields = '__all__'

