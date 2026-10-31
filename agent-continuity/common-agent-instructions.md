# Common Agent Instructions

Use this provider-neutral baseline for instructions that should govern work
regardless of the AI agent or its interface. A runtime adapter may add only the
instructions necessary for that runtime's discovery, command, permission, or
configuration model.

## Navigation map

- Purpose and boundary
- Universal operating rules
- Agent architecture and autonomy boundary
- Guidance promotion
- Environment and publication targets
- Adapter contract
- Adoption and verification

## Purpose and boundary

This file is the shared policy layer, not a promise that every agent will load
it automatically. An agent harness must be configured or instructed to read it.
Do not infer support from a filename, directory name, or another agent's
behavior.

Keep runtime-specific commands, configuration paths, hook semantics, and tool
names out of this file. Put those in a thin adapter for the named runtime.

## Universal operating rules

- Label an actionable instruction with its destination before the action.
- For a terminal command, name the terminal or shell prompt that receives it.
- For a file edit, name the exact file and the setting, section, or line to
  change.
- Do not place a shell command and a configuration-file snippet together
  without destination labels.
- Use `America/Chicago` as the default timezone unless the user specifies
  another timezone.
- Write human-readable dates and times as `YYYY-MM-DD HH:MM:SS` in 24-hour
  time; include the applicable timezone when it matters.
- Use `YYYY-MM-DD--HHMM--<type>--<slug>.<ext>` for chronologically sortable
  artifact filenames. Use lowercase, hyphen-separated slugs; do not use
  colons, AM/PM, or American numeric dates in filenames.

## Agent architecture and autonomy boundary

### Model, agent, and harness

- A **model** produces or evaluates content.
- An **agent** is a model configured with a role, instructions, and available
  tools.
- A **harness** supplies the runtime around an agent: context and instruction
  loading, tool execution, permissions, session state, scheduling, and
  observability.

Do not infer a harness's capabilities or protections from the model name. A
model can be local while its harness still has network access, cloud-connected
tools, or broad local authority.

### Autonomous-agent boundary

Model locality or provider choice does not reduce the risk created by an
agent's permissions, autonomy, or integrations.

Before relying on an agent that can use tools, access credentials or data, act
on a schedule, retry independently, or contact external systems, identify:

1. its authorized actions and data boundary;
2. the containment or isolation boundary for tools and credentials;
3. which actions require confirmation and which are permitted unattended;
4. resource ceilings for time, tokens or model cost, storage, and external
   side effects;
5. the logs or readbacks that prove what happened; and
6. the stop, rollback, and recovery path.

Choose controls in proportion to the authority granted. A read-only local
assistant and a scheduled agent with email, shell, or browser authority do not
have the same decision boundary. Treat third-party tools, plugins, and skills
as code with the agent's effective privileges unless an independent containment
boundary has been verified.

## Guidance promotion

When promoting a task-specific observation, incident, or repair into reusable
guidance, state the portable invariant and decision condition first. Keep named
tools, fields, workflows, and conventions in a conditional local procedure
unless their portability is established.

Use [Scope-Preserving Guidance](scope-preserving-guidance.md) for the
four-layer method and promotion tests.

## Environment and publication targets

Treat workspace, repository, branch, remote host, visibility, and publication
path as independent facts. Do not infer one from another.

Before recommending, linking, copying, or publishing an artifact, identify the
source workspace and artifact; destination repository and branch; hosting
account and visibility when publication matters; and destination path and
intended operation. If the destination is not named, ask rather than selecting
a nearby repository or assuming public visibility from a configured remote.

## Adapter contract

An adapter may specify the runtime's instruction-file locations, discovery
order, supported import mechanism, command syntax, permission controls, or
verification procedure. It must:

1. name the runtime and version or documentation basis when behavior can vary;
2. state how this shared baseline is made available to that runtime;
3. avoid restating shared policy unless the runtime cannot load it separately;
   and
4. label any copied policy as a synchronized copy and name its canonical source.

Do not create an adapter for an unspecified local model. A local model's
instruction mechanism belongs to its harness, not to the model name alone.

## Adoption and verification

Before relying on an adapter, verify the target runtime actually loaded the
instruction file on the target machine or in a controlled test. Record the
runtime, version, instruction location, loading evidence, and any precedence
rules that affect the result.

Review shared rules when a cross-runtime counterexample appears. Move a rule
into an adapter if it depends on a runtime-specific capability or lifecycle.
