# Release Checklist

Use this before publishing a public release.

## Packaging

- [ ] Remove local-only notes, generated HTML files, `.workflow` bundles, `.venv`, `__pycache__`, and logs.
- [ ] Keep `classic` as the default stable theme.
- [ ] Keep `requirements-full.txt` optional; basic Markdown to Word/HTML should only require Python 3 and Pandoc.
- [ ] Confirm `install_all.py` installs every macOS workflow that `uninstall_all.py` removes.
- [ ] Confirm installers copy runtime files into the stable OS runtime directory.
- [ ] Confirm installed workflows and SendTo wrappers point to the runtime directory, not the downloaded repository folder.
- [ ] Confirm uninstallers remove both menu entries and runtime files.

## Smoke Tests

```bash
python3 -m py_compile install_all.py install_new_actions.py install_windows.py uninstall_all.py uninstall_windows.py md_share.py md-to-html-quick-action/build_pretty_html.py
python3 install_runtime.py
python3 md_share.py html --theme classic /path/to/simple.md
python3 md_share.py html --theme article /path/to/simple.md
python3 md_share.py html --theme report /path/to/simple.md
python3 md_share.py html --theme reading /path/to/simple.md
python3 md_share.py html --theme interactive /path/to/simple.md
```

## macOS

```bash
python3 install_all.py
killall Finder
plutil -lint ~/Library/Services/*.workflow/Contents/document.wflow
```

Verify Finder Quick Actions:

- `Markdown 转 Word（含图表）`
- `Markdown 转 HTML（含图表）`
- `MD 转 HTML（选择主题）`
- `多种文档转 MD`
- `HTML 转 MD`

## Windows

```bat
py -3 install_windows.py
py -3 md_share.py html --theme classic path\to\simple.md
```

Verify SendTo entries:

- `Markdown to Word`
- `Markdown to HTML`
- `Markdown to HTML - Choose Theme`
- `Markdown to Word and HTML`
- `Document to Markdown`
- `HTML to Markdown`
- `Markdown Share Check`

## Documentation

- [ ] README first half is useful for human users.
- [ ] README second half is useful for AI agents.
- [ ] README explains basic mode vs full mode.
- [ ] README explains venv recommendation without making it mandatory.
- [ ] Troubleshooting mentions Pandoc, Mermaid CLI, and image path issues.
