
from rest_framework import serializers
from .models import Notice
from django.utils import timezone


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            "id",
            "title",
            "publish_status",
            "type",
            "publisher_name",
            "level",
            "publish_time",
            "create_time",
            "revoke_time",
            "content",
            "target_type",
        ]
        read_only_fields = ["id", "create_time"]  # 创建时间由系统自动设置

    def validate_publish_time(self, value):
        """可选：校验发布时间不能早于当前时间（若业务要求）"""
        if value < timezone.now():
            raise serializers.ValidationError("发布时间不能早于当前时间")
        return value
