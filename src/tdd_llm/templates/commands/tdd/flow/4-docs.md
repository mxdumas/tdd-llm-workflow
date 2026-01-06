# /tdd:flow:4-docs

Document the completed task.

## Instructions

### 1. Load context

Read `.tdd-context.md` (lightweight).

Verify `.tdd-state.local.json`: `current.phase` must be "green".

### 2. Update CHANGELOG.md

**Add entry** under appropriate section (Added/Changed/Fixed):

- Format: `- [Module]: description of change`
- Be **specific** (mention classes/methods)
- Write from user/developer perspective
- See good entry examples at end of document

**Example:**
```markdown
### Added
- GDTF import: extract color wheels with CIE xyY values and gobo images
- `FixtureType.Wheels` collection for accessing fixture wheel definitions
```

### 3. Verify documentation

**Read created files** (from `.tdd-context.md > Files > Create`).

**If public APIs:**
- Verify all public types/methods have documentation
- Add those that are missing

{{DOC_FORMAT}}

### 4. Evaluate if ADR needed

**Read `.tdd-context.md > Decisions`.**

**Create ADR if:**
- Choice between multiple valid approaches
- Decision that impacts multiple modules
- Significant trade-off (performance vs simplicity)

**Don't create if:**
- Standard implementation without alternative
- Decision local to one file
- Obvious choice without trade-off

**If ADR needed:**
- Create in `docs/dev/decisions/`
- Use template if exists
- Numbering: next available number

### 5. Check existing docs

| Document | Update if... |
|----------|--------------|
| `docs/dev/api/*.md` | New API / modification to API / important module |
| `docs/user/**.md` | User-facing documentation -> must be updated when impact UI changes |
| `docs/dev/architecture.md` | Important architecture change |
| `README.md` or `CLAUDE.md` | Important changes to communicate to LLM |

If update needed: do it now.

### 6. Update .tdd-context.md

Add final section:

```markdown
## Documentation
- CHANGELOG updated ([Added/Changed/Fixed])
- Docs complete
- ADR created: [NNN-title] / Not needed
- Other docs: [list] / None
```

### 7. Update phase

Set `current.phase` = "docs" in `.tdd-state.local.json`.

### 8. Report

```
## Documentation: [E1] T4 - Title

### Updated
- `CHANGELOG.md` - Section [Added/Changed/Fixed]
- Docs - [N] added / Already complete

### Created
- `docs/dev/decisions/[NNN-title].md` / No ADR needed

### Verified (no change needed)
- `docs/dev/architecture.md`
- `README.md`

Run `/tdd:flow:5-review` for review and PR creation.
```

## CHANGELOG best practices

**Good:**
```markdown
### Added
- GDTF import: extract color wheels with CIE xyY values and gobo images
- `FixtureType.Wheels` collection for accessing fixture wheel definitions

### Changed
- `GdtfImporter.Import()` now extracts channel functions with DMX ranges
```

**Bad:**
```markdown
### Added
- Added wheels
- New feature
```

## When to create an ADR

**Create:**
- Choice between multiple valid approaches
- Decision that impacts multiple modules
- Significant trade-off (performance vs simplicity)

**Don't create:**
- Standard implementation without alternative
- Decision local to one file
- Obvious choice without trade-off
