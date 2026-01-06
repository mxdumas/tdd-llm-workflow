# Contributing to tdd-llm

## Development Setup

```bash
git clone https://github.com/mxdumas/tdd-llm-workflow
cd tdd-llm-workflow
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -e ".[dev]"
pre-commit install
```

## Running Tests

```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_updater.py  # Run specific test file
```

## Code Quality

```bash
ruff check src/           # Linter
ruff format src/          # Formatter
```

## Project Structure

```
src/tdd_llm/
├── cli.py              # CLI commands (typer)
├── config.py           # Configuration management
├── deployer.py         # Template deployment logic
├── placeholder.py      # Placeholder replacement
├── updater.py          # GitHub template updates
├── converter.py        # MD to TOML conversion
├── paths.py            # Cross-platform paths
└── templates/
    ├── manifest.json   # Template checksums (auto-generated)
    ├── commands/       # TDD workflow commands
    └── placeholders/   # Language/backend specific content
        ├── langs/      # python, csharp, typescript
        └── backends/   # files, jira
```

## Making Changes

### Templates (prompts)

1. Edit files in `src/tdd_llm/templates/`
2. Push to `main`
3. GitHub Action automatically regenerates `manifest.json`
4. Users receive updates via `tdd-llm update`

**No new package version needed for template changes.**

### Source Code

1. Create a branch
2. Make your changes
3. Add tests
4. Open a PR
5. After merge, create a tag to publish to PyPI:

```bash
git tag v1.2.0
git push --tags
```

## Adding a New Language

1. Create `src/tdd_llm/templates/placeholders/langs/<lang>/`
2. Add required files:
   - `BUILD_COMMANDS.md`
   - `BUILD_TEST_CMD.md`
   - `COVERAGE_CMD.md`
   - `TEST_EXAMPLE.md`
   - `MOCK_EXAMPLE.md`
   - `DOC_FORMAT.md`
   - `STANDARDS_QUESTIONS.md`

## Adding a New Backend

1. Create `src/tdd_llm/templates/placeholders/backends/<backend>/`
2. Add required files:
   - `STATE_READ.md`
   - `STATE_UPDATE.md`
   - `EPIC_SOURCE.md`

## Commit Messages

Format: `type: description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `chore`: Maintenance (CI, deps, etc.)
- `refactor`: Refactoring without behavior change
- `test`: Add/modify tests

Examples:
```
feat: add support for Go language
fix: handle network timeout in update command
docs: update README with new options
chore: update template manifest to v1.0.5
```
