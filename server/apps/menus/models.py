
from django.db import models


class Menu(models.Model):
    MENU_TYPE_CHOICES = [
        ('CATALOG', '目录'),
        ('MENU', '菜单'),
        ('BUTTON', '按钮'),
        ('EXTLINK', '外链'),
    ]

    id = models.IntegerField(primary_key=True, verbose_name="菜单ID")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="父级菜单"
    )
    name = models.CharField(max_length=100, verbose_name="菜单名称")
    type = models.CharField(max_length=20, choices=MENU_TYPE_CHOICES, verbose_name="类型")
    route_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="路由名称")
    route_path = models.CharField(max_length=200, blank=True, verbose_name="路由路径")
    component = models.CharField(max_length=200, blank=True, verbose_name="组件路径")
    sort = models.IntegerField(default=0, verbose_name="排序")
    visible = models.BooleanField(default=True, verbose_name="是否可见")
    icon = models.CharField(max_length=100, blank=True, verbose_name="图标")
    redirect = models.CharField(max_length=200, blank=True, verbose_name="重定向路径")
    perm = models.CharField(max_length=200, blank=True, null=True, verbose_name="权限标识")
    params = models.JSONField(blank=True, null=True, verbose_name="路由参数")
    # 新增字段
    keep_alive = models.IntegerField(default=0, choices=[(1, '开启'), (0, '关闭')], verbose_name="是否开启页面缓存")
    always_show = models.IntegerField(default=0, choices=[(1, '始终显示'), (0, '自动隐藏')], verbose_name="只有一个子路由时是否始终显示")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'menus'
        verbose_name = "菜单"
        verbose_name_plural = "菜单管理"
        ordering = ['sort']

    def __str__(self):
        return self.name
