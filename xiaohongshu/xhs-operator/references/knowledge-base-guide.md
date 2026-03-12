# 知识库维护指南

## 文件位置

```
skills/_知识库.yaml
```

## 结构概览

```yaml
# 1. 基础认知 — App 和设备信息（很少变）
app: { package, name, content_types, interaction_types }
device: { model, android, screen, ime }

# 2. 页面结构认知 — 每个页面的布局和导航方式
pages:
  首页: { description, top_bar, bottom_bar, card_structure, how_to_open_post }
  搜索页: { entry, structure, tabs, how_to_search }
  笔记详情页: { structure, bottom_bar, how_to_open_comments }
  评论区: { structure, comment_structure, bottom_bar }

# 3. 核心操作逻辑 — 最重要的部分
operations:
  操作名:
    logic: [步骤列表]
    verified: true/false
    verified_date: "YYYY-MM-DD"
    note: "补充说明"
    wrong_approaches: ["X 方法 → 无效(原因)"]
    success_indicator: "如何确认成功"

# 4. 技术经验 — 输入法/设备相关的 workaround
tech:
  text_input: { method, note }
  submit: { method, note }
  # ...

# 5. 踩坑记录
pitfalls:
  - { issue, cause, solution }

# 6. 更新日志
changelog:
  - "YYYY-MM-DD: 变更内容"
```

## 更新时机

| 场景 | 更新内容 |
|------|---------|
| 成功完成一个操作 | 标记 verified: true，记录 verified_date |
| 发现新的操作方式 | 添加到 operations |
| 操作失败 | 记录到 wrong_approaches 和 pitfalls |
| App 界面变化 | 更新 pages 结构描述 |
| 发现技术 workaround | 添加到 tech |

## 更新原则

1. **记录逻辑，不记录值** — 写"点击评论区的评论条"而非"点击坐标(320,831)"
2. **记录失败路径同样重要** — wrong_approaches 防止下次重蹈覆辙
3. **保持简洁** — 每个操作的 logic 不超过 5-7 步
4. **只更新有变化的部分** — 用 Edit 工具精确修改，不要重写整个文件
5. **changelog 追加** — 每次更新在 changelog 最前面加一行

## 示例：添加新操作

```yaml
# 在 operations 下添加
发表评论:
  logic:
    - "1. 在笔记详情页点击底栏评论框'说点什么...'"
    - "2. 输入框弹出获得焦点"
    - "3. type 输入评论内容"
    - "4. enter 提交"
  verified: true
  verified_date: "2026-03-05"
  note: "用 enter 命令提交，不要点 App 发送按钮"
  success_indicator: "评论数 +1"
```

## 示例：记录踩坑

```yaml
# 在 pitfalls 下追加
- issue: "输入文字后点击 App 发送按钮无效"
  cause: "ADB Keyboard 底部工具栏遮挡了 App 按钮"
  solution: "用 enter 命令（IME_ACTION_SEND）代替点击发送按钮"
```
