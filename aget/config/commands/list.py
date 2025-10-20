"""
List Command - Show available patterns
"""

from pathlib import Path
from typing import Any, Dict, List

from aget.base import BaseCommand
from aget.patterns import registry


class ListCommand(BaseCommand):
    """List available patterns."""

    def __init__(self):
        """Initialize list command."""
        super().__init__()

    def tier_basic(self, **kwargs) -> Dict[str, Any]:
        """
        Basic tier - List patterns from patterns directory.
        """
        args = kwargs.get('args', [])

        # Scan for patterns
        patterns = registry.scan_patterns()

        # Display patterns
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
        installed_patterns = self._get_installed_patterns()

        for category, info in patterns.items():
            print(f"\n{category.upper()}:")
            for pattern in info['patterns']:
                full_id = f"{category}/{pattern['name']}"
                pattern_list.append(full_id)

                # Check if installed
                status = " ✓" if full_id in installed_patterns else ""
                print(f"  {full_id}{status}")

                if pattern.get('description'):
                    print(f"    {pattern['description']}")

        print("\n" + "=" * 40)
        print(f"Total: {len(pattern_list)} patterns available")
        if installed_patterns:
            print(f"Installed: {len(installed_patterns)} patterns")
        print("\nUsage: aget apply <pattern_id>")
        print("Example: aget apply session/wake")

        return {
            'success': True,
            'patterns': pattern_list,
            'installed': installed_patterns
        }

    def tier_git(self, **kwargs) -> Dict[str, Any]:
        """Git tier - same as basic."""
        return self.tier_basic(**kwargs)

    def tier_gh(self, **kwargs) -> Dict[str, Any]:
        """GitHub CLI tier - could fetch remote patterns in future."""
        return self.tier_basic(**kwargs)

    def _get_installed_patterns(self) -> List[str]:
        """
        Get list of installed patterns.

        Reads from .aget/state.json if available.
        """
        state_file = Path.cwd() / ".aget" / "state.json"
        if not state_file.exists():
            return []

        try:
            import json
            state = json.loads(state_file.read_text())
            return state.get('installed_patterns', [])
        except:
            return []