"""
Backup and Rollback System
Provides versioned backups for safe configuration changes.
Critical for RKB agent safety.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class BackupManager:
    """Manages configuration backups and rollbacks."""

    def __init__(self, project_path: Optional[Path] = None):
        """Initialize backup manager for project."""
        self.project_path = project_path or Path.cwd()
        self.backup_dir = self.project_path / ".aget" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.backup_dir / "metadata.json"

    def create_backup(self, reason: str = "manual") -> Dict[str, str]:
        """
        Create a backup of current configuration.

        Args:
            reason: Why backup was created (manual, pre-apply, etc.)

        Returns:
            Dict with backup_id and status
        """
        # Generate backup ID with timestamp and microseconds for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:21]
        backup_id = f"backup_{timestamp}"
        backup_path = self.backup_dir / backup_id

        # Files to backup
        files_to_backup = [
            "AGENTS.md",
            "CLAUDE.md",  # Even if symlink
            ".aget/version.json"
        ]

        # Create backup directory
        backup_path.mkdir(exist_ok=True)

        # Copy files
        backed_up = []
        for file_name in files_to_backup:
            source = self.project_path / file_name
            if source.exists():
                if source.is_file() or source.is_symlink():
                    dest = backup_path / file_name
                    dest.parent.mkdir(parents=True, exist_ok=True)

                    if source.is_symlink():
                        # Save symlink info
                        # Python 3.8 compatible way to read symlink
                        import os
                        link_info = {
                            "is_symlink": True,
                            "target": os.readlink(str(source))
                        }
                        (dest.parent / f"{dest.name}.link").write_text(
                            json.dumps(link_info)
                        )
                    else:
                        shutil.copy2(source, dest)
                    backed_up.append(file_name)

        # Save metadata
        metadata = {
            "backup_id": backup_id,
            "timestamp": timestamp,
            "reason": reason,
            "files": backed_up
        }

        # Update metadata index
        all_metadata = self._load_metadata()
        all_metadata[backup_id] = metadata
        self._save_metadata(all_metadata)

        return {
            "backup_id": backup_id,
            "status": "success",
            "files_backed_up": len(backed_up),
            "location": str(backup_path)
        }

    def list_backups(self) -> List[Dict]:
        """List all available backups."""
        metadata = self._load_metadata()
        backups = []

        for backup_id, info in metadata.items():
            backup_path = self.backup_dir / backup_id
            if backup_path.exists():
                backups.append({
                    "id": backup_id,
                    "timestamp": info.get("timestamp"),
                    "reason": info.get("reason"),
                    "files": info.get("files", [])
                })

        # Sort by timestamp descending (newest first)
        backups.sort(key=lambda x: x["timestamp"], reverse=True)
        return backups

    def rollback(self, backup_id: Optional[str] = None) -> Dict[str, str]:
        """
        Rollback to a specific backup or the most recent one.

        Args:
            backup_id: Specific backup to restore, or None for latest

        Returns:
            Dict with status and restored files
        """
        # Get backup to restore
        if backup_id is None:
            backups = self.list_backups()
            if not backups:
                return {
                    "status": "error",
                    "error": "No backups available"
                }
            backup_id = backups[0]["id"]

        backup_path = self.backup_dir / backup_id
        if not backup_path.exists():
            return {
                "status": "error",
                "error": f"Backup {backup_id} not found"
            }

        # Create pre-rollback backup
        pre_rollback = self.create_backup(reason="pre-rollback")

        # Restore files
        restored = []
        metadata = self._load_metadata()
        backup_info = metadata.get(backup_id, {})

        for file_name in backup_info.get("files", []):
            source = backup_path / file_name
            dest = self.project_path / file_name

            if source.exists():
                # Check for symlink info
                link_file = source.parent / f"{source.name}.link"
                if link_file.exists():
                    # Restore as symlink
                    link_info = json.loads(link_file.read_text())
                    if dest.exists():
                        dest.unlink()
                    dest.symlink_to(link_info["target"])
                else:
                    # Regular file
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
                restored.append(file_name)

        return {
            "status": "success",
            "backup_id": backup_id,
            "files_restored": len(restored),
            "pre_rollback_backup": pre_rollback["backup_id"],
            "message": f"Rolled back to {backup_id}"
        }

    def cleanup_old_backups(self, keep: int = 10) -> int:
        """
        Remove old backups, keeping the most recent N.

        Args:
            keep: Number of recent backups to keep

        Returns:
            Number of backups removed
        """
        backups = self.list_backups()

        if len(backups) <= keep:
            return 0

        to_remove = backups[keep:]
        removed = 0

        for backup in to_remove:
            backup_path = self.backup_dir / backup["id"]
            if backup_path.exists():
                shutil.rmtree(backup_path)
                removed += 1

        # Update metadata
        metadata = self._load_metadata()
        for backup in to_remove:
            metadata.pop(backup["id"], None)
        self._save_metadata(metadata)

        return removed

    def _load_metadata(self) -> Dict:
        """Load backup metadata."""
        if self.metadata_file.exists():
            return json.loads(self.metadata_file.read_text())
        return {}

    def _save_metadata(self, metadata: Dict) -> None:
        """Save backup metadata."""
        self.metadata_file.write_text(json.dumps(metadata, indent=2))