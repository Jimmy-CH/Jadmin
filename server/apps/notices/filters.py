
import django_filters
from .models import Notice


class NoticeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    type = django_filters.ChoiceFilter(choices=Notice.TYPE_CHOICES)
    level = django_filters.ChoiceFilter(choices=Notice.LEVEL_CHOICES)
    publish_status = django_filters.ChoiceFilter(choices=Notice.PUBLISH_STATUS_CHOICES)
    publisher_name = django_filters.CharFilter(lookup_expr="icontains")
    publish_time_after = django_filters.DateTimeFilter(field_name="publish_time", lookup_expr="gte")
    publish_time_before = django_filters.DateTimeFilter(field_name="publish_time", lookup_expr="lte")

    class Meta:
        model = Notice
        fields = ["title", "type", "level", "publish_status", "publisher_name"]
