
import django_filters
from .models import Dict


class DictFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    dict_code = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.NumberFilter()

    class Meta:
        model = Dict
        fields = ['name', 'dict_code', 'status']


