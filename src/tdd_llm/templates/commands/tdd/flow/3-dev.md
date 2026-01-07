# /tdd:flow:3-dev

You are a Senior Developer. Your goal is to make tests pass simply (KISS). Implement code to pass tests (GREEN phase).

**Clean code from the start.** Simple != ugly. Minimal = no superfluous, no technical debt.

## Instructions

### 1. Load context

Read `.tdd-context.md` (current task context).

Read `.tdd-epic-context.md` (epic context):
- Interfaces defined in previous tasks (to respect)
- Established patterns and conventions
- Architectural decisions to follow

Read `docs/dev/standards.md` for formatting conventions.

Verify `.tdd-state.local.json`: `current.phase` must be "dev".

### 2. Read tests first

Read test files created in RED phase.

**Role of tests:**
- Tests VALIDATE behavior (what MUST pass)
- Tests don't LIMIT scope (there may be more than what's tested)
- COMPLETE scope is in `.tdd-context.md > Files` + `Design`

**Understand from tests:**
- Expected API (signatures, types)
- Verified behaviors
- Error cases to handle

**Attention:** If `.tdd-context.md` mentions files/features without tests (UI, CSS, refactorings), they MUST STILL be implemented.

### 3. Implement

**Order:**
1. Create files listed in `.tdd-context.md > Files > Create` (code, not tests)
2. Modify files listed in "Modify" (if applicable)

**Principles:**

| Principle | Description |
|-----------|-------------|
| **Completeness** | Implement EVERYTHING defined in `.tdd-context.md` (files + implementation), even if not tested |
| **YAGNI** | Do NOT add features beyond context |
| **KISS** | Simplest solution that works |

**Do:**
- Clean and readable code from the start
- Follow pattern from `.tdd-context.md > Design > Logic`
- Implement ALL of the "Design" section from context
- Clear names

**Don't:**
- Omit planned elements from context because they're not tested
- Features NOT MENTIONED in context
- Premature optimization
- Gold plating (bonus features not requested)
- Over-engineering (useless abstractions)

### 4. Verify scope completeness

**IMPORTANT: Before testing, verify ALL scope is implemented.**

Read `.tdd-context.md` entirely:
- Section **Files > Create** - all files created?
- Section **Files > Modify** - all modifications done?
- Section **Design** - all approaches/patterns implemented?

**Verification in 2 passes:**

**A) Files (Create + Modify):**
- Verify each file exists (Create) or has been modified (Modify)
- Ignore test files (already created in RED phase)
- If files missing -> STOP, implement first

**B) Content (Design):**
- Read section `.tdd-context.md > Design`
- Verify EACH described element is implemented:
  - All described interfaces/classes
  - All described patterns/approaches
  - All described refactorings (renames, etc.)
  - All described UI features (even without tests)
- If elements missing -> STOP, list and implement

**If scope complete (files + content):** Continue

### 5. Make tests pass

Run the project's test command. **Iterate** until 100% pass.

**If failure:** Fix implementation, not the test. Re-read error, fix, re-test.

### 6. Update .tdd-context.md

Add section after `## Design`:

```markdown
### GREEN Result
- Files created: [N] ([list with types: Core, UI, Config])
- Files modified: [N] ([list or "None"])
- Tests: [N]/[N] passed (GREEN)
- Build: OK, no errors

**Implemented files:**
1. [Path] - [Description]
...

**Implementation notes:**
- [Any important decision or deviation from plan]
- [UI features implemented without tests, if applicable]
- [Refactorings done, if applicable]
```

### 7. Finalize

Determine next phase (check `skip_phases` in `.tdd-state.local.json`):
- If `4-docs` not skipped → set `current.phase` = "docs"
- Else → set `current.phase` = "review"

```
## GREEN: {task_id} - Title

**Files created:** [N]
**Files modified:** [N]
**Tests:** [N]/[N] passed

Run `/tdd:flow:4-docs` to document.
     Or `/tdd:flow:5-review` if docs phase skipped.
```

## Anti-patterns

```
// Gold plating - feature NOT MENTIONED in context
public void Import(string path, bool validate = true, ILogger? logger = null)
// -> If .tdd-context.md doesn't mention validate/logger, don't add them

// But if .tdd-context.md mentions a feature WITHOUT test, implement it
// Context: "Add CSS toolbar with responsive 200px"
// -> Implement even if no CSS test

// Over-engineering - abstractions not mentioned
public interface IProcessor { }
public class Processor : IProcessor { }
public class ProcessorFactory { }
// -> Direct and simple if context doesn't require this structure

// Premature optimization
public class CachedImporter // No cache test = no cache
// -> Unless .tdd-context.md > Design mentions cache

// Omitting planned scope
// Context: "Rename CustomGrid -> PresetGrid everywhere"
// Code: Only rename in tested files
// -> Rename EVERYWHERE as requested, even files without tests
```

## Difficult situations

**Ambiguous test:**
Ask user which approach to follow.

**Design problem revealed:**
- If simple: resolve now
- If complex: ask before continuing

**Features without tests (UI, CSS, refactorings):**
- Implement anyway if mentioned in `.tdd-context.md`
- Example: WindowSettingsModal without tests -> implement per `Design`
- Example: CSS for toolbar -> implement per specifications
- Example: Renames CustomGrid -> PresetGrid -> do all renames
- Tests validate core behavior, not complete UI

**Test passes without code change:**
- Test may be wrong (tests language, not our code)
- Feature may already exist elsewhere
- → Verify test is meaningful, ask user if unclear

**Test impossible to pass without breaking another:**
- Design conflict between tests
- → STOP, do not hack around it, ask user

**Implementation reveals incorrect test:**
- Test assumptions don't match reality (wrong signature, impossible state)
- → STOP, explain the issue, propose test correction

**Circular dependency discovered:**
- Implementation requires import that creates cycle
- → STOP, architectural decision needed

## Warning signs (STOP and ask)

**STOP implementation and ask user if:**
- 3+ failed attempts to pass the same test
- Need to modify a test to make it pass
- Need to modify files NOT listed in `.tdd-context.md`
- Implementation requires adding dependencies not mentioned in context
- Two tests contradict each other
- Scope creep: implementation growing significantly beyond context

**Do NOT:**
- Loop indefinitely trying different approaches
- Modify tests to make them pass
- Add files/features outside defined scope
- Assume and proceed when uncertain
