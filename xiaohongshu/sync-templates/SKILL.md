---
name: sync-templates
description: |
  将本地模板同步到飞书「模板库」表。
  当用户需要：
  (1) 同步新创建的模板到飞书
  (2) 更新已有模板的信息
  (3) 查看本地模板列表
invocation: user
---

# 模板同步 Skill

将 `zodiac-poster` 项目的本地模板同步到飞书「模板库」多维表格。

---

## 飞书配置

```
app_token: Qt6Qbzzy6aWBgassGQhcUU5vngc
table_id: tbl4FKgtMDv3HCWP  # 模板库表
```

### 飞书凭证

```
APP_ID: cli_a9a7190fef38dbb5
APP_SECRET: CyANTKyK1HhZ569m9vasodAGqsjKwh1u
```

---

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

---

## 同步流程

### 步骤1: 扫描模板目录

```python
import os
import glob

TEMPLATES_DIR = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster/assets/templates"

# 查找所有包含 meta.json 的模板目录
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

如果 `examples/` 目录中有 SVG 但没有对应的 PNG，需要先转换：

```python
import sys
sys.path.insert(0, '/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster')

from utils.screenshot import svg_to_png, batch_svg_to_png

# 批量转换 SVG 为 2x PNG
import glob
svg_files = glob.glob('/path/to/examples/*.svg')
for svg_path in svg_files:
    png_path = svg_path.replace('.svg', '.png')
    svg_to_png(svg_path, png_path)  # 输出 2160x2880
```

**注意**：使用 Canvas API 方案确保：
- 精确 2x 分辨率 (2160x2880)
- 无白边问题
- 正确渲染中文字体

### 步骤3: 上传文件到飞书

使用 Python requests 上传文件：

```python
import requests

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
// 查询是否存在
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

---

## 使用示例

```
# 同步所有模板
/sync-templates

# 同步指定模板
/sync-templates personality-monologue

# 查看本地模板列表
/sync-templates --list
```

---

## 输出报告

```markdown
## 模板同步报告

**时间**: 2026-01-05 17:30:00

### 同步结果

| 模板 | 状态 | 说明 |
|------|------|------|
| personality-monologue | ✅ 更新 | 7张示例图 |

### 飞书表格

- **表名**: 模板库
- **table_id**: tbl4FKgtMDv3HCWP
- **记录数**: 1
```

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 缺少 meta.json | 跳过该模板，报告警告 |
| 文件上传失败 | 重试一次，失败则记录错误 |
| 记录更新失败 | 记录错误，继续下一个 |
