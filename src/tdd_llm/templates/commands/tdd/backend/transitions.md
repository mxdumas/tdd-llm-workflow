# /tdd:backend:transitions

Show available status transitions for a story.

## Usage

```
/tdd:backend:transitions <task_id>
```

## Instructions

### 1. Get current status

```bash
tdd-llm backend get-task {task_id}
```

### 2. Get available transitions

{{GET_TRANSITIONS}}

### 3. Display transitions

```
## Status transitions for {task_id}

**Current status:** To Do

**Available transitions:**
- Start Progress → In Progress
- Done → Done
```

### 4. Offer to transition (optional)

Ask user if they want to transition to one of the available statuses.

If yes:
```bash
tdd-llm backend update-status {task_id} {tdd_status}
```

Where `{tdd_status}` is one of: `not_started`, `in_progress`, `completed`
