#!/usr/bin/env python3

from __future__ import annotations

import os
import shutil
from pathlib import Path

from install_runtime import runtime_root


SENDTO = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "SendTo"
SHORTCUTS = [
    "Markdown to Word.bat",
    "Markdown to HTML.bat",
    "Markdown to HTML - Choose Theme.bat",
    "Markdown to Word and HTML.bat",
    "Document to Markdown.bat",
    "HTML to Markdown.bat",
    "Markdown Share Check.bat",
]


def main() -> int:
    removed = 0
    for name in SHORTCUTS:
        path = SENDTO / name
        if path.exists():
            path.unlink()
            print(f"Removed: {path}")
            removed += 1
    runtime = runtime_root()
    if runtime.exists():
        shutil.rmtree(runtime)
        print(f"Removed runtime files: {runtime}")
    print(f"Done. Removed {removed} SendTo action(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
