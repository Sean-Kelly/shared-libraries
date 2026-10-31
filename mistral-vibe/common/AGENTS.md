# Mistral Vibe Adapter

This adapter is for Mistral Vibe Code. Its canonical shared policy is
`agent-continuity/common-agent-instructions.md` in this repository. When
installing this adapter, copy that file beside this one as
`~/.vibe/common-agent-instructions.md`; before substantive work, read and
follow it. The shared policy must remain usable by other agent runtimes.

## Runtime basis

Verified against [Mistral Vibe Code's agent documentation](https://docs.mistral.ai/vibe/code/cli/agents)
on 2026-10-31. Vibe loads user-level instructions from `~/.vibe/AGENTS.md` and
project-level `AGENTS.md` files within a trusted folder.

## Mistral Vibe-specific operation

For a Vibe slash command, say that the command is entered inside the Vibe
session.
