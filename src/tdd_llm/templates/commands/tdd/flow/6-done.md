# /tdd:flow:6-done

Finalize task: state updates and archiving.

## Instructions

### 1. Load context

Read `.tdd-context.md` (lightweight).

Verify `.tdd-state.local.json`: `current.phase` must be "review".

### 2. Final verification

{{BUILD_TEST_CMD}}

If failure: don't continue, fix first.

### 3. Update `docs/state.json`

{{STATE_UPDATE}}

Add completed task:

```json
{
  "epics": {
    "E{N}": {
      "status": "in_progress",
      "completed": ["T1", "T2", "T3", "T{M}"]  // Add task
    }
  }
}
```

**If all epic tasks are completed:**
- Set `epics[E{N}].status` = "completed"

### 4. Reset `.tdd-state.local.json`

```json
{
  "current": {
    "epic": "E{N}",  // or E{N+1} if epic finished
    "task": null,
    "phase": null
  }
}
```

### 5. Archive `.tdd-context.md`

Copy `.tdd-context.md` to `docs/epics/E{N}/T{M}-context.md`

### 6. Enrich `.tdd-epic-context.md`

Read `.tdd-epic-context.md` and add/update:

**A. Status:**
```markdown
## Status
- Epic: E{N} | Tasks: T1, T2, T{M}
- Last updated: {date} (T{M})
```

**B. Architectural decisions** (if new):
```markdown
### AD-{N}: {Title} (T{M})
- {Description}
- Reason: {Justification}
```

**C. Defined interfaces** (if new):
```markdown
### {InterfaceName} (T{M})
{Interface definition}
```

### 7. Commit and push

```bash
git add .
git commit --amend --no-edit
git push --force-with-lease
```

### 8. Final report

```
## Done: [E{N}] T{M} - Title

**PR:** #{N} - {URL}
**Epic E{N}:** [X]/[Y] tasks completed

**Next steps:**
1. Review/merge PR
2. `git checkout main && git pull`
3. `/tdd:flow:1-analyze` for T{M+1}
```

**If epic finished:**
```
## Epic E{N} completed

**Tasks:** T1-T{X} (all completed)
**Next epic:** E{N+1} - {name}
```
