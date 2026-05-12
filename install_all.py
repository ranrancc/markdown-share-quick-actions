#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from install_runtime import sync_runtime


ROOT = Path(__file__).resolve().parent
TOOLS = ["md-to-word-quick-action", "md-to-html-quick-action"]


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

    runtime = sync_runtime(ROOT)
    print(f"Installed runtime files to: {runtime}", flush=True)

    for tool_name in TOOLS:
        tool_dir = runtime / tool_name
        if not tool_dir.exists():
            print(f"Missing tool directory: {tool_dir}", file=sys.stderr)
            return 1

    word_dir = runtime / "md-to-word-quick-action"
    run([sys.executable, "generate_reference_docx.py"], word_dir)
    run([sys.executable, "install_quick_action.py"], word_dir)

    html_dir = runtime / "md-to-html-quick-action"
    run([sys.executable, "install_quick_action.py"], html_dir)

    run([sys.executable, str(ROOT / "install_new_actions.py"), str(runtime)], ROOT)

    print()
    print("Installed Finder Quick Actions:")
    print("- Markdown 转 Word（含图表）")
    print("- Markdown 转 HTML（含图表）")
    print("- MD 转 HTML（选择主题）")
    print("- 多种文档转 MD")
    print("- HTML 转 MD")
    print()
    print("Run `killall Finder` if the menu does not appear immediately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
