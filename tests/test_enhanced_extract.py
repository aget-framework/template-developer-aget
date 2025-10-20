"""
Test enhanced extract command with directory support.
"""

import json
import tempfile
from pathlib import Path

import pytest

from aget.config.commands.extract import ExtractCommand


class TestEnhancedExtract:
    """Test directory extraction enhancements."""

    def setup_method(self):
        """Set up test environment."""
        self.cmd = ExtractCommand()
        self.temp_dir = tempfile.mkdtemp()
        self.test_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_directory_basic(self):
        """Test extracting a basic directory structure."""
        # Create test directory with Python files
        src_dir = self.test_dir / "src"
        src_dir.mkdir()

        # Create some test files
        (src_dir / "module1.py").write_text("def hello(): return 'world'")
        (src_dir / "module2.py").write_text("class TestClass: pass")

        # Create subdirectory
        sub_dir = src_dir / "submodule"
        sub_dir.mkdir()
        (sub_dir / "helper.py").write_text("def helper(): return 42")

        # Extract directory
        result = self.cmd.extract_directory(
            source_dir=src_dir,
            target_dir=self.test_dir / "products",
            package_name="test-package",
            force=False,
            dry_run=False
        )

        assert result['success']
        assert result['files_extracted'] == 3

        # Verify structure
        package_dir = self.test_dir / "products" / "test-package"
        assert package_dir.exists()
        assert (package_dir / "setup.py").exists()
        assert (package_dir / "README.md").exists()
        assert (package_dir / "test_package").exists()

    def test_extract_directory_preserves_structure(self):
        """Test that directory extraction preserves structure."""
        # Create nested structure
        src_dir = self.test_dir / "src"
        src_dir.mkdir()

        # Create nested directories
        (src_dir / "data").mkdir()
        (src_dir / "data" / "loader.py").write_text("def load(): pass")
        (src_dir / "analysis").mkdir()
        (src_dir / "analysis" / "analyzer.py").write_text("def analyze(): pass")

        # Extract
        result = self.cmd.extract_directory(
            source_dir=src_dir,
            target_dir=self.test_dir / "products",
            package_name="nested-package",
            force=False,
            dry_run=False
        )

        assert result['success']

        # Check preserved structure
        pkg = self.test_dir / "products" / "nested-package" / "nested_package"
        assert (pkg / "data" / "loader.py").exists()
        assert (pkg / "analysis" / "analyzer.py").exists()
        assert (pkg / "data" / "__init__.py").exists()
        assert (pkg / "analysis" / "__init__.py").exists()

    def test_extract_directory_sanitizes_content(self):
        """Test that sensitive data is sanitized."""
        src_dir = self.test_dir / "src"
        src_dir.mkdir()

        # Create file with sensitive data
        sensitive_code = '''
api_key = "secret123"
token = "bearer_xyz"
password = "admin123"

def process():
    return api_key
'''
        (src_dir / "config.py").write_text(sensitive_code)

        # Extract
        result = self.cmd.extract_directory(
            source_dir=src_dir,
            target_dir=self.test_dir / "products",
            package_name="sanitized",
            force=False,
            dry_run=False
        )

        assert result['success']

        # Check sanitization
        extracted = (self.test_dir / "products" / "sanitized" / "sanitized" / "config.py")
        content = extracted.read_text()

        assert "secret123" not in content
        assert "REDACTED" in content
        assert "# This file was extracted from" in content

    def test_extract_directory_dry_run(self):
        """Test dry run mode."""
        src_dir = self.test_dir / "src"
        src_dir.mkdir()
        (src_dir / "test.py").write_text("print('test')")

        # Dry run
        result = self.cmd.extract_directory(
            source_dir=src_dir,
            target_dir=self.test_dir / "products",
            package_name="dry-run-test",
            force=False,
            dry_run=True
        )

        assert result['success']
        assert "[DRY RUN]" in result['message']

        # Verify nothing created
        assert not (self.test_dir / "products").exists()

    def test_extract_directory_handles_internal_deps(self):
        """Test handling of internal dependencies."""
        src_dir = self.test_dir / "src"
        src_dir.mkdir()

        # Create file with internal imports
        code_with_deps = '''
from workspace import helper
from outputs.generator import Generator
import workspace.utils

def process():
    return helper.do_something()
'''
        (src_dir / "processor.py").write_text(code_with_deps)

        # Should fail without force
        result = self.cmd.extract_directory(
            source_dir=src_dir,
            target_dir=self.test_dir / "products",
            package_name="with-deps",
            force=False,
            dry_run=False
        )

        assert not result['success']
        assert "internal dependencies" in result['error']

        # Should succeed with force
        result = self.cmd.extract_directory(
            source_dir=src_dir,
            target_dir=self.test_dir / "products",
            package_name="with-deps",
            force=True,
            dry_run=False
        )

        assert result['success']
        assert result['warnings']

    def test_extract_file_vs_directory(self):
        """Test that both file and directory extraction work."""
        src_dir = self.test_dir / "src"
        src_dir.mkdir()
        (src_dir / "single.py").write_text("def single(): pass")

        # Test file extraction
        args = [
            '--from', str(src_dir / "single.py"),
            '--to', str(self.test_dir / "products"),
            '--name', 'single-file'
        ]
        result = self.cmd.execute(args)
        assert result['success']

        # Test directory extraction
        args = [
            '--from', str(src_dir),
            '--to', str(self.test_dir / "products"),
            '--name', 'full-dir'
        ]
        result = self.cmd.execute(args)
        assert result['success']

        # Both should exist
        assert (self.test_dir / "products" / "single-file").exists()
        assert (self.test_dir / "products" / "full-dir").exists()