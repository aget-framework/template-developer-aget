#!/usr/bin/env python3
"""
Sign Off Protocol Pattern - Quick save and exit without prompts.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class SignOffProtocol:
    """Sign off protocol for quick session exit."""

    def __init__(self, project_path: Path = Path.cwd()):
        """Initialize sign off protocol."""
        self.project_path = Path(project_path)
        self.state_file = self.project_path / ".session_state.json"

    def execute(self) -> Dict[str, Any]:
        """
        Execute sign off protocol - quick save and exit.

        Returns:
            Status information about the quick save
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'status': 'signed_off',
            'actions': []
        }

        print(f"{self._bold()}{self._blue()}## Sign Off - {datetime.now():%Y-%m-%d %H:%M}{self._reset()}")

        # Quick commit if there are changes
        git_status = self._check_git_status()
        if git_status['has_changes']:
            # Quick commit without detailed message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            # Add file count to message for better tracking
            change_count = git_status.get('count', 0)
            message = f"checkpoint: Quick save at {timestamp} ({change_count} files)"

            try:
                # Stage and commit
                subprocess.run(
                    ['git', 'add', '-A'],
                    cwd=self.project_path,
                    capture_output=True,
                    timeout=2
                )

                subprocess.run(
                    ['git', 'commit', '-m', message],
                    cwd=self.project_path,
                    capture_output=True,
                    timeout=2
                )

                print(f"{self._green()}✓ Changes saved{self._reset()}")
                result['actions'].append({
                    'action': 'quick_commit',
                    'success': True,
                    'changes': git_status['count']
                })

            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                print(f"{self._yellow()}⚠ Could not save changes: {e.__class__.__name__}{self._reset()}")
                result['actions'].append({
                    'action': 'quick_commit',
                    'success': False,
                    'error': e.__class__.__name__
                })
        else:
            print(f"{self._green()}✓ No changes to save{self._reset()}")
            result['actions'].append({
                'action': 'quick_commit',
                'skipped': True,
                'reason': 'no_changes'
            })

        # Try to push if origin exists
        push_result = self._try_push()
        if push_result['attempted']:
            result['actions'].append(push_result)
            if push_result['success']:
                print(f"{self._green()}✓ Pushed to remote{self._reset()}")
            else:
                reason = push_result.get('reason', 'network issue')
                print(f"ℹ️ Push failed ({reason}) - changes saved locally")
        elif push_result.get('reason') == 'no_remote':
            print(f"ℹ️ No remote configured (local only)")

        # Quick state update with error handling
        state = self._load_state()
        state['last_sign_off'] = datetime.now().isoformat()

        # Track quick saves for metrics
        if 'quick_saves' not in state:
            state['quick_saves'] = 0
        state['quick_saves'] += 1

        if not self._save_state(state):
            print(f"{self._yellow()}⚠ Could not save state (continuing anyway){self._reset()}")

        # Final message - always brief
        print(f"{self._green()}✅ Signed off.{self._reset()}")

        return result

    def _load_state(self) -> Dict[str, Any]:
        """Load session state from disk with recovery."""
        if self.state_file.exists():
            try:
                content = self.state_file.read_text()
                if content.strip():
                    return json.loads(content)
            except (json.JSONDecodeError, IOError) as e:
                # Try backup recovery
                backup_file = self.state_file.with_suffix('.backup')
                if backup_file.exists():
                    try:
                        return json.loads(backup_file.read_text())
                    except:
                        pass
        return {}

    def _save_state(self, state: Dict[str, Any]) -> bool:
        """Save session state to disk with backup.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup if state exists
            if self.state_file.exists():
                try:
                    backup_file = self.state_file.with_suffix('.backup')
                    backup_file.write_text(self.state_file.read_text())
                except:
                    pass

            # Save new state
            self.state_file.write_text(json.dumps(state, indent=2, default=str))
            return True
        except (IOError, OSError):
            return False

    def _check_git_status(self) -> Dict[str, Any]:
        """Quick check for uncommitted changes."""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=1
            )

            if result.returncode != 0:
                return {'has_changes': False, 'is_repo': False}

            changes = result.stdout.strip()
            if changes:
                return {
                    'has_changes': True,
                    'is_repo': True,
                    'count': len(changes.split('\n'))
                }

            return {'has_changes': False, 'is_repo': True}

        except:
            return {'has_changes': False, 'is_repo': False}

    def _try_push(self) -> Dict[str, Any]:
        """Try to push to remote if available."""
        try:
            # Check if remote exists
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=self.project_path,
                capture_output=True,
                timeout=1
            )

            if result.returncode != 0:
                return {
                    'action': 'push',
                    'attempted': False,
                    'reason': 'no_remote'
                }

            # Check if we have anything to push first
            status_result = subprocess.run(
                ['git', 'status', '-sb'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=1
            )

            if 'ahead' not in status_result.stdout:
                return {
                    'action': 'push',
                    'attempted': False,
                    'reason': 'nothing_to_push'
                }

            # Try to push (with short timeout)
            result = subprocess.run(
                ['git', 'push'],
                cwd=self.project_path,
                capture_output=True,
                timeout=5
            )

            return {
                'action': 'push',
                'attempted': True,
                'success': result.returncode == 0
            }

        except subprocess.TimeoutExpired:
            return {
                'action': 'push',
                'attempted': True,
                'success': False,
                'reason': 'timeout'
            }
        except:
            return {
                'action': 'push',
                'attempted': False,
                'reason': 'error'
            }

    # ANSI color helpers
    def _blue(self) -> str:
        return '\033[94m'

    def _green(self) -> str:
        return '\033[92m'

    def _yellow(self) -> str:
        return '\033[93m'

    def _bold(self) -> str:
        return '\033[1m'

    def _reset(self) -> str:
        return '\033[0m'


def apply_pattern(project_path: Path = Path.cwd()) -> Dict[str, Any]:
    """
    Apply sign off pattern to project.

    This is called by `aget apply session/sign_off`.
    """
    protocol = SignOffProtocol(project_path)
    return protocol.execute()


if __name__ == "__main__":
    # Execute sign off protocol
    apply_pattern()