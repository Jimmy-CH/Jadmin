
from rest_framework import serializers
from .models import Role


class RoleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'sort', 'status', 'dataScope']
        read_only_fields = ['id']

    # 将驼峰 dataScope 映射到下划线 data_scope
    dataScope = serializers.IntegerField(source='data_scope', required=False)

    def validate_code(self, value):
        # 创建时检查 code 唯一性（更新时排除自身）
        queryset = Role.objects.filter(code=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("角色编码已存在")
        return value

    def validate_name(self, value):
        queryset = Role.objects.filter(name=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("角色名称已存在")
        return value


class RoleListSerializer(serializers.ModelSerializer):
    dataScope = serializers.IntegerField(source='data_scope')
    createTime = serializers.DateTimeField(source='create_time')
    updateTime = serializers.DateTimeField(source='update_time')

    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'sort', 'status', 'dataScope', 'createTime', 'updateTime']


