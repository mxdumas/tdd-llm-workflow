# /tdd:flow:5-review

Code review and PR creation.

## Instructions

### 1. Load context

Read `.tdd-context.md` and `.tdd-epic-context.md`.
Verify `.tdd-state.local.json`: `current.phase` must be "review".

### 2. Build and tests

Run build and tests. Fix any failures before continuing.

### 3. Verify coverage

Run coverage (command from `docs/dev/standards.md`).
Ensure thresholds are met. If not, add missing tests first.

### 4. Commit and Push

Commit all changes: `{task_id}: {short description}`
Push to origin on current branch.

### 5. Create PR

Create PR with `gh pr create`:
- Title: `{task_id}: {task title}`
- Summary: objective from `.tdd-context.md`
- Changes: list of created/modified files
- Test plan: build, tests, coverage status

### 6. Code review (optional)

If a code review plugin is available (e.g., `/code-review:code-review`), **ask user** if they want to run it:
- **Yes**: For complex changes or those touching multiple modules
- **No**: For small tasks or minor refactoring

Fix any identified issues, amend commit, and force-push.

### 7. Update .tdd-context.md

Add after `## Baseline`:
- Final coverage (line %, delta from baseline)
- PR number
- Review issues fixed (if code review ran)

### 8. Finalize

Set `current.phase` = "done" in `.tdd-state.local.json`.

```
## REVIEW: {task_id} - Title

**Build:** OK
**Tests:** [N]/[N] passed
**Coverage:** [X.X]% (baseline: [Y.Y]%)
**PR:** #{N}

Run `/tdd:flow:6-done` to finalize.
```
