#!/usr/bin/env python3
"""
导出高清图片并上传到飞书多维表格
尺寸: 2160x2880px (2x of 1080x1440)
"""

import asyncio
import os
import requests
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))
from config import LARK_APP_ID, LARK_APP_SECRET, LARK_BITABLE_APP_TOKEN

# 飞书配置
FEISHU_APP_ID = LARK_APP_ID
FEISHU_APP_SECRET = LARK_APP_SECRET
FEISHU_APP_TOKEN = LARK_BITABLE_APP_TOKEN

# 页面配置
PAGES = [
    {"name": "封面", "button": "封面", "filename": "01_cover.png"},
    {"name": "情劫", "button": "情劫", "filename": "02_qingjie.png"},
    {"name": "TOP3", "button": "TOP3", "filename": "03_top3.png"},
    {"name": "TOP2", "button": "TOP2", "filename": "04_top2.png"},
    {"name": "TOP1", "button": "TOP1", "filename": "05_top1.png"},
    {"name": "成长", "button": "成长", "filename": "06_growth.png"},
    {"name": "结尾", "button": "结尾", "filename": "07_ending.png"},
]

OUTPUT_DIR = str((Path(__file__).resolve().parent / "exports").resolve())


def get_feishu_token():
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    })
    data = resp.json()
    if data.get("code") == 0:
        return data["tenant_access_token"]
    raise Exception(f"获取token失败: {data}")


def upload_image_to_feishu(token: str, file_path: str) -> str:
    """上传图片到飞书，返回 file_token"""
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        files = {"file": (file_name, f, "image/png")}
        data = {
            "file_name": file_name,
            "parent_type": "bitable_file",
            "parent_node": FEISHU_APP_TOKEN,
            "size": str(file_size)
        }
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data
        )

    result = resp.json()
    if result.get("code") == 0:
        return result["data"]["file_token"]
    raise Exception(f"上传失败: {result}")


def search_record(token: str, table_id: str, record_name: str):
    """搜索记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{table_id}/records/search"
    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "filter": {
                "conjunction": "and",
                "conditions": [
                    {"field_name": "标题", "operator": "contains", "value": [record_name]}
                ]
            }
        }
    )
    return resp.json()


def update_record(token: str, table_id: str, record_id: str, file_tokens: list):
    """更新记录的图文字段"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{table_id}/records/{record_id}"

    # 构建附件字段值
    attachments = [{"file_token": ft} for ft in file_tokens]

    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "fields": {
                "图文": attachments
            }
        }
    )
    return resp.json()


def create_record(token: str, table_id: str, title: str, file_tokens: list):
    """创建新记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{table_id}/records"

    attachments = [{"file_token": ft} for ft in file_tokens]

    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "fields": {
                "标题": title,
                "图文": attachments
            }
        }
    )
    return resp.json()


async def capture_screenshots():
    """使用 Playwright 截取高清图片"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    async with async_playwright() as p:
        # 启动浏览器，设置 deviceScaleFactor=2 实现 2x 分辨率
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 1080, "height": 1440},
            device_scale_factor=2  # 2x 分辨率，输出 2160x2880
        )
        page = await context.new_page()

        # 导航到预览页面
        await page.goto("http://localhost:8766/preview.html")
        await page.wait_for_timeout(2000)  # 等待字体加载

        # 移除缩放
        await page.evaluate("""
            () => {
                const container = document.querySelector('[style*="transform: scale"]');
                if (container) {
                    container.style.transform = 'none';
                    container.style.marginBottom = '0';
                }
            }
        """)

        screenshots = []

        for page_info in PAGES:
            # 点击按钮切换页面
            await page.click(f'button:has-text("{page_info["button"]}")')
            await page.wait_for_timeout(500)

            # 找到卡片元素并截图
            card = page.locator('[style*="width: 1080px"][style*="height: 1440px"]').first

            filepath = os.path.join(OUTPUT_DIR, page_info["filename"])
            await card.screenshot(path=filepath)
            screenshots.append(filepath)
            print(f"✅ 已导出: {page_info['filename']} (2160x2880)")

        await browser.close()
        return screenshots


async def main():
    print("=" * 50)
    print("开始导出高清图片并上传到飞书")
    print("=" * 50)

    # 1. 截取图片
    print("\n📸 步骤1: 截取高清图片 (2160x2880)...")
    screenshots = await capture_screenshots()
    print(f"共导出 {len(screenshots)} 张图片")

    # 2. 获取飞书 token
    print("\n🔑 步骤2: 获取飞书 access_token...")
    token = get_feishu_token()
    print("✅ Token 获取成功")

    # 3. 上传图片
    print("\n☁️ 步骤3: 上传图片到飞书...")
    file_tokens = []
    for filepath in screenshots:
        file_token = upload_image_to_feishu(token, filepath)
        file_tokens.append(file_token)
        print(f"  ✅ 已上传: {os.path.basename(filepath)} -> {file_token}")

    # 4. 更新/创建记录
    print("\n📝 步骤4: 更新多维表格记录...")
    # 这里需要知道 table_id，先列出所有表

    return file_tokens


if __name__ == "__main__":
    asyncio.run(main())
