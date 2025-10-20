"""Tests for the evolution tracking system."""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
import pytest
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aget.config.commands.evolution import EvolutionCommand


class TestEvolution:
    """Test evolution tracking functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.evolution_cmd = EvolutionCommand()
        self.temp_dir = tempfile.mkdtemp()
        try:
            self.original_cwd = os.getcwd()
        except FileNotFoundError:
            # Handle case where current directory doesn't exist
            self.original_cwd = Path.home()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_evolution_types_defined(self):
        """Test that all evolution types are defined."""
        expected_types = ['decision', 'discovery', 'extraction', 'learning']
        assert all(t in self.evolution_cmd.evolution_types for t in expected_types)

    def test_add_decision_entry(self):
        """Test adding a decision entry."""
        result = self.evolution_cmd.execute([
            '--type', 'decision', 'Use new architecture pattern'
        ])

        assert result['success'] is True
        assert 'Created decision entry' in result['message']
        assert '.aget/evolution/' in result['file']

        # Check file was created
        evolution_dir = Path(self.temp_dir) / '.aget' / 'evolution'
        assert evolution_dir.exists()

        md_files = list(evolution_dir.glob('*-DEC.md'))
        assert len(md_files) == 1

    def test_add_discovery_entry(self):
        """Test adding a discovery entry."""
        result = self.evolution_cmd.execute([
            '--type', 'discovery', 'Found optimization opportunity'
        ])

        assert result['success'] is True
        assert 'Created discovery entry' in result['message']

        # Check file content
        evolution_dir = Path(self.temp_dir) / '.aget' / 'evolution'
        md_files = list(evolution_dir.glob('*-DISC.md'))
        assert len(md_files) == 1

        content = md_files[0].read_text()
        assert 'Found optimization opportunity' in content
        assert 'Discovery' in content

    def test_add_extraction_entry(self):
        """Test adding an extraction entry."""
        result = self.evolution_cmd.execute([
            '--type', 'extraction', 'Moved tool to products directory'
        ])

        assert result['success'] is True
        assert 'Created extraction entry' in result['message']

        # Check file uses correct prefix
        evolution_dir = Path(self.temp_dir) / '.aget' / 'evolution'
        md_files = list(evolution_dir.glob('*-EXT.md'))
        assert len(md_files) == 1

    def test_add_learning_entry(self):
        """Test adding a learning entry."""
        result = self.evolution_cmd.execute([
            '--type', 'learning', 'Tests should run in parallel'
        ])

        assert result['success'] is True
        assert 'Created learning entry' in result['message']

        evolution_dir = Path(self.temp_dir) / '.aget' / 'evolution'
        md_files = list(evolution_dir.glob('*-LEARN.md'))
        assert len(md_files) == 1

    def test_invalid_type_rejected(self):
        """Test that invalid evolution types are rejected."""
        result = self.evolution_cmd.execute([
            '--type', 'invalid', 'Some message'
        ])

        assert result['success'] is False
        assert 'Invalid type' in result['error']

    def test_list_entries(self):
        """Test listing evolution entries."""
        # Create some entries
        self.evolution_cmd.execute(['--type', 'decision', 'First decision'])
        self.evolution_cmd.execute(['--type', 'discovery', 'First discovery'])
        self.evolution_cmd.execute(['--type', 'learning', 'First learning'])

        # List entries
        result = self.evolution_cmd.execute(['--list'])

        assert result['success'] is True
        assert 'Recent Evolution Entries' in result['message']
        assert 'decision' in result['message']
        assert 'discovery' in result['message']
        assert 'learning' in result['message']

    def test_list_with_count(self):
        """Test listing entries with specific count."""
        # Create 5 entries
        for i in range(5):
            self.evolution_cmd.execute(['--type', 'decision', f'Decision {i}'])

        # List only 3
        result = self.evolution_cmd.execute(['--list', '3'])

        assert result['success'] is True
        # Should show "showing 3 of 5"
        assert 'showing 3' in result['message']

    def test_search_entries(self):
        """Test searching evolution entries."""
        # Create entries with different content
        self.evolution_cmd.execute(['--type', 'decision', 'Use workspace directory'])
        self.evolution_cmd.execute(['--type', 'discovery', 'Found performance issue'])
        self.evolution_cmd.execute(['--type', 'learning', 'Workspace organization matters'])

        # Search for 'workspace'
        result = self.evolution_cmd.execute(['--search', 'workspace'])

        assert result['success'] is True
        assert result['matches'] == 2
        assert 'workspace' in result['message'].lower()

    def test_search_no_results(self):
        """Test searching with no matches."""
        self.evolution_cmd.execute(['--type', 'decision', 'Some decision'])

        result = self.evolution_cmd.execute(['--search', 'nonexistent'])

        assert result['success'] is True
        assert 'No entries found' in result['message']

    def test_help_command(self):
        """Test evolution help output."""
        result = self.evolution_cmd.execute(['--help'])

        assert result['success'] is True
        assert 'Evolution Command' in result['message']
        assert 'decision' in result['message']
        assert 'discovery' in result['message']
        assert 'extraction' in result['message']
        assert 'learning' in result['message']

    def test_index_file_created(self):
        """Test that index.json is created and updated."""
        # Add an entry
        self.evolution_cmd.execute(['--type', 'decision', 'Test decision'])

        # Check index file
        index_file = Path(self.temp_dir) / '.aget' / 'evolution' / 'index.json'
        assert index_file.exists()

        index_data = json.loads(index_file.read_text())
        assert 'entries' in index_data
        assert 'stats' in index_data
        assert index_data['stats']['total'] == 1
        assert index_data['stats']['by_type']['decision'] == 1

    def test_index_updated_on_multiple_entries(self):
        """Test that index is properly updated with multiple entries."""
        # Add multiple entries of different types
        self.evolution_cmd.execute(['--type', 'decision', 'Decision 1'])
        self.evolution_cmd.execute(['--type', 'decision', 'Decision 2'])
        self.evolution_cmd.execute(['--type', 'discovery', 'Discovery 1'])

        # Check index
        index_file = Path(self.temp_dir) / '.aget' / 'evolution' / 'index.json'
        index_data = json.loads(index_file.read_text())

        assert index_data['stats']['total'] == 3
        assert index_data['stats']['by_type']['decision'] == 2
        assert index_data['stats']['by_type']['discovery'] == 1
        assert len(index_data['entries']) == 3

    def test_filename_format(self):
        """Test that filenames follow expected format."""
        result = self.evolution_cmd.execute(['--type', 'decision', 'Test'])

        # Extract filename from result
        filepath = Path(result['file'])
        filename = filepath.name

        # Check format: YYYY-MM-DD-HHMMSS-MICROSEC-PREFIX.md
        parts = filename.replace('.md', '').split('-')
        assert len(parts) >= 6
        assert parts[5] == 'DEC'  # Decision prefix (after microseconds)

        # Check date format
        date_str = f"{parts[0]}-{parts[1]}-{parts[2]}"
        datetime.strptime(date_str, '%Y-%m-%d')  # Should not raise

    def test_title_truncation(self):
        """Test that long titles are properly truncated."""
        long_message = "This is a very long decision message that should be truncated in the title but preserved in the content section"

        result = self.evolution_cmd.execute(['--type', 'decision', long_message])

        # Read the created file
        filepath = Path(result['file'])
        content = filepath.read_text()

        # Title should be truncated
        lines = content.split('\n')
        title_line = lines[0]
        assert '...' in title_line

        # Full content should be preserved
        assert long_message in content

    def test_empty_evolution_directory(self):
        """Test handling of empty evolution directory."""
        result = self.evolution_cmd.execute(['--list'])

        assert result['success'] is True
        assert 'No evolution entries found' in result['message']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])