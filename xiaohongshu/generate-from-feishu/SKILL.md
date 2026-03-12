---
name: generating-posters-from-feishu
description: |
  Batch generates zodiac poster sets from Feishu Bitable records with automatic HTML rendering, screenshot capture, and upload back to Feishu.
  Trigger this skill when the user wants to:
  - Pull pending records from Feishu and generate poster images
  - Batch create zodiac posters from spreadsheet data
  - Check how many poster tasks are pending in Feishu Bitable
  - Generate posters and upload results back to Feishu attachments
  - Publish Feishu records to Xiaohongshu and mark as published
  Keywords: 飞书, Feishu, 拉取, 批量生成, 待生成, 多维表格, Bitable, 回传, 上传
---

# 飞书多维表格自动化海报生成器

从飞书多维表格读取待生成的海报内容，自动生成图片并上传回飞书。

---

## 截图工具

使用 `../_shared/scripts/poster_screenshot.py` 进行截图，而非 MCP Playwright（Playwright 的 viewport 尺寸不固定，无法保证精确输出）。

```bash
# 批量截图（推荐，浏览器只启动一次）
python3 ./_shared/scripts/poster_screenshot.py \
    --batch /tmp/html_dir/ /path/to/output/

# 单文件截图
python3 ./_shared/scripts/poster_screenshot.py \
    /tmp/cover.html /path/to/output/cover.png

# 1x 导出（默认 2x → 2160x2880）
python3 ./_shared/scripts/poster_screenshot.py \
    --scale 1 input.html output.png
```

工具自动处理：viewport 1080x1440、默认 2x 导出、字体加载等待 2 秒、截取 `.poster` 元素。

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [io-spec.md](../_shared/io-spec.md) | Unified input/output specifications |
| [field-mapping.md](../_shared/field-mapping.md) | Feishu field definitions |
| [validation-rules.md](../_shared/validation-rules.md) | Content validation rules |
| [cover-generation.md](workflows/cover-generation.md) | Cover page workflow |
| [content-generation.md](workflows/content-generation.md) | Content page workflow |
| [copywriting-rules.md](reference/copywriting-rules.md) | Xiaohongshu copywriting style guide |

---

## 执行前检查

> 飞书配置见 [`../_shared/feishu-config.md`](../_shared/feishu-config.md)

```bash
cp .env.example .env
# 填写 LARK_APP_ID / LARK_APP_SECRET / LARK_BITABLE_APP_TOKEN 等变量
```

---

## 完整生成流程

```
1. 读取 .env 获取飞书配置
2. 调用飞书 API 查询未生成的记录
3. 遍历每条记录:
   a. 读取"模板"字段 → 确定模板 ID
   b. 读取模板设计规范 zodiac-poster/assets/templates/{模板ID}/TEMPLATE.md
   c. AI 根据规范生成 HTML（含智能排版和重点色标记）
   d. 保存 HTML 到 /tmp/ 或 output 目录
   e. 使用截图脚本生成 PNG
   f. 上传图片到飞书存储 → 获取 file_token
   g. 更新记录：已生成=true, 生成图片=[file_tokens...]
4. 汇报生成结果
```

### 防止深色模式

生成的 HTML 必须在 CSS 开头包含以下样式（macOS 深色模式会覆盖默认背景色）：

```css
:root, html, body {
  color-scheme: light only;
  background: #FAF6F1;
}
```

---

## 可用模板

| 模板 | ID | 重点色 | 说明 |
|------|-----|--------|------|
| 编辑暖调 | `editorial-warm` | `#C15F3C` | 编辑杂志风格，带引用块和页码 |
| 极简暖调 | `minimal-warm` | `#C8725A` | 极简居中布局，大留白 |
| 动态编辑风 | `editorial-dynamic` | `#C15F3C` | 4种风格包 × 5种布局变体 |

---

## 封面与内容页风格一致性

同一套图内封面和内容页使用相同风格包，不同记录轮换不同风格（按记录索引）。在 HTML 开头添加 `<!-- [STYLE LOCK: 风格包名称] [LAYOUT LOCK: 布局] -->` 标记。

| 风格包 | 封面装饰 | 内容页装饰 |
|--------|----------|-----------|
| 经典强调 | 圆形装饰、年份背景大字 | 圆形装饰、填色关键词 |
| 简约边框 | 角标装饰、竖线 | 角标装饰、边框关键词 |
| 杂志双线 | 双线边框、星星散布 | 双线边框、双线关键词 |
| 艺术镂空 | 镂空装饰、渐变线 | 镂空装饰、镂空关键词 |

---

## 重点色词规则

重点色词让海报在小红书信息流中一眼抓住注意力。纯黑灰文字缺少视觉锚点，用户滑动时容易跳过。

### 封面

封面至少包含 2 个重点色词（`<span class="accent">词</span>`），形成视觉呼应：

- 主标题中 1-2 个
- 副标题或主标题第二行中另 1 个
- 两个重点色词应形成语义对（对比/递进/因果）

```html
<!-- 正确 -->
<h1 class="main-title">少一点<span class="accent">期待</span><br/>多一点<span class="accent">随缘</span></h1>
```

### 内容页

每张内容页包含 2 个重点色词，形成呼应对：

| 呼应类型 | 示例 |
|----------|------|
| 因果 | `<span class="accent">囤货和冲动消费</span>` → `<span class="accent">只剩心虚</span>` |
| 对比 | `<span class="accent">买的时候爽</span>` → `<span class="accent">看账单心疼</span>` |
| 递进 | `<span class="accent">不在乎贵不贵</span>` → `<span class="accent">只在乎值不值</span>` |
| 转折 | `<span class="accent">本想省钱</span>` → `<span class="accent">结果更亏</span>` |

AI 智能判断流程：断句分析 → 找关系信号词（但/却/结果/只剩/反而/不是...而是/越...越） → 定位呼应对 → 验证语义闭环。

### 总结页

至少 1 个重点色词，与封面首尾呼应。

---

## 总结页规则（Layout S）

套图最后一页使用「总结收尾式」布局：

- 布局标记：`[LAYOUT LOCK: S]`
- 使用 `.main-summary` 容器，内容水平居中
- 包含大引号装饰 + 标题下划线 + 结束星星

```html
<div class="summary-quote">❝</div>
<div class="main-summary">
  <h2 class="summary-title">这就是双子</h2>
  <p class="summary-content">
    来的都是<span class="accent">缘分</span>，<br/>
    留下的才是真心。
  </p>
  <div class="summary-end"><span class="end-star"></span></div>
</div>
```

---

## 回传飞书

生成图片后必须上传回飞书。只更新文本字段而不上传实际图片文件是不完整的。

**方式一：工具脚本（推荐）**

```bash
./scripts/feishu_upload.sh <record_id> <image_dir>
```

**方式二：手动 API 调用**

1. 获取 tenant_access_token
2. 逐张上传图片到飞书存储（`drive/v1/medias/upload_all`），获取 file_token
3. 更新记录：已生成=true, 生成图片路径=目录, 生成图片=[file_tokens]

---

## 发布到小红书后标记已发布

当飞书记录被发布到小红书后，立即标记为「已发布」：

```bash
./scripts/feishu_mark_published.sh <record_id> "<发布的文案>"
```

或调用 `mcp__lark__bitable_v1_appTableRecord_update`，设置 `已发布=true` 和 `小红书文案=<文案>`。

record_id 在拉取记录时就要保存，避免发布后再查询。

---

## 飞书字段参考

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 标题 / 副标题 / 正文内容 | 文本 | 海报内容 |
| 小红书文案 | 文本 | 发布用文案 |
| 分类 | 单选 | 每日运势/节日节点/日常更新等 |
| 用途 | 单选 | 封面布局/长文案布局/套图 |
| 模板 | 文本 | 模板名称 |
| 星座 | 单选 | 12 星座 |
| 已生成 / 已发布 | 复选框 | 状态标记 |
| **生成图片** | **附件** | **上传的图片（必须回传）** |
| 父记录 | 单向关联 | 套图父子关系 |

---

## 输出位置

```
./output/{YYYY}/{MM}/{DD}/
└── {星座}-{标题缩写}-{YYMMDD}-{HHMM}/
    ├── 01-cover.png
    ├── 02-xxx.png
    └── ...
```

---

## 错误处理

| 问题 | 原因 | 解决 |
|------|------|------|
| 飞书"生成图片"字段为空 | 只更新了文本，没上传图片 | `./scripts/feishu_upload.sh <id> <dir>` |
| 飞书 API 调用失败 | 配置错误或权限不足 | 检查 .env 和应用权限 |
| 截图尺寸不是 2160x2880 | 未设置 2x 缩放 | 使用截图工具（默认 2x） |

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `.env` | 飞书配置 |
| `scripts/feishu_upload.sh` | 图片上传工具 |
| `scripts/feishu_mark_published.sh` | 标记已发布 |
| `zodiac-poster/assets/templates.json` | 模板配置 |
| `zodiac-poster/assets/templates/*.md` | 模板设计规范 |
