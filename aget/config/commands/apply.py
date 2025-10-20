"""
Apply Command - Apply patterns to agent configuration
"""

import sys
from pathlib import Path
from typing import Any, Dict

from aget.base import BaseCommand
from aget.patterns import registry


class ApplyCommand(BaseCommand):
    """Apply patterns to agent configuration."""

    def __init__(self):
        """Initialize apply command."""
        super().__init__()

    def tier_basic(self, **kwargs) -> Dict[str, Any]:
        """
        Basic tier - Apply pattern to project.
        """
        args = kwargs.get('args', [])

        if not args:
            return self._list_patterns()

        pattern_id = args[0]
        project_path = Path.cwd()

        # Check if AGENTS.md exists
        if not (project_path / "AGENTS.md").exists():
            return {
                'success': False,
                'error': 'No AGENTS.md found. Run `aget init` first.'
            }

        # Load pattern
        pattern_info = registry.get_pattern(pattern_id)
        if not pattern_info:
            available = registry.list_patterns()
            return {
                'success': False,
                'error': f'Pattern "{pattern_id}" not found.',
                'available': available[:5],  # Show first 5
                'hint': 'Use `aget apply` to list all patterns.'
            }

        # Load and execute pattern
        try:
            module = registry.load_pattern(pattern_id)
            if not module:
                return {
                    'success': False,
                    'error': f'Could not load pattern "{pattern_id}"'
                }

            # Check for apply_pattern function
            if not hasattr(module, 'apply_pattern'):
                return {
                    'success': False,
                    'error': f'Pattern "{pattern_id}" does not have apply_pattern function'
                }

            # Execute pattern
            print(f"🔧 Applying pattern: {pattern_id}")
            if pattern_info.get('description'):
                print(f"   {pattern_info['description']}")
            print("-" * 40)

            result = module.apply_pattern(project_path)

            return {
                'success': True,
                'pattern': pattern_id,
                'result': result
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Pattern execution failed: {str(e)}'
            }

    def tier_git(self, **kwargs) -> Dict[str, Any]:
        """Git tier - same as basic for patterns."""
        return self.tier_basic(**kwargs)

    def tier_gh(self, **kwargs) -> Dict[str, Any]:
        """GitHub CLI tier - same as basic for patterns."""
        return self.tier_basic(**kwargs)

    def _list_patterns(self) -> Dict[str, Any]:
        """List all available patterns."""
        patterns = registry.scan_patterns()

        print("📦 Available Patterns")
        print("=" * 40)

        if not patterns:
            print("No patterns found.")
            print("\nPatterns should be in the patterns/ directory.")
            return {
                'success': True,
                'patterns': []
            }

        pattern_list = []
        for category, info in patterns.items():
            print(f"\n{category.upper()}:")
            for pattern in info['patterns']:
                full_id = f"{category}/{pattern['name']}"
                pattern_list.append(full_id)

                print(f"  {full_id}")
                if pattern.get('description'):
                    print(f"    {pattern['description']}")

        print("\n" + "=" * 40)
        print(f"Total: {len(pattern_list)} patterns available")
        print("\nUsage: aget apply <pattern_id>")
        print("Example: aget apply session/wake")

        return {
            'success': True,
            'patterns': pattern_list
        }