"""
Test suite for migration cleanup pattern.
Tests detection and archiving of migration artifacts.
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.housekeeping.migration_cleanup import MigrationCleanup


class TestMigrationCleanup:
    """Test migration cleanup pattern functionality."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project with migration artifacts."""
        project = tempfile.mkdtemp(prefix="test_migration_")

        # Create various migration artifacts
        artifacts = [
            # Claude backups
            'CLAUDE.md.backup',
            'CLAUDE.md.original',
            'CLAUDE.md.old',

            # Session orphans
            'SESSION_2025_09_20.md',
            'SESSION_2025_09_21.md',

            # Old configs
            '.claude_config',
            '.claude_settings',

            # Deprecated scripts
            'claude_setup.py',
            'claude_utils.sh',

            # Temp migration files
            'data_migration_20250920.tmp',
            'config.migrate'
        ]

        for artifact in artifacts:
            file_path = Path(project) / artifact
            file_path.write_text(f"# Test artifact: {artifact}\n")

        # Create some normal files that should not be cleaned
        normal_files = [
            'README.md',
            'AGENTS.md',
            'main.py',
            '.gitignore'
        ]

        for normal in normal_files:
            file_path = Path(project) / normal
            file_path.write_text(f"# Normal file: {normal}\n")

        yield project

        # Cleanup
        shutil.rmtree(project)

    def test_scan_for_artifacts(self, temp_project):
        """Test scanning for migration artifacts."""
        cleanup = MigrationCleanup(temp_project, dry_run=True)
        artifacts = cleanup.scan_for_artifacts()

        assert len(artifacts) > 0

        # Check categories are correctly identified
        categories = set(a['category'] for a in artifacts)
        assert 'claude_backups' in categories
        assert 'session_orphans' in categories
        assert 'old_configs' in categories
        assert 'deprecated_scripts' in categories
        assert 'temp_migrations' in categories

        # Check specific artifacts are found
        artifact_names = [a['path'].name for a in artifacts]
        assert 'CLAUDE.md.backup' in artifact_names
        assert 'SESSION_2025_09_20.md' in artifact_names
        assert '.claude_config' in artifact_names
        assert 'claude_setup.py' in artifact_names

        # Ensure normal files are not included
        assert 'README.md' not in artifact_names
        assert 'AGENTS.md' not in artifact_names
        assert 'main.py' not in artifact_names

    def test_dry_run_archive(self, temp_project):
        """Test dry run mode doesn't modify files."""
        cleanup = MigrationCleanup(temp_project, dry_run=True)
        cleanup.scan_for_artifacts()

        # Count files before
        files_before = list(Path(temp_project).glob('*'))
        files_before.extend(list(Path(temp_project).glob('.*')))

        # Run archive in dry run
        archived = cleanup.archive_artifacts()

        # Count files after
        files_after = list(Path(temp_project).glob('*'))
        files_after.extend(list(Path(temp_project).glob('.*')))

        # Files should not be moved in dry run
        assert len(files_before) == len(files_after)
        assert len(archived) > 0
        assert all('Would archive:' in str(a) for a in archived)

    def test_actual_archive(self, temp_project):
        """Test actual archiving moves files."""
        cleanup = MigrationCleanup(temp_project, dry_run=False)
        artifacts_found = cleanup.scan_for_artifacts()
        artifact_count = len(artifacts_found)

        # Perform actual archive
        archived = cleanup.archive_artifacts()

        assert len(archived) == artifact_count

        # Check artifacts are moved
        for artifact in artifacts_found:
            assert not artifact['path'].exists()

        # Check backup directory structure
        backup_dir = Path(temp_project) / '.aget' / 'backups'
        assert backup_dir.exists()

        # Find the created backup directory
        migration_dirs = list(backup_dir.glob('migration_*'))
        assert len(migration_dirs) == 1

        # Check manifest file
        manifest_file = migration_dirs[0] / 'manifest.json'
        assert manifest_file.exists()

        with open(manifest_file) as f:
            manifest = json.load(f)
            assert manifest['artifacts'] == artifact_count
            assert 'claude_backups' in manifest['categories']

    def test_category_organization(self, temp_project):
        """Test artifacts are organized by category."""
        cleanup = MigrationCleanup(temp_project, dry_run=False)
        cleanup.scan_for_artifacts()
        cleanup.archive_artifacts()

        backup_dir = Path(temp_project) / '.aget' / 'backups'
        migration_dir = list(backup_dir.glob('migration_*'))[0]

        # Check category directories exist
        assert (migration_dir / 'claude_backups').exists()
        assert (migration_dir / 'session_orphans').exists()
        assert (migration_dir / 'old_configs').exists()

        # Check files are in correct categories
        claude_backups = list((migration_dir / 'claude_backups').glob('*'))
        assert any('CLAUDE.md.backup' in str(f) for f in claude_backups)

    def test_empty_project(self):
        """Test cleanup on project with no artifacts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create only normal files
            (Path(tmpdir) / 'README.md').write_text("# Project")
            (Path(tmpdir) / 'main.py').write_text("print('hello')")

            cleanup = MigrationCleanup(tmpdir, dry_run=True)
            artifacts = cleanup.scan_for_artifacts()

            assert len(artifacts) == 0

            report = cleanup.report()
            assert "No migration artifacts found" in report

    def test_report_generation(self, temp_project):
        """Test report generation with artifacts."""
        cleanup = MigrationCleanup(temp_project, dry_run=True)
        cleanup.scan_for_artifacts()

        report = cleanup.report()

        assert "DRY RUN" in report
        assert "migration artifacts" in report
        assert "Claude Backups:" in report
        assert "Session Orphans:" in report
        assert "Total size:" in report
        assert "CLAUDE.md.backup" in report

    def test_size_calculation(self, temp_project):
        """Test correct size calculation of artifacts."""
        cleanup = MigrationCleanup(temp_project, dry_run=True)
        artifacts = cleanup.scan_for_artifacts()

        total_size = sum(a['size'] for a in artifacts)
        assert total_size > 0

        report = cleanup.report()
        assert f"{total_size:,} bytes" in report

    def test_artifact_patterns(self, temp_project):
        """Test all artifact pattern categories are detected."""
        # Create one file for each pattern category
        test_files = {
            'claude_backups': Path(temp_project) / 'CLAUDE.md.backup',
            'session_orphans': Path(temp_project) / 'SESSION_TEST.md',
            'old_configs': Path(temp_project) / '.claude_config',
            'deprecated_scripts': Path(temp_project) / 'claude_test.py',
            'temp_migrations': Path(temp_project) / 'test.migrate'
        }

        # Ensure all test files exist
        for category, file_path in test_files.items():
            if not file_path.exists():
                file_path.write_text(f"Test {category}")

        cleanup = MigrationCleanup(temp_project, dry_run=True)
        artifacts = cleanup.scan_for_artifacts()

        found_categories = set(a['category'] for a in artifacts)

        # All categories should be represented
        for category in test_files.keys():
            assert category in found_categories

    def test_backup_directory_creation(self, temp_project):
        """Test backup directory is created with proper structure."""
        cleanup = MigrationCleanup(temp_project, dry_run=False)
        cleanup.scan_for_artifacts()
        cleanup.archive_artifacts()

        backup_dir = Path(temp_project) / '.aget' / 'backups'
        assert backup_dir.exists()
        assert backup_dir.is_dir()

        # Check timestamp format in directory name
        migration_dirs = list(backup_dir.glob('migration_*'))
        assert len(migration_dirs) > 0

        dir_name = migration_dirs[0].name
        assert dir_name.startswith('migration_')
        # Check timestamp format (YYYYMMDD_HHMMSS)
        timestamp_part = dir_name.replace('migration_', '')
        assert len(timestamp_part) == 15  # 8 + 1 + 6
        assert timestamp_part[8] == '_'

    def test_preserve_normal_files(self, temp_project):
        """Test that normal files are not affected by cleanup."""
        # Track normal files
        normal_files = ['README.md', 'AGENTS.md', 'main.py', '.gitignore']

        cleanup = MigrationCleanup(temp_project, dry_run=False)
        cleanup.scan_for_artifacts()
        cleanup.archive_artifacts()

        # Check normal files still exist
        for normal_file in normal_files:
            file_path = Path(temp_project) / normal_file
            assert file_path.exists()
            assert file_path.read_text() == f"# Normal file: {normal_file}\n"

    def test_multiple_cleanup_runs(self, temp_project):
        """Test running cleanup multiple times."""
        # First cleanup
        cleanup1 = MigrationCleanup(temp_project, dry_run=False)
        artifacts1 = cleanup1.scan_for_artifacts()
        assert len(artifacts1) > 0
        cleanup1.archive_artifacts()

        # Second cleanup should find nothing
        cleanup2 = MigrationCleanup(temp_project, dry_run=False)
        artifacts2 = cleanup2.scan_for_artifacts()
        assert len(artifacts2) == 0

        # Check we have one backup
        backup_dir = Path(temp_project) / '.aget' / 'backups'
        migration_dirs = list(backup_dir.glob('migration_*'))
        assert len(migration_dirs) == 1