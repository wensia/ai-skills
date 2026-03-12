#!/usr/bin/env python3
"""
SVG/HTML 截图工具 - 使用 Playwright + Canvas API 实现精确 2x 截图

使用方法:
    from utils.screenshot import svg_to_png, html_to_png, render_template_to_png

    # SVG 转 PNG (2x 分辨率)
    svg_to_png('input.svg', 'output.png')

    # HTML 转 PNG (2x 分辨率)
    html_to_png('input.html', 'output.png')

    # 🌟 推荐方案：HTML模板 + 数据注入 → PNG
    render_template_to_png(
        template_path='cover.html',
        output_path='output.png',
        data={'zodiac': '射手座', 'title': '标题'}
    )

    # 批量渲染模板
    batch_render_templates(pages_data, output_dir='./output')
"""

import os
import json
import base64
import asyncio
from playwright.async_api import async_playwright
from typing import Dict, List, Any, Optional


# 默认画布尺寸 (小红书 3:4 比例)
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1440
DEFAULT_SCALE = 2  # 2x 分辨率


def _create_canvas_html(svg_content: str, width: int, height: int, scale: int) -> str:
    """创建使用 Canvas API 渲染 SVG 的 HTML"""
    out_width = width * scale
    out_height = height * scale
    # SVG 内容 base64 编码以避免转义问题
    svg_b64 = base64.b64encode(svg_content.encode('utf-8')).decode('ascii')

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{ background: transparent; }}
        canvas {{ display: block; }}
    </style>
</head>
<body>
    <canvas id="canvas" width="{out_width}" height="{out_height}"></canvas>
    <script>
        async function render() {{
            const svgB64 = "{svg_b64}";
            // 正确处理 UTF-8 编码
            const binaryString = atob(svgB64);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {{
                bytes[i] = binaryString.charCodeAt(i);
            }}
            const svgContent = new TextDecoder('utf-8').decode(bytes);

            const blob = new Blob([svgContent], {{type: 'image/svg+xml;charset=utf-8'}});
            const url = URL.createObjectURL(blob);

            const img = new Image();
            img.width = {out_width};
            img.height = {out_height};

            await new Promise((resolve, reject) => {{
                img.onload = resolve;
                img.onerror = reject;
                img.src = url;
            }});

            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, {out_width}, {out_height});

            URL.revokeObjectURL(url);

            // 返回 base64 PNG 数据
            window.pngData = canvas.toDataURL('image/png');
            window.renderDone = true;
        }}
        render();
    </script>
</body>
</html>"""


async def _svg_to_png_async(
    svg_path: str,
    output_path: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE
) -> bool:
    """异步将 SVG 转换为 PNG"""
    out_width = width * scale
    out_height = height * scale

    # 读取 SVG 内容
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    html_content = _create_canvas_html(svg_content, width, height, scale)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': out_width, 'height': out_height})

        # 加载 HTML
        await page.set_content(html_content)

        # 等待渲染完成
        await page.wait_for_function('window.renderDone === true', timeout=10000)

        # 获取 PNG 数据
        png_data_url = await page.evaluate('window.pngData')

        await browser.close()

    # 解码并保存 PNG
    png_b64 = png_data_url.split(',')[1]
    png_bytes = base64.b64decode(png_b64)

    with open(output_path, 'wb') as f:
        f.write(png_bytes)

    return True


async def _html_to_png_async(
    html_path: str,
    output_path: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE,
    wait_time: int = 2500
) -> bool:
    """异步将 HTML 转换为 PNG (使用 Canvas API 导出)"""
    out_width = width * scale
    out_height = height * scale

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': out_width, 'height': out_height})

        # 打开 HTML 文件
        await page.goto(f'file://{os.path.abspath(html_path)}')

        # 等待字体加载
        await page.wait_for_timeout(wait_time)

        # 注入 Canvas 导出脚本
        png_data_url = await page.evaluate(f'''() => {{
            return new Promise((resolve, reject) => {{
                const svg = document.querySelector('svg');
                if (!svg) {{
                    reject(new Error('No SVG found'));
                    return;
                }}

                // Clone SVG
                const svgClone = svg.cloneNode(true);
                svgClone.setAttribute('width', '{out_width}');
                svgClone.setAttribute('height', '{out_height}');

                const svgString = new XMLSerializer().serializeToString(svgClone);
                const blob = new Blob([svgString], {{type: 'image/svg+xml;charset=utf-8'}});
                const url = URL.createObjectURL(blob);

                const img = new Image();
                img.onload = () => {{
                    const canvas = document.createElement('canvas');
                    canvas.width = {out_width};
                    canvas.height = {out_height};
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, {out_width}, {out_height});
                    URL.revokeObjectURL(url);
                    resolve(canvas.toDataURL('image/png'));
                }};
                img.onerror = reject;
                img.src = url;
            }});
        }}''')

        await browser.close()

    # 解码并保存 PNG
    png_b64 = png_data_url.split(',')[1]
    png_bytes = base64.b64decode(png_b64)

    with open(output_path, 'wb') as f:
        f.write(png_bytes)

    return True


def svg_to_png(
    svg_path: str,
    output_path: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE
) -> bool:
    """
    将 SVG 文件转换为 PNG 图片

    参数:
        svg_path: SVG 文件路径
        output_path: 输出 PNG 文件路径
        width: 画布宽度 (默认 1080)
        height: 画布高度 (默认 1440)
        scale: 缩放倍数 (默认 2, 即 2x 分辨率)

    返回:
        bool: 是否成功
    """
    return asyncio.run(_svg_to_png_async(svg_path, output_path, width, height, scale))


def html_to_png(
    html_path: str,
    output_path: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE,
    wait_time: int = 2500
) -> bool:
    """
    将 HTML 文件转换为 PNG 图片 (HTML 中需包含 SVG)

    参数:
        html_path: HTML 文件路径
        output_path: 输出 PNG 文件路径
        width: 画布宽度 (默认 1080)
        height: 画布高度 (默认 1440)
        scale: 缩放倍数 (默认 2, 即 2x 分辨率)
        wait_time: 等待字体加载时间 (毫秒, 默认 2500)

    返回:
        bool: 是否成功
    """
    return asyncio.run(_html_to_png_async(html_path, output_path, width, height, scale, wait_time))


def batch_svg_to_png(
    svg_paths: list,
    output_dir: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE
) -> list:
    """
    批量将 SVG 文件转换为 PNG

    参数:
        svg_paths: SVG 文件路径列表
        output_dir: 输出目录
        width: 画布宽度
        height: 画布高度
        scale: 缩放倍数

    返回:
        list: 成功生成的 PNG 文件路径列表
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for svg_path in svg_paths:
        filename = os.path.splitext(os.path.basename(svg_path))[0] + '.png'
        output_path = os.path.join(output_dir, filename)

        try:
            svg_to_png(svg_path, output_path, width, height, scale)
            results.append(output_path)
            print(f"✅ {filename} ({width * scale}x{height * scale})")
        except Exception as e:
            print(f"❌ {filename}: {e}")

    return results


# ============================================
# 🌟 推荐方案：HTML 模板 + 数据注入
# ============================================

def _inject_data_to_html(html_content: str, data: Dict[str, Any]) -> str:
    """
    在 HTML 内容中注入 window.POSTER_DATA

    将数据注入到 </head> 标签之前，确保在 React 渲染之前数据就已可用
    """
    data_json = json.dumps(data, ensure_ascii=False)
    injection = f"""
    <script>
      // 注入的海报数据 (由 screenshot.py 自动生成)
      window.POSTER_DATA = {data_json};
    </script>
    """
    return html_content.replace('</head>', injection + '</head>')


async def _render_template_async(
    template_path: str,
    output_path: str,
    data: Dict[str, Any],
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE,
    wait_time: int = 3000
) -> bool:
    """
    异步渲染 HTML 模板并导出为 PNG

    流程:
    1. 读取 HTML 模板
    2. 注入 window.POSTER_DATA
    3. Playwright 加载并渲染
    4. 使用 Canvas API 导出 PNG (避免截图偏移问题)
    """
    out_width = width * scale
    out_height = height * scale

    # 读取模板并注入数据
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    html_with_data = _inject_data_to_html(html_content, data)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': out_width, 'height': out_height})

        # 直接设置 HTML 内容 (比 goto file:// 更可靠)
        await page.set_content(html_with_data)

        # 等待字体加载和 React 渲染
        await page.wait_for_timeout(wait_time)

        # 使用 Canvas API 导出 SVG → PNG
        png_data_url = await page.evaluate(f'''() => {{
            return new Promise((resolve, reject) => {{
                const svg = document.querySelector('#poster-svg');
                if (!svg) {{
                    reject(new Error('No #poster-svg element found'));
                    return;
                }}

                // Clone SVG 并设置输出尺寸
                const svgClone = svg.cloneNode(true);
                svgClone.setAttribute('width', '{out_width}');
                svgClone.setAttribute('height', '{out_height}');

                // 序列化为字符串
                const svgString = new XMLSerializer().serializeToString(svgClone);
                const blob = new Blob([svgString], {{type: 'image/svg+xml;charset=utf-8'}});
                const url = URL.createObjectURL(blob);

                // 绘制到 Canvas
                const img = new Image();
                img.onload = () => {{
                    const canvas = document.createElement('canvas');
                    canvas.width = {out_width};
                    canvas.height = {out_height};
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, {out_width}, {out_height});
                    URL.revokeObjectURL(url);
                    resolve(canvas.toDataURL('image/png'));
                }};
                img.onerror = (e) => {{
                    URL.revokeObjectURL(url);
                    reject(new Error('Failed to load SVG as image'));
                }};
                img.src = url;
            }});
        }}''')

        await browser.close()

    # 解码并保存 PNG
    png_b64 = png_data_url.split(',')[1]
    png_bytes = base64.b64decode(png_b64)

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(png_bytes)

    return True


def render_template_to_png(
    template_path: str,
    output_path: str,
    data: Dict[str, Any],
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE,
    wait_time: int = 3000
) -> bool:
    """
    🌟 推荐方案：将 HTML 模板 + 数据渲染为 PNG

    此方法解决了以下问题:
    - 数据在页面加载前注入，确保 React 组件正确读取
    - 使用 Canvas API 导出，避免 Playwright 元素截图的偏移问题
    - 输出 2x 分辨率 (2160x2880)，满足小红书高清要求

    参数:
        template_path: HTML 模板文件路径 (需包含 React 组件和 #poster-svg)
        output_path: 输出 PNG 文件路径
        data: 要注入的数据字典 (将设置为 window.POSTER_DATA)
        width: 画布宽度 (默认 1080)
        height: 画布高度 (默认 1440)
        scale: 缩放倍数 (默认 2, 即 2x 分辨率)
        wait_time: 等待渲染时间 (毫秒, 默认 3000)

    返回:
        bool: 是否成功

    示例:
        render_template_to_png(
            template_path='templates/cover.html',
            output_path='output/cover.png',
            data={
                'zodiac': '射手座',
                'topic': 'MBTI解读',
                'titleLine1': '射手座最可能是',
                'titleLine2': '什么MBTI'
            }
        )
    """
    return asyncio.run(_render_template_async(
        template_path, output_path, data, width, height, scale, wait_time
    ))


def batch_render_templates(
    pages_data: List[Dict[str, Any]],
    output_dir: str,
    template_dir: Optional[str] = None,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE,
    wait_time: int = 3000
) -> List[str]:
    """
    批量渲染多个 HTML 模板为 PNG

    参数:
        pages_data: 页面数据列表，每项包含:
            - template: 模板文件名 (如 'cover.html')
            - output: 输出文件名 (如 '01_cover.png')
            - data: 要注入的数据字典
        output_dir: 输出目录
        template_dir: 模板目录 (可选，不指定则使用 template 字段的完整路径)
        width: 画布宽度
        height: 画布高度
        scale: 缩放倍数
        wait_time: 等待渲染时间

    返回:
        list: 成功生成的 PNG 文件路径列表

    示例:
        pages = [
            {
                'template': 'cover.html',
                'output': '01_cover.png',
                'data': {'zodiac': '射手座', 'titleLine1': '标题'}
            },
            {
                'template': 'page.html',
                'output': '02_page.png',
                'data': {'zodiac': '射手座', 'partNum': '01'}
            }
        ]
        batch_render_templates(pages, './output', './templates')
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []
    total = len(pages_data)

    for i, page_info in enumerate(pages_data):
        template_name = page_info.get('template', '')
        output_name = page_info.get('output', f'page_{i+1}.png')
        data = page_info.get('data', {})

        # 确定模板路径
        if template_dir:
            template_path = os.path.join(template_dir, template_name)
        else:
            template_path = template_name

        output_path = os.path.join(output_dir, output_name)

        print(f"[{i+1}/{total}] 渲染 {output_name}...")

        try:
            render_template_to_png(
                template_path, output_path, data,
                width, height, scale, wait_time
            )
            size_kb = os.path.getsize(output_path) // 1024
            print(f"    ✓ 完成 ({size_kb}KB)")
            results.append(output_path)
        except Exception as e:
            print(f"    ✗ 失败: {e}")

    return results


# CLI 入口
if __name__ == "__main__":
    import sys
    import glob

    if len(sys.argv) < 2:
        print("Usage: python screenshot.py <svg_file_or_pattern> [output_dir]")
        print("       python screenshot.py --template <html_file> --data '<json>' --output <png_file>")
        print("")
        print("Examples:")
        print("  python screenshot.py '*.svg' ./output")
        print("  python screenshot.py --template cover.html --data '{\"zodiac\":\"射手座\"}' --output cover.png")
        sys.exit(1)

    # 检查是否使用模板模式
    if sys.argv[1] == '--template':
        if len(sys.argv) < 7:
            print("Error: --template mode requires --data and --output")
            sys.exit(1)

        template_path = sys.argv[2]
        data_json = sys.argv[4]
        output_path = sys.argv[6]

        try:
            data = json.loads(data_json)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON data: {e}")
            sys.exit(1)

        print(f"📸 渲染模板: {template_path}")
        render_template_to_png(template_path, output_path, data)
        print(f"✨ 完成: {output_path}")
    else:
        # SVG 批量模式
        pattern = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'

        svg_files = glob.glob(pattern)
        if not svg_files:
            print(f"No files found matching: {pattern}")
            sys.exit(1)

        print(f"📸 开始截图 (3:4 比例, 2x 分辨率)...")
        results = batch_svg_to_png(svg_files, output_dir)
        print(f"✨ 完成! 共 {len(results)} 张")
