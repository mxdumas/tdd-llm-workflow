**Epic source: Jira**

Use the MCP Jira server to fetch epic and story information:

```
Use the Jira MCP tool to:
1. Fetch epic details: GET /rest/api/3/issue/{EPIC_KEY}
2. Fetch stories: JQL search for issues linked to epic
3. Get story details including description, acceptance criteria
```

Map Jira fields to TDD context:
- Epic.summary -> Epic name
- Epic.description -> Epic objective
- Story.summary -> Task title
- Story.description -> Task description
- Story.acceptanceCriteria -> Completion criteria