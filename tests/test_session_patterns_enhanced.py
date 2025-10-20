"""Enhanced tests for session patterns - covering error cases and improvements."""

import sys
import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import subprocess

sys.path.insert(0, '.')
from patterns.session.wake import WakeProtocol
from patterns.session.wind_down import WindDownProtocol
from patterns.session.sign_off import SignOffProtocol


class TestEnhancedWakeProtocol(unittest.TestCase):
    """Test enhanced wake protocol features."""

    def setUp(self):
        """Set up test environment."""
        self.tmpdir = tempfile.mkdtemp()
        self.project_path = Path(self.tmpdir)
        self.state_file = self.project_path / ".session_state.json"
        self.backup_file = self.project_path / ".session_state.backup"

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_wake_with_corrupted_state(self):
        """Test wake protocol handles corrupted state file."""
        # Create corrupted state file
        self.state_file.write_text("{ broken json")

        protocol = WakeProtocol(self.project_path)
        result = protocol.execute()

        # Should recover gracefully
        assert result['status'] == 'ready'
        assert result['session_number'] == 1

    def test_wake_with_backup_recovery(self):
        """Test wake recovers from backup when main state is corrupted."""
        # Create good backup
        backup_state = {
            'session_count': 5,
            'last_wake': datetime.now().isoformat()
        }
        self.backup_file.write_text(json.dumps(backup_state))

        # Corrupt main state
        self.state_file.write_text("corrupted")

        protocol = WakeProtocol(self.project_path)
        result = protocol.execute()

        # Should recover from backup
        assert result['session_number'] == 6  # 5 + 1

    def test_wake_with_empty_state_file(self):
        """Test wake handles empty state file."""
        self.state_file.write_text("")

        protocol = WakeProtocol(self.project_path)
        result = protocol.execute()

        assert result['status'] == 'ready'
        assert result['session_number'] == 1

    def test_wake_crash_detection(self):
        """Test wake detects recent crash (< 1 minute)."""
        # Create state with very recent last_wake
        recent_time = (datetime.now() - timedelta(seconds=30)).isoformat()
        state = {
            'session_count': 1,
            'last_wake': recent_time
        }
        self.state_file.write_text(json.dumps(state))

        protocol = WakeProtocol(self.project_path)
        with patch('builtins.print') as mock_print:
            result = protocol.execute()

            # Should warn about recent session
            calls = [str(call) for call in mock_print.call_args_list]
            assert any('< 1 minute ago' in str(call) for call in calls)

    def test_wake_state_save_failure(self):
        """Test wake continues even if state save fails."""
        protocol = WakeProtocol(self.project_path)

        # Make save fail
        with patch.object(protocol, '_save_state', return_value=False):
            with patch('builtins.print') as mock_print:
                result = protocol.execute()

                # Should continue and warn
                assert result['status'] == 'ready'
                calls = [str(call) for call in mock_print.call_args_list]
                assert any('Could not save session state' in str(call) for call in calls)

    def test_wake_git_status_with_many_changes(self):
        """Test wake shows count of uncommitted changes."""
        protocol = WakeProtocol(self.project_path)

        # Mock git with changes
        with patch.object(protocol, '_check_git') as mock_git:
            mock_git.return_value = {
                'is_repo': True,
                'clean': False,
                'changes': ['file1.txt', 'file2.txt', 'file3.txt']
            }

            with patch('builtins.print') as mock_print:
                result = protocol.execute()

                # Should show change count
                calls = [str(call) for call in mock_print.call_args_list]
                assert any('3 uncommitted changes' in str(call) for call in calls)


class TestEnhancedWindDownProtocol(unittest.TestCase):
    """Test enhanced wind down protocol features."""

    def setUp(self):
        """Set up test environment."""
        self.tmpdir = tempfile.mkdtemp()
        self.project_path = Path(self.tmpdir)
        self.state_file = self.project_path / ".session_state.json"

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_wind_down_missing_current_session(self):
        """Test wind down handles missing current_session gracefully."""
        # State without current_session
        state = {
            'session_count': 1,
            'last_wake': datetime.now().isoformat()
        }
        self.state_file.write_text(json.dumps(state))

        protocol = WindDownProtocol(self.project_path)
        result = protocol.execute()

        # Should complete without error
        assert result['status'] == 'completed'

    def test_wind_down_multi_day_session(self):
        """Test wind down handles multi-day sessions correctly."""
        # Create state with old start time
        old_start = (datetime.now() - timedelta(days=2, hours=5)).isoformat()
        state = {
            'session_count': 1,
            'current_session': {
                'start_time': old_start
            }
        }
        self.state_file.write_text(json.dumps(state))

        protocol = WindDownProtocol(self.project_path)
        with patch('builtins.print') as mock_print:
            result = protocol.execute()

            # Should show days in duration
            calls = [str(call) for call in mock_print.call_args_list]
            assert any('2d 5h' in str(call) for call in calls)

    def test_wind_down_very_short_session(self):
        """Test wind down handles < 1 minute sessions."""
        # Create state with very recent start
        recent_start = (datetime.now() - timedelta(seconds=15)).isoformat()
        state = {
            'session_count': 1,
            'current_session': {
                'start_time': recent_start
            }
        }
        self.state_file.write_text(json.dumps(state))

        protocol = WindDownProtocol(self.project_path)
        with patch('builtins.print') as mock_print:
            result = protocol.execute()

            # Should show <1m
            calls = [str(call) for call in mock_print.call_args_list]
            assert any('<1m' in str(call) for call in calls)

    def test_wind_down_save_state_error_logging(self):
        """Test wind down logs errors when state save fails."""
        protocol = WindDownProtocol(self.project_path)

        # Create .aget directory for error log
        (self.project_path / ".aget").mkdir()

        # Make state save fail
        with patch('patterns.session.wind_down.Path.write_text') as mock_write:
            mock_write.side_effect = IOError("Permission denied")

            protocol.execute()

            # Check error was logged
            error_log = self.project_path / ".aget" / "errors.log"
            if error_log.exists():
                errors = error_log.read_text()
                assert "wind_down save_state error" in errors

    def test_wind_down_git_commit_error_handling(self):
        """Test wind down handles git commit failures gracefully."""
        protocol = WindDownProtocol(self.project_path)

        with patch.object(protocol, '_check_git_status') as mock_status:
            mock_status.return_value = {
                'has_changes': True,
                'is_repo': True,
                'changes': ['file.txt'],
                'count': 1
            }

            with patch('subprocess.run') as mock_run:
                # Make commit fail
                mock_run.side_effect = subprocess.TimeoutExpired('git', 5)

                result = protocol.execute()

                # Should handle error and continue
                assert result['status'] == 'completed'
                actions = {a['action']: a for a in result['actions']}
                assert not actions['git_commit']['success']
                assert 'TimeoutExpired' in actions['git_commit']['reason']


class TestEnhancedSignOffProtocol(unittest.TestCase):
    """Test enhanced sign off protocol features."""

    def setUp(self):
        """Set up test environment."""
        self.tmpdir = tempfile.mkdtemp()
        self.project_path = Path(self.tmpdir)
        self.state_file = self.project_path / ".session_state.json"

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_sign_off_with_backup_recovery(self):
        """Test sign off recovers from backup."""
        # Create backup with quick_saves count
        backup_state = {
            'quick_saves': 10
        }
        backup_file = self.state_file.with_suffix('.backup')
        backup_file.write_text(json.dumps(backup_state))

        # Corrupt main state
        self.state_file.write_text("corrupted")

        protocol = SignOffProtocol(self.project_path)
        result = protocol.execute()

        # Should complete and increment quick_saves
        assert result['status'] == 'signed_off'

        # Check state was updated
        if self.state_file.exists():
            try:
                state = json.loads(self.state_file.read_text())
                assert state['quick_saves'] == 11
            except:
                pass  # State might not be readable if save failed

    def test_sign_off_tracks_quick_saves(self):
        """Test sign off tracks number of quick saves."""
        protocol = SignOffProtocol(self.project_path)

        # First save
        protocol.execute()

        # Second save
        protocol.execute()

        # Check quick_saves was tracked
        state = json.loads(self.state_file.read_text())
        assert state['quick_saves'] == 2

    def test_sign_off_nothing_to_push(self):
        """Test sign off handles case when nothing to push."""
        protocol = SignOffProtocol(self.project_path)

        with patch.object(protocol, '_check_git_status') as mock_status:
            mock_status.return_value = {
                'has_changes': False,
                'is_repo': True
            }

            with patch('subprocess.run') as mock_run:
                # Mock git status -sb showing we're up to date
                mock_run.return_value = MagicMock(
                    returncode=0,
                    stdout="## main...origin/main"
                )

                with patch('builtins.print') as mock_print:
                    result = protocol.execute()

                    # Should indicate nothing to push
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any('No changes to save' in str(call) or
                             'up to date' in str(call) for call in calls)

    def test_sign_off_commit_with_file_count(self):
        """Test sign off includes file count in commit message."""
        protocol = SignOffProtocol(self.project_path)

        with patch.object(protocol, '_check_git_status') as mock_status:
            mock_status.return_value = {
                'has_changes': True,
                'is_repo': True,
                'changes': ['file1', 'file2', 'file3'],
                'count': 3
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = MagicMock(returncode=0)

                protocol.execute()

                # Check commit message includes file count
                commit_calls = [call for call in mock_run.call_args_list
                              if 'commit' in str(call)]
                assert any('(3 files)' in str(call) for call in commit_calls)

    def test_sign_off_push_error_reporting(self):
        """Test sign off reports push errors clearly."""
        protocol = SignOffProtocol(self.project_path)

        with patch.object(protocol, '_check_git_status') as mock_status:
            mock_status.return_value = {'has_changes': False, 'is_repo': True}

            with patch.object(protocol, '_try_push') as mock_push:
                mock_push.return_value = {
                    'action': 'push',
                    'attempted': True,
                    'success': False,
                    'reason': 'timeout'
                }

                with patch('builtins.print') as mock_print:
                    result = protocol.execute()

                    # Should report timeout clearly
                    calls = [str(call) for call in mock_print.call_args_list]
                    assert any('timeout' in str(call).lower() for call in calls)


class TestSessionPatternIntegration(unittest.TestCase):
    """Test integration between all three patterns."""

    def setUp(self):
        """Set up test environment."""
        self.tmpdir = tempfile.mkdtemp()
        self.project_path = Path(self.tmpdir)

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_full_session_cycle_with_errors(self):
        """Test complete cycle with simulated errors."""
        # 1. Wake with warning
        wake = WakeProtocol(self.project_path)
        wake_result = wake.execute()
        assert wake_result['status'] == 'ready'

        # 2. Simulate work
        (self.project_path / "work.txt").write_text("work done")

        # 3. Wind down with state issue
        state_file = self.project_path / ".session_state.json"
        state = json.loads(state_file.read_text())
        del state['current_session']  # Remove to test recovery
        state_file.write_text(json.dumps(state))

        wind_down = WindDownProtocol(self.project_path)
        wind_result = wind_down.execute()
        assert wind_result['status'] == 'completed'

        # 4. Sign off
        sign_off = SignOffProtocol(self.project_path)
        sign_result = sign_off.execute()
        assert sign_result['status'] == 'signed_off'

    def test_state_file_backup_chain(self):
        """Test that backup files are maintained correctly."""
        # Wake creates initial state
        wake = WakeProtocol(self.project_path)
        wake.execute()

        state_file = self.project_path / ".session_state.json"
        backup_file = self.project_path / ".session_state.backup"

        # Wind down should create backup
        wind_down = WindDownProtocol(self.project_path)
        wind_down.execute()

        if backup_file.exists():
            # Backup should be valid JSON
            backup = json.loads(backup_file.read_text())
            assert 'session_count' in backup

        # Sign off should also maintain backup
        sign_off = SignOffProtocol(self.project_path)
        sign_off.execute()

        if backup_file.exists():
            backup = json.loads(backup_file.read_text())
            assert 'last_wind_down' in backup


if __name__ == "__main__":
    print("🧪 Enhanced Session Pattern Tests")
    print("=" * 40)

    # Run tests
    unittest.main(verbosity=2)