
from django.db import models


class OperationLog(models.Model):
    module = models.CharField("功能模块", max_length=100)
    content = models.CharField("操作内容", max_length=255)
    request_uri = models.CharField("请求地址", max_length=255)
    method = models.CharField("请求方法", max_length=20, blank=True, null=True)
    ip = models.GenericIPAddressField("IP地址", blank=True, null=True)
    region = models.CharField("地区", max_length=100, blank=True, null=True)
    browser = models.CharField("浏览器", max_length=100, blank=True, null=True)
    os = models.CharField("操作系统", max_length=100, blank=True, null=True)
    execution_time = models.IntegerField("执行耗时(ms)", help_text="单位：毫秒")
    operator = models.CharField("操作人", max_length=100, blank=True, null=True)
    create_by = models.CharField("创建人ID", max_length=50, blank=True, null=True)
    create_time = models.DateTimeField("操作时间")

    class Meta:
        db_table = 'sys_operation_log'
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name
        ordering = ['-create_time', '-id']

    def __str__(self):
        return f"[{self.module}] {self.content} - {self.operator}"



