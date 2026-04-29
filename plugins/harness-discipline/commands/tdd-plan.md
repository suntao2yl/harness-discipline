---
description: Test-first plan for a feature or change unit. Emits JSON with test cases, implementation skeleton, verification command.
argument-hint: '["description"|--feature-id F003|--contract <path>]'
allowed-tools: Read, Glob, Grep, Bash
---

Use the `tdd-plan` skill now.

Interpret this slash command as:

```text
/tdd-plan $ARGUMENTS
```

Inputs supported:
- A free-form quoted description: `"<what to plan tests for>"`
- `--feature-id F003` to read the feature from `.harness/features.json`
- `--contract <path>` to read an existing contract JSON

Produce JSON to stdout per the schema in `resources/tdd-plan-template.md`.
Do not emit prose around the JSON. Do not write code or tests — only plan.
