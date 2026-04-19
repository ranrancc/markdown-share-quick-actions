# Agent Deployment Guide

Use this guide when an AI coding agent, OpenClaw agent, Codex agent, or similar assistant receives this repository URL and is asked to install or deploy the tool.

## What This Repository Does

This repository installs two macOS Finder Quick Actions:

- `Markdown 转 Word`
- `Markdown 转 HTML`

They convert selected `.md` / `.markdown` files into `.docx` or self-contained `.html` files next to the source file.

## Requirements

- macOS only.
- `python3` must be available.
- `pandoc` must be available.

Do not attempt installation on Linux or Windows. Explain that the package depends on macOS Finder Services.

## Install Procedure

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

## Verify Installation

Check that these directories exist:

```text
~/Library/Services/Markdown 转 Word.workflow
~/Library/Services/Markdown 转 HTML.workflow
```

Then instruct the user to select a Markdown file in Finder, right-click, and look under Quick Actions.

## Uninstall

From the repository root:

```bash
python3 uninstall_all.py
killall Finder
```

## Do Not

- Do not upload user Markdown files or images anywhere.
- Do not modify the user's Markdown files in place.
- Do not overwrite `reference.docx` unless the user explicitly asks to change Word styling.
- Do not run destructive cleanup outside this repository and `~/Library/Services/Markdown 转*.workflow`.
