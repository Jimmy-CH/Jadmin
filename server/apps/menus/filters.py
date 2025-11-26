
import django_filters
from .models import Menu


class MenuFilter(django_filters.FilterSet):
    keywords = django_filters.CharFilter(method='filter_keywords')
    status = django_filters.NumberFilter(field_name='visible')  # 1 显示，0 隐藏

    class Meta:
        model = Menu
        fields = ['keywords', 'status']

    def filter_keywords(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


