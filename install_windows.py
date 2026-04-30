#!/usr/bin/env python3

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SENDTO = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "SendTo"


SHORTCUTS = {
    "Markdown to Word.bat": "md-to-word.bat",
    "Markdown to HTML.bat": "md-to-html.bat",
    "Markdown to Word and HTML.bat": "md-to-both.bat",
    "Markdown Share Check.bat": "md-share-check.bat",
}


def main() -> int:
    if os.name != "nt":
        print("This installer is for Windows. Use install_all.py on macOS.")
        return 2
    if not SENDTO.exists():
        print(f"SendTo directory not found: {SENDTO}", file=sys.stderr)
        return 1
    windows_dir = ROOT / "windows"
    for label, target in SHORTCUTS.items():
        src = windows_dir / target
        dest = SENDTO / label
        if not src.exists():
            print(f"Missing wrapper: {src}", file=sys.stderr)
            return 1
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Installed: {dest}")
    print("Done. Right-click a Markdown file, choose Send to, then pick a Markdown action.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
