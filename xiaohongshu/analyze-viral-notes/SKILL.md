---
name: analyzing-viral-notes
description: Analyzes viral Xiaohongshu notes stored in Feishu Bitable by fetching full content via MCP and identifying viral elements. Use when the user wants to analyze why certain notes went viral, extract successful content patterns, or write analysis results back to Feishu.
---

# 低粉爆文分析器

从飞书"低粉爆文抓取"表获取待分析的笔记，使用小红书 MCP 获取详情，AI 分析爆款元素，回写分析结果。

---

## 上下文优化指南（重要）

1. **限制分析数量**：默认最多处理 10 条笔记
2. **精简输出**：分析过程中不输出完整笔记内容
3. **结构化分析**：使用固定模板输出分析结果

---

## 飞书表格配置

> 详细配置见 [`../_shared/feishu-config.md`](../_shared/feishu-config.md)

```
app_token: <LARK_BITABLE_APP_TOKEN>
table_id: <LARK_VIRAL_NOTES_TABLE_ID>  # 低粉爆文抓取
```

---

## 首次使用 - 初始化分析字段

**如果飞书表格中还没有分析相关字段，需要先创建：**

依次调用 `mcp__lark-mcp__bitable_v1_appTableField_create` 创建以下字段：

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

---

## 执行前检查

> 详细登录流程见 [`../_shared/xiaohongshu-login.md`](../_shared/xiaohongshu-login.md)

```
调用 mcp__xiaohongshu-mcp__check_login_status
```

如果未登录，执行扫码登录。

---

## 核心流程

### 步骤 1: 从飞书获取待分析记录

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_search
参数:
- path: {
    app_token: "<LARK_BITABLE_APP_TOKEN>",
    table_id: "<LARK_VIRAL_NOTES_TABLE_ID>"
  }
- data: {
    filter: {
      conjunction: "and",
      conditions: [{
        field_name: "已分析",
        operator: "is",
        value: ["false"]
      }]
    }
  }
```

**保存每条记录的：**
- `record_id` - 用于回写
- `笔记ID` - 用于获取详情
- `xsec_token` - 用于访问笔记

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

**分析维度：**

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

### 步骤 4: 回写飞书

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_update
参数:
- path: {
    app_token: "<LARK_BITABLE_APP_TOKEN>",
    table_id: "<LARK_VIRAL_NOTES_TABLE_ID>",
    record_id: "<record_id>"
  }
- data: {
    fields: {
      "已分析": true,
      "分析时间": <当前时间戳毫秒>,
      "标题分析": "xxx",
      "开头钩子": "xxx",
      "内容结构": "xxx",
      "情绪价值": "xxx",
      "互动引导": "xxx",
      "封面类型": "文字封面",
      "爆款元素": "数字标题, 痛点开头, 干货内容",
      "可借鉴点": "xxx",
      "内容标签": "情感, 自我提升",
      "完整内容": "<正文内容>",
      "热门评论": "<高赞评论摘要>"
    }
  }
```

---

## 分析提示词

```
请分析这篇小红书爆款笔记：

【笔记信息】
- 标题: {title}
- 点赞: {likes} | 收藏: {favorites} | 评论: {comments}
- 粉丝: {followers} | 互动比: {ratio}

【正文内容】
{content}

【热门评论】
{top_comments}

请输出：
1. 标题分析：使用了什么技巧？
2. 开头钩子：前3行如何吸引用户？
3. 内容结构：正文的组织逻辑？
4. 情绪价值：触动用户的点？
5. 互动引导：引导互动的技巧？
6. 封面类型：文字/图片/人物封面
7. 爆款元素：3-5个可复用标签
8. 可借鉴点：最值得学习的技巧
9. 内容标签：内容类型分类

每个维度不超过50字。
```

---

## 使用示例

### 示例 1: 分析待处理的爆文

```
用户: /analyze-viral-notes
或: 分析飞书里的爆文

Claude:
1. 查询飞书表格，获取已分析=false的记录
2. 获取笔记详情
3. AI 分析并回写结果
```

### 示例 2: 分析指定笔记ID

```
用户: 分析这条笔记 6766e99a000000001d01d8d0

Claude:
1. 从飞书查找该笔记ID的记录
2. 获取详情并分析
```

---

## 输出格式

```
✅ 分析完成！

| 标题 | 点赞 | 爆款元素 | 可借鉴点 |
|------|------|----------|----------|
| xxx  | 5000 | 数字标题,痛点 | 标题结构 |
```

---

## 错误处理

- **xsec_token 过期**：跳过该记录，在备注字段记录失败
- **笔记已删除**：标记已分析=true，备注"笔记已删除"
- **字段不存在**：先执行"初始化分析字段"步骤
