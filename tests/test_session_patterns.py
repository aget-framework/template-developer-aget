"""Test session patterns."""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import time

sys.path.insert(0, '.')
from patterns.session.wake import WakeProtocol
from patterns.session.wind_down import WindDownProtocol
from patterns.session.sign_off import SignOffProtocol


def create_test_project(tmpdir: Path):
    """Create a test project structure."""
    tmpdir.mkdir(exist_ok=True)

    # Create AGENTS.md
    agents_file = tmpdir / "AGENTS.md"
    agents_file.write_text("""# Agent Configuration
## Session Protocols
Wake up protocol configured.
""")

    # Create git repo
    import subprocess
    subprocess.run(['git', 'init'], cwd=tmpdir, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=tmpdir, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=tmpdir, capture_output=True)
    subprocess.run(['git', 'add', '.'], cwd=tmpdir, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Initial'], cwd=tmpdir, capture_output=True)

    # Create patterns
    (tmpdir / "patterns" / "session").mkdir(parents=True)
    (tmpdir / "patterns" / "housekeeping").mkdir(parents=True)

    # Create tests
    (tmpdir / "tests").mkdir()
    (tmpdir / "tests" / "test_example.py").write_text("# Test file")

    # Commit everything to git
    subprocess.run(['git', 'add', '.'], cwd=tmpdir, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Add tests'], cwd=tmpdir, capture_output=True)

    return tmpdir


def test_wake_protocol_first_session():
    """Test wake protocol on first session."""
    print("Testing wake protocol - first session...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_test_project(Path(tmpdir))

        # Execute wake protocol
        protocol = WakeProtocol(project)
        result = protocol.execute()

        # Check result structure
        assert 'timestamp' in result
        assert 'status' in result
        assert result['status'] == 'ready'
        assert result['session_number'] == 1
        assert result['last_session'] == 'First session'

        # Check git status was checked
        assert 'git' in result['checks']
        assert result['checks']['git']['is_repo'] == True
        assert result['checks']['git']['clean'] == True

        # Check patterns were found
        assert 'patterns' in result['checks']
        assert 'session' in result['checks']['patterns']
        assert 'housekeeping' in result['checks']['patterns']

        # Check tests were counted (we created test_example.py)
        assert 'tests' in result['checks']
        assert result['checks']['tests'] >= 1  # At least one test file

        print("✅ First session wake protocol works")


def test_wake_protocol_subsequent_session():
    """Test wake protocol on subsequent sessions."""
    print("\nTesting wake protocol - subsequent session...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_test_project(Path(tmpdir))

        # First session
        protocol = WakeProtocol(project)
        result1 = protocol.execute()
        assert result1['session_number'] == 1

        # Wait a moment
        time.sleep(0.1)

        # Second session
        result2 = protocol.execute()
        assert result2['session_number'] == 2
        assert result2['last_session'] != 'First session'
        assert 'Just now' in result2['last_session'] or 'seconds' in result2['last_session']

        print(f"✅ Session tracking works (session #{result2['session_number']})")
        print(f"✅ Time tracking works ({result2['last_session']})")


def test_session_state_persistence():
    """Test that session state persists."""
    print("\nTesting session state persistence...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_test_project(Path(tmpdir))

        # Create first protocol instance
        protocol1 = WakeProtocol(project)
        result1 = protocol1.execute()

        # Check state file was created
        state_file = project / ".session_state.json"
        assert state_file.exists(), "State file should be created"

        # Load state directly
        state = json.loads(state_file.read_text())
        assert state['session_count'] == 1
        assert state['last_wake'] is not None
        assert 'current_session' in state

        # Create new protocol instance (simulating new agent session)
        protocol2 = WakeProtocol(project)
        result2 = protocol2.execute()

        # Check state was updated
        state = json.loads(state_file.read_text())
        assert state['session_count'] == 2

        print("✅ Session state persists correctly")


def test_git_dirty_detection():
    """Test detection of uncommitted changes."""
    print("\nTesting git dirty detection...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_test_project(Path(tmpdir))

        # Create uncommitted change
        (project / "new_file.txt").write_text("uncommitted")

        protocol = WakeProtocol(project)
        result = protocol.execute()

        assert result['checks']['git']['clean'] == False
        assert len(result['checks']['git']['changes']) > 0

        print("✅ Detects uncommitted git changes")


def test_wake_protocol_performance():
    """Test that wake protocol completes quickly."""
    print("\nTesting wake protocol performance...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_test_project(Path(tmpdir))

        protocol = WakeProtocol(project)

        start = time.time()
        result = protocol.execute()
        duration = time.time() - start

        assert duration < 2.0, f"Wake protocol took {duration:.2f}s (should be <2s)"
        print(f"✅ Performance: {duration:.3f}s (requirement: <2s)")


def test_wind_down_protocol():
    """Test wind down protocol."""
    print("\nTesting wind down protocol...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_test_project(Path(tmpdir))

        # First run wake
        wake = WakeProtocol(project)
        wake_result = wake.execute()
        assert wake_result['session_number'] == 1

        # Create a change to commit
        (project / "test_file.txt").write_text("test content")

        # Run wind down
        wind_down = WindDownProtocol(project)
        result = wind_down.execute()

        assert result['status'] == 'completed'
        assert 'actions' in result

        # Check that actions were taken
        actions = {a['action']: a for a in result['actions']}
        assert 'git_commit' in actions
        assert 'session_notes' in actions
        assert 'run_tests' in actions

        # Check session notes were created
        session_notes = project / "SESSION_NOTES"
        assert session_notes.exists(), "SESSION_NOTES directory should exist"

        # Check state was updated
        state_file = project / ".session_state.json"
        state = json.loads(state_file.read_text())
        assert 'last_wind_down' in state
        assert 'end_time' in state['current_session']

        print("✅ Wind down protocol works")


def test_wind_down_no_changes():
    """Test wind down with no uncommitted changes."""
    print("\nTesting wind down with clean repo...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_test_project(Path(tmpdir))

        wind_down = WindDownProtocol(project)
        result = wind_down.execute()

        # Should still complete successfully
        assert result['status'] == 'completed'

        # Check git commit action shows no changes
        actions = {a['action']: a for a in result['actions']}
        git_action = actions.get('git_commit', {})
        assert git_action.get('reason') == 'no changes' or git_action.get('success')

        print("✅ Handles clean repository correctly")


def test_session_lifecycle():
    """Test complete session lifecycle: wake → work → wind_down."""
    print("\nTesting complete session lifecycle...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_test_project(Path(tmpdir))

        # 1. Wake up
        wake = WakeProtocol(project)
        wake_result = wake.execute()
        assert wake_result['session_number'] == 1
        assert wake_result['status'] == 'ready'

        # 2. Do some work (simulate)
        time.sleep(0.1)  # Brief pause to have measurable duration
        (project / "work.txt").write_text("work done")

        # 3. Wind down
        wind_down = WindDownProtocol(project)
        wind_result = wind_down.execute()
        assert wind_result['status'] == 'completed'
        assert wind_result['session_number'] == 1

        # 4. Check state consistency
        state_file = project / ".session_state.json"
        state = json.loads(state_file.read_text())
        assert state['session_count'] == 1
        assert state['last_wake'] is not None
        assert state['last_wind_down'] is not None

        print("✅ Complete lifecycle works correctly")


def test_sign_off_protocol():
    """Test sign off protocol - quick save and exit."""
    print("\nTesting sign off protocol...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        project = create_test_project(Path(tmpdir))

        # Create a change
        (project / "quick_work.txt").write_text("quick save needed")

        # Run sign off
        sign_off = SignOffProtocol(project)
        result = sign_off.execute()

        assert result['status'] == 'signed_off'
        assert 'actions' in result

        # Check that quick commit was attempted
        actions = {a['action']: a for a in result['actions'] if 'action' in a}
        assert 'quick_commit' in actions or 'push' in actions

        # Check state was updated
        state_file = project / ".session_state.json"
        if state_file.exists():
            state = json.loads(state_file.read_text())
            assert 'last_sign_off' in state

        print("✅ Sign off protocol works")


if __name__ == "__main__":
    print("🌅 Session Pattern Tests")
    print("=" * 40)

    test_wake_protocol_first_session()
    test_wake_protocol_subsequent_session()
    test_session_state_persistence()
    test_git_dirty_detection()
    test_wake_protocol_performance()
    test_wind_down_protocol()
    test_wind_down_no_changes()
    test_session_lifecycle()
    test_sign_off_protocol()

    print("\n" + "=" * 40)
    print("✅ ALL SESSION PATTERN TESTS PASSED")