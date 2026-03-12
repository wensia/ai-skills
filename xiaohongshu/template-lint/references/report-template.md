# 体检报告模板

## 完整体检流程

```mermaid
flowchart TD
    A[输入：截图/HTML/SVG] --> B[Skill A: Layout Lint]
    B --> C[Skill E: Header Collision]
    C --> D[Skill B: Typography]
    D --> E[Skill C: Baseline]
    E --> F[Skill D: Spacing]
    F --> G[Skill F: Grid & Rhythm]
    G --> H[Skill G: Icon Style]
    H --> I[Skill H: Export QA]
    I --> J[生成体检报告]
    J --> K{有 Critical 问题?}
    K -->|是| L[优先修复 Critical]
    K -->|否| M{有 Major 问题?}
    M -->|是| N[修复 Major]
    M -->|否| O[输出优化建议]
    L --> B
    N --> B
```

## 报告模板

```markdown
# Template Lint Report

**文件**：{filename}
**尺寸**：{width}×{height}
**检查时间**：{datetime}

## Summary

| 级别 | 数量 | 状态 |
|------|------|------|
| Critical | {n} | {status} |
| Major | {n} | {status} |
| Minor | {n} | {status} |

## Critical Issues

{critical_issues}

## Major Issues

{major_issues}

## Minor Issues / Suggestions

{minor_issues}

## 修复代码

{fix_code}

---

**检查项**：A B C D E F G H
**通过项**：{passed}
**待修复**：{failed}
```
