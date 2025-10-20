#!/usr/bin/env python3
"""
Session Protocol for CLI Agent Template
Enhanced with state persistence and better session management

ARCH-001: Self-contained architecture - no external dependencies
All patterns must be installed locally, no parent directory references
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

# ANSI color codes
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'


class SessionState:
    """Manage persistent session state"""

    def __init__(self):
        self.state_file = Path('.session_state.json')
        self.state = self.load()

    def load(self):
        """Load session state from disk"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    loaded_state = json.load(f)
                    # Ensure all required keys exist
                    default = self.default_state()
                    for key in default:
                        if key not in loaded_state:
                            loaded_state[key] = default[key]
                    # Ensure current_session has all required keys
                    if 'current_session' in loaded_state:
                        for key in default['current_session']:
                            if key not in loaded_state['current_session']:
                                loaded_state['current_session'][key] = default['current_session'][key]
                    return loaded_state
            except (json.JSONDecodeError, IOError):
                return self.default_state()
        return self.default_state()

    def default_state(self):
        """Return default state structure"""
        return {
            'last_wake': None,
            'last_wind_down': None,
            'session_count': 0,
            'total_commits': 0,
            'current_session': {
                'start_time': None,
                'tasks_completed': [],
                'files_modified': [],
                'tests_run': 0
            }
        }

    def save(self):
        """Save session state to disk"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2, default=str)
        except IOError as e:
            print(f"{YELLOW}⚠ Could not save session state: {e}{RESET}")

    def start_session(self):
        """Mark session start"""
        self.state['last_wake'] = datetime.now().isoformat()
        self.state['session_count'] += 1
        self.state['current_session'] = {
            'start_time': datetime.now().isoformat(),
            'tasks_completed': [],
            'files_modified': [],
            'tests_run': 0
        }
        self.save()

    def end_session(self):
        """Mark session end"""
        self.state['last_wind_down'] = datetime.now().isoformat()
        self.state['current_session']['end_time'] = datetime.now().isoformat()
        self.save()

    def get_session_duration(self):
        """Get current session duration"""
        if self.state['current_session']['start_time']:
            start = datetime.fromisoformat(self.state['current_session']['start_time'])
            return str(datetime.now() - start).split('.')[0]
        return "Unknown"


def run_command(cmd, check=False):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def organize_session_notes():
    """Organize SESSION_NOTES into dated subdirectories"""
    session_dir = Path('SESSION_NOTES')
    if not session_dir.exists():
        session_dir.mkdir(parents=True)
        return

    # Move flat session files into dated directories
    for session_file in session_dir.glob('session_*.md'):
        if session_file.is_file():
            # Extract date from filename (session_YYYYMMDD_HHMM.md)
            try:
                parts = session_file.stem.split('_')
                if len(parts) >= 2:
                    date_str = parts[1]
                    if len(date_str) >= 8 and date_str[:8].isdigit():
                        year = date_str[:4]
                        month = date_str[4:6]
                        day = date_str[6:8]
                        date_dir = session_dir / f"{year}-{month}-{day}"
                        date_dir.mkdir(exist_ok=True)

                        # Move file to dated directory
                        new_path = date_dir / session_file.name
                        if not new_path.exists():
                            session_file.rename(new_path)
            except (IndexError, ValueError, OSError):
                # Skip files that don't match expected format or can't be moved
                pass

    # Archive old sessions (>30 days)
    archive_dir = session_dir / 'archive'
    cutoff = datetime.now() - timedelta(days=30)

    for date_dir in session_dir.glob('????-??-??'):
        if date_dir.is_dir():
            try:
                dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d')
                if dir_date < cutoff:
                    archive_dir.mkdir(exist_ok=True)
                    archive_target = archive_dir / date_dir.name
                    if not archive_target.exists():
                        date_dir.rename(archive_target)
            except ValueError:
                pass


def wake():
    """Wake up protocol - Initialize session with state management"""
    state = SessionState()
    state.start_session()

    print(f"{BOLD}{BLUE}## Wake Up - {datetime.now():%Y-%m-%d %H:%M}{RESET}")

    # Show session info
    if state.state['last_wake']:
        last_wake = datetime.fromisoformat(state.state['last_wake'])
        time_since = str(datetime.now() - last_wake).split('.')[0]
        print(f"📅 Last session: {time_since} ago")
    print(f"🔢 Session #{state.state['session_count']}")

    # Show current directory
    cwd = Path.cwd()
    print(f"📍 {cwd}")

    # Check git status
    git_status = run_command("git status --short")
    if git_status:
        change_count = len(git_status.split('\n'))
        print(f"🔄 {change_count} uncommitted changes")
        # Track modified files
        state.state['current_session']['files_modified'] = git_status.split('\n')
    else:
        print(f"{GREEN}✓ Git repository clean{RESET}")

    # Check pattern status (improved detection)
    patterns_dir = cwd / 'patterns'
    patterns_found = []
    if patterns_dir.exists():
        for pattern_dir in patterns_dir.iterdir():
            if pattern_dir.is_dir() and not pattern_dir.name.startswith('.'):
                patterns_found.append(pattern_dir.name)

    if patterns_found:
        print(f"📦 Patterns available: {', '.join(sorted(patterns_found))}")

    # Check templates
    templates_dir = cwd / 'templates'
    templates_found = []
    if templates_dir.exists():
        for template_dir in templates_dir.iterdir():
            if template_dir.is_dir() and not template_dir.name.startswith('.'):
                templates_found.append(template_dir.name)

    if templates_found:
        print(f"📄 Templates: {', '.join(sorted(templates_found))}")

    # Check if tests exist
    test_count = len(list((cwd / 'tests').glob('test_*.py'))) if (cwd / 'tests').exists() else 0
    if test_count > 0:
        print(f"🧪 Tests: {test_count} test files found")

    # Organize session notes
    organize_session_notes()

    print(f"{GREEN}✅ Ready for tasks.{RESET}")
    state.save()


def wind_down():
    """Wind down protocol - Save session state"""
    state = SessionState()

    print(f"{BOLD}{BLUE}## Wind Down - {datetime.now():%Y-%m-%d %H:%M}{RESET}")
    print(f"⏱ Session duration: {state.get_session_duration()}")

    # Check for uncommitted changes
    git_status = run_command("git status --short")

    if git_status:
        print("📝 Committing changes...")
        run_command("git add -A")

        # Create commit message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_msg = f"session: Wind down at {timestamp}"

        run_command(f'git commit -m "{commit_msg}"')
        print(f"{GREEN}✓ Changes committed{RESET}")
        state.state['total_commits'] += 1
    else:
        print("✓ No changes to commit")

    # Run tests if they exist
    if Path('tests').exists():
        print("🧪 Running tests...")
        result = run_command("python -m pytest tests/ -q")
        if result:
            print(f"{GREEN}✓ Tests passed{RESET}")
            state.state['current_session']['tests_run'] += 1
        else:
            print(f"{YELLOW}⚠ Some tests may have failed{RESET}")

    # Create session note in dated directory
    session_dir = Path('SESSION_NOTES')
    date_str = datetime.now().strftime('%Y-%m-%d')
    date_dir = session_dir / date_str
    date_dir.mkdir(parents=True, exist_ok=True)

    session_file = date_dir / f"session_{datetime.now():%H%M}.md"
    with open(session_file, 'w') as f:
        f.write(f"# Session Notes - {datetime.now():%Y-%m-%d %H:%M}\n\n")
        f.write(f"## Metadata\n")
        f.write(f"- Duration: {state.get_session_duration()}\n")
        f.write(f"- Session #: {state.state['session_count']}\n")
        f.write(f"- Working directory: {Path.cwd()}\n")
        f.write(f"- Git status: {'Clean' if not git_status else 'Changes committed'}\n")
        f.write(f"- Tests run: {state.state['current_session']['tests_run']}\n")

        if state.state['current_session']['files_modified']:
            f.write(f"\n## Files Modified\n")
            for file in state.state['current_session']['files_modified'][:10]:  # First 10
                f.write(f"- {file}\n")

        f.write(f"\n## Patterns Status\n")
        patterns_dir = Path('patterns')
        if patterns_dir.exists():
            for pattern in sorted(patterns_dir.glob('*/*.py')):
                f.write(f"- {pattern.relative_to(patterns_dir)}\n")

    print(f"📝 Session note: {date_str}/{session_file.name}")

    # Update state
    state.end_session()

    # Clean up old sessions
    organize_session_notes()

    print(f"{GREEN}✅ Session preserved.{RESET}")


def sign_off(force_push=False, status_only=False):
    """Sign off protocol - Quick commit and push

    Args:
        force_push: If True, attempt push even if dry-run fails
        status_only: If True, only show status without making changes
    """
    state = SessionState()

    # Phase 3: Load configuration
    config_file = Path('.session_config.json')
    config = {}
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except:
            pass

    print(f"{BOLD}{BLUE}## Sign Off - {datetime.now():%Y-%m-%d %H:%M}{RESET}")
    print(f"⏱ Session duration: {state.get_session_duration()}")

    # Phase 3: Status check mode
    if status_only:
        git_status = run_command("git status --short")
        unpushed = run_command("git log @{u}..HEAD --oneline 2>/dev/null")
        print(f"📊 Status:")
        print(f"  • Uncommitted: {len(git_status.splitlines()) if git_status else 0} files")
        print(f"  • Unpushed: {len(unpushed.splitlines()) if unpushed else 0} commits")
        if config.get('default_branch'):
            print(f"  • Default branch: {config['default_branch']}")
        return

    # Quick commit
    git_status = run_command("git status --short")

    if git_status:
        run_command("git add -A")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_msg = f"chore: Quick sign off at {timestamp}"
        run_command(f'git commit -m "{commit_msg}"')
        print(f"{GREEN}✓ Changes committed{RESET}")
        state.state['total_commits'] += 1
    else:
        print("✓ No changes to commit")

    # Check if we have a remote
    remote = run_command("git remote -v")
    if remote and 'origin' in remote:
        print("📤 Pushing to remote...")

        # Phase 1 Fix: Use current branch instead of guessing
        current_branch = run_command("git branch --show-current")
        if current_branch:
            current_branch = current_branch.strip()

            # Phase 2: Add dry-run check first
            dry_run = run_command(f"git push --dry-run origin {current_branch} 2>&1")
            if dry_run and 'rejected' in dry_run.lower() and not force_push:
                print(f"{YELLOW}⚠ Push would be rejected. Pull first or use --force-push{RESET}")
                print(f"  Details: {dry_run.split('error:')[1] if 'error:' in dry_run else dry_run[:100]}")
                return

            # Attempt actual push with retry logic
            max_retries = config.get('max_retries', 3)
            for attempt in range(max_retries):
                result = run_command(f"git push origin {current_branch} 2>&1")

                # Check for success
                if result and 'error' not in result.lower() and 'rejected' not in result.lower():
                    # Verify push succeeded
                    verify = run_command(f"git log origin/{current_branch}..{current_branch} --oneline")
                    if not verify:  # No commits ahead means push succeeded
                        print(f"{GREEN}✓ Pushed to origin/{current_branch}{RESET}")

                        # Phase 3: Save successful branch to config
                        if not config.get('default_branch'):
                            config['default_branch'] = current_branch
                            try:
                                with open(config_file, 'w') as f:
                                    json.dump(config, f, indent=2)
                            except:
                                pass

                        # Auto-setup origin/HEAD if missing
                        if not run_command("git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null"):
                            run_command(f"git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/{current_branch}")
                        break

                # Handle specific errors
                if result and 'connection' in result.lower() and attempt < max_retries - 1:
                    print(f"{YELLOW}⚠ Network error, retrying ({attempt + 1}/{max_retries})...{RESET}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"{YELLOW}⚠ Push failed: {result if result else 'Unknown error'}{RESET}")
                    break
        else:
            print(f"{YELLOW}⚠ Could not determine current branch{RESET}")
    else:
        print("ℹ No remote configured")

    # Quick session note
    state.end_session()

    print(f"{GREEN}✅ Signed off.{RESET}")


def status():
    """Show current session status"""
    state = SessionState()

    print(f"{BOLD}{BLUE}## Session Status{RESET}")
    print(f"📊 Total sessions: {state.state['session_count']}")
    print(f"💾 Total commits: {state.state['total_commits']}")

    if state.state['last_wake']:
        print(f"🌅 Last wake: {state.state['last_wake']}")
    if state.state['last_wind_down']:
        print(f"🌙 Last wind down: {state.state['last_wind_down']}")

    if state.state['current_session']['start_time']:
        print(f"⏱ Current session: {state.get_session_duration()}")
        print(f"📝 Files modified: {len(state.state['current_session']['files_modified'])}")
        print(f"🧪 Tests run: {state.state['current_session']['tests_run']}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [wake|wind-down|sign-off|status] [options]")
        print(f"       sign-off options: --force-push, --status")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == 'wake':
        wake()
    elif command == 'wind-down':
        wind_down()
    elif command == 'sign-off':
        force_push = '--force-push' in args
        status_only = '--status' in args
        sign_off(force_push=force_push, status_only=status_only)
    elif command == 'status':
        status()
    else:
        print(f"{RED}Unknown command: {command}{RESET}")
        print("Valid commands: wake, wind-down, sign-off, status")
        sys.exit(1)


if __name__ == '__main__':
    main()
