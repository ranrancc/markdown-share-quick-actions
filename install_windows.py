#!/usr/bin/env python3

from __future__ import annotations

import os
import sys
from pathlib import Path

from install_runtime import sync_runtime


ROOT = Path(__file__).resolve().parent
SENDTO = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "SendTo"


SHORTCUTS = {
    "Markdown to Word.bat": '%PY% "%ROOT%\\md_share.py" word %*',
    "Markdown to HTML.bat": '%PY% "%ROOT%\\md_share.py" html %*',
    "Markdown to HTML - Choose Theme.bat": None,
    "Markdown to Word and HTML.bat": '%PY% "%ROOT%\\md_share.py" both %*',
    "Document to Markdown.bat": '%PY% "%ROOT%\\md_share.py" to-md %*',
    "HTML to Markdown.bat": '%PY% "%ROOT%\\md_share.py" html-to-md %*',
    "Markdown Share Check.bat": '%PY% "%ROOT%\\md_share.py" html --check %*',
}


def quote_batch_value(value: Path) -> str:
    return str(value).replace("^", "^^").replace("%", "%%").replace("&", "^&")


def command_prefix() -> str:
    return r"""if exist "%ROOT%\.venv\Scripts\python.exe" (
  set "PY=%ROOT%\.venv\Scripts\python.exe"
) else (
  set "PY=py -3"
)"""


def build_wrapper(root_path: Path, command: str | None) -> str:
    root = quote_batch_value(root_path)
    if command is None:
        # FIX: %* (file path) must come BEFORE --theme so argparse parses correctly
        body = r"""
echo Choose an HTML theme:
echo   1. Classic
echo   2. Article
echo   3. Report
echo   4. Reading
echo   5. Interactive
choice /C 12345 /N /M "Theme [1-5]: "
if errorlevel 5 set "THEME=interactive"
if errorlevel 4 if not defined THEME set "THEME=reading"
if errorlevel 3 if not defined THEME set "THEME=report"
if errorlevel 2 if not defined THEME set "THEME=article"
if errorlevel 1 if not defined THEME set "THEME=classic"
%PY% "%ROOT%\md_share.py" html %* --theme "%THEME%"
""".strip()
    else:
        body = command
    return f"""@echo off
setlocal
set "ROOT={root}"
{command_prefix()}
{body}
if errorlevel 1 pause
"""


def main() -> int:
    if os.name != "nt":
        print("This installer is for Windows. Use install_all.py on macOS.")
        return 2
    if not SENDTO.exists():
        print(f"SendTo directory not found: {SENDTO}", file=sys.stderr)
        return 1
    runtime = sync_runtime(ROOT)
    print(f"Installed runtime files to: {runtime}", flush=True)
    for label, command in SHORTCUTS.items():
        dest = SENDTO / label
        dest.write_text(build_wrapper(runtime, command), encoding="utf-8")
        print(f"Installed: {dest}")
    print("Done. Right-click a Markdown file, choose Send to, then pick a Markdown action.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
