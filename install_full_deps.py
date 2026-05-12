#!/usr/bin/env python3

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from install_runtime import sync_runtime


def venv_python(runtime: Path) -> Path:
    if os.name == "nt":
        return runtime / ".venv" / "Scripts" / "python.exe"
    return runtime / ".venv" / "bin" / "python"


def main() -> int:
    runtime = sync_runtime()
    py = venv_python(runtime)
    if not py.exists():
        subprocess.run([sys.executable, "-m", "venv", str(runtime / ".venv")], check=True)
    subprocess.run([str(py), "-m", "pip", "install", "-U", "pip"], check=True)
    subprocess.run([str(py), "-m", "pip", "install", "-r", str(runtime / "requirements-full.txt")], check=True)
    print(f"Installed full dependencies into: {runtime / '.venv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
