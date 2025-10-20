#!/usr/bin/env python3
"""
Cleanup Pattern - Remove temporary files, caches, and build artifacts.
"""

import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple


class CleanupProtocol:
    """Cleanup protocol for maintenance tasks."""

    def __init__(self, project_path: Path = Path.cwd()):
        """Initialize cleanup protocol."""
        self.project_path = Path(project_path)
        self.cleanup_patterns = {
            'python': [
                '__pycache__',
                '*.pyc',
                '*.pyo',
                '*.pyd',
                '.Python',
                'pip-log.txt',
                'pip-delete-this-directory.txt',
                '.pytest_cache',
                '.coverage',
                'htmlcov',
                '.tox',
                '*.egg-info',
                'dist',
                'build',
                '*.egg',
                '.mypy_cache',
                '.ruff_cache'
            ],
            'javascript': [
                'node_modules',
                'npm-debug.log*',
                'yarn-debug.log*',
                'yarn-error.log*',
                '.npm',
                '.yarn-integrity',
                '.cache',
                '.parcel-cache',
                '.next',
                'out',
                'dist',
                'build'
            ],
            'general': [
                '.DS_Store',
                'Thumbs.db',
                '*~',
                '*.swp',
                '*.swo',
                '*.log',
                '*.tmp',
                '*.temp',
                '*.bak',
                '*.backup',
                '*.old'
            ],
            'ide': [
                '.vscode',
                '.idea',
                '*.sublime-project',
                '*.sublime-workspace',
                '.project',
                '.classpath',
                '.settings'
            ]
        }

    def execute(self, dry_run: bool = True, categories: List[str] = None) -> Dict[str, Any]:
        """
        Execute cleanup protocol.

        Args:
            dry_run: If True, only report what would be cleaned
            categories: Specific categories to clean (default: all)

        Returns:
            Cleanup results including files found and space freed
        """
        result = {
            'dry_run': dry_run,
            'files_found': [],
            'directories_found': [],
            'space_to_free': 0,
            'errors': []
        }

        mode = "DRY RUN" if dry_run else "CLEANUP"
        print(f"🧹 {mode} - Housekeeping Cleanup")
        print("-" * 40)

        # Determine which categories to clean
        if categories is None:
            categories = list(self.cleanup_patterns.keys())

        # Scan for files to clean
        for category in categories:
            if category not in self.cleanup_patterns:
                continue

            patterns = self.cleanup_patterns[category]
            found = self._scan_category(category, patterns)

            for item, size in found:
                if item.is_dir():
                    result['directories_found'].append(str(item.relative_to(self.project_path)))
                else:
                    result['files_found'].append(str(item.relative_to(self.project_path)))
                result['space_to_free'] += size

        # Report findings
        total_items = len(result['files_found']) + len(result['directories_found'])

        if total_items == 0:
            print("✨ No cleanup needed - workspace is clean!")
            result['status'] = 'clean'
            return result

        print(f"Found {total_items} items to clean:")
        print(f"  📁 {len(result['directories_found'])} directories")
        print(f"  📄 {len(result['files_found'])} files")
        print(f"  💾 {self._format_size(result['space_to_free'])} to free")

        # Perform cleanup if not dry run
        if not dry_run:
            cleaned = self._perform_cleanup(
                result['files_found'],
                result['directories_found']
            )
            result['cleaned'] = cleaned
            print(f"\n✅ Cleaned {cleaned} items")
            result['status'] = 'cleaned'
        else:
            print(f"\nℹ️ Run without --dry-run to clean these items")
            result['status'] = 'preview'

        return result

    def _scan_category(self, category: str, patterns: List[str]) -> List[Tuple[Path, int]]:
        """Scan for files matching patterns in a category."""
        found = []

        for pattern in patterns:
            # Handle directory patterns
            if not any(c in pattern for c in ['*', '?', '[']):
                # It's a specific directory name
                for item in self.project_path.rglob(pattern):
                    if item.is_dir():
                        size = self._get_dir_size(item)
                        found.append((item, size))
            else:
                # It's a glob pattern
                for item in self.project_path.rglob(pattern):
                    if item.is_file():
                        size = item.stat().st_size
                        found.append((item, size))

        return found

    def _get_dir_size(self, directory: Path) -> int:
        """Calculate total size of a directory."""
        total = 0
        try:
            for item in directory.rglob('*'):
                if item.is_file():
                    total += item.stat().st_size
        except (PermissionError, OSError):
            pass
        return total

    def _format_size(self, size: int) -> str:
        """Format byte size in human-readable form."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def _perform_cleanup(self, files: List[str], directories: List[str]) -> int:
        """Actually delete files and directories."""
        cleaned = 0

        # Clean files first
        for file_path in files:
            try:
                full_path = self.project_path / file_path
                if full_path.exists():
                    full_path.unlink()
                    cleaned += 1
            except (PermissionError, FileNotFoundError, OSError):
                pass

        # Then clean directories
        for dir_path in directories:
            try:
                full_path = self.project_path / dir_path
                if full_path.exists():
                    shutil.rmtree(full_path)
                    cleaned += 1
            except (PermissionError, FileNotFoundError, OSError):
                pass

        return cleaned


def apply_pattern(project_path: Path = Path.cwd(), dry_run: bool = True) -> Dict[str, Any]:
    """
    Apply cleanup pattern to project.

    This is called by `aget apply housekeeping/cleanup`.
    """
    protocol = CleanupProtocol(project_path)

    # Check for common project types and clean accordingly
    has_python = any(project_path.glob("*.py"))
    has_js = (project_path / "package.json").exists()

    categories = ['general', 'ide']
    if has_python:
        categories.append('python')
    if has_js:
        categories.append('javascript')

    return protocol.execute(dry_run=dry_run, categories=categories)


if __name__ == "__main__":
    import sys
    # Check for --no-dry-run flag
    dry_run = "--no-dry-run" not in sys.argv
    apply_pattern(dry_run=dry_run)