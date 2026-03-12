---
name: feishu-task
description: |
  飞书任务和清单（Tasklist）的完整管理工具。当用户需要创建、查询、更新、完成任务，或管理任务清单时使用此 skill。触发场景包括用户说"创建任务"、"新建待办"、"查看我的任务"、"完成任务"、"任务清单"、"to-do"、"task"，或任何涉及飞书任务管理的需求 -- 即使用户只说"帮我建个待办"或"看看还有什么没做完"。
---

# 飞书任务管理

## 执行前必读

- **时间格式**：ISO 8601 / RFC 3339（带时区），如 `2026-02-28T17:00:00+08:00`
- **current_user_id 强烈建议传入**：从消息上下文的 SenderId 获取（ou_...）。工具会自动将创建者添加为 follower，确保创建者始终可以编辑任务。不传此参数且 members 中不包含自己时，创建后将无法编辑该任务
- **patch/get 必须传** task_guid
- **tasklist.tasks 必须传** tasklist_guid
- **完成任务**：completed_at = `"2026-02-26 15:30:00"`
- **反完成（恢复未完成）**：completed_at = `"0"`（字符串 "0"，不是数字）

---

## 快速索引：意图 -> 工具 -> 必填参数

| 用户意图 | 工具 | action | 必填参数 | 常用可选 |
|---------|------|--------|---------|---------|
| 新建待办 | feishu_task_task | create | summary | current_user_id, members, due, description |
| 查未完成任务 | feishu_task_task | list | - | completed=false, page_size |
| 获取任务详情 | feishu_task_task | get | task_guid | - |
| 完成任务 | feishu_task_task | patch | task_guid, completed_at | - |
| 反完成任务 | feishu_task_task | patch | task_guid, completed_at="0" | - |
| 改截止时间 | feishu_task_task | patch | task_guid, due | - |
| 创建清单 | feishu_task_tasklist | create | name | members |
| 查看清单任务 | feishu_task_tasklist | tasks | tasklist_guid | completed |
| 添加清单成员 | feishu_task_tasklist | add_members | tasklist_guid, members[] | - |

---

## 核心约束

### 用户身份与权限

工具使用 `user_access_token`（用户身份），这意味着：
- 创建任务时可以指定任意成员
- 只能查看和编辑自己是成员的任务
- 如果创建时没把自己加入成员，后续无法编辑该任务

传入 `current_user_id` 后，工具会自动将创建者添加为 follower，避免失去编辑权限。

### 任务成员角色

- **assignee（负责人）**：负责完成任务，可编辑
- **follower（关注人）**：关注进展，接收通知

```json
{
  "members": [
    {"id": "ou_xxx", "role": "assignee"},
    {"id": "ou_yyy", "role": "follower"}
  ]
}
```

`id` 使用用户的 `open_id`（从消息上下文的 SenderId 获取）。

### 清单角色冲突

创建人自动成为清单 owner。如果 `members` 中包含创建人，该用户会被提升为 owner 并从 members 中移除（同一用户只能有一个角色）。因此不要在 `members` 中包含创建人。

### 清单成员角色

| 成员类型 | 角色 | 说明 |
|---------|------|------|
| user | owner | 所有者，可转让 |
| user | editor | 可编辑清单和任务 |
| user | viewer | 只读 |
| chat（群组） | editor/viewer | 整个群组获得权限 |

---

## 使用场景示例

### 创建任务并分配负责人

```json
{
  "action": "create",
  "summary": "准备周会材料",
  "description": "整理本周工作进展和下周计划",
  "current_user_id": "ou_发送者的open_id",
  "due": {
    "timestamp": "2026-02-28 17:00:00",
    "is_all_day": false
  },
  "members": [
    {"id": "ou_协作者的open_id", "role": "assignee"}
  ]
}
```

### 查询未完成任务

```json
{
  "action": "list",
  "completed": false,
  "page_size": 20
}
```

### 完成任务

```json
{
  "action": "patch",
  "task_guid": "任务的guid",
  "completed_at": "2026-02-26 15:30:00"
}
```

### 反完成任务

```json
{
  "action": "patch",
  "task_guid": "任务的guid",
  "completed_at": "0"
}
```

### 创建清单并添加协作者

```json
{
  "action": "create",
  "name": "产品迭代 v2.0",
  "members": [
    {"id": "ou_xxx", "role": "editor"},
    {"id": "ou_yyy", "role": "viewer"}
  ]
}
```

### 将任务加入清单

创建任务时指定 `tasklists` 参数：

```json
{
  "action": "create",
  "summary": "任务标题",
  "tasklists": [
    {
      "tasklist_guid": "清单的guid",
      "section_guid": "分组的guid（可选）"
    }
  ]
}
```

### 重复任务

使用 `repeat_rule` 参数（RRULE 格式），只有设置了截止时间的任务才能设置重复规则：

```json
{
  "action": "create",
  "summary": "每周例会",
  "due": {"timestamp": "2026-03-03 14:00:00", "is_all_day": false},
  "repeat_rule": "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO"
}
```

---

## 常见错误与排查

| 错误现象 | 原因 | 解决方案 |
|---------|------|---------|
| 创建后无法编辑任务 | 创建时未将自己加入 members | 传 current_user_id，或将当前用户加为 assignee/follower |
| patch 失败提示 task_guid 缺失 | 未传 task_guid | patch/get 必须传 task_guid |
| tasks 失败提示 tasklist_guid 缺失 | 未传 tasklist_guid | tasklist.tasks 必须传 tasklist_guid |
| 反完成失败 | completed_at 格式错误 | 使用字符串 `"0"`，不是数字 0 |
| 时间不对 | 使用了 Unix 时间戳 | 改用 ISO 8601 格式：`2024-01-01T00:00:00+08:00` |

---

## 附录

### 资源关系

```
任务清单（Tasklist）
  +-- 自定义分组（Section，可选）
      +-- 任务（Task）
          +-- 成员：负责人（assignee）、关注人（follower）
          +-- 子任务（Subtask）
          +-- 截止时间（due）、开始时间（start）
          +-- 附件、评论
```

### 获取 GUID

- **task_guid**：创建任务后从返回值的 `task.guid` 获取，或通过 `list` 查询
- **tasklist_guid**：创建清单后从返回值的 `tasklist.guid` 获取，或通过 `list` 查询

### 数据权限

- 只能操作自己是成员的任务和清单
- 将任务加入清单需要同时拥有任务和清单的编辑权限
