# tdd-plan — Detailed Reference

## Vertical-slice

This plan is the *blueprint*, not the *commitment*. The implementer should iterate:

```
RED → GREEN: test_1 → impl_1
RED → GREEN: test_2 → impl_2
...
```

Bulk-writing all tests first is "horizontal slicing" — it produces tests of imagined behavior that pass when behavior breaks and fail when it's fine. Plan ahead, but execute one slice at a time.

If the caller is a human, mention this when delivering the JSON. If the caller is `harness-plan`, the contract enforces vertical slicing automatically.

For full philosophy and refactor candidates, see the `tdd` skill.

## Output schema

```json
{
  "framework_detected": "pytest",
  "test_cases": [
    {
      "name": "test_csv_export_empty",
      "type": "unit",
      "rationale": "Empty input should produce just the header row, not crash."
    },
    {
      "name": "test_csv_export_unicode",
      "type": "unit",
      "rationale": "BOM and quoting must survive non-ASCII fields."
    }
  ],
  "implementation_skeleton": [
    {
      "file": "src/csv_export.py",
      "purpose": "CSV exporter with configurable delimiter and quoting",
      "key_functions": [
        "export(rows: list[dict], fields: list[str]) -> str"
      ]
    }
  ],
  "verification_command": "pytest tests/test_csv_export.py -v"
}
```

### Field rules

- `framework_detected`: string or `null` (only if no tests exist in the project).
- `test_cases[].name`: identifier-style, matches a real test the implementer can register (e.g. `test_*` for pytest, `it("...")` description for jest).
- `test_cases[].type`: `unit | integration | e2e | smoke`.
- `test_cases[].rationale`: one sentence — explains *why this case matters*, not what it does.
- `implementation_skeleton[].key_functions`: signatures only, no bodies.
- `verification_command`: must exit 0 iff all proposed tests pass; can be `;`-chained.

### Failure mode

If you cannot produce valid JSON (e.g. ambiguous feature, no detectable framework, can't write a real verification command), output:

```json
{ "error": "<reason>" }
```

and stop. The caller will see the error and decide.
