# /completion-verify protocol

The canonical completion-verification contract for harness-plan,
harness-engineering, and direct user invocation.

## Inputs

The skill accepts a contract via three input modes; exactly one must be
supplied:

| Mode                          | Args                                          |
| ----------------------------- | --------------------------------------------- |
| Contract on disk              | `--contract <path-to-json>`                   |
| Feature in features.json      | `--feature <path> --feature-id F003`          |
| Inline JSON via stdin         | `--stdin`                                     |

`--project-root <path>` (default `.`) sets the cwd for command execution
and the location of the optional `.harness/verify-*.log` evidence file.

`--timeout <seconds>` (default 300) caps each individual command. Per-command
timeout, not a global wall clock.

`--no-evidence-log` skips writing the evidence file.

## Contract shapes accepted

The skill normalizes three contract shapes into the same internal model.

### Shape A: harness-plan current-contract.json

```json
{
  "feature_id": "F003",
  "verification_commands": [
    { "command": "pytest tests/test_csv.py -v", "expected_output": "passed" }
  ],
  "manual_checks": [{ "description": "render dialog and click Export" }]
}
```

### Shape B: raw harness-plan feature

```json
{
  "id": "F003",
  "verification": {
    "command": "pytest tests/test_csv.py -v",
    "expected": "passed",
    "manual_check": "render dialog and click Export"
  }
}
```

### Shape C: minimal contract

```json
{
  "id": "IMPL-001",
  "verification_commands": ["pytest"]
}
```

(Strings are accepted for convenience; they're treated as `{command: <str>}`.)

## Status derivation

| Status        | Meaning                                                        | Exit code |
| ------------- | -------------------------------------------------------------- | --------- |
| `pass`        | All commands exited 0, all `expected_output` matched, no manual checks pending | 0 |
| `fail`        | At least one command failed (non-zero exit, timed out, or expected mismatch)   | 1 |
| `partial`     | All commands passed but manual checks remain                   | 2         |
| `no_commands` | Contract has no commands and no manual checks                  | 3         |
| `error`       | Couldn't load the contract (missing, malformed, missing flags) | 3         |

## Evidence log

When `.harness/` exists at `--project-root` and at least one command ran,
the skill writes `.harness/verify-<contract_id>-<timestamp>.log` containing
each command's exit code, duration, and stdout/stderr tails. The path is
echoed back in the `evidence_log` field.

If `.harness/` doesn't exist, evidence logging is skipped silently —
standalone use doesn't require a campaign directory.

## Output guarantees

- The skill emits exactly one JSON object to stdout.
- No prose, no progress bars, no logging on stdout.
- All non-data output (errors invoking subprocesses, etc.) goes to stderr.
- The output is parseable as JSON in all cases — even when status is
  `error`.

## Stability & non-goals

- The skill does not retry. A failure is a failure; the caller decides
  whether to retry.
- The skill does not interpret `manual_checks_pending`. It surfaces them so
  the caller can prompt the user (or refuse to advance, in autodrive).
- The skill does not implement custom matchers. `expected_output` is tried
  as a regex first, then falls back to substring containment.
- `stdout_tail` / `stderr_tail` are clipped to the last 500 bytes. For full
  output, read the evidence log.

## When NOT to use

- For lint-style checks that don't have a clear pass/fail criterion. Use a
  separate lint runner.
- For pure manual review (e.g., "does this UI look good?"). Manual checks
  are surfaced but never marked done by this skill.
