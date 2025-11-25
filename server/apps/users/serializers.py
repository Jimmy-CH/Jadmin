
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CurrentUserDTOSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='id')
    username = serializers.CharField()
    nickname = serializers.CharField(source='userprofile.nickname', allow_null=True)
    avatar = serializers.CharField(source='userprofile.avatar', allow_null=True)
    roles = serializers.SerializerMethodField()
    perms = serializers.SerializerMethodField()

    class Meta:
        model = User  # 默认的 auth.User
        fields = ['userId', 'username', 'nickname', 'avatar', 'roles', 'perms']

    def get_roles(self, obj):
        return list(obj.groups.values_list('name', flat=True))

    def get_perms(self, obj):
        return [f"{p.content_type.app_label}.{p.codename}" for p in obj.user_permissions.all()]


