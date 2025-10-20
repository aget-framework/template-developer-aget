"""
Capability Detection Module
Detects available tools for three-tier degradation pattern.
"""

import shutil
import subprocess
from functools import lru_cache
from typing import Dict, Optional


class Capabilities:
    """Detects and caches system capabilities."""

    @staticmethod
    @lru_cache(maxsize=None)
    def detect_all() -> Dict[str, bool]:
        """Detect all available capabilities."""
        return {
            'gh': Capabilities.has_gh(),
            'git': Capabilities.has_git(),
            'make': Capabilities.has_make(),
            'python': Capabilities.has_python(),
            'python_version': Capabilities.get_python_version()
        }

    @staticmethod
    @lru_cache(maxsize=None)
    def has_gh() -> bool:
        """Check if GitHub CLI is available."""
        return shutil.which('gh') is not None

    @staticmethod
    @lru_cache(maxsize=None)
    def has_git() -> bool:
        """Check if git is available."""
        return shutil.which('git') is not None

    @staticmethod
    @lru_cache(maxsize=None)
    def has_make() -> bool:
        """Check if make is available."""
        return shutil.which('make') is not None

    @staticmethod
    @lru_cache(maxsize=None)
    def has_python() -> bool:
        """Check if Python 3.8+ is available."""
        try:
            result = subprocess.run(
                ['python3', '--version'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                major, minor = version.split('.')[:2]
                return int(major) >= 3 and int(minor) >= 8
        except Exception:
            pass
        return False

    @staticmethod
    @lru_cache(maxsize=None)
    def get_python_version() -> Optional[str]:
        """Get Python version string."""
        try:
            result = subprocess.run(
                ['python3', '--version'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                return result.stdout.strip().split()[-1]
        except Exception:
            pass
        return None

    @staticmethod
    def has_capability(name: str) -> bool:
        """Check if a specific capability exists."""
        caps = Capabilities.detect_all()
        return caps.get(name, False)