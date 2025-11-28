
from django.db import models


class Notice(models.Model):
    """
    通知公告模型
    """

    # 发布状态
    PUBLISH_STATUS_CHOICES = [
        (0, "未发布"),
        (1, "已发布"),
    ]

    # 通知类型（可扩展）
    TYPE_CHOICES = [
        (1, "系统更新"),
        (2, "系统维护"),
        (3, "安全提醒"),
        (4, "节假日通知"),
        (5, "活动公告"),
        # 可按需扩展
    ]

    # 重要程度（L: 普通, M: 重要, H: 紧急）
    LEVEL_CHOICES = [
        ("L", "普通"),
        ("M", "重要"),
        ("H", "紧急"),
    ]

    # 目标用户类型
    TARGET_TYPE_CHOICES = [
        (1, "全体用户"),
        (2, "指定角色"),
        (3, "指定部门"),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField("标题", max_length=255)
    publish_status = models.SmallIntegerField(
        "发布状态", choices=PUBLISH_STATUS_CHOICES, default=1
    )
    type = models.SmallIntegerField("通知类型", choices=TYPE_CHOICES)
    publisher_name = models.CharField("发布人姓名", max_length=100)
    level = models.CharField("重要程度", max_length=1, choices=LEVEL_CHOICES, default="L")
    publish_time = models.DateTimeField("发布时间")
    create_time = models.DateTimeField("创建时间")
    revoke_time = models.DateTimeField("撤销时间", blank=True, null=True)

    # 扩展字段（预留）
    content = models.TextField("通知内容", blank=True, null=True)  # 虽然 mock 里没出现，但实际需要
    target_type = models.SmallIntegerField(
        "目标类型", choices=TARGET_TYPE_CHOICES, default=1
    )

    class Meta:
        db_table = 'sys_notice'
        verbose_name = "通知公告"
        verbose_name_plural = verbose_name
        ordering = ['-publish_time', '-id']

    def __str__(self):
        return f"[{self.get_type_display()}] {self.title}"

