
from django.db import models
from django.contrib.auth.models import User
from apps.dept.models import Department
from apps.roles.models import Role


class UserProfile(models.Model):
    GENDER_CHOICES = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="用户"
    )
    mobile = models.CharField(max_length=11, blank=True, verbose_name="手机号码")
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0, verbose_name="性别")
    avatar = models.URLField(blank=True, verbose_name="头像")
    status = models.IntegerField(default=1, verbose_name="状态", help_text="1: 正常; 0: 禁用")
    open_id = models.CharField(max_length=100, blank=True, verbose_name="微信OpenID")

    # 外键：部门（多对一）
    dept = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="所属部门"
    )

    # 多对多：角色
    roles = models.ManyToManyField(
        Role,
        blank=True,
        related_name='users',
        verbose_name="角色"
    )

    class Meta:
        db_table = 'user_profile'
        verbose_name = "用户资料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}'s profile"

