
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notice
from .serializers import NoticeSerializer
from .filters import NoticeFilter


class NoticeViewSet(viewsets.ModelViewSet):
    """
    通知公告视图集 - 支持完整 CRUD
    """
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]  # 需登录
    filterset_class = NoticeFilter
    search_fields = ["title", "publisher_name", "content"]
    ordering_fields = ["publish_time", "create_time", "level", "id"]
    ordering = ["-publish_time"]

    def perform_create(self, serializer):
        # 自动设置 create_time 为当前时间（如果模型未设 auto_now_add）
        serializer.save(create_time=timezone.now())

    def destroy(self, request, *args, **kwargs):
        """软删除 or 真实删除？此处为真实删除，可根据需求改为标记删除"""
        return super().destroy(request, *args, **kwargs)
