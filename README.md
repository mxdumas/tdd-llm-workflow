# tdd-llm

Deploy TDD workflow templates for Claude and Gemini AI assistants.

## Features

- Deploy `.claude/` and `.gemini/` configuration directories
- Automatic conversion from Claude (.md) to Gemini (.toml) format
- Language-specific placeholders (Python, C#, TypeScript)
- Backend support for local files or Jira (via MCP)
- Global and project-level configuration (project overrides global)
- Configurable coverage thresholds per project
- Cross-platform (Linux, macOS, Windows)
- Update templates from GitHub without reinstalling the package

## Installation

```bash
pip install tdd-llm
```

## Quick Start

```bash
# Initialize project config (creates .tdd-llm.yaml)
tdd-llm init --lang python --backend files

# Deploy TDD templates to current project
tdd-llm deploy

# Deploy to user-level directories
tdd-llm deploy --target user --lang csharp --backend jira

# Preview changes without writing
tdd-llm deploy --lang typescript --dry-run

# List available languages and backends
tdd-llm list

# Show configuration (merged global + project)
tdd-llm config --show

# Update templates from GitHub (without reinstalling)
tdd-llm update
```

## Configuration

tdd-llm supports two configuration levels:
- **Global** (user-level): Applies to all projects
- **Project** (local): Overrides global settings for a specific project

### Global Configuration

Location:
- Linux/macOS: `~/.config/tdd-llm/config.yaml`
- Windows: `%APPDATA%\tdd-llm\config.yaml`

```yaml
default_target: "project"  # or "user"
default_language: "python"
default_backend: "files"   # or "jira"
platforms:
  - claude
  - gemini
coverage:
  line: 80      # Line coverage threshold (%)
  branch: 70    # Branch coverage threshold (%)
```

### Project Configuration

Create a `.tdd-llm.yaml` file in your project root to override global settings:

```bash
# Initialize project config with custom settings
tdd-llm init --lang typescript --coverage-line 90

# Or modify existing project config
tdd-llm config --project --set-lang csharp
```

Project config file: `.tdd-llm.yaml`
```yaml
default_language: "typescript"
coverage:
  line: 90      # Override only what you need
```

### Configuration Commands

```bash
# Show effective configuration (merged global + project)
tdd-llm config --show

# Modify global config
tdd-llm config --set-coverage-line 80

# Modify project config
tdd-llm config --project --set-lang typescript
```

Coverage thresholds are applied to the generated TDD templates and enforced during the review phase.

## Updating Templates

Templates can be updated from GitHub without reinstalling the package:

```bash
# Update to latest templates
tdd-llm update

# Force re-download all templates
tdd-llm update --force

# Deploy using package templates (ignore cached updates)
tdd-llm deploy --no-cache
```

Updated templates are cached in:
- Linux/macOS: `~/.config/tdd-llm/templates/`
- Windows: `%APPDATA%\tdd-llm\templates\`

## Supported Languages

| Language | Placeholders |
|----------|--------------|
| Python | pytest, coverage, mock examples |
| C# | dotnet test, xUnit, Moq examples |
| TypeScript | Jest, coverage, mock examples |

## Backends

### Files (default)

Uses local markdown files for epic/story management:
- `docs/epics/` - Epic definitions
- `docs/state.json` - Progress tracking

### Jira

Uses MCP Jira server for epic/story management:
- Fetches epics and stories from Jira
- Updates status via Jira API

## TDD Workflow Commands

After deployment, use these commands with Claude or Gemini:

### Flow Commands

| Command | Phase | Description |
|---------|-------|-------------|
| `/tdd:flow:1-analyze` | Plan | Analyze task, write specs |
| `/tdd:flow:2-test` | RED | Write failing tests |
| `/tdd:flow:3-dev` | GREEN | Implement to pass tests |
| `/tdd:flow:4-docs` | Document | Update docs, CHANGELOG |
| `/tdd:flow:5-review` | Review | Code review, create PR |
| `/tdd:flow:6-done` | Done | Commit, update state |
| `/tdd:flow:status` | - | Show current progress |
| `/tdd:flow:next` | - | Auto-execute next step |

### Init Commands

| Command | Description |
|---------|-------------|
| `/tdd:init:1-project` | Initialize project structure |
| `/tdd:init:2-architecture` | Define architecture |
| `/tdd:init:3-standards` | Define code standards |
| `/tdd:init:4-readme` | Generate README |

## Development

```bash
# Clone and install in dev mode
git clone https://github.com/mxdumas/tdd-llm-workflow
cd tdd-llm-workflow
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -e ".[dev]"
pre-commit install

# Run tests
pytest

# Run linter
ruff check src/

# Format code
ruff format src/
```

## License

MIT
