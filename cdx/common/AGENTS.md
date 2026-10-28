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
