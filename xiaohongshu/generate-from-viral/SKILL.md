---
name: generating-content-from-viral
description: Generates new zodiac poster content by learning from analyzed viral notes in Feishu Bitable. Use when the user wants to create content inspired by successful viral patterns, transform viral note structures into new zodiac content, or batch generate poster ideas from viral references.
---

# 从爆文生成星座海报内容

从飞书"低粉爆文抓取"表获取已分析的爆文，结合小红书MCP获取完整内容，AI智能生成新的星座海报素材，自动写入"星座海报生成"表。

---

## 上下文优化指南

1. **限制处理数量**：默认每次只处理 1 条笔记
2. **精简输出**：不输出完整笔记内容，只输出关键信息和生成结果

---

## 飞书表格配置

> 详细配置见 [`../_shared/feishu-config.md`](../_shared/feishu-config.md)

| 表名 | table_id |
|------|----------|
| 低粉爆文抓取（源表） | `<LARK_VIRAL_NOTES_TABLE_ID>` |
| 星座海报生成（目标表） | `<LARK_BITABLE_TABLE_ID>` |

```
app_token: <LARK_BITABLE_APP_TOKEN>
```

---

## 执行前检查

> 详细登录流程见 [`../_shared/xiaohongshu-login.md`](../_shared/xiaohongshu-login.md)

```
调用 mcp__xiaohongshu-mcp__check_login_status
```

如果未登录，执行扫码登录。

---

## 核心执行流程

### 步骤 1: 从飞书获取爆文记录

**用户指定笔记ID：**

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_search
参数:
- path: {
    app_token: "<LARK_BITABLE_APP_TOKEN>",
    table_id: "<LARK_VIRAL_NOTES_TABLE_ID>"
  }
- data: {
    filter: {
      conjunction: "and",
      conditions: [{
        field_name: "笔记ID",
        operator: "is",
        value: ["<用户指定的笔记ID>"]
      }]
    }
  }
```

**保存关键信息：**
- `record_id` - 源记录ID
- `笔记ID` - 用于获取详情
- `xsec_token` - 访问令牌
- `备注` - AI分析结果

### 步骤 2: 获取小红书笔记完整内容

```
调用 mcp__xiaohongshu-mcp__get_feed_detail
参数:
- feed_id: "<笔记ID>"
- xsec_token: "<xsec_token>"
- load_all_comments: false
```

**提取信息：**
- 完整正文内容
- 标题
- 互动数据（点赞、收藏、评论）

### 步骤 3: AI 智能提取星座

**星座识别规则（按优先级）：**
1. 标题中包含的星座名称
2. 正文中提到最多的星座
3. 星座别名映射：射手/人马座 → 射手座

**12星座列表：**
白羊座、金牛座、双子座、巨蟹座、狮子座、处女座、天秤座、天蝎座、射手座、摩羯座、水瓶座、双鱼座

### 步骤 4: AI 生成星座海报内容

**使用以下提示词生成：**

```
你是一位小红书星座内容创作专家。请参考以下爆文，生成一套全新的星座海报内容。

【参考爆文】
标题：{title}
内容：{content}
互动：点赞 {likes} | 收藏 {favorites} | 评论 {comments}
爆款分析：{analysis}

【目标星座】{zodiac}

请生成以下内容（必须是全新原创，不能复制原文）：

## 1. 海报标题（10-15字）
- 直接点名星座，让人一眼看出是写给谁的
- 类型：公式型 / 悬念型 / 情绪型 / 主题型
- 爆款公式：年份/主题 + 情绪词 + 星座名
- 示例：
  - "2026年最值得期待的星座：射手座"
  - "射手座的孤独，其实是一种自由"
  - "射手座2026：这一年，轮到你顺了"

## 2. 副标题（10-20字，可选）
- 补充说明或引发好奇
- 如果主标题已完整，可以留空

## 3. 正文内容（5段式，用于生成5张海报）
- **固定5段**，每段约50字（共250字左右）
- 每段独立成页，适合套图海报
- 结构建议：
  - 第1段：点题/核心观点
  - 第2段：展开/具体表现
  - 第3段：深入/细节描写
  - 第4段：转折/反思
  - 第5段：收尾/提问留钩子

## 4. 用途建议
- 封面布局（标题为主）
- 长文案布局（正文为主）
- 套图（封面+多页内容）**← 5段式默认选此项**

## 5. 小红书文案（200字左右，用于发布时配文）

**核心要求：有人味但不浮躁，亲昵但不轻浮**

风格定位：
| 要素 | 正确 | 错误 |
|------|------|------|
| 人味 | "我们射手座啊" | "射手宝宝们集合！" |
| 亲昵 | "你遇到的是哪一种" | "姐妹们快来看！" |
| 情感 | "心里有本账" | "太扎心了呜呜呜" |
| 语气 | "转身比谁都快" | "说走就走超酷的！" |

过AI检测技巧：
- 增加不完美感："emmm怎么说呢"、"好像是这样"
- 加入主观视角："说实话"、"其实早就"
- 使用不规则标点：破折号代替逗号、适当用"..."留白
- 避免AI腔调：不要"首先...其次..."、不要过于工整的排比

禁止：
- ❌ "宝子们"、"姐妹们"等浮夸称呼
- ❌ "点赞收藏不迷路"等引导语
- ❌ 过多感叹号！！！
- ❌ "太真实了"、"爱死了"等网络热词

请以 JSON 格式输出：
{
  "标题": "xxx（10-15字，直接点名星座）",
  "副标题": "xxx 或留空",
  "正文内容": "第一段内容\n\n第二段内容\n\n第三段内容\n\n第四段内容\n\n第五段内容",
  "星座": "{zodiac}",
  "用途": "套图",
  "小红书文案": "xxx（200字左右，有人味但不浮躁）"
}
```

### 步骤 5: 写入飞书"星座海报生成"表

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_create
参数:
- path: {
    app_token: "<LARK_BITABLE_APP_TOKEN>",
    table_id: "<LARK_BITABLE_TABLE_ID>"
  }
- data: {
    fields: {
      "标题": "<生成的标题，10-15字>",
      "副标题": "<生成的副标题>",
      "正文内容": "<5段式正文，每段约50字>",
      "星座": "<提取的星座>",
      "用途": "套图",
      "小红书文案": "<200字左右的发布文案>"
    }
  }
```

---

## MCP 工具调用顺序

```
1. mcp__xiaohongshu-mcp__check_login_status
   └── 检查登录状态

2. mcp__lark-mcp__bitable_v1_appTableRecord_search
   └── 从源表获取爆文记录

3. mcp__xiaohongshu-mcp__get_feed_detail
   └── 获取笔记完整内容

4. [AI处理] 提取星座 + 生成内容

5. mcp__lark-mcp__bitable_v1_appTableRecord_create
   └── 写入目标表
```

---

## 使用示例

### 示例 1: 指定笔记ID生成

```
用户: /generate-from-viral 694b4645000000001f00d682

Claude:
1. 从飞书查找该笔记ID的记录
2. 获取小红书完整内容
3. 提取星座：射手座
4. AI生成海报内容
5. 写入飞书"星座海报生成"表
6. 返回生成结果预览
```

### 示例 2: 简短触发

```
用户: 从爆文生成内容，笔记ID是 xxx

Claude: 按上述流程执行
```

---

## 输出格式

```
已从爆文生成星座海报内容！

【参考爆文】
- 标题: {原标题}
- 点赞: {likes} | 收藏: {favorites}

【生成内容】
| 字段 | 内容 |
|------|------|
| 星座 | 射手座 |
| 标题 | {10-15字标题} |
| 副标题 | {副标题} |
| 用途 | 套图 |

【正文内容（5段式）】
第1段：{点题}
第2段：{展开}
第3段：{深入}
第4段：{转折}
第5段：{收尾+钩子}

【小红书文案】
{200字左右，有人味但不浮躁}

已写入飞书「星座海报生成」表
```

---

## 错误处理

### 笔记ID不存在
```
症状：在飞书表中找不到该笔记ID
解决：提示用户检查ID是否正确，或先执行爆文抓取
```

### xsec_token 过期
```
症状：获取笔记详情失败
解决：使用飞书表中的"内容摘要"和"备注"字段作为替代
```

### 无法识别星座
```
症状：内容中没有明确的星座信息
解决：询问用户指定星座
```

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `generate-from-viral/SKILL.md` | 本技能文档 |
| `analyze-viral-notes/SKILL.md` | 爆文分析技能 |
| `generate-copywriting/SKILL.md` | 文案风格指南 |
| `config.py` | 飞书表格配置 |
