# Shared Libraries

This repository is a small, public collection of portable setup files and
utilities that can be adapted between environments, including a work Codex
installation.

## Navigation map

- Purpose
- Publishing rules
- Layout

## Purpose

The home and work environments will not have the same paths, credentials,
installed tools, or policies. Files here are therefore published as reviewed,
standalone starting points rather than as a copy of a home machine or its
private knowledge base.

## Publishing rules

- Publish only files that are safe to make public.
- Remove credentials, tokens, session data, personal paths, private records,
  and transcripts before publishing.
- Prefer small, focused directories with a README that explains installation,
  dependencies, and verification.
- Treat each work-environment adaptation as a copy or extension: validate it
  against the installed work tooling before relying on it.

## Layout

- `cdx/common/AGENTS.md` — portable baseline instructions for a user-level
  Codex installation. Copy this reviewed baseline into the target machine's
  `~/.codex/AGENTS.md`; do not copy authentication, hooks, or `config.toml`.
- `cdx/mac/footer/` — macOS turn-footer scripts and hook configuration for
  Codex CLI.

This layout will grow as additional home tooling is made portable and reviewed
for work use.
