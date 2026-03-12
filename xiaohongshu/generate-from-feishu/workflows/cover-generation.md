# Cover Generation Workflow

This document describes the step-by-step workflow for generating poster covers.

---

## Prerequisites

1. Feishu record with required fields (星座, 标题, 模板)
2. Playwright MCP available
3. Template design spec file exists

---

## Workflow Steps

### Step 1: Fetch Record from Feishu

```
Call mcp__lark-mcp__bitable_v1_appTableRecord_search
Parameters:
- path.app_token: <LARK_BITABLE_APP_TOKEN>
- path.table_id: <LARK_BITABLE_TABLE_ID>
- data.filter: { conditions: [{ field_name: "已生成", operator: "is", value: ["false"] }] }
```

### Step 2: Read Template Design Spec

```bash
# Determine template path based on 模板 field value
TEMPLATE_PATH="zodiac-poster/assets/templates/{template_id}/TEMPLATE.md"

# Read the design specification
cat "$TEMPLATE_PATH"
```

### Step 3: Generate HTML

Based on the template design spec:

1. Choose a style package (经典强调/简约边框/杂志双线/艺术镂空)
2. Lock the style in HTML comment: `<!-- [STYLE LOCK: xxx] -->`
3. Generate HTML with:
   - Correct viewport meta tag
   - Dark mode prevention CSS
   - Accent-colored keywords in title

**Cover HTML Requirements:**
```html
<!-- [STYLE LOCK: 杂志双线] [LAYOUT LOCK: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <style>
    :root, html, body { color-scheme: light only; background: #FAF6F1; }
    /* ... template styles ... */
  </style>
</head>
<body>
  <div class="poster">
    <!-- Title with accent words -->
    <h1>少一点<span class="accent">期待</span>
        多一点<span class="accent">随缘</span></h1>
    <!-- ... -->
  </div>
</body>
</html>
```

### Step 4: Save HTML to Output Directory

```bash
# Create output directory
OUTPUT_DIR="output/$(date +%Y)/$(date +%m)/$(date +%d)/{zodiac}-{title}-$(date +%y%m%d)"
mkdir -p "$OUTPUT_DIR"

# Save HTML
HTML_PATH="$OUTPUT_DIR/cover.html"
```

### Step 5: Screenshot Cover

Use the shared screenshot script instead of MCP browser screenshots:

```bash
python3 ./_shared/scripts/poster_screenshot.py \
  "$HTML_PATH" \
  "$OUTPUT_DIR/{zodiac}-{title}-cover.png"
```

### Step 6: Upload to Feishu

```bash
python upload-to-feishu/upload.py \
  --record-id "$RECORD_ID" \
  --images "$OUTPUT_DIR/{zodiac}-{title}-cover.png"
```

### Step 7: Update Record Status

```
Call mcp__lark-mcp__bitable_v1_appTableRecord_update
Parameters:
- path.record_id: $RECORD_ID
- data.fields: { "已生成": true }
```

---

## Checklist

Before marking complete:

- [ ] HTML includes style lock comment
- [ ] Title has accent-colored keywords
- [ ] Screenshot is 1080x1440 px
- [ ] Image uploaded to Feishu attachment field
- [ ] Record marked as 已生成=true
