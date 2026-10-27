#!/usr/bin/env python3
# write-attribution: written_at=2026-08-11 18:24 CDT; written_by=codex; scope=script-add
"""
Summarize Codex turn, context, and session-clock state from a Codex JSONL transcript.

The script is intentionally read-only. It can be run by hand, from a Codex hook that
passes transcript_path on stdin, or by another KOS status surface.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


LOCAL_TZ = ZoneInfo(os.environ.get("KOS_LOCAL_TZ", "America/Chicago"))
DEFAULT_SESSIONS_DIR = Path("~/.codex/sessions").expanduser()


@dataclass
class TokenStats:
    context_used: int | None = None
    context_window: int | None = None
    context_percent: int | None = None
    last_input_tokens: int | None = None
    last_cached_input_tokens: int | None = None
    last_output_tokens: int | None = None
    last_reasoning_output_tokens: int | None = None
    last_total_tokens: int | None = None
    cumulative_total_tokens: int | None = None
    rate_limit_used_percent: float | None = None
    rate_limit_resets_at: int | None = None


@dataclass
class Status:
    transcript_path: str | None
    session_id: str | None
    cwd: str | None
    model: str | None
    turn_count: int
    last_user_turn_at: str | None
    last_user_turn_local: str | None
    previous_user_turn_at: str | None
    gap_seconds: int | None
    gap: str | None
    session_started_at: str | None
    session_started_local: str | None
    elapsed_seconds: int | None
    elapsed: str | None
    latest_event_at: str | None
    token_stats: TokenStats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report Codex turn count, inter-turn gap, and token/context usage."
    )
    parser.add_argument("path", nargs="?", help="Codex JSONL transcript path")
    parser.add_argument("--transcript", help="Codex JSONL transcript path")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--latest",
        action="store_true",
        help="ignore stdin and explicit paths; use the newest Codex transcript",
    )
    parser.add_argument(
        "--no-stdin",
        action="store_true",
        help="do not read hook JSON from stdin",
    )
    return parser.parse_args()


def read_stdin_json(enabled: bool) -> dict[str, Any]:
    if not enabled or sys.stdin.isatty():
        return {}
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def latest_transcript() -> Path | None:
    sessions_dir = Path(os.environ.get("CODEX_SESSIONS_DIR", DEFAULT_SESSIONS_DIR))
    if not sessions_dir.exists():
        return None
    newest: tuple[float, Path] | None = None
    for path in sessions_dir.glob("*/*/*/*.jsonl"):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if newest is None or mtime > newest[0]:
            newest = (mtime, path)
    return newest[1] if newest else None


def choose_transcript(args: argparse.Namespace, hook: dict[str, Any]) -> Path:
    raw = None
    if not args.latest:
        raw = args.transcript or args.path or hook.get("transcript_path")
    if raw:
        return Path(str(raw)).expanduser()
    found = latest_transcript()
    if found is None:
        raise SystemExit("kos-codex-turn-status: no Codex transcript found")
    return found


def parse_ts(raw: Any) -> datetime | None:
    if not isinstance(raw, str) or not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def iso_z(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def local_stamp(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(LOCAL_TZ).strftime("%Y-%m-%d--%H%M %Z")


def compact_number(value: int | float | None) -> str:
    if value is None:
        return "?"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return str(int(value))


def duration(seconds: int | None) -> str | None:
    if seconds is None:
        return None
    if seconds < 0:
        seconds = 0
    if seconds < 60:
        return "<1m"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    minutes = minutes % 60
    if hours < 24:
        return f"{hours}h{minutes:02d}m"
    days = hours // 24
    hours = hours % 24
    return f"{days}d{hours:02d}h"


def text_digest(value: Any) -> str:
    try:
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"))
    except TypeError:
        raw = repr(value)
    return hashlib.sha256(raw.encode("utf-8", "replace")).hexdigest()[:16]


def payload_turn_id(payload: dict[str, Any]) -> str | None:
    turn_id = payload.get("turn_id")
    if isinstance(turn_id, str) and turn_id:
        return turn_id
    meta = payload.get("internal_chat_message_metadata_passthrough")
    if isinstance(meta, dict):
        turn_id = meta.get("turn_id")
        if isinstance(turn_id, str) and turn_id:
            return turn_id
    return None


def user_payload_text(record: dict[str, Any], payload: dict[str, Any]) -> Any:
    record_type = record.get("type")
    payload_type = payload.get("type")

    if record_type == "response_item" and payload_type == "message" and payload.get("role") == "user":
        text_parts: list[str] = []
        content = payload.get("content")
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    text_parts.append(item["text"])
        return "\n".join(text_parts) if text_parts else content

    if record_type == "event_msg" and payload_type == "user_message":
        return payload.get("message")

    return None


def user_turn_marker(record: dict[str, Any], payload: dict[str, Any], ts: datetime | None) -> str | None:
    text = user_payload_text(record, payload)
    if text is None:
        return None
    return f"user-echo:{iso_z(ts)}:{text_digest(text)}"


def user_turn_key(record: dict[str, Any], payload: dict[str, Any], ts: datetime | None) -> str | None:
    record_type = record.get("type")
    payload_type = payload.get("type")
    turn_id = payload_turn_id(payload)

    if record_type == "response_item" and payload_type == "message" and payload.get("role") == "user":
        return f"turn:{turn_id}" if turn_id else user_turn_marker(record, payload, ts)

    if record_type == "event_msg" and payload_type == "user_message":
        return f"turn:{turn_id}" if turn_id else user_turn_marker(record, payload, ts)

    return None


def update_token_stats(stats: TokenStats, payload: dict[str, Any]) -> None:
    info = payload.get("info")
    if not isinstance(info, dict):
        return

    last_usage = info.get("last_token_usage")
    if isinstance(last_usage, dict):
        stats.context_used = int(last_usage["input_tokens"]) if isinstance(last_usage.get("input_tokens"), int) else None
        stats.last_input_tokens = int(last_usage["input_tokens"]) if isinstance(last_usage.get("input_tokens"), int) else None
        stats.last_cached_input_tokens = (
            int(last_usage["cached_input_tokens"]) if isinstance(last_usage.get("cached_input_tokens"), int) else None
        )
        stats.last_output_tokens = int(last_usage["output_tokens"]) if isinstance(last_usage.get("output_tokens"), int) else None
        stats.last_reasoning_output_tokens = (
            int(last_usage["reasoning_output_tokens"])
            if isinstance(last_usage.get("reasoning_output_tokens"), int)
            else None
        )
        stats.last_total_tokens = int(last_usage["total_tokens"]) if isinstance(last_usage.get("total_tokens"), int) else None

    total_usage = info.get("total_token_usage")
    if isinstance(total_usage, dict) and isinstance(total_usage.get("total_tokens"), int):
        stats.cumulative_total_tokens = int(total_usage["total_tokens"])

    if isinstance(info.get("model_context_window"), int):
        stats.context_window = int(info["model_context_window"])

    if stats.context_used is not None and stats.context_window:
        stats.context_percent = round((stats.context_used / stats.context_window) * 100)

    rate_limits = payload.get("rate_limits")
    if isinstance(rate_limits, dict):
        primary = rate_limits.get("primary")
        if isinstance(primary, dict):
            used_percent = primary.get("used_percent")
            if isinstance(used_percent, (int, float)):
                stats.rate_limit_used_percent = float(used_percent)
            resets_at = primary.get("resets_at")
            if isinstance(resets_at, int):
                stats.rate_limit_resets_at = resets_at


def read_status(path: Path, hook: dict[str, Any]) -> Status:
    session_id = hook.get("session_id") if isinstance(hook.get("session_id"), str) else None
    cwd = hook.get("cwd") if isinstance(hook.get("cwd"), str) else None
    model = hook.get("model") if isinstance(hook.get("model"), str) else None
    session_started_at: datetime | None = None
    latest_event_at: datetime | None = None
    user_turns: list[tuple[str, datetime | None]] = []
    seen_turns: set[str] = set()
    seen_user_markers: set[str] = set()
    token_stats = TokenStats()

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise SystemExit(f"kos-codex-turn-status: cannot read {path}: {exc}") from exc

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue

        ts = parse_ts(record.get("timestamp"))
        if ts is not None:
            latest_event_at = ts if latest_event_at is None or ts > latest_event_at else latest_event_at
            session_started_at = ts if session_started_at is None else session_started_at

        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue

        if record.get("type") == "session_meta":
            if isinstance(payload.get("session_id"), str):
                session_id = payload["session_id"]
            if isinstance(payload.get("cwd"), str):
                cwd = payload["cwd"]
            meta_ts = parse_ts(payload.get("timestamp"))
            if meta_ts is not None:
                session_started_at = meta_ts

        if record.get("type") == "turn_context":
            if isinstance(payload.get("cwd"), str):
                cwd = payload["cwd"]
            if isinstance(payload.get("model"), str):
                model = payload["model"]

        key = user_turn_key(record, payload, ts)
        if key:
            marker = user_turn_marker(record, payload, ts)
            duplicate_by_key = key in seen_turns
            duplicate_by_marker = marker in seen_user_markers if marker else False
            if not duplicate_by_key and not duplicate_by_marker:
                user_turns.append((key, ts))
            seen_turns.add(key)
            if marker:
                seen_user_markers.add(marker)

        if record.get("type") == "event_msg" and payload.get("type") == "token_count":
            update_token_stats(token_stats, payload)

    last_user_ts = user_turns[-1][1] if user_turns else None
    previous_user_ts = user_turns[-2][1] if len(user_turns) > 1 else None
    gap_seconds = None
    if last_user_ts is not None and previous_user_ts is not None:
        gap_seconds = int((last_user_ts - previous_user_ts).total_seconds())

    elapsed_seconds = None
    if session_started_at is not None:
        end = latest_event_at or datetime.now(timezone.utc)
        elapsed_seconds = int((end - session_started_at).total_seconds())

    return Status(
        transcript_path=str(path),
        session_id=session_id,
        cwd=cwd,
        model=model,
        turn_count=len(user_turns),
        last_user_turn_at=iso_z(last_user_ts),
        last_user_turn_local=local_stamp(last_user_ts),
        previous_user_turn_at=iso_z(previous_user_ts),
        gap_seconds=gap_seconds,
        gap=duration(gap_seconds),
        session_started_at=iso_z(session_started_at),
        session_started_local=local_stamp(session_started_at),
        elapsed_seconds=elapsed_seconds,
        elapsed=duration(elapsed_seconds),
        latest_event_at=iso_z(latest_event_at),
        token_stats=token_stats,
    )


def line_status(status: Status) -> str:
    parts = [
        f"codex turn {status.turn_count:03d}",
        status.last_user_turn_local or "time ?",
    ]
    if status.gap:
        parts.append(f"gap {status.gap}")

    ts = status.token_stats
    if ts.context_used is not None or ts.context_window is not None:
        pct = f" {ts.context_percent}%" if ts.context_percent is not None else ""
        parts.append(f"ctx {compact_number(ts.context_used)}/{compact_number(ts.context_window)}{pct}")
    if ts.last_total_tokens is not None:
        parts.append(f"last {compact_number(ts.last_total_tokens)}")
    if ts.cumulative_total_tokens is not None:
        parts.append(f"total {compact_number(ts.cumulative_total_tokens)}")
    if status.session_started_local:
        elapsed = f" +{status.elapsed}" if status.elapsed else ""
        parts.append(f"session {status.session_started_local}{elapsed}")
    if status.model:
        parts.append(status.model)
    if status.cwd:
        parts.append(status.cwd)
    return " | ".join(parts)


def main() -> int:
    args = parse_args()
    hook = read_stdin_json(not args.no_stdin)
    path = choose_transcript(args, hook)
    status = read_status(path, hook)
    if args.json:
        print(json.dumps(asdict(status), indent=2, sort_keys=True))
    else:
        print(line_status(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
