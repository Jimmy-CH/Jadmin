
from django.db import models


class Dict(models.Model):
    name = models.CharField("字典名称", max_length=100)
    dict_code = models.CharField("字典编码", max_length=100, unique=True)
    remark = models.TextField("备注", blank=True, null=True)
    status = models.IntegerField("状态", choices=((1, "启用"), (0, "禁用")), default=1)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 'sys_dict'
        verbose_name = "字典"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} ({self.dict_code})"

