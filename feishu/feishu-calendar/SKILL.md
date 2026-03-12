---
name: feishu-calendar
description: |
  飞书日历与日程管理。创建会议、查询日程、修改日程、邀请参会人、查忙闲、回复邀请。

  **触发场景**：
  - 用户说"创建会议"、"约个会"、"安排日程"、"帮我建一个会议"
  - 用户说"查日程"、"看看我的安排"、"这周有什么会"、"搜一下会议"
  - 用户说"改时间"、"推迟会议"、"修改日程"
  - 用户说"邀请某人参会"、"加参会人"、"删除参会人"
  - 用户说"查忙闲"、"看看谁有空"、"找空闲时间"
  - 用户说"接受邀请"、"拒绝会议"、"回复日程"
  - 用户提到"会议室"、"预约会议室"
  - 任何涉及飞书日历、日程、参会人、忙闲的操作
---

# 飞书日历管理

## 执行前必读

- **时区**：Asia/Shanghai（UTC+8），时间格式 ISO 8601，如 `2026-02-25T14:00:00+08:00`
- **create 必填**：summary, start_time, end_time
- **user_open_id**：强烈建议从 SenderId 获取（ou_xxx），确保发起人作为参会人出现
- **ID 格式**：用户 `ou_...`，群 `oc_...`，会议室 `omm_...`，邮箱 `email@...`

---

## 意图 → 工具 → 参数

| 用户意图 | 工具 | action | 必填参数 | 强烈建议 | 常用可选 |
|---------|------|--------|---------|---------|---------|
| 创建会议 | feishu_calendar_event | create | summary, start_time, end_time | user_open_id | attendees, description, location |
| 查时间段日程 | feishu_calendar_event | list | start_time, end_time | - | - |
| 改日程 | feishu_calendar_event | patch | event_id, start_time/end_time | - | summary, description |
| 搜关键词找会 | feishu_calendar_event | search | query | - | - |
| 回复邀请 | feishu_calendar_event | reply | event_id, rsvp_status | - | - |
| 查重复日程实例 | feishu_calendar_event | instances | event_id, start_time, end_time | - | - |
| 查忙闲 | feishu_calendar_freebusy | list | time_min, time_max, user_ids[] | - | - |
| 邀请参会人 | feishu_calendar_event_attendee | create | calendar_id, event_id, attendees[] | - | - |
| 删除参会人 | feishu_calendar_event_attendee | batch_delete | calendar_id, event_id, user_open_ids[] | - | - |

---

## 核心约束

### 1. 为什么要传 user_open_id？

日程创建在用户主日历上，用户能看到，但**不会自动成为参会人**。传 `user_open_id` 后：
- 发起人收到通知、可回复 RSVP、出现在参会人列表中
- 不传则发起人不在参会人列表，不符合常规预期

### 2. 参会人权限（attendee_ability）

工具已默认 `can_modify_event`（参会人可编辑日程和管理参与者）。

| 值 | 能力 |
|----|------|
| `none` | 无权限 |
| `can_see_others` | 可查看参与人列表 |
| `can_invite_others` | 可邀请他人 |
| `can_modify_event` | 可编辑日程（默认） |

### 3. 统一使用 open_id（ou_ 格式）

- 创建日程：`user_open_id = SenderId`
- 邀请参会人：`attendees[].id = "ou_xxx"`
- 删除参会人：`user_open_ids = ["ou_xxx"]`（直接传 open_id）

注意区分：`ou_xxx` 是用户 open_id（应使用的），`user_xxx` 是日程内部 attendee_id（仅内部记录）。

### 4. 会议室预约是异步的

添加会议室参会人后进入异步预约：API 返回 `rsvp_status: "needs_action"`（预约中），最终变为 `accept`（成功）或 `decline`（失败）。用 `feishu_calendar_event_attendee.list` 查询结果。

### 5. instances 仅对重复日程有效

先用 `get` 获取日程详情，确认有 `recurrence` 字段后才能调用 `instances`。对普通日程调用会报错。

---

## 使用示例

### 创建会议并邀请参会人

```json
{
  "action": "create",
  "summary": "项目复盘会议",
  "description": "讨论 Q1 项目进展",
  "start_time": "2026-02-25 14:00:00",
  "end_time": "2026-02-25 15:30:00",
  "user_open_id": "ou_aaa",
  "attendees": [
    {"type": "user", "id": "ou_bbb"},
    {"type": "user", "id": "ou_ccc"},
    {"type": "resource", "id": "omm_xxx"}
  ]
}
```

### 查询未来一周日程

```json
{
  "action": "list",
  "start_time": "2026-02-25 00:00:00",
  "end_time": "2026-03-03 23:59:00"
}
```

### 查忙闲（支持 1-10 个用户）

```json
{
  "action": "list",
  "time_min": "2026-02-25 09:00:00",
  "time_max": "2026-02-25 18:00:00",
  "user_ids": ["ou_aaa", "ou_bbb", "ou_ccc"]
}
```

---

## 常见错误

| 错误现象 | 原因 | 解决 |
|---------|------|------|
| 发起人不在参会人列表 | 未传 `user_open_id` | 传 `user_open_id = SenderId` |
| 时间不对 | 用了 Unix 时间戳 | 改用 ISO 8601：`2024-01-01T00:00:00+08:00` |
| 会议室显示"预约中" | 异步预约未完成 | 等待后用 `list` 查询 `rsvp_status` |
| 修改日程报权限错误 | 非组织者且无编辑权限 | 创建时设置 `attendee_ability: "can_modify_event"` |

---

## 附录

### 参会人类型

| type | id 格式 | 说明 |
|------|---------|------|
| `user` | `ou_xxx` | 飞书用户 |
| `chat` | `oc_xxx` | 飞书群组 |
| `resource` | `omm_xxx` | 会议室 |
| `third_party` | `email@...` | 外部邮箱 |

### 日历类型

| 类型 | 可删除 | 可修改 |
|------|--------|--------|
| `primary`（主日历） | 否 | 是 |
| `shared`（共享日历） | 是 | 是 |
| `resource`（会议室） | 否 | 否 |

### RSVP 状态

| 状态 | 用户含义 | 会议室含义 |
|------|---------|-----------|
| `needs_action` | 未回复 | 预约中 |
| `accept` | 已接受 | 预约成功 |
| `tentative` | 待定 | - |
| `decline` | 拒绝 | 预约失败 |
| `removed` | 已移除 | 已移除 |

### 使用限制

- 每个日程最多 3000 名参会人
- 单次添加用户上限 1000 人，会议室 100 个
- 主日历不可删除
