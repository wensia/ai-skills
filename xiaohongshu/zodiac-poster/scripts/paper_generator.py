#!/usr/bin/env python3
"""
纸质风格海报生成器

专用于生成纸质风格（paper style）的星座海报，使用独立的模板布局。
"""

import json
import os
import sys
import tempfile
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.config_loader import ConfigLoader

# 默认输出目录
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "output"
ASSETS_DIR = Path(__file__).parent.parent / "assets"


@dataclass
class PageConfig:
    """页面配置"""
    usage: str  # cover 或 long
    headline: str
    sub_line: str = ""
    line3: str = ""
    body: List[str] = None


@dataclass
class PaperBatchConfig:
    """纸质风格批量配置"""
    zodiac: str
    color: str
    font: Optional[str]
    pages: List[PageConfig]
    output_dir: Optional[Path] = None


def load_zodiac_symbols() -> dict:
    """加载星座符号 SVG"""
    symbols_path = ASSETS_DIR / "zodiac-symbols.json"
    with open(symbols_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_template(template_name: str) -> str:
    """加载模板文件"""
    template_path = ASSETS_DIR / template_name
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def get_font_family(font_id: str, config: ConfigLoader) -> str:
    """获取字体 family"""
    if font_id:
        font_data = config.get_font(font_id)
        if font_data:
            return font_data.get("family", "'Noto Serif SC', serif")
    return "'Noto Serif SC', serif"


def get_font_links(font_id: str, config: ConfigLoader) -> str:
    """生成字体 CSS 链接"""
    links = []

    # 默认加载思源宋体
    links.append('<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">')

    # 如果指定了其他字体，加载本地字体
    if font_id and font_id != 'songti':
        font_data = config.get_font(font_id)
        if font_data:
            for css_file in font_data.get("css_files", []):
                links.append(f'<link rel="stylesheet" href="{css_file}">')

    return "\n    ".join(links)


def render_cover(
    zodiac: str,
    headline: str,
    sub_line: str,
    line3: str,
    color_id: str,
    font_id: str,
    config: ConfigLoader,
    symbols: dict
) -> str:
    """渲染封面"""
    template = load_template("paper-cover-template.html")
    color_data = config.get_color(color_id)
    palette = color_data.get("palette", {})
    zodiac_data = config.get_zodiac(zodiac)

    replacements = {
        "{{POSTER_WIDTH}}": "1080px",
        "{{POSTER_HEIGHT}}": "1440px",
        "{{BG_PRIMARY}}": palette.get("bg_primary", "#FCF8EB"),
        "{{ACCENT}}": palette.get("accent", "#78553C"),
        "{{ACCENT_SOFT}}": palette.get("accent_soft", "#C8B9A5"),
        "{{TEXT_DARK}}": palette.get("text_dark", "#41322A"),
        "{{TEXT_MUTED}}": palette.get("text_muted", "#96826E"),
        "{{FONT_FAMILY}}": get_font_family(font_id, config),
        "{{FONT_LINKS}}": get_font_links(font_id, config),
        "{{ZODIAC_NAME}}": zodiac,
        "{{HEADLINE}}": headline,
        "{{SUB_LINE}}": sub_line,
        "{{LINE3}}": line3,
        "{{SHOW_LINE3}}": "block" if line3 else "none",
        "{{ZODIAC_SYMBOL_SVG}}": symbols.get(zodiac, {}).get("svg", ""),
    }

    html = template
    for key, value in replacements.items():
        html = html.replace(key, str(value))

    return html


def render_long(
    zodiac: str,
    headline: str,
    body: List[str],
    color_id: str,
    font_id: str,
    config: ConfigLoader,
    symbols: dict
) -> str:
    """渲染长文案"""
    template = load_template("paper-long-template.html")
    color_data = config.get_color(color_id)
    palette = color_data.get("palette", {})

    # 格式化正文
    body_html = "\n".join(f"<p>{line}</p>" for line in body) if body else ""

    replacements = {
        "{{POSTER_WIDTH}}": "1080px",
        "{{POSTER_HEIGHT}}": "1440px",
        "{{BG_PRIMARY}}": palette.get("bg_primary", "#FCF8EB"),
        "{{ACCENT_SOFT}}": palette.get("accent_soft", "#C8B9A5"),
        "{{TEXT_DARK}}": palette.get("text_dark", "#41322A"),
        "{{TEXT_MUTED}}": palette.get("text_muted", "#96826E"),
        "{{FONT_FAMILY}}": get_font_family(font_id, config),
        "{{FONT_LINKS}}": get_font_links(font_id, config),
        "{{ZODIAC_NAME}}": zodiac,
        "{{HEADLINE}}": headline,
        "{{BODY_TEXT}}": body_html,
        "{{ZODIAC_SYMBOL_SVG}}": symbols.get(zodiac, {}).get("svg", ""),
    }

    html = template
    for key, value in replacements.items():
        html = html.replace(key, str(value))

    return html


def html_to_png(html_path: str, output_path: str, width: int = 1080, height: int = 1440) -> str:
    """使用 Playwright 将 HTML 转换为 PNG"""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=2  # 2x 导出，实际像素翻倍
        )
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")

        poster = page.locator(".poster")
        poster.screenshot(path=output_path)

        browser.close()

    return output_path


def generate_paper_batch(batch_config: PaperBatchConfig, config: ConfigLoader) -> List[str]:
    """批量生成纸质风格海报"""
    symbols = load_zodiac_symbols()

    # 输出目录
    output_dir = batch_config.output_dir or DEFAULT_OUTPUT_DIR
    now = datetime.now()
    date_dir = output_dir / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")

    timestamp = now.strftime("%y%m%d-%H%M")
    theme = batch_config.pages[0].headline[:8] if batch_config.pages else "海报"
    theme = "".join(c for c in theme if c.isalnum() or c in "一二三四五六七八九十")

    # 创建套图专属文件夹
    batch_folder_name = f"{batch_config.zodiac}-{theme}-{timestamp}"
    batch_dir = date_dir / batch_folder_name
    batch_dir.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for i, page in enumerate(batch_config.pages, 1):
        # 渲染 HTML
        if page.usage == "cover":
            html = render_cover(
                zodiac=batch_config.zodiac,
                headline=page.headline,
                sub_line=page.sub_line,
                line3=page.line3,
                color_id=batch_config.color,
                font_id=batch_config.font,
                config=config,
                symbols=symbols
            )
        else:
            html = render_long(
                zodiac=batch_config.zodiac,
                headline=page.headline,
                body=page.body or [],
                color_id=batch_config.color,
                font_id=batch_config.font,
                config=config,
                symbols=symbols
            )

        # 保存临时 HTML
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html)
            temp_html = f.name

        # 生成输出路径
        usage_suffix = "cover" if page.usage == "cover" else "long"
        filename = f"{i:02d}-{usage_suffix}.png"
        output_path = batch_dir / filename

        # 生成 PNG
        try:
            result = html_to_png(temp_html, str(output_path))
            generated_files.append(result)
            print(f"  [{i}/{len(batch_config.pages)}] {page.usage}: {filename}")
            os.unlink(temp_html)
        except Exception as e:
            print(f"  [{i}/{len(batch_config.pages)}] 失败: {e}")

    # 生成清单文件
    manifest = {
        "generated_at": now.isoformat(),
        "zodiac": batch_config.zodiac,
        "color": batch_config.color,
        "style": "paper",
        "font": batch_config.font,
        "files": [str(f) for f in generated_files]
    }
    manifest_path = batch_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n  文件夹: {batch_dir}")
    return generated_files


def parse_cover_content(content_str: str) -> PageConfig:
    """解析封面内容"""
    parts = content_str.split("|")
    return PageConfig(
        usage="cover",
        headline=parts[0] if len(parts) > 0 else "",
        sub_line=parts[1] if len(parts) > 1 else "",
        line3=parts[2] if len(parts) > 2 else ""
    )


def parse_long_content(content_str: str) -> PageConfig:
    """解析长文案内容"""
    parts = content_str.split("|")
    return PageConfig(
        usage="long",
        headline=parts[0] if len(parts) > 0 else "",
        body=parts[1:] if len(parts) > 1 else []
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="纸质风格星座海报生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 paper_generator.py --zodiac 射手座 --color parchment --font songti \\
      --cover "别追了|射手回避型|真正吃这一套" \\
      --long "射手座的回避型人格|你越靠近，他越想呼吸|你越追问，他越沉默|空间不是冷漠，而是安全感的来源"
        """
    )

    parser.add_argument("--zodiac", "-z", required=True, help="星座名称")
    parser.add_argument("--color", default="parchment", help="配色（默认: parchment）")
    parser.add_argument("--font", "-f", help="字体：wenkai/songti/alibaba/ziyuan/fasmart",
                        choices=["wenkai", "songti", "alibaba", "ziyuan", "fasmart"], default="songti")
    parser.add_argument("--cover", action="append", help="封面内容（可多次指定）")
    parser.add_argument("--long", action="append", help="长文案内容（可多次指定）")
    parser.add_argument("--output-dir", "-d", type=Path, help="输出目录")

    args = parser.parse_args()

    # 初始化
    config = ConfigLoader()

    # 解析页面
    pages = []

    if args.cover:
        for cover_content in args.cover:
            pages.append(parse_cover_content(cover_content))

    if args.long:
        for long_content in args.long:
            pages.append(parse_long_content(long_content))

    if not pages:
        parser.error("至少需要指定一个 --cover 或 --long")

    batch_config = PaperBatchConfig(
        zodiac=args.zodiac,
        color=args.color,
        font=args.font,
        pages=pages,
        output_dir=args.output_dir
    )

    # 显示配置
    color_name = config.get_color(batch_config.color)
    font_name = config.get_font(batch_config.font) if batch_config.font else None
    print(f"纸质风格生成配置:")
    print(f"  星座: {batch_config.zodiac}")
    print(f"  配色: {color_name.get('name') if color_name else batch_config.color}")
    print(f"  字体: {font_name.get('name') if font_name else '思源宋体'}")
    print(f"  页数: {len(batch_config.pages)}")
    print()
    print("正在生成...")

    # 执行生成
    results = generate_paper_batch(batch_config, config)

    print(f"\n✓ 完成！共生成 {len(results)} 张海报")
