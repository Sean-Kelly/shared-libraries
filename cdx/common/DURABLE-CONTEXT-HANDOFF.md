# Durable Context Handoff

Use this document as a portable pattern for work that must survive an AI session
ending. It is provider-neutral and safe to adapt to any approved repository or
workspace.

## Navigation map

- What durable context is
- The memory stack
- Starting a session
- Ending a session
- Handoff template
- Public-safety boundary

## What durable context is

No AI session is a complete, permanent source of truth. Conversation history,
provider summaries, and workspace snapshots can help, but each can be compacted,
expired, inaccessible, or incomplete.

Treat durable context as a small retrieval system:

```text
entry map -> authoritative records -> task handoff -> evidence
```

The agent should begin with the map, open only the governing records relevant to
the task, and use commits, tests, logs, or source material as evidence.

## The memory stack

| Layer | Purpose | Owner |
| --- | --- | --- |
| Repository instructions | Point to the project rules and sources of truth | Project maintainers |
| Canonical records | Preserve decisions, requirements, and current plans | Named document owner |
| Current-task handoff | State what is active, what changed, and the next proof | The person or agent closing the task |
| Evidence | Preserve commits, tests, issue links, logs, and source references | The system that produced it |
| Provider session or workspace | Keep short-term conversational and file state | The AI provider or workspace owner |

Use provider memory or session-resume features as convenience, not as the only
place a material decision exists. A concise `AGENTS.md` should be a map, not an
encyclopedia.

## Starting a session

1. Read the applicable `AGENTS.md` and the active handoff.
2. Open the named governing record before making a claim or change.
3. Confirm the task, current branch or workspace, success condition, and next
   verification step.
4. Retrieve raw history only when the handoff and its cited evidence leave a
   material gap.

## Ending a session

Before a task is handed off, update the relevant project record and write or
refresh the short active handoff. Include only information that could change a
future decision, implementation, verification, safety boundary, or recovery
action.

Then preserve the actual work in its normal system of record: commit and push
code or documents, retain test results or issue links, and record unresolved
questions with an owner and a condition for reopening them.

Do not use a handoff as a substitute for reviewing the resulting work.

## Handoff template

Copy this into a project-local file such as `docs/active-context.md` and keep it
short.

```md
# Active Context

## Current task

<one sentence describing the desired outcome>

## Governing sources

1. `<path-or-link>` — <why it governs>
2. `<path-or-link>` — <supporting evidence>

## Current state

- Completed: <verified result>
- Active: <what remains>
- Do not assume: <known uncertainty or boundary>

## Next action and proof

- Next action: <one bounded action>
- Proof of success: <specific test, readback, review, or visible result>

## Recovery

- Branch/workspace: <identifier>
- Evidence: <commit, issue, test output, or artifact link>
```

## Public-safety boundary

Keep the handoff inside the data boundary of the project and its approved tools.
Do not place secrets, access tokens, personal data, customer data, internal-only
URLs, raw conversation transcripts, or unreviewed logs in a public repository.

If a work environment has its own policy or approved knowledge system, use that
system as the authoritative location for work-specific context. A public
repository can carry only generic process and intentionally public artifacts.

## Further reading

- OpenAI describes durable sessions, compaction, and recovery in its
  [Agents API overview](https://developers.openai.com/api/docs/guides/agents-api/overview).
- OpenAI's [Sandbox Agents guide](https://developers.openai.com/api/docs/guides/agents/sandboxes)
  distinguishes session history from reusable workspace memory.
- OpenAI's [Codex workflow cookbook](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)
  describes `AGENTS.md` and versioned context files as durable project guidance.
