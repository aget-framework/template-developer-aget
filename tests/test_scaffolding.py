"""Tests for the scaffolding system in aget init."""

import json
import os
import tempfile
from pathlib import Path
import pytest
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aget.config.commands.init import InitCommand


class TestScaffolding:
    """Test scaffolding system with template options."""

    def setup_method(self):
        """Set up test environment."""
        self.init_cmd = InitCommand()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_template_options_available(self):
        """Test that all template options are defined."""
        expected_templates = ['minimal', 'standard', 'agent', 'tool', 'hybrid']
        assert all(t in self.init_cmd.templates for t in expected_templates)

    def test_minimal_template(self):
        """Test minimal template creates correct structure."""
        project_path = Path(self.temp_dir) / "test_minimal"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'minimal'])

        assert result['success'] is True
        assert result['template'] == 'minimal'
        assert (project_path / ".aget").exists()
        assert (project_path / ".aget/evolution").exists()
        assert (project_path / "AGENTS.md").exists()
        # Minimal should not have workspace or products
        assert not (project_path / "workspace").exists()
        assert not (project_path / "products").exists()

    def test_standard_template(self):
        """Test standard template creates correct structure."""
        project_path = Path(self.temp_dir) / "test_standard"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'standard'])

        assert result['success'] is True
        assert result['template'] == 'standard'
        assert (project_path / ".aget").exists()
        assert (project_path / "workspace").exists()
        assert (project_path / "data").exists()
        # Standard should not have products
        assert not (project_path / "products").exists()

    def test_agent_template(self):
        """Test agent template creates full structure."""
        project_path = Path(self.temp_dir) / "test_agent"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'agent'])

        assert result['success'] is True
        assert result['template'] == 'agent'

        # Check all expected directories
        expected_dirs = [
            ".aget", ".aget/evolution", ".aget/checkpoints",
            "src", "workspace", "products", "data",
            "docs", "tests"
        ]
        for dir_name in expected_dirs:
            assert (project_path / dir_name).exists(), f"Missing {dir_name}"

    def test_tool_template(self):
        """Test tool template creates appropriate structure."""
        project_path = Path(self.temp_dir) / "test_tool"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'tool'])

        assert result['success'] is True
        assert result['template'] == 'tool'
        assert (project_path / "src").exists()
        assert (project_path / "products").exists()
        assert (project_path / "docs").exists()
        assert (project_path / "tests").exists()
        # Tool should not have workspace
        assert not (project_path / "workspace").exists()

    def test_hybrid_template(self):
        """Test hybrid template combines agent and tool structures."""
        project_path = Path(self.temp_dir) / "test_hybrid"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'hybrid'])

        assert result['success'] is True
        assert result['template'] == 'hybrid'
        assert (project_path / "workspace").exists()
        assert (project_path / "products").exists()
        assert (project_path / "examples").exists()

    def test_readme_files_created(self):
        """Test that README files are created in appropriate directories."""
        project_path = Path(self.temp_dir) / "test_readme"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'agent'])

        assert result['success'] is True

        # Check for README files
        readme_dirs = ['workspace', 'products', 'src', '.aget/evolution',
                      'data', 'tests', 'docs']
        for dir_name in readme_dirs:
            readme_path = project_path / dir_name / "README.md"
            assert readme_path.exists(), f"Missing README in {dir_name}"

            # Verify content is not empty
            content = readme_path.read_text()
            assert len(content) > 0, f"Empty README in {dir_name}"

    def test_agents_md_content(self):
        """Test AGENTS.md contains correct template information."""
        project_path = Path(self.temp_dir) / "test_agents_md"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'agent'])

        agents_md = project_path / "AGENTS.md"
        content = agents_md.read_text()

        assert "agent template" in content
        assert "workspace/" in content
        assert "products/" in content
        assert ".aget/evolution/" in content

    def test_version_file_includes_template(self):
        """Test version.json includes template information."""
        project_path = Path(self.temp_dir) / "test_version"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'tool'])

        version_file = project_path / ".aget" / "version.json"
        assert version_file.exists()

        version_data = json.loads(version_file.read_text())
        assert version_data['template'] == 'tool'

    def test_invalid_template_rejected(self):
        """Test that invalid template names are rejected."""
        project_path = Path(self.temp_dir) / "test_invalid"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'invalid'])

        assert result['success'] is False
        assert 'Invalid template' in result['error']

    def test_default_template_is_standard(self):
        """Test that standard is the default template."""
        project_path = Path(self.temp_dir) / "test_default"
        project_path.mkdir()
        os.chdir(project_path)

        # No --template argument
        result = self.init_cmd.tier_basic(args=[])

        assert result['success'] is True
        assert result['template'] == 'standard'

    def test_workspace_products_distinction(self):
        """Test that workspace and products directories have distinct READMEs."""
        project_path = Path(self.temp_dir) / "test_distinction"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_basic(args=['--template', 'agent'])

        workspace_readme = (project_path / "workspace" / "README.md").read_text()
        products_readme = (project_path / "products" / "README.md").read_text()

        assert "private workspace" in workspace_readme
        assert "NOT intended for public use" in workspace_readme
        assert "Public" in products_readme
        assert "ready for public use" in products_readme

    def test_gitignore_updated_for_template(self):
        """Test that .gitignore is updated based on template."""
        project_path = Path(self.temp_dir) / "test_gitignore"
        project_path.mkdir()
        os.chdir(project_path)

        result = self.init_cmd.tier_git(args=['--template', 'agent'])

        gitignore = project_path / ".gitignore"
        assert gitignore.exists()

        content = gitignore.read_text()
        assert "workspace/.tmp/" in content
        assert "workspace/*.log" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])