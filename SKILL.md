---
name: markdown-share-quick-actions
description: "Install or use cross-platform Markdown sharing tools that convert Markdown/Obsidian files to Word (.docx) or self-contained HTML. Supports macOS Finder Quick Actions, Windows SendTo/drag-and-drop wrappers, and a general CLI. Use when the user wants to export Markdown notes for teachers/students/colleagues or deploy right-click Markdown conversion."
user-invocable: true
---

# Markdown Share Quick Actions

Convert Markdown files to Word and self-contained HTML with:

- macOS Finder Quick Actions
- Windows SendTo / drag-and-drop `.bat` wrappers
- Cross-platform CLI

## When To Use

- The user wants a right-click or drag-and-drop Markdown to Word or HTML converter.
- The user writes in Obsidian/Markdown and needs shareable `.docx` or `.html`.
- A teacher wants to export lecture notes, course materials, meeting notes, or paper notes.
- The user gives this repository URL to OpenClaw, Codex, or another agent and asks for installation.

## Requirements

- `python3`
- `pandoc`

If `pandoc` is missing on macOS, tell the user to install it:

```bash
brew install pandoc
```

On Windows, point them to:

```text
https://pandoc.org/installing.html
```

## Install

macOS, from the repository root:

```bash
python3 install_all.py
killall Finder
```

Windows:

```bat
py -3 install_windows.py
```

CLI fallback:

```bash
python3 md_share.py both path/to/file.md
```

## Verify

Confirm these exist:

```text
~/Library/Services/Markdown 转 Word.workflow
~/Library/Services/Markdown 转 HTML.workflow
```

On Windows, confirm SendTo contains:

```text
Markdown to Word.bat
Markdown to HTML.bat
Markdown to Word and HTML.bat
```

Then ask the user to select a `.md` file in Finder, right-click, and choose the Quick Action.

## Uninstall

```bash
python3 uninstall_all.py
killall Finder
```

Windows:

```bat
py -3 uninstall_windows.py
```

## Safety

- Conversion runs locally.
- The source Markdown file is not modified.
- Output files are written next to the source file.
- HTML export embeds local images into one file; remind the user to check sensitive content before sharing.
