"""
Extract Command - Bridge workspace tools to public products
Part of Gate 3 implementation for workspace→products promotion.
"""

import ast
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from aget.base import BaseCommand


class ExtractCommand(BaseCommand):
    """Extract and promote workspace tools to public products."""

    def __init__(self):
        """Initialize with extraction rules."""
        super().__init__()

        # Patterns to remove during sanitization
        self.sensitive_patterns = [
            (r'api[_\s]?key\s*=\s*["\'][^"\']*["\']', 'api_key = "REDACTED"'),
            (r'token\s*=\s*["\'][^"\']*["\']', 'token = "REDACTED"'),
            (r'password\s*=\s*["\'][^"\']*["\']', 'password = "REDACTED"'),
            (r'secret\s*=\s*["\'][^"\']*["\']', 'secret = "REDACTED"'),
        ]

        # Common internal imports to clean
        self.internal_imports = [
            'from workspace import',
            'from outputs import',  # Legacy
            'import workspace.',
            'import outputs.',
        ]

    def execute(self, args: List[str]) -> Dict[str, Any]:
        """Execute extract command."""
        if not args or args[0] == '--help':
            return self.show_help()

        if args[0] == '--auto':
            return self.auto_discover(args[1:])

        if '--from' in args and '--to' in args:
            return self.extract_file(args)

        return {
            'success': False,
            'error': 'Invalid command. Use --help for usage.'
        }

    def show_help(self) -> Dict[str, Any]:
        """Show help information."""
        help_text = """Extract Command - Bridge workspace tools to public products

Usage:
  aget extract --from <file> --to <dir>    # Extract specific file
  aget extract --auto                      # Auto-discover extractable tools
  aget extract --help                      # Show this help

Options:
  --from <file>    Source file in workspace/
  --to <dir>       Target directory (usually products/)
  --name <name>    Package name (auto-detected if not specified)
  --force          Force extraction even with warnings
  --dry-run        Preview changes without extracting

Examples:
  aget extract --from workspace/analyzer.py --to products/
  aget extract --from workspace/tool.py --to products/ --name my-tool
  aget extract --auto --dry-run
  aget extract --from workspace/script.py --to products/ --force

Notes:
  - Sanitizes sensitive data (API keys, tokens)
  - Removes internal dependencies
  - Generates setup.py for pip installation
  - Creates README.md with usage instructions
  - Tracks extraction in evolution
"""
        return {
            'success': True,
            'message': help_text
        }

    def extract_file(self, args: List[str]) -> Dict[str, Any]:
        """Extract a file or directory from workspace to products."""
        # Parse arguments
        from_idx = args.index('--from')
        to_idx = args.index('--to')

        source_path = Path(args[from_idx + 1])
        target_dir = Path(args[to_idx + 1])

        # Check for optional arguments
        force = '--force' in args
        dry_run = '--dry-run' in args

        package_name = None
        if '--name' in args:
            name_idx = args.index('--name')
            package_name = args[name_idx + 1]
        else:
            # Auto-detect package name from filename or directory
            if source_path.is_dir():
                package_name = source_path.name.replace('_', '-')
            else:
                package_name = source_path.stem.replace('_', '-')

        # Validate source
        if not source_path.exists():
            return {
                'success': False,
                'error': f'Source not found: {source_path}'
            }

        # Handle directory extraction
        if source_path.is_dir():
            return self.extract_directory(source_path, target_dir, package_name, force, dry_run)

        # Handle file extraction (existing logic)
        if not source_path.suffix == '.py':
            return {
                'success': False,
                'error': 'Only Python files or directories can be extracted'
            }

        # Analyze the file
        analysis = self.analyze_file(source_path)

        # Check for issues
        if analysis['has_internal_deps'] and not force:
            return {
                'success': False,
                'error': 'File has internal dependencies. Use --force to extract anyway.',
                'internal_deps': analysis['internal_deps']
            }

        if dry_run:
            return {
                'success': True,
                'message': f'[DRY RUN] Would extract {source_path} to {target_dir}/{package_name}/',
                'analysis': analysis
            }

        # Create target package directory
        package_dir = target_dir / package_name
        package_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize and copy the file
        target_file = package_dir / f"{package_name.replace('-', '_')}.py"
        sanitized_content = self.sanitize_content(source_path.read_text())
        target_file.write_text(sanitized_content)

        # Generate setup.py
        setup_content = self.generate_setup_py(
            package_name=package_name,
            description=analysis.get('description', f'Extracted from {source_path.name}'),
            dependencies=analysis.get('external_deps', [])
        )
        (package_dir / 'setup.py').write_text(setup_content)

        # Generate README.md
        readme_content = self.generate_readme(
            package_name=package_name,
            source_file=source_path.name,
            description=analysis.get('description', ''),
            has_cli=analysis.get('has_main', False)
        )
        (package_dir / 'README.md').write_text(readme_content)

        # Create __init__.py
        init_content = f'"""Package extracted from {source_path}"""\n\n'
        init_content += f"from .{package_name.replace('-', '_')} import *\n"
        (package_dir / '__init__.py').write_text(init_content)

        # Track in evolution
        self.track_extraction(source_path, package_dir)

        return {
            'success': True,
            'message': f'Extracted {source_path} to {package_dir}',
            'files_created': [
                f'{package_name}/__init__.py',
                f'{package_name}/{package_name.replace("-", "_")}.py',
                f'{package_name}/setup.py',
                f'{package_name}/README.md'
            ],
            'warnings': analysis.get('warnings', [])
        }

    def extract_directory(self, source_dir: Path, target_dir: Path,
                          package_name: str, force: bool, dry_run: bool) -> Dict[str, Any]:
        """Extract a directory structure to products."""
        # Find all Python files in directory
        py_files = list(source_dir.glob('**/*.py'))

        if not py_files:
            return {
                'success': False,
                'error': f'No Python files found in {source_dir}'
            }

        # Analyze all files
        all_internal_deps = set()
        all_external_deps = set()
        has_issues = False

        for py_file in py_files:
            if '__pycache__' in str(py_file):
                continue
            analysis = self.analyze_file(py_file)
            all_internal_deps.update(analysis['internal_deps'])
            all_external_deps.update(analysis['external_deps'])
            if analysis['has_internal_deps'] and not force:
                has_issues = True

        if has_issues and not force:
            return {
                'success': False,
                'error': 'Directory has files with internal dependencies. Use --force to extract anyway.',
                'internal_deps': list(all_internal_deps)
            }

        if dry_run:
            return {
                'success': True,
                'message': f'[DRY RUN] Would extract {source_dir} to {target_dir}/{package_name}/',
                'files': len(py_files),
                'structure': f'{len(set(f.parent for f in py_files))} directories'
            }

        # Create target package directory
        package_dir = target_dir / package_name
        package_dir.mkdir(parents=True, exist_ok=True)

        # Create package subdirectory (Python convention)
        package_subdir = package_dir / package_name.replace('-', '_')
        package_subdir.mkdir(exist_ok=True)

        # Copy and sanitize all Python files maintaining structure
        files_created = []
        for py_file in py_files:
            if '__pycache__' in str(py_file):
                continue

            # Maintain relative structure
            relative_path = py_file.relative_to(source_dir)
            target_file = package_subdir / relative_path
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # Sanitize and write
            sanitized_content = self.sanitize_content(py_file.read_text())
            target_file.write_text(sanitized_content)
            files_created.append(str(relative_path))

            # Create __init__.py files for all directories
            for parent in relative_path.parents:
                if parent != Path('.'):
                    init_file = package_subdir / parent / '__init__.py'
                    if not init_file.exists():
                        init_file.write_text('"""Package module."""\n')

        # Create root __init__.py
        (package_subdir / '__init__.py').write_text(
            f'"""Package extracted from {source_dir.name}/"""\n'
        )

        # Generate setup.py
        setup_content = self.generate_setup_py(
            package_name=package_name,
            description=f'Library extracted from {source_dir.name}',
            dependencies=list(all_external_deps)
        )
        (package_dir / 'setup.py').write_text(setup_content)

        # Generate comprehensive README
        readme_content = self.generate_directory_readme(
            package_name=package_name,
            source_dir=source_dir.name,
            file_count=len(py_files),
            modules=[f.stem for f in py_files if f.parent == source_dir]
        )
        (package_dir / 'README.md').write_text(readme_content)

        # Track in evolution
        self.track_extraction(source_dir, package_dir)

        return {
            'success': True,
            'message': f'Extracted directory {source_dir} to {package_dir}',
            'files_extracted': len(files_created),
            'package_structure': f'{package_name}/\n├── setup.py\n├── README.md\n└── {package_name.replace("-", "_")}/\n    └── {len(files_created)} Python files',
            'warnings': ['Internal dependencies commented out'] if all_internal_deps else []
        }

    def generate_directory_readme(self, package_name: str, source_dir: str,
                                 file_count: int, modules: List[str]) -> str:
        """Generate README for directory extraction."""
        readme = f"""# {package_name}

Library extracted from `{source_dir}/` directory.

## Overview

This package contains {file_count} Python modules originally developed in the workspace.
It has been sanitized and prepared for public use.

## Installation

```bash
pip install -e .
```

## Modules

"""
        for module in modules[:10]:  # List first 10 modules
            readme += f"- `{module}` - Extracted module\n"

        if len(modules) > 10:
            readme += f"- ... and {len(modules) - 10} more\n"

        readme += f"""

## Usage

```python
from {package_name.replace('-', '_')} import *

# Import specific modules
from {package_name.replace('-', '_')}.module_name import ClassName
```

## Development

This package was automatically extracted using AGET's enhanced bridge mechanism.
Original internal dependencies have been removed or refactored.

## License

See the main project license.

---

*Extracted on {datetime.now().strftime('%Y-%m-%d')} using AGET extract*
"""
        return readme

    def auto_discover(self, args: List[str]) -> Dict[str, Any]:
        """Auto-discover extractable tools in workspace."""
        dry_run = '--dry-run' in args

        # Find workspace directory
        workspace_dir = Path.cwd() / 'workspace'
        if not workspace_dir.exists():
            return {
                'success': False,
                'error': 'No workspace/ directory found. Run from project root.'
            }

        # Scan Python files
        py_files = list(workspace_dir.glob('**/*.py'))
        if not py_files:
            return {
                'success': True,
                'message': 'No Python files found in workspace/'
            }

        # Analyze each file
        candidates = []
        for py_file in py_files:
            # Skip __pycache__ and test files
            if '__pycache__' in str(py_file) or 'test_' in py_file.name:
                continue

            analysis = self.analyze_file(py_file)

            # Score extractability
            score = 0
            if not analysis['has_internal_deps']:
                score += 3
            if analysis['has_main']:
                score += 2
            if analysis['description']:
                score += 1
            if len(analysis['external_deps']) < 5:
                score += 1

            if score >= 3:  # Threshold for recommendation
                candidates.append({
                    'file': str(py_file.relative_to(Path.cwd())),
                    'score': score,
                    'has_main': analysis['has_main'],
                    'internal_deps': len(analysis['internal_deps']),
                    'external_deps': len(analysis['external_deps'])
                })

        if not candidates:
            return {
                'success': True,
                'message': 'No extractable candidates found. Files may have internal dependencies.'
            }

        # Sort by score
        candidates.sort(key=lambda x: x['score'], reverse=True)

        # Format output
        output = f"Found {len(candidates)} extractable candidates:\n"
        output += "=" * 60 + "\n\n"

        for candidate in candidates[:10]:  # Show top 10
            output += f"📦 {candidate['file']}\n"
            output += f"   Score: {'⭐' * candidate['score']}\n"
            if candidate['has_main']:
                output += "   ✓ Has CLI interface\n"
            output += f"   Dependencies: {candidate['external_deps']} external"
            if candidate['internal_deps'] > 0:
                output += f", {candidate['internal_deps']} internal (needs cleanup)"
            output += "\n\n"

        if not dry_run:
            output += "To extract a file, run:\n"
            output += f"  aget extract --from {candidates[0]['file']} --to products/\n"

        return {
            'success': True,
            'message': output,
            'candidates': len(candidates)
        }

    def analyze_file(self, filepath: Path) -> Dict[str, Any]:
        """Analyze a Python file for extraction readiness."""
        content = filepath.read_text()

        result = {
            'description': '',
            'has_main': False,
            'has_internal_deps': False,
            'internal_deps': [],
            'external_deps': [],
            'warnings': []
        }

        try:
            tree = ast.parse(content)

            # Get module docstring
            for node in ast.walk(tree):
                if isinstance(node, ast.Module) and ast.get_docstring(node):
                    result['description'] = ast.get_docstring(node).split('\n')[0]
                    break

            # Check for main function
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == 'main':
                    result['has_main'] = True
                if isinstance(node, ast.If):
                    # Check for if __name__ == "__main__"
                    if (hasattr(node.test, 'left') and
                        hasattr(node.test.left, 'id') and
                        node.test.left.id == '__name__'):
                        result['has_main'] = True

            # Analyze imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name
                        if self._is_internal_import(module):
                            result['has_internal_deps'] = True
                            result['internal_deps'].append(module)
                        else:
                            result['external_deps'].append(module)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        if self._is_internal_import(node.module):
                            result['has_internal_deps'] = True
                            result['internal_deps'].append(node.module)
                        else:
                            result['external_deps'].append(node.module)

            # Remove duplicates
            result['internal_deps'] = list(set(result['internal_deps']))
            result['external_deps'] = list(set(result['external_deps']))

            # Check for sensitive data
            for pattern, _ in self.sensitive_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    result['warnings'].append('Contains sensitive data that will be redacted')
                    break

        except SyntaxError as e:
            result['warnings'].append(f'Syntax error in file: {e}')

        return result

    def _is_internal_import(self, module: str) -> bool:
        """Check if an import is internal to the workspace."""
        internal_prefixes = ['workspace', 'outputs', 'src.workspace', 'src.outputs']
        return any(module.startswith(prefix) for prefix in internal_prefixes)

    def sanitize_content(self, content: str) -> str:
        """Sanitize content by removing sensitive data."""
        sanitized = content

        # Apply sensitive pattern replacements
        for pattern, replacement in self.sensitive_patterns:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        # Remove internal imports (comment them out with warning)
        for internal_import in self.internal_imports:
            if internal_import in sanitized:
                sanitized = sanitized.replace(
                    internal_import,
                    f'# EXTRACTED: Removed internal import - {internal_import}'
                )

        # Add extraction header
        header = f"""# This file was extracted from workspace/ on {datetime.now().strftime('%Y-%m-%d')}
# Original internal dependencies have been removed or commented out
# Generated by AGET extract command

"""
        sanitized = header + sanitized

        return sanitized

    def generate_setup_py(self, package_name: str, description: str,
                         dependencies: List[str]) -> str:
        """Generate a setup.py file for the extracted package."""
        # Filter out standard library modules
        stdlib_modules = {
            'os', 'sys', 'json', 'time', 'datetime', 'pathlib',
            're', 'ast', 'collections', 'itertools', 'functools'
        }
        external_deps = [dep for dep in dependencies
                        if dep.split('.')[0] not in stdlib_modules]

        setup_content = f'''"""Setup configuration for {package_name}"""

from setuptools import setup, find_packages

setup(
    name="{package_name}",
    version="0.1.0",
    description="{description}",
    author="Extracted by AGET",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
'''

        for dep in external_deps[:5]:  # Limit to top 5 deps
            setup_content += f'        # "{dep}",\n'

        setup_content += '''    ],
    entry_points={
        'console_scripts': [
            # Add CLI entry point if applicable
            # '{package_name}={package_name}:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
'''.replace('{package_name}', package_name)

        return setup_content

    def generate_readme(self, package_name: str, source_file: str,
                        description: str, has_cli: bool) -> str:
        """Generate a README.md file for the extracted package."""
        readme = f"""# {package_name}

{description or 'Tool extracted from workspace'}

## Origin

This package was extracted from `{source_file}` in the workspace directory.
It has been sanitized and prepared for public use.

## Installation

```bash
pip install .
```

## Usage
"""

        if has_cli:
            readme += f"""
### Command Line

```bash
python -m {package_name}
```
"""

        readme += f"""
### Python API

```python
import {package_name.replace('-', '_')}

# Your code here
```

## Development

This package was automatically extracted using AGET's bridge mechanism.
Original internal dependencies have been removed or refactored.

## License

See the main project license.

---

*Extracted on {datetime.now().strftime('%Y-%m-%d')} using AGET extract*
"""

        return readme

    def track_extraction(self, source_path: Path, target_dir: Path):
        """Track the extraction in evolution."""
        # Import evolution command for tracking
        from aget.config.commands.evolution import EvolutionCommand

        evolution_cmd = EvolutionCommand()

        message = f"Extracted {source_path.name} from workspace/ to {target_dir.name}/"
        evolution_cmd.execute(['--type', 'extraction', message])

    def tier_basic(self, **kwargs) -> Dict[str, Any]:
        """Basic tier implementation."""
        args = kwargs.get('args', [])
        return self.execute(args)

    def tier_git(self, **kwargs) -> Dict[str, Any]:
        """Git tier - same as basic for extract."""
        return self.tier_basic(**kwargs)

    def tier_gh(self, **kwargs) -> Dict[str, Any]:
        """GitHub tier - same as basic for extract."""
        return self.tier_basic(**kwargs)