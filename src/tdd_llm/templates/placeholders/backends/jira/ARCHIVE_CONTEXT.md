**Archive context: Jira**

Archive the task context locally:
```bash
mkdir -p docs/tasks
cp .tdd-context.md docs/tasks/{task_id}-context.md
```

Optionally, add a completion summary as a Jira comment:
```bash
tdd-llm backend add-comment {task_id} "Task completed. Context archived to docs/tasks/{task_id}-context.md"
```

The archived context preserves the technical design decisions made during the task.
