# Turn footer for macOS

This package reproduces the custom status payload behind the line beginning
`Hook · codex turn ...`. It has no credentials, tokens, user transcript,
session ID, or private path.

## Contents

- `turn-status.py` — read-only collector for Codex JSONL
  transcripts.
- `stop-status-hook.py` — Stop-hook wrapper that returns the
  collector line in Codex's hook JSON format.
- `hooks.json` — user-level Codex hook configuration.

## Requirements

- Codex CLI with lifecycle hook support.
- Python 3.9 or later. The scripts use only the Python standard library.
- A local Codex CLI session transcript under `~/.codex/sessions/`.

## Installation

At a macOS Terminal prompt, copy the two scripts to the directory that the
hook wrapper expects:

```sh
mkdir -p "$HOME/.codex/footer"
cp turn-status.py stop-status-hook.py "$HOME/.codex/footer/"
chmod 755 "$HOME/.codex/footer/turn-status.py" "$HOME/.codex/footer/stop-status-hook.py"
```

In a text editor, create `~/.codex/hooks.json` from `hooks.json` only
when it does not already exist. If it already exists, merge the `Stop` entry
rather than replacing the file. Codex merges `hooks.json` with inline `[hooks]`
entries in `config.toml`, but OpenAI recommends one representation per config
layer.

Start a new Codex CLI session, enter `/hooks`, and review/trust the new Stop
hook. Codex records trust for the exact hook definition, so a later change will
need another review.

## Verification

At a macOS Terminal prompt, after starting a Codex session:

```sh
"$HOME/.codex/footer/turn-status.py" --latest --no-stdin
printf '%s' '{"hook_event_name":"Stop"}' | "$HOME/.codex/footer/stop-status-hook.py"
```

The first command prints the turn/context line; the second prints JSON with
`"continue": true` and that line as `"systemMessage"`.

## What Codex provides versus this package

The custom scripts generate only `codex turn ...`. No custom file here emits
either the `Hook ·` prefix or the separate `Worked for …` line; the home
configuration and relevant scripts were searched for both. Those two portions
are therefore not part of this scaffolding. I have not directly read the work
Mac's renderer, so confirm its exact hook label and timing in that installed
Codex version.

The home `~/.codex/config.toml` additionally has this optional native TUI status
line setting; it is unrelated to the hook footer:

```toml
[tui]
status_line = ["model-with-reasoning", "context-remaining", "current-dir"]
status_line_use_colors = true
```

## Disable

In `~/.codex/hooks.json`, remove the `Stop` hook entry or use Codex's `/hooks`
interface to disable it. The wrapper also supports an emergency local kill
switch: create `~/.config/kos/codex-turn-status-hook.off`.
