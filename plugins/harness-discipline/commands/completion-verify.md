---
description: Run a contract's verification commands and emit a structured pass/fail/partial verdict as JSON. Canonical Self-Test executor.
argument-hint: '[--contract <path>|--feature <path> --feature-id F003|--stdin] [--project-root <path>] [--timeout 300]'
allowed-tools: Read, Bash
---

Use the `completion-verify` skill now.

Interpret this slash command as:

```text
/completion-verify $ARGUMENTS
```

Forward `$ARGUMENTS` directly to:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/completion_verify.py $ARGUMENTS
```

Print the script's stdout (a single JSON object) verbatim. Do not add prose.
The exit code reflects status: 0=pass, 1=fail, 2=partial, 3=error/no_commands.
