# /tdd:flow:4-docs

Document the completed task.

## Instructions

### 1. Load context

Read `.tdd-context.md` (lightweight).

Verify `.tdd-state.local.json`: `current.phase` must be "docs".

### 2. Update CHANGELOG.md

**Add entry** under appropriate section (Added/Changed/Fixed):

- Format: `- [Module]: description of change`
- Be **specific** (mention classes/methods)
- Write from user/developer perspective

**Example:**
```markdown
### Added
- GDTF import: extract color wheels with CIE xyY values and gobo images
- `FixtureType.Wheels` collection for accessing fixture wheel definitions
```

### 3. Verify code documentation

**Read created/modified files** (from `.tdd-context.md > Files`).

**If public APIs:**
- Verify all public types/methods have documentation (docstrings, JSDoc, XML docs)
- Follow existing format in the project (check similar files)
- Add those that are missing

### 4. Check documentation to update

**Read `{{AGENT_FILE}}` section "Documentation Structure"** for project doc locations.

For each documentation type listed:
- Check if task changes require an update
- If yes, update now

**If section not found in `{{AGENT_FILE}}`:** Discover doc structure and add it:
```bash
# Find doc directories
find . -type d -name "doc*" -o -name "wiki" -o -name "help" 2>/dev/null | head -10
```

**Common doc types:**

| Type | Update if... |
|------|--------------|
| **Dev docs** (`docs/dev/`, `docs/api/`) | API changes, new patterns |
| **User docs** (`docs/user/`, `help/`) | UI changes, new features, behavior changes |
| **API specs** (`openapi.yaml`, `swagger.json`) | Endpoint changes |
| **Project context** (`README.md`, `{{AGENT_FILE}}`) | Important patterns, setup changes |

### 5. Validate existing examples

**If task modified public APIs:**
- Search docs for code examples using changed functions/classes
- Verify examples still work after changes
- Update outdated examples

### 6. Evaluate if ADR needed

**Read `.tdd-context.md > Decisions`.**

**Create ADR if:**
- Choice between multiple valid approaches
- Decision impacts multiple modules
- Significant trade-off (performance vs simplicity)

**Don't create if:**
- Standard implementation without alternative
- Decision local to one file

**If ADR needed:**
- Find existing ADRs location (usually `docs/dev/decisions/` or `docs/adr/`)
- Use project's ADR template if exists
- Numbering: next available number

### 7. Update .tdd-context.md

Add final section:

```markdown
## Documentation
- CHANGELOG updated ([Added/Changed/Fixed])
- Code docs: Complete
- ADR: [NNN-title] / Not needed
- Other docs: [list] / None
```

### 8. Update phase

Set `current.phase` = "review" in `.tdd-state.local.json`.

### 9. Report

```
## Documentation: {task_id} - Title

### Updated
- `CHANGELOG.md` - Section [Added/Changed/Fixed]
- Code docs: [N] added / Already complete
- [list any other docs updated]

### Created
- `docs/decisions/[NNN-title].md` / No ADR needed

### Verified (no change needed)
- [list docs checked]

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
