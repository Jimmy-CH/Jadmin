import sys
from django.core.management.base import BaseCommand
from apps.notices.models import Notice
from datetime import datetime
if sys.version_info >= (3, 9):
    from zoneinfo import ZoneInfo
else:
    import pytz


class Command(BaseCommand):
    help = "导入 mock 通知公告数据"

    def handle(self, *args, **options):
        mock_data = [
            {
                "id": 1,
                "title": "v2.12.0 新增系统日志，访问趋势统计功能。",
                "publishStatus": 1,
                "type": 1,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:21",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
            {
                "id": 2,
                "title": "v2.13.0 新增菜单搜索。",
                "publishStatus": 1,
                "type": 1,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:22",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
            {
                "id": 3,
                "title": "\r\nv2.14.0 新增个人中心。",
                "publishStatus": 1,
                "type": 1,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:23",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
            {
                "id": 4,
                "title": "v2.15.0 登录页面改造。",
                "publishStatus": 1,
                "type": 1,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:24",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
            {
                "id": 5,
                "title": "v2.16.0 通知公告、字典翻译组件。",
                "publishStatus": 1,
                "type": 1,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:25",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
            {
                "id": 6,
                "title": "系统将于本周六凌晨 2 点进行维护，预计维护时间为 2 小时。",
                "publishStatus": 1,
                "type": 2,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:26",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
            {
                "id": 7,
                "title": "最近发现一些钓鱼邮件，请大家提高警惕，不要点击陌生链接。",
                "publishStatus": 1,
                "type": 3,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:27",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
            {
                "id": 8,
                "title": "国庆假期从 10 月 1 日至 10 月 7 日放假，共 7 天。",
                "publishStatus": 1,
                "type": 4,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:28",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
            {
                "id": 9,
                "title": "公司将在 10 月 15 日举办新产品发布会，敬请期待。",
                "publishStatus": 1,
                "type": 5,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:29",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
            {
                "id": 10,
                "title": "v2.16.1 版本修复了 WebSocket 重复连接导致的后台线程阻塞问题，优化了通知公告。",
                "publishStatus": 1,
                "type": 1,
                "publisherName": "系统管理员",
                "level": "L",
                "publishTime": "2024-09-30 17:30",
                "createTime": "2024-09-28 11:21",
                "revokeTime": "2024-09-30 17:21",
                "targetType": 1,
            },
        ]

        count = 0
        for item in mock_data:
            # 清理标题中的多余空白字符（如 \r\n）
            title = item["title"].strip()

            obj, created = Notice.objects.update_or_create(
                id=item["id"],
                defaults={
                    "title": title,
                    "publish_status": item["publishStatus"],
                    "type": item["type"],
                    "publisher_name": item["publisherName"],
                    "level": item["level"],
                    "publish_time": self._parse_datetime(item["publishTime"]),
                    "create_time": self._parse_datetime(item["createTime"]),
                    "revoke_time": self._parse_datetime(item["revokeTime"]),
                    "target_type": item["targetType"],
                }
            )
            if created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"✅ 成功导入 {count} 条通知公告")
        )

    def _parse_datetime(self, dt_str):
        if not dt_str:
            return None
        naive_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        if sys.version_info >= (3, 9):
            tz = ZoneInfo("Asia/Shanghai")
            return naive_dt.replace(tzinfo=tz)
        else:
            tz = pytz.timezone("Asia/Shanghai")
            return tz.localize(naive_dt)


