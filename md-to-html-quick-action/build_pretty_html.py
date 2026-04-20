#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import sys
from pathlib import Path


STYLE = """
<style>
  :root {
    --bg: #eef2f7;
    --paper: #ffffff;
    --ink: #1e293b;
    --muted: #64748b;
    --line: #e2e8f0;
    --accent: #2563eb;
    --accent-dark: #1d4ed8;
    --accent-bg: #eff6ff;
    --header-from: #1e3a5f;
    --header-to: #2563eb;
    --shadow: 0 24px 80px rgba(30, 58, 138, 0.13);
    --radius: 24px;
    --base-font-size: 20px;
    --font-size: 20px;
    --deck-max-width: 1100px;
    --deck-fullscreen-width: min(96vw, 1320px);
    --content-width: min(var(--deck-max-width), calc(100vw - 72px));
    --text-column-width: min(44em, 100%);
    --wide-column-width: min(56em, 100%);
    --zoom-scale: 1;
  }

  * { box-sizing: border-box; }

  html {
    font-size: var(--font-size);
    scroll-behavior: smooth;
    background: var(--bg);
  }

  body {
    margin: 0;
    min-height: 100vh;
    color: var(--ink);
    font-family: -apple-system, "PingFang SC", "Hiragino Sans GB", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    line-height: 1.78;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }

  /* ── shell & stage ── */

  .page-shell {
    min-height: 100vh;
    width: 100%;
    padding: 32px 20px 72px;
    display: grid;
    justify-items: center;
    align-content: start;
  }

  .stage {
    width: var(--content-width);
    margin: 0 auto;
    max-width: 100%;
  }

  /* ── toolbar ── */

  .toolbar {
    position: sticky;
    top: 14px;
    z-index: 20;
    width: 100%;
    margin: 0 0 20px;
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
  }

  .toolbar button {
    appearance: none;
    border: 0;
    border-radius: 999px;
    padding: 11px 22px;
    font: 600 14px/1.1 -apple-system, "PingFang SC", sans-serif;
    letter-spacing: 0.03em;
    cursor: pointer;
    color: #ffffff;
    background: linear-gradient(135deg, var(--accent), var(--accent-dark));
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.30);
    transition: transform 0.15s ease, filter 0.15s ease;
  }

  .toolbar button:hover { transform: translateY(-1px); filter: brightness(1.07); }
  .toolbar button:active { transform: translateY(0); }

  .zoom-panel {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 9px 16px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid var(--line);
    box-shadow: 0 4px 16px rgba(30, 41, 59, 0.08);
    font: 600 13px/1.1 -apple-system, "PingFang SC", sans-serif;
    color: var(--accent-dark);
    backdrop-filter: blur(14px);
  }

  .zoom-slider {
    -webkit-appearance: none;
    appearance: none;
    width: 130px;
    height: 4px;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent) var(--pct, 20%), var(--line) var(--pct, 20%));
    outline: none;
    cursor: pointer;
    border: none;
  }

  .zoom-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.35);
    cursor: pointer;
    transition: transform 0.12s ease, box-shadow 0.12s ease;
  }

  .zoom-slider::-webkit-slider-thumb:hover {
    transform: scale(1.2);
    box-shadow: 0 3px 12px rgba(37, 99, 235, 0.45);
  }

  .zoom-slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--accent);
    border: none;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.35);
    cursor: pointer;
  }

  .zoom-value {
    min-width: 3.6em;
    text-align: right;
    color: var(--accent-dark);
    font-variant-numeric: tabular-nums;
  }

  /* ── card ── */

  .deck {
    width: 100%;
    background: var(--paper);
    border: 1px solid rgba(226, 232, 240, 0.6);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: clip;
  }

  .deck-header {
    padding: 44px 52px 36px;
    background: linear-gradient(135deg, var(--header-from) 0%, var(--header-to) 100%);
    position: relative;
    overflow: hidden;
  }

  .deck-header::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 75% 40%, rgba(255,255,255,0.10), transparent 55%);
    pointer-events: none;
  }

  .deck-title {
    position: relative;
    z-index: 1;
    margin: 0;
    font-size: clamp(1.5em, 2.8vw, 2.2em);
    font-weight: 800;
    line-height: 1.15;
    color: #ffffff;
    text-align: center;
    letter-spacing: -0.02em;
    max-width: 28em;
    margin-left: auto;
    margin-right: auto;
    text-shadow: 0 2px 14px rgba(0, 0, 0, 0.20);
  }

  .deck-body {
    padding: 36px 52px 64px;
  }

  .deck-body > *:first-child { margin-top: 0; }
  .deck-body > *:last-child { margin-bottom: 0; }

  /* ── headings ── */

  h1, h2, h3, h4 {
    line-height: 1.2;
    color: var(--ink);
    page-break-after: avoid;
    font-weight: 700;
    letter-spacing: -0.015em;
  }

  h1 {
    font-size: 2.2em;
    font-weight: 800;
    margin: 1.6em 0 0.6em;
  }

  h2 {
    font-size: 1.7em;
    font-weight: 700;
    margin: 2em 0 0.75em;
    padding: 0.22em 1em 0.22em 0.8em;
    border-left: 5px solid var(--accent);
    border-bottom: none;
    background: linear-gradient(90deg, rgba(37, 99, 235, 0.07) 0%, transparent 65%);
    border-radius: 0 10px 10px 0;
    text-align: left;
  }

  h3 {
    font-size: 1.32em;
    font-weight: 600;
    margin: 1.7em 0 0.6em;
    color: var(--accent);
    text-align: left;
  }

  h4 {
    font-size: 1.08em;
    font-weight: 600;
    margin: 1.3em 0 0.5em;
  }

  /* ── column widths ── */

  p, li, blockquote { font-size: 1rem; }
  p, ul, ol, blockquote, pre, table, figure { margin: 0 0 1.1em; }

  .deck-body > p,
  .deck-body > ul,
  .deck-body > ol,
  .deck-body > blockquote,
  .deck-body > h4 {
    width: var(--wide-column-width);
    margin-left: auto;
    margin-right: auto;
  }

  .deck-body > h2,
  .deck-body > h3 {
    width: var(--text-column-width);
    margin-left: auto;
    margin-right: auto;
  }

  .deck-body > p,
  .deck-body > li { text-wrap: pretty; }

  .deck-body > p.meta-line {
    width: min(48em, 100%);
    font-size: 0.88rem;
    color: var(--muted);
  }

  /* ── lists ── */

  ul, ol { padding-left: 1.5em; }
  li + li { margin-top: 0.4em; }

  /* ── inline ── */

  a {
    color: var(--accent);
    text-decoration-thickness: 0.08em;
    text-underline-offset: 0.15em;
  }

  strong { color: #0f172a; font-weight: 700; }

  /* ── blockquote ── */

  blockquote {
    margin-left: 0;
    padding: 1.1em 1.3em 1.1em 1.3em;
    border-left: 5px solid var(--accent);
    background: var(--accent-bg);
    border-radius: 0 16px 16px 0;
    color: #1e3a8a;
    font-style: normal;
  }

  /* ── images ── */

  img {
    display: block;
    width: auto;
    max-width: 100%;
    max-height: 78vh;
    margin: 1.2em auto;
    border-radius: 16px;
    box-shadow: 0 12px 40px rgba(30, 41, 59, 0.14);
    page-break-inside: avoid;
    cursor: zoom-in;
  }

  .deck-body > p > img:only-child,
  .deck-body > figure,
  .deck-body > div.sourceCode {
    width: var(--wide-column-width);
    margin-left: auto;
    margin-right: auto;
  }

  .deck-body img[aria-label^="file-"] { margin-bottom: 0.35em; }

  .deck-body figure figcaption,
  .deck-body img[aria-label^="file-"] + figcaption,
  .deck-body figure > p:has(> img[aria-label^="file-"]) + p {
    text-align: center;
    font-size: 0.84rem;
    color: var(--muted);
    letter-spacing: 0.03em;
    margin-top: -0.4em;
  }

  .deck-body > p.image-filename {
    width: var(--wide-column-width);
    margin-top: 0.35em;
    text-align: center;
    font-size: 0.84rem;
    color: var(--muted);
  }

  /* ── table ── */

  table {
    border-collapse: collapse;
    background: var(--paper);
    border-radius: 16px;
    border-style: hidden;
    box-shadow: 0 0 0 1px var(--line);
    overflow: hidden;
  }

  .deck-body > table {
    width: auto;
    max-width: var(--wide-column-width);
    margin-left: auto;
    margin-right: auto;
  }

  th, td {
    padding: 0.78em 1.05em;
    border: 1px solid var(--line);
    vertical-align: top;
  }

  thead tr { background: #1e3a5f; }

  th {
    background: transparent;
    color: #ffffff;
    font-weight: 600;
    font-size: 0.93em;
    letter-spacing: 0.03em;
    border-color: rgba(255, 255, 255, 0.12);
  }

  tbody tr:nth-child(even) td { background: #f0f7ff; }

  tbody tr:hover td {
    background: #dbeafe;
    transition: background 0.12s ease;
  }

  /* ── code ── */

  code, pre, kbd, samp {
    font-family: "SFMono-Regular", "Menlo", "Consolas", monospace;
  }

  code {
    padding: 0.17em 0.38em;
    border-radius: 6px;
    background: #f1f5f9;
    font-size: 0.88em;
    color: #be185d;
  }

  pre {
    padding: 1.1em 1.3em;
    overflow-x: auto;
    border-radius: 16px;
    background: #1e293b;
    color: #e2e8f0;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
    page-break-inside: avoid;
    font-size: 0.88em;
    line-height: 1.65;
  }

  pre code {
    padding: 0;
    background: transparent;
    color: inherit;
    font-size: inherit;
  }

  .deck-body > pre,
  .deck-body > div.sourceCode {
    width: var(--wide-column-width);
    margin-left: auto;
    margin-right: auto;
  }

  /* ── hr ── */

  hr {
    border: 0;
    height: 2px;
    margin: 2.4em 0;
    background: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.35), transparent);
  }

  /* ── lightbox ── */

  .image-lightbox {
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 28px;
    background: rgba(9, 14, 24, 0.90);
    backdrop-filter: blur(10px);
  }

  .image-lightbox.is-open { display: flex; }

  .image-lightbox img {
    width: 94vw;
    height: 92vh;
    max-width: 94vw;
    max-height: 92vh;
    object-fit: contain;
    margin: 0;
    border-radius: 16px;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.45);
    cursor: zoom-out;
    background: #fff;
  }

  .image-lightbox-close {
    position: absolute;
    top: 18px;
    right: 18px;
    appearance: none;
    border: 0;
    border-radius: 999px;
    padding: 11px 15px;
    font: 600 14px/1 -apple-system, "PingFang SC", sans-serif;
    color: #fff;
    background: rgba(255, 255, 255, 0.15);
    cursor: pointer;
  }

  .image-lightbox-close:hover { background: rgba(255, 255, 255, 0.24); }

  /* ── fullscreen ── */

  html.fullscreen-active,
  html.fullscreen-active body,
  html.fullscreen-active .page-shell,
  :fullscreen,
  :fullscreen body,
  :fullscreen .page-shell {
    background: linear-gradient(180deg, #0f172a, #1e293b);
  }

  .fullscreen-active .page-shell {
    padding: 10px 12px 24px;
    width: 100%;
  }

  .fullscreen-active .stage {
    width: min(var(--deck-fullscreen-width), calc(100vw - 24px));
    max-width: calc(100vw - 24px);
  }

  .fullscreen-active .toolbar {
    width: 100%;
    margin-bottom: 12px;
  }

  .fullscreen-active .deck { width: 100%; }

  .fullscreen-active .deck-header { padding: 32px 44px 24px; }

  .fullscreen-active .deck-body { padding: 24px 44px 48px; }

  .fullscreen-active .deck-body img { max-height: 82vh; }

  /* ── responsive ── */

  @media (max-width: 720px) {
    html { font-size: 17px; }
    .page-shell { padding: 18px 10px 38px; }
    .stage { width: min(100%, calc(100vw - 20px)); }
    .toolbar, .deck { width: 100%; }
    .toolbar { top: 8px; margin-bottom: 12px; }
    .toolbar button, .zoom-panel { width: 100%; }
    .deck-header { padding: 28px 22px 20px; }
    .deck-body { padding: 18px 22px 32px; }
    .zoom-panel { justify-content: space-between; }
    img { max-height: 52vh; }
    h2 { padding: 0.2em 0.8em 0.2em 0.6em; }
  }

  /* ── print ── */

  @media print {
    @page { size: A4 portrait; margin: 14mm 16mm; }

    html, body { background: #fff !important; }

    .page-shell { padding: 0 !important; }
    .toolbar { display: none !important; }
    .image-lightbox { display: none !important; }

    .deck {
      width: 100% !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      background: #fff !important;
    }

    .deck-header {
      padding: 0 0 10mm !important;
      border-bottom: 2px solid #1e3a5f !important;
      background: transparent !important;
    }

    .deck-title {
      font-size: 22pt !important;
      color: #1e3a5f !important;
      text-shadow: none !important;
    }

    .deck-body {
      padding: 8mm 0 0 !important;
      font-size: 11pt !important;
      line-height: 1.6 !important;
    }

    h1 { font-size: 20pt !important; }
    h2 {
      font-size: 15pt !important;
      background: none !important;
      border-left-color: #1e3a5f !important;
      padding-left: 0.5em !important;
    }
    h3 { font-size: 13pt !important; color: #1d4ed8 !important; }

    p, li, blockquote, table { font-size: 11pt !important; }

    pre, code {
      white-space: pre-wrap !important;
      word-break: break-word !important;
    }

    img {
      max-width: 100% !important;
      max-height: 180mm !important;
      box-shadow: none !important;
      border: 1px solid #e2e8f0 !important;
    }

    a { color: inherit !important; text-decoration: none !important; }

    thead tr { background: #1e3a5f !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    th { color: #ffffff !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }
</style>
"""


SCRIPT = """
<script>
  (() => {
    const root = document.documentElement;
    const btn = document.getElementById('fullscreen-toggle');
    const zoomSlider = document.getElementById('zoom-slider');
    const zoomValue = document.getElementById('zoom-value');
    const lightbox = document.getElementById('image-lightbox');
    const lightboxImage = document.getElementById('image-lightbox-img');
    const lightboxClose = document.getElementById('image-lightbox-close');
    const baseFontSize = 20;
    const baseDeckWidth = 1100;
    const fullscreenViewportRatio = 0.96;

    function syncButton() {
      const active = !!document.fullscreenElement;
      root.classList.toggle('fullscreen-active', active);
      if (btn) {
        btn.textContent = active ? '退出全屏' : '全屏展示';
      }
    }

    function syncZoom(value) {
      const numericValue = Number(value || 100);
      const scale = numericValue / 100;
      const fontSize = Math.round(baseFontSize * scale * 100) / 100;
      const widthScale = 1 + ((scale - 1) * 0.92);
      const deckWidth = Math.round(baseDeckWidth * widthScale);
      const fullscreenWidth = `${Math.max(70, Math.min(96, fullscreenViewportRatio * widthScale * 100)).toFixed(1)}vw`;

      root.style.setProperty('--zoom-scale', String(scale));
      root.style.setProperty('--font-size', `${fontSize}px`);
      root.style.setProperty('--deck-max-width', `${deckWidth}px`);
      root.style.setProperty('--deck-fullscreen-width', fullscreenWidth);

      if (zoomValue) {
        zoomValue.textContent = `${numericValue}%`;
      }
      if (zoomSlider && Number(zoomSlider.value) !== numericValue) {
        zoomSlider.value = String(numericValue);
      }
      // update slider fill
      if (zoomSlider) {
        const pct = ((numericValue - 75) / (250 - 75) * 100).toFixed(1);
        zoomSlider.style.setProperty('--pct', `${pct}%`);
      }
    }

    async function toggleFullscreen() {
      try {
        if (document.fullscreenElement) {
          await document.exitFullscreen();
        } else {
          await document.documentElement.requestFullscreen();
        }
      } catch (err) {
        console.error(err);
      }
    }

    function closeLightbox() {
      if (!lightbox || !lightboxImage) return;
      lightbox.classList.remove('is-open');
      lightbox.setAttribute('aria-hidden', 'true');
      lightboxImage.removeAttribute('src');
      lightboxImage.removeAttribute('alt');
      document.body.style.overflow = '';
    }

    function openLightbox(img) {
      if (!lightbox || !lightboxImage || !img) return;
      lightboxImage.src = img.currentSrc || img.src;
      lightboxImage.alt = img.alt || img.getAttribute('aria-label') || '';
      lightbox.classList.add('is-open');
      lightbox.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    if (btn) {
      btn.addEventListener('click', toggleFullscreen);
    }

    if (zoomSlider) {
      zoomSlider.addEventListener('input', (event) => {
        syncZoom(event.target.value);
      });
    }

    document.querySelectorAll('.deck-body img').forEach((img) => {
      img.addEventListener('click', () => openLightbox(img));
    });

    if (lightbox) {
      lightbox.addEventListener('click', (event) => {
        if (event.target === lightbox) {
          closeLightbox();
        }
      });
    }

    if (lightboxClose) {
      lightboxClose.addEventListener('click', closeLightbox);
    }

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && lightbox && lightbox.classList.contains('is-open')) {
        closeLightbox();
      }
    });

    document.addEventListener('fullscreenchange', syncButton);
    syncZoom(100);
    syncButton();
  })();
</script>
"""


def extract_between(text: str, start: str, end: str) -> str:
    match = re.search(start + r"(.*?)" + end, text, re.S | re.I)
    return match.group(1).strip() if match else ""


def main() -> int:
    if len(sys.argv) != 4:
      raise SystemExit("Usage: build_pretty_html.py <pandoc_html> <output_html> <title>")

    pandoc_html = Path(sys.argv[1]).read_text(encoding="utf-8")
    output_path = Path(sys.argv[2])
    title = sys.argv[3].strip() or output_path.stem

    head_inner = extract_between(pandoc_html, r"<head[^>]*>", r"</head>")
    body_inner = extract_between(pandoc_html, r"<body[^>]*>", r"</body>")
    body_inner = re.sub(r"<h1[^>]*class=\"title\"[^>]*>.*?</h1>", "", body_inner, flags=re.S | re.I)
    body_inner = re.sub(r"^\s*<header[^>]*id=\"title-block-header\"[^>]*>\s*</header>\s*", "", body_inner, count=1, flags=re.S | re.I)
    body_inner = re.sub(r"^\s*<section[^>]*>\s*<h1[^>]*>.*?</h1>\s*", "", body_inner, count=1, flags=re.S | re.I)
    body_inner = re.sub(r"^\s*<h1[^>]*>.*?</h1>\s*", "", body_inner, count=1, flags=re.S | re.I)
    body_inner = re.sub(r"<p>(原文链接：.*?)</p>", r'<p class="meta-line">\1</p>', body_inner, count=1, flags=re.S)
    body_inner = re.sub(r"<p>(file-\d+)</p>", r'<p class="image-filename">\1</p>', body_inner, flags=re.S)

    extra_styles = "\n".join(re.findall(r"<style.*?>.*?</style>", head_inner, flags=re.S | re.I))

    document = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  {extra_styles}
  {STYLE}
</head>
  <body>
  <div class="page-shell">
    <div class="stage">
      <div class="toolbar">
        <label class="zoom-panel" for="zoom-slider">
          <span>缩放</span>
          <input id="zoom-slider" class="zoom-slider" type="range" min="75" max="250" step="5" value="100" />
          <span id="zoom-value" class="zoom-value">100%</span>
        </label>
        <button id="fullscreen-toggle" type="button">全屏展示</button>
      </div>
      <article class="deck">
        <header class="deck-header">
          <h1 class="deck-title">{html.escape(title)}</h1>
        </header>
        <main class="deck-body">
          {body_inner}
        </main>
      </article>
    </div>
    <div id="image-lightbox" class="image-lightbox" aria-hidden="true">
      <button id="image-lightbox-close" class="image-lightbox-close" type="button">关闭</button>
      <img id="image-lightbox-img" alt="" />
    </div>
  </div>
  {SCRIPT}
</body>
</html>
"""
    output_path.write_text(document, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
