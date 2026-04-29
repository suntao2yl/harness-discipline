# /change-spec output schema

Authoritative format for the markdown a `/change-spec` invocation produces.
Used by reviewers and downstream verifiers to know what to expect.

## Filename and location

`CHG-NNN.md` or `CHG-NNN/spec.md`. NNN is 3-digit minimum, no reuse, no
skipping. See `harness-engineering/docs/id-conventions.md` for the full
convention.

Default locations (in priority order):

1. Inside a harness-plan campaign: `.harness/changes/CHG-NNN/spec.md`
2. Inside an engineering project: `.engineering/design/specs/CHG-NNN.md`
3. Standalone: `CHG-NNN.md` in cwd

## Required sections (in order)

```markdown
# CHG-NNN: <title>

## Why

## Pre-conditions

## Post-conditions

## Interface signatures

## Test list

## Out of scope
```

### Title rules

- Imperative mood: "Add CSV exporter", not "CSV exporter added"
- ≤ 60 chars
- No trailing punctuation

### Why

2-4 sentences. Answer:
- What problem are we solving?
- Why now?
- Reference upstream `REQ-NNN` / `F0XX` if known.

### Pre-conditions

Bulleted list. Each item must be a literal check, not a goal:

✗ "Auth must be working"
✓ "`pytest tests/auth/ -k smoke` exits 0"

### Post-conditions

Bulleted list. Mirror pre-conditions where possible. Each must be testable:

✗ "Users can export data"
✓ "GET /api/exports returns 200 with `Content-Type: text/csv`"

### Interface signatures

Real, language-appropriate signatures:

✗ "Add an export function"
✓ ```python
def export(rows: list[dict], fields: list[str]) -> str: ...
```

For modifications, show the new signature with a comment indicating what
changed.

### Test list

3-8 entries. Format: `name — rationale.` Each rationale ends with a period.

```
- `test_csv_export_empty` — Empty input produces just the header.
- `test_csv_export_unicode` — BOM and quoting survive non-ASCII.
- `test_csv_export_huge` — 100k rows complete under 5s.
```

### Out of scope

2-3 items max. Each has a 1-sentence reason.

```
- Excel export (.xlsx) — different file format, separate change.
- Streaming export — current API contract is synchronous.
```

## Optional sections

- `## Migration` — for changes that touch existing data
- `## Rollback` — for changes hard to undo post-merge
- `## Open questions` — flag-for-human items

## Length

A spec is "right-sized" when it can be read in 60 seconds and reviewed
without scrolling fatigue. Typical: 30-80 lines. If you need more, split
the change first.

## Lint rules (advisory)

These are checked by reviewers, not by automated tools today:

- Title is imperative.
- All required sections present.
- Pre/post-conditions list at least 1 item each.
- Test list has ≥ 3 entries.
- Out of scope has ≥ 2 entries.
- File length ≤ 100 lines (warn) / ≤ 200 lines (error).
