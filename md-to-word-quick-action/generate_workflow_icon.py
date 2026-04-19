#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICON_BASENAME = "md-to-word-icon"
ICON_SIZES = [
    (16, "icon_16x16.png"),
    (32, "icon_16x16@2x.png"),
    (32, "icon_32x32.png"),
    (64, "icon_32x32@2x.png"),
    (128, "icon_128x128.png"),
    (256, "icon_128x128@2x.png"),
    (256, "icon_256x256.png"),
    (512, "icon_256x256@2x.png"),
    (512, "icon_512x512.png"),
    (1024, "icon_512x512@2x.png"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded_rectangle(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_icon(size: int) -> Image.Image:
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    for y in range(size):
        t = y / max(size - 1, 1)
        r = int(37 + 18 * t)
        g = int(99 + 30 * t)
        b = int(235 + 12 * t)
        bg_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=max(2, size // 64)))
    image.alpha_composite(bg)

    outer_margin = int(size * 0.08)
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rectangle(
        shadow_draw,
        (
            outer_margin,
            outer_margin + int(size * 0.02),
            size - outer_margin,
            size - outer_margin + int(size * 0.02),
        ),
        radius=int(size * 0.18),
        fill=(7, 33, 107, 70),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(3, size // 48)))
    image.alpha_composite(shadow)

    doc_x0 = int(size * 0.18)
    doc_y0 = int(size * 0.12)
    doc_x1 = int(size * 0.82)
    doc_y1 = int(size * 0.88)
    corner = int(size * 0.085)
    rounded_rectangle(draw, (doc_x0, doc_y0, doc_x1, doc_y1), radius=corner, fill=(242, 247, 255, 255))

    inner_x0 = int(size * 0.22)
    inner_y0 = int(size * 0.18)
    inner_x1 = int(size * 0.78)
    inner_y1 = int(size * 0.74)
    rounded_rectangle(
        draw,
        (inner_x0, inner_y0, inner_x1, inner_y1),
        radius=int(size * 0.065),
        fill=(31, 92, 231, 255),
    )

    fold = int(size * 0.13)
    draw.polygon(
        [
            (doc_x1 - fold, doc_y0),
            (doc_x1, doc_y0),
            (doc_x1, doc_y0 + fold),
        ],
        fill=(220, 231, 249, 255),
    )
    draw.line(
        [(doc_x1 - fold, doc_y0), (doc_x1 - fold, doc_y0 + fold), (doc_x1, doc_y0 + fold)],
        fill=(190, 207, 233, 255),
        width=max(1, size // 128),
    )

    w_font = font(int(size * 0.30), bold=True)
    md_font = font(int(size * 0.085), bold=True)
    sub_font = font(int(size * 0.07), bold=False)

    title = "W"
    bbox = draw.textbbox((0, 0), title, font=w_font)
    draw.text(
        (
            (inner_x0 + inner_x1 - (bbox[2] - bbox[0])) / 2,
            (inner_y0 + inner_y1 - (bbox[3] - bbox[1])) / 2 - size * 0.03,
        ),
        title,
        font=w_font,
        fill=(255, 255, 255, 255),
    )

    badge_h = int(size * 0.16)
    badge_md = (int(size * 0.22), int(size * 0.73), int(size * 0.48), int(size * 0.73) + badge_h)
    rounded_rectangle(draw, badge_md, radius=int(badge_h * 0.45), fill=(28, 173, 113, 255))

    md_label = "MD"
    md_bbox = draw.textbbox((0, 0), md_label, font=md_font)
    draw.text(
        (
            (badge_md[0] + badge_md[2] - (md_bbox[2] - md_bbox[0])) / 2,
            (badge_md[1] + badge_md[3] - (md_bbox[3] - md_bbox[1])) / 2 - size * 0.004,
        ),
        md_label,
        font=md_font,
        fill=(255, 255, 255, 255),
    )

    sub_label = "DOCX"
    sub_bbox = draw.textbbox((0, 0), sub_label, font=sub_font)
    draw.text(
        (
            doc_x1 - int(size * 0.08) - (sub_bbox[2] - sub_bbox[0]),
            int(size * 0.765),
        ),
        sub_label,
        font=sub_font,
        fill=(85, 111, 160, 255),
    )

    return image


def main() -> int:
    tool_dir = Path(__file__).resolve().parent
    output_path = tool_dir / f"{ICON_BASENAME}.icns"

    with tempfile.TemporaryDirectory(prefix="md-to-word-icon.") as tmp:
        iconset_dir = Path(tmp) / f"{ICON_BASENAME}.iconset"
        iconset_dir.mkdir(parents=True, exist_ok=True)

        for size, filename in ICON_SIZES:
            draw_icon(size).save(iconset_dir / filename)

        subprocess.run(
            ["iconutil", "--convert", "icns", "--output", str(output_path), str(iconset_dir)],
            check=True,
        )

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
