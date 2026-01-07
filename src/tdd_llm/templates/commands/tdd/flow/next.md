# /tdd:flow:next

Automatically execute the next TDD flow step based on current phase.

## Instructions

### 1. Load state

Read in parallel:
- `docs/state.json` (global state: epics, completed tasks)
- `.tdd-state.local.json` (local state: current task, phase, skip_phases)

{{STATE_READ}}

If `docs/state.json` doesn't exist -> display:
```
Project not initialized. Run `/tdd:init:1-project` first.
```

If `.tdd-state.local.json` doesn't exist -> create with current epic.

### 2. Determine and execute next step

| Current phase | Action |
|---------------|--------|
| `null` | Execute `/tdd:flow:1-analyze` |
| `analyze` | Execute `/tdd:flow:1-analyze` (continue/finish) |
| `test` | Execute `/tdd:flow:2-test` |
| `dev` | Execute `/tdd:flow:3-dev` |
| `docs` | Execute `/tdd:flow:4-docs` |
| `review` | Execute `/tdd:flow:5-review` |
| `done` | Execute `/tdd:flow:6-done` |

**Note:** After `6-done`, phase resets to `null` for next task.

### 3. Execute command

Load and execute instructions from corresponding command.

## Notes

- `/tdd:flow:6-done` is included but can be skipped if user prefers manual finalization
- If epic finished, suggest moving to next
- Practical shortcut to avoid remembering which command to run
- All phases (except 1-analyze) use `.tdd-context.md` for context
