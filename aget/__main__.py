"""
AGET v2 Main Entry Point
Future-ready architecture supporting subcommand expansion.
"""

import sys
from typing import List, Optional

from aget import __version__
from aget.config import ConfigModule


class AgetCLI:
    """
    Main CLI router with future-ready architecture.

    v2.0: All commands route through 'config' module
    v2.1+: Subcommand structure (config, track, gate, ship)
    """

    def __init__(self):
        """Initialize with module registry."""
        self.modules = {
            'config': ConfigModule(),
            # Future modules (not in v2.0):
            # 'track': TrackModule(),
            # 'gate': GateModule(),
            # 'ship': ShipModule(),
        }

    def route_command(self, args: List[str]) -> int:
        """
        Route commands to appropriate module.

        v2.0 behavior: Direct commands (init, validate, apply, rollback, list)
        v2.1+ behavior: Subcommands (config init, track todos, etc.)
        """
        if not args:
            return self.show_help()

        command = args[0]

        # Handle version flag
        if command in ['--version', '-v']:
            print(f"aget version {__version__}")
            return 0

        # Handle help flag
        if command in ['--help', '-h', 'help']:
            return self.show_help()

        # v2.0: Direct command routing (backward compatible)
        v2_commands = ['init', 'validate', 'apply', 'rollback', 'list', 'evolution', 'extract']
        if command in v2_commands:
            return self.modules['config'].handle(command, args[1:])

        # v2.1+: Subcommand routing (future expansion)
        # Hidden in v2.0 but structure ready
        if command in self.modules:
            if len(args) < 2:
                return self.modules[command].show_help()
            return self.modules[command].handle(args[1], args[2:])

        # Unknown command
        print(f"Error: Unknown command '{command}'")
        return self.show_help()

    def show_help(self) -> int:
        """Show help message."""
        help_text = f"""
AGET v{__version__} - Agent Configuration Tool

Usage: aget <command> [options]

Commands:
  init        Initialize agent configuration
  validate    Validate AGENTS.md syntax
  apply       Apply a pattern to configuration
  rollback    Restore previous configuration
  list        List available patterns
  evolution   Track decisions and discoveries
  extract     Bridge workspace tools to products

Options:
  --version   Show version information
  --help      Show this help message

Examples:
  aget init                    # Create new AGENTS.md
  aget validate                # Check configuration syntax
  aget apply session-management # Add session pattern
  aget rollback                # Restore previous version

For more information: https://github.com/gmelli/aget-cli-agent-template
"""
        print(help_text.strip())
        return 0


def main():
    """Main entry point."""
    cli = AgetCLI()
    return cli.route_command(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())