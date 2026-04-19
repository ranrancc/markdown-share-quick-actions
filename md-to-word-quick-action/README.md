# Markdown 转 Word

一个给 macOS Finder 用的右键工具。

选中一个或多个 `.md` 文件后，可以直接右键转换成同目录、同名的 `.docx` 文件，适合把 Obsidian / Markdown 笔记快速分享给需要 Word 的朋友。

## 适合谁

- 平时以 Markdown 或 Obsidian 写作
- 偶尔需要把文档发给只看 Word / PDF 的人
- 希望在 Finder 里右键一键转换，不想额外装一堆编辑器 App

## 功能

- 仅在 Finder 选中 Markdown 文件时出现
- 支持单个文件和多选批量转换
- 输出为原目录下同名 `.docx`
- 已有同名 `.docx` 会直接覆盖
- 支持普通 Markdown 图片
- 支持外链图片打包进 Word
- 支持基础 Obsidian 图片写法：`![[image.png]]`
- 支持通过 `reference.docx` 统一控制排版

## 目录说明

- `convert_md_to_docx.sh`
  实际执行转换的脚本
- `install_quick_action.py`
  安装 Finder 右键动作
- `generate_reference_docx.py`
  生成默认 Word 模板
- `reference.docx`
  默认排版模板，可直接替换

## 依赖

- macOS
- `pandoc`
- `python3`

先确认 `pandoc` 已安装：

```bash
which pandoc
```

如果没有结果，先安装 `pandoc` 再继续。

## 安装

在本目录执行：

```bash
python3 generate_reference_docx.py
python3 install_quick_action.py
killall Finder
```

安装完成后，系统会生成：

```text
~/Library/Services/Markdown 转 Word.workflow
```

## 怎么用

1. 在 Finder 里选中一个或多个 `.md` 文件
2. 右键
3. 选择“快速操作”里的“Markdown 转 Word”
4. 等待完成

转换成功后，Word 文件会出现在原 Markdown 文件旁边。

例如：

```text
note.md
-> note.docx
```

## 排版怎么变好看

这个工具的“美观度”主要不是靠脚本，而是靠 `reference.docx`。

如果你想换成自己的字体、标题样式、段落间距、页边距，只需要直接替换这个文件：

```text
reference.docx
```

不需要改脚本。

## 常见问题

### 1. 右键里没看到这个动作

先执行：

```bash
killall Finder
```

如果还没有，再重新运行安装命令：

```bash
python3 install_quick_action.py
killall Finder
```

### 2. 提示找不到 pandoc

说明系统里没有可用的 `pandoc`，先安装它，再重新尝试。

### 3. 图片没有进 Word

通常以下几种最稳：

- `![](./assets/demo.png)`
- `![img](https://example.com/demo.png)`
- `![[demo.png]]`

如果是 Obsidian 里靠 vault 附件规则自动解析、但路径本身并不真实可达的图片，这个工具不一定能找到。

## 分享给朋友时怎么打包

最简单的方式是把整个目录发给对方：

- `convert_md_to_docx.sh`
- `install_quick_action.py`
- `generate_reference_docx.py`
- `reference.docx`
- `README.md`

对方只需要：

1. 安装 `pandoc`
2. 进入这个目录
3. 执行安装命令

```bash
python3 generate_reference_docx.py
python3 install_quick_action.py
killall Finder
```

## 备注

这是一个轻量、本地、免费的方案。

它的目标不是替代 Word 编辑，而是把 Markdown 文档快速、稳定地变成“可以拿去分享”的 Word 文件。
