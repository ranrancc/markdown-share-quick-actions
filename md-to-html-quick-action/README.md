# Markdown 转 HTML

macOS Finder 右键工具。

选中一个或多个 `.md` 文件后，可直接生成同目录、同名的 `.html` 文件。

## 输出格式

默认输出为单文件自包含 HTML：

- 结果是一个 `.html`
- 图片会被内嵌进 HTML
- 双击即可用浏览器打开
- 分享时通常只发这一个文件就够了
- 默认带展示优化样式、全屏按钮和打印样式

这类文件本质上还是普通 HTML，只是资源被转成了内嵌的 data URI。

如果你说的是“把图片也封装在一起”的网页文件，常见有两种：

- 单文件自包含 HTML：兼容性最好，当前工具采用这个
- MHTML / `.mht`：也是单文件封装，但不同浏览器支持不如普通 HTML 稳

## 安装

```bash
python3 generate_workflow_icon.py
python3 install_quick_action.py
killall Finder
```

安装后会生成：

```text
~/Library/Services/Markdown 转 HTML.workflow
```

## 使用

1. Finder 里选中 `.md`
2. 右键
3. 选择 `Markdown 转 HTML`
4. 在原目录得到同名 `.html`

## 展示与打印

导出的 HTML 默认是“展示版”：

- 页面更适合投屏和全屏讲课
- 右上角有 `全屏展示` 按钮
- 浏览器打印时会自动切换到更适合纸张输出的样式
- 仍然保持单文件输出，方便分享

## 依赖

- macOS
- `pandoc`
- `python3`
