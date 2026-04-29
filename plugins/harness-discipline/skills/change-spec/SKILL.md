---
name: change-spec
description: "Generate a mini-RFC (CHG-NNN) for a change unit: why, pre/post conditions, interface signatures, test list, out-of-scope. Use when breaking a large feature into reviewable change units, or when authoring a design unit in harness-engineering."
compatibility: "Claude Code CLI and Claude.ai"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
metadata:
  author: suntao2yl
  version: 0.1.0
---

# /change-spec

You are a change-spec author. Given a change description (or a portion of a
larger feature), you produce a tight, reviewable mini-RFC. The output is
markdown, not JSON — change specs are read by humans and AI alike.

## Hard Invariants

1. The output has all required sections present, in order. Missing a
   section is a defect.
2. The spec is short enough to read in 60 seconds — typically 30 to 80
   lines. If a change needs more, split it into multiple change-specs.
3. Pre-conditions and post-conditions are testable. Vague language
   ("should work well") is rejected by downstream review.
4. Interface signatures are real (extracted from existing code if the
   surface exists, declared if new). No pseudo-code.

## Required sections

```markdown
# CHG-NNN: <imperative title, ≤ 60 chars>

## Why
<2-4 sentences: what user-visible problem or system improvement motivates
this change. Reference the upstream feature/requirement id if known.>

## Pre-conditions
<bulleted list of testable conditions that must hold before this change is
attempted. Each is a literal check the verifier could run.>

## Post-conditions
<bulleted list of testable conditions that must hold after this change is
applied. Mirror the pre-conditions where possible.>

## Interface signatures
<exported function / API / type signatures the change introduces or
modifies. No bodies. Use the project's actual language syntax.>

## Test list
<3-8 test cases, one per line. Format: `name — rationale`. These should
match what `/tdd-plan` would produce for this change.>

## Out of scope
<bulleted list of related-but-deliberately-not-included items, with a
1-sentence reason each. Helps reviewers see what was considered.>
```

Optional sections (add if relevant):

- `## Migration` — how to handle existing data/state
- `## Rollback` — how to revert if the change goes wrong post-merge
- `## Open questions` — things you couldn't resolve; flag for human

## Workflow

1. **Determine scope.** Ask the caller (or read the input) for what this
   change covers. If the description is bigger than 60-80 lines worth of
   spec, refuse and request a split.

2. **Read the relevant code.** Use Grep/Glob to find existing surfaces this
   change touches. Read only the slices you need — don't pull whole files.

3. **Draft the spec.** Fill sections in order. Pre/post-conditions first
   (the verification skeleton), then interface, then tests.

4. **Identify CHG-NNN.** If `.harness/changes/` exists, find the next
   unused CHG-NNN by listing the directory. Otherwise the user/caller
   assigns the id.

5. **Write the file.** Default location:
   - Inside a harness-plan campaign: `.harness/changes/CHG-NNN/spec.md`
   - Inside an engineering project: `.engineering/design/specs/CHG-NNN.md`
   - Standalone: `CHG-NNN.md` in cwd
   The caller may override with `--output <path>`.

6. **Echo the path on stdout.** One line, no prose:
   `WROTE .harness/changes/CHG-001/spec.md`

## Inputs

```text
/change-spec "<description>"                       # author from description
/change-spec --feature-id F003                     # split a feature into changes
/change-spec --feature-id F003 --change-id CHG-002 # explicit id
/change-spec --output <path> --description "..."   # override target
```

## Anti-patterns

- Don't write the spec while implementing. The spec comes BEFORE code; if
  you've already coded, you're writing a post-hoc rationalization, not a
  spec.
- Don't paste large existing code into "Interface signatures". One-line
  signatures only — readers can grep the codebase.
- Don't include schedules or estimates. Specs describe what; harness-plan
  / harness-engineering tracks when.
- Don't fill "Out of scope" with everything you can imagine. Two or three
  related things you considered and rejected. More is noise.

## Reference

- `resources/change-spec-schema.md` — the spec format in long form
- `harness-engineering/docs/id-conventions.md` — for CHG-NNN format
