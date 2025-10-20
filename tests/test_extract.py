"""Tests for the bridge extract command."""

import os
import tempfile
from pathlib import Path
import pytest
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aget.config.commands.extract import ExtractCommand


class TestExtract:
    """Test bridge extraction functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.extract_cmd = ExtractCommand()
        self.temp_dir = tempfile.mkdtemp()
        try:
            self.original_cwd = os.getcwd()
        except FileNotFoundError:
            # Handle case where current directory doesn't exist
            self.original_cwd = Path.home()
        os.chdir(self.temp_dir)

        # Create workspace directory
        self.workspace_dir = Path(self.temp_dir) / 'workspace'
        self.workspace_dir.mkdir()

        # Create products directory
        self.products_dir = Path(self.temp_dir) / 'products'
        self.products_dir.mkdir()

        # Create evolution directory for tracking
        evolution_dir = Path(self.temp_dir) / '.aget' / 'evolution'
        evolution_dir.mkdir(parents=True)

    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def create_test_file(self, filename: str, content: str) -> Path:
        """Create a test file in workspace."""
        filepath = self.workspace_dir / filename
        filepath.write_text(content)
        return filepath

    def test_help_command(self):
        """Test extract help output."""
        result = self.extract_cmd.execute(['--help'])

        assert result['success'] is True
        assert 'Extract Command' in result['message']
        assert '--from' in result['message']
        assert '--auto' in result['message']

    def test_extract_simple_file(self):
        """Test extracting a simple Python file."""
        content = '''"""Simple tool for testing."""

def hello():
    """Say hello."""
    print("Hello, World!")

def main():
    hello()

if __name__ == "__main__":
    main()
'''
        self.create_test_file('simple.py', content)

        result = self.extract_cmd.execute([
            '--from', 'workspace/simple.py',
            '--to', 'products/'
        ])

        assert result['success'] is True
        assert 'files_created' in result
        assert len(result['files_created']) == 4

        # Check package was created
        package_dir = self.products_dir / 'simple'
        assert package_dir.exists()
        assert (package_dir / 'simple.py').exists()
        assert (package_dir / 'setup.py').exists()
        assert (package_dir / 'README.md').exists()
        assert (package_dir / '__init__.py').exists()

    def test_sanitize_sensitive_data(self):
        """Test that sensitive data is sanitized."""
        content = '''"""Tool with secrets."""

API_KEY = "sk-secret-12345"
token = "github_pat_xyz"
password = "admin123"
secret = "top_secret"

def process():
    return API_KEY
'''
        self.create_test_file('sensitive.py', content)

        result = self.extract_cmd.execute([
            '--from', 'workspace/sensitive.py',
            '--to', 'products/'
        ])

        assert result['success'] is True
        assert 'warnings' in result
        assert any('sensitive data' in w.lower() for w in result['warnings'])

        # Check sanitization
        extracted_file = self.products_dir / 'sensitive' / 'sensitive.py'
        extracted_content = extracted_file.read_text()

        assert 'sk-secret-12345' not in extracted_content
        assert 'github_pat_xyz' not in extracted_content
        assert 'admin123' not in extracted_content
        assert 'REDACTED' in extracted_content

    def test_reject_internal_dependencies(self):
        """Test that files with internal dependencies are rejected."""
        content = '''"""Tool with internal deps."""

from workspace import helper
from outputs.utils import process

def main():
    helper.run()
    process()
'''
        self.create_test_file('internal.py', content)

        result = self.extract_cmd.execute([
            '--from', 'workspace/internal.py',
            '--to', 'products/'
        ])

        assert result['success'] is False
        assert 'internal dependencies' in result['error'].lower()
        assert 'internal_deps' in result

    def test_force_extraction_with_warnings(self):
        """Test forcing extraction despite warnings."""
        content = '''"""Tool with internal deps."""

from workspace import helper

def main():
    print("Running")
'''
        self.create_test_file('force.py', content)

        result = self.extract_cmd.execute([
            '--from', 'workspace/force.py',
            '--to', 'products/',
            '--force'
        ])

        assert result['success'] is True
        assert (self.products_dir / 'force').exists()

    def test_custom_package_name(self):
        """Test extraction with custom package name."""
        content = '''"""Custom named tool."""

def main():
    print("Custom")
'''
        self.create_test_file('tool.py', content)

        result = self.extract_cmd.execute([
            '--from', 'workspace/tool.py',
            '--to', 'products/',
            '--name', 'my-custom-tool'
        ])

        assert result['success'] is True
        assert (self.products_dir / 'my-custom-tool').exists()
        assert (self.products_dir / 'my-custom-tool' / 'my_custom_tool.py').exists()

    def test_dry_run_mode(self):
        """Test dry run doesn't create files."""
        content = '''"""Dry run test."""

def main():
    pass
'''
        self.create_test_file('dryrun.py', content)

        result = self.extract_cmd.execute([
            '--from', 'workspace/dryrun.py',
            '--to', 'products/',
            '--dry-run'
        ])

        assert result['success'] is True
        assert '[DRY RUN]' in result['message']
        assert not (self.products_dir / 'dryrun').exists()

    def test_auto_discover_empty(self):
        """Test auto-discover with no Python files."""
        # workspace is empty
        result = self.extract_cmd.execute(['--auto'])

        assert result['success'] is True
        assert 'No Python files found' in result['message']

    def test_auto_discover_candidates(self):
        """Test auto-discover finds extractable candidates."""
        # Create extractable file
        good_content = '''"""Good tool."""

def main():
    print("Hello")

if __name__ == "__main__":
    main()
'''
        self.create_test_file('good.py', good_content)

        # Create non-extractable file
        bad_content = '''"""Bad tool."""

from workspace import helper
from outputs import utils

def process():
    helper.run()
'''
        self.create_test_file('bad.py', bad_content)

        result = self.extract_cmd.execute(['--auto'])

        assert result['success'] is True
        assert result['candidates'] >= 1
        assert 'good.py' in result['message']

    def test_analyze_file_detects_main(self):
        """Test that analyze_file detects main function."""
        content = '''"""Test main detection."""

def helper():
    pass

def main():
    """Main entry point."""
    helper()

if __name__ == "__main__":
    main()
'''
        filepath = self.create_test_file('main_test.py', content)

        analysis = self.extract_cmd.analyze_file(filepath)

        assert analysis['has_main'] is True
        assert analysis['description'] == 'Test main detection.'

    def test_analyze_file_detects_imports(self):
        """Test that analyze_file correctly categorizes imports."""
        content = '''"""Import test."""

import os
import sys
from pathlib import Path

import requests
import numpy as np

from workspace import helper
from outputs.utils import process
'''
        filepath = self.create_test_file('imports.py', content)

        analysis = self.extract_cmd.analyze_file(filepath)

        assert analysis['has_internal_deps'] is True
        assert 'workspace' in analysis['internal_deps']
        assert 'outputs.utils' in analysis['internal_deps']
        assert 'requests' in analysis['external_deps']
        assert 'numpy' in analysis['external_deps']

    def test_generated_setup_py(self):
        """Test that setup.py is properly generated."""
        content = '''"""Package for testing."""

import requests

def main():
    pass
'''
        self.create_test_file('package.py', content)

        result = self.extract_cmd.execute([
            '--from', 'workspace/package.py',
            '--to', 'products/'
        ])

        setup_py = self.products_dir / 'package' / 'setup.py'
        assert setup_py.exists()

        setup_content = setup_py.read_text()
        assert 'name="package"' in setup_content
        assert 'setuptools' in setup_content
        assert 'python_requires' in setup_content

    def test_generated_readme(self):
        """Test that README.md is properly generated."""
        content = '''"""A test package for documentation."""

def main():
    """CLI entry point."""
    pass
'''
        self.create_test_file('doc_test.py', content)

        result = self.extract_cmd.execute([
            '--from', 'workspace/doc_test.py',
            '--to', 'products/'
        ])

        readme = self.products_dir / 'doc-test' / 'README.md'
        assert readme.exists()

        readme_content = readme.read_text()
        assert '# doc-test' in readme_content
        assert 'Origin' in readme_content
        assert 'Installation' in readme_content
        assert 'doc_test.py' in readme_content

    def test_file_not_found(self):
        """Test error when source file doesn't exist."""
        result = self.extract_cmd.execute([
            '--from', 'workspace/nonexistent.py',
            '--to', 'products/'
        ])

        assert result['success'] is False
        assert 'not found' in result['error'].lower()

    def test_non_python_file_rejected(self):
        """Test that non-Python files are rejected."""
        self.create_test_file('data.json', '{"key": "value"}')

        result = self.extract_cmd.execute([
            '--from', 'workspace/data.json',
            '--to', 'products/'
        ])

        assert result['success'] is False
        assert 'Only Python files' in result['error']

    def test_extraction_header_added(self):
        """Test that extraction header is added to sanitized files."""
        content = '''"""Simple file."""

def hello():
    pass
'''
        self.create_test_file('header.py', content)

        result = self.extract_cmd.execute([
            '--from', 'workspace/header.py',
            '--to', 'products/'
        ])

        extracted = self.products_dir / 'header' / 'header.py'
        extracted_content = extracted.read_text()

        assert 'This file was extracted from workspace/' in extracted_content
        assert 'Generated by AGET extract command' in extracted_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])