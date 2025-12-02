
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
            'keep_alive', 'always_show', 'children'
        ]

    def get_children(self, obj):
        """
        获取子节点数据。
        优先使用 build_tree 生成的 _cached_children 属性，
        如果没有，则回退到 ORM 的 children 关联（效率较低）。
        """
        # 检查是否有 build_tree 预先计算好的子节点列表
        if hasattr(obj, '_cached_children'):
            return MenuTreeSerializer(obj._cached_children, many=True, context=self.context).data
        elif hasattr(obj, 'children'):
            return MenuTreeSerializer(obj.children.all(), many=True, context=self.context).data
        else:
            return []


class MenuRouteSerializer(serializers.ModelSerializer):
    """专用于 /menus/routes，输出前端路由所需结构"""
    class Meta:
        model = Menu
        fields = []  # 不直接使用字段，手动构建

    def to_representation(self, instance):
        # 处理 meta 字段
        meta = {
            "title": instance.name,
            "icon": instance.icon or "",             # 如果没有图标，则为空字符串
            "hidden": not bool(instance.visible),    # visible=False -> hidden=True
            "keepAlive": bool(instance.keep_alive),
            "alwaysShow": bool(instance.always_show),
            "params": getattr(instance, 'params', None),
        }

        # 构建基础路由对象
        route = {
            "path": instance.route_path or "",
            # name 优先使用 route_name，否则用菜单名
            "name": instance.route_name or instance.name,
            "meta": meta,
        }

        # 添加可选字段
        if instance.component:
            route["component"] = instance.component

        if instance.redirect:
            route["redirect"] = instance.redirect

        # --- 递归处理子路由 ---
        # 优先使用 build_tree 生成的 _cached_children 属性
        children_to_serialize = []
        if hasattr(instance, '_cached_children'):
            children_to_serialize = instance._cached_children
        elif hasattr(instance, 'children'):
            children_to_serialize = instance.children.all()

        if children_to_serialize:
            route["children"] = [
                MenuRouteSerializer(child, context=self.context).data for child in children_to_serialize
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
        """
        获取子节点数据（用于选项）。
        优先使用 build_tree 生成的 _cached_children 属性。
        """
        if hasattr(obj, '_cached_children'):
            return MenuOptionSerializer(obj._cached_children, many=True, context=self.context).data
        elif hasattr(obj, 'children'):
            return MenuOptionSerializer(obj.children.all(), many=True, context=self.context).data
        else:
            return []


class MenuFormSerializer(serializers.ModelSerializer):
    """用于表单编辑/新增"""
    class Meta:
        model = Menu
        fields = '__all__'
