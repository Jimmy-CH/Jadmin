
from rest_framework import serializers
from .models import Department


class DeptFormSerializer(serializers.ModelSerializer):
    parentId = serializers.IntegerField(
        source='parent_id',
        allow_null=True,
        required=False
    )

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'parentId', 'status', 'sort']
        read_only_fields = ['id']

    def validate_parentId(self, value):
        if value is not None:
            if not Department.objects.filter(id=value).exists():
                raise serializers.ValidationError("父部门不存在")
        return value


class DeptTreeSerializer(serializers.ModelSerializer):
    parentId = serializers.IntegerField(source='parent_id', read_only=True)
    createTime = serializers.DateTimeField(source='create_time', read_only=True)
    updateTime = serializers.DateTimeField(source='update_time', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'parentId', 'name', 'code',
            'sort', 'status', 'children',
            'createTime', 'updateTime'
        ]

    def get_children(self, obj):
        # 递归获取子部门（注意：大数据量时建议非递归构建）
        children = Department.objects.filter(parent=obj).order_by('sort')
        return DeptTreeSerializer(children, many=True, context=self.context).data


