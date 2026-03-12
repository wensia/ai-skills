---
name: feishu-bitable
description: |
  飞书多维表格（Bitable）完整 CRUD 操作，覆盖全部 27 种字段类型。当用户需要读取、创建、更新、删除多维表格记录，管理表结构（字段/视图/数据表），设置筛选条件，或进行任何飞书表格类数据操作时使用此 skill。触发场景包括用户说"更新表格"、"查一下表格"、"导入数据"、"新建多维表格"、"bitable"、"数据表"、"记录"、"字段"，或任何涉及飞书结构化数据管理的需求。
---

# 飞书多维表格（Bitable）

## 执行前必读

写记录前必须先调用 `feishu_bitable_app_table_field.list` 获取字段 type/ui_type，因为不同字段类型对值的数据结构要求完全不同（这是 Bitable 最大的坑）。

关键约束：
- **人员字段**：值必须是 `[{id:"ou_xxx"}]`（数组对象），只能传 id，不能传 name/email
- **日期字段**：毫秒时间戳（如 `1674206443000`），不是秒，不是字符串
- **单选字段**：字符串（如 `"选项1"`），不是数组
- **多选字段**：字符串数组（如 `["选项1", "选项2"]`）
- **超链接字段**：对象 `{link: "...", text: "..."}`，不能直接传字符串 URL
- **附件字段**：必须先上传到当前多维表格，使用返回的 file_token
- **批量上限**：单次 500 条，超过需分批（批量操作是原子性的）
- **并发限制**：同一数据表不支持并发写，需串行调用 + 延迟 0.5-1 秒
- **默认表空行**：`app.create` 自带的默认表有空记录，插入前建议先 list + batch_delete 删除空行

---

## 快速索引：意图 -> 工具 -> 必填参数

| 用户意图 | 工具 | action | 必填参数 | 常用可选 |
|---------|------|--------|---------|---------|
| 查字段 | feishu_bitable_app_table_field | list | app_token, table_id | - |
| 查记录 | feishu_bitable_app_table_record | list | app_token, table_id | filter, sort, field_names |
| 新增一行 | feishu_bitable_app_table_record | create | app_token, table_id, fields | - |
| 批量导入 | feishu_bitable_app_table_record | batch_create | app_token, table_id, records (max 500) | - |
| 更新一行 | feishu_bitable_app_table_record | update | app_token, table_id, record_id, fields | - |
| 批量更新 | feishu_bitable_app_table_record | batch_update | app_token, table_id, records (max 500) | - |
| 创建多维表格 | feishu_bitable_app | create | name | folder_token |
| 创建数据表 | feishu_bitable_app_table | create | app_token, name | fields |
| 创建字段 | feishu_bitable_app_table_field | create | app_token, table_id, field_name, type | property |
| 创建视图 | feishu_bitable_app_table_view | create | app_token, table_id, view_name, view_type | - |

---

## 详细参考文档

遇到字段配置、记录值格式问题或需要完整示例时查阅：

- [字段 Property 配置详解](references/field-properties.md) -- 每种字段类型创建/更新时需要的 `property` 参数结构
- [记录值数据结构详解](references/record-values.md) -- 每种字段类型在记录中对应的 `fields` 值格式
- [使用场景完整示例](references/examples.md) -- 8 个完整场景示例

何时查阅：
- 创建/更新字段收到 `125408X` 错误码 -> 查 field-properties.md
- 写入记录收到 `125406X` 错误码 -> 查 record-values.md
- 需要完整操作流程和参数示例 -> 查 examples.md

---

## 核心使用场景

### 场景 1: 查字段类型（必做第一步）

```json
{
  "action": "list",
  "app_token": "S404b...",
  "table_id": "tbl..."
}
```

返回每个字段的 `field_id`、`field_name`、`type`、`ui_type`、`property`。

### 场景 2: 批量导入数据

```json
{
  "action": "batch_create",
  "app_token": "S404b...",
  "table_id": "tbl...",
  "records": [
    {
      "fields": {
        "客户名称": "字节跳动",
        "负责人": [{"id": "ou_xxx"}],
        "签约日期": 1674206443000,
        "状态": "进行中"
      }
    }
  ]
}
```

### 场景 3: 筛选查询

```json
{
  "action": "list",
  "app_token": "S404b...",
  "table_id": "tbl...",
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "状态",
        "operator": "is",
        "value": ["进行中"]
      },
      {
        "field_name": "截止日期",
        "operator": "isLess",
        "value": ["ExactDate", "1740441600000"]
      }
    ]
  },
  "sort": [{"field_name": "截止日期", "desc": false}]
}
```

filter 说明：
- isEmpty/isNotEmpty 必须传 `value: []`（API 要求必须传空数组，即使逻辑上不需要值）
- 日期筛选可用 `["Today"]`、`["ExactDate", "时间戳"]` 等

---

## 常见错误与排查

| 错误码 | 原因 | 解决方案 |
|--------|------|---------|
| 1254064 | 日期字段格式错误 | 必须用毫秒时间戳（如 `1772121600000`），不能用字符串或秒级时间戳 |
| 1254068 | 超链接字段格式错误 | 必须用对象 `{text: "显示文本", link: "URL"}`，不能传字符串 |
| 1254066 | 人员字段格式错误 | 必须传 `[{id: "ou_xxx"}]`，确认 user_id_type |
| 1254015 | 字段值格式与类型不匹配 | 先 list 字段，按类型构造正确格式 |
| 1254104 | 批量创建超过 500 条 | 分批调用，每批 max 500 |
| 1254291 | 并发写冲突 | 串行调用 + 延迟 0.5-1 秒 |
| 1254303 | 附件未上传到当前表格 | 先调用上传素材接口 |
| 1254045 | 字段名不存在 | 检查字段名（包括空格、大小写） |

---

## 附录

### 资源层级

```
App (多维表格应用)
 +-- Table (数据表) x100
 |    +-- Record (记录/行) x20,000
 |    +-- Field (字段/列) x300
 |    +-- View (视图) x200
 +-- Dashboard (仪表盘)
```

### 筛选 operator 列表

| operator | 含义 | value 要求 |
|----------|------|-----------|
| `is` | 等于 | 单个值 |
| `isNot` | 不等于 | 单个值 |
| `contains` | 包含 | 可多个值 |
| `doesNotContain` | 不包含 | 可多个值 |
| `isEmpty` | 为空 | 必须为 `[]` |
| `isNotEmpty` | 不为空 | 必须为 `[]` |
| `isGreater` | 大于 | 单个值（数字、日期） |
| `isGreaterEqual` | 大于等于 | 单个值（仅数字） |
| `isLess` | 小于 | 单个值（数字、日期） |
| `isLessEqual` | 小于等于 | 单个值（仅数字） |

日期字段特殊值: `["Today"]`, `["Tomorrow"]`, `["ExactDate", "时间戳"]` 等

### 使用限制

| 限制项 | 上限 |
|--------|------|
| 数据表 + 仪表盘 | 100/App |
| 记录数 | 20,000/表 |
| 字段数 | 300/表 |
| 视图数 | 200/表 |
| 批量操作 | 500/次 |

### 其他约束

- 从其他数据源同步的数据表不支持增删改记录
- 公式字段、查看引用字段是只读的
- 删除操作无法恢复
- 视图筛选条件使用 `field_id`，需先调用 field.list 获取
