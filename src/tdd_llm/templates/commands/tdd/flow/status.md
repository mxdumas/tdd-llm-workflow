# /tdd:flow:status

Display current TDD project state: current epic, task, phase, progress.

## Instructions

### 1. Load state

Read in parallel:
- `docs/state.json` (global state: epics, completed tasks)
- `.tdd-state.local.json` (local state: current task, phase, skip_phases)

{{STATE_READ}}

If `docs/state.json` doesn't exist -> display:
```
## Project not initialized

No `docs/state.json` file found.

Run `/tdd:init:1-project` to initialize the project.
```

If `.tdd-state.local.json` doesn't exist -> create with:
```json
{
  "current": {
    "epic": "{first in_progress or not_started epic}",
    "task": null,
    "phase": null
  }
}
```

### 2. Load context

Read in parallel (if exists):
- `.tdd-context.md`
- `.tdd-epic-context.md`

### 3. Display status

```bash
git branch --show-current  # Show current branch
```

```
## TDD Status

**Epic:** {epic_id} - {Epic name}
**Task:** {task_id} - {Name} | No task in progress
**Branch:** {task_id} | main
**Phase:** {phase} | Ready for /tdd:flow:1-analyze

### {epic_id} Progress

{ASCII progress bar}
{completed}/{total} tasks ({percentage}%)

Completed: {list}
Remaining: {list}

### Global Progress

| Epic | Name | Status | Progress |
|------|------|--------|----------|
| {epic_id} | {Name} | in_progress | X/Y |
| ... | ... | ... | ... |

### Next action

{Suggestion based on current phase}
```

### 4. Suggestions by phase

| Current phase | Suggestion |
|---------------|------------|
| `null` | Run `/tdd:flow:1-analyze` to start next task |
| `analyze` | Continue analysis or run `/tdd:flow:1-analyze` |
| `test` | Run `/tdd:flow:2-test` to write tests |
| `dev` | Run `/tdd:flow:3-dev` to implement |
| `docs` | Run `/tdd:flow:4-docs` to document |
| `review` | Run `/tdd:flow:5-review` to validate and create PR |
| `done` | Run `/tdd:flow:6-done` to finalize |

### 5. Show current task info (if applicable)

If `.tdd-context.md` exists and a task is in progress:

```
### Current task: {task_id} - {Title}

**Objective:** {objective summary}

**Files:**
- Tests: {list of test files}
- Code: {list of files to create/modify}
```

### 6. Show epic context (if applicable)

If `.tdd-epic-context.md` exists:

```
### Epic {epic_id} Context

**Architectural decisions:** {N} decisions
**Defined interfaces:** {list of interface names}
**Established patterns:** {short list}

Last updated: {date} ({task_id})
```

## Progress bar format

```
[========--------] 50%
[================] 100%
[----------------] 0%
```

16 characters, = for completed, - for remaining.

## Notes

- This command is read-only (doesn't modify anything)
- Useful for resuming work after a break
- Can be run at any time
