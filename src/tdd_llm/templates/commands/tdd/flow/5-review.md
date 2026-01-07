# /tdd:flow:5-review

Code review phase and PR creation.

## Instructions

### 1. Load context

Read `.tdd-context.md` (current task context).
Read `.tdd-epic-context.md` (epic context).
Verify `.tdd-state.local.json`: `current.phase` must be "review".

### 2. Build and tests

{{BUILD_TEST_CMD}}

If failure, fix first.

### 3. Verify coverage

{{COVERAGE_CMD}}

{{COVERAGE_THRESHOLDS}}

If coverage fails: add missing tests before continuing.

### 4. Commit and Push

```bash
git add .
git commit -m "$(cat <<'EOF'
{task_id}: {short task description}

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

git push -u origin {task_id}
```

### 5. Create PR

```bash
gh pr create --base main --title "{task_id}: {task title}" --body "$(cat <<'EOF'
## Summary

{Description of what the task accomplishes, from .tdd-context.md > Objective}

## Changes

{List of created/modified files}

## Test plan
- [x] Build passes
- [x] Tests pass
- [x] Coverage thresholds met

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 6. Code Review

**Ask user** if they want to run full code review:

> The `/code-review:code-review` plugin performs thorough PR analysis, but it's quite heavy.
> Do you want to use it?
> - **Yes**: For complex, critical changes or those touching multiple modules
> - **No**: For small tasks, simple fixes or minor refactoring

If user accepts, run:

```
/code-review:code-review
```

Fix identified issues. If corrections are made:

```bash
git add .
git commit --amend --no-edit
git push --force-with-lease
```

### 7. Update .tdd-context.md

Add section after `## Baseline`:

```markdown
### Final coverage
- Line: [X.X]% (baseline: [Y.Y]%, delta: [+/-Z.Z]%)
- Branch: [X.X]%
- Status: Thresholds met

### Review
- PR: #{N}
- Issues: [N] fixed
- Standards: Compliant
```

### 8. Finalize

Set `current.phase` = "done" in `.tdd-state.local.json`.

```
## REVIEW: {task_id} - Title

**Build:** OK
**Tests:** [N]/[N] passed
**Coverage:** [X.X]% (baseline: [Y.Y]%)
**PR:** #{N} created

Run `/tdd:flow:6-done` to finalize.
```
