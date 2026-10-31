# Claude Code Adapter

This adapter is for Claude Code. It imports the canonical shared policy from
`common-agent-instructions.md`; do not duplicate shared rules here.

@common-agent-instructions.md

## Runtime basis

Verified against [Claude Code's instruction and memory documentation](https://code.claude.com/docs/en/memory)
on 2026-10-31. Claude Code loads user instructions from `~/.claude/CLAUDE.md`
and supports relative `@path` imports from `CLAUDE.md`.

## Installation

Copy this file to `~/.claude/CLAUDE.md` and copy
`agent-continuity/common-agent-instructions.md` beside it as
`~/.claude/common-agent-instructions.md`. In a Claude Code session, use
`/context` to verify both files appear in the loaded memory files.

## Claude Code-specific operation

For a Claude Code slash command, say that the command is entered inside the
Claude Code session.
