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
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MERMAID_PATTERN = re.compile(r"```mermaid[ \t]*\r?\n(.*?)```", re.DOTALL | re.IGNORECASE)
TOOL_PATH = "/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def subprocess_env() -> dict[str, str]:
    env = os.environ.copy()
    current_path = env.get("PATH", "")
    env["PATH"] = f"{TOOL_PATH}:{current_path}" if current_path else TOOL_PATH
    return env


def mermaid_commands() -> list[list[str]]:
    """Return Mermaid render commands, preferring an installed CLI over npx."""
    env_value = os.environ.get("MERMAID_CLI")
    npm_prefix = os.environ.get("APPDATA")
    candidates = [
        env_value,
        shutil.which("mmdc"),
        "/opt/homebrew/bin/mmdc",
        "/usr/local/bin/mmdc",
        str(Path(npm_prefix) / "npm" / "mmdc.cmd") if npm_prefix else None,
        str(Path(npm_prefix) / "npm" / "mmdc") if npm_prefix else None,
    ]
    commands: list[list[str]] = []
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            commands.append([candidate])

    npx_candidates = [
        shutil.which("npx"),
        "/opt/homebrew/bin/npx",
        "/usr/local/bin/npx",
        str(Path(npm_prefix) / "npm" / "npx.cmd") if npm_prefix else None,
        str(Path(npm_prefix) / "npm" / "npx") if npm_prefix else None,
    ]
    npx = next((item for item in npx_candidates if item and Path(item).exists()), None)
    if npx:
        commands.append([npx, "--yes", "@mermaid-js/mermaid-cli"])
    return commands


def chrome_executable() -> str | None:
    candidates = [
        os.environ.get("PUPPETEER_EXECUTABLE_PATH"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        str(Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def render_block(code: str, out_path: Path) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile(
        suffix=".mmd", mode="w", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        tmp_mmd = f.name
    puppeteer_config = None
    browser_path = chrome_executable()
    if browser_path:
        with tempfile.NamedTemporaryFile(
            suffix=".json", mode="w", delete=False, encoding="utf-8"
        ) as f:
            json.dump(
                {
                    "executablePath": browser_path,
                    "headless": True,
                    "args": ["--no-sandbox", "--disable-setuid-sandbox"],
                },
                f,
            )
            puppeteer_config = f.name
    try:
        errors: list[str] = []
        for base_cmd in mermaid_commands():
            cmd = [
                *base_cmd,
                "-i",
                tmp_mmd,
                "-o",
                str(out_path),
                "--backgroundColor",
                "white",
                "--quiet",
            ]
            if puppeteer_config:
                cmd.extend(["-p", puppeteer_config])
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=45,
                    env=subprocess_env(),
                )
            except Exception as exc:
                errors.append(f"{base_cmd[0]}: {exc}")
                continue
            if result.returncode == 0 and out_path.exists():
                return True, ""
            detail = (result.stderr or result.stdout or "").strip()
            errors.append(f"{base_cmd[0]} exited {result.returncode}: {detail[:500]}")
        if not errors:
            return False, "No Mermaid CLI found. Install with: npm install -g @mermaid-js/mermaid-cli"
        return False, " | ".join(errors)
    finally:
        Path(tmp_mmd).unlink(missing_ok=True)
        if puppeteer_config:
            Path(puppeteer_config).unlink(missing_ok=True)


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

        ok, error = render_block(code, img_path)
        if ok:
            # Absolute path so pandoc can find it from any working directory
            return f"![图{idx}]({img_path})"
        print(f"mermaid-prerender: block {idx} failed: {error}", file=sys.stderr)
        failed.append(idx)
        return match.group(0)

    new_text = MERMAID_PATTERN.sub(replace_block, text)
    output_path.write_text(new_text, encoding="utf-8")

    if failed:
        print(f"mermaid-prerender: failed blocks {failed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
