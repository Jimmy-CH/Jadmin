
import django_filters
from django.contrib.auth.models import User


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    nickname = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    status = django_filters.NumberFilter(field_name='profile__status')
    deptId = django_filters.NumberFilter(field_name='profile__dept_id')

    class Meta:
        model = User
        fields = ['username', 'nickname', 'status', 'deptId']

