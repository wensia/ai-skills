---
name: template-lint
description: |
  Visual QA tool for poster/card HTML templates - catches layout, typography, spacing, and alignment issues.
  Trigger this skill when the user wants to:
  - Check a template for layout problems, overlaps, or misalignment
  - Fix "something looks off" in a poster or card design
  - Optimize font sizes, line heights, or spacing consistency
  - Verify export quality (pixel alignment, font embedding)
  - Run a full visual inspection on HTML/SVG poster templates
  - Debug why icons look inconsistent or headers collide
  Keywords: 体检, lint, 检查模板, 排版, 对齐, 间距, 布局, template check, visual QA
---

# Template Lint - 图文模板体检工具

对 HTML/SVG 海报模板进行全面的视觉体检，发现并修复布局、排版、对齐、间距等问题。

---

## 使用方式

### 完整体检（推荐）

提供截图或 HTML 文件，执行全部 8 项检查（A → H）。

### 针对性检查

指定检查项进行专项体检：

```
帮我检查这个模板的字体排版问题（Skill B）
帮我看看图标间距为什么不对劲（Skill D）
检查标题区域是否会发生重叠（Skill E）
```

---

## 体检项目总览

| ID | 名称 | 检查什么 | 严重级别 |
|----|------|----------|----------|
| A | Layout Lint | 安全区、重叠、对齐、组关系 | Critical |
| B | Typography Lint | 字号层级、混排、字距、行距 | Major |
| C | Baseline Alignment | 数字+符号基线、中英混排 | Major |
| D | Spacing Consistency | 同组元素是否等距 | Major |
| E | Header Collision Guard | 标题文本不重叠、安全区 | Critical |
| F | Grid & Rhythm | 8pt网格、垂直节奏 | Minor |
| G | Icon Consistency | 线宽、端点、风格统一 | Minor |
| H | Export QA | 像素对齐、字体嵌入 | Major |

各检查项的详细输出格式示例见 [references/skill-details.md](references/skill-details.md)。
完整体检流程图和报告模板见 [references/report-template.md](references/report-template.md)。

---

## Skill A：Layout Lint（布局体检）

扫描重叠、边距、安全区、对齐漂移、组间节奏混乱。

**输入**：截图/导出图（PNG/JPG）或 HTML/SVG 文件，画布尺寸（默认 1080x1440）

### 检查项

#### 1. 安全区检查

| 检查点 | 标准 | 容差 |
|--------|------|------|
| 四边留白一致性 | 左右边距相等，上下边距相等 | ±5px |
| 顶部标题区 | 距顶部 ≥80px | - |
| 底部页脚区 | 距底部 ≥60px | - |
| 内容区边界 | x: 80~1000, y: 100~1340 | - |

#### 2. 重叠检查

| 检查点 | 标准 |
|--------|------|
| 文本与文本 | 任意两个文本元素不得覆盖 |
| 文本与图标 | 最小间距 ≥8px |
| 装饰与内容 | 装饰元素不得遮挡核心内容 |

#### 3. 对齐检查

检测视觉居中 vs 数学居中（大写字母、数字需光学微调），组内对齐基准一致性，跨组参考线对齐。

#### 4. 组关系检查

- 对齐基准：left / center / baseline 三选一
- 组内间距统一
- 组间间距 ≥ 组内间距 × 1.5（确保层级区分）

---

## Skill B：Typography Lint（字体排版体检）

检查字号梯度、字距/行距、粗细、中英文混排。

### 字号层级

| 层级 | 推荐字号 | 字重 | 用途 |
|------|----------|------|------|
| H1 | 56-72px | 600-700 | 主标题 |
| H2 | 36-48px | 500-600 | 章节标题 |
| H3 | 28-32px | 400-500 | 副标题/强调 |
| Body | 24-32px | 400 | 正文 |
| Caption | 18-24px | 300-400 | 说明/注释 |

相邻层级字号比应 ≥1.25（推荐 1.33），否则层级感模糊。

### 中英文混排

- 基线统一：中英文基线对齐
- 英文字距：letter-spacing: 0.02-0.05em
- 字体配对：中文宋体配英文 serif，中文黑体配英文 sans-serif

### 行距与字距

| 元素 | 推荐行距 | 推荐字距 |
|------|----------|----------|
| 标题 | 1.1-1.3 | 0.05-0.1em |
| 正文 | 1.6-1.8 | 0-0.02em |
| 中文 | 1.8-2.0 | 0.05-0.1em |
| 英文大写 | 1.2 | 0.1-0.2em |

---

## Skill C：Baseline & Optical Alignment（基线与光学对齐）

专治"85%的字符不在同一水平线"问题。

### 对齐策略

- **同基线对齐**：适用于字号相同或相近的混排
- **光学对齐**：适用于字号差异大导致视觉跳动，通过 `dy` 属性补偿

### 常见组合修正表

| 组合 | 问题 | 修正值 |
|------|------|--------|
| `85` + `%` | % 视觉偏高 | % 下移 2-4px |
| `MATCH` + `INDEX` | 全大写间距 | letter-spacing +2px |
| `2026` + `年` | 数字偏高 | 年上移 1-2px |
| `♈` + `白羊座` | 符号偏大 | 符号缩放 0.85 |
| `∞` + 文字 | 符号居中偏 | ∞ 下移 3-5px |

---

## Skill D：Spacing Consistency（间距一致性）

专治"三个图标间距不一样"问题。

### 等距策略

- **中心点等分**：图标大小相同时，按中心点等距分布
- **外接框等分**：元素大小不一时，按边缘间距等分

### 光学补偿

当图标视觉重量不同时需微调：圆形图标比方形图标视觉上偏大，需要 1-3px 补偿。

### 检查流程

1. 测量所有同组元素的 x/y 坐标
2. 计算间距 = 后一个中心点 - 前一个中心点
3. 所有间距误差 ≤3px 视为合格
4. 视觉检查是否看起来等距

---

## Skill E：Header Collision Guard（标题防撞）

防止标题区域文字重叠或挤压。

| 规则 | 标准值 | 高密度可降至 |
|------|--------|--------------|
| 标题区最小间距 | ≥12px | 8px |
| 标题容器高度 | 120-160px | 100px |
| 安全区顶部 | ≥80px | 60px |

### 文案长度适配

| 策略 | 触发条件 | 实现方式 |
|------|----------|----------|
| 自动换行 | 单行超出容器宽度 | `<br>` 或 `tspan` 分行 |
| 副标题缩放 | 主标题过长 | font-size 缩放 90%-100% |
| 截断 | 超出最大字数 | 仅产品明确允许时使用 |

---

## Skill F：Grid & Rhythm（网格与节奏）

让整张图的"呼吸感"稳定。使用 8pt 网格保证间距有理可依，而非凭感觉。

### 8pt 网格间距

| 间距名 | 值 | 用途 |
|--------|-----|------|
| xs | 8px | 紧凑间距 |
| sm | 16px | 组内间距 |
| md | 24px | 标准间距 |
| lg | 32px | 区块间距 |
| xl | 48px | 大区块间距 |
| xxl | 64px | 主要分隔 |

### 垂直节奏

所有垂直间距应落在网格倍数上（±2px 容差可接受）。

### 中心轴规范

| 布局类型 | 中心轴 | 内容块宽度 |
|----------|--------|------------|
| 居中布局 | x=540 | 800-900px |
| 左对齐 | x=100 | 880px |
| 右对齐 | x=980 | 880px |

---

## Skill G：Icon Style Consistency（图标风格一致性）

图标线宽、圆角、端点风格不统一会让设计显得粗糙。

### 检查项

| 属性 | 推荐值 |
|------|--------|
| 线宽 | 所有图标 stroke-width 一致（推荐 1.5-2px） |
| 端点 | stroke-linecap: round |
| 拐角 | stroke-linejoin: round |
| 大小 | 同组图标尺寸比例 ±5% |
| 颜色 | 同组图标颜色统一或有序 |

---

## Skill H：Export QA（导出验收）

避免"编辑器里看着齐，导出后线条发虚"的问题。

### 像素对齐

- 坐标取整到整数（0.5px 坐标导致线条发虚）
- 使用偶数宽度（奇数宽度居中后产生 0.5px 偏移）
- transform 中的位移四舍五入

### 字体处理

| 平台 | 策略 |
|------|------|
| Web | 确保 @import 或 @font-face 正确加载 |
| 导出 PNG | 等待字体加载（≥2秒） |
| 矢量 | 转曲（text → path） |

### 导出规格

| 用途 | 倍率 | 尺寸 | 格式 |
|------|------|------|------|
| 预览 | 1x | 1080x1440 | PNG |
| 小红书 | 2x | 2160x2880 | PNG |
| 印刷 | 3x | 3240x4320 | PNG/PDF |

### 验收截图点位

检查以下位置是否清晰：左上角边界、标题区字体渲染、图标区线条、页脚小字、渐变边界。

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [references/skill-details.md](references/skill-details.md) | 各检查项详细输出格式示例 |
| [references/report-template.md](references/report-template.md) | 完整流程图和报告模板 |
