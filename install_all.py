#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TOOLS = [
    ROOT / "md-to-word-quick-action",
    ROOT / "md-to-html-quick-action",
]


def run(cmd: list[str], cwd: Path) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> int:
    if sys.platform != "darwin":
        print("This package installs macOS Finder Quick Actions and requires macOS.", file=sys.stderr)
        return 2

    if shutil.which("pandoc") is None and not Path("/opt/homebrew/bin/pandoc").exists():
        print("pandoc was not found. Install it first, for example: brew install pandoc", file=sys.stderr)
        return 2

    for tool_dir in TOOLS:
        if not tool_dir.exists():
            print(f"Missing tool directory: {tool_dir}", file=sys.stderr)
            return 1

    word_dir = ROOT / "md-to-word-quick-action"
    run([sys.executable, "generate_reference_docx.py"], word_dir)
    run([sys.executable, "install_quick_action.py"], word_dir)

    html_dir = ROOT / "md-to-html-quick-action"
    run([sys.executable, "install_quick_action.py"], html_dir)

    print()
    print("Installed Finder Quick Actions:")
    print("- Markdown 转 Word")
    print("- Markdown 转 HTML")
    print()
    print("Run `killall Finder` if the menu does not appear immediately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
