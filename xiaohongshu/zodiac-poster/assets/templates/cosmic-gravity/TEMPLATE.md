# 星际引力风 (Cosmic Gravity) SVG 模板规范

**格式**：纯 SVG（不使用 HTML/CSS）
**特征**：深紫蓝太空背景 + 星星粒子 + 引力轨道装饰 + 渐变光晕
**适用**：星座配对、宇宙能量、神秘感内容、深度解读

---

## 配色系统

| 用途 | 色值 | SVG属性 |
|------|------|---------|
| **主强调色** | `#A78BDA` | fill / stroke（紫色） |
| **辅助强调色** | `#7DB8C9` | fill / stroke（蓝色） |
| **主文字** | `#E8E4F0` | fill（亮色） |
| **次要文字** | `#9B95A8` | fill |
| **装饰元素** | `#6B6380` | stroke |
| **星星粒子** | `#FFFFFF` | fill, opacity: 0.3-0.8 |

### 背景渐变定义

```svg
<defs>
  <!-- 深空背景渐变 -->
  <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#1A1525"/>
    <stop offset="50%" stop-color="#252035"/>
    <stop offset="100%" stop-color="#1E1A2E"/>
  </linearGradient>

  <!-- 中心光晕 -->
  <radialGradient id="centerGlow" cx="50%" cy="40%" r="50%">
    <stop offset="0%" stop-color="#A78BDA" stop-opacity="0.15"/>
    <stop offset="50%" stop-color="#7DB8C9" stop-opacity="0.05"/>
    <stop offset="100%" stop-color="#1A1525" stop-opacity="0"/>
  </radialGradient>

  <!-- 引力轨道渐变 -->
  <linearGradient id="orbitGradient" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#A78BDA" stop-opacity="0"/>
    <stop offset="50%" stop-color="#A78BDA" stop-opacity="0.4"/>
    <stop offset="100%" stop-color="#7DB8C9" stop-opacity="0"/>
  </linearGradient>
</defs>
```

---

## 尺寸规范

**画布**：1080px × 1440px

| 元素 | 尺寸 | 说明 |
|------|------|------|
| 左右边距 | 100px | 内容区 x: 100 ~ 980 |
| 上下边距 | 90px | 内容区 y: 90 ~ 1350 |
| 页眉星座名 | 32px | font-weight: 500 |
| **封面主标题** | **72px** | font-weight: 600, letter-spacing: 6 |
| 章节标题 | 56px | font-weight: 600 |
| 正文 | 32px | line-height: 61px |
| 引用文字 | 28px | font-style: italic |
| 页码 | 28px | font-family: Georgia |
| 星座图标 | 80×80px | 带光晕效果 |
| 星星粒子 | 2-6px | 随机分布 |
| 引力轨道 | 椭圆 | stroke-width: 1-2 |

---

## 字体加载

```svg
<defs>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
  </style>
</defs>
```

---

## 核心设计元素

### 1. 星星粒子装饰

```svg
<!-- 星星粒子层 -->
<g id="stars">
  <circle cx="150" cy="200" r="2" fill="#FFF" opacity="0.6"/>
  <circle cx="890" cy="180" r="3" fill="#FFF" opacity="0.4"/>
  <circle cx="320" cy="350" r="1.5" fill="#FFF" opacity="0.7"/>
  <circle cx="780" cy="420" r="2.5" fill="#FFF" opacity="0.5"/>
  <circle cx="200" cy="600" r="2" fill="#FFF" opacity="0.3"/>
  <circle cx="920" cy="750" r="3" fill="#FFF" opacity="0.4"/>
  <circle cx="130" cy="900" r="1.5" fill="#FFF" opacity="0.6"/>
  <circle cx="850" cy="1100" r="2" fill="#FFF" opacity="0.5"/>
  <circle cx="250" cy="1200" r="2.5" fill="#FFF" opacity="0.4"/>
  <circle cx="950" cy="1300" r="1.5" fill="#FFF" opacity="0.3"/>
  <!-- 可根据需要增减星星 -->
</g>
```

### 2. 引力轨道装饰（封面专用）

```svg
<!-- 引力轨道 -->
<g id="orbits" transform="translate(540, 400)">
  <!-- 外层轨道 -->
  <ellipse cx="0" cy="0" rx="180" ry="60" fill="none" stroke="url(#orbitGradient)" stroke-width="1" transform="rotate(-15)"/>
  <!-- 中层轨道 -->
  <ellipse cx="0" cy="0" rx="140" ry="45" fill="none" stroke="url(#orbitGradient)" stroke-width="1.5" transform="rotate(10)"/>
  <!-- 内层轨道 -->
  <ellipse cx="0" cy="0" rx="100" ry="30" fill="none" stroke="url(#orbitGradient)" stroke-width="1" transform="rotate(-5)"/>
</g>
```

### 3. 双星座光晕布局（封面专用）

```svg
<!-- 双星座布局 -->
<g id="dual-zodiac" transform="translate(540, 380)">
  <!-- 左星座光晕 -->
  <circle cx="-100" cy="0" r="60" fill="#A78BDA" opacity="0.1"/>
  <g transform="translate(-100, 0)">
    {{ZODIAC1_SVG}}
  </g>

  <!-- 连接光线 -->
  <line x1="-40" y1="0" x2="40" y2="0" stroke="url(#orbitGradient)" stroke-width="2"/>

  <!-- 右星座光晕 -->
  <circle cx="100" cy="0" r="60" fill="#7DB8C9" opacity="0.1"/>
  <g transform="translate(100, 0)">
    {{ZODIAC2_SVG}}
  </g>
</g>
```

### 4. 页眉结构

```svg
<g id="header">
  <!-- 星座配对名 -->
  <text x="100" y="130"
        font-family="Noto Serif SC, serif"
        font-size="32"
        font-weight="500"
        fill="#A78BDA"
        letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>

  <!-- 分隔符 -->
  <text x="280" y="130"
        font-family="Georgia, serif"
        font-size="24"
        fill="#6B6380">·</text>

  <!-- 主题词 -->
  <text x="310" y="130"
        font-family="Noto Sans SC, sans-serif"
        font-size="24"
        font-weight="300"
        fill="#9B95A8"
        letter-spacing="3">星际引力</text>

  <!-- 右上角装饰：小星星群 -->
  <g transform="translate(920, 110)">
    <circle cx="0" cy="0" r="2" fill="#FFF" opacity="0.8"/>
    <circle cx="15" cy="-10" r="1.5" fill="#FFF" opacity="0.6"/>
    <circle cx="-10" cy="8" r="1" fill="#FFF" opacity="0.4"/>
  </g>
</g>
```

### 5. 页脚结构

```svg
<g id="footer">
  <!-- 分隔线 -->
  <line x1="100" y1="1350" x2="980" y2="1350"
        stroke="#6B6380" stroke-width="1"/>

  <!-- 页码 -->
  <text x="980" y="1390"
        font-family="Georgia, serif"
        font-size="28"
        fill="#9B95A8"
        text-anchor="end"
        letter-spacing="4">{{PAGE_NUM}}</text>
</g>
```

---

## 封面模板

```svg
<!-- [STYLE: 星际引力风] [TYPE: cover] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1A1525"/>
      <stop offset="50%" stop-color="#252035"/>
      <stop offset="100%" stop-color="#1E1A2E"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="50%" cy="35%" r="50%">
      <stop offset="0%" stop-color="#A78BDA" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="#7DB8C9" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#1A1525" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="orbitGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#A78BDA" stop-opacity="0"/>
      <stop offset="50%" stop-color="#A78BDA" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#7DB8C9" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="textGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#A78BDA"/>
      <stop offset="100%" stop-color="#7DB8C9"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#centerGlow)"/>

  <!-- 星星粒子 -->
  <g id="stars">
    <circle cx="150" cy="200" r="2" fill="#FFF" opacity="0.6"/>
    <circle cx="890" cy="180" r="3" fill="#FFF" opacity="0.4"/>
    <circle cx="320" cy="350" r="1.5" fill="#FFF" opacity="0.7"/>
    <circle cx="780" cy="420" r="2.5" fill="#FFF" opacity="0.5"/>
    <circle cx="200" cy="600" r="2" fill="#FFF" opacity="0.3"/>
    <circle cx="920" cy="750" r="3" fill="#FFF" opacity="0.4"/>
    <circle cx="130" cy="900" r="1.5" fill="#FFF" opacity="0.6"/>
    <circle cx="850" cy="1100" r="2" fill="#FFF" opacity="0.5"/>
    <circle cx="250" cy="1200" r="2.5" fill="#FFF" opacity="0.4"/>
    <circle cx="950" cy="1300" r="1.5" fill="#FFF" opacity="0.3"/>
  </g>

  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#A78BDA" letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>
    <text x="280" y="130" font-family="Georgia, serif" font-size="24" fill="#6B6380">·</text>
    <text x="310" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#9B95A8" letter-spacing="3">星际引力</text>
    <g transform="translate(920, 110)">
      <circle cx="0" cy="0" r="2" fill="#FFF" opacity="0.8"/>
      <circle cx="15" cy="-10" r="1.5" fill="#FFF" opacity="0.6"/>
      <circle cx="-10" cy="8" r="1" fill="#FFF" opacity="0.4"/>
    </g>
  </g>

  <!-- 引力轨道 -->
  <g id="orbits" transform="translate(540, 380)">
    <ellipse cx="0" cy="0" rx="180" ry="60" fill="none" stroke="url(#orbitGradient)" stroke-width="1" transform="rotate(-15)"/>
    <ellipse cx="0" cy="0" rx="140" ry="45" fill="none" stroke="url(#orbitGradient)" stroke-width="1.5" transform="rotate(10)"/>
    <ellipse cx="0" cy="0" rx="100" ry="30" fill="none" stroke="url(#orbitGradient)" stroke-width="1" transform="rotate(-5)"/>
  </g>

  <!-- 双星座布局 -->
  <g id="dual-zodiac" transform="translate(540, 380)">
    <circle cx="-100" cy="0" r="55" fill="#A78BDA" opacity="0.1"/>
    <g transform="translate(-100, 0)">{{ZODIAC1_SVG_LARGE}}</g>
    <line x1="-40" y1="0" x2="40" y2="0" stroke="url(#orbitGradient)" stroke-width="2"/>
    <circle cx="100" cy="0" r="55" fill="#7DB8C9" opacity="0.1"/>
    <g transform="translate(100, 0)">{{ZODIAC2_SVG_LARGE}}</g>
  </g>

  <!-- 配对指数 -->
  <g id="match-index" transform="translate(540, 530)">
    <text x="0" y="0" font-family="Georgia, serif" font-size="18" fill="#9B95A8" text-anchor="middle" letter-spacing="4">COSMIC BOND</text>
    <text x="0" y="50" font-family="Georgia, serif" font-size="56" font-weight="600" fill="url(#textGlow)" text-anchor="middle">{{MATCH_PERCENT}}%</text>
  </g>

  <!-- 分隔线 -->
  <line x1="470" y1="620" x2="610" y2="620" stroke="#6B6380" stroke-width="1"/>

  <!-- 封面标题 -->
  <g id="cover-title" transform="translate(540, 740)">
    <text x="0" y="0" font-family="Noto Serif SC, serif" font-size="72" font-weight="600" fill="#E8E4F0" text-anchor="middle" letter-spacing="6">{{TITLE}}</text>
    <text x="0" y="80" font-family="Noto Serif SC, serif" font-size="32" fill="#9B95A8" text-anchor="middle" letter-spacing="4">{{SUBTITLE}}</text>
  </g>

  <!-- 标语 -->
  <g id="tagline" transform="translate(540, 940)">
    <text x="0" y="0" font-family="Noto Serif SC, serif" font-size="28" fill="#9B95A8" text-anchor="middle" letter-spacing="3">{{TAGLINE_LINE1}}</text>
    <text x="0" y="50" font-family="Noto Serif SC, serif" font-size="28" text-anchor="middle" letter-spacing="3">
      <tspan fill="#A78BDA">{{TAGLINE_HIGHLIGHT}}</tspan><tspan fill="#9B95A8">{{TAGLINE_REST}}</tspan>
    </text>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#6B6380" stroke-width="1"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#9B95A8" text-anchor="end" letter-spacing="4">0 1</text>
  </g>
</svg>
```

### 封面变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC1}}` | 星座1名 | 射手座 |
| `{{ZODIAC2}}` | 星座2名 | 天蝎座 |
| `{{ZODIAC1_SVG_LARGE}}` | 星座1图标(80px, 紫色描边) | `<svg>...</svg>` |
| `{{ZODIAC2_SVG_LARGE}}` | 星座2图标(80px, 蓝色描边) | `<svg>...</svg>` |
| `{{MATCH_PERCENT}}` | 配对指数 | 75 |
| `{{TITLE}}` | 主标题 | 引力相吸 |
| `{{SUBTITLE}}` | 副标题 | 水火交融 |
| `{{TAGLINE_LINE1}}` | 标语第一行 | 看似不合拍 |
| `{{TAGLINE_HIGHLIGHT}}` | 标语高亮 | 却有致命吸引力 |
| `{{TAGLINE_REST}}` | 标语剩余 | （可为空） |

**星座图标颜色规则**：
- 星座1：使用主强调色 `stroke="#A78BDA"`
- 星座2：使用辅助强调色 `stroke="#7DB8C9"`

---

## 内页模板

```svg
<!-- [STYLE: 星际引力风] [TYPE: page] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1A1525"/>
      <stop offset="50%" stop-color="#252035"/>
      <stop offset="100%" stop-color="#1E1A2E"/>
    </linearGradient>
    <radialGradient id="subtleGlow" cx="20%" cy="30%" r="60%">
      <stop offset="0%" stop-color="#A78BDA" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#1A1525" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#subtleGlow)"/>

  <!-- 星星粒子 -->
  <g id="stars">
    <circle cx="150" cy="200" r="2" fill="#FFF" opacity="0.5"/>
    <circle cx="890" cy="280" r="2.5" fill="#FFF" opacity="0.4"/>
    <circle cx="950" cy="750" r="2" fill="#FFF" opacity="0.3"/>
    <circle cx="120" cy="1100" r="1.5" fill="#FFF" opacity="0.5"/>
    <circle cx="920" cy="1250" r="2" fill="#FFF" opacity="0.4"/>
  </g>

  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#A78BDA" letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>
    <text x="280" y="130" font-family="Georgia, serif" font-size="24" fill="#6B6380">·</text>
    <text x="310" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#9B95A8" letter-spacing="3">星际引力</text>
    <g transform="translate(920, 110)">
      <circle cx="0" cy="0" r="2" fill="#FFF" opacity="0.8"/>
      <circle cx="15" cy="-10" r="1.5" fill="#FFF" opacity="0.6"/>
      <circle cx="-10" cy="8" r="1" fill="#FFF" opacity="0.4"/>
    </g>
  </g>

  <!-- 章节标签 -->
  <text x="100" y="220" font-family="Georgia, serif" font-size="24" fill="#A78BDA" letter-spacing="6">ORBIT {{PART_NUM}}</text>

  <!-- 章节标题 -->
  <text x="100" y="310" font-family="Noto Serif SC, serif" font-size="56" font-weight="600" fill="#E8E4F0" letter-spacing="4">{{SECTION_TITLE}}</text>

  <!-- 分隔线 -->
  <line x1="100" y1="340" x2="180" y2="340" stroke="#A78BDA" stroke-width="2"/>

  <!-- 正文内容 -->
  <g id="content" transform="translate(100, 520)">
    {{CONTENT_LINES}}
  </g>

  <!-- 引用区块 -->
  <g id="quote" transform="translate(100, 1050)">
    <!-- 左边框（渐变色） -->
    <line x1="0" y1="0" x2="0" y2="60" stroke="#A78BDA" stroke-width="3"/>
    <!-- 引用文字 -->
    <text x="30" y="40" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#9B95A8" letter-spacing="2">"{{QUOTE}}"</text>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#6B6380" stroke-width="1"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#9B95A8" text-anchor="end" letter-spacing="4">{{PAGE_NUM}}</text>
  </g>
</svg>
```

### 正文内容生成规则

**每行文本模板**：
```svg
<text y="{{LINE_Y}}" font-family="Noto Serif SC, serif" font-size="32" fill="#E8E4F0" letter-spacing="2">
  <tspan fill="#E8E4F0">{{TEXT_BEFORE}}</tspan>
  <tspan fill="#A78BDA">{{HIGHLIGHT}}</tspan>
  <tspan fill="#E8E4F0">{{TEXT_AFTER}}</tspan>
</text>
```

**行间距**：61px（y递增）

**辅助强调色高亮**（可选）：
```svg
<tspan fill="#7DB8C9">{{SECONDARY_HIGHLIGHT}}</tspan>
```

---

## 结尾页模板

```svg
<!-- [STYLE: 星际引力风] [TYPE: end] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1A1525"/>
      <stop offset="50%" stop-color="#252035"/>
      <stop offset="100%" stop-color="#1E1A2E"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="50%" cy="40%" r="45%">
      <stop offset="0%" stop-color="#A78BDA" stop-opacity="0.12"/>
      <stop offset="50%" stop-color="#7DB8C9" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#1A1525" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="textGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#A78BDA"/>
      <stop offset="100%" stop-color="#7DB8C9"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#centerGlow)"/>

  <!-- 星星粒子（更密集，增强仪式感） -->
  <g id="stars">
    <circle cx="150" cy="200" r="2" fill="#FFF" opacity="0.6"/>
    <circle cx="890" cy="180" r="2.5" fill="#FFF" opacity="0.5"/>
    <circle cx="320" cy="350" r="1.5" fill="#FFF" opacity="0.7"/>
    <circle cx="780" cy="420" r="2" fill="#FFF" opacity="0.4"/>
    <circle cx="200" cy="600" r="2.5" fill="#FFF" opacity="0.5"/>
    <circle cx="920" cy="650" r="2" fill="#FFF" opacity="0.6"/>
    <circle cx="130" cy="800" r="1.5" fill="#FFF" opacity="0.4"/>
    <circle cx="850" cy="900" r="2" fill="#FFF" opacity="0.5"/>
    <circle cx="250" cy="1050" r="2.5" fill="#FFF" opacity="0.4"/>
    <circle cx="950" cy="1150" r="1.5" fill="#FFF" opacity="0.6"/>
    <circle cx="180" cy="1250" r="2" fill="#FFF" opacity="0.3"/>
    <circle cx="880" cy="1320" r="2" fill="#FFF" opacity="0.4"/>
  </g>

  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#A78BDA" letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>
    <text x="280" y="130" font-family="Georgia, serif" font-size="24" fill="#6B6380">·</text>
    <text x="310" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#9B95A8" letter-spacing="3">星际引力</text>
    <g transform="translate(920, 110)">
      <circle cx="0" cy="0" r="2" fill="#FFF" opacity="0.8"/>
      <circle cx="15" cy="-10" r="1.5" fill="#FFF" opacity="0.6"/>
      <circle cx="-10" cy="8" r="1" fill="#FFF" opacity="0.4"/>
    </g>
  </g>

  <!-- 居中内容区域 -->
  <g id="centered-content" transform="translate(540, 0)">
    <!-- 章节标签 -->
    <text x="0" y="220" font-family="Georgia, serif" font-size="24" fill="#A78BDA" letter-spacing="6" text-anchor="middle">COSMOS</text>

    <!-- 双星座小图标（带轨道） -->
    <g transform="translate(0, 300)">
      <ellipse cx="0" cy="0" rx="80" ry="25" fill="none" stroke="#6B6380" stroke-width="1" opacity="0.5"/>
      <g transform="translate(-50, 0) scale(0.6)">{{ZODIAC1_SVG}}</g>
      <g transform="translate(50, 0) scale(0.6)">{{ZODIAC2_SVG}}</g>
    </g>

    <!-- 分隔线 -->
    <line x1="-40" y1="370" x2="40" y2="370" stroke="#6B6380" stroke-width="1"/>

    <!-- 主文案区域 -->
    <g id="summary" transform="translate(0, 480)">
      {{CONTENT_LINES}}
    </g>

    <!-- 装饰分隔线（星星） -->
    <g id="content-divider" transform="translate(0, 780)">
      <line x1="-70" y1="0" x2="-20" y2="0" stroke="#6B6380" stroke-width="1"/>
      <circle cx="0" cy="0" r="3" fill="#A78BDA" opacity="0.8"/>
      <line x1="20" y1="0" x2="70" y2="0" stroke="#6B6380" stroke-width="1"/>
    </g>

    <!-- 祝福语区域 -->
    <g id="ending" transform="translate(0, 880)">
      <text y="0" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#9B95A8" text-anchor="middle" letter-spacing="3">{{ENDING_LINE1}}</text>
      <text y="50" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#9B95A8" text-anchor="middle" letter-spacing="3">{{ENDING_LINE2}}</text>

      <!-- END 标记 -->
      <g transform="translate(0, 120)">
        <line x1="-80" y1="0" x2="-25" y2="0" stroke="#6B6380" stroke-width="1"/>
        <text x="0" y="8" font-family="Georgia, serif" font-size="20" fill="url(#textGlow)" text-anchor="middle" letter-spacing="6">ORBIT</text>
        <line x1="25" y1="0" x2="80" y2="0" stroke="#6B6380" stroke-width="1"/>
      </g>
    </g>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#6B6380" stroke-width="1"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#9B95A8" text-anchor="end" letter-spacing="4">{{PAGE_NUM}}</text>
  </g>
</svg>
```

---

## 高亮词规则

### 封面（必须1-2个）
- 标语1个高亮（主强调色 #A78BDA）
- 使用 `fill="#A78BDA"`

### 内页（必须2个呼应对）
- 主高亮：`<tspan fill="#A78BDA">`
- 辅助高亮（可选）：`<tspan fill="#7DB8C9">`
- 两个词形成语义呼应

### 结尾页（1-2个）
- 与封面形成首尾呼应
- 可使用渐变色高亮

---

## 章节标题建议

| 章节 | 标题示例 |
|------|----------|
| ORBIT 01 | 初次相遇 |
| ORBIT 02 | 引力牵引 |
| ORBIT 03 | 碰撞火花 |
| ORBIT 04 | 轨道交汇 |
| ORBIT 05 | 星际挑战 |
| COSMOS | 宇宙结语 |

---

## 检查清单

### 基础检查
- [ ] 画布尺寸 1080×1440
- [ ] 深空背景渐变正确（#1A1525 → #252035 → #1E1A2E）
- [ ] 字体 @import 已添加
- [ ] 页眉结构完整
- [ ] 页脚分隔线 + 右对齐页码
- [ ] 页码格式 "0 X"（带空格）

### 特色元素检查
- [ ] 封面有星星粒子分布
- [ ] 封面有引力轨道装饰
- [ ] 封面有双星座光晕效果
- [ ] 封面有中心光晕渐变
- [ ] 结尾页星星更密集

### 配色检查
- [ ] 主强调色 #A78BDA（紫色）
- [ ] 辅助强调色 #7DB8C9（蓝色）
- [ ] 主文字 #E8E4F0（亮色）
- [ ] 次要文字 #9B95A8
- [ ] 星座1图标：紫色描边
- [ ] 星座2图标：蓝色描边

### 高亮检查
- [ ] 封面：1-2个高亮词（紫色）
- [ ] 内页：2个高亮词呼应对
- [ ] 结尾页：1-2个高亮词

### 结尾页专项检查
- [ ] 有装饰分隔线（星星圆点）
- [ ] 双星座带轨道装饰
- [ ] END 标记改为 ORBIT
- [ ] 星星粒子更密集
