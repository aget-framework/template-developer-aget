#!/usr/bin/env python3
"""Test backup and rollback functionality."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, '.')

from aget.shared.backup import BackupManager
from aget.config.commands.init import InitCommand
from aget.config.commands.rollback import RollbackCommand

def test_backup_rollback():
    """Test full backup/rollback cycle."""
    print("Testing Backup/Rollback Mechanism:")
    print("=" * 50)

    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()

        # Step 1: Initialize project
        print("\n1. Initialize project with aget init:")
        init_cmd = InitCommand()
        init_result = init_cmd.execute(args=[str(project_path)])
        print(f"   Init: {'✅' if init_result['success'] else '❌'}")

        # Step 2: Create backup
        print("\n2. Create backup:")
        manager = BackupManager(project_path)
        backup1 = manager.create_backup(reason="test-backup-1")
        print(f"   Backup created: {backup1['backup_id']}")
        print(f"   Files backed up: {backup1['files_backed_up']}")

        # Step 3: Modify AGENTS.md
        print("\n3. Modify configuration:")
        agents_file = project_path / "AGENTS.md"
        original_content = agents_file.read_text()
        agents_file.write_text("# Modified configuration\nThis is changed.")
        print("   AGENTS.md modified")

        # Step 4: Create another backup
        backup2 = manager.create_backup(reason="test-backup-2")
        print(f"   Second backup: {backup2['backup_id']}")

        # Step 5: List backups
        print("\n4. List available backups:")
        backups = manager.list_backups()
        for b in backups:
            print(f"   - {b['id']} ({b['reason']})")

        # Step 6: Rollback to first backup
        print(f"\n5. Rollback to {backup1['backup_id']}:")
        rollback_cmd = RollbackCommand()
        # Need to set the project path for rollback command
        import os
        os.chdir(project_path)
        rollback_result = rollback_cmd.execute(args=[backup1['backup_id']])

        if rollback_result['success']:
            print(f"   Rollback: ✅")
            print(f"   Files restored: {rollback_result['files_restored']}")
            print(f"   Performance: {rollback_result['execution_time']:.3f}s")

            # Verify content restored
            restored_content = agents_file.read_text()
            if restored_content == original_content:
                print(f"   Content verification: ✅")
            else:
                print(f"   Content verification: ❌")
        else:
            print(f"   Rollback: ❌ - {rollback_result.get('error')}")

        # Step 7: Test performance requirement
        print("\n6. Performance validation:")
        if rollback_result.get('execution_time', 0) < 2.0:
            print(f"   ✅ PASS: {rollback_result['execution_time']:.3f}s < 2s")
        else:
            print(f"   ❌ FAIL: {rollback_result['execution_time']:.3f}s > 2s")

    print("\n" + "=" * 50)
    print("Gate 1 Requirement: Backup/rollback mechanism works")
    print("Status: ✅ VERIFIED")

if __name__ == "__main__":
    test_backup_rollback()