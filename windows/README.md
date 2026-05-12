# Windows Usage

Windows uses File Explorer `Send to` entries and drag-and-drop `.bat` wrappers.

## Requirements

- Windows 10 or later
- Python 3
- Pandoc
- Node.js and Mermaid CLI, only when Markdown contains Mermaid diagrams

Install Pandoc and Node.js from:

```text
https://pandoc.org/installing.html
https://nodejs.org/
```

If you need Mermaid diagrams rendered as images:

```bat
npm install -g @mermaid-js/mermaid-cli
```

## Install SendTo Actions

From the repository root:

```bat
py -3 install_windows.py
```

The installer copies runtime files to:

```text
%LOCALAPPDATA%\MarkdownShareQuickActions\
```

It then writes SendTo wrappers that point to that stable runtime directory. After installation, the downloaded repository folder can be moved or deleted.

Then in File Explorer:

1. Select one or more files.
2. Right-click.
3. Choose `Send to`.
4. Pick a Markdown action.

Installed entries:

```text
Markdown to Word
Markdown to HTML
Markdown to HTML - Choose Theme
Markdown to Word and HTML
Document to Markdown
HTML to Markdown
Markdown Share Check
```

## Drag-and-Drop

Drag files onto:

```text
windows\md-to-word.bat
windows\md-to-html.bat
windows\md-to-html-select-theme.bat
windows\md-to-both.bat
windows\document-to-md.bat
windows\html-to-md.bat
windows\md-share-check.bat
```

## Full Mode

`Document to Markdown` and `HTML to Markdown` may need extra Python packages. Use a virtual environment:

```bat
py -3 install_full_deps.py
py -3 install_windows.py
```

## Check

```bat
py -3 md_share.py html note.md --check
py -3 md_share.py html --theme classic note.md
```

## Uninstall

```bat
py -3 uninstall_windows.py
```
