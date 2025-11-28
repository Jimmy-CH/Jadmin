
from rest_framework import serializers
from .models import OperationLog


class OperationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationLog
        fields = [
            "id",
            "module",
            "content",
            "request_uri",
            "method",
            "ip",
            "region",
            "browser",
            "os",
            "execution_time",
            "operator",
            "create_by",
            "create_time",
        ]
        # read_only_fields = fields  # 所有字段只读（符合日志特性）
