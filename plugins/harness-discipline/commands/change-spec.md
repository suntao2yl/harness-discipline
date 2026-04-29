---
description: Generate a mini-RFC (CHG-NNN) for a change unit. Markdown output with required sections.
argument-hint: '["<description>"|--feature-id F003|--change-id CHG-002|--output <path>]'
allowed-tools: Read, Glob, Grep, Write
---

Use the `change-spec` skill now.

Interpret this slash command as:

```text
/change-spec $ARGUMENTS
```

Author the spec per the schema in `resources/change-spec-schema.md`. Write
the file to disk per the location rules. Echo the written path as a single
line `WROTE <path>` to stdout.
