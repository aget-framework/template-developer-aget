"""Pytest configuration for developer template tests.

Provides template/instance detection for conditional test execution.
Contract tests for instance-specific features should be skipped when running on templates.

v2.10.0: Added template context detection for CI compatibility
"""

import json
import os
import pytest
from pathlib import Path


def get_version_json_path():
    """Find version.json relative to test file location."""
    # Use __file__ parent to find project root reliably (works in CI)
    tests_dir = Path(__file__).parent
    project_root = tests_dir.parent
    return project_root / ".aget" / "version.json"


def is_template_context():
    """
    Detect if tests are running in template context vs instance context.

    Templates are detected by:
    1. agent_name starts with 'template-'
    2. OR instance_type == 'template'

    Returns True for templates (skip instance-only tests).
    Returns False for instances (run all tests).
    """
    version_file = get_version_json_path()

    if not version_file.exists():
        # If no version.json, assume template context (safe default)
        return True

    try:
        with open(version_file) as f:
            data = json.load(f)

        # Check agent_name prefix
        agent_name = data.get("agent_name", "")
        if agent_name.startswith("template-"):
            return True

        # Check instance_type field
        instance_type = data.get("instance_type", "")
        if instance_type == "template":
            return True

        return False
    except (json.JSONDecodeError, IOError):
        # On error, assume template context (safe default)
        return True


# Pytest marker for instance-only tests
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "instance_only: mark test as instance-only (skipped on templates)"
    )


@pytest.fixture(scope="session", autouse=True)
def ensure_project_root():
    """Ensure contract tests run from project root where .aget/ exists."""
    current = Path.cwd()

    # If already at project root, nothing to do
    if (current / ".aget" / "version.json").exists():
        return

    # If in tests/ subdirectory, move up
    if current.name == "tests" and (current.parent / ".aget" / "version.json").exists():
        os.chdir(current.parent)
        return


@pytest.fixture(scope="session")
def template_context():
    """Fixture providing template context detection."""
    return is_template_context()
