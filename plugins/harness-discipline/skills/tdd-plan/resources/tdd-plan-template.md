# /tdd-plan output schema

Authoritative reference for the JSON the skill emits. Used by callers
(harness-plan, harness-engineering) to validate they got a usable plan.

```json
{
  "framework_detected": "pytest | jest | vitest | cargo-test | go-test | null",
  "test_cases": [
    {
      "name": "<snake_case identifier>",
      "type": "unit | integration | e2e | property",
      "rationale": "<one sentence: what bug/edge would this catch?>"
    }
  ],
  "implementation_skeleton": [
    {
      "file": "<relative path>",
      "purpose": "<one sentence>",
      "key_functions": ["<signature>", ...]
    }
  ],
  "verification_command": "<shell command that runs ALL proposed tests>",
  "notes": "<optional: assumptions, missing context the user should fill>"
}
```

## Field rules

- `framework_detected`: lowercase. Use the canonical name. `null` only if no
  test framework is configured in the project.
- `test_cases[]`: 3 to 8 entries. Less than 3 → likely too shallow. More
  than 8 → split the feature first.
- `test_cases[].name`: must be a valid identifier in the framework's
  convention (e.g., `test_*` for pytest, `*.test.*` for vitest).
- `test_cases[].rationale`: full sentence, ends with a period.
- `implementation_skeleton[].key_functions[]`: signatures only, no bodies.
- `verification_command`: must include all test cases listed. Use `-k` or
  similar selectors if you want to scope.
- `notes`: optional, rarely used. Use for "I assumed the test runner is
  pytest, but the project has both pytest and unittest configured — pick one"
  type clarifications.

## Error envelope

If you can't produce a plan, emit:

```json
{ "error": "<short reason>", "details": "<optional longer explanation>" }
```

Callers MUST stop on `error` and surface the message to the user; they MUST
NOT proceed with a partial plan.
