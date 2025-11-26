
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="部门名称")
    code = models.CharField(max_length=50, blank=True, verbose_name="部门编号")  # 新增
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="上级部门"
    )
    sort = models.IntegerField(default=0, verbose_name="排序")
    status = models.IntegerField(
        default=1,
        choices=[(1, '启用'), (0, '禁用')],
        verbose_name="状态"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'departments'
        verbose_name = "部门"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
