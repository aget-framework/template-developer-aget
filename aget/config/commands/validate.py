#!/usr/bin/env python3
"""
AGET Validate Command - Wrapped for v2 CLI architecture.
"""

import argparse
import time
from pathlib import Path
from typing import Dict, Any, List

from aget.base import BaseCommand
from src.aget.commands.validate import ProjectValidator


class ValidateCommand(BaseCommand):
    """
    Validate AGET configuration command.
    Wraps the standalone validator for integration with v2 CLI.
    """

    name = "validate"
    description = "Validate AGET configuration and patterns"

    def tier_basic(self, args: List[str] = None, **kwargs) -> Dict[str, Any]:
        """Basic tier validation using only filesystem operations."""
        start_time = time.time()

        # Parse arguments
        parser = argparse.ArgumentParser(
            prog='aget validate',
            description=self.description
        )
        parser.add_argument(
            'path',
            nargs='?',
            default='.',
            help='Path to project (default: current directory)'
        )
        parser.add_argument(
            '--strict',
            action='store_true',
            help='Treat warnings as errors'
        )
        parser.add_argument(
            '--quiet', '-q',
            action='store_true',
            help='Quiet mode - only show errors'
        )

        parsed_args = parser.parse_args(args or [])

        # Run validation
        project_path = Path(parsed_args.path)
        validator = ProjectValidator(project_path)
        is_valid = validator.validate_all()

        # Handle strict mode
        if parsed_args.strict and validator.warnings:
            is_valid = False

        # Generate report if not quiet
        if not parsed_args.quiet:
            print(validator.generate_report())

        execution_time = time.time() - start_time

        return {
            'success': is_valid,
            'checks_passed': validator.checks_passed,
            'checks_total': validator.checks_total,
            'errors': validator.errors,
            'warnings': validator.warnings,
            'execution_time': execution_time
        }

    def validate_args(self, args: List[str]) -> bool:
        """Validate arguments."""
        # Arguments are optional for validate
        return True

    # Validation doesn't need git or gh tiers, but we define them
    # to prevent BaseCommand from trying non-existent methods
    def tier_git(self, **kwargs) -> Dict[str, Any]:
        """Git tier - just delegates to basic tier."""
        return self.tier_basic(**kwargs)

    def tier_gh(self, **kwargs) -> Dict[str, Any]:
        """GitHub CLI tier - just delegates to basic tier."""
        return self.tier_basic(**kwargs)