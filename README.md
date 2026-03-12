# ai-skills

AI 编程助手 Skills 集合，适用于 Claude Code / Codex / OpenClaw 等工具。

## xiaohongshu/ — 小红书完整工作流

从爆款采集到内容生成、海报制作、发布、互动的全链路 skills。

| Skill | 说明 |
|-------|------|
| fetch-viral-notes | 采集低粉爆款笔记 |
| analyze-viral-notes | 分析爆款规律 |
| generate-from-viral | 从爆款生成新内容 |
| generate-from-feishu | 从飞书表格批量生成海报 |
| zodiac-daily-fortune | 星座每日运势生成 |
| zodiac-poster | 星座海报制作 |
| card-generator | 卡片式宣传页生成 |
| template-lint | 模板质量检查 |
| upload-to-feishu | 上传图片到飞书 |
| sync-templates | 同步模板到飞书表 |
| publish-to-xiaohongshu | 发布到小红书 |
| reply-comments | 评论回复 |

## feishu/ — 飞书 API 操作

统一风格的飞书开放平台 skill 套件，覆盖多维表格、日历、任务、IM、云文档全场景。

| Skill | 说明 |
|-------|------|
| feishu-bitable | 多维表格 CRUD（27 种字段类型、高级筛选、批量操作） |
| feishu-calendar | 日历日程管理（创建会议、忙闲查询、参会人管理） |
| feishu-task | 任务管理（创建/完成/反完成、清单管理） |
| feishu-im-read | IM 消息读取（历史消息、话题回复、搜索、资源下载） |
| feishu-create-doc | 创建云文档（Lark-flavored Markdown 完整语法） |
| feishu-update-doc | 更新云文档（7 种模式：追加/覆盖/定位替换等） |
| feishu-fetch-doc | 获取云文档内容 |
| feishu-channel-rules | 飞书对话输出格式规则（alwaysActive） |

## 配置

小红书工作流需要飞书和小红书相关环境变量，参见 `xiaohongshu/.env.example`。
