#!/usr/bin/env python3
"""
独立海报截图工具 - 替代 MCP Playwright
将 HTML 文件转换为 PNG 截图，避免与 MCP 浏览器实例冲突

用法:
  单文件模式: python poster_screenshot.py input.html output.png
  批量模式:   python poster_screenshot.py --batch input_dir/ output_dir/
  1x 模式:    python poster_screenshot.py --scale 1 input.html output.png

特性:
  - 固定 viewport 1080x1440
  - 默认 2x 导出（实际像素 2160x2880）
  - 等待字体加载
  - 截取 .poster 元素
  - 批量模式复用浏览器实例
  - headless 模式运行
"""

import os
import sys
import argparse
import json
import time
from pathlib import Path
from typing import List

# 配置常量
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1440
DEFAULT_SCALE = 2  # 2x 导出，实际像素 2160x2880
FONT_WAIT_MS = 2000
DEFAULT_SELECTOR = ".poster"


class ScreenshotResult:
    """截图结果"""
    def __init__(self, success: bool, input_path: str, output_path: str = "",
                 error: str = "", duration_ms: int = 0):
        self.success = success
        self.input_path = input_path
        self.output_path = output_path
        self.error = error
        self.duration_ms = duration_ms

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "input": self.input_path,
            "output": self.output_path,
            "error": self.error,
            "duration_ms": self.duration_ms
        }


class PosterScreenshot:
    """海报截图工具类"""

    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT,
                 headless: bool = True, selector: str = DEFAULT_SELECTOR,
                 font_wait_ms: int = FONT_WAIT_MS, scale: int = DEFAULT_SCALE):
        self.width = width
        self.height = height
        self.headless = headless
        self.selector = selector
        self.font_wait_ms = font_wait_ms
        self.scale = scale  # device_scale_factor, 2 = 2x 导出
        self.browser = None
        self.playwright = None

    def __enter__(self):
        """上下文管理器入口 - 启动浏览器"""
        try:
            from playwright.sync_api import sync_playwright
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            return self
        except ImportError:
            print("错误: 请先安装 playwright", file=sys.stderr)
            print("运行: pip install playwright && playwright install chromium", file=sys.stderr)
            sys.exit(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口 - 关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def capture(self, html_path: str, output_path: str) -> ScreenshotResult:
        """
        截取单个 HTML 文件

        Args:
            html_path: HTML 文件路径
            output_path: 输出 PNG 路径

        Returns:
            ScreenshotResult: 截图结果
        """
        start_time = time.time()

        # 验证输入
        html_path = os.path.abspath(html_path)
        output_path = os.path.abspath(output_path)

        if not os.path.exists(html_path):
            return ScreenshotResult(
                success=False,
                input_path=html_path,
                error=f"文件不存在: {html_path}"
            )

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            # 创建页面，设置 device_scale_factor 实现高分辨率导出
            page = self.browser.new_page(
                viewport={"width": self.width, "height": self.height},
                device_scale_factor=self.scale
            )

            # 加载 HTML
            page.goto(f"file://{html_path}")

            # 等待网络空闲（字体加载）
            page.wait_for_load_state("networkidle")

            # 使用 JavaScript 显式等待字体加载完成
            page.evaluate("""
                () => new Promise((resolve) => {
                    if (document.fonts && document.fonts.ready) {
                        document.fonts.ready.then(() => {
                            // 字体加载完成后再等待一小段时间确保渲染
                            setTimeout(resolve, 500);
                        });
                    } else {
                        // 回退：直接等待
                        setTimeout(resolve, 2000);
                    }
                })
            """)

            # 额外等待确保字体渲染完成
            page.wait_for_timeout(self.font_wait_ms)

            # 查找目标元素
            element = page.query_selector(self.selector)

            if element:
                # 截取指定元素
                element.screenshot(path=output_path)
            else:
                # 回退：截取整个页面
                page.screenshot(path=output_path)

            page.close()

            duration_ms = int((time.time() - start_time) * 1000)

            return ScreenshotResult(
                success=True,
                input_path=html_path,
                output_path=output_path,
                duration_ms=duration_ms
            )

        except Exception as e:
            return ScreenshotResult(
                success=False,
                input_path=html_path,
                error=str(e)
            )

    def capture_batch(self, input_dir: str, output_dir: str,
                      pattern: str = "*.html") -> List[ScreenshotResult]:
        """
        批量截取目录中的 HTML 文件

        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            pattern: 文件匹配模式

        Returns:
            List[ScreenshotResult]: 截图结果列表
        """
        import glob

        input_dir = os.path.abspath(input_dir)
        output_dir = os.path.abspath(output_dir)

        if not os.path.isdir(input_dir):
            return [ScreenshotResult(
                success=False,
                input_path=input_dir,
                error=f"目录不存在: {input_dir}"
            )]

        os.makedirs(output_dir, exist_ok=True)

        # 查找所有 HTML 文件
        html_files = sorted(glob.glob(os.path.join(input_dir, pattern)))

        if not html_files:
            return [ScreenshotResult(
                success=False,
                input_path=input_dir,
                error=f"未找到匹配文件: {pattern}"
            )]

        results = []
        for html_path in html_files:
            # 生成输出路径
            basename = os.path.splitext(os.path.basename(html_path))[0]
            output_path = os.path.join(output_dir, f"{basename}.png")

            result = self.capture(html_path, output_path)
            results.append(result)

            # 打印进度
            status = "OK" if result.success else "FAIL"
            print(f"[{status}] {os.path.basename(html_path)} -> {os.path.basename(output_path)}")

        return results


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="海报截图工具 - HTML to PNG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 单文件模式
  %(prog)s cover.html cover.png

  # 批量模式
  %(prog)s --batch ./html_dir/ ./png_dir/

  # 自定义选项
  %(prog)s --width 1200 --height 1600 cover.html cover.png

  # 调试模式（显示浏览器）
  %(prog)s --no-headless cover.html cover.png

  # 输出 JSON 格式结果
  %(prog)s --json cover.html cover.png
        """
    )

    # 位置参数
    parser.add_argument("input", help="输入 HTML 文件或目录")
    parser.add_argument("output", help="输出 PNG 文件或目录")

    # 模式选项
    parser.add_argument("--batch", "-b", action="store_true",
                        help="批量模式：处理目录中的所有 HTML 文件")

    # 尺寸选项
    parser.add_argument("--width", "-W", type=int, default=DEFAULT_WIDTH,
                        help=f"视口宽度（默认: {DEFAULT_WIDTH}）")
    parser.add_argument("--height", "-H", type=int, default=DEFAULT_HEIGHT,
                        help=f"视口高度（默认: {DEFAULT_HEIGHT}）")
    parser.add_argument("--scale", "-S", type=int, default=DEFAULT_SCALE,
                        help=f"导出倍率，2=2x高清（默认: {DEFAULT_SCALE}，实际像素={DEFAULT_WIDTH*DEFAULT_SCALE}x{DEFAULT_HEIGHT*DEFAULT_SCALE}）")

    # 行为选项
    parser.add_argument("--selector", "-s", default=DEFAULT_SELECTOR,
                        help=f"截图元素选择器（默认: {DEFAULT_SELECTOR}）")
    parser.add_argument("--wait", "-w", type=int, default=FONT_WAIT_MS,
                        help=f"字体加载等待时间毫秒（默认: {FONT_WAIT_MS}）")
    parser.add_argument("--no-headless", action="store_true",
                        help="禁用 headless 模式（用于调试）")

    # 输出选项
    parser.add_argument("--json", "-j", action="store_true",
                        help="以 JSON 格式输出结果")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="静默模式，只输出错误")

    args = parser.parse_args()

    # 创建截图工具
    with PosterScreenshot(
        width=args.width,
        height=args.height,
        headless=not args.no_headless,
        selector=args.selector,
        font_wait_ms=args.wait,
        scale=args.scale
    ) as tool:

        if args.batch:
            # 批量模式
            results = tool.capture_batch(args.input, args.output)
        else:
            # 单文件模式
            result = tool.capture(args.input, args.output)
            results = [result]

        # 统计结果
        success_count = sum(1 for r in results if r.success)
        fail_count = len(results) - success_count

        # 输出结果
        if args.json:
            output = {
                "success": fail_count == 0,
                "total": len(results),
                "succeeded": success_count,
                "failed": fail_count,
                "results": [r.to_dict() for r in results]
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        elif not args.quiet:
            print(f"\n完成: {success_count}/{len(results)} 成功")

            # 显示失败项
            for r in results:
                if not r.success:
                    print(f"  失败: {r.input_path}")
                    print(f"    原因: {r.error}")

        # 返回退出码
        sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
