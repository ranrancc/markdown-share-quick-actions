#!/bin/zsh

# Automator strips PATH; restore Homebrew and system tool paths explicitly
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

set -u

SCRIPT_DIR="${0:A:h}"
DEFAULT_PANDOC="/opt/homebrew/bin/pandoc"
PANDOC_BIN="${PANDOC_BIN:-$DEFAULT_PANDOC}"
TEMPLATE_PATH="${MD_TO_WORD_TEMPLATE:-$SCRIPT_DIR/reference.docx}"
MERMAID_SCRIPT="$SCRIPT_DIR/../mermaid-prerender.py"
TMP_DIRS=()

show_alert() {
  local message="$1"
  /usr/bin/osascript -e "display alert \"Markdown 转 Word\" message \"${message//\"/\\\"}\" as critical buttons {\"好\"} default button \"好\"" >/dev/null 2>&1 || true
}

show_notification() {
  local title="$1"
  local message="$2"
  /usr/bin/osascript -e "display notification \"${message//\"/\\\"}\" with title \"${title//\"/\\\"}\"" >/dev/null 2>&1 || true
}

copy_to_clipboard() {
  local content="$1"
  printf '%s' "$content" | /usr/bin/pbcopy 2>/dev/null || true
}

cleanup() {
  local dir
  for dir in "${TMP_DIRS[@]}"; do
    [[ -n "$dir" && -d "$dir" ]] && rm -rf "$dir"
  done
}

trap cleanup EXIT

preprocess_markdown() {
  local input_path="$1"
  local temp_dir
  temp_dir="$(mktemp -d "${TMPDIR:-/tmp}/md-to-word.XXXXXX")"
  TMP_DIRS+=("$temp_dir")

  python3 - "$input_path" "$temp_dir/prepared.md" <<'PY'
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
text = src.read_text(encoding="utf-8")

frontmatter = re.compile(r'\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|$)', re.DOTALL)
text = frontmatter.sub("", text, count=1)

pattern = re.compile(r'!\[\[([^\]]+)\]\]')

def replace(match):
    inner = match.group(1).strip()
    if not inner:
        return match.group(0)
    parts = [part.strip() for part in inner.split("|") if part.strip()]
    target = parts[0]
    alt = ""
    if len(parts) >= 2:
        if not parts[1].isdigit():
            alt = parts[1]
    if not alt:
        alt = Path(target).stem
    return f'![{alt}]({target})'

dst.write_text(pattern.sub(replace, text), encoding="utf-8")
PY

  printf '%s\n' "$temp_dir/prepared.md"
}

preprocess_mermaid() {
  local input_path="$1"
  if ! grep -q '```mermaid' "$input_path" 2>/dev/null; then
    printf '%s\n' "$input_path"
    return
  fi
  if [[ ! -f "$MERMAID_SCRIPT" ]]; then
    printf '%s\n' "$input_path"
    return
  fi
  local temp_dir
  temp_dir="$(mktemp -d "${TMPDIR:-/tmp}/mermaid-render.XXXXXX")"
  TMP_DIRS+=("$temp_dir")
  local output_md="$temp_dir/mermaid-rendered.md"
  if python3 "$MERMAID_SCRIPT" "$input_path" "$output_md" "$temp_dir/assets" "png" >/dev/null 2>&1 \
      && [[ -f "$output_md" ]]; then
    printf '%s\n' "$output_md"
  else
    printf '%s\n' "$input_path"
  fi
}

detect_input_format() {
  local input_path="$1"

  python3 - "$input_path" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="ignore")

if text.startswith("---\n") or text.startswith("---\r\n"):
    print("markdown")
else:
    # Keep Pandoc's broader markdown support, but disable YAML metadata parsing
    # for regular notes so thematic breaks like `---` are not misread as front matter.
    print("markdown-yaml_metadata_block")
PY
}

if [[ ! -x "$PANDOC_BIN" ]]; then
  PANDOC_BIN="$(command -v pandoc 2>/dev/null || true)"
fi

if [[ -z "$PANDOC_BIN" || ! -x "$PANDOC_BIN" ]]; then
  show_alert "没有找到 pandoc。请先安装 pandoc，然后再试一次。"
  exit 1
fi

if [[ ! -f "$TEMPLATE_PATH" ]]; then
  show_alert "没有找到 reference.docx 模板：$TEMPLATE_PATH"
  exit 1
fi

if [[ "$#" -eq 0 ]]; then
  show_alert "没有收到任何 Markdown 文件。请在 Finder 中选择一个或多个 .md 文件后再运行。"
  exit 1
fi

typeset -i success_count=0
typeset -i skip_count=0
typeset -i failure_count=0
typeset -a failures=()

for input_path in "$@"; do
  if [[ ! -f "$input_path" ]]; then
    skip_count+=1
    continue
  fi

  case "${input_path:e:l}" in
    md|markdown) ;;
    *)
      skip_count+=1
      continue
      ;;
  esac

  output_path="${input_path:r}.docx"
  input_dir="${input_path:h}"
  prepared_path="$(preprocess_markdown "$input_path")"
  prepared_path="$(preprocess_mermaid "$prepared_path")"
  input_format="$(detect_input_format "$prepared_path")"
  error_log="$(mktemp "${TMPDIR:-/tmp}/md-to-word-error.XXXXXX")"
  TMP_DIRS+=("$error_log")

  if "$PANDOC_BIN" "$prepared_path" -f "$input_format" -o "$output_path" --reference-doc="$TEMPLATE_PATH" --resource-path="$input_dir" > /dev/null 2>"$error_log"; then
    python3 - "$output_path" <<'PY' 2>/dev/null || true
import sys
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document(sys.argv[1])
for table in doc.tables:
    tblPr = table._tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        table._tbl.insert(0, tblPr)
    jc = tblPr.find(qn('w:jc'))
    if jc is None:
        jc = OxmlElement('w:jc')
        tblPr.append(jc)
    jc.set(qn('w:val'), 'center')
for para in doc.paragraphs:
    if para.style.name == 'Image Caption':
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.save(sys.argv[1])
PY
    success_count+=1
  else
    failure_count+=1
    error_summary="$(sed -n '1,8p' "$error_log")"
    if [[ -n "$error_summary" ]]; then
      failures+=("生成失败：$output_path\n$error_summary")
    else
      failures+=("生成失败：$output_path")
    fi
  fi
done

if (( failure_count > 0 )); then
  summary="成功 ${success_count} 个，失败 ${failure_count} 个"
  if (( skip_count > 0 )); then
    summary="${summary}，跳过 ${skip_count} 个"
  fi
  details="${failures[1]}"
  if (( ${#failures[@]} > 1 )); then
    details="${details}\n另外还有 $(( ${#failures[@]} - 1 )) 个失败文件。"
  fi
  clipboard_text="Markdown 转 Word 失败\n${summary}\n\n${details}"
  copy_to_clipboard "$clipboard_text"
  show_alert "${summary}\n\n${details}\n\n错误详情已复制到剪贴板。"
  exit 1
fi

if (( success_count == 0 )); then
  show_alert "没有可处理的 Markdown 文件。这个动作只对 .md 或 .markdown 文件生效。"
  exit 1
fi

summary="已生成 ${success_count} 个 Word 文件"
if (( skip_count > 0 )); then
  summary="${summary}，跳过 ${skip_count} 个非 Markdown 项"
fi

show_notification "Markdown 转 Word" "$summary"
exit 0
