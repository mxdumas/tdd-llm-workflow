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

### 3. Evaluate complexity and type

Read task file `docs/epics/E{N}/T{M}.md`.

**Determine task type from content/title:**
- `feature` - New functionality (default)
- `bugfix` - Fix existing behavior
- `refactor` - Restructure without behavior change
- `test` - Add/improve tests only
- `doc` - Documentation only
- `config` - Configuration, CI/CD, tooling
- `chore` - Maintenance, dependencies, cleanup

**Applicable phases by type:**

| Type | test | dev | refactor |
|------|:----:|:---:|:--------:|
| feature | yes | yes | yes |
| bugfix | yes | yes | yes |
| refactor | yes | yes | yes |
| test | - | yes | - |
| doc | - | - | - |
| config | - | yes | - |
| chore | - | yes | - |

**Score complexity:**

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| **Files** | 1-2 | 3-5 | 6+ |
| **New interfaces** | 0 | 1-2 | 3+ or public API |
| **External deps** | None | Internal module, known lib | External API, DB, unknown lib |
| **Unknowns** | Mastered pattern | Known pattern, new context | Unknown territory, R&D |
| **Reversibility** | Trivial rollback | Migration possible | Breaking change, data migration |

**Examples:**
- **S (0-3):** Fix typo, add logging, modify constant, simple bug fix
- **M (4-6):** New CRUD endpoint, module refactor, add validation layer
- **L (7-10):** New auth system, DB migration, third-party API integration

**Complexity level:**
- **0-3 → S (Small)** - Fast track (skip to step 7)
- **4-6 → M (Medium)** - Standard flow
- **7-10 → L (Large)** - Full ceremony

Display:
```
Complexity: [S|M|L] (score: X/10)
Type: [feature|bugfix|refactor|test|doc|config|chore]
→ [Fast track|Standard flow|Full ceremony]
→ Phases: analyze [→ test] [→ dev] [→ refactor] → integrate
```

### 4. Load/Create epic context

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

### 5. Explore codebase [M, L only]

Launch exploration agent:

```
Code Scout for [E{N}] T{M}. Report facts only, don't solve.
1. Read docs/dev/architecture.md, docs/dev/standards.md
2. Read task file docs/epics/E{N}/T{M}.md
3. List impacted files (max 10 paths)
4. Find similar patterns (max 3 paths)
```

### 6. Deep analysis [L only]

Perform in-depth analysis covering:

**Data Design**
- Inputs: [types, nullability]
- Outputs: [types]
- Transformations: [if any]

**Logic Flow**
1. Step 1
2. If X then Y else Z
3. ...

**Risk Assessment**
- **Unknowns:** [libraries/APIs not mastered]
- **Technical Debt Risk:** [is simplest solution too dirty?]
- **Reversibility:** [easy to change later?]

**Architecture Questions**
- [Question 1 for user]
- [Question 2 for user]

**Engage discussion with user** to resolve questions before proceeding.

### 7. Decision synthesis

Present to user for confirmation:

---
**VALIDATION REQUIRED - [E{N}] T{M}**

**Objective:** {One sentence}

**Scope**
- IN:
  - {bullet 1}
  - {bullet 2}
  - {bullet 3}
- OUT:
  - {bullet 1}
  - {bullet 2}

**Files impacted**
- Create: `path/file.py` - {responsibility}
- Modify: `path/file.py` - {what changes}

**Design** (M, L only)
```
# Key signatures only
def function_name(param: Type) -> ReturnType: ...
class ClassName:
    def method(self) -> Type: ...
```

**Test cases**
1. `test_happy_path` - {scenario}
2. `test_edge_case` - {scenario}
3. `test_error_handling` - {scenario}

**Risks** (if any)
- {Risk description}

---
> Reply "ok" to proceed, or specify changes.

**On rejection:** Return to relevant step (3, 5, or 6).
**On approval:** Proceed to branch creation.

### 8. Create task branch

```bash
git checkout main && git pull origin main
git checkout -b e{N}-t{M}
```

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

## Analysis
### Data Design
- Inputs: {types, nullability}
- Outputs: {types}
- Transformations: {if any}

### Risk Assessment
- **Unknowns:** {libraries/APIs not mastered}
- **Technical Debt Risk:** {is simplest solution acceptable?}
- **Reversibility:** {easy to change later?}

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
