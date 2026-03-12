#!/usr/bin/env python3
"""
模板同步脚本 - 将本地模板同步到飞书多维表格
"""

import glob
import json
import os
import requests
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from config import LARK_APP_ID, LARK_APP_SECRET, get_bitable

# 飞书配置
APP_ID = LARK_APP_ID
APP_SECRET = LARK_APP_SECRET
APP_TOKEN = get_bitable("模板库")["app_token"]
TABLE_ID = get_bitable("模板库")["table_id"]

# 模板目录
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/templates")


def get_access_token():
    """获取飞书 access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json()["tenant_access_token"]


def upload_file(token, file_path, file_type="image/png"):
    """上传文件到飞书"""
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # 根据文件类型设置 MIME type
    if file_path.endswith('.svg'):
        file_type = "image/svg+xml"
    elif file_path.endswith('.png'):
        file_type = "image/png"
    elif file_path.endswith('.md'):
        file_type = "text/markdown"

    with open(file_path, "rb") as f:
        files = {"file": (file_name, f, file_type)}
        data = {
            "file_name": file_name,
            "parent_type": "bitable_file",
            "parent_node": APP_TOKEN,
            "size": str(file_size)
        }
        resp = requests.post(url, headers={"Authorization": f"Bearer {token}"}, files=files, data=data)

    result = resp.json()
    if result.get("code") == 0:
        file_token = result["data"]["file_token"]
        print(f"  ✅ 上传: {file_name} → {file_token}")
        return file_token
    else:
        print(f"  ❌ 上传失败: {file_name} - {result}")
        return None


def search_record(token, template_id):
    """查询是否已存在该模板记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "filter": {
            "conjunction": "and",
            "conditions": [{
                "field_name": "模板ID",
                "operator": "is",
                "value": [template_id]
            }]
        }
    }
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()

    if result.get("code") == 0 and result.get("data", {}).get("total", 0) > 0:
        return result["data"]["items"][0]["record_id"]
    return None


def create_record(token, fields):
    """创建新记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json={"fields": fields})
    result = resp.json()

    if result.get("code") == 0:
        print(f"  ✅ 创建记录成功")
        return result["data"]["record"]["record_id"]
    else:
        print(f"  ❌ 创建失败: {result}")
        return None


def update_record(token, record_id, fields):
    """更新现有记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.put(url, headers=headers, json={"fields": fields})
    result = resp.json()

    if result.get("code") == 0:
        print(f"  ✅ 更新记录成功")
    else:
        print(f"  ❌ 更新失败: {result}")


def sync_template(token, template_dir):
    """同步单个模板"""
    template_id = os.path.basename(template_dir)
    print(f"\n📦 同步模板: {template_id}")

    # 读取 meta.json
    meta_path = os.path.join(template_dir, "meta.json")
    if not os.path.exists(meta_path):
        print(f"  ⚠️ 跳过: 缺少 meta.json")
        return

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    # 读取 PROMPT.md
    prompt_path = os.path.join(template_dir, "PROMPT.md")
    prompt_content = ""
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read()

    # 上传示例图
    examples_dir = os.path.join(template_dir, "examples")
    example_tokens = []
    if os.path.exists(examples_dir):
        png_files = sorted(glob.glob(os.path.join(examples_dir, "*.png")))
        for png_path in png_files:
            ft = upload_file(token, png_path)
            if ft:
                example_tokens.append({"file_token": ft})

    # 上传 SVG 模板
    cover_svg_token = None
    page_svg_token = None
    summary_svg_token = None

    cover_svg = os.path.join(template_dir, "cover.svg")
    if os.path.exists(cover_svg):
        cover_svg_token = upload_file(token, cover_svg)

    page_svg = os.path.join(template_dir, "page.svg")
    if os.path.exists(page_svg):
        page_svg_token = upload_file(token, page_svg)

    summary_svg = os.path.join(template_dir, "summary.svg")
    if os.path.exists(summary_svg):
        summary_svg_token = upload_file(token, summary_svg)

    # 构建记录字段
    fields = {
        "模板ID": meta.get("id", template_id),
        "模板名称": meta.get("name", template_id),
        "描述": meta.get("description", ""),
        "强调色": meta.get("accent_color", ""),
        "适用场景": ", ".join(meta.get("suitable_for", [])),
        "提示词": prompt_content,
    }

    # 添加附件字段
    if example_tokens:
        fields["示例图"] = example_tokens
    if cover_svg_token:
        fields["封面模板"] = [{"file_token": cover_svg_token}]
    if page_svg_token:
        fields["内页模板"] = [{"file_token": page_svg_token}]
    if summary_svg_token:
        fields["结尾页模板"] = [{"file_token": summary_svg_token}]

    # 查询是否已存在
    existing_record = search_record(token, meta.get("id", template_id))

    if existing_record:
        print(f"  📝 更新现有记录: {existing_record}")
        update_record(token, existing_record, fields)
    else:
        print(f"  ➕ 创建新记录")
        create_record(token, fields)


def main():
    print("🚀 开始同步模板到飞书...")
    print(f"📁 模板目录: {TEMPLATES_DIR}")

    # 获取 token
    print("\n🔑 获取 access token...")
    token = get_access_token()
    print("✅ Token 获取成功")

    # 扫描模板目录
    template_dirs = [
        d for d in glob.glob(os.path.join(TEMPLATES_DIR, "*"))
        if os.path.isdir(d) and os.path.exists(os.path.join(d, "meta.json"))
    ]

    print(f"\n📊 发现 {len(template_dirs)} 个模板")

    # 同步每个模板
    for template_dir in template_dirs:
        sync_template(token, template_dir)

    print("\n\n🎉 同步完成!")
    print(f"📊 共同步 {len(template_dirs)} 个模板")


if __name__ == "__main__":
    main()
