# /tdd:backend:labels

Manage labels on a story.

## Usage

```
/tdd:backend:labels <task_id>
```

## Instructions

### 1. Get current labels

```bash
tdd-llm backend get-task {task_id}
```

Show current labels from the response.

### 2. Modify labels

{{UPDATE_LABELS}}

### 3. Confirm changes

```bash
tdd-llm backend get-task {task_id}
```

Show updated labels.

## Common labels

| Label | Purpose |
|-------|---------|
| `bug` | Bug fix |
| `feature` | New feature |
| `urgent` | High priority |
| `blocked` | Blocked by dependency |
| `needs-review` | Ready for review |
| `reviewed` | Review completed |
