# Validation Rules

This document defines validation rules for content generation and publishing.

---

## Record Validation (Before Generation)

### Required Fields

| Field | Rule | Error Message |
|-------|------|---------------|
| 星座 | Must not be empty | "缺少必填字段: 星座" |
| 标题 | Must not be empty | "缺少必填字段: 标题" |
| 模板 | Must be valid template ID | "无效的模板ID" |

### Optional Field Defaults

| Field | Default Value |
|-------|---------------|
| 副标题 | Empty string |
| 正文内容 | Empty (cover-only mode) |
| 用途 | "封面" |

---

## Content Validation

### Title Rules

| Rule | Limit | Example |
|------|-------|---------|
| Max length | 20 Chinese characters | "射手座脾气好吗" |
| No emojis (Xiaohongshu title) | - | - |
| Required accent word | At least 1 `<span class="accent">` | `<span class="accent">期待</span>` |

### Content Rules

| Rule | Limit |
|------|-------|
| Min paragraphs for套图 | 6 paragraphs (to generate 5 content pages) |
| Max paragraph length | 60 characters per paragraph |
| Total length | 200-300 characters |

---

## Copywriting Style Rules

### Recommended

| Pattern | Example |
|---------|---------|
| Casual filler words | emmm、怎么说呢、好像是、反正就是 |
| Varied punctuation | 破折号、省略号、不规则标点 |
| Short sentences | 主语 + 动词，简洁有力 |
| Personal perspective | 我觉得、我发现 |

### Prohibited

| Pattern | Why |
|---------|-----|
| 宝子们、姐妹们 | AI-detectable, overly familiar |
| 感叹号堆砌 (!!!) | Looks artificial |
| 太真实了！爱死了！必看！ | Generic viral bait |
| 点赞收藏不迷路 | Spam-like CTA |
| 首先...其次...最后... | Structured enumeration |

---

## HTML Generation Rules

### Style Lock

Every HTML file must include a style lock comment:

```html
<!-- [STYLE LOCK: 杂志双线] [LAYOUT LOCK: B] -->
```

**Rule**: All pages in a set must use the same STYLE LOCK and LAYOUT LOCK values.

### Dark Mode Prevention

Every HTML must include:

```css
:root, html, body {
  color-scheme: light only;
  background: #FAF6F1;
}
```

### Accent Words (Poster Cover)

Cover pages must have accent-colored keywords:

```html
<!-- CORRECT -->
<h1>少一点<span class="accent">期待</span>
    多一点<span class="accent">随缘</span></h1>

<!-- WRONG - No accent words -->
<h1>少一点期待，多一点随缘</h1>
```

---

## Image Validation

### Screenshot Checks

| Check | Expected |
|-------|----------|
| Dimensions | 1080 × 1440 px |
| File format | PNG |
| File size | < 5 MB |
| Contains content | Not blank/white |

### Upload Checks

| Check | Action |
|-------|--------|
| File exists | Verify path before upload |
| Upload success | Check for file_token in response |
| Attachment updated | Verify field contains file_token array |

---

## Publishing Validation

### Pre-publish Checks

| Check | Requirement |
|-------|-------------|
| 已生成 | Must be `true` |
| 生成图片 | Must have at least 1 attachment |
| Xiaohongshu login | Must be logged in |

### Post-publish Updates

| Field | Value |
|-------|-------|
| 已发布 | `true` |
| 小红书文案 | Actual published caption |

---

## Validation Script

Run this script to validate a record before generation:

```bash
python generate-from-feishu/scripts/validate_record.py --record-id "recXXX"
```

Output:
- Exit code 0: Valid
- Exit code 1: Invalid (errors printed to stderr)
