---
name: generating-posters-from-feishu
description: Generates zodiac poster sets from Feishu Bitable records with automatic HTML rendering and screenshot capture. Use when the user wants to batch generate posters from spreadsheet data, process pending Feishu records, sync generated images back to Feishu, or check how many tasks are pending in the Bitable.
---

# 飞书多维表格自动化海报生成器

从飞书多维表格读取待生成的海报内容，自动生成图片并上传回飞书。

---

## ⚠️ 关键要求

### 1. 使用独立截图工具（避免浏览器抢占）

**使用 `../_shared/scripts/poster_screenshot.py` 进行截图，避免 MCP Playwright 浏览器抢占问题。**

**单文件截图：**
```bash
python3 ./_shared/scripts/poster_screenshot.py \
    /tmp/cover.html \
    /path/to/output/cover.png
```

**批量截图（推荐，一套图多页时浏览器只启动一次）：**
```bash
python3 ./_shared/scripts/poster_screenshot.py \
    --batch /tmp/html_dir/ /path/to/output/
```

**工具自动处理：**
- viewport 尺寸 1080x1440
- **默认 2x 导出（实际像素 2160×2880）**
- 字体加载等待 2 秒
- 截取 `.poster` 元素

**如需 1x 导出（1080×1440）：**
```bash
python3 ./_shared/scripts/poster_screenshot.py \
    --scale 1 input.html output.png
```

### 2. 生成后必须回传图片到飞书（重要！）

**生成图片后，必须执行以下两个步骤：**

1. **上传图片文件**到飞书存储，获取 file_token
2. **更新记录**，将 file_token 写入"生成图片"附件字段

**不能只更新文本字段！必须上传实际图片文件！**

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

### 检查环境配置

```bash
cp .env.example .env
# 然后填写 LARK_APP_ID / LARK_APP_SECRET / LARK_BITABLE_APP_TOKEN 等变量
```

确保 `config.py` 可从环境变量读取飞书凭证和表格信息。

---

## 核心功能

### 功能 1: 从飞书获取待生成记录

```bash
cd "."
source .env

# 获取 Token
TOKEN=$(curl -s "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$LARK_APP_ID\", \"app_secret\": \"$LARK_APP_SECRET\"}" | jq -r '.tenant_access_token')

# 查询未生成的记录
curl -s "https://open.feishu.cn/open-apis/bitable/v1/apps/$LARK_BITABLE_APP_TOKEN/tables/$LARK_BITABLE_TABLE_ID/records?page_size=100" \
  -H "Authorization: Bearer $TOKEN" > /tmp/feishu_records.json
```

### 功能 2: 生成海报

**流程：**
1. 读取模板设计规范 `zodiac-poster/assets/templates/{模板ID}/TEMPLATE.md`
2. AI 根据规范生成 HTML（包含智能排版和重点色标记）
3. 保存 HTML 到 `/tmp/`
4. 使用仓库内截图脚本 `../_shared/scripts/poster_screenshot.py` 生成 PNG
5. 保存图片到 `output/{YYYY}/{MM}/{DD}/{星座}-{标题}-{时间戳}/`
6. 将生成结果回传到飞书附件字段

**当前可用模板：**

| 模板 | ID | 重点色 | 说明 |
|------|-----|--------|------|
| 编辑暖调 | `editorial-warm` | `#C15F3C` | 编辑杂志风格，带引用块和页码 |
| 极简暖调 | `minimal-warm` | `#C8725A` | 极简居中布局，大留白，适合封面 |
| 动态编辑风 | `editorial-dynamic` | `#C15F3C` | 4种风格包 × 5种布局变体，随机组合 |

### ⚠️ 封面与内容页风格一致性（重要！）

**生成套图时，封面和所有内容页必须使用相同的风格包：**

| 套图序号 | 风格包 | 封面装饰 | 内容页装饰 |
|---------|--------|----------|-----------|
| 1 | 经典强调 | 圆形装饰、年份背景大字 | 圆形装饰、填色关键词 |
| 2 | 简约边框 | 角标装饰、竖线 | 角标装饰、边框关键词 |
| 3 | 杂志双线 | 双线边框、星星散布 | 双线边框、双线关键词 |
| 4 | 艺术镂空 | 镂空装饰、渐变线 | 镂空装饰、镂空关键词 |

**随机分配规则：**
- 不同记录使用不同风格包（按记录索引轮换）
- 同一套图内封面和内容页必须使用相同风格包
- 在 HTML 开头添加 `<!-- [STYLE LOCK: 风格包名称] [LAYOUT LOCK: 布局] -->` 标记

### 🔴 封面重点色词规则（最重要！必须遵守！）

> **⚠️ 这是最常见的错误！生成封面前务必检查！**

**封面必须包含至少 2 个重点色词（`<span class="accent">词</span>`），形成视觉呼应！**

| 位置 | 要求 | 正确示例 |
|------|------|----------|
| 主标题 (h1) | **必须**包含 1-2 个 | `少一点<span class="accent">期待</span>` |
| 副标题 (sub-title) | **必须**包含 1 个 | `多一点<span class="accent">随缘</span>` |

**🎯 重点色词选择策略：**

| 文案类型 | 选择策略 | 示例 |
|----------|----------|------|
| 对比句 | 标记对比的两个核心词 | `<span class="accent">期待</span>` vs `<span class="accent">随缘</span>` |
| 情感句 | 标记情感词 + 结果词 | `<span class="accent">欢迎</span>` + `<span class="accent">强留</span>` |
| 描述句 | 标记形容词 + 名词 | `<span class="accent">热情</span>` + `<span class="accent">无情</span>` |

**❌ 错误示例（0个重点色词）：**
```html
<h1 class="main-title">少一点期待<br/>多一点随缘</h1>
<p class="sub-title">射手座的2026新年愿望</p>
<!-- 问题：全是黑/灰文字，没有任何重点色！ -->
```

**✅ 正确示例（2个重点色词）：**
```html
<h1 class="main-title">少一点<span class="accent">期待</span><br/>多一点<span class="accent">随缘</span></h1>
<p class="sub-title">射手座的2026新年愿望</p>
<!-- 或者：副标题也加重点色 -->
<p class="sub-title">射手座的<span class="accent">2026</span>新年愿望</p>
```

**✅ 更多正确示例：**
```html
<!-- 年度总结 -->
<h1 class="main-title">来的都<span class="accent">欢迎</span><br/>走的不<span class="accent">强留</span></h1>
<p class="sub-title">射手座的2025年度总结</p>

<!-- 情感类 -->
<h1 class="main-title">不是<span class="accent">无情</span><br/>是<span class="accent">热情</span>用完了</h1>
<p class="sub-title">懒得再装了</p>
```

**🚨 生成封面检查清单：**
- [ ] 主标题中是否有至少1个 `<span class="accent">词</span>`？
- [ ] 副标题或主标题第二行是否有另一个 `<span class="accent">词</span>`？
- [ ] 两个重点色词是否形成呼应（对比/递进/因果）？

### 🔴 内容页重点色呼应对（必须遵守！）

> **⚠️ 内容页必须有 2 个重点色词形成语义呼应！单个重点色词视为不合格！**

**内容页必须包含 2 个重点色词，形成呼应对！**

| 位置 | 要求 | 样式 |
|------|------|------|
| 正文中 | **必须 2 个呼应对** | `<span class="accent">词1</span>` ... `<span class="accent">词2</span>` |
| 引用/金句 | 可选 0-1 个 | 同上 |

**🎯 呼应对类型（AI 智能判断）：**

| 类型 | 说明 | 示例 |
|------|------|------|
| **因果呼应** | 原因 → 结果 | `<span class="accent">囤货和冲动消费</span>` → `<span class="accent">只剩心虚</span>` |
| **对比呼应** | A vs B | `<span class="accent">买的时候爽</span>` → `<span class="accent">看账单心疼</span>` |
| **递进呼应** | 从弱到强 | `<span class="accent">不在乎贵不贵</span>` → `<span class="accent">只在乎值不值</span>` |
| **转折呼应** | 预期 vs 实际 | `<span class="accent">本想省钱</span>` → `<span class="accent">结果更亏</span>` |

**🤖 AI 智能判断流程：**

1. **断句分析**：将正文按句拆分
2. **找关系信号词**：
   - 有"但/却/结果/只剩/反而"等词 → 转折/因果
   - 有"不是...而是"结构 → 对比
   - 有"越...越"结构 → 递进
3. **定位呼应对**：
   - 第一个词：原因/前提/表面（通常在前半段）
   - 第二个词：结果/转折/本质（通常在后半段）
4. **验证呼应关系**：两个词是否形成完整的语义闭环

**❌ 错误示例（只有1个重点色词）：**
```html
<div class="content-text">
  <p><span class="accent">囤货和冲动消费</span>是大忌</p>
  <p>买的时候爽</p>
  <p>回头看账单只剩心虚</p>
</div>
<!-- 问题："只剩心虚"没有标记，缺少呼应！ -->
```

**✅ 正确示例（2个重点色词形成呼应）：**
```html
<div class="content-text">
  <p><span class="accent">囤货和冲动消费</span>是大忌</p>
  <p>买的时候爽</p>
  <p>回头看账单<span class="accent">只剩心虚</span></p>
</div>
<!-- "囤货和冲动消费"(原因) → "只剩心虚"(结果) 形成因果呼应 -->
```

**🚨 生成内容页检查清单：**
- [ ] 每张内容页是否有 **2 个** 重点色词？
- [ ] 2 个重点色词是否形成呼应对（因果/对比/递进/转折）？
- [ ] 重点色词是否标记了情感核心（而非主题词）？

### 🔴 总结页重点色词规则（必须遵守！）

**总结页必须包含至少 1 个重点色词，与封面首尾呼应！**

| 位置 | 要求 | 示例 |
|------|------|------|
| 总结正文 | **必须** 1-2 个 | `不如追求<span class="accent">体验多少</span>` |
| 结尾祝语 | 可选 0-1 个 | `愿你的每一笔消费都有<span class="accent">记忆点</span>` |

**✅ 正确示例：**
```html
<div class="summary-text">
  <p>与其追求拥有多少</p>
  <p>不如追求<span class="accent">体验多少</span></p>
  <p>花对了地方</p>
  <p>快乐自然会来</p>
</div>
```

**🚨 总结页检查清单：**
- [ ] 总结页是否有至少 1 个重点色词？
- [ ] 重点色词是否与封面的核心词形成首尾呼应？

### 🎯 总结页规则（最后一页使用 Layout S）

> **套图的最后一页必须使用「总结收尾式」布局 (Layout S)！**

**总结页特征：**
- 布局标记：`[LAYOUT LOCK: S]`（最后一页专用）
- 内容水平居中
- 独立的视觉风格：大引号装饰 + 标题下划线 + 结束星星

**生成最后一页时：**
1. 使用 `.main-summary` 作为主容器
2. 使用 `.summary-title` 作为标题
3. 使用 `.summary-content` 作为正文
4. 添加 `.summary-end` 结束装饰

**HTML 结构：**
```html
<!-- 最后一页使用 Layout S -->
<div class="summary-quote">❝</div>
<div class="main-summary">
  <h2 class="summary-title">这就是双子</h2>
  <p class="summary-content">
    来的都是<span class="accent">缘分</span>，<br/>
    留下的才是真心。<br/><br/>
    这就是双子座。
  </p>
  <div class="summary-end">
    <span class="end-star"></span>
  </div>
</div>
```

**🚨 生成总结页检查清单：**
- [ ] 最后一页是否使用了 `[LAYOUT LOCK: S]` 标记？
- [ ] 是否使用了 `.main-summary` 容器？
- [ ] 内容是否水平居中？
- [ ] 是否有结束装饰符 `.summary-end`？

### 功能 3: 回传飞书（⚠️ 必须执行）

**方式一：使用工具脚本（推荐）**

```bash
cd "."
./scripts/feishu_upload.sh <record_id> <image_dir>

# 示例
./scripts/feishu_upload.sh recv6ycsM6G5kD "./output/2025/12/27/射手座-孽缘星座-251227"
```

**方式二：手动执行 API 调用**

```bash
cd "."
source .env

RECORD_ID="<记录ID>"
IMAGE_DIR="<图片目录>"

# 1. 获取 Token
TOKEN=$(curl -s "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$LARK_APP_ID\", \"app_secret\": \"$LARK_APP_SECRET\"}" | jq -r '.tenant_access_token')

# 2. 上传每张图片（必须！）
for img in "$IMAGE_DIR"/*.png; do
  filename=$(basename "$img")
  filesize=$(stat -f%z "$img")

  # 上传到飞书存储
  curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all" \
    -H "Authorization: Bearer $TOKEN" \
    -F "file_name=$filename" \
    -F "parent_type=bitable_file" \
    -F "parent_node=$LARK_BITABLE_APP_TOKEN" \
    -F "size=$filesize" \
    -F "file=@$img"

  # 记录返回的 file_token
done

# 3. 更新记录（包含附件字段！）
curl -s -X PUT "https://open.feishu.cn/open-apis/bitable/v1/apps/$LARK_BITABLE_APP_TOKEN/tables/$LARK_BITABLE_TABLE_ID/records/$RECORD_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "已生成": true,
      "生成图片路径": "<IMAGE_DIR>",
      "生成图片": [
        {"file_token": "<token1>"},
        {"file_token": "<token2>"},
        ...
      ]
    }
  }'
```

---

## 飞书多维表格字段（素材库）

| 序号 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 1 | 标题 | 文本 | 海报主标题 |
| 2 | 副标题 | 文本 | 海报副标题 |
| 3 | 正文内容 | 文本 | 内容页正文 |
| 4 | 小红书文案 | 文本 | 发布用文案 |
| 5 | 分类 | 单选 | 每日运势/节日节点/日常更新/依恋类型/MBTI |
| 6 | 用途 | 单选 | 封面布局/长文案布局/套图 |
| 7 | 模板 | 文本 | 模板名称 |
| 8 | 星座 | 单选 | 12 星座 |
| 9 | 依恋类型 | 单选 | 安全型/焦虑型/回避型/混乱型 |
| 10 | MBTI | 单选 | 16种人格类型 |
| 11 | 已生成 | 复选框 | 生成状态 |
| 12 | 已发布 | 复选框 | 发布状态 |
| 13 | **生成图片** | **附件** | **上传的图片（必须回传！）** |
| 14 | 生成图片路径 | 文本 | 本地路径 |
| 15 | 父记录 | 单向关联 | 自关联（套图父子关系） |

---

## 完整生成流程（重要！）

```
用户: 从飞书拉取待生成的海报

Claude 执行:
1. 读取 .env 获取飞书配置
2. 调用飞书 API 查询记录
3. 遍历每条记录:
   a. 读取模板规范
   b. AI 生成 HTML
   c. 保存 HTML 到 /tmp/ 或 output 目录

   ⚠️ 【必须】使用独立截图工具（避免 MCP 浏览器抢占）:
   d. 执行截图脚本:
      ```bash
      # 批量模式（推荐，一套图多页时浏览器只启动一次）
      python3 ./_shared/scripts/poster_screenshot.py \
          --batch /tmp/html_dir/ /path/to/output/

      # 或单文件模式
      python3 ./_shared/scripts/poster_screenshot.py \
          /tmp/cover.html /path/to/output/cover.png
      ```

   工具自动处理：viewport 1080x1440、字体加载等待、截取 .poster 元素

   ⚠️ 【必须】防止深色模式：
   生成的 HTML 必须在 CSS 开头包含以下样式：
   ```css
   :root, html, body {
     color-scheme: light only;
     background: #FAF6F1;
   }
   ```
   否则系统深色模式会导致背景变成深灰色！

   ⚠️ 【必须】回传飞书:
   e. 上传所有图片到飞书存储，获取 file_token
   f. 更新记录:
      - 已生成 = true
      - 生成图片路径 = <目录路径>
      - 生成图片 = [file_tokens...]  ← 必须包含附件！

4. 汇报生成结果
```

---

## 输出位置

```
./output/{YYYY}/{MM}/{DD}/
└── {星座}-{标题缩写}-{YYMMDD}-{HHMM}/
    ├── 01-cover.png     # 封面
    ├── 02-xxx.png       # 内容页1
    ├── 03-xxx.png       # 内容页2
    └── ...
```

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `.env` | 飞书配置 |
| `scripts/feishu_upload.sh` | **图片上传工具脚本** |
| `zodiac-poster/assets/templates.json` | 模板配置 |
| `zodiac-poster/assets/templates/*.md` | 模板设计规范 |

---

## ⚠️ 发布到小红书后标记已发布（重要！）

**如果从飞书拉取的记录被发布到小红书，必须立即将该记录标记为「已发布」。**

### 触发条件

当以下情况发生时，必须执行标记操作：
1. 用户要求"从飞书拉取xxx并发布到小红书"
2. 用户要求"发布飞书记录到小红书"
3. 任何涉及飞书记录 + 小红书发布的操作

### 标记方式

**方式一：使用工具脚本（推荐）**

```bash
cd "."
./scripts/feishu_mark_published.sh <record_id> "<发布的文案>"

# 示例
./scripts/feishu_mark_published.sh recv6Gc0wjHbf9 "射手座的感情..."
```

**方式二：直接调用 MCP API**

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_update
参数:
- path: { app_token, table_id, record_id }
- data: {
    fields: {
      "已发布": true,
      "小红书文案": "<实际发布的文案>"
    }
  }
```

### 完整流程（从飞书拉取 → 发布小红书 → 标记已发布）

```
1. 从飞书拉取记录
   └── 保存 record_id（重要！）

2. 生成/获取图片
   └── 从飞书下载或本地生成

3. 准备文案
   ├── 使用飞书"小红书发送文案"字段
   └── 或 AI 生成新文案

4. ⚠️ 自动生成话题标签
   ├── 分析文案内容
   └── 生成 3-5 个标签（如 ["射手座", "星座", "情感"]）

5. 发布到小红书
   ├── title + content + images + tags
   └── 确认发布成功

6. ⚠️ 立即标记飞书记录为已发布
   ├── "已发布" = true
   └── "小红书文案" = 实际发布的文案
```

### 注意事项

- **必须在发布成功后立即执行标记**，不要遗漏
- 如果标记失败，提示用户手动在飞书中勾选
- record_id 在拉取记录时就要保存，不要发布后再查询

---

## 错误处理

### 图片未回传到飞书

**症状**：飞书表格中"生成图片"字段为空

**原因**：只更新了文本字段，没有上传实际图片

**解决**：
```bash
# 使用工具脚本补传
./scripts/feishu_upload.sh <record_id> <image_dir>
```

### 飞书 API 调用失败

1. 检查 .env 配置是否正确
2. 检查 APP_ID 和 APP_SECRET 是否有效
3. 确认应用已开通多维表格和云文档权限

### 图片生成失败

1. 检查 Playwright MCP 是否正常
2. 确认 HTML 语法正确
3. 查看 /tmp/ 目录下的 HTML 文件

### 截图尺寸错误（不是 2160x2880）

**症状**：生成的图片尺寸是 1080×1440 而不是 2160×2880

**原因**：未设置 `device_scale_factor=2`

**解决**：使用独立截图工具，默认 2x 导出
```bash
python3 ./_shared/scripts/poster_screenshot.py \
    input.html output.png
```

**注意**：截图工具默认设置 viewport 为 1080x1440 + 2x 导出 = 实际像素 2160×2880
