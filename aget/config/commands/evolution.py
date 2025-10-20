"""
Evolution Command - Capture decisions, discoveries, and insights
Part of Gate 3 implementation for tracking agent evolution.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from aget.base import BaseCommand


class EvolutionCommand(BaseCommand):
    """Capture and manage evolution entries."""

    def __init__(self):
        """Initialize with evolution types."""
        super().__init__()
        self.evolution_types = {
            'decision': {
                'prefix': 'DEC',
                'description': 'Architectural or design decisions',
                'template': """# Decision: {title}

**Date**: {date}
**Type**: Decision

## Context
{context}

## Decision
{content}

## Rationale
{rationale}

## Consequences
-

## Status
Active
"""
            },
            'discovery': {
                'prefix': 'DISC',
                'description': 'Patterns or insights discovered',
                'template': """# Discovery: {title}

**Date**: {date}
**Type**: Discovery

## What Was Found
{content}

## Context
{context}

## Implications
-

## Next Steps
-
"""
            },
            'extraction': {
                'prefix': 'EXT',
                'description': 'Bridge extraction from workspace to products',
                'template': """# Extraction: {title}

**Date**: {date}
**Type**: Extraction

## Source
`workspace/{source}`

## Target
`products/{target}`

## What Was Extracted
{content}

## Transformations Applied
- Removed private dependencies
- Sanitized API keys
- Generated documentation

## Public URL
{url}
"""
            },
            'learning': {
                'prefix': 'LEARN',
                'description': 'Lessons learned or insights gained',
                'template': """# Learning: {title}

**Date**: {date}
**Type**: Learning

## Insight
{content}

## Context
{context}

## Application
How this can be applied:
-
"""
            }
        }

    def execute(self, args: List[str]) -> Dict[str, Any]:
        """Execute evolution command."""
        if not args or args[0] == '--help':
            return self.show_help()

        if args[0] == '--list':
            return self.list_entries(args[1:])

        if args[0] == '--search':
            return self.search_entries(args[1:])

        if args[0] == '--type' and len(args) >= 3:
            return self.add_entry(args[1], ' '.join(args[2:]))

        return {
            'success': False,
            'error': 'Invalid command. Use --help for usage.'
        }

    def show_help(self) -> Dict[str, Any]:
        """Show help information."""
        help_text = """Evolution Command - Track decisions, discoveries, and insights

Usage:
  aget evolution --type <type> "<message>"  # Add new entry
  aget evolution --list [n]                 # List recent entries (default: 10)
  aget evolution --search <term>            # Search entries
  aget evolution --help                     # Show this help

Types:
"""
        for type_name, type_info in self.evolution_types.items():
            help_text += f"  {type_name:12} - {type_info['description']}\n"

        help_text += """
Examples:
  aget evolution --type decision "Use workspace/ instead of outputs/ for case-sensitivity"
  aget evolution --type discovery "Found pattern: all agents need checkpoints"
  aget evolution --type extraction "Extracted cost-analyzer tool to products/"
  aget evolution --list 5
  aget evolution --search "workspace"
"""

        return {
            'success': True,
            'message': help_text
        }

    def add_entry(self, entry_type: str, content: str) -> Dict[str, Any]:
        """Add a new evolution entry."""
        # Validate type
        if entry_type not in self.evolution_types:
            return {
                'success': False,
                'error': f'Invalid type: {entry_type}. Valid types: {", ".join(self.evolution_types.keys())}'
            }

        # Get or create evolution directory
        evolution_dir = Path.cwd() / ".aget" / "evolution"
        if not evolution_dir.exists():
            evolution_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp (include microseconds for uniqueness)
        now = datetime.now()
        type_info = self.evolution_types[entry_type]
        filename = f"{now.strftime('%Y-%m-%d-%H%M%S')}-{now.microsecond:06d}-{type_info['prefix']}.md"
        filepath = evolution_dir / filename

        # Extract title (first 50 chars or until punctuation)
        title = content[:50].split('.')[0].split('!')[0].split('?')[0]
        if len(title) < len(content):
            title += '...'

        # Prepare template variables
        template_vars = {
            'title': title,
            'date': now.strftime('%Y-%m-%d %H:%M:%S'),
            'content': content,
            'context': 'Added via `aget evolution` command',
            'rationale': '',
            'source': '',
            'target': '',
            'url': ''
        }

        # Generate content from template
        entry_content = type_info['template'].format(**template_vars)

        # Write file
        filepath.write_text(entry_content)

        # Update index
        self._update_index(evolution_dir, filename, entry_type, title)

        return {
            'success': True,
            'message': f'Created {entry_type} entry: {filename}',
            'file': str(filepath)
        }

    def list_entries(self, args: List[str]) -> Dict[str, Any]:
        """List recent evolution entries."""
        # Parse count argument
        count = 10
        if args and args[0].isdigit():
            count = int(args[0])

        # Find evolution directory
        evolution_dir = Path.cwd() / ".aget" / "evolution"
        if not evolution_dir.exists():
            return {
                'success': True,
                'message': 'No evolution entries found. Use `aget evolution --type <type> "<message>"` to add entries.'
            }

        # Get all markdown files
        entries = sorted(evolution_dir.glob("*.md"), reverse=True)[:count]

        if not entries:
            return {
                'success': True,
                'message': 'No evolution entries found.'
            }

        # Format output
        output = f"Recent Evolution Entries (showing {len(entries)} of {len(list(evolution_dir.glob('*.md')))})\n"
        output += "=" * 60 + "\n\n"

        for entry_path in entries:
            # Parse filename for metadata
            filename = entry_path.name
            parts = filename.replace('.md', '').split('-')

            if len(parts) >= 5:
                date = f"{parts[0]}-{parts[1]}-{parts[2]}"
                time = parts[3][:2] + ':' + parts[3][2:4] if len(parts[3]) >= 4 else parts[3]
                # Skip microseconds part (parts[4]) and get type prefix
                type_prefix = parts[5] if len(parts) > 5 else 'UNK'

                # Get type from prefix
                entry_type = 'unknown'
                for type_name, type_info in self.evolution_types.items():
                    if type_info['prefix'] == type_prefix:
                        entry_type = type_name
                        break

                # Read first line for title
                first_line = entry_path.read_text().split('\n')[0]
                title = first_line.replace('# ', '').replace('Decision: ', '').replace('Discovery: ', '')
                title = title.replace('Extraction: ', '').replace('Learning: ', '')

                output += f"📝 {date} {time} [{entry_type:10}] {title[:60]}\n"
                output += f"   File: {filename}\n\n"

        return {
            'success': True,
            'message': output
        }

    def search_entries(self, args: List[str]) -> Dict[str, Any]:
        """Search evolution entries for a term."""
        if not args:
            return {
                'success': False,
                'error': 'Search term required. Usage: aget evolution --search <term>'
            }

        search_term = ' '.join(args).lower()

        # Find evolution directory
        evolution_dir = Path.cwd() / ".aget" / "evolution"
        if not evolution_dir.exists():
            return {
                'success': True,
                'message': 'No evolution entries to search.'
            }

        # Search all markdown files
        matches = []
        for entry_path in evolution_dir.glob("*.md"):
            content = entry_path.read_text()
            if search_term in content.lower():
                # Count occurrences
                occurrences = content.lower().count(search_term)

                # Get title
                first_line = content.split('\n')[0]
                title = first_line.replace('# ', '').strip()

                matches.append({
                    'file': entry_path.name,
                    'title': title,
                    'occurrences': occurrences
                })

        if not matches:
            return {
                'success': True,
                'message': f'No entries found containing "{search_term}"'
            }

        # Sort by occurrences
        matches.sort(key=lambda x: x['occurrences'], reverse=True)

        # Format output
        output = f"Found '{search_term}' in {len(matches)} entries:\n"
        output += "=" * 60 + "\n\n"

        for match in matches:
            output += f"📝 {match['file']}\n"
            output += f"   {match['title'][:60]}\n"
            output += f"   ({match['occurrences']} occurrence{'s' if match['occurrences'] > 1 else ''})\n\n"

        return {
            'success': True,
            'message': output,
            'matches': len(matches)
        }

    def _update_index(self, evolution_dir: Path, filename: str, entry_type: str, title: str):
        """Update the evolution index file."""
        index_file = evolution_dir / "index.json"

        # Load existing index or create new
        if index_file.exists():
            index = json.loads(index_file.read_text())
        else:
            index = {
                'entries': [],
                'stats': {
                    'total': 0,
                    'by_type': {}
                }
            }

        # Add new entry
        index['entries'].insert(0, {
            'filename': filename,
            'type': entry_type,
            'title': title,
            'created': datetime.now().isoformat()
        })

        # Update stats
        index['stats']['total'] += 1
        if entry_type not in index['stats']['by_type']:
            index['stats']['by_type'][entry_type] = 0
        index['stats']['by_type'][entry_type] += 1

        # Keep only last 100 entries in index
        index['entries'] = index['entries'][:100]

        # Save index
        index_file.write_text(json.dumps(index, indent=2))

    def tier_basic(self, **kwargs) -> Dict[str, Any]:
        """Basic tier implementation."""
        args = kwargs.get('args', [])
        return self.execute(args)

    def tier_git(self, **kwargs) -> Dict[str, Any]:
        """Git tier - same as basic for evolution."""
        return self.tier_basic(**kwargs)

    def tier_gh(self, **kwargs) -> Dict[str, Any]:
        """GitHub tier - same as basic for evolution."""
        return self.tier_basic(**kwargs)