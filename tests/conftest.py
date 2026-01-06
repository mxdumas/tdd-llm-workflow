"""Shared test fixtures for tdd-llm."""

import tempfile
import shutil
from pathlib import Path
from unittest import mock

import pytest


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
