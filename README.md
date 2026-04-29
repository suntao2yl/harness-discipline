# harness-discipline

[English](README.md) | [中文](README.zh-CN.md)

Three reusable discipline skills for AI-driven software engineering, designed
to be composed into larger lifecycle harnesses (`harness-plan`,
`harness-engineering`) or used standalone.

## Skills

| Slash command       | Purpose                                                       |
| ------------------- | ------------------------------------------------------------- |
| `/tdd-plan`         | Test-first plan: test cases + implementation skeleton         |
| `/completion-verify`| Run a contract's verification commands and produce JSON verdict |
| `/change-spec`      | Generate a mini-RFC for a change unit (CHG-NNN)               |

Each skill is independent, has its own SKILL.md, and can be invoked without
loading the others — load on demand.

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
