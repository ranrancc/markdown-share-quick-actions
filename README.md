# Markdown Share Quick Actions

面向 macOS 的 Markdown 分享右键工具包。安装后，Finder 里选中一个或多个 `.md` / `.markdown` 文件，可以右键一键导出：

- `Markdown 转 Word`：生成同目录同名 `.docx`
- `Markdown 转 HTML`：生成同目录同名 `.html`

这个包适合高校教师、研究者和 Obsidian/Markdown 用户：平时用 Markdown 写课程讲义、会议纪要、论文笔记，分享时一键变成 Word 或可投屏的单文件 HTML。

## 给 OpenClaw / Codex / 任意智能体的快速部署指令

如果用户给你这个仓库 URL，并要求安装或部署，请按这个顺序执行：

1. 确认系统是 macOS。
2. 确认 `python3` 可用。
3. 确认 `pandoc` 可用；如果没有，提示用户先安装：

```bash
brew install pandoc
```

4. 在仓库根目录执行：

```bash
python3 install_all.py
killall Finder
```

5. 告诉用户：在 Finder 中选中 `.md` 或 `.markdown` 文件，右键打开“快速操作”，选择 `Markdown 转 Word` 或 `Markdown 转 HTML`。

## 一键安装

```bash
git clone https://github.com/ranrancc/markdown-share-quick-actions.git
cd markdown-share-quick-actions
python3 install_all.py
killall Finder
```

安装完成后会生成：

```text
~/Library/Services/Markdown 转 Word.workflow
~/Library/Services/Markdown 转 HTML.workflow
```

## 一键卸载

```bash
python3 uninstall_all.py
killall Finder
```

## 单独安装

只安装 Word 导出：

```bash
cd md-to-word-quick-action
python3 generate_reference_docx.py
python3 install_quick_action.py
killall Finder
```

只安装 HTML 导出：

```bash
cd md-to-html-quick-action
python3 install_quick_action.py
killall Finder
```

## 功能说明

### Markdown 转 Word

- 支持单个文件和多选批量转换。
- 输出为原目录下同名 `.docx`。
- 使用 `reference.docx` 控制 Word 排版样式。
- 支持普通 Markdown 图片。
- 支持外链图片。
- 支持基础 Obsidian 图片写法：`![[image.png]]`。

### Markdown 转 HTML

- 输出为原目录下同名 `.html`。
- 默认生成单文件自包含 HTML，图片会内嵌。
- 适合投屏、网页分享、发给学生或同事。
- HTML 自带展示优化样式、全屏按钮、缩放档位、打印样式、图片点击放大。

## 依赖

- macOS
- `python3`
- `pandoc`

检查依赖：

```bash
python3 --version
pandoc --version
```

如果 `pandoc` 不存在，常见安装方式：

```bash
brew install pandoc
```

## 使用方法

1. 在 Finder 里选中一个或多个 `.md` / `.markdown` 文件。
2. 右键。
3. 选择“快速操作”里的：
   - `Markdown 转 Word`
   - `Markdown 转 HTML`
4. 输出文件会出现在原 Markdown 文件旁边。

例如：

```text
course-note.md
course-note.docx
course-note.html
```

## 给教师的典型场景

- 把 Obsidian 课程讲义导出成 Word，发给学院、学生或行政同事。
- 把 Markdown 课堂笔记导出成 HTML，直接浏览器打开投屏。
- 把论文阅读笔记导出成可打印的网页。
- 把会议纪要批量转成 Word 归档。

## 故障排查

### 右键菜单里看不到动作

先刷新 Finder：

```bash
killall Finder
```

如果仍然看不到，重新安装：

```bash
python3 install_all.py
killall Finder
```

### 提示找不到 pandoc

安装 pandoc：

```bash
brew install pandoc
```

### Word 图片没有显示

优先使用这些写法：

```markdown
![](./assets/demo.png)
![demo](https://example.com/demo.png)
![[demo.png]]
```

如果 Obsidian 附件依赖 vault 内部规则，但 Markdown 文件旁边没有真实图片路径，转换器可能找不到图片。

### 想改 Word 样式

替换这个文件即可：

```text
md-to-word-quick-action/reference.docx
```

标题、字体、页边距、段落样式都由它控制。

## 目录结构

```text
markdown-share-quick-actions/
├── install_all.py
├── uninstall_all.py
├── README.md
├── AGENTS.md
├── SKILL.md
├── md-to-word-quick-action/
│   ├── convert_md_to_docx.sh
│   ├── install_quick_action.py
│   ├── generate_reference_docx.py
│   ├── reference.docx
│   └── README.md
└── md-to-html-quick-action/
    ├── convert_md_to_html.sh
    ├── build_pretty_html.py
    ├── install_quick_action.py
    └── README.md
```

## 安全说明

- 所有转换都在本机执行。
- 工具不会上传你的 Markdown、图片或导出文件。
- HTML 导出使用 `pandoc --embed-resources`，会把本地图片内嵌到 HTML 文件中，分享前请确认文件中不含敏感图片。
