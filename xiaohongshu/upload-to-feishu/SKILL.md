---
name: upload-to-feishu
description: |
  Upload generated poster images to Feishu Bitable attachment fields via Python script.
  Triggers: "upload images to feishu", "upload posters", "batch upload to feishu",
  "上传图片到飞书", "上传海报", "把图片传到飞书", "update feishu attachments".
  Required because lark-mcp does not support file uploads natively.
  Supports single/multiple image files or entire directories, with configurable
  target table and attachment field names.
---

# 飞书图片上传器

由于 lark-mcp 不支持文件上传，使用 Python 脚本将生成的海报图片上传到飞书多维表格的附件字段。运行前先配置 `.env`（可从 `.env.example` 复制）。

## 命令行用法

### 上传单个或多个图片

```bash
python upload-to-feishu/upload.py \
  --record-id "recXXX" \
  --images "path/to/img1.png" "path/to/img2.png"
```

### 上传目录中所有图片

```bash
python upload-to-feishu/upload.py \
  --record-id "recXXX" \
  --dir "path/to/images/"
```

目录模式自动识别 `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp` 格式，按文件名排序上传。

### 指定附件字段名或目标表格

```bash
python upload-to-feishu/upload.py \
  --record-id "recXXX" \
  --dir "path/to/images/" \
  --field "生成图片" \
  --table "星座海报生成"
```

## 参数说明

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `--record-id` | 是 | - | 飞书记录 ID |
| `--images` | 否* | - | 图片路径列表（空格分隔） |
| `--dir` | 否* | - | 图片目录路径 |
| `--field` | 否 | `生成图片` | 附件字段名 |
| `--table` | 否 | `星座海报生成` | 表格名称 |

`--images` 和 `--dir` 至少需要指定一个。

## 典型工作流

1. **创建飞书记录** — 调用 `mcp__lark-mcp__bitable_v1_appTableRecord_create`，获取 `record_id`
2. **生成海报图片** — 使用 zodiac-poster skill 生成 HTML 并截图，保存到 `output/{YYYY}/{MM}/{DD}/{标题}/`
3. **准备上传目录** — 将图片按顺序命名复制到 `output/.upload/{record_id}/`（如 `01-cover.png`, `02-page-01.png`）
4. **执行上传**：

```bash
python upload-to-feishu/upload.py \
  --record-id "recXXX" \
  --dir "output/.upload/recXXX/"
```

## 依赖配置

脚本依赖项目根目录的 `config.py`，凭证应通过环境变量或 `.env` 文件提供：

```python
# config.py
import os
LARK_APP_ID = os.environ["FEISHU_APP_ID"]
LARK_APP_SECRET = os.environ["FEISHU_APP_SECRET"]

def get_bitable(table_name):
    return {
        "app_token": "<LARK_BITABLE_APP_TOKEN>",
        "table_id": "<LARK_BITABLE_TABLE_ID>"
    }
```

## 错误处理

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| 获取 token 失败 | 凭证过期或错误 | 检查环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET |
| 上传文件失败 | 文件过大或格式不支持 | 检查文件大小和格式 |
| 更新记录失败 | record_id 无效 | 确认记录存在且有权限 |
| 目录不存在 | 路径错误 | 检查目录路径是否正确 |

## 相关 Skills

- `zodiac-poster` — 生成海报图片
- `generate-from-feishu` — 从飞书生成内容
