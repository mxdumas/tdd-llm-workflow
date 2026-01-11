# /tdd:flow:5-review

Code review and PR creation.

## Instructions

### 1. Load context

Read `.tdd-context.md` and `.tdd-epic-context.md`.
Verify `.tdd-state.local.json`: `current.phase` must be "review".

### 2. Verify scope completion

Review the **Scope** section in `.tdd-context.md` and verify each item:
- Check that every scope item has been implemented
- For each item, identify the file(s) and test(s) that implement it

Present a checklist:
```
## Scope Verification

- [x] Item 1: implemented in `file.py`, tested in `test_file.py`
- [x] Item 2: implemented in `other.py`, tested in `test_other.py`
- [ ] Item 3: NOT IMPLEMENTED - missing XYZ
```

If any item is unchecked, **STOP**, inform the user, and return to `/tdd:flow:3-dev` to complete implementation.

### 3. Build and tests

Run build and tests. Fix any failures before continuing.

### 4. Verify coverage

Run coverage (command from `docs/dev/standards.md`).

{{COVERAGE_THRESHOLDS}}

If not met, add missing tests first.

### 5. Commit and Push

Commit all changes: `{task_id}: {short description}`
Push to origin on current branch.

### 6. Create PR

Create PR with `gh pr create`:
- Title: `{task_id}: {task title}`
- Summary: objective from `.tdd-context.md`
- Changes: list of created/modified files
- Test plan: build, tests, coverage status

### 7. Code review (optional)

If a code review plugin is available (e.g., `/code-review:code-review`), **ask user** if they want to run it:
- **Yes**: For complex changes or those touching multiple modules
- **No**: For small tasks or minor refactoring

Fix any identified issues, amend commit, and force-push.

### 8. Update .tdd-context.md

Add after `## Baseline`:
- Final coverage (line %, delta from baseline)
- PR number
- Review issues fixed (if code review ran)

### 9. Finalize

Set `current.phase` = "done" in `.tdd-state.local.json`.

```
## REVIEW: {task_id} - Title

**Build:** OK
**Tests:** [N]/[N] passed
**Coverage:** [X.X]% (baseline: [Y.Y]%)
**PR:** #{N}

Run `/tdd:flow:6-done` to finalize.
```
