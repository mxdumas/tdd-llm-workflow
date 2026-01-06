# /tdd:flow:status

Display current TDD project state: current epic, task, phase, progress.

## Instructions

### 1. Load state

Read in parallel:
- `docs/state.json` (global state: epics, completed tasks)
- `.tdd-state.local.json` (local state: current task, phase)

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
    "epic": "E{last in_progress or first not_started epic}",
    "task": null,
    "phase": null
  }
}
```

### 2. Load context

Read in parallel:
- Current epic file (`docs/epics/E{N}.md`)
- `.tdd-context.md` (if exists)
- `.tdd-epic-context.md` (if exists)

### 3. Display status

```bash
git branch --show-current  # Show current branch
```

```
## TDD Status

**Epic:** E{N} - {Epic name}
**Task:** {T{M} - {Name} | No task in progress}
**Branch:** {e{N}-t{M} | main}
**Phase:** {phase | Ready for /tdd:flow:1-analyze}

### E{N} Progress

{ASCII progress bar}
{completed}/{total} tasks ({percentage}%)

Completed: {list T1, T2, ...}
Remaining: {list T3, T4, ...}

### Global Progress

| Epic | Name | Status | Progress |
|------|------|--------|----------|
| E0 | Foundation | completed | 3/3 |
| E1 | {Name} | in_progress | 2/5 |
| E2 | {Name} | not_started | 0/4 |
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

### 5. Show current task info (if applicable)

If `.tdd-context.md` exists and a task is in progress:

```
### Current task: T{M} - {Title}

**Objective:** {objective summary}

**Files:**
- Tests: {list of test files}
- Code: {list of files to create/modify}
```

### 6. Show epic context (if applicable)

If `.tdd-epic-context.md` exists:

```
### Epic E{N} Context

**Architectural decisions:** {N} decisions
**Defined interfaces:** {list of interface names}
**Established patterns:** {short list}

Last updated: {date} (T{M})
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
