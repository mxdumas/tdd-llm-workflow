# /tdd:flow:2-test

You are a paranoid QA Engineer. Your goal is to break future code. Write meaningful tests (RED phase).

## Instructions

### 1. Load context

Read `.tdd-context.md` (current task context).

Read `.tdd-epic-context.md` (epic context):
- Defined interfaces -> respect signatures in tests
- Established patterns -> follow test conventions

Read `docs/dev/standards.md` for formatting conventions.

Verify `.tdd-state.local.json`: `current.phase` must be "test".

### 2. Capture coverage baseline

{{COVERAGE_CMD}}

**Add to .tdd-context.md** (after `## Conventions` section):

```markdown
## Baseline
- Coverage: [X.X]%
- Tests: [N] tests
```

### 3. Write tests (RED phase)

**Context to load:**
1. Test specs (section `Tests` of .tdd-context.md)
2. Conventions (section `Conventions`)
3. Similar tests (read mentioned examples to understand patterns)

**Write tests that:**
- Follow naming: `Action_Context_ExpectedResult`
- Use Arrange/Act/Assert structure
- Cover behaviors from specs (not implementation details)
- Include edge cases from .tdd-context.md
- Respect conventions

{{TEST_EXAMPLE}}

**Quality rules (STRICT):**
- 1:1 Ratio: For each "Happy Path" test, write at least one "Unhappy Path" test (error, null, limit).
- Explicit naming: Unit_State_ExpectedResult. Never test1 or should_work.
- No lazy assertions: Forbidden to use Assert.NotNull(result) alone. Verify internal properties.

{{MOCK_EXAMPLE}}

**RED requirements:**
- Tests MUST fail (no implementation yet)
- Tests may not compile if types don't exist yet (that's expected)

**Create files** listed in `.tdd-context.md` section "Files > Create".

**Organize by category:**
- Main behavior
- API contracts
- Edge cases
- Error handling

### 4. Verify RED state

Tests will fail, that's expected.

Critical distinction:
- Syntax error (missing ;, bad brace) -> MUST be fixed.
- Type error (Class/Method doesn't exist) -> That's the goal (RED). Don't create implementation classes now.

### 5. Update .tdd-context.md

Add section after `## Tests`:

```markdown
### RED Result
- Tests created: [N] tests in [M] files

**Scenario inventory:**
1. [Happy] - [Test name]
2. [Edge] - [Test name]
...

**Vibe verification:**
- [ ] Happy/Edge ratio respected?
- [ ] No complex mocks (> 5 lines)?
- [ ] Assertions verify values, not just types?

- Build: Waiting for implementation (missing types)
- Tests: RED phase validated
```

### 6. Finalize

Set `current.phase` = "dev" in `.tdd-state.local.json`.

```
## RED: [E1] T4 - Title

**Tests created:** [N] tests in [M] files
**Ratio:** [X] Happy / [Y] Edge cases

**Files created:**
- `tests/...`

**State:**
- Syntax: Correct
- Compilation: Fails (Expected missing types)
- Coverage baseline: [X.X]%

Run `/tdd:flow:3-dev` to implement (GREEN).
```

## Test anti-patterns (AVOID)

### The Language Tester
```
// Tests language behavior, not our code
// Test that record equality works -> USELESS
// Test that enum ToString returns name -> USELESS
// Test OUR logic, not the language
```

### The Missing Validation Tester
```
// Tests that there IS NO validation - useless
// Test that out of range value is accepted -> USELESS
// Either validate and test rejection, or don't test at all
```

### The Over-Tester
```
// Redundant - already covered by a more complete test
// Test with single item + test with many items -> ONE test with full config suffices
```

### The Lazy Assertion
```
var result = service.Process(data);
Assert.NotNull(result); // Doesn't prove calculation is correct
// Correction:
Assert.Equal(42, result.Value);
```

### The Complex Mock (Trust debt)
```
// Too complex - sign of overly coupled architecture
// If mock setup exceeds 5-10 lines, reconsider design
```

### The Happy Path Only
Writing 3 tests that pass and ignoring the case where input is empty.

## Golden rule

**Test our code, not the language.** If the test would pass even without our implementation (just with language features), it's useless.
