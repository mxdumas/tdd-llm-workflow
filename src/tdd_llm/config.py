"""Configuration management for tdd-llm."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml

from .paths import get_config_dir

# Project-level config filename
PROJECT_CONFIG_NAME = ".tdd-llm.yaml"


@dataclass
class CoverageThresholds:
    """Coverage threshold configuration."""

    line: int = 80
    branch: int = 70

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {"line": self.line, "branch": self.branch}


@dataclass
class ConfigSource:
    """Tracks where configuration was loaded from."""

    global_path: Path | None = None
    project_path: Path | None = None

    @property
    def active_path(self) -> Path | None:
        """Return the most specific config path (project > global)."""
        return self.project_path or self.global_path


@dataclass
class Config:
    """TDD-LLM configuration."""

    default_target: Literal["project", "user"] = "project"
    default_language: str = "python"
    default_backend: Literal["files", "jira"] = "files"
    platforms: list[str] = field(default_factory=lambda: ["claude", "gemini"])
    coverage: CoverageThresholds = field(default_factory=CoverageThresholds)
    source: ConfigSource = field(default_factory=ConfigSource)

    @classmethod
    def _load_from_file(cls, path: Path) -> dict:
        """Load raw config data from a YAML file."""
        if not path.exists():
            return {}
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    @classmethod
    def _merge_data(cls, base: dict, override: dict) -> dict:
        """Merge two config dicts, with override taking precedence."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = cls._merge_data(result[key], value)
            else:
                result[key] = value
        return result

    @classmethod
    def _from_data(cls, data: dict, source: ConfigSource) -> "Config":
        """Create Config from data dict."""
        coverage_data = data.get("coverage", {})
        coverage = CoverageThresholds(
            line=coverage_data.get("line", 80),
            branch=coverage_data.get("branch", 70),
        )

        return cls(
            default_target=data.get("default_target", "project"),
            default_language=data.get("default_language", "python"),
            default_backend=data.get("default_backend", "files"),
            platforms=data.get("platforms", ["claude", "gemini"]),
            coverage=coverage,
            source=source,
        )

    @classmethod
    def load(
        cls,
        path: Path | None = None,
        project_path: Path | None = None,
        include_project: bool = True,
    ) -> "Config":
        """Load configuration from YAML files.

        Loads global config first, then merges project config on top.
        Project config values override global config values.

        Args:
            path: Path to global config file. Defaults to user config directory.
            project_path: Project root to look for .tdd-llm.yaml. Defaults to cwd.
            include_project: If True, also load project-level config.

        Returns:
            Config instance with merged values.
        """
        global_path = path or get_config_dir() / "config.yaml"
        source = ConfigSource()

        # Load global config
        global_data = cls._load_from_file(global_path)
        if global_path.exists():
            source.global_path = global_path

        # Load project config if requested
        project_data = {}
        if include_project:
            proj_root = project_path or Path.cwd()
            proj_config_path = proj_root / PROJECT_CONFIG_NAME
            project_data = cls._load_from_file(proj_config_path)
            if proj_config_path.exists():
                source.project_path = proj_config_path

        # Merge: project overrides global
        merged_data = cls._merge_data(global_data, project_data)

        return cls._from_data(merged_data, source)

    def save(self, path: Path | None = None, project: bool = False) -> Path:
        """Save configuration to YAML file.

        Args:
            path: Path to config file. If None, uses default location.
            project: If True, save to project config (.tdd-llm.yaml in cwd).
                    If False, save to global config.

        Returns:
            Path where config was saved.
        """
        if path:
            config_path = path
        elif project:
            config_path = Path.cwd() / PROJECT_CONFIG_NAME
        else:
            config_path = get_config_dir() / "config.yaml"

        config_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "default_target": self.default_target,
            "default_language": self.default_language,
            "default_backend": self.default_backend,
            "platforms": self.platforms,
            "coverage": self.coverage.to_dict(),
        }

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)

        return config_path

    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "default_target": self.default_target,
            "default_language": self.default_language,
            "default_backend": self.default_backend,
            "platforms": self.platforms,
            "coverage": self.coverage.to_dict(),
        }


def get_project_config_path(project_path: Path | None = None) -> Path:
    """Get the project config file path.

    Args:
        project_path: Project root. Defaults to cwd.

    Returns:
        Path to project config file (may not exist).
    """
    return (project_path or Path.cwd()) / PROJECT_CONFIG_NAME


def get_global_config_path() -> Path:
    """Get the global config file path.

    Returns:
        Path to global config file (may not exist).
    """
    return get_config_dir() / "config.yaml"


def is_first_run() -> bool:
    """Check if this is the first run (no global config exists).

    Returns:
        True if global config does not exist.
    """
    return not get_global_config_path().exists()


def get_available_languages() -> list[str]:
    """Get list of available language placeholders.

    Returns:
        List of language names with placeholder directories.
    """
    from .paths import get_placeholders_dir

    langs_dir = get_placeholders_dir() / "langs"
    if not langs_dir.exists():
        return []

    return sorted([d.name for d in langs_dir.iterdir() if d.is_dir()])


def get_available_backends() -> list[str]:
    """Get list of available backend placeholders.

    Returns:
        List of backend names with placeholder directories.
    """
    from .paths import get_placeholders_dir

    backends_dir = get_placeholders_dir() / "backends"
    if not backends_dir.exists():
        return []

    return sorted([d.name for d in backends_dir.iterdir() if d.is_dir()])
