

from django.core.management.base import BaseCommand
from apps.dept.models import Department


class Command(BaseCommand):
    help = "从 mock 数据导入部门信息（支持父子层级）"

    def handle(self, *args, **options):
        # 模拟 mock 数据中的 deptMap
        dept_data = [
            {"id": 1, "name": "有来技术", "code": "YOULAI", "parentId": 0, "status": 1, "sort": 1},
            {"id": 2, "name": "研发部门", "code": "RD001", "parentId": 1, "status": 1, "sort": 1},
            {"id": 3, "name": "测试部门", "code": "QA001", "parentId": 1, "status": 1, "sort": 1},
        ]

        # 先按 parentId 排序：parentId=0（顶级）优先，确保父部门先创建
        dept_data.sort(key=lambda x: x["parentId"])

        created_count = 0
        updated_count = 0

        for item in dept_data:
            parent_id = item["parentId"]
            parent = None
            if parent_id != 0:  # parentId=0 表示无上级
                try:
                    parent = Department.objects.get(id=parent_id)
                except Department.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"警告：父部门 ID={parent_id} 不存在，跳过设置上级")
                    )

            dept, created = Department.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "code": item["code"],
                    "parent": parent,
                    "status": item["status"],
                    "sort": item["sort"],
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"部门数据导入完成：新增 {created_count} 个，更新 {updated_count} 个"
            )
        )
