#!/bin/zsh

set -u

SCRIPT_DIR="${0:A:h}"
DEFAULT_PANDOC="/opt/homebrew/bin/pandoc"
PANDOC_BIN="${PANDOC_BIN:-$DEFAULT_PANDOC}"
TEMPLATE_PATH="${MD_TO_WORD_TEMPLATE:-$SCRIPT_DIR/reference.docx}"
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

  if "$PANDOC_BIN" "$prepared_path" -o "$output_path" --reference-doc="$TEMPLATE_PATH" --resource-path="$input_dir" >/dev/null 2>&1; then
    success_count+=1
  else
    failure_count+=1
    failures+=("无法写入输出文件：$output_path")
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
  show_alert "${summary}\n\n${details}"
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
