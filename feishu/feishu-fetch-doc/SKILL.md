---
name: feishu-fetch-doc
description: |
  获取飞书云文档内容（返回 Markdown）。读取飞书文档、知识库文档，并处理文档中的图片、文件和画板。

  **触发场景**：
  - 用户说"读文档"、"看看这个文档"、"获取文档内容"、"打开飞书文档"
  - 用户发送飞书文档链接（包含 feishu.cn/docx/ 或 feishu.cn/wiki/）
  - 用户说"知识库文档"、"wiki 文档"
  - 用户说"下载文档里的图片"、"获取文档附件"
  - 需要读取飞书云文档的文本内容
---

# 获取飞书云文档

调用 `feishu_mcp_fetch_doc` 获取文档的 Markdown 内容。

## 参数

- **`doc_id`**（必填）：从 URL 中提取文档 token
  - 云文档：`https://xxx.feishu.cn/docx/doxcnXXXX` → `doxcnXXXX`
  - 知识库：`https://xxx.feishu.cn/wiki/YKx9bRgm9` → `YKx9bRgm9`

## 图片、文件、画板处理

文档中的媒体文件需要通过 `feishu_drive_fetch_media` 单独下载。

返回的 Markdown 中，媒体以 HTML 标签形式出现：

| 类型 | 标记格式 | 示例 |
|------|---------|------|
| 图片 | `<image token="xxx" .../>` | `<image token="Rkr8bc75Yopo3gx..." width="1833" height="2491"/>` |
| 文件 | `<view type="1"><file token="xxx" name="..."/></view>` | `<file token="G6FWbvXkro..." name="skills.zip"/>` |
| 画板 | `<whiteboard token="xxx"/>` | `<whiteboard token="Z1FjwXuUJh6..."/>` |

提取 `token` 后调用：
```json
{
  "action": "fetch",
  "file_token": "提取的token",
  "output_path": "/path/to/save/file"
}
```

## 工具组合

| 需求 | 工具 |
|------|------|
| 获取文档文本 | `feishu_mcp_fetch_doc` |
| 下载图片/文件/画板 | `feishu_drive_fetch_media` |
