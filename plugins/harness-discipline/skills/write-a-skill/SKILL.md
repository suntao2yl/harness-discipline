---
name: write-a-skill
description: "Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill, or refactor an existing skill that has grown too large."
compatibility: "Claude Code CLI and Claude.ai"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
metadata:
  author: suntao2yl (adapted from mattpocock/skills)
  version: 0.1.0
  upstream: https://github.com/mattpocock/skills/tree/master/write-a-skill
---

# /write-a-skill

## Process

1. **Gather requirements** — ask:
   - What task / domain does the skill cover?
   - What specific use cases?
   - Needs scripts, or just instructions?
   - Reference materials to bundle?

2. **Draft** — create:
   - `SKILL.md` (concise, ≤100 lines)
   - `REFERENCE.md` / `EXAMPLES.md` if content > 100 lines
   - `scripts/` if deterministic operations are needed

3. **Review with user** — coverage, gaps, level of detail.

## Skill structure

```
skill-name/
├── SKILL.md           # Main instructions (required, ≤100 lines)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md template

```md
---
name: skill-name
description: Brief capability sentence. Use when [specific triggers].
compatibility: "Claude Code CLI and Claude.ai"
allowed-tools: [...]
metadata:
  author: ...
  version: 0.1.0
---

# Skill Name

## Quick start
[Minimal working example]

## Workflow
[Step-by-step with checklists]

## Advanced
See [REFERENCE.md](REFERENCE.md).
```

## Description rules

The description is **the only thing the agent sees** when deciding which skill to load — surfaced in the system prompt alongside every other installed skill. Every word costs tokens on every conversation.

**Goal**: agent knows (1) what capability and (2) when to trigger.

**Format**: ≤1024 chars (target ~250); third person; first sentence = what; second sentence = `Use when [specific triggers]`.

**Good**: `Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.`

**Bad**: `Helps with documents.`

## When to add scripts

Add a script when:

- Operation is deterministic (validation, formatting, parsing)
- Same code would otherwise be regenerated repeatedly
- Errors need explicit handling

Scripts save tokens and improve reliability vs. generated code.

## When to split files

Split into separate files when:

- `SKILL.md` exceeds 100 lines
- Content has distinct domains
- Advanced features are rarely needed (progressive disclosure)

## Review checklist

- [ ] Description includes triggers ("Use when ...")
- [ ] `SKILL.md` ≤ 100 lines
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples included
- [ ] References one level deep (no chains of chains)
