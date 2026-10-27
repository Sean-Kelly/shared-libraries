#!/usr/bin/env python3
# write-attribution: written_at=2026-08-11 18:34 CDT; written_by=codex; scope=script-add
"""
Codex Stop hook wrapper for kos-codex-turn-status.

Stop hooks must emit JSON on stdout. This wrapper converts the human-readable
status line into structured hook output so Codex can surface it without treating
plain text as an invalid Stop-hook result.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


STATUS_SCRIPT = Path.home() / ".codex" / "footer" / "turn-status.py"
KILL_SWITCH = Path.home() / ".config/kos/codex-turn-status-hook.off"


def hook_output(line: str) -> dict[str, object]:
    # Codex 0.142.5 rejects hookSpecificOutput on Stop even though newer docs
    # describe hook-specific additionalContext for more events.
    return {
        "continue": True,
        "systemMessage": line,
    }


def main() -> int:
    payload = sys.stdin.read()
    if KILL_SWITCH.exists():
        print(json.dumps({"continue": True}))
        return 0

    try:
        result = subprocess.run(
            [str(STATUS_SCRIPT)],
            input=payload,
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
    except Exception as exc:
        print(json.dumps(hook_output(f"codex status unavailable: {exc}")))
        return 0

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        print(json.dumps(hook_output(f"codex status unavailable: {detail}")))
        return 0

    line = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else "codex status unavailable: empty output"
    print(json.dumps(hook_output(line)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
