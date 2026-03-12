# 小红书 MCP 登录检查

在使用小红书相关功能前，需要确保 MCP 已登录。

---

## 检查登录状态

```
调用 mcp__xiaohongshu-mcp__check_login_status
```

**返回结果：**
- `logged_in: true` - 已登录，可继续操作
- `logged_in: false` - 未登录，需要执行登录流程

---

## 登录流程

如果未登录，执行以下步骤：

### 方式一：扫码登录（推荐）

```bash
cd "${XIAOHONGSHU_MCP_DIR:-./xiaohongshu-mcp}"
./xiaohongshu-login-darwin-arm64
```

执行后会显示二维码，使用小红书 APP 扫码登录。

### 方式二：MCP 获取二维码

```
调用 mcp__xiaohongshu-mcp__get_login_qrcode
```

返回 Base64 编码的二维码图片，超时时间约 5 分钟。

---

## Cookies 管理

### 删除 Cookies（重置登录）

```
调用 mcp__xiaohongshu-mcp__delete_cookies
```

删除后需要重新登录。

---

## 登录状态过期处理

当遇到以下错误时，说明登录状态已过期：
- `xsec_token 无效`
- `请求被拒绝`
- `需要登录`

解决方法：
1. 执行 `delete_cookies` 清除旧 cookies
2. 重新执行登录流程

---

## 相关 Skills

以下 skills 需要小红书登录：

- `fetch-viral-notes` - 抓取低粉爆文
- `analyze-viral-notes` - 分析爆文
- `generate-from-viral` - 从爆文生成内容
- `publish-to-xiaohongshu` - 发布到小红书
- `reply-comments` - 回复小红书评论
