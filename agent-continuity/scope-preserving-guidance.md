# Scope-Preserving Guidance

Use this provider-neutral playbook when turning an observation, incident,
experiment, or local repair into reusable guidance. Its purpose is to preserve the
reasoning that matters without promoting a successful local method into an
unconditional rule.

## Navigation map

- Purpose
- Four-layer model
- Promotion tests
- Writing procedure
- Environment and publication targets
- Examples
- Limits and review

## Purpose

The durable product is a portable constraint and a clear decision test. The tool,
interface feature, or convention used in the originating case remains a conditional
implementation detail unless it has independently established portability.

## Four-layer model

Before drafting reusable guidance, write four short statements:

1. **Observed circumstance** — facts established in the originating case.
2. **Portable invariant** — the constraint that remains true in materially
   different contexts.
3. **Decision test** — observable facts that determine which response fits.
4. **Local method** — the tool, field, interface, or convention used when the test
   passes.

Only the invariant is normally unconditional. The decision test is reusable when its
conditions are observable. The local method must state its preconditions.

## Promotion tests

### Replacement test

Replace the domain nouns with a materially different case. If the instruction becomes
nonsensical or unsafe, it belongs in a local procedure rather than a general rule.

### Counterexample test

Name the nearest ordinary situation where the method is unavailable, prohibited, or
has different meaning. If that situation defeats the instruction, promote the
underlying constraint and make the method conditional.

### Layer test

Restate the sentence in this form:

> Preserve **X**. If **Y** is observed, use **Z**.

If the restatement exposes a missing condition, do not write “always use Z.”

### Subsumption test

Check whether an existing principle already supplies the invariant. If it does, link
or cite that principle and add only the missing decision test or local procedure.
Avoid minting a new standing rule for an old constraint.

## Writing procedure

1. Preserve the observed case in a case or decision record, including uncertainty.
2. Draft the invariant without named products, interfaces, organizations, or local
   conventions.
3. Write the decision test using facts a future reader can observe or verify.
4. Write the local method as a conditional branch with its prerequisites.
5. Run the promotion tests and revise the scope of each statement.
6. State the decision: **adopt**, **extend**, **defer**, or **reject**.
7. Record what evidence would revise the guidance, especially if the rule rests on a
   single case.

Use a case record or probationary procedure when recurrence, consequence, or trigger
clarity is not yet sufficient for a standing rule.

## Environment and publication targets

Workspace, repository, branch, remote host, visibility, and destination path are
independent facts. Do not infer one from another.

Before recommending, linking, copying, or publishing an artifact, identify:

- the source workspace and artifact;
- the destination repository and branch;
- the hosting account and visibility when publication matters; and
- the destination path and intended operation.

If the destination is not named, ask rather than selecting a nearby repository or
assuming public visibility from a configured remote.

## Examples

### Interface example

Observed circumstance: a form has no supplied account number and includes a field
explicitly labeled for comments.

- **Invariant:** do not invent an identifier.
- **Decision test:** does the form explicitly provide a field for a preference or
  comment?
- **Local method:** if yes, record the preference in that field; otherwise ask how
  it should be represented.

“Always put preferences in Comments” fails the counterexample test: many forms lack
that field or reserve it for a different purpose.

### Operations example

Observed circumstance: an automated task failed after a temporary network outage and
one retry succeeded.

- **Invariant:** transient dependency failures need bounded recovery and evidence.
- **Decision test:** is the failure classified as transient, and is retry safe for
  the operation?
- **Local method:** retry within the owner's documented limit and retain the result.

“Always retry failed operations” fails when the action is non-idempotent, costly, or
likely to make a partial failure worse.

## Limits and review

This playbook does not prohibit local procedures. Specific methods are valuable when
their scope and prerequisites are named. It also does not require every observation
to become policy; a well-preserved case record may be the correct outcome.

Review a rule when a new case requires an exception, when its decision test cannot be
observed reliably, or when a local method is repeatedly copied into unrelated work.
The response may be to clarify conditions, relocate the method, or retire the rule.
