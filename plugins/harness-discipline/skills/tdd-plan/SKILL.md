---
name: tdd-plan
description: "Test-first planner: produce JSON with test cases, implementation skeleton, and a real verification command. Use when seeding a harness-plan/harness-engineering contract, or when starting any feature where you want tests written before code."
compatibility: "Claude Code CLI and Claude.ai"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
metadata:
  author: suntao2yl
  version: 0.2.0
---

# /tdd-plan

Given a feature description or contract, produce a structured plan that lists tests **before** implementation. Output is machine-readable JSON so it can seed a contract directly.

## Hard invariants

1. Tests come before implementation. `test_cases` is non-empty.
2. Every test case names what is tested in plain language and gives a one-sentence rationale. No skeleton-only entries.
3. `verification_command` is a real, executable command running the tests you propose. No placeholders like `echo TODO`.
4. The plan doesn't write code or tests — it plans them. Implementation is downstream.
5. **Vertical-slice discipline.** This plan exists so the implementer can iterate one test ��� one impl → repeat. Do NOT encourage the caller to write all tests first then all impl — that produces tests of imagined behavior. See [REFERENCE.md](REFERENCE.md#vertical-slice).

## Inputs

- `/tdd-plan "<free-form description>"`
- `/tdd-plan --feature-id F003` — read `.harness/features.json`
- `/tdd-plan --contract <path>` — read existing contract

If none provided, ask once for the feature description.

## Workflow

1. **Detect framework** via Glob/Grep on existing patterns (`tests/**`, `*_test.py`, `*.test.ts`, `pytest.ini`, `package.json::scripts.test`, etc.). Test command must use the framework already present, not a new one.
2. **Enumerate test cases** (3-8 total). Cover happy path (1-2), edge cases (1-3: empty/large/unicode/concurrent), failure paths (1-3: invalid input, missing dep, permission denied). Skip categories that don't apply. Don't pad — fewer real cases beats more shallow ones.
3. **Sketch implementation skeleton.** For each new file the impl will likely create or modify: path, one-sentence purpose, key function/type signatures (no bodies). Don't sketch what already exists — read relevant files first.
4. **Produce verification_command.** A single shell command (or `;`-chained commands) that runs the proposed tests. Should pass once implementation is complete, and only then.
5. **Output JSON to stdout.** No prose around it. Schema and example: [REFERENCE.md](REFERENCE.md#output-schema).

## Anti-patterns

- No rationale-less test cases. Downstream contract validators reject them.
- Don't pick a framework absent from the project. If no tests exist, output `framework_detected: null` and emit a single smoke test using whatever runner the user can install easily.
- No implementation code in the skeleton — signatures only.
- Don't read full files to plan tests — Grep for symbols and read relevant slices.

## When called by harness-plan or harness-engineering

The caller pipes your JSON into a contract or design spec. Requirements:

1. JSON valid (parseable, no trailing prose).
2. `verification_command` exit-codes 0 only when all proposed tests pass.

If you can't satisfy either, return `{"error": "<reason>"}` — caller stops.

## Composes with

- `tdd` — the philosophy / red-green-refactor loop the plan feeds into.
- `completion-verify` — runs the `verification_command` you produce.
- `change-spec` — when the plan should be split across change units.

See [REFERENCE.md](REFERENCE.md), `resources/tdd-plan-template.md`.
