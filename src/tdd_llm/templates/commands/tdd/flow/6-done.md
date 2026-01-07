# /tdd:flow:6-done

Finalize task: state updates and archiving.

## Instructions

### 1. Load context

Read `.tdd-context.md` (lightweight).

Verify `.tdd-state.local.json`: `current.phase` must be "done".

### 2. Update state

{{STATE_UPDATE}}

**In `docs/state.json`:**

```json
{
  "epics": {
    "{epic_id}": {
      "status": "in_progress",
      "completed": [..., "{task_id}"]
    }
  }
}
```

If all epic tasks completed: set `status` = "completed".

**Reset `.tdd-state.local.json`:**

```json
{
  "current": {
    "epic": "{epic_id}",
    "task": null,
    "phase": null
  }
}
```

### 3. Archive context

{{ARCHIVE_CONTEXT}}

Update `.tdd-epic-context.md` status:

```markdown
## Status
- Epic: {epic_id} | Completed: [task_list]
- Last updated: {date} ({task_id})
```

### 4. Commit state changes

```bash
git add docs/state.json .tdd-state.local.json .tdd-epic-context.md docs/epics/
git commit -m "{task_id}: finalize"
git push
```

### 5. Final report

```
## Done: {task_id} - Title

**PR:** #{N} - {URL}
**Epic {epic_id}:** [X]/[Y] tasks completed

**Next:** Merge PR, then `git checkout main && git pull`, then `/tdd:flow:1-analyze`
```

**If epic completed:**
```
## Epic {epic_id} completed

**Tasks:** All [N] completed
**Next epic:** {next_epic_id} - {name}
```
