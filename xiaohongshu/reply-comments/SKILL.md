---
name: replying-to-comments
description: Manages Xiaohongshu comment replies by fetching comments and generating warm, concise responses. Use when the user wants to view all comments across notes, check for new comments, generate professional reply suggestions, or batch manage comment interactions.
---

# 小红书评论回复助手

自动获取笔记评论，生成温暖简短的回复（≤100字），用户确认后执行。

---

## 执行前检查

> 详细登录流程见 [`../_shared/xiaohongshu-login.md`](../_shared/xiaohongshu-login.md)
> 飞书配置见 [`../_shared/feishu-config.md`](../_shared/feishu-config.md)

1. **xiaohongshu-mcp 状态**：调用 `check_login_status` 确保已登录
2. **飞书配置**：确保可访问多维表格（用于保存回复记录）

---

## 输入方式

支持三种输入：

1. **批量查看**：查看所有笔记的评论汇总
2. **标题搜索**：提供笔记标题，查看/回复该笔记评论
3. **链接/ID**：直接提供笔记链接或 feed_id

---

## 模式一：批量查看所有笔记评论

当用户说"查看所有评论"、"检查新评论"、"有没有新评论"时触发。

### 流程

```
Step 1: 获取笔记列表
- 使用已知 user_id: 63a4d7e00000000026010ffd
- mcp__xiaohongshu-mcp__search_feeds(keyword="射手座生存指南") → 获取 xsec_token
- mcp__xiaohongshu-mcp__user_profile(user_id, xsec_token) → 获取最近10篇笔记

Step 2: 逐篇获取评论
- 遍历笔记列表
- mcp__xiaohongshu-mcp__get_feed_detail(feed_id, xsec_token, limit=5) → 获取每篇评论

Step 3: 汇总展示
输出格式：
| # | 笔记标题 | 评论数 | 最新评论预览 |
|---|----------|--------|--------------|
| 1 | 黑化后的射手 | 5 | "太准了！" |
| 2 | 射手座配对指南 | 3 | "和天蝎能配吗" |

Step 4: 用户选择
- 输入序号查看详情并回复
- 或直接选择要回复的评论
```

---

## 模式二：单篇笔记评论回复

当用户指定笔记标题或链接时触发。

### Step 1: 获取笔记评论

**方式A - 标题搜索：**
```
1. mcp__xiaohongshu-mcp__search_feeds → 搜索笔记
2. 从结果中匹配用户账号的笔记，获取 feed_id 和 xsec_token
3. mcp__xiaohongshu-mcp__get_feed_detail → 获取评论列表
```

**方式B - 链接/ID：**
```
1. 解析链接提取 feed_id（链接格式：https://www.xiaohongshu.com/explore/{feed_id}）
2. 从 list_feeds 或 search_feeds 获取有效 xsec_token
3. mcp__xiaohongshu-mcp__get_feed_detail → 获取评论列表
```

**get_feed_detail 参数：**
- `feed_id`: 笔记ID
- `xsec_token`: 访问令牌
- `load_all_comments`: true（加载全部评论）
- `limit`: 10（最多10条一级评论）

### Step 2: 分析评论生成回复

遍历每条评论，判断类型并生成回复：

```
IF 评论涉及星座问题（包含星座名称、星座特征、配对等关键词）:
    → 使用 WebSearch 搜索相关星座知识
    → 结合专业知识生成专业回复
ELSE:
    → 直接生成温暖简短的回复
```

**输出格式：**

| # | 评论者 | 评论内容 | 建议回复 | 类型 |
|---|--------|----------|----------|------|
| 1 | 用户A | 说得太对了！ | 谢谢认可～ | 普通 |
| 2 | 用户B | 射手和天蝎能在一起吗 | 可以的，射手的热情... | 星座 |

### Step 3: 用户确认

展示所有待回复内容，等待用户选择：
- **全部回复**：执行所有回复
- **部分回复**：用户指定要回复的评论序号
- **修改后回复**：用户修改某条回复内容后执行
- **取消**：不执行任何回复

### Step 4: 执行回复并保存

```
1. mcp__xiaohongshu-mcp__reply_comment_in_feed → 执行回复
   参数：
   - feed_id: 笔记ID
   - xsec_token: 访问令牌
   - comment_id: 目标评论ID
   - user_id: 目标评论用户ID
   - content: 回复内容

2. mcp__lark-mcp__bitable_v1_appTableRecord_create → 保存到飞书
   字段：笔记标题、笔记ID、评论内容、评论用户、回复内容、回复时间、是否星座问题
```

---

## 回复风格指南

### 核心原则

| 必须 | 禁止 |
|------|------|
| ≤100字 | 批判、说教 |
| 温暖真诚 | 模板化/机械回复 |
| 有人情味 | 过度营销 |
| 简短有力 | 敷衍应付 |
| 自然口语化 | AI腔调 |

### 回复类型与模板

**1. 普通互动（点赞、认可类）：**
- "谢谢你的认可～"
- "哈哈被你发现了"
- "懂的都懂！"
- "握手～"

**2. 问题咨询（星座相关）：**
- 需要 WebSearch 搜索后回复
- 示例："射手确实很注重自由，但真正爱上时会主动为你停留的～"
- 示例："这个问题很多人问过，射手的冷淡通常是在试探你的反应..."

**3. 共鸣分享（表达认同）：**
- "懂你的感受，射手就是这样的矛盾体"
- "同为射手，深有体会"
- "被说中了～"

**4. 负面/质疑评论：**
- "每个人感受不同，谢谢分享你的看法"
- "理解你的观点～"
- "也有道理呢"
- 绝不争辩、不解释、不反驳

---

## 星座问题识别关键词

以下关键词触发 WebSearch：

- 12星座名称：白羊、金牛、双子、巨蟹、狮子、处女、天秤、天蝎、射手、摩羯、水瓶、双鱼
- 配对词：配对、合适、能不能在一起、般配
- 性格词：性格、特点、缺点、优点、黑化、回避、焦虑
- 情感词：喜欢、爱上、分手、复合、冷战、忽冷忽热

---

## MCP 工具清单

| 工具 | 用途 | 必需参数 |
|------|------|----------|
| `search_feeds` | 搜索笔记 | keyword |
| `list_feeds` | 获取首页（用于获取token） | 无 |
| `user_profile` | 获取用户笔记列表 | user_id, xsec_token |
| `get_feed_detail` | 获取笔记详情和评论 | feed_id, xsec_token |
| `reply_comment_in_feed` | 回复评论 | feed_id, xsec_token, comment_id, user_id, content |
| `bitable_v1_appTableRecord_create` | 保存回复记录 | app_token, table_id, fields |

---

## 飞书记录字段

| 字段 | 类型 | 说明 |
|------|------|------|
| 笔记标题 | 文本 | 原笔记标题 |
| 笔记ID | 文本 | feed_id |
| 评论内容 | 文本 | 用户评论原文 |
| 评论用户 | 文本 | 评论者昵称 |
| 回复内容 | 文本 | 我方回复 |
| 回复时间 | 日期 | 回复时间戳 |
| 是否星座问题 | 复选框 | 是否涉及星座 |

---

## 使用示例

**示例1：批量查看所有评论**
```
用户：查看所有笔记的评论
用户：检查新评论
用户：有没有新评论
```

**示例2：标题搜索**
```
用户：回复「黑化后的射手」的评论
用户：查看「放弃型射手」的评论
```

**示例3：链接输入**
```
用户：回复这篇笔记的评论 https://www.xiaohongshu.com/explore/69521017000000001d0398da
```

**示例4：指定数量**
```
用户：回复「射手座配对指南」的最新5条评论
```

---

## 错误处理

| 错误 | 处理方式 |
|------|----------|
| 笔记未找到 | 提示用户检查标题/链接是否正确 |
| 无评论 | 提示"该笔记暂无评论" |
| 回复失败 | 记录失败原因，继续处理下一条 |
| MCP 未连接 | 提示重连 xiaohongshu-mcp |

---

## 注意事项

1. **回复频率**：避免短时间内大量回复，建议每条间隔2-3秒
2. **内容审核**：确保回复内容符合平台规范
3. **用户确认**：必须等待用户确认后才执行回复
4. **记录保存**：每次回复都保存到飞书，便于追踪
