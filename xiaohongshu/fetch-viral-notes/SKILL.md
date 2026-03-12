---
name: fetching-viral-notes
description: Searches Xiaohongshu for low-follower viral notes and saves them to Feishu Bitable. Use this skill whenever the user wants to find trending content, discover viral posts, research successful notes, analyze what's working on XHS, build a content library, scrape competitor content, or batch collect high-engagement low-follower posts — even if they don't explicitly say "fetch viral notes". Triggers on keywords like 抓取, 爆文, 低粉, 热门笔记, 竞品分析, 内容库.
---

# 小红书低粉爆文抓取器

搜索小红书内容，筛选低粉高互动的爆文，保存到飞书多维表格。

## 上下文优化

为防止上下文溢出（长输出会占满对话窗口导致后续操作失败）：

- **默认最多 5 条**笔记，用户可指定更多
- **静默处理**：获取详情和保存过程不输出中间结果
- **一次性汇报**：处理完成后输出汇总表格
- 遇到 Context low 提示时立即停止，汇报已完成的结果

汇报格式：
```
搜索关键词：xxx | 搜索结果：X 条 | 符合条件：Y 条 | 已保存：Y 条

| 标题 | 点赞 | 粉丝 | 互动比 |
|------|------|------|--------|
| xxx  | 5000 | 2000 | 2.5    |
```

---

## 执行前检查

### 1. 小红书登录

> 详细流程见 [`../_shared/xiaohongshu-login.md`](../_shared/xiaohongshu-login.md)

调用 `mcp__xiaohongshu-mcp__check_login_status`，未登录则执行扫码登录。

### 2. 飞书配置

> 详细配置见 [`../_shared/feishu-config.md`](../_shared/feishu-config.md)

```
app_token: <LARK_BITABLE_APP_TOKEN>
table_id: <LARK_VIRAL_NOTES_TABLE_ID>  # 低粉爆文抓取
```

### 3. 首次使用

如果飞书表格字段未初始化：
```bash
cd "."
python fetch-viral-notes/init_bitable_fields.py
```

---

## 核心 MCP 工具

### 搜索笔记

```
mcp__xiaohongshu-mcp__search_feeds
  keyword: "搜索关键词"
  filters:
    sort_by: "最多点赞"       # 综合|最新|最多点赞|最多评论|最多收藏
    note_type: "不限"         # 不限|视频|图文
    publish_time: "一周内"    # 不限|一天内|一周内|半年内
```

### 获取笔记详情

```
mcp__xiaohongshu-mcp__get_feed_detail
  feed_id: "笔记ID"
  xsec_token: "从搜索结果获取"
```

### 获取作者信息

```
mcp__xiaohongshu-mcp__user_profile
  user_id: "作者ID"
  xsec_token: "从笔记详情获取"
```

### 保存到飞书

```
mcp__lark-mcp__bitable_v1_appTableRecord_create
  path: { app_token, table_id }
  data:
    fields:
      笔记ID, 标题, 内容摘要, 作者昵称, 作者粉丝数,
      点赞数, 收藏数, 评论数, 搜索关键词, 笔记链接
```

---

## 低粉爆文筛选标准

**核心定义：粉丝少但互动高 — 说明内容本身有爆款潜力**

| 指标 | 默认条件 | 用户可自定义 |
|------|----------|-------------|
| 作者粉丝数 | < 10,000 | 如"粉丝5000以下" |
| 点赞数 | > 1,000 | 如"点赞5000以上" |
| 互动粉丝比 | > 0.1 | — |

```
互动粉丝比 = (点赞 + 收藏 + 评论) / 粉丝数
```

比值越高说明内容质量越好。

---

## 执行流程

```
1. 检查登录 → 只输出"已登录"或引导登录
2. 搜索内容 → 记录结果数量，不输出列表
3. 逐条处理（默认最多5条）:
   - 获取详情 + 作者信息（静默）
   - 筛选：粉丝 < 阈值 且 点赞 > 阈值
   - 保存到飞书（静默）
4. 输出汇总表格
```

---

## 飞书表格字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 笔记ID | 文本 | 唯一标识 |
| 标题 | 文本 | 笔记标题 |
| 内容摘要 | 文本 | 正文前200字 |
| 作者昵称 | 文本 | — |
| 作者ID | 文本 | — |
| 作者粉丝数 | 数字 | 抓取时的粉丝数 |
| 点赞数 | 数字 | — |
| 收藏数 | 数字 | — |
| 评论数 | 数字 | — |
| 互动粉丝比 | 数字 | (点赞+收藏+评论)/粉丝 |
| 笔记类型 | 单选 | 图文/视频 |
| 笔记链接 | 文本 | — |
| 封面图 | 文本 | URL |
| 搜索关键词 | 文本 | 抓取时使用的关键词 |
| 抓取时间 | 日期 | — |
| 已分析 | 复选框 | — |
| 备注 | 文本 | 人工备注 |

---

## 注意事项

- **请求间隔**：每次抓取间隔 2-3 秒，避免被限流
- **去重**：保存前检查笔记ID是否已存在
- **时效性**：互动数据会变化，记录抓取时间便于对比
- **登录有效期**：cookies 约 7 天过期

---

## 错误处理

| 问题 | 原因 | 解决 |
|------|------|------|
| 未登录 | cookies 过期 | 扫码重新登录 |
| 获取详情失败 | xsec_token 过期或笔记已删除 | 跳过该笔记继续 |
| 飞书写入失败 | 字段类型不匹配 | 运行 init_bitable_fields.py |
