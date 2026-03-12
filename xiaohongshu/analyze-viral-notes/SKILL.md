---
name: analyze-viral-notes
description: |
  Analyze viral Xiaohongshu (Little Red Book) notes to extract what made them go viral.
  Triggers: "analyze viral notes", "analyze trending posts", "why did this note go viral",
  "爆文分析", "分析爆款", "分析飞书里的爆文", "viral content analysis", "content patterns".
  Fetches unanalyzed notes from Feishu Bitable, retrieves full content via xiaohongshu-mcp,
  performs AI analysis on viral elements (title hooks, emotional triggers, engagement tactics),
  and writes structured results back to Feishu.
---

# 低粉爆文分析器

从飞书"低粉爆文抓取"表获取待分析笔记，通过小红书 MCP 获取详情，AI 分析爆款元素，回写分析结果。

## 上下文优化

- 默认最多处理 10 条笔记
- 分析过程中不输出完整笔记内容
- 使用固定模板输出分析结果

## 飞书表格配置

详细配置见 [`../_shared/feishu-config.md`](../_shared/feishu-config.md)

```
app_token: <LARK_BITABLE_APP_TOKEN>
table_id: <LARK_VIRAL_NOTES_TABLE_ID>  # 低粉爆文抓取
```

## 首次使用 - 初始化分析字段

如果飞书表格中还没有分析相关字段，依次调用 `mcp__lark-mcp__bitable_v1_appTableField_create` 创建：

| 字段名 | 类型 | type值 | 说明 |
|--------|------|--------|------|
| 分析时间 | 日期 | 5 | `date_formatter: "yyyy/MM/dd HH:mm"` |
| 标题分析 | 文本 | 1 | |
| 开头钩子 | 文本 | 1 | |
| 内容结构 | 文本 | 1 | |
| 情绪价值 | 文本 | 1 | |
| 互动引导 | 文本 | 1 | |
| 封面类型 | 单选 | 3 | options: 文字封面/图片封面/人物封面 |
| 爆款元素 | 文本 | 1 | |
| 可借鉴点 | 文本 | 1 | |
| 内容标签 | 文本 | 1 | |
| 完整内容 | 文本 | 1 | |
| 热门评论 | 文本 | 1 | |

## 执行前检查

详细登录流程见 [`../_shared/xiaohongshu-login.md`](../_shared/xiaohongshu-login.md)

调用 `mcp__xiaohongshu-mcp__check_login_status`，如果未登录则执行扫码登录。

## 核心流程

### 步骤 1: 从飞书获取待分析记录

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_search
参数:
- path: { app_token: "<LARK_BITABLE_APP_TOKEN>", table_id: "<LARK_VIRAL_NOTES_TABLE_ID>" }
- data: {
    filter: {
      conjunction: "and",
      conditions: [{ field_name: "已分析", operator: "is", value: ["false"] }]
    }
  }
```

保存每条记录的 `record_id`（回写用）、`笔记ID`（获取详情用）、`xsec_token`（访问笔记用）。

### 步骤 2: 获取笔记详情

```
调用 mcp__xiaohongshu-mcp__get_feed_detail
参数:
- feed_id: "<笔记ID>"
- xsec_token: "<xsec_token>"
- load_all_comments: true
- limit: 20
```

### 步骤 3: AI 分析爆款元素

分析维度（每个维度不超过50字）：

| 维度 | 分析内容 |
|------|----------|
| 标题分析 | 数字/疑问句/痛点词/情绪词等技巧 |
| 开头钩子 | 前3行如何吸引用户 |
| 内容结构 | 正文组织逻辑，信息密度 |
| 情绪价值 | 共鸣点，情感触发点 |
| 互动引导 | 评论/收藏引导技巧 |
| 封面类型 | 文字封面/图片封面/人物封面 |
| 爆款元素 | 3-5个可复用标签 |
| 可借鉴点 | 最值得学习的1-2个技巧 |
| 内容标签 | 情感/干货/种草等分类 |

分析时使用以下信息：标题、点赞/收藏/评论数、粉丝数、互动比、正文内容、热门评论。

### 步骤 4: 回写飞书

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_update
参数:
- path: { app_token: "<LARK_BITABLE_APP_TOKEN>", table_id: "<LARK_VIRAL_NOTES_TABLE_ID>", record_id: "<record_id>" }
- data: {
    fields: {
      "已分析": true,
      "分析时间": <当前时间戳毫秒>,
      "标题分析": "...",
      "开头钩子": "...",
      "内容结构": "...",
      "情绪价值": "...",
      "互动引导": "...",
      "封面类型": "文字封面",
      "爆款元素": "数字标题, 痛点开头, 干货内容",
      "可借鉴点": "...",
      "内容标签": "情感, 自我提升",
      "完整内容": "<正文内容>",
      "热门评论": "<高赞评论摘要>"
    }
  }
```

## 使用示例

- `/analyze-viral-notes` 或 "分析飞书里的爆文" — 自动查询未分析记录并批量处理
- "分析这条笔记 6766e99a000000001d01d8d0" — 从飞书查找该笔记ID的记录，获取详情并分析

## 输出格式

完成后输出摘要表格：

| 标题 | 点赞 | 爆款元素 | 可借鉴点 |
|------|------|----------|----------|
| xxx  | 5000 | 数字标题,痛点 | 标题结构 |

## 错误处理

- **xsec_token 过期**：跳过该记录，在备注字段记录失败原因
- **笔记已删除**：标记已分析=true，备注"笔记已删除"
- **字段不存在**：先执行"初始化分析字段"步骤创建所需字段
