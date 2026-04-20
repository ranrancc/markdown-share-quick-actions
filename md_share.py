#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORD_TEMPLATE = ROOT / "md-to-word-quick-action" / "reference.docx"
HTML_BUILDER = ROOT / "md-to-html-quick-action" / "build_pretty_html.py"
MERMAID_PRERENDER = ROOT / "mermaid-prerender.py"
MARKDOWN_SUFFIXES = {".md", ".markdown"}


def find_pandoc() -> str:
    env_value = os.environ.get("PANDOC_BIN")
    candidates = [
        env_value,
        shutil.which("pandoc"),
        "/opt/homebrew/bin/pandoc",
        "/usr/local/bin/pandoc",
        r"C:\Program Files\Pandoc\pandoc.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Pandoc\pandoc.exe",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        expanded = os.path.expandvars(os.path.expanduser(candidate))
        if Path(expanded).exists() or shutil.which(expanded):
            return expanded
    raise RuntimeError("pandoc was not found. Install pandoc first: https://pandoc.org/installing.html")


def preprocess_mermaid(src: Path, tmp_dir: Path, fmt: str) -> Path:
    """Render ```mermaid blocks to images; return path to rewritten MD."""
    if not MERMAID_PRERENDER.exists():
        return src
    text = src.read_text(encoding="utf-8")
    if "```mermaid" not in text:
        return src
    out_md = tmp_dir / "mermaid-rendered.md"
    assets_dir = tmp_dir / "mermaid-assets"
    result = subprocess.run(
        [sys.executable, str(MERMAID_PRERENDER), str(src), str(out_md), str(assets_dir), fmt],
        capture_output=True,
    )
    if result.returncode == 0 and out_md.exists():
        return out_md
    return src


def postprocess_docx(dest: Path) -> None:
    """Center tables and image captions in a pandoc-generated docx."""
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml.ns import qn as dqn
        from docx.oxml import OxmlElement
    except ImportError:
        return
    doc = Document(dest)
    for table in doc.tables:
        tblPr = table._tbl.find(dqn("w:tblPr"))
        if tblPr is None:
            tblPr = OxmlElement("w:tblPr")
            table._tbl.insert(0, tblPr)
        jc = tblPr.find(dqn("w:jc"))
        if jc is None:
            jc = OxmlElement("w:jc")
            tblPr.append(jc)
        jc.set(dqn("w:val"), "center")
    for para in doc.paragraphs:
        if para.style.name == "Image Caption":
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.save(dest)


def preprocess_markdown(src: Path, dst: Path) -> None:
    text = src.read_text(encoding="utf-8")
    pattern = re.compile(r"!\[\[([^\]]+)\]\]")

    def replace(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        if not inner:
            return match.group(0)
        parts = [part.strip() for part in inner.split("|") if part.strip()]
        target = parts[0]
        alt = ""
        if len(parts) >= 2 and not parts[1].isdigit():
            alt = parts[1]
        if not alt:
            alt = Path(target).stem
        return f"![{alt}]({target})"

    dst.write_text(pattern.sub(replace, text), encoding="utf-8")


def output_path(src: Path, suffix: str, output_dir: Path | None) -> Path:
    base_dir = output_dir if output_dir else src.parent
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"{src.stem}.{suffix}"


def convert_word(src: Path, output_dir: Path | None, pandoc: str) -> Path:
    if not WORD_TEMPLATE.exists():
        raise RuntimeError(f"Missing Word reference template: {WORD_TEMPLATE}")
    dest = output_path(src, "docx", output_dir)
    with tempfile.TemporaryDirectory(prefix="md-share-word.") as tmp:
        tmp_dir = Path(tmp)
        prepared = tmp_dir / "prepared.md"
        preprocess_markdown(src, prepared)
        ready = preprocess_mermaid(prepared, tmp_dir, "png")
        cmd = [
            pandoc,
            str(ready),
            "-o",
            str(dest),
            f"--reference-doc={WORD_TEMPLATE}",
            f"--resource-path={src.parent}",
        ]
        subprocess.run(cmd, check=True)
    postprocess_docx(dest)
    return dest


def convert_html(src: Path, output_dir: Path | None, pandoc: str) -> Path:
    if not HTML_BUILDER.exists():
        raise RuntimeError(f"Missing HTML builder: {HTML_BUILDER}")
    dest = output_path(src, "html", output_dir)
    with tempfile.TemporaryDirectory(prefix="md-share-html.") as tmp:
        tmp_dir = Path(tmp)
        prepared = tmp_dir / "prepared.md"
        rendered = tmp_dir / "rendered.html"
        preprocess_markdown(src, prepared)
        ready = preprocess_mermaid(prepared, tmp_dir, "svg")
        cmd = [
            pandoc,
            str(ready),
            "-o",
            str(rendered),
            "--standalone",
            "--embed-resources",
            f"--resource-path={src.parent}",
            "--metadata",
            f"title={src.stem}",
        ]
        subprocess.run(cmd, check=True)
        subprocess.run([sys.executable, str(HTML_BUILDER), str(rendered), str(dest), src.stem], check=True)
    return dest


def iter_markdown_files(paths: list[Path], recursive: bool) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        expanded = path.expanduser().resolve()
        if expanded.is_dir() and recursive:
            files.extend(p for p in expanded.rglob("*") if p.is_file() and p.suffix.lower() in MARKDOWN_SUFFIXES)
        elif expanded.is_file() and expanded.suffix.lower() in MARKDOWN_SUFFIXES:
            files.append(expanded)
    return sorted(dict.fromkeys(files), key=lambda p: str(p).lower())


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown files to Word or self-contained HTML.")
    parser.add_argument("format", choices=["word", "html", "both"], help="Output format.")
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown files, or directories when --recursive is used.")
    parser.add_argument("-o", "--output-dir", type=Path, default=None, help="Optional output directory.")
    parser.add_argument("--recursive", action="store_true", help="Scan directories recursively for Markdown files.")
    parser.add_argument("--pandoc", default=None, help="Path to pandoc. Overrides auto detection.")
    args = parser.parse_args()

    try:
        pandoc = args.pandoc or find_pandoc()
        files = iter_markdown_files(args.paths, args.recursive)
        if not files:
            print("No Markdown files found.", file=sys.stderr)
            return 2

        outputs: list[Path] = []
        for src in files:
            if args.format in {"word", "both"}:
                outputs.append(convert_word(src, args.output_dir.expanduser().resolve() if args.output_dir else None, pandoc))
            if args.format in {"html", "both"}:
                outputs.append(convert_html(src, args.output_dir.expanduser().resolve() if args.output_dir else None, pandoc))

        for path in outputs:
            print(path)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
