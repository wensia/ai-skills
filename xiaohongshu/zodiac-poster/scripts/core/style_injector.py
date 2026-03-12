"""
风格注入器

根据风格配置生成 CSS 变量、装饰元素和背景样式
"""

from typing import Dict, Any, List


class StyleInjector:
    """风格注入器 - 生成风格相关的 CSS 和 HTML"""

    def __init__(self, style_data: Dict[str, Any]):
        """
        初始化风格注入器

        Args:
            style_data: 风格配置数据
        """
        self.style_data = style_data

    def get_css_variables(self) -> Dict[str, str]:
        """获取风格的 CSS 变量"""
        variables = {}

        # 装饰元素配置
        decorations = self.style_data.get("decorations", {})
        variables["--corner-show"] = "block" if decorations.get("corners", False) else "none"
        variables["--circle-show"] = "block" if decorations.get("background_circles", False) else "none"
        variables["--grain-show"] = "block" if decorations.get("grain_texture", False) else "none"

        return variables

    def get_all_css(self, palette: Dict[str, str]) -> str:
        """生成完整的风格 CSS"""
        css_parts = []

        decorations = self.style_data.get("decorations", {})

        # 角落装饰
        if decorations.get("corners", False):
            css_parts.append("""
        .corner {
            position: absolute;
            width: 80px; height: 80px;
            border: 2px solid var(--accent-soft);
            opacity: 0.4;
        }
        .corner-tl { top: 60px; left: 60px; border-right: none; border-bottom: none; }
        .corner-tr { top: 60px; right: 60px; border-left: none; border-bottom: none; }
        .corner-bl { bottom: 60px; left: 60px; border-right: none; border-top: none; }
        .corner-br { bottom: 60px; right: 60px; border-left: none; border-top: none; }
            """)

        # 背景圆圈
        if decorations.get("background_circles", False):
            css_parts.append("""
        .bg-circle {
            position: absolute;
            border-radius: 50%;
            background: var(--accent-soft);
            opacity: 0.08;
        }
        .circle-1 { width: 300px; height: 300px; top: -100px; right: -50px; }
        .circle-2 { width: 200px; height: 200px; bottom: 200px; left: -80px; }
            """)

        # 颗粒纹理
        if decorations.get("grain_texture", False):
            css_parts.append("""
        .grain-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
            opacity: 0.03;
            pointer-events: none;
        }
            """)

        # 暗角效果 (vintage)
        if decorations.get("vignette", False):
            css_parts.append("""
        .vignette {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.15) 100%);
            pointer-events: none;
        }
            """)

        # 模糊圆圈 (ins)
        if decorations.get("blur_circles", False):
            css_parts.append("""
        .blur-circle {
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.3;
        }
        .blur-1 { width: 400px; height: 400px; top: -150px; right: -100px; background: var(--accent-soft); }
        .blur-2 { width: 300px; height: 300px; bottom: 100px; left: -100px; background: var(--bg-secondary); }
            """)

        # 装饰边框 (vintage)
        if decorations.get("decorative_border", False):
            css_parts.append("""
        .decorative-border {
            position: absolute;
            top: 40px; left: 40px; right: 40px; bottom: 40px;
            border: 1px solid var(--accent-soft);
            opacity: 0.3;
            pointer-events: none;
        }
            """)

        return "\n".join(css_parts)

    def get_background_css(self, palette: Dict[str, str]) -> str:
        """生成背景样式 CSS"""
        bg_type = self.style_data.get("background", {}).get("type", "solid")

        if bg_type == "gradient":
            gradient = self.style_data.get("background", {}).get("gradient", {})
            direction = gradient.get("direction", "180deg")
            stops = gradient.get("stops", ["var(--bg-primary)", "var(--bg-secondary)"])
            return f"background: linear-gradient({direction}, {', '.join(stops)});"
        else:
            return "background: var(--bg-primary);"

    def get_decoration_html(self) -> str:
        """生成装饰元素的 HTML"""
        html_parts = []
        decorations = self.style_data.get("decorations", {})

        # 角落装饰
        if decorations.get("corners", False):
            html_parts.append("""
        <div class="corner corner-tl"></div>
        <div class="corner corner-tr"></div>
        <div class="corner corner-bl"></div>
        <div class="corner corner-br"></div>
            """)

        # 背景圆圈
        if decorations.get("background_circles", False):
            html_parts.append("""
        <div class="bg-circle circle-1"></div>
        <div class="bg-circle circle-2"></div>
            """)

        # 颗粒纹理
        if decorations.get("grain_texture", False):
            html_parts.append('<div class="grain-overlay"></div>')

        # 暗角效果
        if decorations.get("vignette", False):
            html_parts.append('<div class="vignette"></div>')

        # 模糊圆圈
        if decorations.get("blur_circles", False):
            html_parts.append("""
        <div class="blur-circle blur-1"></div>
        <div class="blur-circle blur-2"></div>
            """)

        # 装饰边框
        if decorations.get("decorative_border", False):
            html_parts.append('<div class="decorative-border"></div>')

        return "\n".join(html_parts)

    def get_divider_html(self) -> str:
        """生成分隔线的 HTML"""
        divider_type = self.style_data.get("divider", {}).get("type", "dot")

        if divider_type == "dot":
            return """
        <div class="divider" style="display: flex; justify-content: center; align-items: center; gap: 15px;">
            <div style="width: 40px; height: 1px; background: var(--accent-soft);"></div>
            <div style="width: 6px; height: 6px; border-radius: 50%; background: var(--accent); opacity: 0.6;"></div>
            <div style="width: 40px; height: 1px; background: var(--accent-soft);"></div>
        </div>
            """
        elif divider_type == "line":
            return """
        <div class="divider" style="display: flex; justify-content: center;">
            <div style="width: 100px; height: 1px; background: var(--accent-soft);"></div>
        </div>
            """
        elif divider_type == "double_line":
            return """
        <div class="divider" style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
            <div style="width: 80px; height: 1px; background: var(--accent-soft);"></div>
            <div style="width: 60px; height: 1px; background: var(--accent-soft);"></div>
        </div>
            """
        elif divider_type == "doodle":
            return """
        <div class="divider" style="display: flex; justify-content: center;">
            <svg width="120" height="20" viewBox="0 0 120 20">
                <path d="M10 10 Q30 5, 60 10 T110 10" fill="none" stroke="var(--accent-soft)" stroke-width="2" stroke-linecap="round"/>
            </svg>
        </div>
            """
        else:
            return '<div class="divider"></div>'
