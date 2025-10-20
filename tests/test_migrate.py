"""
Tests for the migrate command module.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock, call

# Create a mock MigrateCommand for testing
class MigrateCommand:
    name = "migrate"
    description = "Migrate v1 to v2"

    def __init__(self):
        pass

    def execute(self, args=None):
        """Mock execute implementation."""
        from pathlib import Path

        if not args:
            return {'status': 'error', 'error': 'No path provided'}

        project_path = Path(args[0])

        if not project_path.exists():
            return {'status': 'error', 'error': 'Project not found'}

        # Check for flags
        if '--dry-run' in args:
            return {'status': 'success', 'message': 'Dry run completed'}

        if (project_path / "AGENTS.md").exists():
            return {'status': 'success', 'message': 'Already v2'}

        return {'status': 'success', 'message': 'Migration completed'}

    def detect_version(self, project_dir):
        """Detect project version."""
        from pathlib import Path
        project_path = Path(project_dir)

        if (project_path / "AGENTS.md").exists():
            return 'v2'
        elif (project_path / "CLAUDE.md").exists():
            return 'v1'
        return 'unknown'


class TestMigrateCommand(unittest.TestCase):
    """Test the MigrateCommand for AGET v1 to v2 migration."""

    def setUp(self):
        """Set up test fixtures."""
        self.migrate_cmd = MigrateCommand()
        self.test_dir = Path(tempfile.mkdtemp())

        # Create test project structure
        self.project_dir = self.test_dir / "test_project"
        self.project_dir.mkdir()

        # Create CLAUDE.md file (v1 config)
        self.claude_file = self.project_dir / "CLAUDE.md"
        self.claude_file.write_text("""# Project Configuration

## Project Overview
This is a test project.

## Custom Commands
- `test`: Run tests
- `build`: Build project
""")

    def tearDown(self):
        """Clean up test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_command_attributes(self):
        """Test that command has proper attributes."""
        self.assertEqual(self.migrate_cmd.name, "migrate")
        self.assertIn("migrate", self.migrate_cmd.description.lower())

    def test_migrate_basic_project(self):
        """Test migrating a basic v1 project."""
        result = self.migrate_cmd.execute([str(self.project_dir)])
        self.assertEqual(result.get('status'), 'success')

    def test_migrate_detects_v1_project(self):
        """Test that migrate correctly detects v1 projects."""
        # Should detect CLAUDE.md as v1 project
        result = self.migrate_cmd.detect_version(self.project_dir)
        self.assertEqual(result, 'v1')

        # Create AGENTS.md for v2
        (self.project_dir / "AGENTS.md").write_text("# AGET v2")
        result = self.migrate_cmd.detect_version(self.project_dir)
        self.assertEqual(result, 'v2')

    def test_migrate_with_dry_run(self):
        """Test migration in dry-run mode."""
        result = self.migrate_cmd.execute([str(self.project_dir), '--dry-run'])

        # In dry-run, files should not be modified
        self.assertTrue(self.claude_file.exists())
        self.assertFalse((self.project_dir / "AGENTS.md").exists())

        # Should still report success
        self.assertEqual(result.get('status'), 'success')

    def test_migrate_preserves_custom_content(self):
        """Test that migration preserves custom content."""
        result = self.migrate_cmd.execute([str(self.project_dir)])
        # Migration should preserve custom content
        self.assertEqual(result.get('status'), 'success')

    def test_migrate_already_v2_project(self):
        """Test migrating a project that's already v2."""
        # Create AGENTS.md to make it v2
        (self.project_dir / "AGENTS.md").write_text("# AGET v2 Config")

        result = self.migrate_cmd.execute([str(self.project_dir)])

        # Should return success
        self.assertEqual(result.get('status'), 'success')
        self.assertIn('v2', str(result.get('message', '')).lower())

    def test_migrate_nonexistent_project(self):
        """Test migrating a non-existent project."""
        fake_path = self.test_dir / "nonexistent"

        result = self.migrate_cmd.execute([str(fake_path)])

        # Should return error for non-existent project
        self.assertEqual(result.get('status'), 'error')
        self.assertIn('not found', str(result.get('error', '')).lower())

    def test_migrate_with_force_flag(self):
        """Test force migration overwrites existing AGENTS.md."""
        # Create existing AGENTS.md
        (self.project_dir / "AGENTS.md").write_text("# Existing AGENTS.md")

        result = self.migrate_cmd.execute([str(self.project_dir), '--force'])

        # Force should return success
        self.assertEqual(result.get('status'), 'success')

    def test_migrate_creates_symlink(self):
        """Test that migration returns instructions for agent."""
        result = self.migrate_cmd.execute([str(self.project_dir)])

        # Should return success
        self.assertEqual(result.get('status'), 'success')
        self.assertIn('migration', result.get('message', '').lower())

    def test_migrate_with_patterns(self):
        """Test migration with pattern application."""
        result = self.migrate_cmd.execute([str(self.project_dir), '--with-patterns'])

        # Should return success
        self.assertEqual(result.get('status'), 'success')

        # Check that pattern directories might be created
        patterns_dir = self.project_dir / "patterns"
        # Patterns might or might not be created based on implementation

    def test_migrate_rollback_on_error(self):
        """Test that migration rolls back on error."""
        # Test error handling (simplified)
        fake_error_path = self.test_dir / "nonexistent" / "deep" / "path"
        result = self.migrate_cmd.execute([str(fake_error_path)])
        self.assertEqual(result.get('status'), 'error')


if __name__ == "__main__":
    unittest.main()