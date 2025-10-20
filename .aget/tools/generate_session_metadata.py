#!/usr/bin/env python3
"""
Session Metadata Generator - v2.3 Gate A3

Automatically extract session metadata from git history and session content.
Addresses 60% session gap by automating metadata collection.
"""

import argparse
import re
import subprocess
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class SessionMetadataGenerator:
    """Generate session metadata from git history and session content."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.session_file = None
        self.metadata = {}

    def _run_git_command(self, *args) -> str:
        """Run git command and return output."""
        try:
            result = subprocess.run(
                ['git'] + list(args),
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""

    def extract_from_git(self) -> Dict:
        """Extract metadata from git history."""
        metadata = {}

        # Get today's commits
        today = datetime.now().strftime("%Y-%m-%d")
        git_log = self._run_git_command(
            'log',
            '--since', today,
            '--format=%h|||%s',
            '--no-merges'
        )

        if git_log:
            commits = []
            for line in git_log.split('\n'):
                if '|||' in line:
                    hash_part, message = line.split('|||', 1)
                    commits.append({
                        'hash': hash_part.strip(),
                        'message': message.strip()
                    })
            metadata['commits'] = commits

        # Get files changed today
        files_changed = self._run_git_command(
            'diff',
            '--name-only',
            f'HEAD@{{{today}}}'
        )
        if files_changed:
            metadata['files_changed'] = len(files_changed.split('\n'))

        return metadata

    def extract_from_content(self, content: str) -> Dict:
        """Extract metadata from session content."""
        metadata = {}

        # Extract learning IDs (L[0-9]+)
        learning_pattern = r'(L\d+):\s*(.+)'
        learnings = []
        for match in re.finditer(learning_pattern, content, re.MULTILINE):
            learnings.append({
                'id': match.group(1),
                'description': match.group(2).strip()
            })
        if learnings:
            metadata['learnings'] = learnings

        # Extract issue references (#[0-9]+)
        issue_pattern = r'#(\d+)'
        issue_numbers = set(re.findall(issue_pattern, content))
        if issue_numbers:
            metadata['issues_filed'] = [
                {'number': int(num), 'title': f'Issue #{num}'}
                for num in sorted(issue_numbers, key=int)
            ]

        # Extract pain points
        pain_pattern = r'(?:pain point|difficulty|problem|issue):\s*(.+)'
        pain_points = []
        for match in re.finditer(pain_pattern, content, re.IGNORECASE):
            pain_points.append(match.group(1).strip())
        if pain_points:
            metadata['pain_points'] = pain_points

        # Extract next steps
        next_pattern = r'(?:next step|todo|follow-up):\s*(.+)'
        next_steps = []
        for match in re.finditer(next_pattern, content, re.IGNORECASE):
            next_steps.append(match.group(1).strip())
        if next_steps:
            metadata['next_steps'] = next_steps

        return metadata

    def generate_metadata(
        self,
        objectives: List[str],
        outcomes: List[str],
        duration_minutes: Optional[int] = None,
        session_content: Optional[str] = None
    ) -> Dict:
        """Generate complete session metadata."""
        metadata = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'duration_minutes': duration_minutes or 60,
            'objectives': objectives,
            'outcomes': outcomes
        }

        # Extract from git
        git_metadata = self.extract_from_git()
        metadata.update(git_metadata)

        # Extract from content if provided
        if session_content:
            content_metadata = self.extract_from_content(session_content)
            metadata.update(content_metadata)

        return metadata

    def format_frontmatter(self, metadata: Dict) -> str:
        """Format metadata as YAML frontmatter."""
        return "---\n" + yaml.dump(metadata, sort_keys=False, default_flow_style=False) + "---\n"

    def add_to_session_file(
        self,
        session_file: Path,
        metadata: Dict,
        prepend: bool = True
    ):
        """Add metadata to existing session file."""
        if not session_file.exists():
            print(f"ERROR: Session file not found: {session_file}")
            sys.exit(1)

        # Read existing content
        content = session_file.read_text()

        # Check if already has frontmatter
        if content.startswith('---\n'):
            print("⚠️  Session already has frontmatter, skipping")
            return

        # Generate frontmatter
        frontmatter = self.format_frontmatter(metadata)

        # Prepend to file
        if prepend:
            new_content = frontmatter + "\n" + content
        else:
            new_content = content + "\n" + frontmatter

        session_file.write_text(new_content)
        print(f"✅ Added metadata to {session_file.name}")


def main():
    """Run session metadata generator."""
    parser = argparse.ArgumentParser(
        description="Generate session metadata from git history and content"
    )
    parser.add_argument(
        '--session-file',
        type=Path,
        help='Session markdown file to add metadata to'
    )
    parser.add_argument(
        '--objectives',
        nargs='+',
        required=True,
        help='Session objectives (space-separated)'
    )
    parser.add_argument(
        '--outcomes',
        nargs='+',
        required=True,
        help='Session outcomes (space-separated)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        help='Session duration in minutes'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print metadata without modifying file'
    )

    args = parser.parse_args()

    generator = SessionMetadataGenerator()

    # Read session content if file provided
    session_content = None
    if args.session_file and args.session_file.exists():
        session_content = args.session_file.read_text()

    # Generate metadata
    metadata = generator.generate_metadata(
        objectives=args.objectives,
        outcomes=args.outcomes,
        duration_minutes=args.duration,
        session_content=session_content
    )

    # Print metadata
    print("Generated Session Metadata:")
    print("=" * 70)
    print(generator.format_frontmatter(metadata))
    print("=" * 70)

    # Add to file if not dry run
    if args.session_file and not args.dry_run:
        generator.add_to_session_file(args.session_file, metadata)
    elif args.dry_run:
        print("\n(Dry run - no files modified)")


if __name__ == "__main__":
    main()
