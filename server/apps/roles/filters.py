# filters.py
import django_filters
from .models import Role
from django.db import models


class RoleFilter(django_filters.FilterSet):
    keywords = django_filters.CharFilter(method='filter_keywords')

    class Meta:
        model = Role
        fields = ['status']

    def filter_keywords(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(code__icontains=value)
        )

