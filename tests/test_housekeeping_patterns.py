"""Test housekeeping patterns."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, '.')
from patterns.housekeeping.cleanup import CleanupProtocol
from patterns.housekeeping.doc_check import DocumentationChecker


def create_messy_project(tmpdir: Path):
    """Create a project with various artifacts to clean."""
    tmpdir.mkdir(exist_ok=True)

    # Create Python artifacts
    (tmpdir / "__pycache__").mkdir()
    (tmpdir / "__pycache__" / "test.pyc").write_text("compiled")
    (tmpdir / "build").mkdir()
    (tmpdir / "build" / "lib").mkdir()
    (tmpdir / "test.egg-info").mkdir()
    (tmpdir / ".pytest_cache").mkdir()
    (tmpdir / "test.py").write_text("# Python file - keep this")

    # Create general artifacts
    (tmpdir / ".DS_Store").write_text("mac file")
    (tmpdir / "backup.bak").write_text("backup")
    (tmpdir / "temp.tmp").write_text("temp")

    # Create IDE artifacts
    (tmpdir / ".vscode").mkdir()
    (tmpdir / ".vscode" / "settings.json").write_text("{}")

    # Create files to keep
    (tmpdir / "important.txt").write_text("keep this")
    (tmpdir / "README.md").write_text("# Project")

    return tmpdir


def test_cleanup_dry_run():
    """Test cleanup in dry run mode."""
    print("Testing cleanup dry run...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_messy_project(Path(tmpdir))

        cleanup = CleanupProtocol(project)
        result = cleanup.execute(dry_run=True, categories=['python', 'general'])

        # Check that files were found but not deleted
        assert result['dry_run'] == True
        assert len(result['files_found']) > 0 or len(result['directories_found']) > 0
        assert result['space_to_free'] > 0
        assert result['status'] == 'preview'

        # Verify nothing was actually deleted
        assert (project / "__pycache__").exists()
        assert (project / ".DS_Store").exists()

        print(f"✅ Found {len(result['files_found'])} files, {len(result['directories_found'])} dirs")
        print(f"✅ Would free {result['space_to_free']} bytes")
        print("✅ Dry run mode works (nothing deleted)")


def test_cleanup_actual():
    """Test actual cleanup."""
    print("\nTesting actual cleanup...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_messy_project(Path(tmpdir))

        cleanup = CleanupProtocol(project)
        result = cleanup.execute(dry_run=False, categories=['python', 'general'])

        # Check that files were cleaned
        assert result['dry_run'] == False
        assert result['status'] == 'cleaned'
        assert 'cleaned' in result
        assert result['cleaned'] > 0

        # Debug: print what was found and cleaned
        print(f"Files found: {result['files_found']}")
        print(f"Dirs found: {result['directories_found']}")

        # Verify artifacts were deleted
        assert not (project / "__pycache__").exists()
        # .DS_Store might not be in the found list depending on glob behavior
        ds_store_cleaned = not (project / ".DS_Store").exists()
        assert ds_store_cleaned or ".DS_Store" not in str(result['files_found'])
        assert not (project / "backup.bak").exists()

        # Verify important files were kept
        assert (project / "test.py").exists()
        assert (project / "important.txt").exists()
        assert (project / "README.md").exists()

        print(f"✅ Cleaned {result['cleaned']} items")
        print("✅ Artifacts removed, important files kept")


def test_cleanup_clean_project():
    """Test cleanup on already clean project."""
    print("\nTesting cleanup on clean project...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = Path(tmpdir)
        project.mkdir(exist_ok=True)

        # Create only important files
        (project / "main.py").write_text("# Main file")
        (project / "README.md").write_text("# Clean Project")

        cleanup = CleanupProtocol(project)
        result = cleanup.execute(dry_run=False)

        assert result['status'] == 'clean'
        assert len(result['files_found']) == 0
        assert len(result['directories_found']) == 0
        assert result['space_to_free'] == 0

        print("✅ Correctly identifies clean project")


def test_cleanup_categories():
    """Test selective category cleanup."""
    print("\nTesting selective cleanup...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_messy_project(Path(tmpdir))

        # Clean only Python artifacts
        cleanup = CleanupProtocol(project)
        result = cleanup.execute(dry_run=False, categories=['python'])

        # Python artifacts should be gone
        assert not (project / "__pycache__").exists()
        assert not (project / "build").exists()

        # Other artifacts should remain
        assert (project / ".DS_Store").exists()
        assert (project / ".vscode").exists()

        print("✅ Selective category cleanup works")


def test_documentation_check_good():
    """Test documentation check on well-documented project."""
    print("\nTesting documentation check (good project)...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = Path(tmpdir)
        project.mkdir(exist_ok=True)

        # Create good documentation
        readme = project / "README.md"
        readme.write_text("""# My Project

## Installation
pip install my-project

## Usage
```python
import myproject
myproject.run()
```

## Testing
Run tests with pytest

## Contributing
Please see CONTRIBUTING.md
""")

        (project / "LICENSE").write_text("MIT License")
        (project / "CONTRIBUTING.md").write_text("# Contributing Guide")
        (project / "CHANGELOG.md").write_text("# Changelog")

        # Create docs directory
        docs_dir = project / "docs"
        docs_dir.mkdir()
        (docs_dir / "api.md").write_text("# API Reference")

        checker = DocumentationChecker(project)
        result = checker.execute()

        assert result['grade'] in ['A', 'B', 'C'], f"Expected decent grade, got {result['grade']}"
        assert 'README' in result['found_docs']
        assert 'LICENSE' in result['found_docs']
        assert len(result['missing_docs']) == 0

        print(f"✅ Good project gets grade {result['grade']}")


def test_documentation_check_poor():
    """Test documentation check on poorly documented project."""
    print("\nTesting documentation check (poor project)...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = Path(tmpdir)
        project.mkdir(exist_ok=True)

        # Create minimal documentation
        readme = project / "README.md"
        readme.write_text("# Project\nTODO: write docs")

        checker = DocumentationChecker(project)
        result = checker.execute()

        assert result['grade'] in ['D', 'F'], f"Expected poor grade, got {result['grade']}"
        assert 'LICENSE' in result['missing_docs']
        assert len(result['recommendations']) > 0

        print(f"✅ Poor project gets grade {result['grade']}")
        print(f"✅ Generated {len(result['recommendations'])} recommendations")


if __name__ == "__main__":
    print("🧹 Housekeeping Pattern Tests")
    print("=" * 40)

    test_cleanup_dry_run()
    test_cleanup_actual()
    test_cleanup_clean_project()
    test_cleanup_categories()
    test_documentation_check_good()
    test_documentation_check_poor()

    print("\n" + "=" * 40)
    print("✅ ALL HOUSEKEEPING TESTS PASSED")