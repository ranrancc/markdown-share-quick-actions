#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import sys
from pathlib import Path


STYLE = """
<style>
  :root {
    --bg: #f4efe5;
    --paper: #fffdf8;
    --ink: #1f2937;
    --muted: #667085;
    --line: #e7dcc9;
    --accent: #b45309;
    --accent-strong: #92400e;
    --shadow: 0 24px 70px rgba(105, 74, 32, 0.14);
    --radius: 24px;
    --base-font-size: 19px;
    --font-size: 19px;
    --deck-max-width: 1100px;
    --deck-fullscreen-width: 94vw;
    --content-width: min(var(--deck-max-width), calc(100vw - 72px));
    --text-column-width: min(44em, 100%);
    --wide-column-width: min(56em, 100%);
    --zoom-scale: 1;
  }

  * { box-sizing: border-box; }

  html {
    font-size: var(--font-size);
    scroll-behavior: smooth;
    background:
      radial-gradient(circle at top left, rgba(245, 158, 11, 0.10), transparent 22rem),
      radial-gradient(circle at bottom right, rgba(180, 83, 9, 0.12), transparent 26rem),
      linear-gradient(180deg, #fbf8f1, #f2eadb 72%, #efe4d2);
  }

  body {
    margin: 0;
    min-height: 100vh;
    color: var(--ink);
    font-family: "Georgia", "Iowan Old Style", "Palatino Linotype", serif;
    line-height: 1.72;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }

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
    padding: 12px 18px;
    font: 600 14px/1.1 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    letter-spacing: 0.01em;
    cursor: pointer;
    color: #fffdf9;
    background: linear-gradient(135deg, var(--accent), var(--accent-strong));
    box-shadow: 0 14px 32px rgba(146, 64, 14, 0.22);
  }

  .toolbar button:hover {
    transform: translateY(-1px);
    filter: brightness(1.02);
  }

  .toolbar button:active {
    transform: translateY(0);
  }

  .zoom-panel {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 999px;
    background: rgba(255, 252, 247, 0.9);
    border: 1px solid rgba(197, 168, 130, 0.3);
    box-shadow: 0 14px 32px rgba(105, 74, 32, 0.12);
    font: 600 13px/1.1 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #7c4a17;
    backdrop-filter: blur(14px);
  }

  .zoom-panel select {
    appearance: none;
    border: 1px solid rgba(197, 168, 130, 0.45);
    background: #fffdf8;
    color: #8a3b12;
    border-radius: 999px;
    padding: 7px 30px 7px 12px;
    font: inherit;
    cursor: pointer;
  }

  .zoom-value {
    min-width: 3.4em;
    text-align: right;
    color: #8a3b12;
  }

  .deck {
    width: 100%;
    margin: 0;
    background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(255,252,247,0.98));
    border: 1px solid rgba(197, 168, 130, 0.28);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: clip;
  }

  .deck-header {
    padding: 34px 46px 16px;
    border-bottom: 1px solid rgba(231, 220, 201, 0.78);
    background:
      linear-gradient(180deg, rgba(255,255,255,0.78), rgba(255,249,240,0.92)),
      radial-gradient(circle at top right, rgba(245, 158, 11, 0.10), transparent 18rem);
  }

  .deck-title {
    margin: 0;
    font-size: clamp(1.45em, 2.7vw, 2.15em);
    line-height: 1.12;
    color: #1e293b;
    text-align: center;
    max-width: 30em;
    margin-left: auto;
    margin-right: auto;
  }

  .deck-body {
    padding: 24px 46px 56px;
  }

  .deck-body > *:first-child { margin-top: 0; }
  .deck-body > *:last-child { margin-bottom: 0; }

  .deck-body > h2:first-child,
  .deck-body > h3:first-child,
  .deck-body > p:first-child {
    margin-top: 0;
  }

  h1, h2, h3, h4 {
    line-height: 1.18;
    letter-spacing: -0.015em;
    color: #162033;
    page-break-after: avoid;
  }

  h1 { font-size: 2.2em; margin: 1.5em 0 0.55em; }
  h2 {
    font-size: 1.65em;
    margin: 1.6em 0 0.68em;
    padding-bottom: 0.25em;
    border-bottom: 1px solid rgba(231, 220, 201, 0.85);
    text-align: left;
  }
  h3 {
    font-size: 1.34em;
    margin: 1.35em 0 0.55em;
    text-align: left;
  }
  h4 { font-size: 1.08em; margin: 1.25em 0 0.45em; }

  p, li, blockquote { font-size: 1rem; }
  p, ul, ol, blockquote, pre, table, figure { margin: 0 0 1em; }

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
    padding-left: 1.2em;
    padding-right: 1.2em;
  }

  .deck-body > p,
  .deck-body > li {
    text-wrap: pretty;
  }

  .deck-body > p.meta-line {
    width: min(48em, 100%);
    font-size: 0.9rem;
    color: var(--muted);
  }

  .deck-body > p.image-filename {
    width: var(--wide-column-width);
    margin-top: 0.35em;
    text-align: center;
    font-size: 0.88rem;
    color: rgba(92, 100, 114, 0.62);
    letter-spacing: 0.01em;
  }

  .deck-body img[aria-label^="file-"] {
    margin-bottom: 0.35em;
  }

  .deck-body img[aria-label^="file-"] + figcaption,
  .deck-body figure > p:has(> img[aria-label^="file-"]) + p {
    text-align: center;
    font-size: 0.88rem;
    color: rgba(92, 100, 114, 0.62);
  }

  ul, ol { padding-left: 1.35em; }
  li + li { margin-top: 0.32em; }

  a {
    color: #8a3b12;
    text-decoration-thickness: 0.08em;
    text-underline-offset: 0.14em;
  }

  strong { color: #111827; }

  blockquote {
    margin-left: 0;
    padding: 1em 1.1em 1em 1.2em;
    border-left: 4px solid rgba(180, 83, 9, 0.45);
    background: rgba(251, 243, 228, 0.9);
    border-radius: 0 16px 16px 0;
    color: #4b5563;
  }

  img {
    display: block;
    width: auto;
    max-width: 100%;
    max-height: 78vh;
    margin: 1.1em auto;
    border-radius: 18px;
    box-shadow: 0 16px 40px rgba(89, 66, 33, 0.16);
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

  table {
    width: 100%;
    border-collapse: collapse;
    background: rgba(255, 252, 246, 0.9);
    overflow: hidden;
    border-radius: 16px;
    border-style: hidden;
    box-shadow: 0 0 0 1px rgba(220, 204, 178, 0.88);
  }

  th, td {
    padding: 0.72em 0.82em;
    border: 1px solid rgba(220, 204, 178, 0.88);
    vertical-align: top;
  }

  th {
    background: rgba(247, 232, 208, 0.92);
    text-align: left;
  }

  code, pre, kbd, samp {
    font-family: "SFMono-Regular", "Menlo", "Consolas", monospace;
  }

  code {
    padding: 0.16em 0.32em;
    border-radius: 8px;
    background: rgba(245, 238, 223, 0.94);
    font-size: 0.92em;
  }

  pre {
    padding: 1em 1.1em;
    overflow-x: auto;
    border-radius: 18px;
    background: #1f2937;
    color: #f9fafb;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
    page-break-inside: avoid;
  }

  .deck-body > pre,
  .deck-body > div.sourceCode {
    width: var(--wide-column-width);
  }

  .deck-body > table {
    width: var(--wide-column-width);
  }

  .image-lightbox {
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 28px;
    background: rgba(9, 14, 24, 0.88);
    backdrop-filter: blur(10px);
  }

  .image-lightbox.is-open {
    display: flex;
  }

  .image-lightbox img {
    width: 94vw;
    height: 92vh;
    max-width: 94vw;
    max-height: 92vh;
    object-fit: contain;
    margin: 0;
    border-radius: 16px;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.42);
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
    font: 600 14px/1 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #fff;
    background: rgba(255, 255, 255, 0.14);
    cursor: pointer;
  }

  .image-lightbox-close:hover {
    background: rgba(255, 255, 255, 0.22);
  }

  pre code {
    padding: 0;
    background: transparent;
    color: inherit;
  }

  hr {
    border: 0;
    height: 1px;
    margin: 2.1em 0;
    background: linear-gradient(90deg, transparent, rgba(180, 83, 9, 0.34), transparent);
  }

  html.fullscreen-active,
  html.fullscreen-active body,
  html.fullscreen-active .page-shell,
  :fullscreen,
  :fullscreen body,
  :fullscreen .page-shell {
    background:
      radial-gradient(circle at top left, rgba(245, 158, 11, 0.08), transparent 20rem),
      linear-gradient(180deg, #171f2d, #0f1724);
  }

  .fullscreen-active .page-shell {
    padding: 10px;
    width: 100%;
  }

  .fullscreen-active .stage {
    width: min(var(--deck-fullscreen-width), calc(100vw - 24px));
  }

  .fullscreen-active .toolbar {
    width: 100%;
    margin-bottom: 12px;
  }

  .fullscreen-active .deck {
    width: 100%;
  }

  .fullscreen-active .deck-header {
    padding: 28px 40px 12px;
  }

  .fullscreen-active .deck-body {
    padding: 20px 40px 44px;
  }

  .fullscreen-active .deck-body img {
    max-height: 82vh;
  }

  @media (max-width: 720px) {
    html { font-size: 17px; }
    .page-shell { padding: 18px 10px 38px; }
    .stage { width: min(100%, calc(100vw - 20px)); }
    .toolbar, .deck { width: 100%; }
    .toolbar { top: 8px; margin-bottom: 12px; }
    .toolbar button, .zoom-panel { width: 100%; }
    .deck-header { padding: 24px 20px 10px; }
    .deck-body { padding: 16px 20px 28px; }
    .zoom-panel { justify-content: space-between; }
    img { max-height: 52vh; }
  }

  @media print {
    @page {
      size: A4 portrait;
      margin: 14mm 16mm;
    }

    html, body {
      background: #fff !important;
    }

    .page-shell {
      padding: 0 !important;
    }

    .toolbar {
      display: none !important;
    }

    .image-lightbox {
      display: none !important;
    }

    .deck {
      width: 100% !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
      background: #fff !important;
    }

    .deck-header {
      padding: 0 0 10mm !important;
      border-bottom: 1px solid #c8c8c8 !important;
      background: transparent !important;
    }

    .deck-body {
      padding: 8mm 0 0 !important;
      font-size: 11pt !important;
      line-height: 1.6 !important;
    }

    .deck-title {
      font-size: 24pt !important;
    }

    h1 { font-size: 20pt !important; }
    h2 { font-size: 16pt !important; }
    h3 { font-size: 13pt !important; }

    p, li, blockquote, table {
      font-size: 11pt !important;
    }

    pre, code {
      white-space: pre-wrap !important;
      word-break: break-word !important;
    }

    img {
      max-width: 100% !important;
      max-height: 180mm !important;
      box-shadow: none !important;
      border: 1px solid #e6e6e6 !important;
    }

    a {
      color: inherit !important;
      text-decoration: none !important;
    }
  }
</style>
"""


SCRIPT = """
<script>
  (() => {
    const root = document.documentElement;
    const btn = document.getElementById('fullscreen-toggle');
    const zoomSelect = document.getElementById('zoom-select');
    const zoomValue = document.getElementById('zoom-value');
    const lightbox = document.getElementById('image-lightbox');
    const lightboxImage = document.getElementById('image-lightbox-img');
    const lightboxClose = document.getElementById('image-lightbox-close');
    const zoomPresets = [90, 100, 110, 125, 150, 175, 200];
    const baseFontSize = 19;
    const baseDeckWidth = 1100;
    const fullscreenViewportRatio = 0.94;

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
      const fullscreenWidth = `${Math.max(70, Math.min(94, fullscreenViewportRatio * widthScale * 100)).toFixed(1)}vw`;

      root.style.setProperty('--zoom-scale', String(scale));
      root.style.setProperty('--font-size', `${fontSize}px`);
      root.style.setProperty('--deck-max-width', `${deckWidth}px`);
      root.style.setProperty('--deck-fullscreen-width', fullscreenWidth);

      if (zoomValue) {
        zoomValue.textContent = `${numericValue}%`;
      }
      if (zoomSelect && String(zoomSelect.value) != String(numericValue)) {
        zoomSelect.value = String(numericValue);
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

    if (zoomSelect) {
      zoomSelect.addEventListener('change', (event) => {
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
        <label class="zoom-panel" for="zoom-select">
          <span>缩放</span>
          <select id="zoom-select">
            <option value="90">90%</option>
            <option value="100" selected>100%</option>
            <option value="110">110%</option>
            <option value="125">125%</option>
            <option value="150">150%</option>
            <option value="175">175%</option>
            <option value="200">200%</option>
          </select>
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
