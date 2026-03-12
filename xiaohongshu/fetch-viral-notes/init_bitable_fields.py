#!/usr/bin/env python3
"""
低粉爆文抓取表 - 字段初始化脚本

初始化飞书多维表格的字段结构，用于存储小红书低粉爆文数据。

Usage:
    python init_bitable_fields.py [--dry-run]

Options:
    --dry-run   预览模式，不实际创建字段
"""

import sys
import argparse
import requests
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 从 config.py 导入配置
from config import (
    LARK_APP_ID,
    LARK_APP_SECRET,
    get_bitable,
)

# 获取"低粉爆文抓取"表格配置
TABLE_NAME = "低粉爆文抓取"
_bitable = get_bitable(TABLE_NAME)
APP_TOKEN = _bitable.get("app_token")
TABLE_ID = _bitable.get("table_id")

# 飞书 API 基础 URL
LARK_API_BASE = "https://open.feishu.cn/open-apis"


class LarkBitableClient:
    """飞书多维表格客户端"""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token = None

    def _get_tenant_token(self) -> str:
        """获取 tenant_access_token"""
        if self._token:
            return self._token

        url = f"{LARK_API_BASE}/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"获取 token 失败: {data}")

        self._token = data["tenant_access_token"]
        return self._token

    def _headers(self) -> dict:
        """构建请求头"""
        return {
            "Authorization": f"Bearer {self._get_tenant_token()}",
            "Content-Type": "application/json"
        }

    def list_fields(self, app_token: str, table_id: str) -> list:
        """获取数据表的所有字段"""
        url = f"{LARK_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        resp = requests.get(url, headers=self._headers())
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"获取字段列表失败: {data}")

        return data.get("data", {}).get("items", [])

    def create_field(self, app_token: str, table_id: str, field_config: dict) -> dict:
        """创建字段"""
        url = f"{LARK_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        resp = requests.post(url, headers=self._headers(), json=field_config)
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"创建字段失败: {data}")

        return data.get("data", {}).get("field", {})

    def update_field(self, app_token: str, table_id: str, field_id: str, field_config: dict) -> dict:
        """更新字段"""
        url = f"{LARK_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/fields/{field_id}"
        resp = requests.put(url, headers=self._headers(), json=field_config)
        data = resp.json()

        if data.get("code") != 0:
            raise Exception(f"更新字段失败: {data}")

        return data.get("data", {}).get("field", {})


def build_field_configs() -> list:
    """
    构建字段配置

    飞书字段类型:
    - 1: 多行文本
    - 2: 数字
    - 3: 单选
    - 5: 日期
    - 7: 复选框
    - 15: 超链接
    """
    fields = []

    # 1. 笔记ID - 首列（索引字段）
    fields.append({
        "field_name": "笔记ID",
        "type": 1,  # 文本
    })

    # 2. 标题
    fields.append({
        "field_name": "标题",
        "type": 1,
    })

    # 3. 内容摘要
    fields.append({
        "field_name": "内容摘要",
        "type": 1,
    })

    # 4. 作者昵称
    fields.append({
        "field_name": "作者昵称",
        "type": 1,
    })

    # 5. 作者ID
    fields.append({
        "field_name": "作者ID",
        "type": 1,
    })

    # 6. 作者粉丝数
    fields.append({
        "field_name": "作者粉丝数",
        "type": 2,  # 数字
        "property": {
            "formatter": "0"  # 整数格式
        }
    })

    # 7. 点赞数
    fields.append({
        "field_name": "点赞数",
        "type": 2,
        "property": {
            "formatter": "0"
        }
    })

    # 8. 收藏数
    fields.append({
        "field_name": "收藏数",
        "type": 2,
        "property": {
            "formatter": "0"
        }
    })

    # 9. 评论数
    fields.append({
        "field_name": "评论数",
        "type": 2,
        "property": {
            "formatter": "0"
        }
    })

    # 10. 互动粉丝比
    fields.append({
        "field_name": "互动粉丝比",
        "type": 2,
        "property": {
            "formatter": "0.00%"  # 百分比格式
        }
    })

    # 11. 笔记类型 - 单选
    fields.append({
        "field_name": "笔记类型",
        "type": 3,
        "property": {
            "options": [
                {"name": "图文"},
                {"name": "视频"},
            ]
        }
    })

    # 12. 笔记链接
    fields.append({
        "field_name": "笔记链接",
        "type": 15,  # 超链接
    })

    # 13. 封面图
    fields.append({
        "field_name": "封面图",
        "type": 1,
    })

    # 14. 搜索关键词
    fields.append({
        "field_name": "搜索关键词",
        "type": 1,
    })

    # 15. 抓取时间
    fields.append({
        "field_name": "抓取时间",
        "type": 5,  # 日期
        "property": {
            "date_formatter": "yyyy/MM/dd HH:mm"
        }
    })

    # 16. 已分析 - 复选框
    fields.append({
        "field_name": "已分析",
        "type": 7,
    })

    # 17. 备注
    fields.append({
        "field_name": "备注",
        "type": 1,
    })

    # 18. xsec_token (用于后续操作)
    fields.append({
        "field_name": "xsec_token",
        "type": 1,
    })

    return fields


def print_preview(fields: list):
    """打印预览信息"""
    print("\n" + "=" * 60)
    print(f"低粉爆文抓取表 - 字段初始化预览")
    print(f"表格: {TABLE_NAME}")
    print(f"app_token: {APP_TOKEN}")
    print(f"table_id: {TABLE_ID}")
    print("=" * 60)

    type_map = {1: "文本", 2: "数字", 3: "单选", 5: "日期", 7: "复选框", 15: "超链接"}

    print("\n将创建/更新的字段:")
    for i, field in enumerate(fields, 1):
        ftype = type_map.get(field["type"], str(field["type"]))
        print(f"  {i:2}. {field['field_name']} ({ftype})")

    print("\n" + "=" * 60)


def init_fields(client: LarkBitableClient, field_configs: list, dry_run: bool = False):
    """初始化字段"""

    if dry_run:
        print("\n预览模式，不会实际修改飞书表格")
        return

    # 获取现有字段
    existing_fields = client.list_fields(APP_TOKEN, TABLE_ID)
    existing_map = {f["field_name"]: f for f in existing_fields}

    print(f"\n现有字段: {len(existing_fields)} 个")

    created = 0
    updated = 0
    skipped = 0

    for config in field_configs:
        field_name = config["field_name"]

        if field_name in existing_map:
            existing = existing_map[field_name]
            # 如果是单选字段，可以更新选项
            if config["type"] == 3 and "property" in config:
                try:
                    client.update_field(APP_TOKEN, TABLE_ID, existing["field_id"], config)
                    print(f"  已更新: {field_name}")
                    updated += 1
                except Exception as e:
                    print(f"  更新失败 {field_name}: {e}")
                    skipped += 1
            else:
                print(f"  已跳过: {field_name} (已存在)")
                skipped += 1
        else:
            # 创建新字段
            try:
                client.create_field(APP_TOKEN, TABLE_ID, config)
                print(f"  已创建: {field_name}")
                created += 1
            except Exception as e:
                print(f"  创建失败 {field_name}: {e}")

    print(f"\n完成: 创建 {created} / 更新 {updated} / 跳过 {skipped}")


def main():
    parser = argparse.ArgumentParser(description="初始化低粉爆文抓取表字段")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际修改")
    args = parser.parse_args()

    # 检查配置
    if not LARK_APP_ID or not LARK_APP_SECRET:
        print("错误: 请在 config.py 中配置 LARK_APP_ID 和 LARK_APP_SECRET")
        sys.exit(1)

    if not APP_TOKEN or not TABLE_ID:
        print(f"错误: 请在 config.py 的 LARK_BITABLES 中配置 '{TABLE_NAME}' 表格")
        sys.exit(1)

    # 构建字段配置
    fields = build_field_configs()

    # 打印预览
    print_preview(fields)

    if args.dry_run:
        print("\n预览完成（--dry-run 模式）")
        return

    # 初始化客户端
    client = LarkBitableClient(LARK_APP_ID, LARK_APP_SECRET)

    # 初始化字段
    print(f"\n开始初始化字段...")
    init_fields(client, fields, args.dry_run)

    print("\n完成!")


if __name__ == "__main__":
    main()
