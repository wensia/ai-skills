#!/usr/bin/env python3
"""
星座海报生成器 - 无头模式
使用 Playwright 无头浏览器将 HTML 转换为 PNG

用法:
  python3 generate_poster.py <input.html> -z 天秤座 -t 无声告别
  python3 generate_poster.py <input.html> -o /path/to/output.png
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 默认输出根目录
DEFAULT_OUTPUT_DIR = os.environ.get("XHS_POSTER_OUTPUT_DIR", str(Path(__file__).resolve().parents[2] / "output"))


def get_output_path(base_dir: str, zodiac: str, theme: str) -> Path:
    """生成输出路径：base_dir/YYYY/MM/DD/星座-主题-YYMMDD-HHmm.png"""
    now = datetime.now()

    # 创建日期目录
    date_dir = Path(base_dir) / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
    date_dir.mkdir(parents=True, exist_ok=True)

    # 生成文件名
    timestamp = now.strftime("%y%m%d-%H%M")
    filename = f"{zodiac}-{theme}-{timestamp}.png"

    return date_dir / filename


def html_to_png_playwright(html_path: str, output_path: str, width: int = 1080, height: int = 1440) -> str:
    """使用 Playwright 无头模式将 HTML 转换为 PNG"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("错误: 请先安装 playwright")
        print("运行: pip install playwright && playwright install chromium")
        sys.exit(1)

    with sync_playwright() as p:
        # 启动无头浏览器
        browser = p.chromium.launch(headless=True)

        # 创建页面，设置视口大小，2x 导出
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=2  # 2x 导出，实际像素翻倍
        )

        # 加载 HTML 文件
        html_url = f"file://{os.path.abspath(html_path)}"
        page.goto(html_url)

        # 等待字体加载
        page.wait_for_timeout(2000)

        # 截图 - 尝试找到 .poster 元素，否则截取整个页面
        poster = page.query_selector(".poster")
        if poster:
            poster.screenshot(path=output_path)
        else:
            page.screenshot(path=output_path)

        browser.close()

    return output_path


def html_to_png_wkhtmltoimage(html_path: str, output_path: str, width: int = 1080, height: int = 1440) -> str:
    """使用 wkhtmltoimage 将 HTML 转换为 PNG（备选方案）"""
    import subprocess

    cmd = [
        "wkhtmltoimage",
        "--width", str(width),
        "--height", str(height),
        "--quality", "100",
        "--disable-javascript",
        str(html_path),
        str(output_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 or Path(output_path).exists():
            return output_path
        else:
            raise Exception(f"wkhtmltoimage 错误: {result.stderr}")
    except FileNotFoundError:
        raise Exception("未找到 wkhtmltoimage，请安装或使用 playwright")


def main():
    parser = argparse.ArgumentParser(
        description="星座海报生成器 - 无头模式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s input.html -z 天秤座 -t 无声告别
  %(prog)s input.html -o /custom/path/output.png
  %(prog)s input.html --engine wkhtmltoimage
        """
    )
    parser.add_argument("html_file", help="输入的 HTML 文件路径")
    parser.add_argument("-o", "--output", help="完整输出路径（指定后忽略 -z/-t）")
    parser.add_argument("-d", "--output-dir", help=f"输出根目录（默认: {DEFAULT_OUTPUT_DIR}）",
                        default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("-z", "--zodiac", help="星座名称（默认: 星座）", default="星座")
    parser.add_argument("-t", "--theme", help="主题名称（默认: 海报）", default="海报")
    parser.add_argument("-W", "--width", type=int, help="宽度（默认: 1080）", default=1080)
    parser.add_argument("-H", "--height", type=int, help="高度（默认: 1440）", default=1440)
    parser.add_argument("-e", "--engine", choices=["playwright", "wkhtmltoimage"],
                        help="渲染引擎（默认: playwright）", default="playwright")

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.html_file):
        print(f"错误: 文件不存在 - {args.html_file}")
        sys.exit(1)

    # 确定输出路径
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path = get_output_path(args.output_dir, args.zodiac, args.theme)

    print(f"正在生成海报 (无头模式)...")
    print(f"  引擎: {args.engine}")
    print(f"  输入: {args.html_file}")
    print(f"  输出: {output_path}")

    # 生成图片
    try:
        if args.engine == "playwright":
            result = html_to_png_playwright(args.html_file, str(output_path), args.width, args.height)
        else:
            result = html_to_png_wkhtmltoimage(args.html_file, str(output_path), args.width, args.height)

        print(f"✓ 生成成功: {result}")
        return result
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
