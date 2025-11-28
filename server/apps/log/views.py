
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import OperationLog
from .serializers import OperationLogSerializer
from .filters import OperationLogFilter


class OperationLogViewSet(viewsets.ModelViewSet):
    """
    操作日志视图集
    """
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    permission_classes = [IsAuthenticated]  # 需登录
    filterset_class = OperationLogFilter
    search_fields = ["module", "content", "operator", "ip", "region"]
    ordering_fields = ["create_time", "execution_time", "id"]
    ordering = ["-create_time"]  # 默认按时间倒序
