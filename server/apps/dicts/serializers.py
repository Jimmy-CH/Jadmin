
from rest_framework import serializers
from .models import Dict


class DictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dict
        fields = ['id', 'name', 'dict_code', 'remark', 'status']
        read_only_fields = ['id']

    def validate_dict_code(self, value):
        # 创建时检查唯一性（更新时排除自身）
        queryset = Dict.objects.filter(dict_code=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("字典编码已存在")
        return value


