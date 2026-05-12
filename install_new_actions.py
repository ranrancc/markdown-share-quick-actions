#!/usr/bin/env python3

from __future__ import annotations

import plistlib
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def runner_snippet(root: Path) -> str:
    return f"""
RUNNER="{root / ".venv" / "bin" / "python"}"
if [[ ! -x "$RUNNER" ]]; then
  RUNNER="$(command -v python3 || true)"
fi
if [[ -z "$RUNNER" ]]; then
  /usr/bin/osascript -e 'display alert "Markdown Share" message "没有找到 python3。" as critical buttons {{"好"}} default button "好"' >/dev/null 2>&1 || true
  exit 1
fi
""".strip()


NEW_ACTIONS = [
    (
        "MD 转 HTML（选择主题）.workflow",
        "MD 转 HTML（选择主题）",
        ROOT / "md-to-html-quick-action" / "md-to-html-icon.icns",
        "md-to-html-icon",
        lambda root: f"""
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
{runner_snippet(root)}
theme="$(/usr/bin/osascript -e 'choose from list {{"经典样式", "文章样式", "报告样式", "阅读样式", "交互样式"}} with title "MD 转 HTML" with prompt "选择 HTML 主题：" default items {{"经典样式"}} OK button name "转换" cancel button name "取消"' 2>/dev/null || true)"
if [[ -z "$theme" || "$theme" == "false" ]]; then
  exit 0
fi
case "$theme" in
  "经典样式") theme="classic" ;;
  "文章样式") theme="article" ;;
  "报告样式") theme="report" ;;
  "阅读样式") theme="reading" ;;
  "交互样式") theme="interactive" ;;
  *) exit 0 ;;
esac
output="$("$RUNNER" "{root / "md_share.py"}" html --theme "$theme" "$@" 2>&1)"
exit_code="$?"
if [[ "$exit_code" == "0" ]]; then
  count="$(printf '%s\\n' "$output" | sed '/^$/d' | wc -l | tr -d ' ')"
  /usr/bin/osascript -e "display notification \\"已生成 $count 个 HTML 文件\\" with title \\"MD 转 HTML\\"" >/dev/null 2>&1 || true
else
  /usr/bin/osascript -e "display alert \\"MD 转 HTML 失败\\" message \\"${{output//\\"/\\\\\\"}}\\" as critical buttons {{\\"好\\"}} default button \\"好\\"" >/dev/null 2>&1 || true
  exit "$exit_code"
fi
""".strip(),
    ),
    (
        "多种文档转 MD.workflow",
        "多种文档转 MD",
        ROOT / "md-to-word-quick-action" / "md-to-word-icon.icns",
        "md-to-word-icon",
        lambda root: f"""
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
{runner_snippet(root)}
output="$("$RUNNER" "{root / "md_share.py"}" to-md "$@" 2>&1)"
exit_code="$?"
if [[ "$exit_code" == "0" ]]; then
  count="$(printf '%s\\n' "$output" | sed '/^$/d' | wc -l | tr -d ' ')"
  /usr/bin/osascript -e "display notification \\"已生成 $count 个 Markdown 文件\\" with title \\"多种文档转 MD\\"" >/dev/null 2>&1 || true
else
  /usr/bin/osascript -e "display alert \\"多种文档转 MD 失败\\" message \\"${{output//\\"/\\\\\\"}}\\" as critical buttons {{\\"好\\"}} default button \\"好\\"" >/dev/null 2>&1 || true
  exit "$exit_code"
fi
""".strip(),
    ),
    (
        "HTML 转 MD.workflow",
        "HTML 转 MD",
        ROOT / "md-to-html-quick-action" / "md-to-html-icon.icns",
        "md-to-html-icon",
        lambda root: f"""
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
{runner_snippet(root)}
output="$("$RUNNER" "{root / "md_share.py"}" html-to-md "$@" 2>&1)"
exit_code="$?"
if [[ "$exit_code" == "0" ]]; then
  count="$(printf '%s\\n' "$output" | sed '/^$/d' | wc -l | tr -d ' ')"
  /usr/bin/osascript -e "display notification \\"已生成 $count 个 Markdown 文件\\" with title \\"HTML 转 MD\\"" >/dev/null 2>&1 || true
else
  /usr/bin/osascript -e "display alert \\"HTML 转 MD 失败\\" message \\"${{output//\\"/\\\\\\"}}\\" as critical buttons {{\\"好\\"}} default button \\"好\\"" >/dev/null 2>&1 || true
  exit "$exit_code"
fi
""".strip(),
    ),
]


def build_info_plist(menu_title: str, icon_basename: str) -> dict:
    return {
        "CFBundleIconFile": f"{icon_basename}.icns",
        "NSServices": [
            {
                "NSBackgroundColorName": "background",
                "NSIconName": icon_basename,
                "NSMenuItem": {"default": menu_title},
                "NSMessage": "runWorkflowAsService",
                "NSRequiredContext": {"NSApplicationIdentifier": "com.apple.finder"},
                "NSSendFileTypes": ["public.item"],
            }
        ],
    }


def build_document_wflow(command: str) -> dict:
    return {
        "actions": [
            {
                "action": {
                    "ActionBundlePath": "/System/Library/Automator/Run Shell Script.action",
                    "ActionName": "Run Shell Script",
                    "ActionParameters": {
                        "CheckedForUserDefaultShell": True,
                        "COMMAND_STRING": command,
                        "inputMethod": 1,
                        "shell": "/bin/zsh",
                        "source": "",
                    },
                    "AMAccepts": {"Container": "List", "Optional": True, "Types": ["com.apple.cocoa.string"]},
                    "AMActionVersion": "2.0.3",
                    "AMApplication": ["Automator"],
                    "AMParameterProperties": {
                        "CheckedForUserDefaultShell": {},
                        "COMMAND_STRING": {},
                        "inputMethod": {},
                        "shell": {},
                        "source": {},
                    },
                    "AMProvides": {"Container": "List", "Types": ["com.apple.cocoa.string"]},
                    "arguments": {
                        "0": {"default value": 0, "name": "inputMethod", "required": "0", "type": "0", "uuid": "0"},
                        "1": {"default value": False, "name": "CheckedForUserDefaultShell", "required": "0", "type": "0", "uuid": "1"},
                        "2": {"default value": "", "name": "source", "required": "0", "type": "0", "uuid": "2"},
                        "3": {"default value": "", "name": "COMMAND_STRING", "required": "0", "type": "0", "uuid": "3"},
                        "4": {"default value": "/bin/sh", "name": "shell", "required": "0", "type": "0", "uuid": "4"},
                    },
                    "BundleIdentifier": "com.apple.RunShellScript",
                    "CanShowSelectedItemsWhenRun": False,
                    "CanShowWhenRun": True,
                    "Category": ["AMCategoryUtilities"],
                    "CFBundleVersion": "2.0.3",
                    "Class Name": "RunShellScriptAction",
                    "InputUUID": "3E75B8BF-5C82-4EA4-B46F-0BE7B2D290F1",
                    "isViewVisible": 1,
                    "Keywords": ["Markdown", "HTML", "Export"],
                    "location": "309.000000:305.000000",
                    "nibPath": "/System/Library/Automator/Run Shell Script.action/Contents/Resources/Base.lproj/main.nib",
                    "OutputUUID": "7D67603C-99B8-4D11-8B81-49F65373450E",
                    "UnlocalizedApplications": ["Automator"],
                    "UUID": "144DCB2D-91EA-463D-9E26-EBD33CF30BA6",
                },
                "isViewVisible": 1,
            }
        ],
        "AMApplicationBuild": "512",
        "AMApplicationVersion": "2.10",
        "AMDocumentVersion": "2",
        "connectors": {},
        "workflowMetaData": {
            "applicationBundleID": "com.apple.finder",
            "applicationBundleIDsByPath": {"/System/Library/CoreServices/Finder.app": "com.apple.finder"},
            "applicationPath": "/System/Library/CoreServices/Finder.app",
            "applicationPaths": ["/System/Library/CoreServices/Finder.app"],
            "inputTypeIdentifier": "com.apple.Automator.fileSystemObject",
            "outputTypeIdentifier": "com.apple.Automator.nothing",
            "presentationMode": 15,
            "processesInput": False,
            "serviceApplicationBundleID": "com.apple.finder",
            "serviceApplicationPath": "/System/Library/CoreServices/Finder.app",
            "serviceInputTypeIdentifier": "com.apple.Automator.fileSystemObject",
            "serviceOutputTypeIdentifier": "com.apple.Automator.nothing",
            "serviceProcessesInput": False,
            "systemImageName": "doc.text",
            "useAutomaticInputType": False,
            "workflowTypeIdentifier": "com.apple.Automator.servicesMenu",
        },
    }


def main() -> int:
    if sys.platform != "darwin":
        print("This installer creates macOS Finder Quick Actions and requires macOS.", file=sys.stderr)
        return 2
    runtime_root = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else ROOT

    services_dir = Path.home() / "Library" / "Services"
    services_dir.mkdir(parents=True, exist_ok=True)

    installed: list[Path] = []
    for workflow_name, menu_title, icon_path, icon_basename, command_builder in NEW_ACTIONS:
        icon_path = runtime_root / icon_path.relative_to(ROOT)
        command = command_builder(runtime_root)
        workflow_dir = services_dir / workflow_name
        contents_dir = workflow_dir / "Contents"
        resources_dir = contents_dir / "Resources"
        if workflow_dir.exists():
            shutil.rmtree(workflow_dir)
        contents_dir.mkdir(parents=True, exist_ok=True)
        resources_dir.mkdir(parents=True, exist_ok=True)
        with (contents_dir / "info.plist").open("wb") as f:
            plistlib.dump(build_info_plist(menu_title, icon_basename), f, fmt=plistlib.FMT_XML)
        with (contents_dir / "document.wflow").open("wb") as f:
            plistlib.dump(build_document_wflow(command), f, fmt=plistlib.FMT_XML)
        if icon_path.exists():
            shutil.copy2(icon_path, resources_dir / icon_path.name)
        installed.append(workflow_dir)

    for path in installed:
        print(path)
    print("Installed additional Finder Quick Actions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
