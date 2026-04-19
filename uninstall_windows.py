#!/usr/bin/env python3

from __future__ import annotations

import os
from pathlib import Path


SENDTO = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "SendTo"
SHORTCUTS = [
    "Markdown to Word.bat",
    "Markdown to HTML.bat",
    "Markdown to Word and HTML.bat",
]


def main() -> int:
    removed = 0
    for name in SHORTCUTS:
        path = SENDTO / name
        if path.exists():
            path.unlink()
            print(f"Removed: {path}")
            removed += 1
    print(f"Done. Removed {removed} SendTo action(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
