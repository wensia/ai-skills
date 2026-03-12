---
name: generating-content-from-viral
description: Generates new zodiac poster content by learning from analyzed viral notes stored in Feishu Bitable. Use this skill whenever the user wants to create content inspired by viral patterns, generate zodiac posts, transform successful note structures into new content, batch produce poster ideas, write XHS copy from reference material, or create star sign content — even if they don't explicitly mention "generate from viral". Triggers on keywords like 生成内容, 爆文参考, 星座海报, 写文案, 从爆文学习.
---

# 从爆文生成星座海报内容

从飞书"低粉爆文抓取"表获取已分析的爆文，通过小红书 MCP 获取完整内容，AI 生成新的星座海报素材，写入"星座海报生成"表。

## 上下文优化

- 默认每次只处理 **1 条**笔记（避免上下文溢出）
- 不输出完整笔记内容，只输出关键信息和生成结果

---

## 配置

> 飞书详细配置见 [`../_shared/feishu-config.md`](../_shared/feishu-config.md)
> 登录流程见 [`../_shared/xiaohongshu-login.md`](../_shared/xiaohongshu-login.md)

```
app_token: <LARK_BITABLE_APP_TOKEN>
源表 (低粉爆文抓取): <LARK_VIRAL_NOTES_TABLE_ID>
目标表 (星座海报生成): <LARK_BITABLE_TABLE_ID>
```

执行前调用 `mcp__xiaohongshu-mcp__check_login_status` 确认登录。

---

## 执行流程

### 1. 从飞书获取爆文记录

```
mcp__lark-mcp__bitable_v1_appTableRecord_search
  path: { app_token, table_id: <LARK_VIRAL_NOTES_TABLE_ID> }
  data:
    filter:
      conjunction: "and"
      conditions:
        - field_name: "笔记ID"
          operator: "is"
          value: ["<用户指定的笔记ID>"]
```

保存：`record_id`、`笔记ID`、`xsec_token`、`备注`（AI分析结果）

### 2. 获取小红书笔记完整内容

```
mcp__xiaohongshu-mcp__get_feed_detail
  feed_id: "<笔记ID>"
  xsec_token: "<xsec_token>"
  load_all_comments: false
```

提取：完整正文、标题、互动数据。

### 3. AI 提取星座

按优先级识别：
1. 标题中的星座名称
2. 正文中出现最多的星座
3. 别名映射（射手/人马座 → 射手座）

12星座：白羊、金牛、双子、巨蟹、狮子、处女、天秤、天蝎、射手、摩羯、水瓶、双鱼

无法识别时直接询问用户。

### 4. AI 生成海报内容

使用以下提示词：

```
你是一位小红书星座内容创作专家。请参考以下爆文，生成一套全新的星座海报内容。

【参考爆文】
标题：{title}
内容：{content}
互动：点赞 {likes} | 收藏 {favorites} | 评论 {comments}
爆款分析：{analysis}

【目标星座】{zodiac}

请生成以下内容（全新原创，不能复制原文）：

## 1. 海报标题（10-15字）
- 直接点名星座
- 爆款公式：年份/主题 + 情绪词 + 星座名

## 2. 副标题（10-20字，可选）

## 3. 正文内容（5段式，每段约50字，共250字）
每段独立成页，适合套图海报：
- 第1段：点题/核心观点
- 第2段：展开/具体表现
- 第3段：深入/细节描写
- 第4段：转折/反思
- 第5段：收尾/提问留钩子

## 4. 用途建议
5段式默认选"套图"

## 5. 小红书文案（200字左右）

风格要求 — 有人味但不浮躁，亲昵但不轻浮：
| 要素 | 正确示范 | 应避免 |
|------|----------|--------|
| 人味 | "我们射手座啊" | "射手宝宝们集合！" |
| 亲昵 | "你遇到的是哪一种" | "姐妹们快来看！" |
| 情感 | "心里有本账" | "太扎心了呜呜呜" |
| 语气 | "转身比谁都快" | "说走就走超酷的！" |

过AI检测技巧（让文案读起来更自然）：
- 增加不完美感："emmm怎么说呢"、"好像是这样"
- 加入主观视角："说实话"、"其实早就"
- 使用不规则标点：破折号代替逗号、适当用"..."留白

应避免（这些表达会让读者感觉是机器写的）：
- "宝子们"、"姐妹们"等浮夸称呼
- "点赞收藏不迷路"等引导语
- 过多感叹号
- "首先...其次..."等工整排比

请以 JSON 格式输出：
{
  "标题": "xxx",
  "副标题": "xxx 或留空",
  "正文内容": "第一段\n\n第二段\n\n第三段\n\n第四段\n\n第五段",
  "星座": "{zodiac}",
  "用途": "套图",
  "小红书文案": "xxx"
}
```

### 5. 写入飞书

```
mcp__lark-mcp__bitable_v1_appTableRecord_create
  path: { app_token, table_id: <LARK_BITABLE_TABLE_ID> }
  data:
    fields: { 标题, 副标题, 正文内容, 星座, 用途, 小红书文案 }
```

---

## 输出格式

```
已从爆文生成星座海报内容！

【参考爆文】标题: {原标题} | 点赞: {likes} | 收藏: {favorites}

【生成内容】
| 字段 | 内容 |
|------|------|
| 星座 | 射手座 |
| 标题 | {标题} |
| 副标题 | {副标题} |
| 用途 | 套图 |

【正文（5段式）】
第1段：{点题}
第2段：{展开}
第3段：{深入}
第4段：{转折}
第5段：{收尾}

【小红书文案】
{200字文案}

已写入飞书「星座海报生成」表
```

---

## 错误处理

| 问题 | 解决 |
|------|------|
| 笔记ID不存在 | 提示用户检查ID，或先执行爆文抓取 |
| xsec_token 过期 | 用飞书表中"内容摘要"和"备注"字段作为替代 |
| 无法识别星座 | 直接询问用户指定星座 |
