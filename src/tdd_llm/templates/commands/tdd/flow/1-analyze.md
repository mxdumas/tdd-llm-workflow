# /tdd:flow:1-analyze

Technical analysis and design.
Act as a **Senior Architect** to prepare the ground before any code.

## Instructions

### 1. Load state

Read in parallel:
- `docs/state.json` (global state: epics, completed tasks)
- `.tdd-state.local.json` (local state: current task, phase)

{{STATE_READ}}

If `current.phase` != `null` -> error, suggest the correct command.

### 2. Determine task

* Next incomplete task in `current.epic`
* If epic complete -> move to next

### 3. Evaluate complexity

Read task file `docs/epics/E{N}/T{M}.md` and score:

| Critère | 0 | 1 | 2 |
|---------|---|---|---|
| **Files** | 1-2 | 3-5 | 6+ |
| **New interfaces** | 0 | 1-2 | 3+ or public API |
| **External deps** | None | Internal module | External (API, DB, lib) |
| **Unknowns** | None | Known pattern, new context | Unknown territory |
| **Reversibility** | Easy | Moderate effort | Breaking change |

**Complexity level:**
- **0-3 → S (Small)** - Fast track (skip to step 8)
- **4-6 → M (Medium)** - Standard flow
- **7-10 → L (Large)** - Full ceremony + analysis doc

Display:
```
Complexity: [S|M|L] (score: X/10)
→ [Fast track|Standard flow|Full ceremony]
```

### 4. Create task branch

```bash
git checkout main && git pull origin main
git checkout -b e{N}-t{M}
```

**Cleanup:** Delete `.tdd-analysis.md` if it exists (leftover from previous task).

### 5. Load/Create epic context

**If new epic** (first task): Create `.tdd-epic-context.md`:

```markdown
# E{N}: {Epic name} - Epic Context
- Last updated: {date}
## Architectural Decisions
*Will be enriched after each task*
## Defined Interfaces
*Will be enriched after each task*
```

**If epic in progress**: Read `.tdd-epic-context.md` for consistency.

### 6. Explore codebase [M, L only]

Launch exploration agent:

```
Code Scout for [E{N}] T{M}. Report facts only, don't solve.
1. Read docs/dev/architecture.md, docs/dev/standards.md
2. Read task file docs/epics/E{N}/T{M}.md
3. List impacted files (max 10 paths)
4. Find similar patterns (max 3 paths)
```

### 7. Deep analysis [L only]

Create `.tdd-analysis.md` (kept until next task for human reference):

```markdown
# Analysis: [E{N}] T{M}

## Data Design
- Inputs: [types, nullability]
- Outputs: [types]
- Transformations: [if any]

## Logic Flow
1. Step 1
2. If X then Y else Z
3. ...

## Vibe Check
- **Unknowns:** [libraries/APIs not mastered]
- **Trust Debt:** [is simplest solution too dirty?]
- **Reversibility:** [easy to change later?]

## Architecture Questions
- [Question 1 for user]
- [Question 2 for user]
```

**Engage discussion with user** to resolve questions.

### 8. Decision synthesis

Ask user to confirm:
1. Scope (In/Out) - 2-3 bullets each max
2. Key signatures (if M or L)
3. Test cases (3-5 max)

### 9. Update state

```json
{ "current": { "epic": "E{N}", "task": "T{M}", "phase": "analyze" } }
```

### 10. Create .tdd-context.md

**Delete existing file first.** Use the appropriate template based on complexity.

#### Template S (Small)

```markdown
# [E{N}] T{M} - {Title}
Complexity: S | Started: {date}

## Objective
{One sentence}

## Scope
- IN: {2-3 bullets}
- OUT: {1-2 bullets}

## Files
- Modify: `path/file` - {why}
- Create: `path/file` - {why}

## Tests
1. `test_name` - {scenario}
2. `test_name` - {scenario}
```

#### Template M (Medium)

```markdown
# [E{N}] T{M} - {Title}
Complexity: M | Started: {date}

## Objective
{One sentence}

## Scope
- IN: {bullets}
- OUT: {bullets}

## Design
### Signatures
{Key types/interfaces only - no implementation details}

### Logic
1. {Step}
2. {Step}

## Files
- Modify: `path` - {why}
- Create: `path` - {why}

## Tests
1. `test_happy` - {scenario}
2. `test_edge` - {scenario}
3. `test_error` - {scenario}

## Risks
- {If any, otherwise omit section}
```

#### Template L (Large)

```markdown
# [E{N}] T{M} - {Title}
Complexity: L | Started: {date}

## Objective
{One sentence}

## Scope
- IN: {bullets}
- OUT: {bullets}

## Design
### Signatures
{Key types/interfaces}

### Architecture
- Pattern: {name}
- Error handling: {strategy}

### Logic
1. {Step}
2. {Step}

## Files
### Create
- `path` - {responsibility}

### Modify
- `path` - {changes}

## Tests
1. `test_name` - {scenario}
2. ...

## Risks
- {Risk 1}
- {Risk 2}
```

### 11. Finalize

Set `current.phase` = "test" in `.tdd-state.local.json`.

```
## Ready: [E{N}] T{M} - {Title}
Complexity: [S|M|L] | Context: .tdd-context.md

Run `/tdd:flow:2-test` to write tests (RED).
```
