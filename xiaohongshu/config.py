import os
from pathlib import Path


def _require(name: str) -> str:
    value = os.environ.get(name, '').strip()
    if not value:
        raise RuntimeError(f'Missing required environment variable: {name}')
    return value


LARK_APP_ID = _require('LARK_APP_ID')
LARK_APP_SECRET = _require('LARK_APP_SECRET')
LARK_BITABLE_APP_TOKEN = _require('LARK_BITABLE_APP_TOKEN')
LARK_BITABLE_TABLE_ID = _require('LARK_BITABLE_TABLE_ID')
LARK_VIRAL_NOTES_TABLE_ID = os.environ.get('LARK_VIRAL_NOTES_TABLE_ID', '').strip()
LARK_TEMPLATE_TABLE_ID = os.environ.get('LARK_TEMPLATE_TABLE_ID', '').strip()
XHS_POSTER_OUTPUT_DIR = os.environ.get(
    'XHS_POSTER_OUTPUT_DIR',
    str(Path(__file__).resolve().parent / 'output')
)
XIAOHONGSHU_MCP_DIR = os.environ.get(
    'XIAOHONGSHU_MCP_DIR',
    str(Path(__file__).resolve().parent / 'xiaohongshu-mcp')
)


BITABLES = {
    '星座海报生成': {
        'app_token': LARK_BITABLE_APP_TOKEN,
        'table_id': LARK_BITABLE_TABLE_ID,
    },
    '素材库': {
        'app_token': LARK_BITABLE_APP_TOKEN,
        'table_id': LARK_BITABLE_TABLE_ID,
    },
    '低粉爆文抓取': {
        'app_token': LARK_BITABLE_APP_TOKEN,
        'table_id': LARK_VIRAL_NOTES_TABLE_ID,
    },
    '模板库': {
        'app_token': LARK_BITABLE_APP_TOKEN,
        'table_id': LARK_TEMPLATE_TABLE_ID,
    },
}


def get_bitable(table_name: str) -> dict:
    bitable = BITABLES.get(table_name)
    if not bitable:
        raise KeyError(f'Unknown bitable: {table_name}')
    if not bitable.get('app_token') or not bitable.get('table_id'):
        raise RuntimeError(f'Bitable config incomplete for: {table_name}')
    return bitable
