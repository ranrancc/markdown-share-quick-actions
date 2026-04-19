# Agent Deployment Guide

Use this guide when an AI coding agent, OpenClaw agent, Codex agent, or similar assistant receives this repository URL and is asked to install or deploy the tool.

## What This Repository Does

This repository converts Markdown files to Word and self-contained HTML. It includes:

- A cross-platform CLI: `md_share.py`
- macOS Finder Quick Actions
- Windows SendTo / drag-and-drop wrappers

They convert selected `.md` / `.markdown` files into `.docx` or self-contained `.html` files next to the source file.

## Requirements

- Python 3 must be available.
- `pandoc` must be available.

macOS Finder integration requires macOS. Windows integration uses SendTo actions. Linux and other systems should use the CLI only.

## Install Procedure By Platform

### macOS

From the repository root:

```bash
python3 install_all.py
killall Finder
```

If `pandoc` is missing, ask the user to install it:

```bash
brew install pandoc
```

Then rerun:

```bash
python3 install_all.py
killall Finder
```

### Windows

If `pandoc` is missing, ask the user to install it from:

```text
https://pandoc.org/installing.html
```

Then run from the repository root:

```bat
py -3 install_windows.py
```

Tell the user to right-click Markdown files in Explorer, choose `Send to`, then choose a Markdown action.

### CLI Fallback

Use this on any platform when system integration is not desired:

```bash
python3 md_share.py word path/to/file.md
python3 md_share.py html path/to/file.md
python3 md_share.py both path/to/file.md
```

## Verify Installation

Check that these directories exist:

```text
~/Library/Services/Markdown 转 Word.workflow
~/Library/Services/Markdown 转 HTML.workflow
```

Then instruct the user to select a Markdown file in Finder, right-click, and look under Quick Actions.

On Windows, check that these files exist in `%APPDATA%\Microsoft\Windows\SendTo`:

```text
Markdown to Word.bat
Markdown to HTML.bat
Markdown to Word and HTML.bat
```

## Uninstall

From the repository root:

```bash
python3 uninstall_all.py
killall Finder
```

Windows:

```bat
py -3 uninstall_windows.py
```

## Do Not

- Do not upload user Markdown files or images anywhere.
- Do not modify the user's Markdown files in place.
- Do not overwrite `reference.docx` unless the user explicitly asks to change Word styling.
- Do not run destructive cleanup outside this repository, `~/Library/Services/Markdown 转*.workflow`, or the package's own Windows SendTo `.bat` entries.
