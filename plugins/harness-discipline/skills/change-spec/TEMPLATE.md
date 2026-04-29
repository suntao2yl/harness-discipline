# change-spec — Template

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

## Optional sections

Add when relevant:

- `## Migration` — how to handle existing data/state during the change.
- `## Rollback` — how to revert if the change goes wrong post-merge.
- `## Open questions` — things you couldn't resolve; flag for human review.

## Field rules

### Title
- Imperative mood: "Add CSV parser", not "Adding" or "Adds".
- ≤ 60 chars.

### Why
- 2-4 sentences. Lead with the user-visible or system-visible problem.
- Reference upstream id if applicable: `Drives F004; addresses INC-23.`

### Pre-conditions / Post-conditions
- Each item is something a verifier could check programmatically OR by reading code/state.
- Examples that work: `tests/test_csv.py exists`, `Endpoint /api/export returns 200 on GET with valid token`.
- Examples that don't: `code is clean`, `users are happy`.

### Interface signatures
- Use the project's actual language syntax (Python type hints, TypeScript types, Go function signatures, etc.).
- One line per signature when possible.
- For modifications: show before / after on adjacent lines.

### Test list
- 3-8 cases. Fewer real cases beats more shallow ones.
- Format: `test_name — one-sentence rationale`.
- Should be deliverable by `/tdd-plan` if invoked separately.

### Out of scope
- Two to three items that you specifically considered and chose to exclude.
- Each with a one-sentence reason: `Bulk import — out of scope; gated on F009 schema migration.`
- Don't list "everything we won't do" — only the things a reviewer might wonder about.
