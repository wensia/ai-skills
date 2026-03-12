# 各检查项详细规范与输出格式

## Skill A：Layout Lint 输出格式

```markdown
## Layout Lint Report

### Critical Issues
1. **[重叠]** 标题与副标题发生覆盖
   - 位置：y=120~150px 区域
   - 修复：副标题下移 20px，设置 y=170px
   - 验收：两元素间距 ≥12px

### Major Issues
2. **[安全区]** 左边距不一致
   - 问题：标题 x=100px，正文 x=95px
   - 修复：统一设置 x=100px
   - 验收：所有左对齐元素 x 值一致

### Minor Issues
3. **[对齐]** 页码未完全右对齐
   - 问题：当前 x=970px，应为 x=980px
   - 修复：设置 text-anchor="end", x=980
   - 验收：与右边距对齐
```

---

## Skill B：Typography Lint 输出格式

```markdown
## Typography Lint Report

### 字号层级
- H1: 72px (主标题)
- H2: 56px (章节标题)
- H3: 54px ← 与 H2 太接近（比例 1.04），建议改为 42px

### 混排问题
1. **[基线漂移]** "85%" 中 % 符号偏高
   - 当前：同基线
   - 修复：% 添加 baseline-shift: -2px 或使用 dy="2" 属性

### 建议配置
- line-height: 1.8 (中文正文)
- letter-spacing: 4px (英文标题)
- word-spacing: 0.5em (英文正文)
```

---

## Skill C：Baseline Alignment 输出格式

```markdown
## Baseline Alignment Report

### 需要对齐的对象
| 元素组 | 当前状态 | 对齐基准 | 修正建议 |
|--------|----------|----------|----------|
| "85" + "%" | % 偏高 3px | baseline | `<tspan dy="3">%</tspan>` |
| "MATCH INDEX" | 视觉居中 | x-height | 无需修正 |
| "∞" 符号 | 偏高 5px | optical center | `transform="translate(0, 5)"` |

### SVG 修正代码
<!-- 修正前 -->
<text>85%</text>
<!-- 修正后 -->
<text>
  <tspan>85</tspan>
  <tspan dy="3" font-size="0.8em">%</tspan>
</text>
```

---

## Skill D：Spacing Consistency 输出格式

```markdown
## Spacing Consistency Report

### 图标组间距检查
| 间距 | 测量值 | 期望值 | 状态 |
|------|--------|--------|------|
| A→B | 120px | 120px | ✓ |
| B→C | 115px | 120px | ✗ 差 5px |

### 修复方案
1. 选中图标组
2. 执行 "Align vertical center"
3. 执行 "Distribute horizontally"
4. 光学微调：C 图标右移 2px（因为 C 更圆，视觉上偏左）

### SVG 修正
<!-- 修正前 -->
<g transform="translate(200, 0)">A</g>
<g transform="translate(320, 0)">B</g>
<g transform="translate(435, 0)">C</g>
<!-- 修正后：等距 120px -->
<g transform="translate(200, 0)">A</g>
<g transform="translate(320, 0)">B</g>
<g transform="translate(440, 0)">C</g>
```

---

## Skill E：Header Collision Guard 输出格式

```markdown
## Header Collision Check

### 当前状态
- 主标题宽度：580px
- 副标题宽度：320px
- 两者间距：8px ← 临界值

### 兼容性测试
| 文案类型 | 示例 | 状态 |
|----------|------|------|
| 最短 | "双子×射手" | ✓ 间距 45px |
| 标准 | "射手座×狮子座" | ✓ 间距 12px |
| 最长 | "摩羯座×天蝎座·命定之约" | ✗ 重叠 |

### 修复建议
1. 推荐安全区高度：140px（当前 120px）
2. 长文案 fallback：
   - 优先：副标题字号缩放至 90%
   - 备选：主标题换行
```

---

## Skill F：Grid & Rhythm 输出格式

```markdown
## Grid & Rhythm Report

### 网格选择：8pt grid

### 中心轴
- 类型：居中布局
- 中心轴：x=540
- 内容区宽度：880px (100 → 980)

### 垂直间距检查
| 模块 | 当前间距 | 网格值 | 修正 |
|------|----------|--------|------|
| 页眉→标题 | 70px | 72px (8×9) | +2px |
| 标题→副标题 | 45px | 48px (8×6) | +3px |
| 图标组→指数 | 24px | 24px (8×3) | ✓ |

### 建议模块间距
- 图标组 → MATCH INDEX：24px
- MATCH INDEX → 85%：8px
- 85% → 分割线：16px
- 分割线 → 主标题：32px
```

---

## Skill G：Icon Consistency 输出格式

```markdown
## Icon Consistency Report

### 当前状态
| 图标 | 线宽 | 端点 | 拐角 | 大小 |
|------|------|------|------|------|
| 星座1 | 2px | round | round | 80px |
| ∞ 符号 | 2.5px | round | miter | 40px | ← 不一致
| 星座2 | 2px | round | round | 80px |

### 修复建议
统一标准：stroke-width: 2px, stroke-linecap: round, stroke-linejoin: round
```

---

## Skill H：Export QA 输出格式

```markdown
## Export QA Report

### 像素对齐检查
| 元素 | 当前值 | 修正值 | 状态 |
|------|--------|--------|------|
| 分隔线 x | 100.5 | 100 | ✗ |
| 页码 y | 1390 | 1390 | ✓ |
| 图标 transform | translate(540.3, 320) | translate(540, 320) | ✗ |

### 字体检查
- [ ] @import 字体链接可访问
- [x] 中文字体：Noto Serif SC
- [x] 英文字体：Georgia
- [ ] 等待时间：需 ≥2秒

### 导出建议
- 小红书发布：2x (2160×2880) PNG
- 使用截图工具：`poster_screenshot.py`
- 等待字体加载：已内置 2 秒等待

### 验收点位截图
1. 标题区 [x=100, y=100, w=400, h=100] - 检查字体
2. 图标区 [x=400, y=280, w=280, h=150] - 检查线条
3. 页脚区 [x=900, y=1340, w=100, h=60] - 检查小字
```
