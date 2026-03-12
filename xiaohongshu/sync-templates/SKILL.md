---
name: sync-templates
description: |
  Sync local poster templates to Feishu Bitable "模板库" table.
  Triggers: "sync templates", "upload templates to feishu", "update template library",
  "同步模板", "更新模板库", "模板同步到飞书", "list local templates".
  Scans local template directories for meta.json, uploads example images,
  and creates/updates Feishu Bitable records with template metadata and prompts.
invocation: user
---

# 模板同步 Skill

将 `zodiac-poster` 项目的本地模板同步到飞书「模板库」多维表格。

## 飞书配置

```
app_token: Qt6Qbzzy6aWBgassGQhcUU5vngc
table_id: tbl4FKgtMDv3HCWP  # 模板库表
```

### 飞书凭证

从环境变量读取，不要硬编码：

```python
import os
APP_ID = os.environ["FEISHU_APP_ID"]
APP_SECRET = os.environ["FEISHU_APP_SECRET"]
```

确保运行前已设置 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 环境变量。

## 模板目录

```
/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster/assets/templates/
```

### 模板结构

每个模板目录应包含：

```
{template-id}/
├── meta.json          # 必须 - 模板元信息
├── PROMPT.md          # 必须 - 精简版提示词
├── cover.svg          # 封面 SVG 模板
├── page.svg           # 内页 SVG 模板
├── summary.svg        # 结尾页 SVG 模板
└── examples/          # 示例图目录
    ├── 01_cover.png
    ├── 02_page.png
    └── ...
```

### meta.json 格式

```json
{
  "id": "personality-monologue",
  "name": "性格独白风",
  "description": "书信感、PART标签、左边框引用",
  "accent_color": "#C4653A",
  "suitable_for": ["性格独白", "情感解读"]
}
```

## 同步流程

### 步骤1: 扫描模板目录

```python
import os, glob

TEMPLATES_DIR = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster/assets/templates"

template_dirs = [
    d for d in glob.glob(os.path.join(TEMPLATES_DIR, "*"))
    if os.path.isdir(d) and os.path.exists(os.path.join(d, "meta.json"))
]
```

### 步骤2: 读取模板信息

对每个模板目录：
1. 读取 `meta.json` 获取元信息
2. 读取 `PROMPT.md` 获取提示词内容
3. 收集 `examples/*.png` 示例图列表

### 步骤2.5: SVG 转 PNG (如需要)

如果 `examples/` 目录中有 SVG 但没有对应 PNG，先转换：

```python
import sys
sys.path.insert(0, '/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster')
from utils.screenshot import svg_to_png

import glob
for svg_path in glob.glob('/path/to/examples/*.svg'):
    png_path = svg_path.replace('.svg', '.png')
    svg_to_png(svg_path, png_path)  # 输出 2160x2880
```

使用 Canvas API 方案确保精确 2x 分辨率 (2160x2880)、无白边、正确渲染中文字体。

### 步骤3: 上传文件到飞书

使用 Python requests 上传（凭证从环境变量读取）：

```python
import os, requests

def upload_file(token, file_path):
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        files = {"file": (file_name, f)}
        data = {
            "file_name": file_name,
            "parent_type": "bitable_file",
            "parent_node": "Qt6Qbzzy6aWBgassGQhcUU5vngc",
            "size": str(file_size)
        }
        resp = requests.post(url, headers={"Authorization": f"Bearer {token}"}, files=files, data=data)

    return resp.json()["data"]["file_token"]
```

### 步骤4: 创建/更新飞书记录

使用飞书 MCP 操作记录：

```javascript
// 查询是否已存在
mcp__lark-mcp__bitable_v1_appTableRecord_search({
  path: { app_token: "Qt6Qbzzy6aWBgassGQhcUU5vngc", table_id: "tbl4FKgtMDv3HCWP" },
  data: {
    filter: {
      conjunction: "and",
      conditions: [{ field_name: "模板ID", operator: "is", value: [template_id] }]
    }
  }
})

// 创建新记录
mcp__lark-mcp__bitable_v1_appTableRecord_create({
  path: { app_token: "...", table_id: "..." },
  data: {
    fields: {
      "模板ID": "personality-monologue",
      "模板名称": "性格独白风",
      "描述": "...",
      "强调色": "#C4653A",
      "适用场景": "性格独白, 情感解读",
      "示例图": [{ file_token: "..." }, ...],
      "提示词": "..."
    }
  }
})

// 更新现有记录
mcp__lark-mcp__bitable_v1_appTableRecord_update({
  path: { app_token: "...", table_id: "...", record_id: "..." },
  data: { fields: { ... } }
})
```

## 使用示例

```
/sync-templates                          # 同步所有模板
/sync-templates personality-monologue    # 同步指定模板
/sync-templates --list                   # 查看本地模板列表
```

## 输出报告

完成后输出同步摘要，包括每个模板的状态（新建/更新）、示例图数量，以及飞书表格总记录数。

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 缺少 meta.json | 跳过该模板，报告警告 |
| 文件上传失败 | 重试一次，失败则记录错误 |
| 记录更新失败 | 记录错误，继续下一个 |
