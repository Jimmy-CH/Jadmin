
import django_filters
from .models import Department


class DeptFilter(django_filters.FilterSet):
    keywords = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Department
        fields = ['keywords']

