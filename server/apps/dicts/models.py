
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


class DictItem(models.Model):
    """
    字典项模型：用于存储字典（Dict）下的具体选项值
    例如：字典 "gender" 下的 ["男", "女", "保密"]
    """
    dict_code = models.CharField("字典编码", max_length=100, db_index=True)
    label = models.CharField("显示标签", max_length=100)
    value = models.CharField("实际值", max_length=100)
    sort = models.IntegerField("排序", default=0)
    status = models.IntegerField(
        "状态",
        choices=((1, "启用"), (0, "禁用")),
        default=1
    )
    tag = models.CharField(
        "标签类型（前端展示用）",
        max_length=50,
        blank=True,
        null=True,
        help_text="如: 'success', 'warning', 'danger', 'info' 等"
    )
    remark = models.TextField("备注", blank=True, null=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 'sys_dict_item'
        verbose_name = "字典项"
        verbose_name_plural = verbose_name
        ordering = ['sort', 'id']
        # 可选：确保同一字典下 value 唯一
        # unique_together = [('dict_code', 'value')]

    def __str__(self):
        return f"{self.label} ({self.value}) [{self.dict_code}]"

