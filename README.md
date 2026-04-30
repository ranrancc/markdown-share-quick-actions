# Markdown Share Quick Actions

跨平台 Markdown 分享工具包。它提供一个通用命令行转换器，并为 macOS 和 Windows 提供系统集成：

- macOS：Finder 右键快速操作
- Windows：SendTo 菜单和拖拽 `.bat`
- 其他系统：通用 CLI

这个包适合高校教师、研究者和 Obsidian/Markdown 用户：平时用 Markdown 写课程讲义、会议纪要、论文笔记，分享时一键变成 Word 或可投屏的单文件 HTML。

## 给 OpenClaw / Codex / 任意智能体的快速部署指令

如果用户给你这个仓库 URL，并要求安装或部署，请按这个顺序执行：

1. 识别用户系统：macOS、Windows 或其他。
2. 确认 Python 3 可用。
3. 确认 `pandoc` 可用；如果没有，提示用户先安装。
4. 如果 Markdown 中包含 ```mermaid 图表，确认 Node.js 和 Mermaid CLI 可用。

macOS 常用安装：

```bash
brew install pandoc
npm install -g @mermaid-js/mermaid-cli  # 仅 Mermaid 图表需要
```

Windows 请从 Pandoc 和 Node.js 官网安装：

```text
https://pandoc.org/installing.html
https://nodejs.org/
```

如果要导出 Mermaid 图表，安装 Node.js 后再运行：

```bat
npm install -g @mermaid-js/mermaid-cli
```

5. 按系统执行安装。

macOS：

```bash
python3 install_all.py
killall Finder
```

Windows：

```bat
py -3 install_windows.py
```

6. 先自检，再告诉用户如何使用：

```bash
python3 md_share.py html note.md --check
```

   - macOS：Finder 中选中 `.md` 或 `.markdown` 文件，右键打开“快速操作”。
   - Windows：文件资源管理器中选中文件，右键 `Send to`，选择 Markdown 动作。
   - 其他系统：使用 `python3 md_share.py word|html|both <files...>`。

## macOS 一键安装

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
~/Library/Services/Markdown 转 Word（含图表）.workflow
~/Library/Services/Markdown 转 HTML（含图表）.workflow
```

## macOS 一键卸载

```bash
python3 uninstall_all.py
killall Finder
```

## Windows 安装

```bat
git clone https://github.com/ranrancc/markdown-share-quick-actions.git
cd markdown-share-quick-actions
py -3 install_windows.py
```

安装后，在文件资源管理器中选中 `.md` / `.markdown` 文件，右键：

```text
Send to -> Markdown to Word
Send to -> Markdown to HTML
Send to -> Markdown to Word and HTML
```

也可以直接把 Markdown 文件拖到：

```text
windows\md-to-word.bat
windows\md-to-html.bat
windows\md-to-both.bat
```

## Windows 卸载

```bat
py -3 uninstall_windows.py
```

## 通用命令行

适用于 macOS、Windows、Linux：

```bash
python3 md_share.py word note.md
python3 md_share.py html note.md
python3 md_share.py both note.md
python3 md_share.py both ./notes --recursive
python3 md_share.py html note.md --check
```

Windows 上如果 `python3` 不可用，通常使用：

```bat
py -3 md_share.py both note.md
py -3 md_share.py html note.md --check
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
- Windows / Linux 可使用通用 CLI
- `python3` 或 Windows `py -3`
- `pandoc`
- 可选但推荐：Node.js / npm / Mermaid CLI。只有当 Markdown 里包含 ```mermaid 图表并希望导出为图片时需要。

安装 Mermaid CLI：

```bash
npm install -g @mermaid-js/mermaid-cli
```

检查依赖：

```bash
python3 --version
pandoc --version
npm --version  # 可选：仅 Mermaid 图表预渲染需要
mmdc --version # 可选：仅 Mermaid 图表预渲染需要
python3 md_share.py html note.md --check
```

如果 `pandoc` 不存在，常见安装方式：

```bash
brew install pandoc
```

Windows 用户从 Pandoc 官网下载安装包：

```text
https://pandoc.org/installing.html
```

## 使用方法

### macOS

1. 在 Finder 里选中一个或多个 `.md` / `.markdown` 文件。
2. 右键。
3. 选择“快速操作”里的：
   - `Markdown 转 Word`
   - `Markdown 转 HTML`
   - `Markdown 转 Word（含图表）`
   - `Markdown 转 HTML（含图表）`
4. 输出文件会出现在原 Markdown 文件旁边。

例如：

```text
course-note.md
course-note.docx
course-note.html
```

### Windows

1. 在文件资源管理器中选中一个或多个 `.md` / `.markdown` 文件。
2. 右键。
3. 选择 `Send to`。
4. 选择：
   - `Markdown to Word`
   - `Markdown to HTML`
   - `Markdown to Word and HTML`

或者直接拖拽到 `windows/*.bat`。

如果含 Mermaid 图表，先在命令提示符或 PowerShell 里运行：

```bat
py -3 md_share.py html note.md --check
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

### Mermaid 图表没有变成图片

先运行自检：

```bash
python3 md_share.py html note.md --check
```

如果提示缺 Node.js 或 Mermaid CLI：

```bash
npm install -g @mermaid-js/mermaid-cli
```

macOS 的 Finder 快速操作会自动补 Homebrew 的 PATH。Windows 会自动查找常见的 Node.js、Chrome 和 Edge 安装路径。

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
├── install_windows.py
├── uninstall_all.py
├── uninstall_windows.py
├── md_share.py
├── mermaid-prerender.py
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
└── windows/
    ├── md-to-word.bat
    ├── md-to-html.bat
    ├── md-to-both.bat
    └── README.md
```

## 安全说明

- 所有转换都在本机执行。
- 工具不会上传你的 Markdown、图片或导出文件。
- HTML 导出使用 `pandoc --embed-resources`，会把本地图片内嵌到 HTML 文件中，分享前请确认文件中不含敏感图片。
