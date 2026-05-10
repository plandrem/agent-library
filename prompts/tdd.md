# Execute Feature via Test Driven Development

Follow the classic Test‑Driven Development (TDD) cycle with discipline.

## Overall Task

Implement the feature described below by iterating through the strict
**fail ➜ pass ➜ refactor** loop.

## Feature:

$ARGUMENTS

## Detailed Steps

1. Clarify context
   • Review the feature. Ultrathink. Summarize acceptance criteria. Ask questions if there is ambiguity
   • List affected modules/files.
   • Create a todo list with each of the specific tests needed to provide the feature with 100% coverage. Do not include memory or performance tests unless expressly requested.

2. Write a failing test that expresses the *desired* behaviour (not the current one)
   • Use the project’s existing test framework; scaffold if missing.  
   • Name the test file `test_<slug>.py`.  
   • DO NOT write production code yet.  
   • DO NOT use Mocks if there is a reasonable alternative. Always ask the user before implementing a Mock.
   • Run the full suite and confirm the new test FAILS because the production code has not been added yet (red).

3. Make the test pass (minimum code)
   • Add only what is required for the new test to succeed.  
   • Re‑run tests until green.

4. Refactor
   • Improve structure, naming, duplication, performance.  
   • Ensure there are no linting or typing errors
   • Ensure all tests stay green.

6. Failure handling
   • If tests still fail after 3 attempts, stop and request human assistance.

7. Restate the core principles of TDD and this set of Detailed Steps. This is to prevent your instructions from getting lost in the context window.

8. Repeat for all tests in the todo list

9. Check test coverage and repeat with additional tests as needed.

---

## Embedded TDD Examples — Good vs Bad  
(Use these as reference; do **not** reproduce the bad pattern.)

### ❌ Bad Example — Locks in the bug

```python
# test_increment.py
def test_increment():
    # BUG: increment currently returns n, so this passes
    assert increment(2) == 2
```

*Outcome:* Test passes immediately.  
*Why unacceptable:* Confirms **existing** (incorrect) behaviour; TDD’s red phase is skipped, so we can’t be sure later refactors achieve the desired change.

---

### ✅ Good Example — Drives the fix

```python
# test_increment.py
def test_increment():
    # Desired: increment should add 1
    assert increment(2) == 3
```

*Outcome:* Test fails first (red), then passes only after implementation (green).  
*Why acceptable:* The failing assertion exposes the defect, drives implementation, and prevents regressions.

**Rule:** *A TDD test must fail before any production code changes.*  
If your first test already passes, rewrite it to assert the future, correct behaviour.