# Unified Input/Output Specification

This document defines the standard input sources and output formats for all skills in this project.

---

## Input Sources

### Feishu Bitable

All content data is stored in Feishu Bitable (多维表格).

| Table | app_token | table_id | Purpose |
|-------|-----------|----------|---------|
| 星座海报生成表 | `<LARK_BITABLE_APP_TOKEN>` | `<LARK_BITABLE_TABLE_ID>` | Store poster content to generate |
| 低粉爆文抓取表 | `<LARK_BITABLE_APP_TOKEN>` | `<LARK_VIRAL_NOTES_TABLE_ID>` | Store viral notes for analysis |

### Xiaohongshu MCP

Used for fetching note details, comments, and publishing content.

**Login check**: Always call `mcp__xiaohongshu-mcp__check_login_status` before operations.

---

## Output Specifications

### Image Output

| Property | Value |
|----------|-------|
| **Path Pattern** | `output/{YYYY}/{MM}/{DD}/{zodiac}-{title}-{YYMMDD}/` |
| **Viewport** | 1080 × 1440 px (3:4 vertical ratio) |
| **Actual Pixels** | 2160 × 2880 px (2x export, `device_scale_factor=2`) |
| **Format** | PNG |
| **Naming** | `{zodiac}-{title}-cover.png`, `{zodiac}-{title}-page-02.png`, etc. |

### File Naming Convention

```
output/
└── 2026/
    └── 01/
        └── 02/
            └── 射手座-脾气好吗-260102/
                ├── 射手座-脾气好吗-cover.png
                ├── 射手座-脾气好吗-page-02.png
                ├── 射手座-脾气好吗-page-03.png
                └── ...
```

---

## Feishu Writeback Rules

After generating content, update these fields in Feishu:

| Field | Type | Description |
|-------|------|-------------|
| 已生成 | Boolean | Set to `true` after images generated |
| 生成图片 | Attachment | Upload actual image files (not just paths) |
| 已发布 | Boolean | Set to `true` after published to Xiaohongshu |
| 小红书文案 | Text | Store the published caption |

**Important**: The `生成图片` field requires actual file upload via the upload script, not just text updates.

---

## Screenshot Requirements

Use the shared screenshot script instead of MCP browser screenshots:

```bash
python3 ./_shared/scripts/poster_screenshot.py \
  <input.html> \
  <output.png>
```

For full poster sets, prefer batch mode so the browser instance is reused:

```bash
python3 ./_shared/scripts/poster_screenshot.py \
  --batch <html_dir> <output_dir>
```

### Dark Mode Prevention

All HTML templates must include:

```css
:root, html, body {
  color-scheme: light only;
  background: #FAF6F1;
}
```

---

## Xiaohongshu Publishing Format

| Property | Requirement |
|----------|-------------|
| Title | ≤ 20 Chinese characters |
| Content | 100-200 characters |
| Images | Local absolute paths or HTTP URLs |
| Tags | 3-5 hashtags |

---

## Cross-Reference

- **Feishu credentials**: See [feishu-config.md](feishu-config.md)
- **Xiaohongshu login**: See [xiaohongshu-login.md](xiaohongshu-login.md)
- **Field mapping**: See [field-mapping.md](field-mapping.md)
- **Validation rules**: See [validation-rules.md](validation-rules.md)
