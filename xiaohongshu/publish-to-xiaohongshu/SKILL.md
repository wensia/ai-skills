---
name: publish-to-xiaohongshu
description: Publishes content to Xiaohongshu (XHS/Little Red Book) and marks the Feishu Bitable record as published. Use this skill whenever the user wants to post content to XHS, publish a note, upload images to Xiaohongshu, send zodiac posters live, batch publish ready content, or push generated content to their XHS account — even if they don't say "publish". Triggers on keywords like 发布, 发小红书, 上线, 推送, 发帖, post.
---

# 小红书发布器

通过 xiaohongshu-mcp 发布内容到小红书，发布成功后自动标记飞书记录为已发布。

## 执行前检查

调用 `mcp__xiaohongshu-mcp__check_login_status` 确认登录。未登录时：
```bash
cd ./xiaohongshu-mcp && ./xiaohongshu-login-darwin-arm64
```

## 飞书配置

> 详细配置见 [`../_shared/feishu-config.md`](../_shared/feishu-config.md)

```
app_token: <LARK_BITABLE_APP_TOKEN>
table_id: <LARK_BITABLE_TABLE_ID>
```

关键字段：标题、正文内容、小红书文案（优先使用）、生成图片路径、已生成、**已发布**

---

## 发布流程

### 1. 从飞书获取记录

```python
import requests

# 获取 token
token_resp = requests.post(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={"app_id": "<LARK_APP_ID>", "app_secret": "<LARK_APP_SECRET>"}
)
token = token_resp.json()["tenant_access_token"]

# 查询记录
resp = requests.post(
    f"https://open.feishu.cn/open-apis/bitable/v1/apps/<LARK_BITABLE_APP_TOKEN>/tables/<LARK_BITABLE_TABLE_ID>/records/search",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"filter": {"conjunction": "and", "conditions": [
        {"field_name": "标题", "operator": "contains", "value": ["<标题>"]}
    ]}}
)
record = resp.json()["data"]["items"][0]
record_id = record["record_id"]  # 后续标记已发布时需要
```

### 2. 准备发布内容

**标题（20字以内）：** 直接使用记录标题，超长时提炼核心卖点。

**正文优先级：**
1. "小红书文案"字段（如果有内容）
2. AI 根据"正文内容"生成 100-200 字文案

**话题标签（3-5个）：**
- 必选：具体星座名、"星座"、"12星座"
- 按主题追加：配对→星座配对、性格→星座性格、发疯→发疯文学

### 3. 发布到小红书

```
mcp__xiaohongshu-mcp__publish_content
  title: "标题"          # 20字以内
  content: "正文"
  images: ["/abs/path/01.png", "/abs/path/02.png"]  # 本地绝对路径
  tags: ["射手座", "星座", "发疯文学"]               # 可选
```

### 4. 标记飞书记录已发布

发布成功后立即更新飞书（避免重复发布）：

```python
update_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{RECORD_ID}"
resp = requests.put(update_url,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"fields": {"已发布": True}}
)
```

如果标记失败，记录 record_id 提示用户手动勾选，不影响发布成功状态。

---

## 文案生成指南

当"小红书文案"字段为空时，AI 根据正文内容生成。

**风格要求 — 自然口语化，避免 AI 腔调：**
- 加入个人视角："我发现..."、"说实话..."
- 使用不完美表达："emmm"、"有点"、"好像"
- 适当省略主语，用短句
- 加入情绪词："笑死"、"真的会"

**示例模板：**
```
{星座}就是这样的存在

说实话，{核心特点}这件事，{星座}真的太典了

{展开描述，1-2句}

{口语化补充}

所以别怪我们{行为}，这就是{星座}的日常啊
```

---

## 平台限制

| 项目 | 限制 |
|------|------|
| 标题 | 20字以内 |
| 正文 | 1000字以内 |
| 图片 | 1-18张，PNG/JPG，本地绝对路径 |
| 每日发帖 | 建议50篇以内 |

---

## 错误处理

| 问题 | 解决 |
|------|------|
| 未登录 | 运行登录工具扫码 |
| 图片路径无效 | 确保使用绝对路径 |
| 发布失败 | 检查标题长度、账号限流、图片是否存在 |
| 飞书标记失败 | 记录 record_id，提示手动勾选 |
