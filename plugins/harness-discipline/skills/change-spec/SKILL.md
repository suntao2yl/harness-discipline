---
name: change-spec
description: "Generate a tight mini-RFC (CHG-NNN) for a change unit: why, pre/post conditions, interface signatures, test list, out-of-scope. Use when breaking a large feature into reviewable change units, authoring a tiny-commit refactor plan, or designing a unit in harness-engineering."
compatibility: "Claude Code CLI and Claude.ai"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
metadata:
  author: suntao2yl
  version: 0.3.0
---

# /change-spec

Given a change description (or a portion of a larger feature), produce a tight, reviewable mini-RFC. Output is markdown — change specs are read by humans and AI alike.

## Hard invariants

1. All required sections present, in order. Missing a section is a defect.
2. Short enough to read in 60 seconds — typically 30-80 lines. Larger changes must be split into multiple change-specs.
3. Pre- and post-conditions are testable. Vague language ("should work well") is rejected by downstream review.
4. Interface signatures are real (extracted from existing code if the surface exists, declared if new). No pseudo-code.

## Inputs

```text
/change-spec "<description>"
/change-spec --feature-id F003                     # split a feature into changes
/change-spec --feature-id F003 --change-id CHG-002
/change-spec --output <path> --description "..."   # override target
```

## Workflow

1. **Determine scope.** If the description exceeds 60-80 lines worth of spec, refuse and request a split.
2. **Read relevant code.** Grep/Glob existing surfaces. Slices only — no whole-file reads.
3. **Draft the spec.** Fill sections in order: pre/post (verification skeleton) → interface → tests.
4. **Identify CHG-NNN.** If `.harness/changes/` exists, list it for the next unused id; otherwise caller assigns.
5. **Write the file.** Default location:
   - Inside a harness-plan campaign: `.harness/changes/CHG-NNN/spec.md`
   - Inside an engineering project: `.engineering/design/specs/CHG-NNN.md`
   - Standalone: `CHG-NNN.md` in cwd
   - Caller may override with `--output <path>`.
6. **Echo the path on stdout.** One line, no prose: `WROTE .harness/changes/CHG-001/spec.md`

## Required sections

See [TEMPLATE.md](TEMPLATE.md) for the full template with field-by-field rules. Optional sections: `Migration`, `Rollback`, `Open questions`.

## Anti-patterns

- Don't write the spec while implementing. Spec comes BEFORE code; otherwise it's post-hoc rationalization.
- Don't paste large existing code into Interface Signatures. One-line signatures — readers can grep.
- Don't include schedules or estimates. Specs describe *what*; harness-plan / harness-engineering tracks *when*.
- Don't pad Out of Scope. Two or three things you considered and rejected. More is noise.
- Don't smuggle drive-by refactors, style fixes, or speculative abstractions into a CHG. Every changed line must trace to a stated Pre/Post condition. See [resources/code-anti-patterns.md](resources/code-anti-patterns.md) for concrete before/after pairs covering hidden assumptions, speculative complexity, drive-by refactoring, and vague success criteria.

## Surgical-changes test

A change-spec passes the surgical test when:

1. Every line in the eventual diff traces to a Pre/Post condition.
2. Stylistic drift (quotes, type hints, formatting) inside the touched file is zero — match surrounding style even if you'd write it differently.
3. Adjacent improvements ("while I'm here let me also...") are filed as separate CHGs, not folded in.

This is downstream review's first check. Failing it means the spec was too loose, not that the implementation was sloppy — fix the spec.

## Tiny-commit refactor plans

`change-spec` is also the tool for producing tiny-commit refactor plans (one CHG per commit). Use when a refactor must land in small, individually revertable steps. Each CHG names exactly one observable transformation; the chain together completes the refactor. Adapted pattern from `mattpocock/skills/request-refactor-plan`.

## Composes with

- `tdd-plan` — `Test list` should align with what `/tdd-plan` would produce.
- `harness-plan` change units — propose → spec (this skill) → verify → archive.
- `harness-engineering` design phase — design units use this same format.

See [TEMPLATE.md](TEMPLATE.md), [resources/code-anti-patterns.md](resources/code-anti-patterns.md), `resources/change-spec-schema.md`, `harness-engineering/docs/id-conventions.md`.
