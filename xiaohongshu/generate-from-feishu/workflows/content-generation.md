# Content Page Generation Workflow

This document describes the workflow for generating content pages (套图内容页).

---

## Prerequisites

1. Cover page already generated with STYLE LOCK
2. 正文内容 field contains multiple paragraphs (≥6 for full set)
3. Same template spec as cover

---

## Key Rules

### Style Consistency

**All content pages MUST use the same style as the cover!**

```html
<!-- Cover uses this style -->
<!-- [STYLE LOCK: 杂志双线] [LAYOUT LOCK: B] -->

<!-- ALL content pages must also use -->
<!-- [STYLE LOCK: 杂志双线] [LAYOUT LOCK: ?] -->
```

The STYLE LOCK must be identical. LAYOUT LOCK can vary (A/B/C/D/E) for visual variety.

### Layout Variation Strategy

For a 6-page set (1 cover + 5 content pages):

| Page | Suggested Layout | Purpose |
|------|------------------|---------|
| Cover | A or B | Eye-catching, centered |
| Page 2 | C | Number-led, introduce topic |
| Page 3 | D | Quote style, key insight |
| Page 4 | C | Continue numbering |
| Page 5 | B | Chapter style, climax |
| Page 6 | S | Summary, centered conclusion |

### Summary Page (Layout S)

The **last content page** should use Layout S (Summary style):

```html
<!-- [STYLE LOCK: 杂志双线] [LAYOUT LOCK: S] -->
<div class="summary-quote">❝</div>
<div class="main-summary">
  <h2 class="summary-title">这就是射手</h2>
  <p class="summary-content">
    总结性的文字...<br/>
    留有余韵的收尾。
  </p>
  <div class="summary-end">
    <span class="end-star"></span>
  </div>
</div>
```

---

## Workflow Steps

### Step 1: Parse Content Paragraphs

```python
# Split content by newlines
paragraphs = record['正文内容'].split('\n')
# Filter empty lines
paragraphs = [p.strip() for p in paragraphs if p.strip()]
# Should have at least 5 paragraphs for 5 content pages
```

### Step 2: Generate HTML for Each Page

For each paragraph:

1. Read the style lock from cover HTML
2. Choose appropriate layout variant (A/B/C/D/E or S for last page)
3. Generate HTML with same style, different layout

```bash
# For each page (02, 03, 04, 05, 06...)
HTML_PATH="$OUTPUT_DIR/page-{page_num}.html"
```

### Step 3: Screenshot Each Page

Repeat for each page with the shared screenshot script:

```bash
python3 ./_shared/scripts/poster_screenshot.py \
  "$HTML_PATH" \
  "$OUTPUT_DIR/{zodiac}-{title}-page-{num}.png"
```

For a full set, prefer batch mode so the browser instance is reused:

```bash
python3 ./_shared/scripts/poster_screenshot.py \
  --batch "$OUTPUT_DIR/html" "$OUTPUT_DIR"
```

### Step 4: Batch Upload

```bash
python upload-to-feishu/upload.py \
  --record-id "$RECORD_ID" \
  --dir "$OUTPUT_DIR/"
```

### Step 5: Update Record

```
Call mcp__lark-mcp__bitable_v1_appTableRecord_update
Parameters:
- data.fields: { "已生成": true }
```

---

## Content Page Structure

### Standard Content Page (Layout C)

```html
<div class="poster">
  <div class="number-lead">01</div>
  <div class="main-c">
    <h2 class="section-keyword">核心关键词</h2>
    <p class="content-c">
      这是本页的正文内容...<br/>
      可以有<span class="accent">重点词</span>标记。
    </p>
  </div>
</div>
```

### Quote Style Page (Layout D)

```html
<div class="poster">
  <div class="quote-mark">❝</div>
  <div class="main-d">
    <blockquote class="quote-content">
      金句内容...
    </blockquote>
  </div>
</div>
```

---

## Checklist

- [ ] All pages use same STYLE LOCK as cover
- [ ] Layout varies for visual interest
- [ ] Last page uses Layout S (summary)
- [ ] Each page has one content paragraph
- [ ] All images uploaded to Feishu
- [ ] Total pages = paragraphs + 1 (cover)
