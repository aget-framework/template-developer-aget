"""
Rollback Command - Restore previous configuration
Implements three-tier degradation pattern.
"""

import subprocess
from pathlib import Path
from typing import Any, Dict

from aget.base import BaseCommand
from aget.shared.backup import BackupManager


class RollbackCommand(BaseCommand):
    """Rollback to previous configuration state."""

    def tier_basic(self, **kwargs) -> Dict[str, Any]:
        """
        Basic tier - Restore from .aget/backups/ directory.
        """
        args = kwargs.get('args', [])

        # Get backup ID if specified
        backup_id = None
        if args and len(args) > 0 and not args[0].startswith('--'):
            backup_id = args[0]

        # Create backup manager
        manager = BackupManager()

        # List available backups if requested
        if '--list' in args:
            backups = manager.list_backups()
            return {
                'success': True,
                'action': 'list',
                'backups': backups,
                'message': f'Found {len(backups)} backup(s)'
            }

        # Perform rollback
        result = manager.rollback(backup_id)

        if result['status'] == 'success':
            return {
                'success': True,
                'backup_id': result['backup_id'],
                'files_restored': result['files_restored'],
                'pre_rollback_backup': result['pre_rollback_backup'],
                'message': result['message']
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown error')
            }

    def tier_git(self, **kwargs) -> Dict[str, Any]:
        """
        Git tier - Also create git commit documenting rollback.
        """
        # First do basic rollback
        result = self.tier_basic(**kwargs)
        if not result['success'] or result.get('action') == 'list':
            return result

        # Create git commit
        try:
            backup_id = result['backup_id']
            message = f"rollback: Restored configuration from {backup_id}"

            subprocess.run(
                ['git', 'add', 'AGENTS.md', 'CLAUDE.md', '.aget/'],
                capture_output=True,
                timeout=2
            )

            subprocess.run(
                ['git', 'commit', '-m', message],
                capture_output=True,
                timeout=2
            )

            result['git_commit'] = True
            result['message'] += ' (git: committed)'
        except Exception as e:
            result['git_commit'] = False
            result['git_error'] = str(e)

        return result

    def tier_gh(self, **kwargs) -> Dict[str, Any]:
        """
        GitHub CLI tier - Also create issue documenting rollback.
        """
        # First do git tier
        result = self.tier_git(**kwargs)
        if not result['success'] or result.get('action') == 'list':
            return result

        # Create GitHub issue
        try:
            backup_id = result['backup_id']
            title = f"Configuration rolled back to {backup_id}"
            body = f"""## Rollback Report

**Backup ID**: {backup_id}
**Files Restored**: {result['files_restored']}
**Pre-rollback Backup**: {result['pre_rollback_backup']}

This is an automated report from AGET v2 rollback operation.
"""

            gh_result = subprocess.run(
                ['gh', 'issue', 'create',
                 '--title', title,
                 '--body', body,
                 '--label', 'rollback'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if gh_result.returncode == 0:
                result['gh_issue'] = True
                result['issue_url'] = gh_result.stdout.strip()
                result['message'] += ' (gh: issue created)'
            else:
                result['gh_issue'] = False
        except Exception as e:
            result['gh_issue'] = False
            result['gh_error'] = str(e)

        return result