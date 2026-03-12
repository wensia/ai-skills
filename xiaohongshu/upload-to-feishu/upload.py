#!/usr/bin/env python3
"""飞书多维表格图片上传脚本

由于 lark-mcp 不支持文件上传，使用此脚本将图片上传到飞书多维表格附件字段。

使用方式:
    python upload.py --record-id "recXXX" --images "path/to/img1.png" "path/to/img2.png"
    python upload.py --record-id "recXXX" --dir "path/to/images/"
"""

import argparse
import os
import sys
from pathlib import Path

import requests

# 添加项目根目录到 path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import LARK_APP_ID, LARK_APP_SECRET, get_bitable

# 飞书 API 基础地址
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"


def get_tenant_access_token() -> str:
    """获取飞书 tenant_access_token"""
    url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": LARK_APP_ID,
        "app_secret": LARK_APP_SECRET
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()

    if data.get("code") != 0:
        raise Exception(f"获取 token 失败: {data.get('msg')}")

    return data["tenant_access_token"]


def upload_file(token: str, file_path: str, app_token: str) -> str:
    """上传单个文件到飞书

    Args:
        token: tenant_access_token
        file_path: 本地文件路径
        app_token: 多维表格 app_token

    Returns:
        file_token: 上传后的文件标识
    """
    url = f"{FEISHU_API_BASE}/drive/v1/medias/upload_all"

    file_path = Path(file_path)
    file_size = file_path.stat().st_size
    file_name = file_path.name

    headers = {
        "Authorization": f"Bearer {token}"
    }

    with open(file_path, "rb") as f:
        files = {
            "file": (file_name, f, "application/octet-stream")
        }
        data = {
            "file_name": file_name,
            "parent_type": "bitable_image",
            "parent_node": app_token,
            "size": str(file_size)
        }

        response = requests.post(url, headers=headers, data=data, files=files)
        response.raise_for_status()
        result = response.json()

    if result.get("code") != 0:
        raise Exception(f"上传文件失败 {file_name}: {result.get('msg')}")

    return result["data"]["file_token"]


def update_bitable_record(
    token: str,
    app_token: str,
    table_id: str,
    record_id: str,
    field_name: str,
    file_tokens: list[str]
) -> dict:
    """更新多维表格记录的附件字段

    Args:
        token: tenant_access_token
        app_token: 多维表格 app_token
        table_id: 表格 ID
        record_id: 记录 ID
        field_name: 附件字段名
        file_tokens: 文件 token 列表

    Returns:
        API 响应数据
    """
    url = f"{FEISHU_API_BASE}/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 附件字段格式: [{"file_token": "xxx"}, ...]
    attachments = [{"file_token": ft} for ft in file_tokens]

    payload = {
        "fields": {
            field_name: attachments
        }
    }

    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 0:
        raise Exception(f"更新记录失败: {result.get('msg')}")

    return result


def upload_images_to_feishu(
    record_id: str,
    image_paths: list[str],
    field_name: str = "生成图片",
    table_name: str = "星座海报生成"
) -> dict:
    """上传图片到飞书多维表格附件字段

    Args:
        record_id: 记录 ID
        image_paths: 图片路径列表
        field_name: 附件字段名
        table_name: 表格名称

    Returns:
        {
            "success": True,
            "file_tokens": [...],
            "uploaded_count": N
        }
    """
    # 获取表格配置
    bitable = get_bitable(table_name)
    app_token = bitable["app_token"]
    table_id = bitable["table_id"]

    # 获取 token
    print("正在获取飞书访问令牌...")
    token = get_tenant_access_token()

    # 上传所有图片
    file_tokens = []
    for i, path in enumerate(image_paths, 1):
        print(f"正在上传图片 ({i}/{len(image_paths)}): {Path(path).name}")
        file_token = upload_file(token, path, app_token)
        file_tokens.append(file_token)
        print(f"  -> file_token: {file_token}")

    # 更新记录
    print(f"正在更新记录 {record_id}...")
    update_bitable_record(
        token=token,
        app_token=app_token,
        table_id=table_id,
        record_id=record_id,
        field_name=field_name,
        file_tokens=file_tokens
    )

    print(f"上传完成！共上传 {len(file_tokens)} 张图片")

    return {
        "success": True,
        "file_tokens": file_tokens,
        "uploaded_count": len(file_tokens)
    }


def main():
    parser = argparse.ArgumentParser(description="上传图片到飞书多维表格")
    parser.add_argument("--record-id", required=True, help="记录 ID")
    parser.add_argument("--images", nargs="+", help="图片路径列表")
    parser.add_argument("--dir", help="图片目录（会按文件名排序上传）")
    parser.add_argument("--field", default="生成图片", help="附件字段名")
    parser.add_argument("--table", default="星座海报生成", help="表格名称")

    args = parser.parse_args()

    # 收集图片路径
    image_paths = []

    if args.images:
        image_paths.extend(args.images)

    if args.dir:
        dir_path = Path(args.dir)
        if not dir_path.exists():
            print(f"错误：目录不存在 {args.dir}")
            sys.exit(1)

        # 支持的图片格式
        extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

        # 套图文件名规则：
        # - cover.png (封面)
        # - page-02.png ~ page-99.png (内容页，从02开始)
        # 排除：page-01.png (应该用cover.png), *-interaction.png 等非标准文件
        import re
        valid_pattern = re.compile(r'^(cover|page-0[2-9]|page-[1-9][0-9])\.png$', re.IGNORECASE)

        for f in sorted(dir_path.iterdir()):
            if f.suffix.lower() in extensions:
                # 检查是否符合套图命名规范
                if valid_pattern.match(f.name):
                    image_paths.append(str(f))
                else:
                    print(f"跳过非标准文件: {f.name}")

    if not image_paths:
        print("错误：请指定图片路径 (--images) 或图片目录 (--dir)")
        sys.exit(1)

    # 验证文件存在
    for path in image_paths:
        if not Path(path).exists():
            print(f"错误：文件不存在 {path}")
            sys.exit(1)

    # 执行上传
    try:
        result = upload_images_to_feishu(
            record_id=args.record_id,
            image_paths=image_paths,
            field_name=args.field,
            table_name=args.table
        )
        print(f"\n成功：已上传 {result['uploaded_count']} 张图片到飞书")
    except Exception as e:
        print(f"\n错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
