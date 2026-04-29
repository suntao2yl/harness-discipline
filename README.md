# harness-discipline

[English](README.md) | [中文](README.zh-CN.md)

Reusable discipline skills for AI-driven software engineering, designed to
be composed into larger lifecycle harnesses (`harness-plan`,
`harness-engineering`) or used standalone.

## Skills

### Core (used by harness-plan / harness-engineering)

| Slash command        | Purpose                                                         |
| -------------------- | --------------------------------------------------------------- |
| `/tdd-plan`          | Test-first plan: test cases + implementation skeleton           |
| `/completion-verify` | Run a contract's verification commands and produce JSON verdict |
| `/change-spec`       | Generate a mini-RFC for a change unit (CHG-NNN); enforces the surgical-changes test |

### Engineering practice (standalone)

| Skill name        | Purpose                                                                          |
| ----------------- | -------------------------------------------------------------------------------- |
| `tdd`             | Red-green-refactor in vertical slices; tests survive refactors                   |
| `write-a-skill`   | Author or refactor skills with proper structure and progressive disclosure       |

### Token / safety helpers (recommended for autodrive)

| Skill name        | Purpose                                                                          |
| ----------------- | -------------------------------------------------------------------------------- |
| `caveman`         | Ultra-compressed output mode; cuts token usage ~75% with no loss of substance    |
| `git-guardrails`  | PreToolUse hook that blocks dangerous git commands before they execute           |

Each skill is independent, has its own SKILL.md (≤100 lines), and can be
invoked without loading the others — load on demand.

The four standalone / helper skills (`tdd`, `write-a-skill`, `caveman`,
`git-guardrails`) are adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) under MIT.

The `change-spec` anti-patterns reference (`skills/change-spec/resources/code-anti-patterns.md`)
distills concrete before/after pairs from
[karpathy-guidelines](https://github.com/forrestchang/andrej-karpathy-skills) under MIT —
hidden assumptions, speculative complexity, drive-by refactoring, and vague
success criteria, each shown as a bad spec vs. a surgical spec.

## Why this exists

`harness-plan` and `harness-engineering` both need TDD planning, completion
verification, and change specs. Before this plugin those capabilities were
duplicated as prose inside two SKILL.md files. Extracting them here:

- avoids duplication and drift
- lets users invoke the disciplines outside of a campaign
- aligns with the OpenSpec / Superpowers / Harness three-layer model for AI
  coding workflows

See `harness-engineering/docs/dedup-matrix.md` for the canonical mapping of
which skill owns which capability.

## Install

```bash
claude plugin marketplace add https://github.com/suntao2yl/claude-skill-discipline.git
claude plugin install harness-discipline@harness-discipline-marketplace
```

## License

MIT
