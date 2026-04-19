#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ICON_BASENAME = "md-to-html-icon"
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


def font(size: int, bold: bool = False):
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


def rounded_rectangle(draw: ImageDraw.ImageDraw, box, radius: int, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_icon(size: int) -> Image.Image:
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    for y in range(size):
        t = y / max(size - 1, 1)
        r = int(253 - 13 * t)
        g = int(147 + 48 * t)
        b = int(60 + 68 * t)
        bg_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=max(2, size // 64)))
    image.alpha_composite(bg)

    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rectangle(
        shadow_draw,
        (int(size * 0.1), int(size * 0.13), int(size * 0.9), int(size * 0.9)),
        radius=int(size * 0.16),
        fill=(98, 42, 7, 70),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(3, size // 48)))
    image.alpha_composite(shadow)

    draw = ImageDraw.Draw(image)
    doc = (int(size * 0.16), int(size * 0.1), int(size * 0.84), int(size * 0.88))
    rounded_rectangle(draw, doc, radius=int(size * 0.085), fill=(255, 249, 243, 255))

    fold = int(size * 0.14)
    draw.polygon(
        [
            (doc[2] - fold, doc[1]),
            (doc[2], doc[1]),
            (doc[2], doc[1] + fold),
        ],
        fill=(255, 232, 216, 255),
    )
    draw.line(
        [(doc[2] - fold, doc[1]), (doc[2] - fold, doc[1] + fold), (doc[2], doc[1] + fold)],
        fill=(238, 205, 184, 255),
        width=max(1, size // 128),
    )

    panel = (int(size * 0.21), int(size * 0.18), int(size * 0.79), int(size * 0.56))
    rounded_rectangle(draw, panel, radius=int(size * 0.055), fill=(237, 104, 37, 255))

    angle_font = font(int(size * 0.18), bold=True)
    code_font = font(int(size * 0.09), bold=True)
    md_font = font(int(size * 0.08), bold=True)

    for label, xpos in [("<", int(size * 0.29)), (">", int(size * 0.66))]:
      bbox = draw.textbbox((0, 0), label, font=angle_font)
      draw.text(
          (xpos - (bbox[2] - bbox[0]) / 2, int(size * 0.235)),
          label,
          font=angle_font,
          fill=(255, 255, 255, 255),
      )

    slash_bbox = draw.textbbox((0, 0), "/", font=code_font)
    draw.text(
        ((panel[0] + panel[2] - (slash_bbox[2] - slash_bbox[0])) / 2, int(size * 0.29)),
        "/",
        font=code_font,
        fill=(255, 234, 223, 255),
    )

    badge = (int(size * 0.22), int(size * 0.68), int(size * 0.46), int(size * 0.68) + int(size * 0.15))
    rounded_rectangle(draw, badge, radius=int(size * 0.05), fill=(33, 163, 107, 255))
    md_bbox = draw.textbbox((0, 0), "MD", font=md_font)
    draw.text(
        (
            (badge[0] + badge[2] - (md_bbox[2] - md_bbox[0])) / 2,
            (badge[1] + badge[3] - (md_bbox[3] - md_bbox[1])) / 2 - size * 0.003,
        ),
        "MD",
        font=md_font,
        fill=(255, 255, 255, 255),
    )

    html_bbox = draw.textbbox((0, 0), "HTML", font=code_font)
    draw.text(
        (doc[2] - int(size * 0.08) - (html_bbox[2] - html_bbox[0]), int(size * 0.72)),
        "HTML",
        font=code_font,
        fill=(123, 89, 68, 255),
    )

    return image


def main() -> int:
    tool_dir = Path(__file__).resolve().parent
    output_path = tool_dir / f"{ICON_BASENAME}.icns"

    with tempfile.TemporaryDirectory(prefix="md-to-html-icon.") as tmp:
        iconset_dir = Path(tmp) / f"{ICON_BASENAME}.iconset"
        iconset_dir.mkdir(parents=True, exist_ok=True)
        for size, filename in ICON_SIZES:
            draw_icon(size).save(iconset_dir / filename)
        subprocess.run(["iconutil", "--convert", "icns", "--output", str(output_path), str(iconset_dir)], check=True)

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
