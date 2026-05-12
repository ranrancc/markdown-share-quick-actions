#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path

from install_runtime import runtime_root


WORKFLOWS = [
    "Markdown 转 Word.workflow",
    "Markdown 转 HTML.workflow",
    "Markdown 转 Word（含图表）.workflow",
    "Markdown 转 HTML（含图表）.workflow",
    "MD 转 HTML（选择主题）.workflow",
    "多种文档转 MD.workflow",
    "HTML 转 MD.workflow",
]


def main() -> int:
    services_dir = Path.home() / "Library" / "Services"
    removed = 0
    for workflow in WORKFLOWS:
        path = services_dir / workflow
        if path.exists():
            shutil.rmtree(path)
            print(f"Removed: {path}")
            removed += 1
        else:
            print(f"Not found: {path}")
    runtime = runtime_root()
    if runtime.exists():
        shutil.rmtree(runtime)
        print(f"Removed runtime files: {runtime}")
    print(f"Done. Removed {removed} workflow(s). Run `killall Finder` if needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
