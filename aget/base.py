"""
Base Command with Three-Tier Degradation Pattern
Foundation for all AGET v2 commands per ADR-004.
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from aget.shared.capabilities import Capabilities


class BaseCommand(ABC):
    """
    Base class for all AGET commands implementing three-tier degradation.

    Every command MUST implement tier_basic for filesystem-only operation.
    Commands MAY implement tier_git and tier_gh for enhanced functionality.
    """

    def __init__(self):
        """Initialize command with capability detection."""
        self.capabilities = Capabilities.detect_all()
        self.start_time = None
        self.execution_time = None

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute command using appropriate tier.
        Implements three-tier degradation pattern from ADR-004.
        """
        self.start_time = time.time()

        try:
            # Try richest tier first
            if self.capabilities.get('gh') and hasattr(self, 'tier_gh'):
                result = self.tier_gh(**kwargs)
                result['tier_used'] = 'gh'
            # Fall back to git tier
            elif self.capabilities.get('git') and hasattr(self, 'tier_git'):
                result = self.tier_git(**kwargs)
                result['tier_used'] = 'git'
            # Always have basic tier
            else:
                result = self.tier_basic(**kwargs)
                result['tier_used'] = 'basic'

            # Add performance metrics
            self.execution_time = time.time() - self.start_time
            result['execution_time'] = self.execution_time

            # Validate <2 second requirement from Gate 1
            if self.execution_time > 2.0:
                result['warning'] = f"Command took {self.execution_time:.2f}s (>2s limit)"

            return result

        except Exception as e:
            self.execution_time = time.time() - self.start_time
            return {
                'success': False,
                'error': str(e),
                'tier_used': 'error',
                'execution_time': self.execution_time
            }

    @abstractmethod
    def tier_basic(self, **kwargs) -> Dict[str, Any]:
        """
        Basic tier implementation - MUST be implemented.
        Uses only filesystem operations, no external tools.
        This ensures command works everywhere (RKB safety).
        """
        pass

    def tier_git(self, **kwargs) -> Dict[str, Any]:
        """
        Git tier implementation - optional.
        Can use local git operations.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement git tier"
        )

    def tier_gh(self, **kwargs) -> Dict[str, Any]:
        """
        GitHub CLI tier implementation - optional.
        Can use gh commands for enhanced features.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement gh tier"
        )

    def validate_performance(self) -> bool:
        """Check if command meets <2 second performance requirement."""
        return self.execution_time is None or self.execution_time < 2.0

    @property
    def tier_available(self) -> str:
        """Report highest available tier for this command."""
        if self.capabilities.get('gh') and hasattr(self, 'tier_gh'):
            return 'gh'
        elif self.capabilities.get('git') and hasattr(self, 'tier_git'):
            return 'git'
        else:
            return 'basic'