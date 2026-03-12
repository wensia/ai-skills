"""
模板渲染器

将配色、用途、风格三维配置合并，渲染最终的 HTML 模板。
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from .config_loader import ConfigLoader
from .style_injector import StyleInjector


class TemplateRenderer:
    """模板渲染器 - 生成最终的海报 HTML"""

    def __init__(self, config: ConfigLoader, template_path: Optional[Path] = None):
        """
        初始化模板渲染器

        Args:
            config: ConfigLoader 实例
            template_path: 模板文件路径，默认为 assets/unified-template.html
        """
        self.config = config

        if template_path is None:
            self.template_path = Path(__file__).parent.parent.parent / "assets" / "unified-template.html"
        else:
            self.template_path = Path(template_path)

        self.template = self._load_template()

    def _load_template(self) -> str:
        """加载模板文件"""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def render(
        self,
        color_id: str,
        usage_id: str,
        style_id: str,
        zodiac_name: str,
        content: Dict[str, Any],
        font_id: Optional[str] = None
    ) -> str:
        """
        渲染海报 HTML

        Args:
            color_id: 配色ID
            usage_id: 用途ID
            style_id: 风格ID
            zodiac_name: 星座中文名
            content: 内容字典，包含 headline, sub_line, subtitle, body, emphasis, footer
            font_id: 字体ID（可选），如 'wenkai' 或 'songti'

        Returns:
            渲染后的完整 HTML 字符串
        """
        # 获取配置
        color_data = self.config.get_color(color_id)
        usage_data = self.config.get_usage(usage_id)
        style_data = self.config.get_style(style_id)
        zodiac_data = self.config.get_zodiac(zodiac_name)

        if not all([color_data, usage_data, style_data, zodiac_data]):
            raise ValueError(f"无效的配置: color={color_id}, usage={usage_id}, style={style_id}, zodiac={zodiac_name}")

        palette = color_data.get("palette", {})
        settings = usage_data.get("settings", {})
        sections = settings.get("sections", {})
        dimensions = usage_data.get("dimensions", {"width": 1080, "height": 1440})

        # 创建风格注入器
        style_injector = StyleInjector(style_data)

        # 构建替换字典
        replacements = {}

        # 配色变量
        replacements["{{BG_PRIMARY}}"] = palette.get("bg_primary", "#FAF6F1")
        replacements["{{BG_SECONDARY}}"] = palette.get("bg_secondary", "#F5EDE4")
        replacements["{{ACCENT}}"] = palette.get("accent", "#DA7756")
        replacements["{{ACCENT_SOFT}}"] = palette.get("accent_soft", "#E8B49A")
        replacements["{{TEXT_DARK}}"] = palette.get("text_dark", "#2D2926")
        replacements["{{TEXT_MUTED}}"] = palette.get("text_muted", "#6B5B4F")
        replacements["{{TEXT_LIGHT}}"] = palette.get("text_light", "#8B7B6B")

        # 布局尺寸
        replacements["{{POSTER_WIDTH}}"] = f"{dimensions.get('width', 1080)}px"
        replacements["{{POSTER_HEIGHT}}"] = f"{dimensions.get('height', 1440)}px"

        # 布局设置 - 字体优先级：font_id参数 > 风格覆盖 > 用途默认
        if font_id:
            font_data = self.config.get_font(font_id)
            font_family = font_data.get("family", "'LXGW WenKai', serif") if font_data else "'LXGW WenKai', serif"
        else:
            font_override = style_data.get("typography", {}).get("font_override")
            font_family = font_override or settings.get("font_family", "'LXGW WenKai', serif")
        replacements["{{FONT_FAMILY}}"] = font_family
        replacements["{{ICON_SIZE}}"] = settings.get("icon_size", "120px")
        replacements["{{ZODIAC_NAME_SIZE}}"] = settings.get("zodiac_name_size", "64px")
        replacements["{{ZODIAC_NAME_MARGIN}}"] = settings.get("zodiac_name_margin", "50px")
        replacements["{{HEADLINE_SIZE}}"] = settings.get("headline_size", "72px")
        replacements["{{SUB_LINE_SIZE}}"] = settings.get("sub_line_size", "42px")
        replacements["{{DIVIDER_MARGIN}}"] = settings.get("divider_margin", "0 0 70px 0")

        # 区块显示控制
        replacements["{{SHOW_SUBTITLE}}"] = "block" if sections.get("subtitle", False) else "none"
        replacements["{{SHOW_SUB_LINE}}"] = "block" if sections.get("sub_line", True) else "none"
        replacements["{{SHOW_BODY_TEXT}}"] = "block" if sections.get("body_text", False) else "none"
        replacements["{{SHOW_EMPHASIS_BOX}}"] = "block" if sections.get("emphasis_box", False) else "none"
        replacements["{{SHOW_SIDE_LINE}}"] = "block" if sections.get("side_line", False) else "none"

        # 风格相关变量
        css_vars = style_injector.get_css_variables()
        for var_name, var_value in css_vars.items():
            replacements[f"{{{{{var_name.replace('--', '').upper().replace('-', '_')}}}}}"] = var_value

        # 星座信息
        replacements["{{ZODIAC_NAME}}"] = zodiac_name
        replacements["{{ZODIAC_ID}}"] = zodiac_data.get("id", "sagittarius")
        replacements["{{ZODIAC_EN}}"] = zodiac_data.get("en", "SAGITTARIUS")

        # 内容
        replacements["{{HEADLINE}}"] = content.get("headline", "")
        replacements["{{SUB_LINE}}"] = content.get("sub_line", "")
        replacements["{{SUBTITLE}}"] = content.get("subtitle", "")
        replacements["{{BODY_TEXT}}"] = self._format_body_text(content.get("body", []))
        replacements["{{EMPHASIS_TEXT}}"] = content.get("emphasis", "")
        replacements["{{FOOTER_TEXT}}"] = content.get("footer", "懂的人自然懂 ✦")

        # 风格 CSS
        replacements["{{STYLE_CSS}}"] = style_injector.get_all_css(palette)

        # 背景样式
        replacements["{{BG_STYLE}}"] = style_injector.get_background_css(palette)

        # 装饰元素 HTML
        replacements["{{DECORATIONS_HTML}}"] = style_injector.get_decoration_html()

        # 分隔线 HTML
        replacements["{{DIVIDER_HTML}}"] = style_injector.get_divider_html()

        # 字体链接
        replacements["{{FONT_LINKS}}"] = self._generate_font_links()

        # 执行替换
        html = self.template
        for placeholder, value in replacements.items():
            html = html.replace(placeholder, str(value))

        return html

    def _format_body_text(self, body_lines: List[str]) -> str:
        """格式化正文内容"""
        if not body_lines:
            return ""
        if isinstance(body_lines, str):
            body_lines = [body_lines]
        return "\n".join(f"<p>{line}</p>" for line in body_lines)

    def _generate_font_links(self) -> str:
        """生成字体 CSS 链接"""
        links = []
        for font_id, font_data in self.config.list_fonts().items():
            for css_file in font_data.get("css_files", []):
                links.append(f'<link rel="stylesheet" href="{css_file}">')
        return "\n    ".join(links)

    def render_cover(
        self,
        color_id: str,
        style_id: str,
        zodiac_name: str,
        headline: str,
        sub_line: str = "",
        footer: str = "懂的人自然懂 ✦"
    ) -> str:
        """
        快捷方法：渲染封面

        Args:
            color_id: 配色ID
            style_id: 风格ID
            zodiac_name: 星座中文名
            headline: 主标题
            sub_line: 副行文字
            footer: 底部文字

        Returns:
            渲染后的 HTML
        """
        content = {
            "headline": headline,
            "sub_line": sub_line,
            "footer": footer
        }
        return self.render(color_id, "cover", style_id, zodiac_name, content)

    def render_long(
        self,
        color_id: str,
        style_id: str,
        zodiac_name: str,
        headline: str,
        subtitle: str = "",
        body: List[str] = None,
        emphasis: str = "",
        footer: str = "懂的人自然懂 ✦"
    ) -> str:
        """
        快捷方法：渲染长文案

        Args:
            color_id: 配色ID
            style_id: 风格ID
            zodiac_name: 星座中文名
            headline: 主标题
            subtitle: 副标题
            body: 正文段落列表
            emphasis: 强调框内容
            footer: 底部文字

        Returns:
            渲染后的 HTML
        """
        content = {
            "headline": headline,
            "subtitle": subtitle,
            "body": body or [],
            "emphasis": emphasis,
            "footer": footer
        }
        return self.render(color_id, "long", style_id, zodiac_name, content)
