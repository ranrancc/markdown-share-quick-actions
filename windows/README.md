# Windows Usage

Windows does not support macOS Finder Quick Actions. This package provides two Windows-friendly options instead:

1. Drag Markdown files onto a `.bat` wrapper.
2. Install SendTo menu entries, then right-click Markdown files and choose `Send to`.

## Requirements

- Windows 10 or later
- Python 3
- Pandoc
- Node.js and Mermaid CLI, only when your Markdown contains ```mermaid diagrams

Install Pandoc and Node.js from:

```text
https://pandoc.org/installing.html
https://nodejs.org/
```

If you need Mermaid diagrams rendered as images, install Mermaid CLI after Node.js:

```bat
npm install -g @mermaid-js/mermaid-cli
```

You can check the environment before converting:

```bat
py -3 md_share.py html note.md --check
```

## Drag-and-Drop

Drag one or more `.md` / `.markdown` files onto:

- `windows\md-to-word.bat`
- `windows\md-to-html.bat`
- `windows\md-to-both.bat`
- `windows\md-share-check.bat`

The output files are written next to the Markdown source files.

## Install SendTo Actions

From the repository root:

```bat
py -3 install_windows.py
```

Then in File Explorer:

1. Select one or more Markdown files.
2. Right-click.
3. Choose `Send to`.
4. Pick `Markdown to Word`, `Markdown to HTML`, `Markdown to Word and HTML`, or `Markdown Share Check`.

## Uninstall

```bat
py -3 uninstall_windows.py
```
