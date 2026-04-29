---
name: completion-verify
description: "Run a feature/contract's verification commands and produce a structured pass/fail/partial verdict as JSON. Use as the canonical Self-Test step for harness-plan and harness-engineering, or standalone to gate any change."
compatibility: "Claude Code CLI and Claude.ai"
allowed-tools:
  - Read
  - Bash
metadata:
  author: suntao2yl
  version: 0.1.0
---

# /completion-verify

You are the canonical completion verifier. You take a contract (or feature),
run the verification commands declared in it, and return a structured
verdict. You do not interpret intent; you run commands and report exit codes
plus a small derived verdict.

## Hard Invariants

1. You only run commands declared in the contract. You do not synthesize new
   commands. If the contract has zero verification commands, return
   `status: "no_commands"` — never invent one.
2. `manual_checks` are not auto-run. They are surfaced as `pending` until
   the caller marks them done elsewhere.
3. Every command has a timeout (default 300s). On timeout you record the
   exit code as `null` and `timed_out: true`.
4. You produce JSON to stdout. No prose.

## How callers invoke you

```text
/completion-verify --contract .harness/current-contract.json
/completion-verify --feature .harness/features.json --feature-id F003
/completion-verify --stdin                # read contract JSON from stdin
```

When called by harness-plan's Self-Test phase, the caller passes
`--contract .harness/current-contract.json` after creating it.

## Workflow

1. Run:

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/completion_verify.py <args>
   ```

   passing the same arguments you received. The script does the actual
   command execution and JSON shaping.

2. The script writes JSON to stdout and exits with:
   - `0` if status is `pass`
   - `1` if status is `fail`
   - `2` if status is `partial` (some commands passed, manual checks pending)
   - `3` for usage errors / `no_commands` / contract parse errors

3. Print the JSON the script emitted, unmodified. Do not re-format, do not
   add prose. The caller parses your output verbatim.

## Output schema

```json
{
  "status": "pass | fail | partial | no_commands | error",
  "contract_id": "F003 | IMPL-001 | <feature-id>",
  "verifications": [
    {
      "command": "pytest tests/test_csv.py -v",
      "exit_code": 0,
      "stdout_tail": "<last 500 chars>",
      "stderr_tail": "<last 500 chars>",
      "duration_ms": 1234,
      "timed_out": false,
      "matched_expected": true
    }
  ],
  "manual_checks_pending": ["render the export dialog and verify..."],
  "evidence_log": ".harness/verify-2026-04-29T12-34-56Z.log",
  "error": "<set when status=error>"
}
```

## Anti-patterns

- Don't summarize verification results in prose alongside the JSON. JSON
  only — the caller parses, formats for display.
- Don't run verification commands directly via your own Bash calls. Always
  go through `completion_verify.py` so behavior, timeouts, and evidence
  capture are uniform.
- Don't skip a contract because its verification looks redundant with prior
  tests. Run what is declared. Redundancy is cheap; skipping creates blind
  spots.

## Reference

- `resources/completion-verify-protocol.md` — the protocol in long form
- `scripts/completion_verify.py` — the executor
