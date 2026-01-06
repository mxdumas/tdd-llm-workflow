# /tdd:flow:next

Automatically execute the next TDD flow step based on current phase.

## Instructions

### 1. Load state

Read in parallel:
- `docs/state.json` (global state: epics, completed tasks)
- `.tdd-state.local.json` (local state: current task, phase)

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

**Note:** After `review`, phase stays `review` until `/tdd:flow:6-done` is run manually (finalization = explicit action).

### 3. Execute command

Load and execute instructions from corresponding command.

## Notes

- `/tdd:flow:6-done` is never called automatically (commit = user decision)
- If epic finished, suggest moving to next
- Practical shortcut to avoid remembering which command to run
- All phases (except 1-analyze) use `.tdd-context.md` for context
