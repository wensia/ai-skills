#!/usr/bin/env python3
"""
SVG 截图脚本 - 批量将模板示例 SVG 转换为 PNG
使用 utils/screenshot.py 中的 Canvas API 方案
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.screenshot import svg_to_png


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    examples_dir = os.path.join(base_dir, "assets/templates/destined-bond/examples")

    files = ['01_cover', '02_page', '03_end']

    print("📸 开始截图 (3:4 比例, 2x 分辨率)...")

    for name in files:
        svg_path = os.path.join(examples_dir, f"{name}.svg")
        png_path = os.path.join(examples_dir, f"{name}.png")

        if os.path.exists(svg_path):
            svg_to_png(svg_path, png_path, scale=2)
            print(f"✅ {name}.png (2160x2880)")
        else:
            print(f"⚠️ 未找到: {svg_path}")

    print("✨ 完成!")


if __name__ == "__main__":
    main()
