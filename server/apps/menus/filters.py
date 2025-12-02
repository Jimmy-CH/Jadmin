
import django_filters
from .models import Menu


class MenuFilter(django_filters.FilterSet):
    parent_isnull = django_filters.BooleanFilter(field_name='parent', lookup_expr='isnull')

    class Meta:
        model = Menu
        fields = ['parent', 'type', 'visible', 'parent_isnull']
