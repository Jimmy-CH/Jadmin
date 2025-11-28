
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.dept.models import Department
from apps.roles.models import Role
from apps.users.models import UserProfile


class Command(BaseCommand):
    help = "从 mock 数据导入用户及其资料（含部门和角色）"

    def handle(self, *args, **options):
        mock_users = [
            {
                "id": 2,
                "username": "admin",
                "nickname": "系统管理员",
                "mobile": "17621210366",
                "gender": 1,
                "avatar": "https://foruda.gitee.com/images/1723603502796844527/03cdca2a_716974.gif",
                "email": "",
                "status": 1,
                "deptId": 1,
                "roleIds": [2],
            },
            {
                "id": 3,
                "username": "test",
                "nickname": "测试小用户",
                "mobile": "17621210366",
                "gender": 1,
                "avatar": "https://foruda.gitee.com/images/1723603502796844527/03cdca2a_716974.gif",
                "email": "youlaitech@163.com",
                "status": 1,
                "deptId": 3,
                "roleIds": [3],
            },
        ]

        created_count = 0
        updated_count = 0

        for item in mock_users:
            # Step 1: 创建或更新 User
            user, user_created = User.objects.update_or_create(
                id=item["id"],
                defaults={
                    "username": item["username"],
                    "email": item["email"] or "",
                    # 设置一个默认密码（如 admin / test），便于登录
                    "is_active": True,
                }
            )
            # 如果是新建用户，设一个简单密码（例如 username 本身）
            if user_created:
                user.set_password(item["username"])  # admin -> password=admin
                user.save()

            # Step 2: 获取关联对象
            dept = None
            if item["deptId"]:
                try:
                    dept = Department.objects.get(id=item["deptId"])
                except Department.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"部门 ID={item['deptId']} 不存在，用户 {user.username} 不关联部门")
                    )

            roles = []
            if item["roleIds"]:
                roles = Role.objects.filter(id__in=item["roleIds"])
                if len(roles) != len(item["roleIds"]):
                    missing = set(item["roleIds"]) - set(r.id for r in roles)
                    self.stdout.write(
                        self.style.WARNING(f"角色 ID {missing} 不存在，用户 {user.username} 部分角色未关联")
                    )

            # Step 3: 创建或更新 UserProfile
            profile, profile_created = UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    "mobile": item["mobile"],
                    "gender": item["gender"],
                    "avatar": item["avatar"],
                    "status": item["status"],
                    "dept": dept,
                }
            )

            # Step 4: 设置多对多角色关系（必须在 save() 后设置）
            profile.roles.set(roles)

            if user_created:
                created_count += 1
            else:
                updated_count += 1

            self.stdout.write(f"✅ 用户 {user.username} (ID={user.id}) 导入成功")

        self.stdout.write(
            self.style.SUCCESS(
                f"用户数据导入完成：新增 {created_count} 个，更新 {updated_count} 个"
            )
        )