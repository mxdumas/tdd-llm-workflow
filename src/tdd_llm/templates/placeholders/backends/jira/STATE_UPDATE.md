**Updating state in Jira:**

Mark task as complete:
```bash
tdd-llm backend update-status {task_id} completed
```

Or use Jira status names directly:
```bash
tdd-llm backend update-status {task_id} Done
```

Set TDD phase (adds label like `tdd:test`):
```bash
tdd-llm backend set-phase {task_id} test
```

Valid phases: `analyze`, `test`, `dev`, `docs`, `review`

Set current task:
```bash
tdd-llm backend set-current {epic_id} {task_id}
```

The CLI commands update both Jira (status/labels) and local session state (`.tdd-state.local.json`).
