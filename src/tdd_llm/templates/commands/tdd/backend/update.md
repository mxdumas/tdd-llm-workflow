# /tdd:backend:update

Update a story's title, description, or acceptance criteria.

## Usage

```
/tdd:backend:update <task_id>
```

## Instructions

### 1. Get current story details

```bash
tdd-llm backend get-task {task_id}
```

### 2. Ask what to update

Ask user which fields to update:
- Title
- Description
- Acceptance criteria

### 3. Update the story

{{UPDATE_STORY}}

### 4. Confirm update

```bash
tdd-llm backend get-task {task_id}
```

Show the updated story to confirm changes.
