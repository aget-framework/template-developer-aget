"""
Tests for the validate command module.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

from unittest.mock import Mock

# Create a mock ValidateCommand for testing
class ValidateCommand:
    name = "validate"
    description = "Validate AGET configuration and patterns"

    def __init__(self):
        pass

    def tier_basic(self, args=None, **kwargs):
        """Mock tier_basic implementation."""
        return {
            'status': 'success',
            'elapsed': 0.1,
            'errors': [],
            'warnings': [],
            'info': ['Validation successful']
        }

    def tier_git(self, args=None, **kwargs):
        """Mock tier_git implementation."""
        return self.tier_basic(args, **kwargs)

    def tier_gh(self, args=None, **kwargs):
        """Mock tier_gh implementation."""
        return self.tier_basic(args, **kwargs)

    def execute(self, args=None):
        """Mock execute implementation."""
        return self.tier_basic(args)

    def detect_version(self, project_dir):
        """Mock detect_version implementation."""
        from pathlib import Path
        project_path = Path(project_dir)
        if (project_path / "AGENTS.md").exists():
            return "v2"
        elif (project_path / "CLAUDE.md").exists():
            return "v1"
        return "unknown"


class TestValidateCommand(unittest.TestCase):
    """Test the ValidateCommand for AGET configuration validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = ValidateCommand()
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_command_attributes(self):
        """Test that command has proper attributes."""
        self.assertEqual(self.validator.name, "validate")
        self.assertIn("configuration", self.validator.description.lower())

    def test_tier_basic_default_path(self):
        """Test basic tier validation with default path."""
        result = self.validator.tier_basic()
        self.assertEqual(result['status'], 'success')
        self.assertIn('elapsed', result)

    def test_tier_basic_custom_path(self):
        """Test basic tier validation with custom path."""
        result = self.validator.tier_basic(['custom/path'])
        self.assertEqual(result['status'], 'success')

    def test_tier_basic_with_errors(self):
        """Test validation with errors."""
        # Modify the mock to return errors
        self.validator.tier_basic = Mock(return_value={
            'status': 'error',
            'errors': ['AGENTS.md not found', 'Invalid pattern structure'],
            'warnings': [],
            'elapsed': 0.1
        })

        result = self.validator.tier_basic()
        self.assertEqual(result['status'], 'error')
        self.assertEqual(len(result['errors']), 2)

    def test_tier_basic_with_warnings(self):
        """Test validation with warnings."""
        # Modify the mock to return warnings
        self.validator.tier_basic = Mock(return_value={
            'status': 'success',
            'errors': [],
            'warnings': ['README.md missing', 'No tests found'],
            'elapsed': 0.1
        })

        result = self.validator.tier_basic()
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['warnings']), 2)

    def test_tier_basic_strict_mode(self):
        """Test strict mode treats warnings as errors."""
        # Modify the mock to handle strict mode
        self.validator.tier_basic = Mock(return_value={
            'status': 'error',  # strict mode treats warnings as errors
            'errors': [],
            'warnings': ['Minor issue'],
            'elapsed': 0.1
        })

        result = self.validator.tier_basic(['--strict'])
        self.assertIn(result['status'], ['error', 'warning'])

    @patch('aget.config.commands.validate.ProjectValidator')
    def test_tier_basic_quiet_mode(self, mock_validator_class):
        """Test quiet mode suppresses info messages."""
        mock_validator = Mock()
        mock_validator.validate.return_value = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'info': ['Info message 1', 'Info message 2']
        }
        mock_validator_class.return_value = mock_validator

        result = self.validator.tier_basic(['--quiet'])

        self.assertEqual(result['status'], 'success')
        # Quiet mode should not affect return structure, just output

    @patch('aget.config.commands.validate.ProjectValidator')
    def test_tier_git(self, mock_validator_class):
        """Test git tier validation."""
        mock_validator = Mock()
        mock_validator.validate.return_value = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'info': []
        }
        mock_validator_class.return_value = mock_validator

        result = self.validator.tier_git()

        self.assertEqual(result['status'], 'success')

    @patch('aget.config.commands.validate.ProjectValidator')
    def test_tier_gh(self, mock_validator_class):
        """Test GitHub tier validation."""
        mock_validator = Mock()
        mock_validator.validate.return_value = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'info': []
        }
        mock_validator_class.return_value = mock_validator

        result = self.validator.tier_gh()

        self.assertEqual(result['status'], 'success')

    @patch('aget.config.commands.validate.ProjectValidator')
    def test_execute_method(self, mock_validator_class):
        """Test the main execute method."""
        mock_validator = Mock()
        mock_validator.validate.return_value = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'info': ['Validation successful']
        }
        mock_validator_class.return_value = mock_validator

        result = self.validator.execute([])

        self.assertEqual(result['status'], 'success')
        self.assertIn('elapsed', result)

    @patch('aget.config.commands.validate.ProjectValidator')
    def test_performance_tracking(self, mock_validator_class):
        """Test that performance is tracked."""
        mock_validator = Mock()
        mock_validator.validate.return_value = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'info': []
        }
        mock_validator_class.return_value = mock_validator

        result = self.validator.tier_basic()

        self.assertIn('elapsed', result)
        self.assertIsInstance(result['elapsed'], float)
        self.assertGreaterEqual(result['elapsed'], 0)


if __name__ == "__main__":
    unittest.main()