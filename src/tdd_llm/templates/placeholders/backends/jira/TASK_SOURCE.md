**Task source: Jira**

Use the MCP Jira server to fetch story details:

```
Use the Jira MCP tool to:
1. Fetch story: GET /rest/api/3/issue/{STORY_KEY}
2. Extract: summary, description, acceptance criteria
```

Task identification:
- epic_id: Jira epic key (e.g., `PROJ-100`)
- task_id: Jira story key (e.g., `PROJ-1234`)

Map Jira fields:
- `summary` → Task title
- `description` → Task description / requirements
- `acceptanceCriteria` or `customfield_*` → Completion criteria
