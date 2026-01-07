# /tdd:flow:3-dev

Senior Developer. Make tests pass simply (GREEN phase).
Clean code from the start. Simple != ugly. Minimal = no superfluous.

## Instructions

### 1. Load context

Read `.tdd-context.md`, `.tdd-epic-context.md`, `docs/dev/standards.md`.

Verify `.tdd-state.local.json`: `current.phase` must be "dev".

### 2. Implement

**Scope = `.tdd-context.md`** (files + design), not just what's tested.
Tests validate, they don't limit. Implement UI, CSS, refactors even without tests.

**Order:**
1. Create files listed in `Files > Create` (code, not tests)
2. Modify files in `Modify`
3. Follow `Design > Logic`

**Do:** Clean code, clear names, follow patterns from context.

**Don't:** Features not in context. Premature optimization. Over-engineering.

### 3. Make tests pass

Run tests. **Iterate** until 100% pass. Fix implementation, not tests.

### 4. Update .tdd-context.md

Add after `## Design`:

```markdown
### GREEN Result
- Tests: [N]/[N] passed
- Build: OK
- Notes: [Any deviation from plan, or "None"]
```

### 5. Finalize

Determine next phase (check `skip_phases` in `.tdd-state.local.json`):
- If `4-docs` not skipped → set `current.phase` = "docs"
- Else → set `current.phase` = "review"

```
## GREEN: {task_id} - Title

**Tests:** [N]/[N] passed

Run `/tdd:flow:4-docs` to document.
     Or `/tdd:flow:5-review` if docs phase skipped.
```

## When to stop and ask

**STOP and ask user if:**
- 3+ failed attempts on same test
- Need to modify a test to pass
- Need files not listed in `.tdd-context.md`
- Two tests contradict each other
- Test assumptions don't match reality (wrong signature, impossible state)
- Circular dependency discovered
- Scope creep: implementation growing beyond context

**Do NOT:**
- Loop indefinitely trying approaches
- Modify tests to make them pass
- Add files/features outside scope
- Assume and proceed when uncertain
