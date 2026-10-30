# Agent Continuity

Provider-neutral patterns for making a project or workspace understandable to a
fresh AI agent after a prior session ends.

## Navigation map

- Scope
- Files
- Use

## Scope

These documents apply to Codex, Claude, Mistral, local models, and future
agents. They describe durable project records and retrieval practices; they do
not require a specific provider's memory, session, or workspace feature.

## Files

- `durable-context-handoff.md` — a pattern for records that preserve material
  context across session boundaries.
- `cold-start-continuity-audit.md` — a copy/paste prompt that tests whether a
  fresh agent can reconstruct local state without relying on earlier chat.

## Use

Keep the canonical facts, decisions, evidence, and active-task record inside
the project or approved knowledge system that owns them. Use this directory for
generic patterns only; do not put private project context, transcripts,
credentials, or captured data here.
