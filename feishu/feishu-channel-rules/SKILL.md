---
name: feishu-channel-rules
description: |
  飞书对话输出格式规则（始终激活）。约束 AI 在飞书渠道中只输出 Markdown 文本，禁止输出卡片 JSON。包含飞书支持的 Markdown 语法参考。

  **始终激活**：在所有飞书对话（私聊、群聊）中自动生效，无需触发。
alwaysActive: true
---

# 飞书输出格式规则（强制）

## 回复如何呈现

系统自动选择最佳消息格式，你只需输出 Markdown 文本：

- **私聊**：实时流式渲染在消息卡片中（打字机效果）
- **群聊**：生成完毕后一次性发送（含代码块/表格时自动用卡片，否则普通消息）
- 不需要也不应该自己构造卡片，系统自动处理

## 严格禁止

以下行为会导致消息格式异常，必须避免：

- 输出飞书卡片 JSON（含 `"tag"`, `"elements"`, `"header"`, `"config"` 的 JSON）
- 输出消息卡片模板代码（无论 v1 还是 v2）
- 用 JSON "美化"回复 — 直接用 Markdown

## 正确做法

```
#### 操作确认

调试模式已成功关闭。

- 插件运行状态：正常
- debug 信息：已过滤
```

---

## 飞书 Markdown 语法参考

以下语法必须严格遵守，不能使用语法以外的写法。

### 标题

```
#### 四级标题
##### 五级标题
```

不支持一二三级标题（`#`、`##`、`###`），会导致卡片显示异常。可用加粗替代。

### 文本样式

| 语法 | 效果 |
|------|------|
| `**加粗**` | **加粗** |
| `*斜体*` | *斜体* |
| `~~删除线~~` | ~~删除线~~ |

加粗内容只能是中文或英文，不能含中文符号或表情符号。

### 链接

```
[链接文字](https://www.example.com)
<a href='https://open.feishu.cn'>文字链接</a>
```

### @指定人

```
<at id=id_01></at>
<at ids=id_01,id_02,xxx></at>
```

id 必须来自用户提供的真实 ID（`ou_` 开头、不超过 10 位字符串、或邮箱）。

### 彩色文本

```
<font color='green'>绿色文本</font>
```

颜色枚举：`neutral`, `blue`, `turquoise`, `lime`, `orange`, `violet`, `wathet`, `green`, `yellow`, `red`, `purple`, `carmine`

### 图片

```
![hover_text](image_key)
```

image_key 不支持 http 链接。

### 列表

```
- 无序列表
    - 二级列表

1. 有序列表
    1.1 二级列表
```

4 个空格代表一层缩进。

### 代码块

````
```JSON
{"key": "value"}
```
````

支持指定编程语言，未指定默认 Plain Text。

### 其他元素

| 元素 | 语法 |
|------|------|
| 分割线 | `---` |
| 标签 | `<text_tag color='red'>标签文本</text_tag>` |
| 人员组件 | `<person id='user_id' show_name=true show_avatar=true style='normal'></person>` |
| 数字角标 | `<number_tag background_color='grey' font_color='white' url='...'>1</number_tag>` |

person 标签不能嵌套在 font 中。

---

> 直接给出排版好的 Markdown 内容即可，不要告诉用户"我无法发卡片"。
