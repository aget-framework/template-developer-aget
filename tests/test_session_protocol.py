"""
Tests for session protocol functionality
"""

import sys
import os
from pathlib import Path
import subprocess
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_wake_command_exists():
    """Test that wake command is callable"""
    script_path = Path(__file__).parent.parent / 'scripts' / 'aget_session_protocol.py'
    result = subprocess.run(
        [sys.executable, str(script_path), 'wake'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    assert result.returncode == 0
    assert "Wake Up" in result.stdout or "Ready for tasks" in result.stdout


def test_session_protocol_imports():
    """Test that session protocol can be imported"""
    from scripts import aget_session_protocol
    assert hasattr(aget_session_protocol, 'wake')
    assert hasattr(aget_session_protocol, 'wind_down')
    assert hasattr(aget_session_protocol, 'sign_off')


def test_wake_output_format():
    """Test that wake produces expected output format"""
    script_path = Path(__file__).parent.parent / 'scripts' / 'aget_session_protocol.py'
    result = subprocess.run(
        [sys.executable, str(script_path), 'wake'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    # Check for expected elements
    assert "📍" in result.stdout  # Location marker
    assert "📦" in result.stdout  # Patterns marker
    assert "📄" in result.stdout  # Templates marker
    assert "✅" in result.stdout  # Ready marker


def test_invalid_command():
    """Test that invalid command returns error"""
    script_path = Path(__file__).parent.parent / 'scripts' / 'aget_session_protocol.py'
    result = subprocess.run(
        [sys.executable, str(script_path), 'invalid'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    assert result.returncode == 1
    assert "Unknown command" in result.stdout


def test_pattern_detection():
    """Test that patterns are detected correctly"""
    # Create a temporary patterns directory
    with tempfile.TemporaryDirectory() as tmpdir:
        patterns_dir = Path(tmpdir) / 'patterns'
        patterns_dir.mkdir()

        # Create pattern subdirectories
        for pattern in ['session', 'housekeeping']:
            (patterns_dir / pattern).mkdir()
            (patterns_dir / pattern / 'README.md').touch()

        # Run wake in the temp directory
        script_path = Path(__file__).parent.parent / 'scripts' / 'aget_session_protocol.py'
        result = subprocess.run(
            [sys.executable, str(script_path), 'wake'],
            capture_output=True,
            text=True,
            cwd=tmpdir
        )

        # Should detect the patterns we created
        assert "session" in result.stdout or "housekeeping" in result.stdout


if __name__ == '__main__':
    # Simple test runner for manual testing
    import pytest
    pytest.main([__file__, '-v'])