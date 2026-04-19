#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W)


def qn(tag: str) -> str:
    return f"{{{W}}}{tag}"


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    child = parent.find(qn(tag))
    if child is None:
        child = ET.SubElement(parent, qn(tag))
    return child


def set_fonts(run_props: ET.Element, ascii_font: str, east_asia_font: str, hint: str = "eastAsia") -> None:
    r_fonts = ensure_child(run_props, "rFonts")
    r_fonts.set(qn("ascii"), ascii_font)
    r_fonts.set(qn("hAnsi"), ascii_font)
    r_fonts.set(qn("eastAsia"), east_asia_font)
    r_fonts.set(qn("cs"), ascii_font)
    r_fonts.set(qn("hint"), hint)


def set_size(run_props: ET.Element, size_half_points: int) -> None:
    sz = ensure_child(run_props, "sz")
    sz.set(qn("val"), str(size_half_points))
    sz_cs = ensure_child(run_props, "szCs")
    sz_cs.set(qn("val"), str(size_half_points))


def apply_style(
    styles_root: ET.Element,
    style_id: str,
    *,
    ascii_font: str,
    east_asia_font: str,
    size: int,
    color: str | None = None,
    bold: bool = False,
    italic: bool = False,
    spacing_before: int | None = None,
    spacing_after: int | None = None,
    line: int | None = None,
    indent_left: int | None = None,
    indent_hanging: int | None = None,
    indent_first_line: int | None = None,
    shading_fill: str | None = None,
) -> None:
    style = styles_root.find(f"./{qn('style')}[@{qn('styleId')}='{style_id}']")
    if style is None:
        return

    p_pr = ensure_child(style, "pPr")
    r_pr = ensure_child(style, "rPr")

    set_fonts(r_pr, ascii_font, east_asia_font)
    set_size(r_pr, size)

    if color:
        color_node = ensure_child(r_pr, "color")
        color_node.set(qn("val"), color)

    if bold:
        ensure_child(r_pr, "b")

    if italic:
        ensure_child(r_pr, "i")

    if spacing_before is not None or spacing_after is not None or line is not None:
        spacing = ensure_child(p_pr, "spacing")
        if spacing_before is not None:
            spacing.set(qn("before"), str(spacing_before))
        if spacing_after is not None:
            spacing.set(qn("after"), str(spacing_after))
        if line is not None:
            spacing.set(qn("line"), str(line))
            spacing.set(qn("lineRule"), "auto")

    if indent_left is not None or indent_hanging is not None:
        ind = ensure_child(p_pr, "ind")
        if indent_left is not None:
            ind.set(qn("left"), str(indent_left))
        if indent_hanging is not None:
            ind.set(qn("hanging"), str(indent_hanging))
        if indent_first_line is not None:
            ind.set(qn("firstLine"), str(indent_first_line))
    elif indent_first_line is not None:
        ind = ensure_child(p_pr, "ind")
        ind.set(qn("firstLine"), str(indent_first_line))

    if shading_fill:
        shd = ensure_child(r_pr, "shd")
        shd.set(qn("val"), "clear")
        shd.set(qn("fill"), shading_fill)


def update_styles_xml(styles_xml: bytes) -> bytes:
    root = ET.fromstring(styles_xml)

    doc_defaults = ensure_child(root, "docDefaults")
    rpr_default = ensure_child(doc_defaults, "rPrDefault")
    default_rpr = ensure_child(rpr_default, "rPr")
    set_fonts(default_rpr, "Calibri", "宋体")
    set_size(default_rpr, 24)
    lang = ensure_child(default_rpr, "lang")
    lang.set(qn("val"), "en-US")
    lang.set(qn("eastAsia"), "zh-CN")

    ppr_default = ensure_child(doc_defaults, "pPrDefault")
    default_ppr = ensure_child(ppr_default, "pPr")
    spacing = ensure_child(default_ppr, "spacing")
    spacing.set(qn("before"), "0")
    spacing.set(qn("after"), "140")
    spacing.set(qn("line"), "336")
    spacing.set(qn("lineRule"), "auto")
    ind = ensure_child(default_ppr, "ind")
    ind.set(qn("firstLine"), "420")

    apply_style(
        root,
        "Normal",
        ascii_font="Georgia",
        east_asia_font="宋体",
        size=24,
        color="222222",
        spacing_after=140,
        line=336,
        indent_first_line=420,
    )
    apply_style(
        root,
        "Title",
        ascii_font="Calibri",
        east_asia_font="微软雅黑",
        size=40,
        color="1F3A5F",
        bold=True,
        spacing_before=0,
        spacing_after=220,
        line=300,
    )
    apply_style(
        root,
        "Subtitle",
        ascii_font="Calibri",
        east_asia_font="等线",
        size=24,
        color="5C6B7A",
        spacing_before=0,
        spacing_after=180,
        line=280,
    )
    apply_style(
        root,
        "Heading1",
        ascii_font="Calibri",
        east_asia_font="微软雅黑",
        size=32,
        color="1F4E79",
        bold=True,
        spacing_before=260,
        spacing_after=140,
        line=300,
    )
    apply_style(
        root,
        "Heading2",
        ascii_font="Calibri",
        east_asia_font="等线",
        size=27,
        color="285A6E",
        bold=True,
        spacing_before=220,
        spacing_after=100,
        line=288,
    )
    apply_style(
        root,
        "Heading3",
        ascii_font="Calibri",
        east_asia_font="等线",
        size=24,
        color="4B5D73",
        bold=True,
        spacing_before=180,
        spacing_after=60,
        line=288,
    )
    apply_style(
        root,
        "BlockText",
        ascii_font="Georgia",
        east_asia_font="楷体",
        size=23,
        color="5A5A5A",
        italic=True,
        spacing_before=60,
        spacing_after=140,
        line=320,
        indent_left=520,
    )
    apply_style(
        root,
        "SourceCode",
        ascii_font="Consolas",
        east_asia_font="等线",
        size=20,
        color="2D3748",
        spacing_before=80,
        spacing_after=140,
        line=260,
        shading_fill="F3F5F7",
    )
    apply_style(
        root,
        "Table",
        ascii_font="Calibri",
        east_asia_font="宋体",
        size=21,
        spacing_after=0,
        line=260,
    )
    apply_style(
        root,
        "Compact",
        ascii_font="Calibri",
        east_asia_font="宋体",
        size=21,
        color="222222",
        spacing_before=0,
        spacing_after=0,
        line=240,
        indent_first_line=0,
    )
    apply_style(
        root,
        "Caption",
        ascii_font="Calibri",
        east_asia_font="等线",
        size=20,
        color="6C7883",
        italic=True,
        spacing_after=60,
        line=260,
    )
    apply_style(
        root,
        "ImageCaption",
        ascii_font="Calibri",
        east_asia_font="等线",
        size=20,
        color="6C7883",
        italic=True,
        spacing_after=60,
        line=260,
    )
    apply_style(
        root,
        "TableCaption",
        ascii_font="Calibri",
        east_asia_font="等线",
        size=20,
        color="6C7883",
        italic=True,
        spacing_after=60,
        line=260,
    )
    apply_style(
        root,
        "Hyperlink",
        ascii_font="Calibri",
        east_asia_font="等线",
        size=22,
        color="1E5A96",
    )
    apply_style(
        root,
        "TOCHeading",
        ascii_font="Calibri",
        east_asia_font="微软雅黑",
        size=26,
        color="1F4E79",
        bold=True,
        spacing_before=180,
        spacing_after=100,
        line=288,
    )

    for style_id in ("TitleChar", "SubtitleChar", "Heading1Char", "Heading2Char", "Heading3Char", "VerbatimChar"):
        style = root.find(f"./{qn('style')}[@{qn('styleId')}='{style_id}']")
        if style is None:
            continue
        r_pr = ensure_child(style, "rPr")
        if style_id == "VerbatimChar":
            set_fonts(r_pr, "Consolas", "等线")
            set_size(r_pr, 20)
        elif style_id == "TitleChar":
            set_fonts(r_pr, "Calibri", "微软雅黑")
            set_size(r_pr, 40)
        elif style_id == "SubtitleChar":
            set_fonts(r_pr, "Calibri", "等线")
            set_size(r_pr, 24)
        else:
            set_fonts(r_pr, "Calibri", "等线")

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def update_document_xml(document_xml: bytes) -> bytes:
    root = ET.fromstring(document_xml)
    sect_pr = root.find(f".//{qn('sectPr')}")
    if sect_pr is not None:
        pg_mar = ensure_child(sect_pr, "pgMar")
        pg_mar.set(qn("top"), "1320")
        pg_mar.set(qn("right"), "1260")
        pg_mar.set(qn("bottom"), "1320")
        pg_mar.set(qn("left"), "1260")
        pg_mar.set(qn("header"), "720")
        pg_mar.set(qn("footer"), "720")
        pg_mar.set(qn("gutter"), "0")

    # Keep the sample table in the reference document readable; actual exported
    # tables will be generated by pandoc and can size themselves independently.
    for tbl in root.findall(f".//{qn('tbl')}"):
        tbl_grid = tbl.find(qn("tblGrid"))
        if tbl_grid is not None:
            grid_cols = tbl_grid.findall(qn("gridCol"))
            if len(grid_cols) == 2:
                for col in grid_cols:
                    col.set(qn("w"), "3960")

        for tc in tbl.findall(f".//{qn('tc')}"):
            tc_pr = ensure_child(tc, "tcPr")
            tc_w = ensure_child(tc_pr, "tcW")
            tc_w.set(qn("w"), "3960")
            tc_w.set(qn("type"), "dxa")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def refresh_docx(docx_path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / docx_path.name
        with zipfile.ZipFile(docx_path, "r") as src, zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as dst:
            for info in src.infolist():
                data = src.read(info.filename)
                if info.filename == "word/styles.xml":
                    data = update_styles_xml(data)
                elif info.filename == "word/document.xml":
                    data = update_document_xml(data)
                dst.writestr(info, data)
        shutil.move(tmp_path, docx_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the default reference.docx template.")
    parser.add_argument(
        "--output",
        default=Path(__file__).resolve().with_name("reference.docx"),
        type=Path,
        help="Output path for reference.docx",
    )
    args = parser.parse_args()

    pandoc_bin = shutil.which("pandoc") or "/opt/homebrew/bin/pandoc"
    if not Path(pandoc_bin).exists():
        raise SystemExit("pandoc not found. Please install pandoc first.")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    seed_markdown = """% 高校教师分享稿模板
% 适合从 Obsidian 直接导出给同行、学生或合作伙伴阅读

# 标题示例

这是一个偏高校教师分享风的 Word 模板。它保留 Markdown 的简洁结构，但在导出后更像一篇已经整理过的成稿，适合转发、交流与轻正式分享。

## 二级标题

- 列表条目一
- 列表条目二

> 这是引用块示例，用于强调或摘录。

### 三级标题

```python
print("hello world")
```

| 列一 | 列二 |
| --- | --- |
| A | B |
"""

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        seed_path = tmp_dir_path / "seed.md"
        seed_path.write_text(seed_markdown, encoding="utf-8")
        subprocess.run([pandoc_bin, str(seed_path), "-o", str(args.output)], check=True)

    refresh_docx(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
