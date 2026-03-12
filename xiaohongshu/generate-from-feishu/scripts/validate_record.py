#!/usr/bin/env python3
"""
Validate Feishu Bitable records before poster generation.

Usage:
    python validate_record.py --record-id "recXXX"
    python validate_record.py --json '{"星座": "射手座", "标题": "test"}'

Exit codes:
    0: Valid
    1: Invalid (errors printed to stderr)
"""

import argparse
import json
import sys
from typing import Tuple, List, Dict, Any


# Required fields for generation
REQUIRED_FIELDS = ['星座', '标题', '模板']

# Valid zodiac signs
VALID_ZODIACS = [
    '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座',
    '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座'
]

# Valid template IDs
VALID_TEMPLATES = ['editorial-warm', 'editorial-dynamic', 'minimal-warm']

# Content validation rules
MIN_PARAGRAPHS_FOR_SET = 6
MAX_TITLE_LENGTH = 20
MIN_PARAGRAPH_LENGTH = 10
MAX_PARAGRAPH_LENGTH = 100


def validate_record(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a record for poster generation.

    Args:
        record: Dictionary with field names as keys

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in record or not record.get(field):
            errors.append(f"缺少必填字段: {field}")

    # Validate zodiac
    zodiac = record.get('星座', '')
    if zodiac and zodiac not in VALID_ZODIACS:
        errors.append(f"无效的星座: {zodiac}")

    # Validate template
    template = record.get('模板', '')
    if template and template not in VALID_TEMPLATES:
        errors.append(f"无效的模板ID: {template} (可选: {', '.join(VALID_TEMPLATES)})")

    # Validate title length
    title = record.get('标题', '')
    if title and len(title) > MAX_TITLE_LENGTH:
        errors.append(f"标题过长: {len(title)} 字 (最大 {MAX_TITLE_LENGTH})")

    # Validate content paragraphs for 套图
    usage = record.get('用途', '')
    content = record.get('正文内容', '')

    if usage == '套图' or (content and '\n' in content):
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

        if len(paragraphs) < MIN_PARAGRAPHS_FOR_SET:
            errors.append(
                f"正文段落不足: {len(paragraphs)} 段 "
                f"(套图至少需要 {MIN_PARAGRAPHS_FOR_SET} 段)"
            )

        # Check individual paragraph lengths
        for i, para in enumerate(paragraphs, 1):
            if len(para) < MIN_PARAGRAPH_LENGTH:
                errors.append(f"第 {i} 段过短: {len(para)} 字 (最少 {MIN_PARAGRAPH_LENGTH})")
            elif len(para) > MAX_PARAGRAPH_LENGTH:
                errors.append(f"第 {i} 段过长: {len(para)} 字 (最多 {MAX_PARAGRAPH_LENGTH})")

    return len(errors) == 0, errors


def validate_style_lock(html_content: str) -> Tuple[bool, List[str]]:
    """
    Validate HTML content has proper style lock.

    Args:
        html_content: HTML string

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check for style lock comment
    if '[STYLE LOCK:' not in html_content:
        errors.append("HTML 缺少 STYLE LOCK 注释")

    # Check for dark mode prevention
    if 'color-scheme: light only' not in html_content:
        errors.append("HTML 缺少深色模式防护 CSS")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description='Validate Feishu record for generation')
    parser.add_argument('--record-id', help='Feishu record ID to fetch and validate')
    parser.add_argument('--json', help='JSON string of record fields to validate')
    parser.add_argument('--html', help='HTML file path to validate style lock')
    args = parser.parse_args()

    all_errors = []

    if args.json:
        try:
            record = json.loads(args.json)
            is_valid, errors = validate_record(record)
            all_errors.extend(errors)
        except json.JSONDecodeError as e:
            all_errors.append(f"JSON 解析错误: {e}")

    if args.html:
        try:
            with open(args.html, 'r', encoding='utf-8') as f:
                html_content = f.read()
            is_valid, errors = validate_style_lock(html_content)
            all_errors.extend(errors)
        except FileNotFoundError:
            all_errors.append(f"HTML 文件不存在: {args.html}")

    if args.record_id:
        print(f"TODO: Fetch record {args.record_id} from Feishu and validate")
        # This would require Feishu API integration

    if all_errors:
        for error in all_errors:
            print(f"❌ {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print("✅ 验证通过")
        sys.exit(0)


if __name__ == '__main__':
    main()
