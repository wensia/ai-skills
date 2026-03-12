---
name: uploading-images-to-feishu
description: Uploads images to Feishu Bitable attachment fields using a Python script (since lark-mcp does not support file uploads). Use when the user needs to upload generated poster images to Feishu records, batch upload cover and content pages, or update attachment fields.
---

# 飞书图片上传器

由于 lark-mcp 不支持文件上传，使用此 Python 脚本将生成的海报图片上传到飞书多维表格的附件字段。运行前先配置 `.env`（可从 `.env.example` 复制）。

---

## 使用场景

1. 海报生成后，将图片上传到飞书记录
2. 批量上传一组图片（封面 + 内容页）
3. 更新已有记录的附件字段

---

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

目录模式会自动识别 `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp` 格式，并按文件名排序上传。

### 指定附件字段名

```bash
python upload-to-feishu/upload.py \
  --record-id "recXXX" \
  --dir "path/to/images/" \
  --field "生成图片"
```

### 指定目标表格

```bash
python upload-to-feishu/upload.py \
  --record-id "recXXX" \
  --dir "path/to/images/" \
  --table "星座海报生成"
```

---

## 参数说明

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `--record-id` | 是 | - | 飞书记录 ID |
| `--images` | 否* | - | 图片路径列表（空格分隔） |
| `--dir` | 否* | - | 图片目录路径 |
| `--field` | 否 | `生成图片` | 附件字段名 |
| `--table` | 否 | `星座海报生成` | 表格名称 |

*注：`--images` 和 `--dir` 至少需要指定一个。

---

## 典型工作流

### 1. 创建飞书记录

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_create
→ 获取 record_id
```

### 2. 生成海报图片

```
使用 zodiac-poster skill 生成 HTML 并截图
→ 保存到 output/{YYYY}/{MM}/{DD}/{标题}/
```

### 3. 准备上传目录

```bash
# 创建上传目录
mkdir -p output/.upload/{record_id}

# 复制图片（按顺序命名）
cp cover.png  output/.upload/{record_id}/01-cover.png
cp page-01.png output/.upload/{record_id}/02-page-01.png
...
```

### 4. 执行上传

```bash
python upload-to-feishu/upload.py \
  --record-id "recXXX" \
  --dir "output/.upload/recXXX/"
```

---

## 输出示例

```
正在获取飞书访问令牌...
正在上传图片 (1/6): 01-cover.png
  -> file_token: boxcnXXXXXX
正在上传图片 (2/6): 02-page-01.png
  -> file_token: boxcnYYYYYY
...
正在更新记录 recXXX...
上传完成！共上传 6 张图片

成功：已上传 6 张图片到飞书
```

---

## 依赖配置

脚本依赖项目根目录的 `config.py`：

```python
# config.py
LARK_APP_ID = "xxx"
LARK_APP_SECRET = "xxx"

def get_bitable(table_name):
    return {
        "app_token": "<LARK_BITABLE_APP_TOKEN>",
        "table_id": "<LARK_BITABLE_TABLE_ID>"  # 星座海报生成
    }
```

---

## 错误处理

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| 获取 token 失败 | 凭证过期或错误 | 检查 config.py 中的 APP_ID/SECRET |
| 上传文件失败 | 文件过大或格式不支持 | 检查文件大小和格式 |
| 更新记录失败 | record_id 无效 | 确认记录存在且有权限 |
| 目录不存在 | 路径错误 | 检查目录路径是否正确 |

---

## 相关 Skills

- `zodiac-poster` - 生成海报图片
- `generate-from-feishu` - 从飞书生成内容

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `upload-to-feishu/upload.py` | 上传脚本 |
| `config.py` | 飞书凭证配置 |
| `_shared/feishu-config.md` | 飞书表格配置 |
