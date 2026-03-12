# Feishu Bitable Field Mapping

This document defines all field names and their types used across Feishu tables.

---

## Table 1: 星座海报生成表 (<LARK_BITABLE_TABLE_ID>)

### Input Fields (User fills)

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| 星座 | SingleSelect | Zodiac sign (12 options) | 射手座 |
| 标题 | Text | Main poster title | 别追了 |
| 副标题 | Text | Subtitle | 射手回避型 |
| 正文内容 | Text (multiline) | Content paragraphs (newline-separated) | 段落1\n段落2 |
| 模板 | SingleSelect | Template ID | editorial-warm |
| 用途 | SingleSelect | Purpose (封面/内容页/套图) | 套图 |

### Output Fields (System fills)

| Field Name | Type | Description |
|------------|------|-------------|
| 已生成 | Checkbox | Whether images have been generated |
| 生成图片 | Attachment | Uploaded poster images |
| 已发布 | Checkbox | Whether published to Xiaohongshu |
| 小红书文案 | Text | Published caption text |
| 生成时间 | DateTime | Generation timestamp |

### Content Format Specification (内容格式规范)

本节定义海报内容的完整格式结构，用于指导内容生成和数据录入。

#### 封面内容 (Cover Content)

封面由以下字段组成，用于生成第一张海报图片：

| 元素 | 对应字段 | 要求 | 示例 |
|------|----------|------|------|
| 主标题 | `标题` | 10-20字，简短有力，需含重点词 | 别追了 |
| 副标题 | `副标题` | 可选，补充说明，通常为星座+特征 | 射手回避型 |
| 星座符号 | `星座` | 自动生成对应符号和英文名 | ♐ Sagittarius |

**封面生成规则**：
- 主标题中至少1个词需标记为 `<span class="accent">重点词</span>`
- 副标题为空时，封面仅显示主标题和星座信息

#### 正文内容 (Body Content)

正文内容存储在 `正文内容` 字段，使用**换行符**分隔各段落：

```
第一段：话题引入（1-2句，直入主题）
第二段：核心观点（1-2句，主要论点）
第三段：具体方面A（1-2句，第一维度展开）
第四段：具体方面B（1-2句，第二维度展开）
第五段：具体方面C（1-2句，第三维度展开，可选）
第六段：收尾（1-2句，留有余韵）
```

**段落要求**：

| 项目 | 要求 |
|------|------|
| 最少段落数 | 6段（用于生成1封面+5内容页） |
| 每段字数 | 30-60字 |
| 总字数 | 200-300字 |
| 分隔方式 | 使用 `\n` 换行分隔 |

**示例**：

```
我们射手座啊，从来不是你们以为的那种洒脱。

表面上嘻嘻哈哈，其实心里早就有了答案——只是不想承认而已。

喜欢一个人的时候，会忍不住靠近，但又怕太明显。

讨厌一个人的时候，不会撕破脸，只会慢慢消失在你的世界里。

说走就走？那是因为早就在心里告别过无数次了。

有些人是过客，有些人才是归途。你遇到的，是哪一种？
```

#### 用途与生成对应关系

| 用途 | 生成内容 | 标题要求 | 正文要求 |
|------|----------|----------|----------|
| 封面 | 仅生成1张封面图 | 必填 | 可为空 |
| 内容页 | 仅生成正文页 | 必填 | 必填，≥1段 |
| 套图 | 1封面 + N内容页 | 必填 | 必填，≥6段 |

> **注意**：无论何种用途，`标题` 字段都是必填项。

---

## Table 2: 低粉爆文抓取表 (<LARK_VIRAL_NOTES_TABLE_ID>)

### Input Fields (Scraped data)

| Field Name | Type | Description |
|------------|------|-------------|
| 笔记ID | Text | Xiaohongshu note ID (feed_id) |
| 标题 | Text | Note title |
| 作者 | Text | Author name |
| 粉丝数 | Number | Author follower count |
| 点赞数 | Number | Like count |
| 收藏数 | Number | Save count |
| 评论数 | Number | Comment count |
| xsec_token | Text | Access token for fetching details |
| 抓取时间 | DateTime | Scrape timestamp |

### Analysis Fields (AI fills)

| Field Name | Type | Description |
|------------|------|-------------|
| 已分析 | Checkbox | Whether analysis is complete |
| 分析时间 | DateTime | Analysis timestamp |
| 标题分析 | Text | Title pattern analysis |
| 开头钩子 | Text | Opening hook analysis |
| 内容结构 | Text | Content structure analysis |
| 情绪价值 | Text | Emotional value analysis |
| 爆款元素 | Text | Viral elements summary |
| 可复用点 | Text | Reusable patterns |

---

## Field Type Reference

| Type | MCP `type` value | Notes |
|------|------------------|-------|
| Text | 1 | Single or multiline |
| Number | 2 | |
| SingleSelect | 3 | |
| MultiSelect | 4 | |
| DateTime | 5 | Use `date_formatter: "yyyy/MM/dd HH:mm"` |
| Checkbox | 7 | Boolean |
| Attachment | 17 | Requires file upload |

---

## Zodiac Options (星座)

| Chinese | English | Symbol |
|---------|---------|--------|
| 白羊座 | Aries | ♈ |
| 金牛座 | Taurus | ♉ |
| 双子座 | Gemini | ♊ |
| 巨蟹座 | Cancer | ♋ |
| 狮子座 | Leo | ♌ |
| 处女座 | Virgo | ♍ |
| 天秤座 | Libra | ♎ |
| 天蝎座 | Scorpio | ♏ |
| 射手座 | Sagittarius | ♐ |
| 摩羯座 | Capricorn | ♑ |
| 水瓶座 | Aquarius | ♒ |
| 双鱼座 | Pisces | ♓ |

---

## Template Options (模板)

| ID | Name | Description |
|----|------|-------------|
| editorial-warm | 编辑暖调 | Magazine style, warm colors |
| editorial-dynamic | 动态编辑风 | Dynamic magazine style |
| minimal-warm | 简约暖调 | Minimal warm style |
