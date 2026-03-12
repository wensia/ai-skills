# 命定之约风 (Destined Bond) SVG 模板规范

**格式**：纯 SVG（不使用 HTML/CSS）
**特征**：居中对称布局 + 无限符号装饰 + 暖棕配色 + 配对指数突出展示
**适用**：星座配对、CP分析、缘分解读、关系解析

---

## 配色系统

| 用途 | 色值 | SVG属性 |
|------|------|---------|
| **主强调色** | `#B86B4A` | fill / stroke |
| **辅助强调色** | `#8B7355` | fill / stroke |
| **主文字** | `#4A3F35` | fill |
| **次要文字** | `#7D7067` | fill |
| **分隔线/装饰** | `#D4C9BE` | stroke |

### 背景渐变定义

```svg
<defs>
  <!-- 主背景渐变 (165度) -->
  <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#FDF8F4"/>
    <stop offset="50%" stop-color="#F8EDE5"/>
    <stop offset="100%" stop-color="#F2E4D8"/>
  </linearGradient>

  <!-- 光照叠加层 -->
  <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/>
    <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
    <stop offset="80%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
  </linearGradient>
</defs>
```

---

## 字体加载

```svg
<defs>
  <style>
    /* 中文字体仍使用 Google Fonts CDN */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
  </style>
</defs>
```

**注意**：封面和结尾页的配对指数百分比使用 `Times New Roman` 字体（等高数字）。

---

## 尺寸规范

**画布**：1080px × 1440px

| 元素 | 尺寸 | 说明 |
|------|------|------|
| 左右边距 | 100px | 内容区 x: 100 ~ 980 |
| 上下边距 | 90px | 内容区 y: 90 ~ 1350 |
| **封面配对指数** | **96px** | Times New Roman, 视觉核心 |
| 封面星座配对 | 56px | font-weight: 600 |
| 封面主题词 | 48px | font-weight: 600 |
| 章节标题 | 56px | font-weight: 600 |
| 正文 | 32px | line-height: 61px |
| 引用文字 | 26px | font-style: italic |
| 结尾页配对指数 | 72px | Times New Roman |
| 结尾页总结文字 | 28px | |
| 页码 | 24-28px | font-family: Georgia |

---

## 核心设计元素

### 1. 顶部装饰 - 无限符号（封面/结尾页专用）

```svg
<g id="top-decoration" transform="translate(540, 120)">
  <path d="M-20,0 C-20,-12 -8,-12 0,0 C8,12 20,12 20,0 C20,-12 8,-12 0,0 C-8,12 -20,12 -20,0"
        fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.4"/>
</g>
```

### 2. 分隔装饰 - 小无限符号

```svg
<g transform="translate(0, {{Y_POSITION}})">
  <line x1="-80" y1="0" x2="-25" y2="0" stroke="#D4C9BE" stroke-width="1"/>
  <path d="M-12,0 C-12,-7 -5,-7 0,0 C5,7 12,7 12,0 C12,-7 5,-7 0,0 C-5,7 -12,7 -12,0"
        fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
  <line x1="25" y1="0" x2="80" y2="0" stroke="#D4C9BE" stroke-width="1"/>
</g>
```

### 3. 页眉结构（内页专用）

```svg
<g id="header">
  <!-- 星座配对名 -->
  <text x="100" y="130"
        font-family="Noto Serif SC, serif"
        font-size="32"
        font-weight="500"
        fill="#B86B4A"
        letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>

  <!-- 分隔符 -->
  <text x="360" y="130"
        font-family="Georgia, serif"
        font-size="24"
        fill="#D4C9BE">·</text>

  <!-- 主题词 -->
  <text x="385" y="130"
        font-family="Noto Sans SC, sans-serif"
        font-size="24"
        font-weight="300"
        fill="#7D7067"
        letter-spacing="3">命定之约</text>

  <!-- 右上角装饰：小无限符号 -->
  <g transform="translate(940, 110)">
    <path d="M-15,0 C-15,-10 -5,-10 0,0 C5,10 15,10 15,0 C15,-10 5,-10 0,0 C-5,10 -15,10 -15,0"
          fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
  </g>
</g>
```

### 4. 页脚结构

```svg
<g id="footer">
  <!-- 分隔线 -->
  <line x1="100" y1="1350" x2="980" y2="1350"
        stroke="#D4C9BE" stroke-width="1.5"/>

  <!-- 页码 -->
  <text x="980" y="1388"
        font-family="Georgia, serif"
        font-size="24"
        fill="#7D7067"
        text-anchor="end"
        letter-spacing="6">{{PAGE_NUM}}</text>
</g>
```

---

## 封面模板

**特点**：无页眉、全居中布局、配对指数为视觉核心（96px大字）

```svg
<!-- [STYLE: 命定之约风] [TYPE: cover] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      /* 中文字体仍使用 Google Fonts CDN */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDF8F4"/>
      <stop offset="50%" stop-color="#F8EDE5"/>
      <stop offset="100%" stop-color="#F2E4D8"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>

  <!-- 顶部装饰 - 简化的无限符号 -->
  <g id="top-decoration" transform="translate(540, 120)">
    <path d="M-20,0 C-20,-12 -8,-12 0,0 C8,12 20,12 20,0 C20,-12 8,-12 0,0 C-8,12 -20,12 -20,0"
          fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.4"/>
  </g>

  <!-- 主视觉区域 - 居中的星座配对 -->
  <g id="hero-section" transform="translate(540, 0)">
    <!-- 英文副标题 -->
    <text x="0" y="320" font-family="Georgia, serif" font-size="20" fill="#8B7355" text-anchor="middle" letter-spacing="8">DESTINED BOND</text>

    <!-- 主标题：星座配对 (视觉核心) -->
    <text x="0" y="420" font-family="Noto Serif SC, serif" font-size="56" font-weight="600" fill="#B86B4A" text-anchor="middle" letter-spacing="6">{{ZODIAC1}} × {{ZODIAC2}}</text>

    <!-- 中文副标题 -->
    <text x="0" y="490" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#7D7067" text-anchor="middle" letter-spacing="4">命定之约</text>
  </g>

  <!-- 配对指数区域 -->
  <g id="match-section" transform="translate(540, 0)">
    <!-- 装饰线 -->
    <line x1="-60" y1="560" x2="60" y2="560" stroke="#D4C9BE" stroke-width="1"/>

    <!-- 标签 -->
    <text x="0" y="620" font-family="Noto Sans SC, sans-serif" font-size="20" font-weight="400" fill="#8B7355" text-anchor="middle" letter-spacing="4">契合指数</text>

    <!-- 百分比 (视觉核心) -->
    <text x="0" y="710" font-family="Times New Roman, Times, serif" font-size="96" font-weight="600" fill="#B86B4A" text-anchor="middle" letter-spacing="4">{{MATCH_PERCENT}}%</text>
  </g>

  <!-- 主题概念 -->
  <g id="concept-section" transform="translate(540, 0)">
    <!-- 分隔装饰 -->
    <g transform="translate(0, 820)">
      <line x1="-80" y1="0" x2="-25" y2="0" stroke="#D4C9BE" stroke-width="1"/>
      <path d="M-12,0 C-12,-7 -5,-7 0,0 C5,7 12,7 12,0 C12,-7 5,-7 0,0 C-5,7 -12,7 -12,0"
            fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
      <line x1="25" y1="0" x2="80" y2="0" stroke="#D4C9BE" stroke-width="1"/>
    </g>

    <!-- 主题词 -->
    <text x="0" y="920" font-family="Noto Serif SC, serif" font-size="48" font-weight="600" fill="#4A3F35" text-anchor="middle" letter-spacing="12">{{THEME_TITLE}}</text>

    <!-- 描述 -->
    <text x="0" y="985" font-family="Noto Serif SC, serif" font-size="24" fill="#7D7067" text-anchor="middle" letter-spacing="4">{{THEME_DESC}}</text>
  </g>

  <!-- 标语 -->
  <g id="tagline" transform="translate(540, 0)">
    <text x="0" y="1100" font-family="Noto Serif SC, serif" font-size="24" fill="#7D7067" text-anchor="middle" letter-spacing="2">{{TAGLINE_LINE1}}</text>
    <text x="0" y="1150" font-family="Noto Serif SC, serif" font-size="24" text-anchor="middle" letter-spacing="2">
      <tspan fill="#B86B4A">{{TAGLINE_HIGHLIGHT}}</tspan><tspan fill="#7D7067">{{TAGLINE_REST}}</tspan>
    </text>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4C9BE" stroke-width="1.5"/>
    <text x="980" y="1388" font-family="Georgia, serif" font-size="24" fill="#7D7067" text-anchor="end" letter-spacing="6">01</text>
  </g>
</svg>
```

### 封面变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC1}}` | 星座1名 | 射手座 |
| `{{ZODIAC2}}` | 星座2名 | 狮子座 |
| `{{MATCH_PERCENT}}` | 配对指数 | 85 |
| `{{THEME_TITLE}}` | 主题词 | 命中注定 |
| `{{THEME_DESC}}` | 主题描述 | 火象最佳CP |
| `{{TAGLINE_LINE1}}` | 标语第一行 | 两个人在一起 |
| `{{TAGLINE_HIGHLIGHT}}` | 标语高亮 | 发光发热 |
| `{{TAGLINE_REST}}` | 标语剩余 | ，谁也不用收敛 |

---

## 内页模板

**特点**：有页眉、左对齐布局、BOND标签、引用区块

```svg
<!-- [STYLE: 命定之约风] [TYPE: page] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDF8F4"/>
      <stop offset="50%" stop-color="#F8EDE5"/>
      <stop offset="100%" stop-color="#F2E4D8"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>

  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#B86B4A" letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>
    <text x="360" y="130" font-family="Georgia, serif" font-size="24" fill="#D4C9BE">·</text>
    <text x="385" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#7D7067" letter-spacing="3">命定之约</text>
    <g transform="translate(940, 110)">
      <path d="M-15,0 C-15,-10 -5,-10 0,0 C5,10 15,10 15,0 C15,-10 5,-10 0,0 C-5,10 -15,10 -15,0" fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
    </g>
  </g>

  <!-- 章节标签 -->
  <text x="100" y="220" font-family="Georgia, serif" font-size="24" fill="#B86B4A" letter-spacing="6">BOND {{PART_NUM}}</text>

  <!-- 章节标题 -->
  <text x="100" y="310" font-family="Noto Serif SC, serif" font-size="56" font-weight="600" fill="#4A3F35" letter-spacing="4">{{SECTION_TITLE}}</text>

  <!-- 分隔线 -->
  <rect x="100" y="340" width="80" height="3" fill="#B86B4A"/>

  <!-- 正文内容 -->
  <g id="content" transform="translate(100, 520)">
    {{CONTENT_LINES}}
  </g>

  <!-- 引用区块 -->
  <g id="quote" transform="translate(100, 1050)">
    <!-- 左边框 -->
    <line x1="0" y1="0" x2="0" y2="60" stroke="#B86B4A" stroke-width="3"/>
    <!-- 引用文字 -->
    <text x="30" y="40" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#7D7067" letter-spacing="2">"{{QUOTE}}"</text>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4C9BE" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#7D7067" text-anchor="end" letter-spacing="4">{{PAGE_NUM}}</text>
  </g>
</svg>
```

### 正文内容生成规则

**字体规范**：
| 属性 | 值 | 说明 |
|------|-----|------|
| 字体大小 | **32px** | 正文主字号 |
| 字间距 | **4px** | letter-spacing |
| 行间距 | **61px** | y 坐标递增值 |
| 主文字色 | **#4A3F35** | fill |
| 高亮色 | **#B86B4A** | fill |

#### 高亮标记语法

使用 `【词】` 标记需要高亮的词，生成脚本只负责解析标记，不做语义判断。

**示例**：
```
两个射手相遇
就像【照镜子】
哇这人好【懂】我
```

渲染结果：
```svg
<text y="0" ...><tspan fill="#4A3F35">两个射手相遇</tspan></text>
<text y="61" ...><tspan fill="#4A3F35">就像</tspan><tspan fill="#B86B4A">照镜子</tspan></text>
<text y="122" ...><tspan fill="#4A3F35">哇这人好</tspan><tspan fill="#B86B4A">懂</tspan><tspan fill="#4A3F35">我</tspan></text>
```

#### 内容页高亮规则

**每段正文高亮 2 个呼应词**，形成对比/递进/因果/转折关系：

| 类型 | 说明 | 示例 |
|------|------|------|
| 对比 | 两个词形成对比 | 【懂】vs【玩】、【走】vs【停】 |
| 递进 | 层层递进 | 【疯】→【更疯】 |
| 因果 | 原因和结果 | 因为【默契】所以【舒服】 |
| 转折 | 前后反差 | 虽然【硬】但【不记仇】 |

**原则**：
1. 每段只高亮2个呼应词
2. 两个词必须有语义关联
3. 避免连续高亮
4. 不是每行都要高亮

**每行文本模板**：
```svg
<text y="{{LINE_Y}}" font-family="Noto Serif SC, serif" font-size="32" letter-spacing="4">
  <tspan fill="#4A3F35">{{TEXT_BEFORE}}</tspan>
  <tspan fill="#B86B4A">{{HIGHLIGHT}}</tspan>
  <tspan fill="#4A3F35">{{TEXT_AFTER}}</tspan>
</text>
```

**行间距**：61px（y递增：0, 61, 122, 183, 244, 305...）

### 内页变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC1}}` | 星座1名 | 射手座 |
| `{{ZODIAC2}}` | 星座2名 | 狮子座 |
| `{{PART_NUM}}` | 章节编号 | 01 |
| `{{SECTION_TITLE}}` | 章节标题 | 初见时刻 |
| `{{CONTENT_LINES}}` | 正文内容 | 多行text元素 |
| `{{QUOTE}}` | 引用文字 | 火象的相遇，注定热烈 |
| `{{PAGE_NUM}}` | 页码 | 0 2 |

---

## 结尾页模板

**特点**：顶部无限符号、全居中布局、配对指数、总结要点、祝福语、END标记

```svg
<!-- [STYLE: 命定之约风] [TYPE: end] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      /* 中文字体仍使用 Google Fonts CDN */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDF8F4"/>
      <stop offset="50%" stop-color="#F8EDE5"/>
      <stop offset="100%" stop-color="#F2E4D8"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>

  <!-- 顶部装饰 -->
  <g id="top-decoration" transform="translate(540, 120)">
    <path d="M-20,0 C-20,-12 -8,-12 0,0 C8,12 20,12 20,0 C20,-12 8,-12 0,0 C-8,12 -20,12 -20,0"
          fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.4"/>
  </g>

  <!-- 主内容区域 -->
  <g id="main-content" transform="translate(540, 0)">

    <!-- 标题区：星座配对 -->
    <text x="0" y="280" font-family="Noto Serif SC, serif" font-size="42" font-weight="600" fill="#B86B4A" text-anchor="middle" letter-spacing="4">{{ZODIAC1}} × {{ZODIAC2}}</text>
    <text x="0" y="340" font-family="Noto Sans SC, sans-serif" font-size="20" font-weight="300" fill="#7D7067" text-anchor="middle" letter-spacing="6">命定之约</text>

    <!-- 分隔线 -->
    <line x1="-50" y1="400" x2="50" y2="400" stroke="#D4C9BE" stroke-width="1"/>

    <!-- 核心数据：契合指数 -->
    <g transform="translate(0, 500)">
      <text x="0" y="0" font-family="Noto Sans SC, sans-serif" font-size="18" font-weight="400" fill="#8B7355" text-anchor="middle" letter-spacing="4">契合指数</text>
      <text x="0" y="70" font-family="Times New Roman, Times, serif" font-size="72" font-weight="600" fill="#B86B4A" text-anchor="middle" letter-spacing="2">{{MATCH_PERCENT}}%</text>
    </g>

    <!-- 分隔装饰 -->
    <g transform="translate(0, 640)">
      <line x1="-60" y1="0" x2="-20" y2="0" stroke="#D4C9BE" stroke-width="1"/>
      <path d="M-10,0 C-10,-6 -4,-6 0,0 C4,6 10,6 10,0 C10,-6 4,-6 0,0 C-4,6 -10,6 -10,0"
            fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
      <line x1="20" y1="0" x2="60" y2="0" stroke="#D4C9BE" stroke-width="1"/>
    </g>

    <!-- 总结要点 -->
    <g id="summary" transform="translate(0, 720)">
      <text y="0" font-family="Noto Serif SC, serif" font-size="28" fill="#B86B4A" text-anchor="middle" letter-spacing="4">{{SUMMARY_HIGHLIGHT}}</text>
      <text y="60" font-family="Noto Serif SC, serif" font-size="28" text-anchor="middle" letter-spacing="2">
        <tspan fill="#4A3F35">{{SUMMARY_LINE1_BEFORE}}</tspan><tspan fill="#B86B4A">{{SUMMARY_LINE1_HIGHLIGHT}}</tspan>
      </text>
      <text y="120" font-family="Noto Serif SC, serif" font-size="28" fill="#4A3F35" text-anchor="middle" letter-spacing="2">{{SUMMARY_LINE2}}</text>
    </g>

    <!-- 分隔装饰 -->
    <g transform="translate(0, 920)">
      <line x1="-80" y1="0" x2="-25" y2="0" stroke="#D4C9BE" stroke-width="1"/>
      <path d="M-12,0 C-12,-7 -5,-7 0,0 C5,7 12,7 12,0 C12,-7 5,-7 0,0 C-5,7 -12,7 -12,0"
            fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
      <line x1="25" y1="0" x2="80" y2="0" stroke="#D4C9BE" stroke-width="1"/>
    </g>

    <!-- 祝福语 -->
    <g id="blessing" transform="translate(0, 1020)">
      <text y="0" font-family="Noto Serif SC, serif" font-size="24" font-style="italic" fill="#7D7067" text-anchor="middle" letter-spacing="2">{{BLESSING_LINE1}}</text>
      <text y="50" font-family="Noto Serif SC, serif" font-size="24" font-style="italic" fill="#7D7067" text-anchor="middle" letter-spacing="2">{{BLESSING_LINE2}}</text>
    </g>

    <!-- END 标记 -->
    <g id="end-mark" transform="translate(0, 1180)">
      <line x1="-60" y1="0" x2="-20" y2="0" stroke="#D4C9BE" stroke-width="1.5"/>
      <text x="0" y="6" font-family="Georgia, serif" font-size="18" fill="#B86B4A" text-anchor="middle" letter-spacing="6">END</text>
      <line x1="20" y1="0" x2="60" y2="0" stroke="#D4C9BE" stroke-width="1.5"/>
    </g>

  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4C9BE" stroke-width="1.5"/>
    <text x="980" y="1388" font-family="Georgia, serif" font-size="24" fill="#7D7067" text-anchor="end" letter-spacing="6">{{PAGE_NUM}}</text>
  </g>
</svg>
```

### 结尾页变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC1}}` | 星座1名 | 射手座 |
| `{{ZODIAC2}}` | 星座2名 | 狮子座 |
| `{{MATCH_PERCENT}}` | 配对指数 | 85 |
| `{{SUMMARY_HIGHLIGHT}}` | 总结高亮 | 火象最佳CP |
| `{{SUMMARY_LINE1_BEFORE}}` | 总结行1前半 | 一起 |
| `{{SUMMARY_LINE1_HIGHLIGHT}}` | 总结行1高亮 | 发光发热 |
| `{{SUMMARY_LINE2}}` | 总结行2 | 谁也不用收敛自己 |
| `{{BLESSING_LINE1}}` | 祝福语行1 | 愿你遇到的狮子 |
| `{{BLESSING_LINE2}}` | 祝福语行2 | 都愿意和你一起发光 |
| `{{PAGE_NUM}}` | 页码 | 03 |

---

## 章节标题建议

| 章节 | 标题示例 |
|------|----------|
| BOND 01 | 初见时刻 / 第一眼 |
| BOND 02 | 相处模式 / 一起疯的时候 |
| BOND 03 | 争执瞬间 / 吵架的时候 |
| BOND 04 | 心动时刻 / 最甜的瞬间 |
| BOND 05 | 挑战关卡 / 最难的时刻 |

---

## 高亮词规则

### 封面（1-2个）
- 标语中1个高亮词
- 使用 `fill="#B86B4A"`

### 内页（2个呼应对）
- 使用 `<tspan fill="#B86B4A">` 包裹高亮词
- 两个词形成语义呼应

### 结尾页（2-3个）
- 总结高亮 + 总结行高亮
- 与封面形成首尾呼应

---

## 检查清单

### 基础检查
- [ ] 画布尺寸 1080×1440
- [ ] 背景渐变定义正确（暖棕色系）
- [ ] 配对指数使用 Times New Roman（系统字体，无需 @import）
- [ ] 页脚分隔线 + 右对齐页码

### 封面专项检查
- [ ] **无页眉**
- [ ] 顶部有无限符号装饰
- [ ] 配对指数使用 96px Times New Roman
- [ ] 有分隔装饰（小无限符号）
- [ ] 主题词 48px 居中

### 内页专项检查
- [ ] 页眉结构完整（双星座名+分隔符+主题词+小无限符号）
- [ ] BOND XX 章节标签
- [ ] 引用区块有左边框
- [ ] 页码格式 "0 X"（带空格）

### 结尾页专项检查
- [ ] **无页眉**
- [ ] 顶部有无限符号装饰
- [ ] 配对指数使用 72px Times New Roman
- [ ] 有两处分隔装饰
- [ ] 祝福语使用斜体 24px
- [ ] END 标记居中
