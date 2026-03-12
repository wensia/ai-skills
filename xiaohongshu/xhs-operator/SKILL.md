---
name: xhs-operator
description: |
  Operate the Xiaohongshu (RED/小红书) mobile app on a physical Android phone via USB.
  Use this skill whenever the user asks to interact with XHS — searching posts, viewing comments,
  replying to comments, liking, bookmarking, browsing feed, or any other XHS app operation.
  Also triggers when the user mentions "小红书", "XHS", "RED app", "手机操作", or refers to
  phone automation tasks involving social media content. The skill manages a self-evolving
  knowledge base that accumulates operation experience across sessions.
---

# XHS 手机操作智能体

你是一个通过 USB 控制真实 Android 手机来操作小红书 App 的智能体。你有两个核心工具：
1. **控制命令** (`python -m src.control <cmd>`) — 直接操作手机
2. **技能回放** (`python main.py skill run <name>`) — 执行已验证的操作序列

## 核心原则：自进化

**操作逻辑不变，App 元素会变。** 每次操作都在积累经验，让下一次更快更准。

### 操作前：查阅知识库

每次执行任何 XHS 操作之前，**必须**先读取知识库：

```
Read skills/_知识库.yaml
```

知识库包含：
- 页面结构认知（各页面的布局和元素关系）
- 核心操作逻辑（经过验证的操作步骤）
- 技术经验（输入法、设备相关的 workaround）
- 踩坑记录（已知的坑和解决方案）
- 错误路径（已证明无效的操作方式）

### 操作后：更新知识库

每次操作完成后，如果发现了新信息，**必须**更新知识库：

- 新发现的操作逻辑 → 添加到 `operations` 节
- 新的坑 → 添加到 `pitfalls` 节
- 验证了某个操作 → 标记 `verified: true` 并记录日期
- 发现错误路径 → 添加到对应操作的 `wrong_approaches`

## 控制命令参考

所有命令都在项目根目录下执行。

- 本地示例：`/Users/panyuhang/我的项目/编程/xiaohongshu/agent/`
- Ubuntu 部署示例：`/home/panyuhang/projects/xiaohongshu-agent/`

| 命令 | 说明 |
|------|------|
| `python -m src.control observe` | 截图 + 元素列表（每次操作前先 observe） |
| `python -m src.control tap <N>` | 点击第 N 号元素 |
| `python -m src.control tap-xy <x> <y>` | 点击坐标 |
| `python -m src.control long-press <N>` | 长按第 N 号元素 |
| `python -m src.control type "文本"` | 输入文本（支持中文） |
| `python -m src.control clear-type "文本"` | 清空再输入 |
| `python -m src.control swipe up/down` | 滑动翻页 |
| `python -m src.control enter` | 提交/发送（IME 发送键） |
| `python -m src.control back` | 返回 |
| `python -m src.control open com.xingin.xhs` | 打开小红书 |
| `python -m src.control wait <秒>` | 等待 |

### 技能回放

已验证的复合操作可以直接回放：

```bash
python main.py skill list              # 列出所有技能
python main.py skill run "回复评论" -p comment_text="目标评论" -p reply_text="回复内容"
```

### 受控自进化闭环

当一次技能运行失败，先不要直接覆盖正式技能，按下面顺序走：

```bash
python main.py evolution propose --skill "查看笔记评论"
python main.py evolution validate --candidate evolution/candidates/<候选目录>
python main.py evolution promote --candidate evolution/candidates/<候选目录>
```

说明：
- `propose` 会基于最近一次 `run-report.json` 生成候选技能和候选知识库补丁
- `validate` 会读取 `evolution/cases.yaml` 跑回归用例
- `promote` 只有在验证全部通过后才允许覆盖正式技能并合并知识库

## 操作流程模板

### 手动操作流程（无现成技能时）

```
1. observe → 理解当前页面
2. 查阅知识库中对应操作的 logic
3. 按 logic 逐步执行，每步后 observe 确认
4. 完成后更新知识库
```

### 技能回放流程（有已验证技能时）

```
1. 查阅知识库确认操作逻辑
2. skill run 执行
3. 如果失败 → 切换到手动模式排查
4. 更新知识库
```

## 关键技术约束

这些是通过踩坑验证的硬约束，不要尝试绕过：

1. **文本输入**: 必须用 `type` 命令（底层是 ADB_KEYBOARD_INPUT_TEXT + base64），不能用 adb input text
2. **提交评论/回复**: 必须用 `enter` 命令（IME_ACTION_SEND），不能点 App 发送按钮（被键盘工具栏遮挡）
3. **清空输入框**: 必须用 `clear-type`（Ctrl+A + DEL），u2 的 clear_text 会崩溃
4. **resource-id**: XHS 所有 resource-id 已混淆，不可用于元素匹配
5. **剪贴板**: Android 16 禁止 shell 访问剪贴板
6. **u2 断连**: 键盘弹出/收起后 u2 可能断连，observe 会自动重连

## 创建新技能

当你成功完成一个新操作且经过验证，应将其保存为可复用技能。

### 技能 YAML 格式

详见 `references/skill-format.md`。核心结构：

```yaml
name: 技能名称
description: 简明描述，包含前提条件
tags: [已验证, 类别标签]
app_package: com.xingin.xhs
parameters:
  - name: param_name
    description: "参数说明（示例: xxx）"
steps:
  - action: tap/type/enter/swipe_up/back/wait/observe
    target:
      text_contains: "{{param_name}}"  # 优先用文本匹配
    wait: 1.0
    description: "步骤说明"
```

### 元素匹配优先级

1. `text` / `text_contains` — 最稳定，App 更新后文案通常不变
2. `desc` / `desc_contains` — 次选，用于图标等无文字元素
3. `nth_clickable` + `area` — 兜底，按位置匹配
4. `tap_coords` (x_pct/y_pct) — 最后手段，分辨率变化会失效

## 故障排查

| 现象 | 可能原因 | 解决方案 |
|------|---------|---------|
| observe 无响应 | USB 断连 | 重新连接设备 |
| 输入中文乱码 | 未使用 ADB Keyboard | 确认输入法设置 |
| 点击无反应 | 元素被遮挡/不可点击 | observe 查看可点击元素列表 |
| 评论发送失败 | 没用 enter 命令 | 用 `enter` 代替点击发送 |
| 技能执行中断 | 页面状态变化 | 切换手动模式排查后更新技能 |

## 自进化记录规范

知识库更新时遵循以下规范：

```yaml
# 操作逻辑记录模板
操作名:
  logic:
    - "1. 步骤描述（重点记录'为什么这样做'）"
    - "2. 步骤描述"
  verified: true/false
  verified_date: "YYYY-MM-DD"
  note: "补充说明"
  wrong_approaches:
    - "X 方法 → 失败原因"
  success_indicator: "如何确认操作成功"

# 踩坑记录模板
- issue: "问题现象"
  cause: "根本原因"
  solution: "解决方案"
```
