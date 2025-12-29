#!/usr/bin/env python3
"""v3.0 Wake Protocol Contract Tests - Developer Template

Tests that wake protocol correctly reports agent identity, version, capabilities,
and developer-specific information.

v3.0.0: 5D Composition Architecture - instance_type replaces roles

Part of AGET framework developer template validation.
"""

import pytest
import json
from pathlib import Path


def test_wake_protocol_reports_agent_name():
    """Wake protocol must report agent name from version.json (if present)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        # agent_name optional in templates, required in instantiated agents
        if "agent_name" in data:
            agent_name = data["agent_name"]
            assert agent_name, "agent_name field is empty"
            assert isinstance(agent_name, str), "agent_name must be a string"


def test_wake_protocol_reports_version():
    """Wake protocol must report current AGET version."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        assert "aget_version" in data, "version.json missing aget_version field"
        # Version format: X.Y.Z
        version = data["aget_version"]
        base_version = version.split("-")[0]  # Handle pre-release
        parts = base_version.split(".")
        assert len(parts) == 3, f"Version format invalid: {version} (expected X.Y.Z)"


def test_wake_protocol_reports_capabilities():
    """Wake protocol must report agent capabilities (if present)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        # Capabilities are optional in template, but if present, must be dict
        if "capabilities" in data:
            capabilities = data["capabilities"]
            assert isinstance(capabilities, (dict, list)), "capabilities must be dict or list"


def test_wake_protocol_reports_domain():
    """Wake protocol must report agent domain for context (if present)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        # Domain is optional in template, but if present, must be string
        if "domain" in data:
            domain = data["domain"]
            assert isinstance(domain, str), "domain must be a string"
            assert domain, "domain field is empty"


# ============================================================================
# Developer-Specific Wake Protocol Tests (v3.0)
# ============================================================================


def test_wake_displays_developer_mode():
    """Wake protocol must indicate developer (action-taking) mode.

    v3.0: Uses instance_type and template fields instead of roles.
    - instance_type: "aget" (advisory) vs "AGET" (action-taking) vs "template"
    - template: archetype name (developer, supervisor, etc.)
    """
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        # v3.0: Check template or instance_type
        template = data.get("template", "")
        instance_type = data.get("instance_type", "")

        # Developer is an action-taking archetype
        if template == "developer":
            # For templates, instance_type is "template"
            # For instances, should be "AGET" (action-taking)
            if instance_type != "template":
                assert instance_type == "AGET", \
                    f"Developer instances should have instance_type 'AGET', got '{instance_type}'"


def test_wake_displays_domain():
    """Wake protocol must display domain for developer agents.

    v3.0: Domain indicates the development focus area.
    """
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        # v3.0: Check template field
        template = data.get("template", "")

        if template == "developer":
            # Domain should be defined for developer agents
            domain = data.get("domain")
            if domain is not None:
                assert isinstance(domain, str), \
                    f"domain must be string, got {type(domain)}"
                assert domain.strip(), \
                    "domain must not be empty string"
