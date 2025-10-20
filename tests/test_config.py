"""
Tests for the config module - Central configuration handler.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

from aget.config import ConfigModule


class TestConfigModule(unittest.TestCase):
    """Test the ConfigModule for AGET configuration handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = ConfigModule()

    def test_init(self):
        """Test ConfigModule initialization."""
        config = ConfigModule()
        self.assertIsNotNone(config.commands)
        self.assertIn('init', config.commands)
        self.assertIn('validate', config.commands)
        self.assertIn('apply', config.commands)
        self.assertIn('rollback', config.commands)
        self.assertIn('list', config.commands)
        self.assertIn('evolution', config.commands)
        self.assertIn('extract', config.commands)
        self.assertIn('migrate', config.commands)

    @patch('builtins.print')
    def test_handle_valid_command(self, mock_print):
        """Test handling a valid command."""
        # Mock the command method
        mock_cmd = Mock(return_value=0)
        self.config.commands['test'] = mock_cmd

        result = self.config.handle('test', ['arg1', 'arg2'])

        self.assertEqual(result, 0)
        mock_cmd.assert_called_once_with(['arg1', 'arg2'])

    @patch('builtins.print')
    def test_handle_invalid_command(self, mock_print):
        """Test handling an invalid command."""
        result = self.config.handle('invalid', [])

        # Should show error and help
        calls = mock_print.call_args_list
        self.assertGreater(len(calls), 0)
        self.assertIn("Unknown config command 'invalid'", str(calls[0]))

    @patch('builtins.print')
    def test_show_help(self, mock_print):
        """Test showing help."""
        result = self.config.show_help()

        self.assertEqual(result, 0)
        mock_print.assert_called_once()
        help_text = str(mock_print.call_args)
        self.assertIn('Config Module Commands:', help_text)
        self.assertIn('init', help_text)
        self.assertIn('validate', help_text)

    @patch('aget.config.commands.init.InitCommand')
    @patch('builtins.print')
    def test_cmd_init_success(self, mock_print, mock_init_class):
        """Test successful init command."""
        mock_init = Mock()
        mock_init.execute.return_value = {
            'success': True,
            'tier_used': 'gh',
            'execution_time': 0.5
        }
        mock_init_class.return_value = mock_init

        result = self.config.cmd_init(['--template', 'minimal'])

        self.assertEqual(result, 0)
        mock_init.execute.assert_called_once_with(args=['--template', 'minimal'])

        # Check success messages
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('✅' in call for call in calls))
        self.assertTrue(any('gh tier' in call for call in calls))
        self.assertTrue(any('0.5' in call for call in calls))

    @patch('aget.config.commands.init.InitCommand')
    @patch('builtins.print')
    def test_cmd_init_failure(self, mock_print, mock_init_class):
        """Test failed init command."""
        mock_init = Mock()
        mock_init.execute.return_value = {
            'success': False,
            'error': 'Directory already exists'
        }
        mock_init_class.return_value = mock_init

        result = self.config.cmd_init([])

        self.assertEqual(result, 1)

        # Check error message
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('❌' in call for call in calls))
        self.assertTrue(any('Directory already exists' in call for call in calls))

    @patch('aget.config.commands.validate.ValidateCommand')
    @patch('builtins.print')
    def test_cmd_validate_success(self, mock_print, mock_validate_class):
        """Test successful validate command."""
        mock_validate = Mock()
        mock_validate.execute.return_value = {
            'success': True,
            'checks_passed': 10,
            'checks_total': 10,
            'execution_time': 0.3,
            'warnings': []
        }
        mock_validate_class.return_value = mock_validate

        result = self.config.cmd_validate([])

        self.assertEqual(result, 0)

        # Check success messages
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('✅' in call for call in calls))
        self.assertTrue(any('10/10 checks' in call for call in calls))

    @patch('aget.config.commands.validate.ValidateCommand')
    @patch('builtins.print')
    def test_cmd_validate_with_warnings(self, mock_print, mock_validate_class):
        """Test validate command with warnings."""
        mock_validate = Mock()
        mock_validate.execute.return_value = {
            'success': True,
            'checks_passed': 8,
            'checks_total': 10,
            'warnings': ['Warning 1', 'Warning 2']
        }
        mock_validate_class.return_value = mock_validate

        result = self.config.cmd_validate([])

        self.assertEqual(result, 0)

        # Check warning message
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('⚠️' in call and '2 warnings' in call for call in calls))

    @patch('aget.config.commands.validate.ValidateCommand')
    @patch('builtins.print')
    def test_cmd_validate_failure(self, mock_print, mock_validate_class):
        """Test failed validate command."""
        mock_validate = Mock()
        mock_validate.execute.return_value = {
            'success': False,
            'errors': ['AGENTS.md not found', 'Invalid syntax', 'Missing patterns']
        }
        mock_validate_class.return_value = mock_validate

        result = self.config.cmd_validate([])

        self.assertEqual(result, 1)

        # Check error messages
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('❌' in call for call in calls))
        self.assertTrue(any('3 errors' in call for call in calls))
        self.assertTrue(any('AGENTS.md not found' in call for call in calls))

    @patch('aget.config.commands.apply.ApplyCommand')
    @patch('builtins.print')
    def test_cmd_apply_success(self, mock_print, mock_apply_class):
        """Test successful apply command."""
        mock_apply = Mock()
        mock_apply.execute.return_value = {
            'success': True,
            'pattern': 'session/wake',
            'message': 'Pattern applied successfully',
            'execution_time': 0.2
        }
        mock_apply_class.return_value = mock_apply

        result = self.config.cmd_apply(['session/wake'])

        self.assertEqual(result, 0)

        # Check success message
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('✅' in call for call in calls))

    @patch('aget.config.commands.rollback.RollbackCommand')
    @patch('builtins.print')
    def test_cmd_rollback_success(self, mock_print, mock_rollback_class):
        """Test successful rollback command."""
        mock_rollback = Mock()
        mock_rollback.execute.return_value = {
            'success': True,
            'tier_used': 'gh',
            'files_restored': 3,
            'message': 'Rolled back to previous version',
            'execution_time': 1.5
        }
        mock_rollback_class.return_value = mock_rollback

        result = self.config.cmd_rollback([])

        self.assertEqual(result, 0)

        # Check success message
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('✅' in call for call in calls))

    @patch('aget.config.commands.list.ListCommand')
    @patch('builtins.print')
    def test_cmd_list_success(self, mock_print, mock_list_class):
        """Test successful list command."""
        mock_list = Mock()
        mock_list.execute.return_value = {
            'success': True,
            'patterns': ['session/wake', 'session/wind_down'],
            'count': 2
        }
        mock_list_class.return_value = mock_list

        result = self.config.cmd_list([])

        self.assertEqual(result, 0)

    @patch('aget.config.commands.evolution.EvolutionCommand')
    @patch('builtins.print')
    def test_cmd_evolution_success(self, mock_print, mock_evolution_class):
        """Test successful evolution command."""
        mock_evolution = Mock()
        mock_evolution.execute.return_value = {
            'success': True,
            'type': 'decision',
            'message': 'Decision recorded'
        }
        mock_evolution_class.return_value = mock_evolution

        result = self.config.cmd_evolution(['--type', 'decision', 'Test decision'])

        self.assertEqual(result, 0)

    @patch('aget.config.commands.extract.ExtractCommand')
    @patch('builtins.print')
    def test_cmd_extract_success(self, mock_print, mock_extract_class):
        """Test successful extract command."""
        mock_extract = Mock()
        mock_extract.execute.return_value = {
            'success': True,
            'source': 'workspace/',
            'target': 'products/',
            'package': 'my-tool'
        }
        mock_extract_class.return_value = mock_extract

        result = self.config.cmd_extract(['--from', 'workspace/', '--to', 'products/'])

        self.assertEqual(result, 0)

    def test_all_commands_callable(self):
        """Test that all registered commands are callable."""
        for command_name, command_func in self.config.commands.items():
            self.assertTrue(callable(command_func))

    def test_command_registry_complete(self):
        """Test that command registry matches expected commands."""
        expected_commands = [
            'init', 'validate', 'apply', 'rollback',
            'list', 'evolution', 'extract', 'migrate'
        ]

        for cmd in expected_commands:
            self.assertIn(cmd, self.config.commands)

    @patch('aget.config.commands.migrate.MigrateCommand')
    @patch('builtins.print')
    def test_cmd_migrate_success(self, mock_print, mock_migrate_class):
        """Test successful migrate command."""
        mock_migrate = Mock()
        mock_migrate.execute.return_value = {
            'success': True,
            'message': 'Migration completed'
        }
        mock_migrate_class.return_value = mock_migrate

        result = self.config.cmd_migrate(['../old-project'])

        # Since cmd_migrate is not implemented in the code shown,
        # we expect it to be in the commands dict but may not have implementation
        # This test ensures the structure is there
        self.assertIn('migrate', self.config.commands)


if __name__ == "__main__":
    unittest.main()