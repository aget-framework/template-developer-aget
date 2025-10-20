"""
Tests for the template installer
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_installer_imports():
    """Test that installer can be imported"""
    from installer.install import TemplateInstaller
    assert TemplateInstaller is not None


def test_installer_dry_run():
    """Test installer in dry-run mode"""
    from installer.install import TemplateInstaller

    with tempfile.TemporaryDirectory() as tmpdir:
        installer = TemplateInstaller(tmpdir, template='minimal', dry_run=True)
        success = installer.install()
        assert success is True

        # In dry-run, no files should be created
        claude_file = Path(tmpdir) / 'CLAUDE.md'
        assert not claude_file.exists()


def test_installer_minimal_template():
    """Test installing minimal template"""
    from installer.install import TemplateInstaller

    with tempfile.TemporaryDirectory() as tmpdir:
        installer = TemplateInstaller(tmpdir, template='minimal', dry_run=False)

        # Create minimal template if it doesn't exist
        template_dir = installer.source / 'templates' / 'minimal'
        template_dir.mkdir(parents=True, exist_ok=True)

        claude_template = template_dir / 'CLAUDE.md'
        if not claude_template.exists():
            claude_template.write_text("# Test Template\n{{PROJECT_NAME}}")

        # Run installation
        success = installer.install()
        assert success is True

        # Check that files were created
        claude_file = Path(tmpdir) / 'CLAUDE.md'
        scripts_dir = Path(tmpdir) / 'scripts'

        assert claude_file.exists() or scripts_dir.exists()


def test_installer_project_detection():
    """Test that installer detects project type correctly"""
    from installer.install import TemplateInstaller

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python project indicator
        requirements = Path(tmpdir) / 'requirements.txt'
        requirements.write_text("pytest\n")

        installer = TemplateInstaller(tmpdir, dry_run=True)

        # Create a test file to customize
        test_file = Path(tmpdir) / 'test.md'
        test_file.write_text("{{PROJECT_TYPE}}")

        installer.customize_file(test_file)

        content = test_file.read_text()
        assert "Python" in content


def test_installer_validates_target():
    """Test that installer validates target directory"""
    from installer.install import TemplateInstaller

    # Try to install to non-existent directory
    installer = TemplateInstaller('/nonexistent/path', dry_run=True)
    success = installer.install()
    assert success is False


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])