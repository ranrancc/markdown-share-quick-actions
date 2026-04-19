---
name: markdown-share-quick-actions
description: "Install macOS Finder Quick Actions that convert selected Markdown/Obsidian files to Word (.docx) or self-contained HTML. Use when the user wants to deploy local Markdown sharing tools, export Markdown notes for teachers/students/colleagues, or install right-click Markdown conversion on macOS."
user-invocable: true
---

# Markdown Share Quick Actions

Install two macOS Finder Quick Actions:

- `Markdown 转 Word`
- `Markdown 转 HTML`

## When To Use

- The user wants a right-click Markdown to Word or HTML converter.
- The user writes in Obsidian/Markdown and needs shareable `.docx` or `.html`.
- A teacher wants to export lecture notes, course materials, meeting notes, or paper notes.
- The user gives this repository URL to OpenClaw, Codex, or another agent and asks for installation.

## Requirements

- macOS
- `python3`
- `pandoc`

If `pandoc` is missing, tell the user to install it:

```bash
brew install pandoc
```

## Install

From the repository root:

```bash
python3 install_all.py
killall Finder
```

## Verify

Confirm these exist:

```text
~/Library/Services/Markdown 转 Word.workflow
~/Library/Services/Markdown 转 HTML.workflow
```

Then ask the user to select a `.md` file in Finder, right-click, and choose the Quick Action.

## Uninstall

```bash
python3 uninstall_all.py
killall Finder
```

## Safety

- Conversion runs locally.
- The source Markdown file is not modified.
- Output files are written next to the source file.
- HTML export embeds local images into one file; remind the user to check sensitive content before sharing.
