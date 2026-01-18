# /tdd:backend:comments

Read or add comments on a story.

## Usage

```
/tdd:backend:comments <task_id> [comment]
```

## Instructions

{{LIST_COMMENTS}}

### Display format

```
## Comments on {task_id}

**John Doe** - Jan 15, 2024 10:30
> Comment text here

**Jane Smith** - Jan 16, 2024 14:20
> Another comment
```

## Workflow

1. If no comment argument provided, list existing comments
2. If comment argument provided, add the comment then list all comments
