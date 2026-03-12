#!/usr/bin/env python3
"""
星座海报批量生成器

支持一次性生成一套同风格的封面 + 多张长文案图

用法:
  # 命令行模式
  python3 batch_generator.py --zodiac 射手座 --color 温暖 --style 经典 \
      --cover "封面标题|副标题" \
      --long "标题|副标题|正文1|正文2|强调" \
      --long "标题|正文内容"

  # JSON 配置模式
  python3 batch_generator.py --config batch.json
"""

import os
import sys
import json
import argparse
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core import ConfigLoader, TemplateRenderer

# 路径配置
SCRIPT_DIR = Path(__file__).parent
DEFAULT_OUTPUT_DIR = Path(os.environ.get("XHS_POSTER_OUTPUT_DIR", str(Path(__file__).resolve().parents[2] / "output")))


@dataclass
class PageConfig:
    """单页配置"""
    usage: str  # "cover" 或 "long"
    headline: str = ""
    sub_line: str = ""  # 封面用
    subtitle: str = ""  # 长文案用
    body: List[str] = field(default_factory=list)
    emphasis: str = ""
    footer: str = ""


@dataclass
class BatchConfig:
    """批量生成配置"""
    zodiac: str
    color: str
    style: str
    pages: List[PageConfig]
    output_dir: Optional[Path] = None
    font: Optional[str] = None  # 字体ID: wenkai(霞鹜文楷) 或 songti(思源宋体)


def parse_page_content(content_str: str, usage: str) -> PageConfig:
    """
    解析页面内容字符串

    格式: "部分1|部分2|部分3..."
    封面: "标题|副行"
    长文案: "标题|副标题|正文1|正文2...|[强调]"
    """
    parts = [p.strip() for p in content_str.split("|")]
    page = PageConfig(usage=usage)

    if usage == "cover":
        page.headline = parts[0] if len(parts) > 0 else ""
        page.sub_line = parts[1] if len(parts) > 1 else ""
        if len(parts) > 2:
            page.sub_line += "<br>" + parts[2]
    else:
        page.headline = parts[0] if len(parts) > 0 else ""
        page.subtitle = parts[1] if len(parts) > 1 else ""
        # 最后一部分如果以 [xxx] 格式，作为强调
        if len(parts) > 2:
            remaining = parts[2:]
            if remaining and remaining[-1].startswith("[") and remaining[-1].endswith("]"):
                page.emphasis = remaining[-1][1:-1]
                page.body = remaining[:-1]
            else:
                page.body = remaining

    return page


def load_batch_config(config_path: Path) -> BatchConfig:
    """从 JSON 文件加载批量配置"""
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pages = []
    for page_data in data.get("pages", []):
        page = PageConfig(
            usage=page_data.get("usage", "cover"),
            headline=page_data.get("headline", ""),
            sub_line=page_data.get("sub_line", ""),
            subtitle=page_data.get("subtitle", ""),
            body=page_data.get("body", []),
            emphasis=page_data.get("emphasis", ""),
            footer=page_data.get("footer", "")
        )
        pages.append(page)

    return BatchConfig(
        zodiac=data.get("zodiac", "射手座"),
        color=data.get("color", "warm-apricot"),
        style=data.get("style", "classic"),
        pages=pages,
        output_dir=Path(data["output_dir"]) if "output_dir" in data else None,
        font=data.get("font")
    )


def html_to_png(html_path: str, output_path: str, width: int = 1080, height: int = 1440) -> str:
    """使用 Playwright 将 HTML 转换为 PNG"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("错误: 请先安装 playwright")
        print("运行: pip install playwright && playwright install chromium")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=2  # 2x 导出，实际像素翻倍
        )
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.wait_for_timeout(2000)

        poster = page.query_selector(".poster")
        if poster:
            poster.screenshot(path=output_path)
        else:
            page.screenshot(path=output_path)

        browser.close()

    return output_path


def generate_batch(batch_config: BatchConfig, config: ConfigLoader, renderer: TemplateRenderer) -> List[str]:
    """
    批量生成海报

    Returns:
        生成的文件路径列表
    """
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
        # 生成底部文字
        footer = page.footer
        if not footer:
            if page.usage == "cover":
                footer = f"{batch_config.zodiac} · 星座物语"
            else:
                footer = "给予理解 · 收获真心"

        # 构建内容
        content = {
            "headline": page.headline,
            "sub_line": page.sub_line,
            "subtitle": page.subtitle,
            "body": page.body,
            "emphasis": page.emphasis,
            "footer": footer
        }

        # 渲染 HTML
        html = renderer.render(
            color_id=batch_config.color,
            usage_id=page.usage,
            style_id=batch_config.style,
            zodiac_name=batch_config.zodiac,
            content=content,
            font_id=batch_config.font
        )

        # 保存临时 HTML
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html)
            temp_html = f.name

        # 生成输出路径（简化文件名，因为文件夹名已包含信息）
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

    # 生成清单文件（放在套图文件夹内）
    manifest = {
        "generated_at": now.isoformat(),
        "zodiac": batch_config.zodiac,
        "color": batch_config.color,
        "style": batch_config.style,
        "files": [str(f) for f in generated_files]
    }
    manifest_path = batch_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n  文件夹: {batch_dir}")
    return generated_files


def main():
    parser = argparse.ArgumentParser(
        description="星座海报批量生成器 - 一次生成封面+多张长文案",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用命令行参数
  %(prog)s --zodiac 射手座 --color 温暖 --style 经典 \\
      --cover "射手座的真心|从不轻易给出" \\
      --long "射手座在感情里|看似潇洒实则深情|自由是本能|真心是选择|[请好好珍惜]" \\
      --long "和射手座相处|给他空间|理解他的自由"

  # 使用 JSON 配置文件
  %(prog)s --config batch.json

JSON 配置示例:
  {
    "zodiac": "射手座",
    "color": "warm-apricot",
    "style": "classic",
    "pages": [
      {"usage": "cover", "headline": "标题", "sub_line": "副行"},
      {"usage": "long", "headline": "标题", "subtitle": "副标题", "body": ["正文1", "正文2"], "emphasis": "强调"}
    ]
  }

内容格式 (用 | 分隔):
  封面: "标题|副行|副行2"
  长文案: "标题|副标题|正文1|正文2|...|[强调]"
        """
    )

    parser.add_argument("--config", "-c", type=Path, help="JSON 配置文件路径")
    parser.add_argument("--zodiac", "-z", help="星座名称")
    parser.add_argument("--color", help="配色方案（ID或关键词）", default="warm-apricot")
    parser.add_argument("--style", "-s", help="风格（ID或关键词）", default="classic")
    parser.add_argument("--font", "-f", help="字体：wenkai(霞鹜文楷)/songti(思源宋体)/alibaba(阿里巴巴普惠体)/ziyuan(资源圆体)/fasmart(霞鹜尚智黑)",
                        choices=["wenkai", "songti", "alibaba", "ziyuan", "fasmart"], default=None)
    parser.add_argument("--cover", action="append", help="封面内容（可多次指定）")
    parser.add_argument("--long", action="append", help="长文案内容（可多次指定）")
    parser.add_argument("--output-dir", "-d", type=Path, help="输出目录")

    args = parser.parse_args()

    # 初始化核心模块
    config = ConfigLoader()
    renderer = TemplateRenderer(config)

    # 加载配置
    if args.config:
        batch_config = load_batch_config(args.config)
    else:
        if not args.zodiac:
            parser.error("必须指定 --zodiac 或 --config")

        pages = []

        # 解析封面
        if args.cover:
            for cover_content in args.cover:
                pages.append(parse_page_content(cover_content, "cover"))

        # 解析长文案
        if args.long:
            for long_content in args.long:
                pages.append(parse_page_content(long_content, "long"))

        if not pages:
            parser.error("至少需要指定一个 --cover 或 --long")

        # 解析配色和风格（支持关键词）
        color_id = config.get_color_id(args.color) or args.color
        style_id = config.get_style_id(args.style) or args.style

        batch_config = BatchConfig(
            zodiac=args.zodiac,
            color=color_id,
            style=style_id,
            pages=pages,
            output_dir=args.output_dir,
            font=args.font
        )

    # 显示配置信息
    color_name = config.get_color(batch_config.color)
    style_name = config.get_style(batch_config.style)
    font_name = config.get_font(batch_config.font) if batch_config.font else None
    print(f"批量生成配置:")
    print(f"  星座: {batch_config.zodiac}")
    print(f"  配色: {color_name.get('name') if color_name else batch_config.color}")
    print(f"  风格: {style_name.get('name') if style_name else batch_config.style}")
    print(f"  字体: {font_name.get('name') if font_name else '默认'}")
    print(f"  页数: {len(batch_config.pages)}")
    print()
    print("正在生成...")

    # 执行生成
    files = generate_batch(batch_config, config, renderer)

    print()
    print(f"✓ 完成！共生成 {len(files)} 张海报")


if __name__ == "__main__":
    main()
