# 技能 YAML 格式参考

## 完整字段说明

```yaml
# === 元数据 ===
name: 技能名称              # 必填，唯一标识
description: 技能描述        # 必填，包含前提条件和适用场景
tags:                       # 分类标签
  - 已验证                   # 表示经过实测验证
  - 评论互动                 # 功能分类
app_package: com.xingin.xhs  # 目标应用包名

# === 参数定义 ===
parameters:
  - name: param_name         # 参数名，在 steps 中用 {{param_name}} 引用
    description: "参数说明（示例: 具体值）"
    # default: "默认值"      # 可选

# === 操作步骤 ===
steps:
  - action: tap              # 动作类型（见下方列表）
    target:                  # 元素匹配条件（tap/long_press 时需要）
      text: "精确文本"
      text_contains: "部分文本"
      desc: "精确描述"
      desc_contains: "部分描述"
      nth_clickable: 3       # 第 N 个可点击元素
      area: "bottom"         # 屏幕区域过滤: top/middle/bottom
    wait: 1.0                # 执行后等待秒数
    optional: false          # true 时匹配失败不中断
    retry: 2                 # 匹配失败重试次数
    pre_swipe: "up"          # 重试前先滑动方向
    description: "步骤说明"
```

## 支持的动作类型

| action | 必填字段 | 说明 |
|--------|---------|------|
| `tap` | target | 点击匹配的元素 |
| `tap_comment_reply` | text | 根据评论文本定位对应的“回复”入口并点击 |
| `read_nav_badge` | text | 读取底部导航按钮角标未读数，适合点击前采集消息数 |
| `long_press` | target | 长按匹配的元素 |
| `tap_coords` | x_pct + y_pct | 点击屏幕百分比坐标 |
| `type` | text | 输入文本（ADB Keyboard） |
| `clear_and_type` | text | 清空后输入 |
| `enter` | - | IME 发送键（提交评论等） |
| `back` | - | 返回键 |
| `home` | - | Home 键 |
| `swipe_up` | - | 向上滑动 |
| `swipe_down` | - | 向下滑动 |
| `wait` | wait | 纯等待 |
| `open_app` | package | 打开应用 |
| `observe` | - | 截图 + 打印内容（调试用） |

## 元素匹配优先级

编写技能时，选择最稳定的匹配方式：

1. **text / text_contains** — 最优先。文案是最稳定的标识
2. **desc / desc_contains** — 用于图标（如搜索图标 desc="搜索"）
3. **nth_clickable + area** — 位置匹配，适合布局固定的按钮
4. **tap_coords (x_pct/y_pct)** — 最后手段。用百分比而非绝对坐标

## 参数模板语法

在 text、text_contains、desc_contains、description 字段中，用 `{{参数名}}` 引用参数：

```yaml
steps:
  - action: tap
    target:
      text_contains: "{{comment_text}}"
    description: "点击包含'{{comment_text}}'的评论"
  - action: type
    text: "{{reply_text}}"
```

## 编写原则

1. **记录逻辑而非坐标** — 坐标会变，"点击评论条进入回复"的逻辑不会变
2. **每步都有 description** — 描述目的而非操作（"进入回复输入界面" 而非 "点击坐标 320,831"）
3. **标注 verified** — 只有实测通过的技能才标 `已验证`
4. **记录失败路径** — 在知识库的 wrong_approaches 中记录试过但无效的方式
5. **合理的 wait 值** — 页面跳转 2.0s，输入后 0.5s，点击后 1.0s
