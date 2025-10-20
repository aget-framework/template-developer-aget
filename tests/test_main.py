"""
Tests for the __main__ module - AGET CLI entry point.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys

from aget.__main__ import AgetCLI, main
from aget import __version__


class TestAgetCLI(unittest.TestCase):
    """Test the main AGET CLI router."""

    def setUp(self):
        """Set up test fixtures."""
        self.cli = AgetCLI()

    def test_init(self):
        """Test CLI initialization."""
        cli = AgetCLI()
        self.assertIn('config', cli.modules)
        self.assertIsNotNone(cli.modules['config'])

    @patch('builtins.print')
    def test_show_version(self, mock_print):
        """Test version display."""
        result = self.cli.route_command(['--version'])

        self.assertEqual(result, 0)
        mock_print.assert_called_once()
        call_args = str(mock_print.call_args)
        self.assertIn('aget version', call_args)
        self.assertIn(__version__, call_args)

    @patch('builtins.print')
    def test_show_version_short_flag(self, mock_print):
        """Test version display with -v flag."""
        result = self.cli.route_command(['-v'])

        self.assertEqual(result, 0)
        mock_print.assert_called_once()

    @patch('builtins.print')
    def test_show_help(self, mock_print):
        """Test help display."""
        result = self.cli.route_command(['--help'])

        self.assertEqual(result, 0)
        mock_print.assert_called_once()
        call_args = str(mock_print.call_args)
        self.assertIn('AGET', call_args)
        self.assertIn('Usage:', call_args)
        self.assertIn('Commands:', call_args)

    @patch('builtins.print')
    def test_show_help_short_flag(self, mock_print):
        """Test help display with -h flag."""
        result = self.cli.route_command(['-h'])

        self.assertEqual(result, 0)
        mock_print.assert_called_once()

    @patch('builtins.print')
    def test_show_help_word(self, mock_print):
        """Test help display with 'help' command."""
        result = self.cli.route_command(['help'])

        self.assertEqual(result, 0)
        mock_print.assert_called_once()

    @patch('builtins.print')
    def test_no_arguments(self, mock_print):
        """Test behavior with no arguments."""
        result = self.cli.route_command([])

        self.assertEqual(result, 0)
        mock_print.assert_called_once()
        call_args = str(mock_print.call_args)
        self.assertIn('Usage:', call_args)

    def test_route_init_command(self):
        """Test routing 'init' command to config module."""
        mock_config = Mock()
        mock_config.handle.return_value = 0
        self.cli.modules['config'] = mock_config

        result = self.cli.route_command(['init', '--template', 'minimal'])

        self.assertEqual(result, 0)
        mock_config.handle.assert_called_once_with('init', ['--template', 'minimal'])

    def test_route_validate_command(self):
        """Test routing 'validate' command."""
        mock_config = Mock()
        mock_config.handle.return_value = 0
        self.cli.modules['config'] = mock_config

        result = self.cli.route_command(['validate'])

        mock_config.handle.assert_called_once_with('validate', [])

    def test_route_apply_command(self):
        """Test routing 'apply' command."""
        mock_config = Mock()
        mock_config.handle.return_value = 0
        self.cli.modules['config'] = mock_config

        result = self.cli.route_command(['apply', 'session/wake'])

        mock_config.handle.assert_called_once_with('apply', ['session/wake'])

    def test_route_rollback_command(self):
        """Test routing 'rollback' command."""
        mock_config = Mock()
        mock_config.handle.return_value = 0
        self.cli.modules['config'] = mock_config

        result = self.cli.route_command(['rollback'])

        mock_config.handle.assert_called_once_with('rollback', [])

    def test_route_list_command(self):
        """Test routing 'list' command."""
        mock_config = Mock()
        mock_config.handle.return_value = 0
        self.cli.modules['config'] = mock_config

        result = self.cli.route_command(['list'])

        mock_config.handle.assert_called_once_with('list', [])

    def test_route_evolution_command(self):
        """Test routing 'evolution' command."""
        mock_config = Mock()
        mock_config.handle.return_value = 0
        self.cli.modules['config'] = mock_config

        result = self.cli.route_command(['evolution', '--type', 'decision', 'Message'])

        mock_config.handle.assert_called_once_with('evolution', ['--type', 'decision', 'Message'])

    def test_route_extract_command(self):
        """Test routing 'extract' command."""
        mock_config = Mock()
        mock_config.handle.return_value = 0
        self.cli.modules['config'] = mock_config

        result = self.cli.route_command(['extract', '--from', 'workspace/', '--to', 'products/'])

        mock_config.handle.assert_called_once_with('extract', ['--from', 'workspace/', '--to', 'products/'])

    @patch('builtins.print')
    def test_unknown_command(self, mock_print):
        """Test handling of unknown command."""
        result = self.cli.route_command(['unknown'])

        # Should show error and help
        self.assertEqual(result, 0)  # show_help returns 0
        calls = mock_print.call_args_list
        self.assertEqual(len(calls), 2)

        # First call is error message
        self.assertIn("Unknown command 'unknown'", str(calls[0]))

        # Second call is help text
        self.assertIn('Usage:', str(calls[1]))

    def test_subcommand_routing_future(self):
        """Test subcommand routing (future v2.1+ feature)."""
        mock_module = Mock()
        mock_module.handle.return_value = 0
        self.cli.modules['track'] = mock_module

        # Hidden feature in v2.0
        result = self.cli.route_command(['track', 'todos', 'add'])

        mock_module.handle.assert_called_once_with('todos', ['add'])

    def test_subcommand_no_action(self):
        """Test subcommand with no action shows help."""
        mock_module = Mock()
        mock_module.show_help.return_value = 0
        self.cli.modules['config'] = mock_module

        result = self.cli.route_command(['config'])

        mock_module.show_help.assert_called_once()

    @patch('sys.argv', ['aget', 'init'])
    @patch('aget.__main__.AgetCLI')
    def test_main_entry_point(self, mock_cli_class):
        """Test main() entry point."""
        mock_cli = Mock()
        mock_cli.route_command.return_value = 0
        mock_cli_class.return_value = mock_cli

        result = main()

        self.assertEqual(result, 0)
        mock_cli.route_command.assert_called_once_with(['init'])

    @patch('sys.argv', ['aget'])
    @patch('aget.__main__.AgetCLI')
    def test_main_no_args(self, mock_cli_class):
        """Test main() with no arguments."""
        mock_cli = Mock()
        mock_cli.route_command.return_value = 0
        mock_cli_class.return_value = mock_cli

        result = main()

        self.assertEqual(result, 0)
        mock_cli.route_command.assert_called_once_with([])

    def test_all_v2_commands_routed(self):
        """Test all v2 commands are properly routed."""
        v2_commands = ['init', 'validate', 'apply', 'rollback', 'list', 'evolution', 'extract']

        mock_config = Mock()
        mock_config.handle.return_value = 0
        self.cli.modules['config'] = mock_config

        for command in v2_commands:
            mock_config.reset_mock()
            result = self.cli.route_command([command])

            self.assertEqual(result, 0)
            mock_config.handle.assert_called_once()
            self.assertEqual(mock_config.handle.call_args[0][0], command)


if __name__ == "__main__":
    unittest.main()