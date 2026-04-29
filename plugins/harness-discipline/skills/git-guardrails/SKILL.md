---
name: git-guardrails
description: "Set up Claude Code PreToolUse hook to block dangerous git commands (push, reset --hard, clean -fd, branch -D, checkout ., restore .) before they execute. Use when user wants git safety hooks, autodrive protection, or to block destructive git operations."
compatibility: "Claude Code CLI only (uses settings.json hooks)"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
metadata:
  author: suntao2yl (adapted from mattpocock/skills)
  version: 0.1.0
  upstream: https://github.com/mattpocock/skills/tree/master/git-guardrails-claude-code
---

# /git-guardrails

Install a `PreToolUse` Bash hook that blocks dangerous git commands before Claude can run them. When matched, the hook exits with code 2 and Claude sees a `BLOCKED` message instead of executing.

## What gets blocked

- `git push` (all variants, including `--force`)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

## Workflow

### 1. Ask scope

Project-only (`.claude/settings.json`) or global (`~/.claude/settings.json`)?

### 2. Copy the hook script

Bundled at `scripts/block-dangerous-git.sh`. Copy to:

- **Project**: `.claude/hooks/block-dangerous-git.sh`
- **Global**: `~/.claude/hooks/block-dangerous-git.sh`

`chmod +x` after copying.

### 3. Register the hook in settings

Merge into existing `hooks.PreToolUse` (do NOT overwrite other hooks).

**Project**:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh" }
        ]
      }
    ]
  }
}
```

**Global**:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/block-dangerous-git.sh" }
        ]
      }
    ]
  }
}
```

### 4. Customize

Ask user if they want to add or remove patterns. Edit the `DANGEROUS_PATTERNS` array in the copied script.

### 5. Verify

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

Must exit `2` and print `BLOCKED:` to stderr.

## Autodrive synergy

In autodrive nobody approves tool calls. This hook is the last line of defense against irreversible git operations. Pair with `caveman` for short logs + `harness-plan` for resumable state.
