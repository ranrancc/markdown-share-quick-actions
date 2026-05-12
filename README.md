# Markdown Share Quick Actions

把 Markdown 一键转成 Word、单文件 HTML，也可以把常见文档或 HTML 转回 Markdown。

适合教师、研究者、Obsidian 用户和长期用 Markdown 写作的人：平时用 Markdown 写讲义、笔记、会议纪要，分享时用右键菜单导出成 `.docx` 或可直接打开的 `.html`。

## 主要功能

- macOS：Finder 右键快速操作。
- Windows：文件资源管理器 `Send to` 菜单和拖拽 `.bat`。
- 其他系统：通用命令行。
- Markdown 转 Word，支持图片、基础 Obsidian 图片语法和 Mermaid 图表预渲染。
- Markdown 转 HTML，生成单文件自包含网页，适合投屏、分享、打印。
- 5 种 HTML 主题：经典样式、文章样式、报告样式、阅读样式、交互样式。
- 完整模式可用：多种文档转 Markdown、HTML 转 Markdown、URL 转 Markdown。

## HTML 主题

| 中文名 | 命令参数 | 适合场景 |
| --- | --- | --- |
| 经典样式 | `classic` | 默认稳定样式，适合通用分享 |
| 文章样式 | `article` | 长文、公众号风格文章 |
| 报告样式 | `report` | 课程材料、研究报告、正式文档 |
| 阅读样式 | `reading` | 极简阅读、打印前预览 |
| 交互样式 | `interactive` | 长讲义、带目录投屏展示 |

## 安装

### macOS

先安装 Pandoc：

```bash
brew install pandoc
```

下载并安装右键菜单：

```bash
git clone https://github.com/ranrancc/markdown-share-quick-actions.git
cd markdown-share-quick-actions
python3 install_all.py
killall Finder
```

安装器会把运行文件复制到稳定目录：

```text
~/Library/Application Support/Markdown Share Quick Actions/
```

Finder 右键菜单会指向这个目录。安装完成后，下载/克隆的仓库目录可以移动或删除。

安装后，在 Finder 里选中 `.md` / `.markdown` 文件，右键打开“快速操作”，可以看到：

```text
Markdown 转 Word（含图表）
Markdown 转 HTML（含图表）
MD 转 HTML（选择主题）
多种文档转 MD
HTML 转 MD
```

### Windows

先安装：

- Python 3: https://www.python.org/downloads/windows/
- Pandoc: https://pandoc.org/installing.html

然后运行：

```bat
git clone https://github.com/ranrancc/markdown-share-quick-actions.git
cd markdown-share-quick-actions
py -3 install_windows.py
```

安装器会把运行文件复制到稳定目录：

```text
%LOCALAPPDATA%\MarkdownShareQuickActions\
```

SendTo 菜单会指向这个目录。安装完成后，下载/克隆的仓库目录可以移动或删除。

安装后，在文件资源管理器里选中文件，右键选择 `Send to`，可以看到：

```text
Markdown to Word
Markdown to HTML
Markdown to HTML - Choose Theme
Markdown to Word and HTML
Document to Markdown
HTML to Markdown
Markdown Share Check
```

### Mermaid 图表支持

如果 Markdown 里有 Mermaid 图表，还需要 Node.js 和 Mermaid CLI：

```bash
npm install -g @mermaid-js/mermaid-cli
```

安装后可以自检：

```bash
python3 md_share.py html note.md --check
```

Windows 可用：

```bat
py -3 md_share.py html note.md --check
```

## 完整模式

基础模式只需要 Python 3 和 Pandoc，足够完成 Markdown 转 Word/HTML。

如果要使用“多种文档转 MD / HTML 转 MD / URL 转 MD”，建议把完整依赖安装到稳定运行目录的虚拟环境里，避免污染系统 Python：

```bash
python3 install_full_deps.py
python3 install_all.py
killall Finder
```

Windows:

```bat
py -3 install_full_deps.py
py -3 install_windows.py
```

说明：右键菜单会优先使用稳定运行目录里的 `.venv`；没有虚拟环境时才退回系统可用的 Python。

## 命令行用法

```bash
python3 md_share.py word note.md
python3 md_share.py html note.md
python3 md_share.py html note.md --theme article
python3 md_share.py both note.md
python3 md_share.py both ./notes --recursive
python3 md_share.py to-md file.docx
python3 md_share.py html-to-md page.html
python3 md_share.py url-to-md "https://example.com/article"
```

Windows 上如果 `python3` 不可用，通常使用：

```bat
py -3 md_share.py html note.md --theme report
```

## 卸载

macOS:

```bash
python3 uninstall_all.py
killall Finder
```

这会同时移除 Finder workflow 和 `~/Library/Application Support/Markdown Share Quick Actions/` 里的运行文件。

Windows:

```bat
py -3 uninstall_windows.py
```

这会同时移除 SendTo 菜单和 `%LOCALAPPDATA%\MarkdownShareQuickActions\` 里的运行文件。

## 故障排查

### 右键菜单里看不到动作

macOS 先刷新 Finder：

```bash
killall Finder
```

如果仍然看不到，重新安装：

```bash
python3 install_all.py
killall Finder
```

### 提示找不到 pandoc

macOS:

```bash
brew install pandoc
```

Windows: 从 https://pandoc.org/installing.html 下载安装包。

### Mermaid 图表没有变成图片

先运行自检：

```bash
python3 md_share.py html note.md --check
```

如果提示缺 Node.js 或 Mermaid CLI：

```bash
npm install -g @mermaid-js/mermaid-cli
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

替换这个文件：

```text
md-to-word-quick-action/reference.docx
```

标题、字体、页边距、段落样式都由它控制。

## 安全说明

- 所有转换都在本机执行。
- 工具不会上传你的 Markdown、图片或导出文件。
- HTML 导出使用 `pandoc --embed-resources`，会把本地图片内嵌到 HTML 文件中，分享前请确认文件中不含敏感图片。
- URL 转 Markdown 会访问用户提供的网址；公开发布时请把它视为完整模式能力，而不是默认必需能力。

---

# Agent Installation Guide

This section is written for Codex, OpenClaw, Claude Code, and other AI agents that install or debug this repository for a user.

## Goal

Install local Markdown conversion tools without uploading user files or modifying source Markdown files in place.

## System Routing

1. Detect the user's OS.
2. Use macOS Finder Quick Actions on macOS.
3. Use Windows SendTo wrappers on Windows.
4. Use the CLI on Linux or unsupported systems.

## Dependency Levels

### Basic

Required for Markdown to Word/HTML:

- Python 3
- Pandoc

Optional, only when Markdown contains Mermaid code blocks:

- Node.js
- Mermaid CLI: `npm install -g @mermaid-js/mermaid-cli`

### Full

Required for document/HTML/URL to Markdown:

```bash
python3 install_full_deps.py
```

Windows:

```bat
py -3 install_full_deps.py
```

Prefer the runtime virtual environment for full mode. Do not install heavy conversion dependencies into the user's global Python unless the user explicitly asks.

## macOS Install

From the repository root:

```bash
python3 install_all.py
killall Finder
```

Runtime files are copied to:

```text
~/Library/Application Support/Markdown Share Quick Actions/
```

Expected workflows:

```text
~/Library/Services/Markdown 转 Word（含图表）.workflow
~/Library/Services/Markdown 转 HTML（含图表）.workflow
~/Library/Services/MD 转 HTML（选择主题）.workflow
~/Library/Services/多种文档转 MD.workflow
~/Library/Services/HTML 转 MD.workflow
```

The theme chooser presents Chinese labels and maps them to CLI slugs:

```text
经典样式 -> classic
文章样式 -> article
报告样式 -> report
阅读样式 -> reading
交互样式 -> interactive
```

## Windows Install

From the repository root:

```bat
py -3 install_windows.py
```

Runtime files are copied to:

```text
%LOCALAPPDATA%\MarkdownShareQuickActions\
```

The installer writes SendTo wrappers with the runtime root embedded as an absolute path. Do not replace this with a blind copy of `windows/*.bat`, because copied batch files would resolve `%~dp0` to the SendTo folder instead of the runtime directory.

Expected SendTo entries:

```text
Markdown to Word.bat
Markdown to HTML.bat
Markdown to HTML - Choose Theme.bat
Markdown to Word and HTML.bat
Document to Markdown.bat
HTML to Markdown.bat
Markdown Share Check.bat
```

## Verification

Run these checks before declaring installation complete:

```bash
python3 md_share.py html README.md --check
python3 md_share.py html --theme article /path/to/simple.md
```

For a Mermaid sample, verify that conversion produces no `Mermaid render incomplete` error.

macOS plist check:

```bash
plutil -lint ~/Library/Services/*.workflow/Contents/document.wflow
```

Windows sanity check:

```bat
py -3 md_share.py html --theme classic path\to\simple.md
```

## Robustness Notes

- Do not use `status="$?"` in Automator zsh scripts. `status` is a read-only zsh special parameter; use `exit_code` or `rc`.
- Keep `classic` as the compatibility theme. It writes `note.html`; other themes write `note.<theme>.html`.
- `to-md`, `html-to-md`, and `url-to-md` are full-mode features because they require extra Python packages.
- `install_all.py` should install the complete macOS Quick Actions set.
- `uninstall_all.py` should remove every workflow that `install_all.py` creates.
- `install_windows.py` should generate SendTo wrappers with an absolute runtime path.
- Installed workflows and SendTo entries should point to the stable runtime directory, not the downloaded repository folder.

## Do Not

- Do not upload user Markdown files or images.
- Do not modify source Markdown files in place.
- Do not overwrite `md-to-word-quick-action/reference.docx` unless the user asks to change Word styling.
- Do not commit private Obsidian research notes, local `.workflow` bundles, `.venv`, `__pycache__`, or generated output files.
