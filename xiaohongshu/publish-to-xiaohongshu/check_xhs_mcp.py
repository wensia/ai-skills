#!/usr/bin/env python3
"""
小红书 MCP 检测脚本

检查 xiaohongshu-mcp 服务是否运行，并提供启动命令。

Usage:
    python check_xhs_mcp.py [--json] [--start]
"""

import os
import sys
import json
import argparse
import subprocess
import socket
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
XHS_MCP_DIR = PROJECT_ROOT / "xiaohongshu-mcp"
XHS_MCP_BIN = XHS_MCP_DIR / "xiaohongshu-mcp-darwin-arm64"
XHS_LOGIN_BIN = XHS_MCP_DIR / "xiaohongshu-login-darwin-arm64"
COOKIES_FILE = XHS_MCP_DIR / "cookies.json"

MCP_PORT = 18060
MCP_URL = f"http://localhost:{MCP_PORT}/mcp"


def check_port_open(port: int) -> bool:
    """检查端口是否开放"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex(('localhost', port))
        return result == 0
    except:
        return False
    finally:
        sock.close()


def check_mcp_running() -> dict:
    """检查 MCP 服务是否运行"""
    result = {
        "running": False,
        "port": MCP_PORT,
        "url": MCP_URL,
        "bin_exists": XHS_MCP_BIN.exists(),
        "login_bin_exists": XHS_LOGIN_BIN.exists()
    }

    if check_port_open(MCP_PORT):
        result["running"] = True

    return result


def check_cookies() -> dict:
    """检查登录状态（通过 cookies 文件）"""
    result = {
        "cookies_exists": COOKIES_FILE.exists(),
        "cookies_valid": False,
        "cookies_path": str(COOKIES_FILE)
    }

    if COOKIES_FILE.exists():
        try:
            with open(COOKIES_FILE, "r") as f:
                cookies = json.load(f)
                # 检查是否有有效的 cookie
                if cookies and len(cookies) > 0:
                    result["cookies_valid"] = True
                    result["cookies_count"] = len(cookies)
        except:
            pass

    return result


def generate_start_command() -> str:
    """生成启动命令"""
    return f"cd {XHS_MCP_DIR} && ./xiaohongshu-mcp-darwin-arm64 -headless=true &"


def generate_login_command() -> str:
    """生成登录命令"""
    return f"cd {XHS_MCP_DIR} && ./xiaohongshu-login-darwin-arm64"


def start_mcp_server() -> bool:
    """启动 MCP 服务"""
    if not XHS_MCP_BIN.exists():
        print(f"❌ MCP 二进制文件不存在: {XHS_MCP_BIN}")
        return False

    try:
        subprocess.Popen(
            [str(XHS_MCP_BIN), "-headless=true"],
            cwd=str(XHS_MCP_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ MCP 服务启动中...")
        return True
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False


def print_status(mcp_status: dict, cookies_status: dict):
    """打印检测状态"""
    print("\n" + "=" * 60)
    print("小红书 MCP 配置检测")
    print("=" * 60)

    print("\n🔌 MCP 服务状态:")
    if mcp_status["running"]:
        print(f"  ✅ 服务运行中")
        print(f"  📍 地址: {mcp_status['url']}")
    else:
        print("  ❌ 服务未运行")
        if mcp_status["bin_exists"]:
            print(f"  💡 启动命令: {generate_start_command()}")
        else:
            print(f"  ⚠️  二进制文件不存在: {XHS_MCP_BIN}")

    print("\n🍪 登录状态:")
    if cookies_status["cookies_valid"]:
        print(f"  ✅ Cookies 有效 ({cookies_status.get('cookies_count', 0)} 条)")
    elif cookies_status["cookies_exists"]:
        print("  ⚠️  Cookies 文件存在但可能无效")
        print(f"  💡 登录命令: {generate_login_command()}")
    else:
        print("  ❌ 未登录")
        print(f"  💡 登录命令: {generate_login_command()}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="检测小红书 MCP 状态")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--start", action="store_true", help="启动 MCP 服务")
    parser.add_argument("--check-only", action="store_true", help="仅检测，返回状态码")
    args = parser.parse_args()

    mcp_status = check_mcp_running()
    cookies_status = check_cookies()

    if args.json:
        print(json.dumps({
            "mcp": mcp_status,
            "cookies": cookies_status,
            "ready": mcp_status["running"] and cookies_status["cookies_valid"],
            "start_command": generate_start_command(),
            "login_command": generate_login_command()
        }, indent=2, ensure_ascii=False))
        return

    if args.check_only:
        if mcp_status["running"] and cookies_status["cookies_valid"]:
            print("ready")
            sys.exit(0)
        else:
            print("not_ready")
            sys.exit(1)

    if args.start:
        if mcp_status["running"]:
            print("✅ MCP 服务已在运行")
        else:
            start_mcp_server()
        return

    # 打印状态
    print_status(mcp_status, cookies_status)

    # 返回状态码
    if mcp_status["running"] and cookies_status["cookies_valid"]:
        print("\n✨ 配置完成，可以发布到小红书！")
        sys.exit(0)
    else:
        print("\n⚠️  请完成上述配置后再使用")
        sys.exit(1)


if __name__ == "__main__":
    main()
