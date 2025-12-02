
from django.db import models


class Menu(models.Model):
    MENU_TYPE_CHOICES = (
        ("MENU", '菜单'),
        ("CATALOG", '目录'),
        ("LINK", '外链'),
        ("BUTTON", '按钮'),
    )

    name = models.CharField(max_length=100, verbose_name="菜单名称")
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="父菜单"
    )
    type = models.CharField(max_length=20, default="MENU", choices=MENU_TYPE_CHOICES, verbose_name="菜单类型")
    route_name = models.CharField(max_length=100, blank=True, verbose_name="路由名称")
    route_path = models.CharField(max_length=200, blank=True, verbose_name="路由路径")
    component = models.CharField(max_length=200, blank=True, verbose_name="组件路径")
    perm = models.CharField(max_length=100, blank=True, verbose_name="权限标识")
    visible = models.IntegerField(
        default=1,
        choices=[(1, '显示'), (0, '隐藏')],
        verbose_name="是否可见"
    )
    sort = models.IntegerField(default=0, verbose_name="排序")
    icon = models.CharField(max_length=100, blank=True, verbose_name="图标")
    redirect = models.CharField(max_length=200, blank=True, verbose_name="跳转路径")

    # 新增字段
    keep_alive = models.IntegerField(
        default=0,
        choices=[(1, '开启'), (0, '关闭')],
        verbose_name="是否开启页面缓存"
    )
    always_show = models.IntegerField(
        default=0,
        choices=[(1, '始终显示'), (0, '自动隐藏')],
        verbose_name="只有一个子路由时是否始终显示"
    )
    params = models.JSONField(blank=True, null=True, verbose_name="路由参数")  # 存 [ {"key": "...", "value": "..."} ]

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'menus'
        verbose_name = "菜单"
        verbose_name_plural = verbose_name
        ordering = ['sort', 'id']

    def __str__(self):
        return self.name

