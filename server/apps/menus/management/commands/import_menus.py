
from django.core.management.base import BaseCommand
from apps.menus.models import Menu


class Command(BaseCommand):
    help = "从 mock 数据导入菜单（支持多级嵌套）"

    def handle(self, *args, **options):
        # 从 mock /menus 接口提取的原始数据（扁平化前）
        raw_menu_tree = [
            {
                "id": 1,
                "parentId": 0,
                "name": "系统管理",
                "type": "CATALOG",
                "routeName": "",
                "routePath": "/system",
                "component": "Layout",
                "sort": 1,
                "visible": 1,
                "icon": "system",
                "redirect": "/system/user",
                "perm": None,
                "children": [
                    {
                        "id": 2,
                        "parentId": 1,
                        "name": "用户管理",
                        "type": "MENU",
                        "routeName": "User",
                        "routePath": "user",
                        "component": "system/user/index",
                        "sort": 1,
                        "visible": 1,
                        "icon": "el-icon-User",
                        "redirect": None,
                        "perm": None,
                        "children": [
                            {"id": 105, "parentId": 2, "name": "用户查询", "type": "BUTTON", "perm": "sys:user:query"},
                            {"id": 31, "parentId": 2, "name": "用户新增", "type": "BUTTON", "perm": "sys:user:add"},
                            {"id": 32, "parentId": 2, "name": "用户编辑", "type": "BUTTON", "perm": "sys:user:edit"},
                            {"id": 33, "parentId": 2, "name": "用户删除", "type": "BUTTON", "perm": "sys:user:delete"},
                            {"id": 88, "parentId": 2, "name": "重置密码", "type": "BUTTON", "perm": "sys:user:password:reset"},
                            {"id": 106, "parentId": 2, "name": "用户导入", "type": "BUTTON", "perm": "sys:user:import"},
                            {"id": 107, "parentId": 2, "name": "用户导出", "type": "BUTTON", "perm": "sys:user:export"},
                        ],
                    },
                    {
                        "id": 3,
                        "parentId": 1,
                        "name": "角色管理",
                        "type": "MENU",
                        "routeName": "Role",
                        "routePath": "role",
                        "component": "system/role/index",
                        "sort": 2,
                        "visible": 1,
                        "icon": "role",
                        "redirect": None,
                        "perm": None,
                        "children": [
                            {"id": 70, "parentId": 3, "name": "角色新增", "type": "BUTTON", "perm": "sys:role:add"},
                            {"id": 71, "parentId": 3, "name": "角色编辑", "type": "BUTTON", "perm": "sys:role:edit"},
                            {"id": 72, "parentId": 3, "name": "角色删除", "type": "BUTTON", "perm": "sys:role:delete"},
                        ],
                    },
                    {
                        "id": 4,
                        "parentId": 1,
                        "name": "菜单管理",
                        "type": "MENU",
                        "routeName": "Menu",
                        "routePath": "menu",
                        "component": "system/menu/index",
                        "sort": 3,
                        "visible": 1,
                        "icon": "menu",
                        "redirect": None,
                        "perm": None,
                        "children": [
                            {"id": 73, "parentId": 4, "name": "菜单新增", "type": "BUTTON", "perm": "sys:menu:add"},
                            {"id": 74, "parentId": 4, "name": "菜单编辑", "type": "BUTTON", "perm": "sys:menu:edit"},
                            {"id": 75, "parentId": 4, "name": "菜单删除", "type": "BUTTON", "perm": "sys:menu:delete"},
                        ],
                    },
                    {
                        "id": 5,
                        "parentId": 1,
                        "name": "部门管理",
                        "type": "MENU",
                        "routeName": "Dept",
                        "routePath": "dept",
                        "component": "system/dept/index",
                        "sort": 4,
                        "visible": 1,
                        "icon": "tree",
                        "redirect": None,
                        "perm": None,
                        "children": [
                            {"id": 76, "parentId": 5, "name": "部门新增", "type": "BUTTON", "perm": "sys:dept:add"},
                            {"id": 77, "parentId": 5, "name": "部门编辑", "type": "BUTTON", "perm": "sys:dept:edit"},
                            {"id": 78, "parentId": 5, "name": "部门删除", "type": "BUTTON", "perm": "sys:dept:delete"},
                        ],
                    },
                    {
                        "id": 6,
                        "parentId": 1,
                        "name": "字典管理",
                        "type": "MENU",
                        "routeName": "Dict",
                        "routePath": "dict",
                        "component": "system/dict/index",
                        "sort": 5,
                        "visible": 1,
                        "icon": "dict",
                        "redirect": None,
                        "perm": None,
                        "children": [
                            {"id": 79, "parentId": 6, "name": "字典新增", "type": "BUTTON", "perm": "sys:dict:add"},
                            {"id": 81, "parentId": 6, "name": "字典编辑", "type": "BUTTON", "perm": "sys:dict_type:edit"},
                            {"id": 84, "parentId": 6, "name": "字典删除", "type": "BUTTON", "perm": "sys:dict_type:delete"},
                        ],
                    },
                    {
                        "id": 135,
                        "parentId": 1,
                        "name": "字典项",
                        "type": "MENU",
                        "routeName": "DictData",
                        "routePath": "dict-item",
                        "component": "system/dict/dict-item",
                        "sort": 6,
                        "visible": 0,
                        "icon": "",
                        "redirect": None,
                        "perm": None,
                        "children": [
                            {"id": 136, "parentId": 135, "name": "字典项新增", "type": "BUTTON", "perm": "sys:dict-item:add"},
                            {"id": 137, "parentId": 135, "name": "字典项编辑", "type": "BUTTON", "perm": "sys:dict-item:edit"},
                            {"id": 138, "parentId": 135, "name": "字典项删除", "type": "BUTTON", "perm": "sys:dict-item:delete"},
                        ],
                    },
                    {
                        "id": 117,
                        "parentId": 1,
                        "name": "系统日志",
                        "type": "MENU",
                        "routeName": "Log",
                        "routePath": "log",
                        "component": "system/log/index",
                        "sort": 6,
                        "visible": 1,
                        "icon": "document",
                        "redirect": None,
                        "perm": None,
                        "children": [],
                    },
                    {
                        "id": 120,
                        "parentId": 1,
                        "name": "系统配置",
                        "type": "MENU",
                        "routeName": "Config",
                        "routePath": "config",
                        "component": "system/config/index",
                        "sort": 7,
                        "visible": 1,
                        "icon": "setting",
                        "redirect": None,
                        "perm": None,
                        "children": [
                            {"id": 121, "name": "查询系统配置", "type": "BUTTON", "perm": "sys:config:query"},
                            {"id": 122, "name": "新增系统配置", "type": "BUTTON", "perm": "sys:config:add"},
                            {"id": 123, "name": "修改系统配置", "type": "BUTTON", "perm": "sys:config:update"},
                            {"id": 124, "name": "删除系统配置", "type": "BUTTON", "perm": "sys:config:delete"},
                            {"id": 125, "name": "刷新系统配置", "type": "BUTTON", "perm": "sys:config:refresh"},
                        ],
                    },
                    {
                        "id": 126,
                        "parentId": 1,
                        "name": "通知公告",
                        "type": "MENU",
                        "routeName": "Notice",
                        "routePath": "notice",
                        "component": "system/notice/index",
                        "sort": 9,
                        "visible": 1,
                        "icon": "",
                        "redirect": None,
                        "perm": None,
                        "children": [
                            {"id": 127, "name": "查询", "type": "BUTTON", "perm": "sys:notice:query"},
                            {"id": 128, "name": "新增", "type": "BUTTON", "perm": "sys:notice:add"},
                            {"id": 129, "name": "编辑", "type": "BUTTON", "perm": "sys:notice:edit"},
                            {"id": 130, "name": "删除", "type": "BUTTON", "perm": "sys:notice:delete"},
                            {"id": 133, "name": "发布", "type": "BUTTON", "perm": "sys:notice:publish"},
                            {"id": 134, "name": "撤回", "type": "BUTTON", "perm": "sys:notice:revoke"},
                        ],
                    },
                ],
            },
            {
                "id": 118,
                "parentId": 0,
                "name": "系统工具",
                "type": "CATALOG",
                "routePath": "/codegen",
                "component": "Layout",
                "sort": 2,
                "visible": 1,
                "icon": "menu",
                "children": [
                    {
                        "id": 119,
                        "parentId": 118,
                        "name": "代码生成",
                        "type": "MENU",
                        "routePath": "codegen",
                        "component": "codegen/index",
                        "sort": 1,
                        "visible": 1,
                        "icon": "code",
                        "children": [],
                    }
                ],
            },
            {
                "id": 40,
                "parentId": 0,
                "name": "接口文档",
                "type": "CATALOG",
                "routePath": "/api",
                "component": "Layout",
                "sort": 7,
                "visible": 1,
                "icon": "api",
                "children": [
                    {
                        "id": 41,
                        "parentId": 40,
                        "name": "Apifox",
                        "type": "MENU",
                        "routePath": "apifox",
                        "component": "demo/api/apifox",
                        "sort": 1,
                        "visible": 1,
                        "icon": "api",
                        "children": [],
                    }
                ],
            },
            {
                "id": 26,
                "parentId": 0,
                "name": "平台文档",
                "type": "CATALOG",
                "routePath": "/doc",
                "component": "Layout",
                "sort": 8,
                "visible": 1,
                "icon": "document",
                "redirect": "https://juejin.cn/post/7228990409909108793",
                "children": [
                    {
                        "id": 102,
                        "parentId": 26,
                        "name": "平台文档(内嵌)",
                        "type": "EXTLINK",
                        "routePath": "internal-doc",
                        "component": "demo/internal-doc",
                        "sort": 1,
                        "visible": 1,
                        "icon": "document",
                    },
                    {
                        "id": 30,
                        "parentId": 26,
                        "name": "平台文档(外链)",
                        "type": "EXTLINK",
                        "routePath": "https://juejin.cn/post/7228990409909108793",
                        "component": "",
                        "sort": 2,
                        "visible": 1,
                        "icon": "link",
                    },
                ],
            },
            {
                "id": 20,
                "parentId": 0,
                "name": "多级菜单",
                "type": "CATALOG",
                "routePath": "/multi-level",
                "component": "Layout",
                "sort": 9,
                "visible": 1,
                "icon": "cascader",
                "children": [
                    {
                        "id": 21,
                        "parentId": 20,
                        "name": "菜单一级",
                        "type": "CATALOG",
                        "routePath": "multi-level1",
                        "component": "Layout",
                        "sort": 1,
                        "visible": 1,
                        "children": [
                            {
                                "id": 22,
                                "parentId": 21,
                                "name": "菜单二级",
                                "type": "CATALOG",
                                "routePath": "multi-level2",
                                "component": "Layout",
                                "sort": 1,
                                "visible": 1,
                                "children": [
                                    {
                                        "id": 23,
                                        "parentId": 22,
                                        "name": "菜单三级-1",
                                        "type": "MENU",
                                        "routePath": "multi-level3-1",
                                        "component": "demo/multi-level/children/children/level3-1",
                                        "sort": 1,
                                        "visible": 1,
                                    },
                                    {
                                        "id": 24,
                                        "parentId": 22,
                                        "name": "菜单三级-2",
                                        "type": "MENU",
                                        "routePath": "multi-level3-2",
                                        "component": "demo/multi-level/children/children/level3-2",
                                        "sort": 2,
                                        "visible": 1,
                                    },
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "id": 36,
                "parentId": 0,
                "name": "组件封装",
                "type": "CATALOG",
                "routePath": "/component",
                "component": "Layout",
                "sort": 10,
                "visible": 1,
                "icon": "menu",
                "children": [
                    {"id": 108, "name": "增删改查", "type": "MENU", "routePath": "curd", "component": "demo/curd/index", "sort": 0},
                    {"id": 109, "name": "列表选择器", "type": "MENU", "routePath": "table-select", "component": "demo/table-select/index", "sort": 1},
                    {"id": 37, "name": "富文本编辑器", "type": "MENU", "routePath": "wang-editor", "component": "demo/wang-editor", "sort": 2},
                    {"id": 38, "name": "图片上传", "type": "MENU", "routePath": "upload", "component": "demo/upload", "sort": 3},
                    {"id": 95, "name": "字典组件", "type": "MENU", "routePath": "dict-demo", "component": "demo/dict", "sort": 4},
                    {"id": 39, "name": "图标选择器", "type": "MENU", "routePath": "icon-selector", "component": "demo/icon-selector", "sort": 4},
                ],
            },
            {
                "id": 110,
                "parentId": 0,
                "name": "路由参数",
                "type": "CATALOG",
                "routePath": "/route-param",
                "component": "Layout",
                "sort": 11,
                "visible": 1,
                "icon": "el-icon-ElementPlus",
                "children": [
                    {
                        "id": 111,
                        "parentId": 110,
                        "name": "参数(type=1)",
                        "type": "MENU",
                        "routePath": "route-param-type1",
                        "component": "demo/route-param",
                        "sort": 1,
                        "visible": 1,
                        "icon": "el-icon-Star",
                        "params": {"type": "1"},
                    },
                    {
                        "id": 112,
                        "parentId": 110,
                        "name": "参数(type=2)",
                        "type": "MENU",
                        "routePath": "route-param-type2",
                        "component": "demo/route-param",
                        "sort": 2,
                        "visible": 1,
                        "icon": "el-icon-StarFilled",
                        "params": {"type": "2"},
                    },
                ],
            },
            {
                "id": 89,
                "parentId": 0,
                "name": "功能演示",
                "type": "CATALOG",
                "routePath": "/function",
                "component": "Layout",
                "sort": 12,
                "visible": 1,
                "icon": "menu",
                "children": [
                    {"id": 97, "name": "Icons", "type": "MENU", "routePath": "icon-demo", "component": "demo/icons", "sort": 2, "icon": "el-icon-Notification"},
                    {"id": 90, "name": "Websocket", "type": "MENU", "routePath": "/function/websocket", "component": "demo/websocket", "sort": 3},
                    {"id": 91, "name": "敬请期待...", "type": "CATALOG", "routePath": "other/:id", "component": "demo/other", "sort": 4},
                ],
            },
        ]

        # 类型映射
        TYPE_MAP = {
            "CATALOG": 2,
            "MENU": 1,
            "BUTTON": 4,
            "EXTLINK": 3,
        }

        created_count = 0

        def create_menu_items(items, parent=None):
            nonlocal created_count
            for item in items:
                menu_type = item["type"]
                params = item.get("params", None)

                menu, created = Menu.objects.update_or_create(
                    id=item["id"],
                    defaults={
                        "name": item["name"],
                        "parent": parent,
                        "type": menu_type,
                        "route_name": item.get("routeName") or "",
                        "route_path": item.get("routePath") or "",
                        "component": item.get("component") or "",
                        "perm": item.get("perm") or "",
                        "visible": item.get("visible", 1),
                        "sort": item.get("sort", 0),
                        "icon": item.get("icon", ""),
                        "redirect": item.get("redirect") or "",
                        "keep_alive": 1 if item.get("keepAlive") else 0,
                        "always_show": 1 if item.get("alwaysShow") else 0,
                        "params": params,
                    }
                )
                if created:
                    created_count += 1

                # 递归处理子菜单
                children = item.get("children", [])
                if children:
                    create_menu_items(children, parent=menu)

        # 清空旧数据（可选，谨慎使用）
        # Menu.objects.all().delete()

        # 导入根菜单
        create_menu_items(raw_menu_tree)

        self.stdout.write(
            self.style.SUCCESS(f"✅ 菜单数据导入完成，共 {created_count} 条记录")
        )
