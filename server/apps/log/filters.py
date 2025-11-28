
import django_filters
from .models import OperationLog


class OperationLogFilter(django_filters.FilterSet):
    module = django_filters.CharFilter(lookup_expr="icontains")
    content = django_filters.CharFilter(lookup_expr="icontains")
    operator = django_filters.CharFilter(lookup_expr="icontains")
    ip = django_filters.CharFilter(lookup_expr="icontains")
    region = django_filters.CharFilter(lookup_expr="icontains")
    create_time_after = django_filters.DateTimeFilter(field_name="create_time", lookup_expr="gte")
    create_time_before = django_filters.DateTimeFilter(field_name="create_time", lookup_expr="lte")

    class Meta:
        model = OperationLog
        fields = ["module", "content", "operator", "ip", "region"]
