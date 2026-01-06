"""Tests for placeholder module."""

import pytest

from tdd_llm.config import Config, CoverageThresholds
from tdd_llm.placeholder import (
    find_placeholders,
    get_config_placeholder,
    load_placeholder,
    replace_placeholders,
    get_all_placeholders_for_lang,
    get_all_placeholders_for_backend,
)


class TestFindPlaceholders:
    """Tests for find_placeholders function."""

    def test_find_single_placeholder(self):
        """Test finding a single placeholder."""
        content = "Hello {{NAME}} world"
        result = find_placeholders(content)
        assert result == {"NAME"}

    def test_find_multiple_placeholders(self):
        """Test finding multiple placeholders."""
        content = "{{FOO}} and {{BAR}} and {{BAZ}}"
        result = find_placeholders(content)
        assert result == {"FOO", "BAR", "BAZ"}

    def test_find_duplicate_placeholders(self):
        """Test that duplicates are deduplicated."""
        content = "{{NAME}} and {{NAME}} again"
        result = find_placeholders(content)
        assert result == {"NAME"}

    def test_no_placeholders(self):
        """Test content without placeholders."""
        content = "No placeholders here"
        result = find_placeholders(content)
        assert result == set()

    def test_placeholder_with_numbers(self):
        """Test placeholder names can contain numbers."""
        content = "{{TEST_123}} and {{V2_NAME}}"
        result = find_placeholders(content)
        assert result == {"TEST_123", "V2_NAME"}

    def test_invalid_placeholder_ignored(self):
        """Test that invalid placeholder names are ignored."""
        content = "{{lowercase}} and {{123START}}"  # invalid: lowercase, starts with number
        result = find_placeholders(content)
        assert result == set()


class TestGetConfigPlaceholder:
    """Tests for get_config_placeholder function."""

    def test_coverage_thresholds_default(self):
        """Test COVERAGE_THRESHOLDS with default config."""
        config = Config()
        result = get_config_placeholder("COVERAGE_THRESHOLDS", config)

        assert result is not None
        assert "Line >= 80%" in result
        assert "Branch >= 70%" in result

    def test_coverage_thresholds_custom(self):
        """Test COVERAGE_THRESHOLDS with custom config."""
        config = Config(coverage=CoverageThresholds(line=95, branch=85))
        result = get_config_placeholder("COVERAGE_THRESHOLDS", config)

        assert result is not None
        assert "Line >= 95%" in result
        assert "Branch >= 85%" in result

    def test_unknown_placeholder_returns_none(self):
        """Test unknown placeholder returns None."""
        config = Config()
        result = get_config_placeholder("UNKNOWN_PLACEHOLDER", config)
        assert result is None

    def test_none_config_returns_none(self):
        """Test None config returns None."""
        result = get_config_placeholder("COVERAGE_THRESHOLDS", None)
        assert result is None


class TestLoadPlaceholder:
    """Tests for load_placeholder function."""

    def test_load_lang_placeholder(self):
        """Test loading language-specific placeholder."""
        result = load_placeholder("BUILD_TEST_CMD", lang="python", backend=None)
        assert result is not None
        assert "pytest" in result

    def test_load_backend_placeholder(self):
        """Test loading backend-specific placeholder."""
        result = load_placeholder("STATE_READ", lang=None, backend="files")
        assert result is not None
        assert "state.json" in result

    def test_load_jira_backend_placeholder(self):
        """Test loading Jira backend placeholder."""
        result = load_placeholder("STATE_READ", lang=None, backend="jira")
        assert result is not None
        assert "Jira" in result or "MCP" in result

    def test_config_placeholder_takes_priority(self):
        """Test config-based placeholder takes priority over files."""
        config = Config(coverage=CoverageThresholds(line=99, branch=99))
        result = load_placeholder("COVERAGE_THRESHOLDS", lang="python", backend=None, config=config)

        assert result is not None
        assert "99%" in result

    def test_unknown_placeholder_returns_none(self):
        """Test unknown placeholder returns None."""
        result = load_placeholder("NONEXISTENT_PLACEHOLDER", lang="python", backend="files")
        assert result is None


class TestReplacePlaceholders:
    """Tests for replace_placeholders function."""

    def test_replace_lang_placeholder(self):
        """Test replacing language placeholder."""
        content = "Run: {{BUILD_TEST_CMD}}"
        result = replace_placeholders(content, lang="python")

        assert "{{BUILD_TEST_CMD}}" not in result
        assert "pytest" in result

    def test_replace_config_placeholder(self):
        """Test replacing config-based placeholder."""
        config = Config(coverage=CoverageThresholds(line=90, branch=80))
        content = "Thresholds: {{COVERAGE_THRESHOLDS}}"
        result = replace_placeholders(content, config=config)

        assert "{{COVERAGE_THRESHOLDS}}" not in result
        assert "Line >= 90%" in result
        assert "Branch >= 80%" in result

    def test_remove_unfound_placeholder(self):
        """Test unfound placeholders are removed by default."""
        content = "Keep {{NONEXISTENT}} this"
        result = replace_placeholders(content, lang="python", remove_unfound=True)

        assert "{{NONEXISTENT}}" not in result
        assert "Keep  this" in result

    def test_keep_unfound_placeholder(self):
        """Test keeping unfound placeholders."""
        content = "Keep {{NONEXISTENT}} this"
        result = replace_placeholders(content, lang="python", remove_unfound=False)

        assert "{{NONEXISTENT}}" in result

    def test_replace_multiple_placeholders(self):
        """Test replacing multiple placeholders."""
        config = Config()
        content = "Test: {{BUILD_TEST_CMD}}\nCoverage: {{COVERAGE_THRESHOLDS}}"
        result = replace_placeholders(content, lang="python", config=config)

        assert "{{BUILD_TEST_CMD}}" not in result
        assert "{{COVERAGE_THRESHOLDS}}" not in result
        assert "pytest" in result
        assert "80%" in result


class TestGetAllPlaceholders:
    """Tests for get_all_placeholders_* functions."""

    def test_get_all_placeholders_for_python(self):
        """Test getting all placeholders for Python."""
        placeholders = get_all_placeholders_for_lang("python")

        assert "BUILD_TEST_CMD" in placeholders
        assert "COVERAGE_CMD" in placeholders
        assert "TEST_EXAMPLE" in placeholders

    def test_get_all_placeholders_for_csharp(self):
        """Test getting all placeholders for C#."""
        placeholders = get_all_placeholders_for_lang("csharp")

        assert "BUILD_TEST_CMD" in placeholders
        assert "dotnet" in placeholders["BUILD_TEST_CMD"]

    def test_get_all_placeholders_for_files_backend(self):
        """Test getting all placeholders for files backend."""
        placeholders = get_all_placeholders_for_backend("files")

        assert "STATE_READ" in placeholders
        assert "STATE_UPDATE" in placeholders

    def test_get_all_placeholders_for_nonexistent_lang(self):
        """Test getting placeholders for non-existent language."""
        placeholders = get_all_placeholders_for_lang("nonexistent")
        assert placeholders == {}
