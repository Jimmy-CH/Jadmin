
from django.core.management.base import BaseCommand
from apps.dicts.models import Dict, DictItem


class Command(BaseCommand):
    help = "从 mock 数据导入字典及字典项"

    def handle(self, *args, **options):
        # 字典数据（来自 mock 的 dicts/page）
        dict_data = [
            {"id": 1, "name": "性别", "dictCode": "gender", "status": 1},
            {"id": 2, "name": "通知级别", "dictCode": "notice_level", "status": 1},
            {"id": 3, "name": "通知类型", "dictCode": "notice_type", "status": 1},
        ]

        # 字典项数据（来自 mock 的 dicts/:code/items）
        dict_item_data = {
            "gender": [
                {"id": 1, "value": "1", "label": "男", "sort": 1, "status": 1, "tag": None},
                {"id": 2, "value": "2", "label": "女", "sort": 2, "status": 1, "tag": None},
                {"id": 3, "value": "0", "label": "保密", "sort": 3, "status": 1, "tag": None},
            ],
            "notice_level": [
                {"id": 4, "value": "L", "label": "低", "sort": 1, "status": 1, "tag": "info"},
                {"id": 5, "value": "M", "label": "中", "sort": 2, "status": 1, "tag": "warning"},
                {"id": 6, "value": "H", "label": "高", "sort": 3, "status": 1, "tag": "danger"},
            ],
            "notice_type": [
                {"id": 7, "value": "1", "label": "系统升级", "sort": 1, "status": 1, "tag": "success"},
                {"id": 8, "value": "2", "label": "系统维护", "sort": 2, "status": 1, "tag": "primary"},
                {"id": 9, "value": "3", "label": "安全警告", "sort": 3, "status": 1, "tag": "danger"},
                {"id": 10, "value": "4", "label": "假期通知", "sort": 4, "status": 1, "tag": "success"},
                {"id": 11, "value": "5", "label": "公司新闻", "sort": 5, "status": 1, "tag": "primary"},
                {"id": 12, "value": "99", "label": "其他", "sort": 6, "status": 1, "tag": "info"},
            ],
        }

        dict_count = 0
        item_count = 0

        # 导入字典
        for d in dict_data:
            obj, created = Dict.objects.update_or_create(
                id=d["id"],
                defaults={
                    "name": d["name"],
                    "dict_code": d["dictCode"],
                    "status": d["status"],
                    "remark": "",
                }
            )
            if created:
                dict_count += 1

        # 导入字典项
        for dict_code, items in dict_item_data.items():
            for item in items:
                obj, created = DictItem.objects.update_or_create(
                    id=item["id"],
                    defaults={
                        "dict_code": dict_code,
                        "label": item["label"],
                        "value": item["value"],
                        "sort": item["sort"],
                        "status": item["status"],
                        "tag": item["tag"],
                        "remark": "",
                    }
                )
                if created:
                    item_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ 字典导入完成：{dict_count} 条，字典项导入完成：{item_count} 条"
            )
        )

