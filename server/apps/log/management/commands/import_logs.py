
from django.core.management.base import BaseCommand
from apps.log.models import OperationLog
from datetime import datetime
from zoneinfo import ZoneInfo


class Command(BaseCommand):
    help = "导入 mock 操作日志数据"

    def handle(self, *args, **options):
        # 来自 mock 的 logs/page -> data.list
        mock_logs = [
            {
                "id": 36192,
                "module": "菜单",
                "content": "菜单列表",
                "requestUri": "/api/v1/menus",
                "method": None,
                "ip": "183.156.148.241",
                "region": "浙江省 杭州市",
                "browser": "Chrome 109.0.0.0",
                "os": "OSX",
                "executionTime": 5,
                "createBy": None,
                "createTime": "2024-07-07 20:38:47",
                "operator": "系统管理员",
            },
            {
                "id": 36190,
                "module": "字典",
                "content": "字典分页列表",
                "requestUri": "/api/v1/dict/page",
                "method": None,
                "ip": "183.156.148.241",
                "region": "浙江省 杭州市",
                "browser": "Chrome 109.0.0.0",
                "os": "OSX",
                "executionTime": 9,
                "createBy": None,
                "createTime": "2024-07-07 20:38:45",
                "operator": "系统管理员",
            },
            {
                "id": 36193,
                "module": "部门",
                "content": "部门列表",
                "requestUri": "/api/v1/dept",
                "method": None,
                "ip": "192.168.31.134",
                "region": "0 内网IP",
                "browser": "Chrome 125.0.0.0",
                "os": "Windows 10 or Windows Server 2016",
                "executionTime": 27,
                "createBy": None,
                "createTime": "2024-07-07 20:38:45",
                "operator": "系统管理员",
            },
            {
                "id": 36191,
                "module": "菜单",
                "content": "菜单列表",
                "requestUri": "/api/v1/menus",
                "method": None,
                "ip": "192.168.31.134",
                "region": "0 内网IP",
                "browser": "Chrome 125.0.0.0",
                "os": "Windows 10 or Windows Server 2016",
                "executionTime": 39,
                "createBy": None,
                "createTime": "2024-07-07 20:38:44",
                "operator": "系统管理员",
            },
            {
                "id": 36189,
                "module": "角色",
                "content": "角色分页列表",
                "requestUri": "/api/v1/roles/page",
                "method": None,
                "ip": "192.168.31.134",
                "region": "0 内网IP",
                "browser": "Chrome 125.0.0.0",
                "os": "Windows 10 or Windows Server 2016",
                "executionTime": 55,
                "createBy": None,
                "createTime": "2024-07-07 20:38:43",
                "operator": "系统管理员",
            },
            {
                "id": 36188,
                "module": "用户",
                "content": "用户分页列表",
                "requestUri": "/api/v1/users/page",
                "method": None,
                "ip": "192.168.31.134",
                "region": "0 内网IP",
                "browser": "Chrome 125.0.0.0",
                "os": "Windows 10 or Windows Server 2016",
                "executionTime": 92,
                "createBy": None,
                "createTime": "2024-07-07 20:38:42",
                "operator": "系统管理员",
            },
            {
                "id": 36187,
                "module": "登录",
                "content": "登录",
                "requestUri": "/api/v1/auth/login",
                "method": None,
                "ip": "192.168.31.134",
                "region": "0 内网IP",
                "browser": "Chrome 125.0.0.0",
                "os": "Windows 10 or Windows Server 2016",
                "executionTime": 19340,
                "createBy": None,
                "createTime": "2024-07-07 20:38:09",
                "operator": "系统管理员",
            },
            {
                "id": 36186,
                "module": "登录",
                "content": "登录",
                "requestUri": "/api/v1/auth/login",
                "method": None,
                "ip": "192.168.31.134",
                "region": "0 内网IP",
                "browser": "Chrome 125.0.0.0",
                "os": "Windows 10 or Windows Server 2016",
                "executionTime": 19869,
                "createBy": None,
                "createTime": "2024-07-07 20:37:59",
                "operator": "系统管理员",
            },
            {
                "id": 36185,
                "module": "登录",
                "content": "登录",
                "requestUri": "/api/v1/auth/login",
                "method": None,
                "ip": "112.103.111.59",
                "region": "黑龙江省 哈尔滨市",
                "browser": "Chrome 97.0.4692.98",
                "os": "Android",
                "executionTime": 96,
                "createBy": None,
                "createTime": "2024-07-07 20:37:21",
                "operator": "系统管理员",
            },
            {
                "id": 36184,
                "module": "登录",
                "content": "登录",
                "requestUri": "/api/v1/auth/login",
                "method": None,
                "ip": "114.86.204.190",
                "region": "上海 上海市",
                "browser": "Chrome 125.0.0.0",
                "os": "Windows 10 or Windows Server 2016",
                "executionTime": 89,
                "createBy": None,
                "createTime": "2024-07-07 20:29:37",
                "operator": "系统管理员",
            },
        ]

        shanghai_tz = ZoneInfo("Asia/Shanghai")

        count = 0
        for log in mock_logs:

            naive_dt = datetime.strptime(log["createTime"], "%Y-%m-%d %H:%M:%S")
            aware_dt = naive_dt.replace(tzinfo=shanghai_tz)
            obj, created = OperationLog.objects.update_or_create(
                id=log["id"],
                defaults={
                    "module": log["module"],
                    "content": log["content"],
                    "request_uri": log["requestUri"],
                    "method": log["method"],
                    "ip": log["ip"],
                    "region": log["region"],
                    "browser": log["browser"],
                    "os": log["os"],
                    "execution_time": log["executionTime"],
                    "create_by": log["createBy"],
                    "create_time": aware_dt,
                    "operator": log["operator"],
                }
            )
            if created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"✅ 成功导入 {count} 条操作日志")
        )

