"""
Config Module - All v2.0 functionality lives here.
In v2.1+ this becomes 'aget config' subcommand.
"""

from typing import List


class ConfigModule:
    """Handles all configuration-related commands."""

    def __init__(self):
        """Initialize config module with command registry."""
        self.commands = {
            'init': self.cmd_init,
            'validate': self.cmd_validate,
            'apply': self.cmd_apply,
            'rollback': self.cmd_rollback,
            'list': self.cmd_list,
            'evolution': self.cmd_evolution,
            'extract': self.cmd_extract,
            'migrate': self.cmd_migrate,
        }

    def handle(self, command: str, args: List[str]) -> int:
        """Handle a config subcommand."""
        if command not in self.commands:
            print(f"Error: Unknown config command '{command}'")
            return self.show_help()

        return self.commands[command](args)

    def show_help(self) -> int:
        """Show config module help."""
        print("""
Config Module Commands:
  init        Initialize agent configuration
  validate    Validate AGENTS.md syntax
  apply       Apply a pattern to configuration
  rollback    Restore previous configuration
  list        List available patterns
  evolution   Track decisions and discoveries
  extract     Bridge workspace tools to products
""")
        return 0

    def cmd_init(self, args: List[str]) -> int:
        """Initialize command - will use InitCommand class."""
        # Placeholder for Step 3
        from aget.config.commands.init import InitCommand
        cmd = InitCommand()
        result = cmd.execute(args=args)
        if result['success']:
            print(f"✅ Configuration initialized ({result['tier_used']} tier)")
            if result['execution_time'] < 2.0:
                print(f"⚡ Completed in {result['execution_time']:.2f}s")
            return 0
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return 1

    def cmd_validate(self, args: List[str]) -> int:
        """Validate command - validate AGET configuration."""
        from aget.config.commands.validate import ValidateCommand
        cmd = ValidateCommand()
        result = cmd.execute(args=args)

        if result['success']:
            print(f"✅ Validation passed ({result['checks_passed']}/{result['checks_total']} checks)")
            if result.get('warnings'):
                print(f"⚠️  {len(result['warnings'])} warnings found")
            if result.get('execution_time', 0) < 2.0:
                print(f"⚡ Completed in {result.get('execution_time', 0):.2f}s")
            return 0
        else:
            errors = result.get('errors', [])
            if errors:
                print(f"❌ Validation failed: {len(errors)} errors")
                for error in errors[:3]:  # Show first 3 errors
                    print(f"   • {error}")
            else:
                # Failed due to warnings in strict mode
                print(f"❌ Validation failed (strict mode): {len(result.get('warnings', []))} warnings")
                for warning in result.get('warnings', [])[:3]:
                    print(f"   • {warning}")
            return 1

    def cmd_apply(self, args: List[str]) -> int:
        """Apply command - apply patterns to configuration."""
        from aget.config.commands.apply import ApplyCommand
        cmd = ApplyCommand()
        result = cmd.execute(args=args)

        if result['success']:
            if 'patterns' in result:
                # Listed patterns successfully
                return 0
            else:
                # Applied pattern successfully
                print(f"✅ Pattern '{result['pattern']}' applied successfully")
                if result.get('execution_time', 0) < 2.0:
                    print(f"⚡ Completed in {result.get('execution_time', 0):.2f}s")
                return 0
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            if 'available' in result:
                print(f"   Available patterns: {', '.join(result['available'])}")
            if 'hint' in result:
                print(f"   {result['hint']}")
            return 1

    def cmd_rollback(self, args: List[str]) -> int:
        """Rollback command - restore previous configuration."""
        from aget.config.commands.rollback import RollbackCommand
        cmd = RollbackCommand()
        result = cmd.execute(args=args)

        if result.get('action') == 'list':
            # List mode
            backups = result.get('backups', [])
            if backups:
                print("Available backups:")
                for backup in backups[:5]:  # Show recent 5
                    print(f"  {backup['id']} - {backup['reason']}")
            else:
                print("No backups available")
            return 0
        elif result['success']:
            print(f"✅ Rollback successful ({result['tier_used']} tier)")
            print(f"   Restored: {result['files_restored']} files")
            if result['execution_time'] < 2.0:
                print(f"⚡ Completed in {result['execution_time']:.2f}s")
            return 0
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return 1

    def cmd_list(self, args: List[str]) -> int:
        """List command - show available patterns."""
        from aget.config.commands.list import ListCommand
        cmd = ListCommand()
        result = cmd.execute(args=args)

        if result['success']:
            if result.get('execution_time', 0) < 2.0:
                print(f"⚡ Completed in {result.get('execution_time', 0):.2f}s")
            return 0
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return 1

    def cmd_evolution(self, args: List[str]) -> int:
        """Evolution command - track decisions and discoveries."""
        from aget.config.commands.evolution import EvolutionCommand
        cmd = EvolutionCommand()
        result = cmd.execute(args=args)

        if result['success']:
            print(result['message'])
            if result.get('execution_time', 0) < 2.0 and 'execution_time' in result:
                print(f"⚡ Completed in {result.get('execution_time', 0):.2f}s")
            return 0
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return 1

    def cmd_extract(self, args: List[str]) -> int:
        """Extract command - bridge workspace tools to products."""
        from aget.config.commands.extract import ExtractCommand
        cmd = ExtractCommand()
        result = cmd.execute(args=args)

        if result['success']:
            if 'message' in result:
                print(result['message'])
            if 'files_created' in result:
                print(f"✅ Created {len(result['files_created'])} files")
                for file in result['files_created']:
                    print(f"   • {file}")
            if 'warnings' in result and result['warnings']:
                print(f"⚠️  {len(result['warnings'])} warnings:")
                for warning in result['warnings']:
                    print(f"   • {warning}")
            if result.get('execution_time', 0) < 2.0 and 'execution_time' in result:
                print(f"⚡ Completed in {result.get('execution_time', 0):.2f}s")
            return 0
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            if 'internal_deps' in result:
                print(f"   Internal dependencies found:")
                for dep in result['internal_deps']:
                    print(f"   • {dep}")
            return 1

    def cmd_migrate(self, args: List[str]) -> int:
        """Migrate command - intelligent migration to AGET v2."""
        from aget.config.commands.migrate import MigrateCommand
        cmd = MigrateCommand()
        result = cmd.execute(args)

        if result['success']:
            print(result['message'])
            if result.get('requires_agent'):
                print("\n⚠️  This migration requires agent intelligence.")
                print("Follow the instructions above to complete migration.")
            return 0
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return 1