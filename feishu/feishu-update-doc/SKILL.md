---
name: feishu-update-doc
description: |
  更新飞书云文档内容，支持 7 种更新模式（追加、覆盖、定位替换、全文替换、前/后插入、删除）。当用户需要修改、更新、追加、替换、删除飞书文档中的内容时使用此 skill。触发场景包括用户说"更新文档"、"修改文档"、"在文档里加点内容"、"删掉这一段"、"替换文档中的..."，或任何涉及编辑已有飞书云文档的需求。
---

# 更新飞书云文档

通过 MCP 调用 `update-doc`，更新飞书云文档内容。优先使用局部更新（replace_range/append/insert_before/insert_after），慎用 overwrite（会清空文档重写，可能丢失图片、评论等）。

## 7 种更新模式

| 模式 | 用途 | 需要定位 | 需要 markdown |
|------|------|---------|-------------|
| append | 追加到末尾 | 否 | 是 |
| overwrite | 完全覆盖（慎用） | 否 | 是 |
| replace_range | 定位替换（唯一匹配） | 是 | 是 |
| replace_all | 全文替换（多处） | 是 | 是 |
| insert_before | 在匹配内容前插入 | 是 | 是 |
| insert_after | 在匹配内容后插入 | 是 | 是 |
| delete_range | 删除匹配内容 | 是 | 否 |

---

## 定位方式

需要定位的模式（replace_range/replace_all/insert_before/insert_after/delete_range）支持两种方式，二选一：

### selection_with_ellipsis -- 内容定位

两种格式：

1. **范围匹配**：`开头内容...结尾内容` -- 匹配从开头到结尾的所有内容（含中间部分）。建议 10-20 字符确保唯一性。
2. **精确匹配**：`完整内容`（不含 `...`）-- 匹配完整文本，适合短文本、关键词。

转义：内容本身包含 `...` 时，用 `\.\.\.` 表示字面量三个点。

### selection_by_title -- 标题定位

格式：`## 章节标题`（可带或不带 # 前缀）

自动定位整个章节（从该标题到下一个同级或更高级标题之前）。

示例：
- `## 功能说明` -- 定位二级标题"功能说明"及其下所有内容
- `功能说明` -- 定位任意级别的"功能说明"标题

---

## 可选参数

### new_title

更新文档标题。仅支持纯文本，1-800 字符。标题更新在内容更新之后执行，可与任何 mode 配合使用。

---

## 返回值

成功：
```json
{
  "success": true,
  "doc_id": "文档ID",
  "mode": "使用的模式",
  "message": "文档更新成功（xxx模式）"
}
```

异步模式（大文档超时）返回 `task_id`，用该 task_id 再次调用 update-doc（仅传 task_id）查询状态。

---

## 使用示例

### append -- 追加到末尾

```json
{
  "doc_id": "文档ID或URL",
  "mode": "append",
  "markdown": "## 新章节\n\n追加的内容..."
}
```

### replace_range -- 定位替换

用 selection_with_ellipsis：
```json
{
  "doc_id": "文档ID或URL",
  "mode": "replace_range",
  "selection_with_ellipsis": "## 旧章节标题...旧章节结尾。",
  "markdown": "## 新章节标题\n\n新的内容..."
}
```

用 selection_by_title（替换整个章节）：
```json
{
  "doc_id": "文档ID或URL",
  "mode": "replace_range",
  "selection_by_title": "## 功能说明",
  "markdown": "## 功能说明\n\n更新后的功能说明内容..."
}
```

### replace_all -- 全文替换

支持多处同时替换（replace_range 要求唯一匹配）。返回值包含 `replace_count` 字段。

```json
{
  "doc_id": "文档ID或URL",
  "mode": "replace_all",
  "selection_with_ellipsis": "张三",
  "markdown": "李四"
}
```

`markdown` 可为空字符串，表示删除所有匹配内容。

### insert_before / insert_after -- 前后插入

```json
{
  "doc_id": "文档ID或URL",
  "mode": "insert_after",
  "selection_with_ellipsis": "```python...```",
  "markdown": "**输出示例**：\n```\nresult = 42\n```"
}
```

### delete_range -- 删除内容

```json
{
  "doc_id": "文档ID或URL",
  "mode": "delete_range",
  "selection_by_title": "## 废弃章节"
}
```

不需要 markdown 参数。

### 同时更新标题和内容

在任何模式中添加 `new_title` 参数：

```json
{
  "doc_id": "文档ID或URL",
  "mode": "append",
  "markdown": "## 更新日志\n\n2025-12-18: 新增功能...",
  "new_title": "项目文档（已更新）"
}
```

---

## 最佳实践

### 小粒度精确替换

定位范围越小越安全。表格、分栏等嵌套块中，应精确定位到需要修改的文本，避免影响其他内容（如图片引用）。

### 保护不可重建的内容

图片、画板、电子表格、多维表格、任务等以 token 形式存储，无法读出后原样写入。替换时避开包含这些内容的区域，精确定位到纯文本部分。

### 分步更新优于整体覆盖

修改多处内容时，多次小范围替换逐步修改，优于用 overwrite 重写整个文档。原因：局部更新保留原有媒体、评论、协作历史。

### insert 模式的定位注意

使用 insert_before/insert_after 时，如果目标内容重复出现，需扩大 selection_with_ellipsis 范围来唯一定位。扩大范围时注意：插入位置基于匹配范围的边界（insert_after 在结尾之后，insert_before 在开头之前）。

### 修复画板语法错误

当返回画板写入失败的 warning 时：
1. warning 中包含 whiteboard 标签（如 `<whiteboard token="xxx"/>`）
2. 修正 Mermaid/PlantUML 语法
3. 用 replace_range 替换：selection_with_ellipsis 使用 warning 中的 whiteboard 标签，markdown 提供修正后的代码块

---

## 注意事项

- **Markdown 语法**：支持飞书扩展语法（Lark-flavored Markdown），详见 feishu-create-doc skill 及其 [Lark Markdown 语法参考](../feishu-create-doc/references/lark-markdown-syntax.md)
