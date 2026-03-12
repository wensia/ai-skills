---
name: publish-to-xiaohongshu
description: 使用 xiaohongshu-mcp 发布内容到小红书，发布成功后自动标记飞书记录为已发布。
---

# 小红书发布器（xiaohongshu-mcp）

使用 xiaohongshu-mcp 工具发布内容到小红书，发布成功后自动标记飞书多维表格的"已发布"字段。

---

## 核心工具

本 skill 使用 `xiaohongshu-mcp` MCP 服务，主要工具：

| 工具名 | 功能 | 必需参数 |
|--------|------|----------|
| `mcp__xiaohongshu-mcp__check_login_status` | 检查登录状态 | 无 |
| `mcp__xiaohongshu-mcp__publish_content` | 发布图文 | title, content, images |
| `mcp__xiaohongshu-mcp__publish_with_video` | 发布视频 | title, content, video |

---

## 飞书配置

```
app_token: <LARK_BITABLE_APP_TOKEN>
table_id: <LARK_BITABLE_TABLE_ID>
```

### 关键字段

| 字段 | 说明 |
|------|------|
| 标题 | 海报标题 |
| 正文内容 | 套图正文（用于生成小红书文案） |
| 小红书文案 | 预设的发布文案（优先使用） |
| 生成图片路径 | 本地图片目录路径 |
| 已生成 | 图片是否已生成 |
| **已发布** | **发布成功后必须标记为 true** |

---

## 完整发布流程

```
┌─────────────────────────────────────────────────────────────┐
│                    小红书发布完整流程                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 检查小红书登录状态                                        │
│     └── mcp__xiaohongshu-mcp__check_login_status            │
│                    ↓                                        │
│  2. 从飞书拉取记录                                           │
│     ├── 保存 record_id（必须！用于后续标记已发布）            │
│     ├── 获取图片路径                                         │
│     └── 获取文案内容                                         │
│                    ↓                                        │
│  3. 准备发布内容                                             │
│     ├── 标题（≤20字）                                       │
│     ├── 正文（优先用"小红书文案"字段，否则 AI 生成）          │
│     ├── 图片数组                                            │
│     └── 话题标签（3-5个）                                    │
│                    ↓                                        │
│  4. 发布到小红书                                             │
│     └── mcp__xiaohongshu-mcp__publish_content               │
│                    ↓                                        │
│  5. ⚠️ 【必须】标记飞书记录已发布                            │
│     ├── 更新「已发布」= true                                 │
│     └── 使用 Python requests 调用飞书 API                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 步骤详解

### 步骤 1: 检查登录状态

```
调用: mcp__xiaohongshu-mcp__check_login_status
```

如果未登录，提示用户：
```bash
cd ./xiaohongshu-mcp
./xiaohongshu-login-darwin-arm64
```

### 步骤 2: 从飞书获取记录

```python
import requests

# 获取 token
token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
token_resp = requests.post(token_url, json={
    "app_id": "<LARK_APP_ID>",
    "app_secret": "<LARK_APP_SECRET>"
})
token = token_resp.json()["tenant_access_token"]

# 查询记录
search_url = "https://open.feishu.cn/open-apis/bitable/v1/apps/<LARK_BITABLE_APP_TOKEN>/tables/<LARK_BITABLE_TABLE_ID>/records/search"
resp = requests.post(search_url,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={
        "filter": {
            "conjunction": "and",
            "conditions": [{
                "field_name": "标题",
                "operator": "contains",
                "value": ["<用户指定的标题>"]
            }]
        }
    }
)
record = resp.json()["data"]["items"][0]
record_id = record["record_id"]  # ⚠️ 必须保存！
```

### 步骤 3: 准备发布内容

**标题规则（≤20字）：**
- 直接使用记录标题
- 或提炼核心卖点

**正文来源优先级：**
1. 优先使用"小红书文案"字段内容
2. 如果为空，AI 根据"正文内容"生成（100-200字）

**话题标签（3-5个）：**
```python
# 根据内容自动生成
tags = ["射手座", "星座", "12星座"]  # 必选
# 根据主题添加
if "配对" in content: tags.append("星座配对")
if "性格" in content: tags.append("星座性格")
```

### 步骤 4: 发布到小红书

```
调用: mcp__xiaohongshu-mcp__publish_content
参数:
- title: "射手座的发疯文学语录"  # ≤20字
- content: "发疯是一种解压方式..."  # 正文
- images: ["/path/to/01.png", "/path/to/02.png", ...]  # 本地绝对路径
- tags: ["射手座", "星座", "发疯文学"]  # 可选
```

### 步骤 5: ⚠️ 【必须】标记飞书记录已发布

**发布成功后，必须立即更新飞书记录！**

```python
import requests

APP_TOKEN = "<LARK_BITABLE_APP_TOKEN>"
TABLE_ID = "<LARK_BITABLE_TABLE_ID>"
RECORD_ID = "<之前保存的 record_id>"

# 获取 token
token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
token_resp = requests.post(token_url, json={
    "app_id": "<LARK_APP_ID>",
    "app_secret": "<LARK_APP_SECRET>"
})
token = token_resp.json()["tenant_access_token"]

# 更新记录
update_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{RECORD_ID}"
resp = requests.put(
    update_url,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={
        "fields": {
            "已发布": True
        }
    }
)

if resp.json().get("code") == 0:
    print("✅ 飞书记录已标记为已发布")
else:
    print(f"❌ 标记失败: {resp.json()}")
```

---

## 使用示例

### 发布指定记录

```
用户: 发布"射手座的发疯文学语录"到小红书

Claude 执行:
1. 检查登录状态 → mcp__xiaohongshu-mcp__check_login_status
2. 从飞书查询记录 → 获取 record_id, 图片路径, 文案
3. 发布到小红书 → mcp__xiaohongshu-mcp__publish_content
4. 标记飞书记录已发布 → Python requests 更新
```

### 批量发布

```
用户: 发布所有已生成但未发布的记录

Claude 执行:
1. 查询飞书: 已生成=true AND 已发布=false
2. 遍历每条记录:
   - 发布到小红书
   - 标记已发布
3. 输出发布报告
```

---

## 文案生成规则

### 标题（≤20字）

```
原标题: 射手座的发疯文学语录
小红书标题: 射手座的发疯文学语录  # 直接使用，刚好20字内

原标题: 射手座遇到处女座会怎样相处
小红书标题: 射手遇处女：相处模式大揭秘  # 提炼核心
```

### 正文（100-200字）

**防 AI 检测技巧：**
- 加入个人视角："我发现..."、"说实话..."
- 使用不完美表达："emmm"、"有点"、"好像"
- 适当省略主语
- 用短句，避免长复合句
- 加入情绪词："笑死"、"真的会"、"太真实"

**模板示例：**
```
{星座}就是这样的存在

说实话，{核心特点}这件事，{星座}真的太典了

{展开描述1，1-2句}

{展开描述2，口语化}

所以别怪我们{行为}，这就是{星座}的日常啊
```

---

## 话题标签规则

### 必选标签
- 具体星座名（如"射手座"）
- "星座"
- "12星座"

### 主题标签

| 主题 | 推荐标签 |
|------|----------|
| 配对 | 星座配对、恋爱 |
| 性格 | 星座性格、性格分析 |
| 黑化 | 星座黑化、反差 |
| 情感 | 情感、恋爱 |
| 发疯 | 发疯文学、精神状态 |

### 标签数量
- 推荐 3-5 个
- 不超过 8 个

---

## 发布限制

| 限制项 | 限制值 |
|--------|--------|
| 标题长度 | ≤ 20 字 |
| 正文长度 | ≤ 1000 字 |
| 图片数量 | 1-18 张 |
| 图片格式 | PNG/JPG |
| 图片来源 | 本地绝对路径 |
| 每日发帖量 | ≤ 50 篇（建议） |

---

## 错误处理

### 小红书未登录

```bash
cd ./xiaohongshu-mcp
./xiaohongshu-login-darwin-arm64
```

### 图片路径无效

确保使用绝对路径，如：
```
./output/发疯文学语录/01_封面.png
```

### 发布失败

检查：
1. 标题是否超过 20 字
2. 账号是否被限流
3. 图片是否存在

### 飞书标记失败

如果 API 调用失败：
1. 记录失败的 record_id
2. 提示用户手动勾选"已发布"
3. 不影响发布成功的状态

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `publish-to-xiaohongshu/SKILL.md` | 本技能文档 |
| `_shared/feishu-config.md` | 飞书配置 |
| `xiaohongshu-mcp/` | 小红书 MCP 服务 |
| `xiaohongshu-mcp/cookies.json` | 登录凭证 |

---

## 参考

- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
