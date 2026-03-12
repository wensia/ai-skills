"""
配置加载器

加载和管理星座海报的配色、用途、风格、字体配置
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List


class ConfigLoader:
    """配置加载器 - 管理所有海报配置"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化配置加载器

        Args:
            config_path: 配置文件路径，默认为 assets/colors.json
        """
        if config_path is None:
            self.config_path = Path(__file__).parent.parent.parent / "assets" / "colors.json"
        else:
            self.config_path = Path(config_path)

        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_color(self, color_id: str) -> Optional[Dict[str, Any]]:
        """获取配色方案"""
        return self.config.get("colors", {}).get(color_id)

    def get_color_id(self, keyword: str) -> Optional[str]:
        """根据关键词获取配色ID"""
        for color_id, color_data in self.config.get("colors", {}).items():
            if keyword in color_data.get("keywords", []) or keyword == color_data.get("name"):
                return color_id
        return None

    def get_usage(self, usage_id: str) -> Optional[Dict[str, Any]]:
        """获取用途/布局配置"""
        return self.config.get("usages", {}).get(usage_id)

    def get_style(self, style_id: str) -> Optional[Dict[str, Any]]:
        """获取风格配置"""
        return self.config.get("styles", {}).get(style_id)

    def get_style_id(self, keyword: str) -> Optional[str]:
        """根据关键词获取风格ID"""
        for style_id, style_data in self.config.get("styles", {}).items():
            if keyword in style_data.get("keywords", []) or keyword == style_data.get("name"):
                return style_id
        return None

    def get_font(self, font_id: str) -> Optional[Dict[str, Any]]:
        """获取字体配置"""
        return self.config.get("fonts", {}).get(font_id)

    def get_zodiac(self, zodiac_name: str) -> Optional[Dict[str, Any]]:
        """获取星座配置"""
        return self.config.get("zodiac", {}).get(zodiac_name)

    def list_colors(self) -> Dict[str, Any]:
        """列出所有配色方案"""
        return self.config.get("colors", {})

    def list_styles(self) -> Dict[str, Any]:
        """列出所有风格"""
        return self.config.get("styles", {})

    def list_fonts(self) -> Dict[str, Any]:
        """列出所有字体"""
        return self.config.get("fonts", {})

    def list_zodiacs(self) -> Dict[str, Any]:
        """列出所有星座"""
        return self.config.get("zodiac", {})
