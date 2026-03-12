---
name: feishu-im-read
description: |
  飞书消息读取与搜索。获取群聊/单聊历史消息、读取话题回复、跨会话搜索、下载图片和文件。

  **触发场景**：
  - 用户说"看看聊天记录"、"群里说了什么"、"最近的消息"、"历史消息"
  - 用户说"话题回复"、"看看这个讨论"、"thread 里面说了什么"
  - 用户说"搜索消息"、"找一下谁说过"、"搜一下关键词"
  - 用户说"下载图片"、"下载文件"、"获取附件"
  - 用户提到"聊天"、"消息"、"群消息"、"单聊"、"私聊记录"
  - 需要按时间范围查看消息、翻页获取更多消息
---

# 飞书 IM 消息读取

## 执行前必读

- 以用户身份（user_access_token）调用，只能读取用户有权限的会话
- `feishu_im_user_get_messages` 中 `open_id` 和 `chat_id` 必须二选一
- 消息中有 `thread_id` 时，根据用户意图判断是否展开话题回复
- 消息中出现资源标记时，用 `feishu_im_user_fetch_resource` 下载（需 `message_id` + `file_key` + `type`）

---

## 意图 → 工具

| 用户意图 | 工具 | 必填参数 | 常用可选 |
|---------|------|---------|---------|
| 获取群聊/单聊消息 | feishu_im_user_get_messages | chat_id 或 open_id（二选一） | relative_time, start_time/end_time, page_size, sort_rule |
| 获取话题回复 | feishu_im_user_get_thread_messages | thread_id（omt_xxx） | page_size, sort_rule |
| 跨会话搜索 | feishu_im_user_search_messages | 至少一个过滤条件 | query, sender_ids, chat_id, relative_time, start_time/end_time, page_size |
| 下载图片 | feishu_im_user_fetch_resource | message_id, file_key（img_xxx）, type="image" | - |
| 下载文件/音频/视频 | feishu_im_user_fetch_resource | message_id, file_key（file_xxx）, type="file" | - |

---

## 核心约束

### 1. 时间范围

用户没有明确指定时间时，根据意图推断合适的 `relative_time`，确保消息覆盖完整。用户明确指定时间则直接使用。

### 2. 分页

- `page_size` 范围 1-50，默认 50
- `has_more=true` 时用 `page_token` 翻页
- 需要完整结果时继续翻页，浏览概览时首页通常够用

### 3. 话题回复展开策略

| 场景 | 行为 |
|------|------|
| 需要理解上下文（默认） | 对 thread_id 获取最新 10 条回复（`page_size: 10, sort_rule: "create_time_desc"`） |
| 用户要"完整对话"/"详细讨论" | 获取全部回复（`page_size: 50, sort_rule: "create_time_asc"`），需要时翻页 |
| 用户只浏览概览 / 明确说不看回复 | 跳过话题展开 |

话题消息不支持时间过滤（API 限制），只能通过分页获取。

### 4. 跨会话搜索参数

| 参数 | 说明 |
|------|------|
| `query` | 关键词，匹配消息内容 |
| `sender_ids` | 发送者 open_id 列表 |
| `chat_id` | 限定搜索范围 |
| `mention_ids` | 被@用户的 open_id 列表 |
| `message_type` | file / image / media |
| `sender_type` | user / bot / all（默认 user） |
| `chat_type` | group / p2p |

搜索结果每条消息额外包含 `chat_id`、`chat_type`、`chat_name`。单聊还有 `chat_partner`。

### 5. 资源下载

消息 `content` 中的资源标记需用 `feishu_im_user_fetch_resource` 下载：

| 资源类型 | 标记格式 | fetch 参数 |
|---------|---------|-----------|
| 图片 | `![image](img_xxx)` | type=`"image"`, file_key=`img_xxx` |
| 文件 | `<file key="file_xxx" name="..."/>` | type=`"file"`, file_key=`file_xxx` |
| 音频 | `<audio key="file_xxx" .../>` | type=`"file"`, file_key=`file_xxx` |
| 视频 | `<video key="file_xxx" .../>` | type=`"file"`, file_key=`file_xxx` |

文件大小限制 100MB，不支持表情包和卡片内资源。

### 6. 时间过滤

| 方式 | 参数 | 示例 |
|------|------|------|
| 相对时间 | `relative_time` | `today`、`yesterday`、`this_week`、`last_3_days` |
| 精确时间 | `start_time` + `end_time` | `2026-02-27T00:00:00+08:00` |

两者互斥。可用 relative_time：`today`、`yesterday`、`day_before_yesterday`、`this_week`、`last_week`、`this_month`、`last_month`、`last_{N}_{unit}`（unit: minutes/hours/days）。

### 7. open_id vs chat_id

| 参数 | 格式 | 场景 |
|------|------|------|
| chat_id | `oc_xxx` | 已知会话 ID（群聊或单聊） |
| open_id | `ou_xxx` | 已知用户 ID，获取与该用户的单聊（自动解析） |

两者必须二选一，优先用 `chat_id`。

---

## 常见错误

| 错误现象 | 原因 | 解决 |
|---------|------|------|
| 消息太少 | 时间范围太窄 | 推断合适的 `relative_time` |
| 消息不完整 | 未翻页 | has_more=true 时用 page_token |
| 话题内容不完整 | 未展开 thread_id | 发现 thread_id 时获取回复 |
| "open_id 和 chat_id 不能同时提供" | 同时传了两个 | 只传其中一个 |
| "relative_time 和 start_time/end_time 不能同时使用" | 时间参数冲突 | 选一种方式 |
| 图片/文件下载失败 | file_key 或 message_id 不匹配 | 确认 file_key 来自该 message_id |
