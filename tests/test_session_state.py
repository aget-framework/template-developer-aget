"""
Tests for session state management
"""

import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.aget_session_protocol import SessionState, organize_session_notes


class TestSessionState:
    """Test SessionState class"""

    def test_default_state(self):
        """Test default state creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            state = SessionState()
            assert state.state['session_count'] == 0
            assert state.state['total_commits'] == 0
            assert state.state['last_wake'] is None
            assert state.state['last_wind_down'] is None

    def test_save_and_load(self):
        """Test state persistence"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create and save state
            state1 = SessionState()
            state1.state['session_count'] = 5
            state1.state['total_commits'] = 10
            state1.save()

            # Load in new instance
            state2 = SessionState()
            assert state2.state['session_count'] == 5
            assert state2.state['total_commits'] == 10

    def test_start_session(self):
        """Test session start tracking"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            state = SessionState()

            initial_count = state.state['session_count']
            state.start_session()

            assert state.state['session_count'] == initial_count + 1
            assert state.state['last_wake'] is not None
            assert state.state['current_session']['start_time'] is not None

    def test_end_session(self):
        """Test session end tracking"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            state = SessionState()

            state.start_session()
            state.end_session()

            assert state.state['last_wind_down'] is not None
            assert 'end_time' in state.state['current_session']

    def test_get_session_duration(self):
        """Test duration calculation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            state = SessionState()

            # No session started
            assert state.get_session_duration() == "Unknown"

            # Start session
            state.start_session()
            duration = state.get_session_duration()
            assert duration != "Unknown"
            assert ":" in duration  # Should be in HH:MM:SS format

    def test_corrupt_state_file(self):
        """Test handling of corrupted state file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create corrupt state file
            with open('.session_state.json', 'w') as f:
                f.write("not valid json{")

            # Should fall back to default state
            state = SessionState()
            assert state.state['session_count'] == 0


class TestOrganizeSessionNotes:
    """Test session notes organization"""

    def test_create_session_dir(self):
        """Test SESSION_NOTES directory creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            organize_session_notes()
            assert Path('SESSION_NOTES').exists()

    def test_organize_flat_files(self):
        """Test organizing flat session files into dated directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create SESSION_NOTES with flat files
            session_dir = Path('SESSION_NOTES')
            session_dir.mkdir()

            # Use recent dates that won't be archived (within last 30 days)
            today = datetime.now()
            yesterday = today - timedelta(days=1)

            # Format dates as YYYYMMDD
            today_str = today.strftime('%Y%m%d')
            yesterday_str = yesterday.strftime('%Y%m%d')

            # Create test session files with recent dates
            (session_dir / f'session_{today_str}_1430.md').touch()
            (session_dir / f'session_{yesterday_str}_0900.md').touch()

            organize_session_notes()

            # Check files were moved to dated directories (YYYY-MM-DD format)
            today_dir = today.strftime('%Y-%m-%d')
            yesterday_dir = yesterday.strftime('%Y-%m-%d')

            assert (session_dir / today_dir / f'session_{today_str}_1430.md').exists()
            assert (session_dir / yesterday_dir / f'session_{yesterday_str}_0900.md').exists()

    def test_archive_old_sessions(self):
        """Test archiving sessions older than 30 days"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            session_dir = Path('SESSION_NOTES')
            session_dir.mkdir()

            # Create old dated directory (>30 days)
            old_date = datetime.now() - timedelta(days=35)
            old_dir = session_dir / old_date.strftime('%Y-%m-%d')
            old_dir.mkdir()
            (old_dir / 'session_1000.md').touch()

            # Create recent directory (<30 days)
            recent_date = datetime.now() - timedelta(days=5)
            recent_dir = session_dir / recent_date.strftime('%Y-%m-%d')
            recent_dir.mkdir()
            (recent_dir / 'session_1100.md').touch()

            organize_session_notes()

            # Check old directory was archived
            assert (session_dir / 'archive' / old_date.strftime('%Y-%m-%d')).exists()
            # Check recent directory remains
            assert recent_dir.exists()
            assert not (session_dir / 'archive' / recent_date.strftime('%Y-%m-%d')).exists()

    def test_skip_invalid_filenames(self):
        """Test handling of files with invalid names"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            session_dir = Path('SESSION_NOTES')
            session_dir.mkdir()

            # Create files with invalid names
            (session_dir / 'random_file.md').touch()
            (session_dir / 'session_invalid.md').touch()

            organize_session_notes()

            # Files should remain in place
            assert (session_dir / 'random_file.md').exists()
            assert (session_dir / 'session_invalid.md').exists()


def test_imports():
    """Test that all required imports work"""
    from scripts import aget_session_protocol
    assert hasattr(aget_session_protocol, 'wake')
    assert hasattr(aget_session_protocol, 'wind_down')
    assert hasattr(aget_session_protocol, 'sign_off')
    assert hasattr(aget_session_protocol, 'status')
    assert hasattr(aget_session_protocol, 'SessionState')
    assert hasattr(aget_session_protocol, 'organize_session_notes')