
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Department
from .serializers import DeptFormSerializer, DeptTreeSerializer
from .filters import DeptFilter


class DeptViewSet(viewsets.ModelViewSet):
    """
    部门管理视图集
    - list: 获取树形部门列表（支持 keywords 过滤）
    - create: 新增部门
    - retrieve: 获取部门详情（扁平）
    - update / partial_update: 更新部门
    - destroy: 删除部门（级联删除子部门？根据业务决定）
    """
    queryset = Department.objects.all()
    filter_class = DeptFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return DeptTreeSerializer
        return DeptFormSerializer

    def get_queryset(self):
        if self.action == 'list':
            # 只查询根节点，由序列化器递归展开 children
            return Department.objects.filter(parent__isnull=True).order_by('sort')
        return Department.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": "200",
            "msg": "查询成功",
            "data": serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dept = serializer.save()
        return Response({
            "code": "200",
            "msg": "新增部门成功",
            "data": {}
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "code": "200",
            "msg": "更新部门成功",
            "data": {}
        })

    def partial_update(self, request, *args, **kwargs):
        # 支持 PATCH（可选）
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 检查是否有子部门，防止误删
        if instance.department_set.exists():
            return Response({"code": "400", "msg": "请先删除子部门", "data": {}}, status=400)
        instance.delete()
        return Response({
            "code": "200",
            "msg": "删除成功",
            "data": {}
        })

