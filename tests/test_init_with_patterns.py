"""
Test init command with --with-patterns flag.
"""

import json
import tempfile
from pathlib import Path

import pytest

from aget.config.commands.init import InitCommand


class TestInitWithPatterns:
    """Test --with-patterns flag enhancement."""

    def setup_method(self):
        """Set up test environment."""
        self.cmd = InitCommand()
        self.temp_dir = tempfile.mkdtemp()
        self.test_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_without_patterns(self):
        """Test basic init without patterns."""
        result = self.cmd.tier_basic(args=[str(self.test_dir), '--template', 'minimal'])

        assert result['success']
        assert (self.test_dir / "AGENTS.md").exists()
        assert (self.test_dir / ".aget").exists()
        assert 'patterns_applied' in result
        assert result['patterns_applied'] == []

    def test_init_with_patterns_minimal(self):
        """Test minimal template with patterns."""
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'minimal', '--with-patterns']
        )

        assert result['success']
        assert 'patterns_applied' in result
        # Minimal template should apply session/wake
        expected_patterns = self.cmd._get_patterns_for_template('minimal')
        assert expected_patterns == ['session/wake']

    def test_init_with_patterns_standard(self):
        """Test standard template with patterns."""
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'standard', '--with-patterns']
        )

        assert result['success']
        assert 'patterns_applied' in result
        expected_patterns = self.cmd._get_patterns_for_template('standard')
        assert 'session/wake' in expected_patterns
        assert 'session/wind_down' in expected_patterns
        assert 'housekeeping/cleanup' in expected_patterns

    def test_init_with_patterns_agent(self):
        """Test agent template with patterns."""
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'agent', '--with-patterns']
        )

        assert result['success']
        assert 'patterns_applied' in result
        expected_patterns = self.cmd._get_patterns_for_template('agent')
        # Agent template should have most patterns
        assert len(expected_patterns) >= 5
        assert 'session/wake' in expected_patterns
        assert 'housekeeping/sanity_check' in expected_patterns

    def test_pattern_mapping_completeness(self):
        """Test that all templates have pattern mappings."""
        for template_type in self.cmd.templates.keys():
            patterns = self.cmd._get_patterns_for_template(template_type)
            assert isinstance(patterns, list)
            # All templates should have at least one pattern
            if template_type != 'minimal':
                assert len(patterns) >= 1

    def test_init_creates_correct_directories(self):
        """Test that correct directories are created."""
        # Test agent template
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'agent']
        )

        assert result['success']
        expected_dirs = self.cmd.templates['agent']['dirs']
        for dir_path in expected_dirs:
            full_path = self.test_dir / dir_path
            assert full_path.exists(), f"Directory {dir_path} not created"

    def test_init_force_overwrites(self):
        """Test --force flag overwrites existing config."""
        # First init
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'minimal']
        )
        assert result['success']

        # Second init without force should fail
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'standard']
        )
        assert not result['success']
        assert "already exists" in result['error']

        # Third init with force should succeed
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'standard', '--force']
        )
        assert result['success']

    def test_readme_files_created(self):
        """Test that README files are created in key directories."""
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'agent']
        )

        assert result['success']

        # Check for README files
        assert (self.test_dir / "workspace" / "README.md").exists()
        assert (self.test_dir / "products" / "README.md").exists()
        assert (self.test_dir / ".aget" / "evolution" / "README.md").exists()

    def test_version_tracking_created(self):
        """Test that version.json is created."""
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'standard']
        )

        assert result['success']
        version_file = self.test_dir / ".aget" / "version.json"
        assert version_file.exists()

        version_data = json.loads(version_file.read_text())
        assert version_data['template'] == 'standard'
        assert 'aget_version' in version_data

    def test_claude_compatibility(self):
        """Test CLAUDE.md backward compatibility."""
        result = self.cmd.tier_basic(
            args=[str(self.test_dir), '--template', 'minimal']
        )

        assert result['success']
        claude_file = self.test_dir / "CLAUDE.md"
        assert claude_file.exists()

        # Should be symlink or redirect file
        if claude_file.is_symlink():
            # readlink() was added in Python 3.9, use resolve() for compatibility
            import os
            target = os.readlink(str(claude_file))
            assert target == "AGENTS.md"
        else:
            content = claude_file.read_text()
            assert "AGENTS.md" in content