---
name: creating-zodiac-posters
description: |
  Creates zodiac-themed vertical posters (1080x1440) for Xiaohongshu/social media.
  Trigger this skill when the user wants to:
  - Generate zodiac poster images (星座海报) from content
  - Create cover + content page sets (套图) for horoscope posts
  - Design Chinese-style social media cards with accent color highlights
  - Batch generate poster sets from Markdown design specs
  - Build HTML posters with screenshot capture
  Keywords: 海报, poster, 星座, zodiac, 套图, 封面, 内容页, 截图
---

# 星座海报生成器 v4.0

生成适用于社交媒体的星座主题竖版海报（1080x1440px，3:4比例）。

---

## 截图工具

使用独立 Python 截图工具 `../_shared/scripts/poster_screenshot.py`，而非 MCP Playwright。原因：Playwright 的 viewport 尺寸不固定，无法保证 1080x1440 的精确输出。

```bash
# 单文件
python3 ./_shared/scripts/poster_screenshot.py \
    /tmp/cover.html ./output/cover.png

# 批量（推荐：浏览器只启动一次，速度更快）
python3 ./_shared/scripts/poster_screenshot.py \
    --batch /tmp/poster_html/ /path/to/output/
```

工具自动处理：固定 viewport 1080x1440、等待字体加载 2 秒、截取 `.poster` 元素、headless 模式。支持 `--json` 输出。

---

## 模板系统

使用 Markdown 设计规范文档定义模板样式，AI 根据规范生成 HTML。

| 模板 | ID | 重点色 | 说明 |
|------|-----|--------|------|
| 编辑暖调 | `editorial-warm` | `#C15F3C` | 编辑杂志风格，居中对称，温和内敛 |
| 动态编辑 | `editorial-dynamic` | `#C15F3C` | 动态编辑风，非对称布局，视觉张力强 |
| 极简暖调 | `minimal-warm` | `#C8725A` | 极简居中布局，大留白，适合封面 |

### 模板选择指南

| 主题类型 | 推荐模板 | 推荐装饰 |
|----------|----------|----------|
| 每日运势 | `editorial-dynamic` | 大字号日期背景 + 圆形装饰 |
| 年运势/月运势 | `editorial-dynamic` | 大字号背景 + 圆形装饰 |
| 自由/孤独/情感 | `editorial-dynamic` | 大留白 + 放大淡色图标 |
| 性格/兴奋点 | `editorial-dynamic` | 斜线装饰 + 色块副标题 |
| 规则/清单/指南 | `editorial-dynamic` | 左侧竖线 + 编号列表 |
| 配对/对比/常规 | `editorial-warm` | 居中布局 + 引用块 |

### 模板规范文件

```
assets/templates/editorial-warm/TEMPLATE.md
assets/templates/editorial-dynamic/TEMPLATE.md
assets/templates/editorial-dynamic/examples/
```

---

## 套图生成规则

### 正文段落数 = 内容页数量

正文内容中的每一段（以空行 `\n\n` 分隔）对应一张内容页。每套图固定包含：封面 + 内容页 + 总结页。

| 正文段落数 | 生成页面 | 总图片数 |
|------------|----------|----------|
| N段 | 1封面 + N内容页 + 1总结页 | N+2张 |

```python
# 解析逻辑
paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
num_pages = len(paragraphs)
```

每张内容页包含：
1. **关键词/小标题**：从段落提取 2-4 字核心词
2. **正文**：该段落完整内容
3. **页码**：02, 03, 04...

### 风格一致性

一条记录的封面 + 所有内容页使用同一种风格包 + 同一种布局变体。视觉一致性是小红书套图专业感的基础。

详细的风格锁定系统（包括随机分配公式、布局变体定义、执行流程）见 [references/style-lock-system.md](references/style-lock-system.md)。

---

## 生成流程

### 步骤 0：确定模板

从飞书记录的"模板"字段获取值，映射为模板 ID：

| 字段值 | 模板 ID |
|--------|---------|
| 编辑暖调 | `editorial-warm` |
| 动态编辑风 | `editorial-dynamic` |
| 极简暖调 | `minimal-warm` |
| （空） | `editorial-warm`（默认） |

### 步骤 1：读取设计规范

```
读取 assets/templates/{模板ID}/TEMPLATE.md
```

### 步骤 1.5：确定风格锁定配置

在生成任何页面之前，确定风格包和布局变体并记录。详见 [references/style-lock-system.md](references/style-lock-system.md)。

### 步骤 2：AI 智能处理

1. 分析内容长度 → 决定字号调整（详见 [references/typography-rules.md](references/typography-rules.md)）
2. 识别关键词 → 决定重点色标记（详见 [references/highlight-rules.md](references/highlight-rules.md)）
3. 根据规范生成 HTML → 包含完整 CSS 样式

### 步骤 3：替换内容变量

**封面变量：**
- `{{header_tag}}` → 头部标签（如"射手座 · 回避型"）
- `{{keyword}}` → 关键词
- `{{line1}}` / `{{line2}}` → 主/副标题（支持高亮）
- `{{desc}}` → 底部描述
- `{{zodiac_symbol}}` → 星座符号 SVG

**内容页变量：**
- `{{keyword}}` → 分类标签
- `{{mini_title}}` → 小标题
- `{{body_text}}` → 正文（支持高亮）
- `{{quote_text}}` → 引用块文字
- `{{zodiac_symbol}}` → 星座符号 SVG

### 步骤 4：保存并截图

```bash
# 保存 HTML
output/{YYYY}/{MM}/{DD}/{zodiac}-{title}-{YYMMDD}/cover.html
output/{YYYY}/{MM}/{DD}/{zodiac}-{title}-{YYMMDD}/page-01.html

# 批量截图（推荐）
python3 ./_shared/scripts/poster_screenshot.py \
    --batch /path/to/html_dir/ /path/to/output/
```

### 防止深色模式

生成的 HTML 必须在 CSS 开头包含以下样式。原因：macOS 深色模式会覆盖默认背景色，导致暖杏色背景变成深灰色。

```css
:root, html, body {
  color-scheme: light only;
  background: #FAF6F1;
}
```

---

## 内容类型规则

不同内容类型对封面元素有不同要求。详见 [references/content-type-rules.md](references/content-type-rules.md)。

核心要点：每日运势封面必须在同一行显示日期+星座（48-56px 加粗），这是用户识别相关性的第一要素。

---

## 排版与高亮

- **智能排版**：根据内容长度动态调整字号和行高。行尾应以文字结束，标点不留在行尾。详见 [references/typography-rules.md](references/typography-rules.md)。
- **重点色高亮**：使用【】标记语法，AI 在生成内容时标注高亮词，脚本解析渲染。详见 [references/highlight-rules.md](references/highlight-rules.md)。

---

## 飞书多维表格字段

| 字段 | 类型 | 说明 |
|------|------|------|
| 星座 | 单选 | 12星座 |
| 模板 | 单选 | 模板中文名 |
| 标题 / 副标题 | 文本 | 海报标题 |
| 正文内容 | 长文本 | 内容页正文 |
| 用途 | 单选 | 封面/长文案 |
| 已生成 / 已发布 | 复选框 | 状态标记 |

---

## 星座符号

从 `templates.json` 的 `zodiac_symbols` 获取 SVG 路径：

| 星座 | ID | 星座 | ID |
|------|-----|------|-----|
| 白羊座 | `aries` | 天秤座 | `libra` |
| 金牛座 | `taurus` | 天蝎座 | `scorpio` |
| 双子座 | `gemini` | 射手座 | `sagittarius` |
| 巨蟹座 | `cancer` | 摩羯座 | `capricorn` |
| 狮子座 | `leo` | 水瓶座 | `aquarius` |
| 处女座 | `virgo` | 双鱼座 | `pisces` |

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `assets/templates.json` | 模板配置（含重点色、星座符号） |
| `assets/templates/*.md` | Markdown 设计规范文档 |
| `assets/previews/*/` | 模板预览图片 |
