"""
AGET Pattern Library
Provides reusable patterns for agent configuration.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import importlib.util


class PatternRegistry:
    """Registry of available patterns."""

    def __init__(self):
        """Initialize pattern registry."""
        self.patterns_dir = Path(__file__).parent.parent.parent / "patterns"
        self._registry = None

    def scan_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Scan patterns directory and build registry.

        Returns:
            Dictionary of pattern categories and their patterns
        """
        registry = {}

        if not self.patterns_dir.exists():
            return registry

        # Scan each category directory
        for category_dir in self.patterns_dir.iterdir():
            if not category_dir.is_dir():
                continue

            if category_dir.name.startswith('.'):
                continue

            category = category_dir.name
            registry[category] = {
                'path': str(category_dir),
                'patterns': []
            }

            # Find Python files in category
            for pattern_file in category_dir.glob("*.py"):
                if pattern_file.name.startswith('_'):
                    continue

                pattern_name = pattern_file.stem
                pattern_info = self._get_pattern_info(pattern_file)

                registry[category]['patterns'].append({
                    'name': pattern_name,
                    'file': str(pattern_file),
                    'description': pattern_info.get('description', ''),
                    'requires': pattern_info.get('requires', [])
                })

            # Check for README
            readme = category_dir / "README.md"
            if readme.exists():
                registry[category]['readme'] = str(readme)

        self._registry = registry
        return registry

    def _get_pattern_info(self, pattern_file: Path) -> Dict[str, Any]:
        """
        Extract pattern metadata from file.

        Looks for docstring and pattern metadata.
        """
        info = {}

        try:
            # Read file to extract docstring
            content = pattern_file.read_text()
            lines = content.split('\n')

            # Find module docstring
            in_docstring = False
            docstring_lines = []

            for line in lines:
                if line.strip().startswith('"""'):
                    if not in_docstring:
                        in_docstring = True
                        # Check if it's a single-line docstring
                        if line.strip().endswith('"""') and len(line.strip()) > 6:
                            info['description'] = line.strip()[3:-3].strip()
                            break
                    else:
                        # End of multi-line docstring
                        break
                elif in_docstring:
                    docstring_lines.append(line)

            if docstring_lines:
                # Use first non-empty line as description
                for line in docstring_lines:
                    if line.strip():
                        info['description'] = line.strip()
                        break

        except Exception:
            pass

        return info

    def list_patterns(self) -> List[str]:
        """
        List all available patterns.

        Returns:
            List of pattern identifiers (category/name)
        """
        if not self._registry:
            self.scan_patterns()

        patterns = []
        for category, data in self._registry.items():
            for pattern in data['patterns']:
                patterns.append(f"{category}/{pattern['name']}")

        return sorted(patterns)

    def get_pattern(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Get pattern information by identifier.

        Args:
            identifier: Pattern identifier (e.g., "session/wake")

        Returns:
            Pattern information or None if not found
        """
        if not self._registry:
            self.scan_patterns()

        parts = identifier.split('/')
        if len(parts) != 2:
            return None

        category, name = parts

        if category not in self._registry:
            return None

        for pattern in self._registry[category]['patterns']:
            if pattern['name'] == name:
                return {
                    'category': category,
                    'name': name,
                    'file': pattern['file'],
                    'description': pattern.get('description', ''),
                    'requires': pattern.get('requires', [])
                }

        return None

    def load_pattern(self, identifier: str):
        """
        Load and return pattern module.

        Args:
            identifier: Pattern identifier

        Returns:
            Pattern module or None
        """
        pattern_info = self.get_pattern(identifier)
        if not pattern_info:
            return None

        # Dynamic import of pattern module
        spec = importlib.util.spec_from_file_location(
            f"pattern_{pattern_info['name']}",
            pattern_info['file']
        )

        if not spec or not spec.loader:
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module


# Global registry instance
registry = PatternRegistry()