
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Department, Role


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


class UserProfileSerializer(serializers.ModelSerializer):
    deptId = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='dept',
        allow_null=True,
        required=False
    )
    roleIds = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Role.objects.all(),
        source='roles',
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['mobile', 'gender', 'avatar', 'status', 'open_id', 'deptId', 'roleIds']

    # 可选：输出时也显示 deptId 和 roleIds 为 ID 列表
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['deptId'] = instance.dept_id  # 直接输出 ID
        data['roleIds'] = list(instance.roles.values_list('id', flat=True))
        return data


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    nickname = serializers.CharField(source='first_name', required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'profile']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': False},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        first_name = validated_data.get('first_name', '')

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=first_name
        )
        user.set_unusable_password()
        user.save()

        # 安全创建或获取 Profile
        profile, created = UserProfile.objects.get_or_create(user=user)

        # 更新普通字段
        for attr, value in profile_data.items():
            if attr not in ['dept', 'roles']:
                setattr(profile, attr, value)

        # 处理外键和多对多
        if 'dept' in profile_data:
            profile.dept = profile_data['dept']
        if 'roles' in profile_data:
            profile.roles.set(profile_data['roles'])

        profile.save()
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # 安全获取或创建 Profile（兼容旧用户）
        profile, created = UserProfile.objects.get_or_create(user=instance)

        # 更新普通字段
        for attr, value in profile_data.items():
            if attr not in ['dept', 'roles']:
                setattr(profile, attr, value)

        # 处理外键和多对多
        if 'dept' in profile_data:
            profile.dept = profile_data['dept']
        if 'roles' in profile_data:
            profile.roles.set(profile_data['roles'])

        profile.save()
        return instance
