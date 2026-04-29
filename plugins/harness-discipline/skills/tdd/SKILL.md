---
name: tdd
description: "Test-driven development with red-green-refactor in vertical slices. Use when user wants TDD, mentions red-green-refactor, asks for test-first development, or wants integration tests that survive refactors."
compatibility: "Claude Code CLI and Claude.ai"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
metadata:
  author: suntao2yl (adapted from mattpocock/skills)
  version: 0.1.0
  upstream: https://github.com/mattpocock/skills/tree/master/tdd
---

# /tdd

## Philosophy

**Tests verify behavior through public interfaces, not implementation details.** Code can change entirely; tests shouldn't.

- **Good test** = integration-style, exercises real code paths through public APIs, reads like a spec, survives refactors. See [tests.md](tests.md).
- **Bad test** = mocks internal collaborators, asserts call counts, breaks on rename. Warning sign: refactor breaks the test, behavior unchanged.

See [mocking.md](mocking.md) for what to mock and what not to.

## Anti-Pattern: horizontal slices

**DO NOT write all tests first, then all implementation.**

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

Bulk-written tests test *imagined* behavior — they pass when behavior breaks and fail when behavior is fine. Tracer-bullet one test at a time so each test responds to what you learned from the previous cycle.

## Workflow

### 1. Plan

- [ ] Confirm public interface with user
- [ ] List behaviors to test (not implementation steps); prioritize critical paths
- [ ] Look for [deep module](deep-modules.md) opportunities
- [ ] Design for [testability](interface-design.md)
- [ ] Get user approval

You can't test everything. Confirm which behaviors matter most.

### 2. Tracer bullet

```
RED:   one test for first behavior → fails
GREEN: minimal code to pass → passes
```

This proves the path works end-to-end.

### 3. Incremental loop

For each remaining behavior:

```
RED:   next test → fails
GREEN: minimal code → passes
```

Rules: one test at a time, only enough code to pass current test, no anticipation, observable behavior only.

### 4. Refactor

After GREEN, look for [refactor candidates](refactoring.md): extract duplication, deepen modules (move complexity behind simple interfaces), apply SOLID where natural. Run tests after each step. **Never refactor while RED.**

## Composes with

- `tdd-plan` — produces the per-feature contract this skill iterates on
- `completion-verify` — gates each GREEN with the contract's verification commands
- `change-spec` — when the work spans multiple change units
