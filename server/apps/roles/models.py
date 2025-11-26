
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="角色名称")
    code = models.CharField(max_length=50, unique=True, verbose_name="角色编码")
    description = models.TextField(blank=True, verbose_name="描述")
    status = models.IntegerField(
        default=1,
        choices=[(1, '正常'), (0, '停用')],
        verbose_name="角色状态"
    )
    sort = models.IntegerField(default=0, verbose_name="排序")
    data_scope = models.IntegerField(
        default=1,
        verbose_name="数据权限",
        help_text="1:全部; 2:本部门及子部门; 3:本部门; 4:本人"
    )  # 新增字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'roles'
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
