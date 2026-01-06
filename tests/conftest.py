"""Shared test fixtures for tdd-llm."""

import os
import tempfile
import shutil
from pathlib import Path
from unittest import mock

import pytest


@pytest.fixture(autouse=True)
def consistent_terminal_width():
    """Force consistent terminal width for Rich/Typer output across platforms."""
    import shutil
    # Mock get_terminal_size to return a fixed size on all platforms
    with mock.patch.object(shutil, "get_terminal_size", return_value=os.terminal_size((200, 50))):
        with mock.patch.dict(os.environ, {"COLUMNS": "200", "LINES": "50", "TERM": "xterm-256color"}):
            yield


@pytest.fixture(autouse=True)
def skip_first_run_wizard():
    """Disable first-run wizard for all tests."""
    with mock.patch("tdd_llm.cli.is_first_run", return_value=False):
        yield


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    dirpath = tempfile.mkdtemp()
    yield Path(dirpath)
    shutil.rmtree(dirpath)


@pytest.fixture
def temp_config_file(temp_dir):
    """Create a temporary config file path."""
    return temp_dir / "config.yaml"
