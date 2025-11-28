from datetime import datetime

from django.core.management.base import BaseCommand
from apps.roles.models import Role


class Command(BaseCommand):
    help = "从 mock 数据导入角色到数据库"

    def handle(self, *args, **options):
        # 从 mock 数据中提取的角色列表（模拟 roles/page 接口返回的 list）
        mock_role_data = [
            {
                "id": 2,
                "name": "系统管理员",
                "code": "ADMIN",
                "status": 1,
                "sort": 2,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": None,
            },
            {
                "id": 3,
                "name": "访问游客",
                "code": "GUEST",
                "status": 1,
                "sort": 3,
                "createTime": "2021-05-26 15:49:05",
                "updateTime": "2019-05-05 16:00:00",
            },
            {
                "id": 4,
                "name": "系统管理员1",
                "code": "ADMIN1",
                "status": 1,
                "sort": 2,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": None,
            },
            {
                "id": 5,
                "name": "系统管理员2",
                "code": "ADMIN2",
                "status": 1,
                "sort": 2,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": None,
            },
            {
                "id": 6,
                "name": "系统管理员3",
                "code": "ADMIN3",
                "status": 1,
                "sort": 2,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": None,
            },
            {
                "id": 7,
                "name": "系统管理员4",
                "code": "ADMIN4",
                "status": 1,
                "sort": 2,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": None,
            },
            {
                "id": 8,
                "name": "系统管理员5",
                "code": "ADMIN5",
                "status": 1,
                "sort": 2,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": None,
            },
            {
                "id": 9,
                "name": "系统管理员6",
                "code": "ADMIN6",
                "status": 1,
                "sort": 2,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": "2023-12-04 11:43:15",
            },
            {
                "id": 10,
                "name": "系统管理员7",
                "code": "ADMIN7",
                "status": 1,
                "sort": 2,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": None,
            },
            {
                "id": 11,
                "name": "系统管理员8",
                "code": "ADMIN8",
                "status": 1,
                "sort": 2,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": None,
            },
        ]

        from datetime import datetime

        count_created = 0
        count_updated = 0

        for item in mock_role_data:
            # 转换时间字符串为 datetime 对象（处理 None）
            create_time = self._parse_datetime(item["createTime"])
            update_time = self._parse_datetime(item["updateTime"])

            role, created = Role.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "code": item["code"],
                    "status": item["status"],
                    "sort": item["sort"],
                    "data_scope": 1,  # 默认值，mock 数据未提供，可按需调整
                    "create_time": create_time,
                    "update_time": update_time,
                }
            )

            if created:
                count_created += 1
            else:
                count_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"成功导入角色：新增 {count_created} 个，更新 {count_updated} 个"
            )
        )

    def _parse_datetime(self, dt_str):
        if not dt_str:
            return None
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # 兼容可能的格式问题
            return None

