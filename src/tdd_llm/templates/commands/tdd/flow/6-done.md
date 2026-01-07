# /tdd:flow:6-done

Finalize task: state updates and archiving.

## Instructions

### 1. Load context

Read `.tdd-context.md` (lightweight).

Verify `.tdd-state.local.json`: `current.phase` must be "done".

### 2. Final verification

Run build and tests. If failure, fix first.

### 3. Update `docs/state.json`

{{STATE_UPDATE}}

Add completed task:

```json
{
  "epics": {
    "{epic_id}": {
      "status": "in_progress",
      "completed": [..., "{task_id}"]  // Add task
    }
  }
}
```

**If all epic tasks are completed:**
- Set `epics[{epic_id}].status` = "completed"

### 4. Reset `.tdd-state.local.json`

```json
{
  "current": {
    "epic": "{epic_id}",  // or next epic if finished
    "task": null,
    "phase": null
  }
}
```

### 5. Archive `.tdd-context.md`

{{ARCHIVE_CONTEXT}}

### 6. Enrich `.tdd-epic-context.md`

Read `.tdd-epic-context.md` and add/update:

**A. Status:**
```markdown
## Status
- Epic: {epic_id} | Completed tasks: [list]
- Last updated: {date} ({task_id})
```

**B. Architectural decisions** (if new):
```markdown
### AD-{N}: {Title} ({task_id})
- {Description}
- Reason: {Justification}
```

**C. Defined interfaces** (if new):
```markdown
### {InterfaceName} ({task_id})
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
## Done: {task_id} - Title

**PR:** #{N} - {URL}
**Epic {epic_id}:** [X]/[Y] tasks completed

**Next steps:**
1. Review/merge PR
2. `git checkout main && git pull`
3. `/tdd:flow:1-analyze` for next task
```

**If epic finished:**
```
## Epic {epic_id} completed

**Tasks:** All completed
**Next epic:** {next_epic_id} - {name}
```
