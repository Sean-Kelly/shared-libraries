# Global Codex Instructions

## Execution Context

- Always label actionable instructions by destination before the action.
- For terminal commands, say which terminal or shell prompt receives the command.
- For file edits, name the exact file to open in Pulsar, VS Code, or another editor, and name the line or setting to change.
- For Codex TUI commands, say the command is typed inside the Codex session.
- Do not place shell commands and config-file snippets adjacent without destination labels.

## File Naming

- Use `America/Chicago` as the default timezone unless the user specifies
  another timezone.
- For human-readable dates and times, use `YYYY-MM-DD HH:MM:SS` in 24-hour
  time; include the applicable timezone when it matters.
- For chronologically sortable artifact filenames, use
  `YYYY-MM-DD--HHMM--<type>--<slug>.<ext>`.
- Use lowercase, hyphen-separated slugs; do not use colons, AM/PM, or
  American numeric dates in filenames.

## Reusable Guidance

- When promoting a task-specific observation, incident, or repair into reusable
  guidance, state the portable invariant and decision condition first. Keep named
  tools, fields, workflows, and conventions in a conditional local procedure unless
  their portability is established.

## Environment Boundaries

- Treat workspace, repository, branch, remote host, visibility, and publication path
  as independent facts. Do not infer one from another. Before recommending, linking,
  copying, or publishing an artifact, name the intended target and verify the
  attributes relevant to that action; if the target is unspecified, ask.
