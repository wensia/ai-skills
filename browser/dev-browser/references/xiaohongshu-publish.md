# 小红书发布笔记指南

使用 dev-browser 自动化发布小红书图文笔记的最佳实践。

## 常见问题与解决方案

### 问题 1: 点击元素超时（元素在视口外）

**现象**: 使用 `selectSnapshotRef` 点击按钮时报错 `element is outside of the viewport`

**原因**: 小红书创作者页面使用了复杂的布局，某些按钮可能在视口外

**解决方案**: 使用 `page.evaluate()` 在浏览器内执行 JavaScript 点击

```typescript
// ❌ 可能失败
const btn = await client.selectSnapshotRef("xiaohongshu", "e105");
await btn.click();

// ✅ 更可靠的方式
await page.evaluate(() => {
  const elements = document.querySelectorAll('div');
  for (const el of elements) {
    if (el.textContent === '上传图文' && el.textContent.length < 10) {
      el.click();
      break;
    }
  }
});
```

### 问题 2: 文件选择器超时

**现象**: 使用 `page.waitForEvent('filechooser')` 等待文件选择器超时

**原因**: 小红书的上传按钮可能不会触发标准的文件选择器事件

**解决方案**: 直接找到隐藏的 `input[type="file"]` 元素，使用 `setInputFiles()` 上传

```typescript
// ❌ 可能超时
const fileChooserPromise = page.waitForEvent('filechooser');
await uploadBtn.click();
const fileChooser = await fileChooserPromise;
await fileChooser.setFiles(imagePaths);

// ✅ 直接设置文件输入
const fileInput = await page.$('input[type="file"]');
if (fileInput) {
  await fileInput.setInputFiles(imagePaths);
}
```

### 问题 3: 点击发布按钮

**现象**: 通过 snapshot ref 点击发布按钮不稳定

**解决方案**: 使用文本选择器

```typescript
// ✅ 使用文本选择器更可靠
const publishBtn = await page.$('button:has-text("发布")');
await publishBtn.click();
```

## 完整发布流程

### Step 1: 启动服务器

```bash
cd skills/dev-browser && ./server.sh &
```

### Step 2: 导航到发布页面

```typescript
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("xiaohongshu", { viewport: { width: 1280, height: 900 } });

// 直接导航到创作者发布页面
await page.goto("https://creator.xiaohongshu.com/publish/publish?source=official");
await page.waitForTimeout(3000);
```

### Step 3: 选择上传图文

```typescript
// 点击"上传图文"选项
await page.evaluate(() => {
  const elements = document.querySelectorAll('div');
  for (const el of elements) {
    if (el.textContent === '上传图文' && el.textContent.length < 10) {
      el.click();
      break;
    }
  }
});
await page.waitForTimeout(2000);
```

### Step 4: 上传图片

```typescript
const imagePaths = [
  '/path/to/image1.png',
  '/path/to/image2.png',
  // ... 最多 18 张图片
];

// 直接设置文件输入
const fileInput = await page.$('input[type="file"]');
await fileInput.setInputFiles(imagePaths);

// 等待上传完成
await page.waitForTimeout(8000);
```

### Step 5: 填写标题和正文

```typescript
// 获取快照找到输入框
const snapshot = await client.getAISnapshot("xiaohongshu");

// 填写标题（找到 placeholder 为"填写标题会有更多赞哦～"的输入框）
const titleInput = await page.$('input[placeholder*="标题"]');
// 或通过 snapshot ref
const titleInput = await client.selectSnapshotRef("xiaohongshu", "e235");
await titleInput.fill("你的标题");

// 填写正文
const contentInput = await page.$('[contenteditable="true"]');
// 或通过 snapshot ref 找到正文输入区域
await contentInput.fill(`你的正文内容

#话题1 #话题2 #话题3`);
```

### Step 6: 发布

```typescript
// 点击发布按钮
const publishBtn = await page.$('button:has-text("发布")');
await publishBtn.click();

// 等待发布完成
await page.waitForTimeout(5000);

// 验证发布成功
const url = page.url();
if (url.includes('/publish/success')) {
  console.log('发布成功！');
}
```

### Step 7: 清理

```typescript
await client.close("xiaohongshu");
await client.disconnect();
```

## 完整示例脚本

```typescript
import { connect, waitForPageLoad } from "@/client.js";

async function publishXiaohongshu(title: string, content: string, imagePaths: string[]) {
  const client = await connect();
  const page = await client.page("xiaohongshu", { viewport: { width: 1280, height: 900 } });

  try {
    // 1. 导航到发布页面
    await page.goto("https://creator.xiaohongshu.com/publish/publish?source=official");
    await page.waitForTimeout(3000);

    // 2. 切换到图文上传
    await page.evaluate(() => {
      const elements = document.querySelectorAll('div');
      for (const el of elements) {
        if (el.textContent === '上传图文' && el.textContent.length < 10) {
          el.click();
          break;
        }
      }
    });
    await page.waitForTimeout(2000);

    // 3. 上传图片
    const fileInput = await page.$('input[type="file"]');
    if (!fileInput) throw new Error('未找到文件上传输入框');
    await fileInput.setInputFiles(imagePaths);
    await page.waitForTimeout(8000); // 等待上传完成

    // 4. 填写标题
    const snapshot = await client.getAISnapshot("xiaohongshu");
    // 根据快照找到标题输入框的 ref
    const titleInput = await page.$('input[placeholder*="标题"]');
    if (titleInput) {
      await titleInput.fill(title);
    }

    // 5. 填写正文
    const contentArea = await page.$('div[contenteditable="true"]');
    if (contentArea) {
      await contentArea.click();
      await contentArea.fill(content);
    }
    await page.waitForTimeout(1000);

    // 6. 发布
    const publishBtn = await page.$('button:has-text("发布")');
    if (!publishBtn) throw new Error('未找到发布按钮');
    await publishBtn.click();
    await page.waitForTimeout(5000);

    // 7. 验证结果
    const url = page.url();
    if (url.includes('/publish/success')) {
      console.log('发布成功！');
      return true;
    } else {
      console.log('发布状态未知，当前URL:', url);
      return false;
    }
  } finally {
    await client.close("xiaohongshu");
    await client.disconnect();
  }
}

// 使用示例
const title = "射手遇到射手";
const content = `双倍自由双倍疯🔥
两个射手相遇，就像照镜子
说走就走×2，没人踩刹车！

#射手座 #星座配对 #命定之约`;
const images = [
  '/path/to/01_cover.png',
  '/path/to/02_page.png',
  '/path/to/03_page.png',
];

await publishXiaohongshu(title, content, images);
```

## 注意事项

| 项目 | 说明 |
|------|------|
| 登录状态 | 需要提前登录小红书账号，建议使用 Extension Mode 连接已登录的浏览器 |
| 图片限制 | 最多 18 张图片，单张最大 32MB |
| 图片格式 | 支持 png、jpg、jpeg、webp，不支持 gif |
| 标题长度 | 最多 20 个字符 |
| 正文长度 | 最多 1000 个字符 |
| 等待时间 | 上传图片后需要等待足够时间（建议 8 秒以上） |

## 调试技巧

1. **截图调试**: 在每个关键步骤后截图
   ```typescript
   await page.screenshot({ path: "tmp/step1.png" });
   ```

2. **获取快照**: 使用 `getAISnapshot()` 查看页面元素
   ```typescript
   const snapshot = await client.getAISnapshot("xiaohongshu");
   console.log(snapshot);
   ```

3. **检查 URL**: 验证当前页面状态
   ```typescript
   console.log('当前URL:', page.url());
   ```
