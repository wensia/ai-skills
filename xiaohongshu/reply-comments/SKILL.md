---
name: replying-to-comments
description: Fetches and replies to Xiaohongshu comments with warm, natural responses. Use this skill whenever the user wants to check comments, view new replies, respond to readers, manage comment interactions, batch reply to XHS notes, handle negative feedback, or engage with their audience — even if they don't explicitly say "reply to comments". Triggers on keywords like 评论, 回复, 新评论, 互动, comments, 查看评论.
---

# 小红书评论回复助手

获取笔记评论，生成温暖简短的回复（100字以内），用户确认后执行。

## 执行前检查

> 登录流程见 [`../_shared/xiaohongshu-login.md`](../_shared/xiaohongshu-login.md)
> 飞书配置见 [`../_shared/feishu-config.md`](../_shared/feishu-config.md)

1. 调用 `mcp__xiaohongshu-mcp__check_login_status` 确认登录
2. 确认飞书可访问（用于保存回复记录）

---

## 输入方式

| 方式 | 示例 |
|------|------|
| 批量查看 | "查看所有评论"、"有新评论吗" |
| 标题搜索 | "回复「黑化后的射手」的评论" |
| 链接/ID | 直接提供笔记链接或 feed_id |

---

## 模式一：批量查看所有笔记评论

触发词："查看所有评论"、"检查新评论"、"有没有新评论"

**流程：**

1. **获取笔记列表**
   - 使用 user_id: `63a4d7e00000000026010ffd`
   - `search_feeds(keyword="射手座生存指南")` 获取 xsec_token
   - `user_profile(user_id, xsec_token)` 获取最近10篇笔记

2. **逐篇获取评论**
   - `get_feed_detail(feed_id, xsec_token, limit=5)`

3. **汇总展示**

   | # | 笔记标题 | 评论数 | 最新评论预览 |
   |---|----------|--------|--------------|
   | 1 | 黑化后的射手 | 5 | "太准了！" |
   | 2 | 射手座配对指南 | 3 | "和天蝎能配吗" |

4. **用户选择**序号查看详情或直接回复

---

## 模式二：单篇笔记评论回复

### Step 1: 获取评论

**标题搜索：** `search_feeds` → 匹配自己账号的笔记 → `get_feed_detail`

**链接/ID：** 解析 `https://www.xiaohongshu.com/explore/{feed_id}` → 通过 `list_feeds` 或 `search_feeds` 获取 xsec_token → `get_feed_detail`

参数：`feed_id`, `xsec_token`, `load_all_comments: true`, `limit: 10`

### Step 2: 分析评论生成回复

对每条评论判断类型：
- **含星座关键词** → 使用 WebSearch 搜索相关知识，生成专业回复
- **其他** → 直接生成温暖简短回复

输出表格：

| # | 评论者 | 评论内容 | 建议回复 | 类型 |
|---|--------|----------|----------|------|
| 1 | 用户A | 说得太对了！ | 谢谢认可～ | 普通 |
| 2 | 用户B | 射手和天蝎能配吗 | 可以的，射手的热情... | 星座 |

### Step 3: 用户确认

展示所有待回复，等待用户选择：全部回复 / 指定序号 / 修改后回复 / 取消

### Step 4: 执行回复并保存

```
mcp__xiaohongshu-mcp__reply_comment_in_feed
  feed_id, xsec_token, comment_id, user_id, content

mcp__lark-mcp__bitable_v1_appTableRecord_create
  fields: 笔记标题, 笔记ID, 评论内容, 评论用户, 回复内容, 回复时间, 是否星座问题
```

---

## 回复风格指南

### 核心原则

回复应该像朋友之间的对话 — 温暖、简短、自然。100字以内，避免说教和模板化表达。

### 按评论类型回复

**普通互动（点赞、认可）：**
- "谢谢你的认可～"
- "哈哈被你发现了"
- "懂的都懂！"
- "握手～"

**星座问题咨询：**
- 先 WebSearch 搜索，再结合知识回复
- "射手确实很注重自由，但真正爱上时会主动为你停留的～"
- "这个问题很多人问过，射手的冷淡通常是在试探你的反应..."

**共鸣分享：**
- "懂你的感受，射手就是这样的矛盾体"
- "同为射手，深有体会"
- "被说中了～"

**负面/质疑评论：**
- "每个人感受不同，谢谢分享你的看法"
- "理解你的观点～"
- "也有道理呢"
- 对负面评论保持温和，争辩只会激化矛盾、伤害账号形象

---

## 星座问题识别关键词

以下关键词出现时触发 WebSearch（确保回复有专业依据）：

- **星座名**：白羊、金牛、双子、巨蟹、狮子、处女、天秤、天蝎、射手、摩羯、水瓶、双鱼
- **配对**：配对、合适、能不能在一起、般配
- **性格**：性格、特点、缺点、优点、黑化、回避、焦虑
- **情感**：喜欢、爱上、分手、复合、冷战、忽冷忽热

---

## 注意事项

- **回复频率**：每条间隔 2-3 秒，避免被平台判定为机器人
- **用户确认优先**：生成回复后等待用户确认，不自动执行
- **记录保存**：每次回复保存到飞书，便于追踪互动历史

---

## 错误处理

| 问题 | 解决 |
|------|------|
| 笔记未找到 | 提示检查标题/链接 |
| 无评论 | 提示"该笔记暂无评论" |
| 回复失败 | 记录原因，继续处理下一条 |
| MCP 未连接 | 提示重连 xiaohongshu-mcp |
