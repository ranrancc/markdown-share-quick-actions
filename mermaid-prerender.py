#!/usr/bin/env python3
"""Pre-render Mermaid code blocks in a Markdown file to PNG or SVG images.

Usage:
  mermaid-prerender.py <input.md> <output.md> <assets_dir> [png|svg]

Each ```mermaid block is rendered via npx @mermaid-js/mermaid-cli and replaced
with a standard Markdown image reference using an absolute path, so pandoc can
locate the file regardless of its working directory.  If rendering fails for a
block the original code fence is preserved unchanged.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MERMAID_PATTERN = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)


def render_block(code: str, out_path: Path) -> bool:
    with tempfile.NamedTemporaryFile(
        suffix=".mmd", mode="w", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        tmp_mmd = f.name
    try:
        result = subprocess.run(
            [
                "npx",
                "--yes",
                "@mermaid-js/mermaid-cli",
                "-i",
                tmp_mmd,
                "-o",
                str(out_path),
                "--backgroundColor",
                "white",
                "--quiet",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return out_path.exists()
    except Exception:
        return False
    finally:
        Path(tmp_mmd).unlink(missing_ok=True)


def main() -> int:
    if len(sys.argv) < 4:
        print(
            "Usage: mermaid-prerender.py <input.md> <output.md> <assets_dir> [png|svg]",
            file=sys.stderr,
        )
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    assets_dir = Path(sys.argv[3])
    fmt = sys.argv[4] if len(sys.argv) > 4 else "png"

    assets_dir.mkdir(parents=True, exist_ok=True)
    text = input_path.read_text(encoding="utf-8")

    if not MERMAID_PATTERN.search(text):
        # No mermaid blocks — write unchanged and exit fast
        output_path.write_text(text, encoding="utf-8")
        return 0

    counter = [0]
    failed: list[int] = []

    def replace_block(match: re.Match) -> str:  # type: ignore[type-arg]
        code = match.group(1)
        counter[0] += 1
        idx = counter[0]
        h = hashlib.md5(code.encode()).hexdigest()[:6]
        img_name = f"mermaid-{idx:02d}-{h}.{fmt}"
        img_path = assets_dir / img_name

        if render_block(code, img_path):
            # Absolute path so pandoc can find it from any working directory
            return f"![图{idx}]({img_path})"
        failed.append(idx)
        return match.group(0)

    new_text = MERMAID_PATTERN.sub(replace_block, text)
    output_path.write_text(new_text, encoding="utf-8")

    if failed:
        print(f"mermaid-prerender: failed blocks {failed}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
