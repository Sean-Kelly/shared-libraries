# Cold-Start Continuity Audit

Use this provider-neutral prompt in a new AI-agent session to test whether a
workspace can be resumed without relying on earlier chat or hidden memory.

## Navigation map

- Purpose
- Prompt
- Passing result
- Safety boundary

## Purpose

A workspace is independently bootable when a fresh agent can find its local
entry point, read its governing records, distinguish evidence from inference,
and identify one bounded next action without asking a person to reconstruct
history.

## Prompt

**In a new agent session:** paste the following prompt.

```text
This is a cold-start continuity test. Do not rely on prior chat history, model
memory, or assumptions about another machine.

Inspect only the local workspace and its approved local records. First read the
applicable AGENTS.md files. Then find and read the local continuity entry point
(for example, ACTIVE-CONTEXT.md, WORKSPACE-BOOTSTRAP.md, or an equivalent
document) and the records it names.

Do not modify files or settings.

Report:

1. What system/workspace this is and its stated boundary.
2. What tools, hooks, bookmarklets, or other adaptations are recorded as
   installed or adopted here.
3. The governing sources for current work, in their stated order.
4. The current task, completed work, unresolved items, and exact next action.
5. The evidence supporting each installed/adopted item.
6. Anything you could not verify locally. Do not infer it from filenames,
   repository names, or likely similarity to another environment.
7. Whether this workspace is independently bootable by a fresh agent. If not,
   identify the smallest missing record or pointer needed to make it so.

Keep the report concise and distinguish observed facts from inferences.
```

## Passing result

A passing report cites local records, identifies the current boundary and next
proof, and names unknowns plainly. A report that guesses from a repository name,
assumes another machine has the same setup, or relies on unavailable chat
history is a failed continuity test.

## Safety boundary

Run the audit only where the agent is authorized to read the workspace. Keep
work-specific records in their approved local system; this public prompt is not
a channel for transferring private information.
