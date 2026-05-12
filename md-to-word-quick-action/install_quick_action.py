#!/usr/bin/env python3

from __future__ import annotations

import plistlib
import shutil
import subprocess
import sys
from pathlib import Path

WORKFLOW_NAME = "Markdown 转 Word（含图表）.workflow"
MENU_TITLE = "Markdown 转 Word（含图表）"
ICON_BASENAME = "md-to-word-icon"


def build_info_plist() -> dict:
    return {
        "CFBundleIconFile": f"{ICON_BASENAME}.icns",
        "NSServices": [
            {
                "NSBackgroundColorName": "background",
                "NSIconName": ICON_BASENAME,
                "NSMenuItem": {"default": MENU_TITLE},
                "NSMessage": "runWorkflowAsService",
                "NSRequiredContext": {"NSApplicationIdentifier": "com.apple.finder"},
                "NSSendFileTypes": ["public.item"],
            }
        ]
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
                    "AMAccepts": {
                        "Container": "List",
                        "Optional": True,
                        "Types": ["com.apple.cocoa.string"],
                    },
                    "AMActionVersion": "2.0.3",
                    "AMApplication": ["Automator"],
                    "AMParameterProperties": {
                        "CheckedForUserDefaultShell": {},
                        "COMMAND_STRING": {},
                        "inputMethod": {},
                        "shell": {},
                        "source": {},
                    },
                    "AMProvides": {
                        "Container": "List",
                        "Types": ["com.apple.cocoa.string"],
                    },
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
                    "InputUUID": "77E8E2F0-A5A1-4F68-BBC0-A5502D40AD6B",
                    "isViewVisible": 1,
                    "Keywords": ["Shell", "Script", "Run", "Command"],
                    "location": "309.000000:305.000000",
                    "nibPath": "/System/Library/Automator/Run Shell Script.action/Contents/Resources/Base.lproj/main.nib",
                    "OutputUUID": "2D69CB2F-C459-49E0-BFF4-292B772E6BE6",
                    "UnlocalizedApplications": ["Automator"],
                    "UUID": "E5B34E55-6C4D-4D6B-A1CB-269C9B2FDF86",
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
            "systemImageName": ICON_BASENAME,
            "useAutomaticInputType": False,
            "workflowTypeIdentifier": "com.apple.Automator.servicesMenu",
        },
    }


def main() -> int:
    tool_dir = Path(__file__).resolve().parent
    services_dir = Path.home() / "Library" / "Services"
    workflow_dir = services_dir / WORKFLOW_NAME
    contents_dir = workflow_dir / "Contents"
    resources_dir = contents_dir / "Resources"

    converter_path = tool_dir / "convert_md_to_docx.sh"
    cli_path = tool_dir.parent / "md_share.py"
    template_path = tool_dir / "reference.docx"
    icon_script_path = tool_dir / "generate_workflow_icon.py"
    icon_path = tool_dir / f"{ICON_BASENAME}.icns"

    if not converter_path.exists():
        raise SystemExit(f"Missing converter script: {converter_path}")
    if not cli_path.exists():
        raise SystemExit(f"Missing shared CLI: {cli_path}")
    if not template_path.exists():
        raise SystemExit(f"Missing reference template: {template_path}")
    if not icon_script_path.exists():
        raise SystemExit(f"Missing icon generator script: {icon_script_path}")

    if not icon_path.exists():
        subprocess.run([sys.executable, str(icon_script_path)], check=True)
    if not icon_path.exists():
        raise SystemExit(f"Missing workflow icon: {icon_path}")

    services_dir.mkdir(parents=True, exist_ok=True)
    if workflow_dir.exists():
        shutil.rmtree(workflow_dir)
    contents_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)

    runner = tool_dir.parent / ".venv" / "bin" / "python"
    command = (
        'export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"\n'
        f'RUNNER="{runner}"\n'
        'if [[ ! -x "$RUNNER" ]]; then RUNNER="$(command -v python3 || true)"; fi\n'
        'if [[ -z "$RUNNER" ]]; then exit 1; fi\n'
        f'exec "$RUNNER" "{cli_path}" word "$@"'
    )

    with (contents_dir / "info.plist").open("wb") as f:
        plistlib.dump(build_info_plist(), f, fmt=plistlib.FMT_XML)

    with (contents_dir / "document.wflow").open("wb") as f:
        plistlib.dump(build_document_wflow(command), f, fmt=plistlib.FMT_XML)

    shutil.copy2(icon_path, resources_dir / icon_path.name)

    print(workflow_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
