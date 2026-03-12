# 飞书多维表格配置

本仓库不内置真实飞书凭证或固定表 ID。所有环境都应通过环境变量提供配置。

---

## 必需环境变量

```bash
LARK_APP_ID=
LARK_APP_SECRET=
LARK_BITABLE_APP_TOKEN=
LARK_BITABLE_TABLE_ID=
```

## 可选环境变量

```bash
LARK_VIRAL_NOTES_TABLE_ID=
LARK_TEMPLATE_TABLE_ID=
XHS_POSTER_OUTPUT_DIR=
XIAOHONGSHU_MCP_DIR=
```

---

## 表名约定

| 逻辑表名 | 环境变量 | 用途 |
|----------|----------|------|
| 素材库 / 星座海报生成 | `LARK_BITABLE_TABLE_ID` | 主内容表 |
| 低粉爆文抓取 | `LARK_VIRAL_NOTES_TABLE_ID` | 爆文抓取与分析 |
| 模板库 | `LARK_TEMPLATE_TABLE_ID` | 模板同步 |

如需新增表，请同步更新仓库根目录 `config.py` 中的 `BITABLES` 映射。

---

## MCP 调用模板

### 查询记录

```
mcp__lark-mcp__bitable_v1_appTableRecord_search
参数:
- path: {
    app_token: "<LARK_BITABLE_APP_TOKEN>",
    table_id: "<table_id>"
  }
- data: {
    filter: {
      conjunction: "and",
      conditions: [{
        field_name: "字段名",
        operator: "is",
        value: ["值"]
      }]
    }
  }
```

### 创建记录

```
mcp__lark-mcp__bitable_v1_appTableRecord_create
参数:
- path: {
    app_token: "<LARK_BITABLE_APP_TOKEN>",
    table_id: "<table_id>"
  }
- data: {
    fields: {
      "字段名": "值"
    }
  }
```

### 更新记录

```
mcp__lark-mcp__bitable_v1_appTableRecord_update
参数:
- path: {
    app_token: "<LARK_BITABLE_APP_TOKEN>",
    table_id: "<table_id>",
    record_id: "<record_id>"
  }
- data: {
    fields: {
      "字段名": "新值"
    }
  }
```
