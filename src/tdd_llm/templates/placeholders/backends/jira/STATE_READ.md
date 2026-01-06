**Loading state from Jira:**

Use the MCP Jira server to fetch epic and story status:

```
Use the Jira MCP tool to:
1. Get current epic status (JQL: project = {PROJECT} AND issuetype = Epic AND status != Done)
2. Get stories in current epic (JQL: "Epic Link" = {EPIC_KEY})
3. Determine next story to work on (first story with status = "To Do" or "In Progress")
```

If no active epic found -> display:
```
No active epic found in Jira. Create an epic first or check project configuration.
```

Store current task context in `.tdd-state.local.json` for session continuity.