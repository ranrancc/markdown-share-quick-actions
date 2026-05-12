#!/usr/bin/env python3

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


APP_NAME = "Markdown Share Quick Actions"
ROOT = Path(__file__).resolve().parent

RUNTIME_FILES = [
    "md_share.py",
    "mermaid-prerender.py",
    "requirements-full.txt",
]

RUNTIME_DIRS = {
    "md-to-html-quick-action": [
        "build_pretty_html.py",
        "convert_md_to_html.sh",
        "generate_workflow_icon.py",
        "install_quick_action.py",
        "md-to-html-icon.icns",
    ],
    "md-to-word-quick-action": [
        "convert_md_to_docx.sh",
        "generate_reference_docx.py",
        "generate_workflow_icon.py",
        "install_quick_action.py",
        "md-to-word-icon.icns",
        "reference.docx",
    ],
}


def runtime_root() -> Path:
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_NAME
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        if base:
            return Path(base) / "MarkdownShareQuickActions"
    return Path.home() / ".local" / "share" / "markdown-share-quick-actions"


def copy_file(src: Path, dest: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Missing runtime file: {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def sync_runtime(source_root: Path = ROOT, dest_root: Path | None = None) -> Path:
    dest_root = dest_root or runtime_root()
    dest_root.mkdir(parents=True, exist_ok=True)

    for rel in RUNTIME_FILES:
        src = source_root / rel
        if src.exists():
            copy_file(src, dest_root / rel)

    for dirname, filenames in RUNTIME_DIRS.items():
        for filename in filenames:
            copy_file(source_root / dirname / filename, dest_root / dirname / filename)

    return dest_root


def main() -> int:
    dest = sync_runtime()
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
