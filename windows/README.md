# Windows Usage

Windows does not support macOS Finder Quick Actions. This package provides two Windows-friendly options instead:

1. Drag Markdown files onto a `.bat` wrapper.
2. Install SendTo menu entries, then right-click Markdown files and choose `Send to`.

## Requirements

- Windows 10 or later
- Python 3
- Pandoc

Install Pandoc from:

```text
https://pandoc.org/installing.html
```

## Drag-and-Drop

Drag one or more `.md` / `.markdown` files onto:

- `windows\md-to-word.bat`
- `windows\md-to-html.bat`
- `windows\md-to-both.bat`

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
4. Pick `Markdown to Word`, `Markdown to HTML`, or `Markdown to Word and HTML`.

## Uninstall

```bat
py -3 uninstall_windows.py
```
