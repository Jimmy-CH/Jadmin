
from rest_framework import serializers
from .models import Menu


class KeyValueSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()


class MenuFormSerializer(serializers.ModelSerializer):
    parentId = serializers.IntegerField(source='parent_id', required=False, allow_null=True)
    keepAlive = serializers.IntegerField(source='keep_alive', required=False)
    alwaysShow = serializers.IntegerField(source='always_show', required=False)
    params = KeyValueSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = [
            'id', 'parentId', 'name', 'type', 'routeName', 'routePath',
            'component', 'perm', 'visible', 'sort', 'icon', 'redirect',
            'keepAlive', 'alwaysShow', 'params'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'routeName': {'source': 'route_name'},
            'routePath': {'source': 'route_path'},
            'component': {'source': 'component'},
            'perm': {'source': 'perm'},
            'visible': {'source': 'visible'},
            'icon': {'source': 'icon'},
            'redirect': {'source': 'redirect'},
        }

    def validate_parentId(self, value):
        if value is not None and not Menu.objects.filter(id=value).exists():
            raise serializers.ValidationError("父菜单不存在")
        return value

    def to_internal_value(self, data):
        # 先正常解析
        validated_data = super().to_internal_value(data)
        # 单独处理 params：从 list[dict] 转为存储格式
        params = data.get('params')
        if params is not None:
            validated_data['params'] = params  # JSONField 直接存 list of dict
        return validated_data


class MenuTreeSerializer(serializers.ModelSerializer):
    parentId = serializers.IntegerField(source='parent_id', read_only=True)
    keepAlive = serializers.IntegerField(source='keep_alive', read_only=True)
    alwaysShow = serializers.IntegerField(source='always_show', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            'id', 'parentId', 'name', 'type', 'routeName', 'routePath',
            'component', 'perm', 'visible', 'sort', 'icon', 'redirect',
            'keepAlive', 'alwaysShow', 'children'
        ]
        extra_kwargs = {
            'routeName': {'source': 'route_name'},
            'routePath': {'source': 'route_path'},
            'component': {'source': 'component'},
            'perm': {'source': 'perm'},
            'visible': {'source': 'visible'},
            'icon': {'source': 'icon'},
            'redirect': {'source': 'redirect'},
        }

    def get_children(self, obj):
        children = Menu.objects.filter(parent=obj).order_by('sort')
        return MenuTreeSerializer(children, many=True, context=self.context).data

