# Code anti-patterns: when changes go wrong

Concrete before/after pairs for the four most common ways change scope balloons.
Keep specs *surgical* — every changed line should trace to the change's stated
goal. Patterns adapted from
[karpathy-guidelines](https://github.com/forrestchang/andrej-karpathy-skills)
(MIT), distilled and aligned to the change-spec workflow.

Use this file when:
- Authoring a change-spec and tempted to expand scope
- Reviewing a diff that "fixes the bug" but touches 12 files
- Triaging whether a "small refactor" is really one CHG or six

---

## 1. Hidden assumptions (Think before coding)

**Symptom:** Spec says "export user data" — implementation silently picks JSON,
all-users, all-fields, file-on-disk.

**Bad spec:**
```
Goal: Export users to file.
Implementation: write users.json with all fields.
```

**Surgical spec:**
```
Goal: Export the *active* user subset (status='active') as JSON,
returned by GET /users/export. Out of scope: CSV, file-on-disk,
soft-deleted users, PII redaction.
Open questions: which fields are PII-sensitive? (caller decides before merge)
```

**Rule:** If the description allows >1 interpretation, the spec must pin one
*and* list the rejected ones in `Out of scope`. Silent picks rot under review.

---

## 2. Speculative complexity (Simplicity first)

**Symptom:** "Add a discount calculator" produces `DiscountStrategy` ABC,
`PercentageDiscount` / `FixedDiscount` subclasses, `DiscountConfig` dataclass,
`DiscountCalculator` orchestrator. 200 lines for a one-line multiply.

**Bad interface signature:**
```
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: ...
```

**Surgical interface:**
```
def calculate_discount(amount: float, percent: float) -> float
```

**Rule:** A change-spec interface section that introduces an abstract base
class, a registry, a config object, or a `Manager` for a single concrete need
is over-spec'd. Refuse and split: write the concrete CHG now, file an "open
question" CHG for the second case when it appears.

Test: "Could a senior engineer collapse this to one function?" If yes, do that.

---

## 3. Drive-by refactoring (Surgical changes)

**Symptom:** CHG-014 says *"fix empty-email crash in validator"*. Diff:
adds docstring, adds type hints, tightens email regex, adds username length
check, switches `'` → `"`.

**Bad diff:**
```diff
- def validate_user(user_data):
+ def validate_user(user_data: dict) -> bool:
+     """Validate user data."""
+     email = user_data.get('email', '').strip()
+     if not email:
          raise ValueError("Email required")
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:
          raise ValueError("Invalid email")
+     if len(user_data.get('username', '')) < 3:
+         raise ValueError("Username too short")
```

**Surgical diff (only the bug):**
```diff
  def validate_user(user_data):
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
```

**Rule:** Every changed line traces to a `Pre/Post condition` in the spec.
Lines that don't are scope creep — strip them out, file a separate CHG if they
matter. This is the canonical Surgical-Changes test for downstream review.

Stylistic drift (quotes, type hints, formatting) inside an unrelated CHG is
*always* defect-tier feedback — even if the new style is "better." Match the
surrounding file.

---

## 4. Vague success criteria (Goal-driven execution)

**Symptom:** Spec says "fix authentication". Three days later, six PRs, no
clear "done" condition.

**Bad pre/post:**
```
Pre:  Auth is broken.
Post: Auth works.
```

**Surgical pre/post:**
```
Pre:  test_password_change_invalidates_old_session FAILS — the existing
      session cookie remains valid after POST /password/change.
Post: That test passes; the full auth suite (15 tests) is still green.
```

**Rule:** Pre- and post-conditions in a spec are testable strings — usually a
specific test name or a `curl` invocation with expected status code. If you
can't write one, the change is too vague to spec; refine the goal first.

This is what `/tdd-plan` is for: it produces the failing test that *becomes*
the pre-condition.

---

## Quick checklist for spec authors

Before declaring a change-spec ready:

- [ ] Goal pins one interpretation; alternatives moved to `Out of scope`.
- [ ] Interface introduces zero abstractions that lack a second concrete user.
- [ ] Pre/post conditions name a specific failing test or observable signal.
- [ ] Test list contains *only* tests that fail before and pass after.
- [ ] Diff preview (mental or real) has no stylistic / unrelated changes.

Fail any of these → split the change or rewrite the spec. Don't proceed.
