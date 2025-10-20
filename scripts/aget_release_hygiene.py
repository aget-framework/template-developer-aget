#!/usr/bin/env python3
"""
Release Hygiene Checker for AGET Templates
Ensures the template is clean and ready for release

Usage:
    python3 scripts/aget_release_hygiene.py        # Check only
    python3 scripts/aget_release_hygiene.py --fix  # Auto-fix issues
    python3 scripts/aget_release_hygiene.py --ci   # CI mode (exit 1 on issues)
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Tuple, Set

class HygieneChecker:
    """Checks and fixes release hygiene issues"""

    def __init__(self, root_path: Path = None):
        self.root = root_path or Path.cwd()
        self.issues = []
        self.warnings = []
        self.fixed = []

    def check_root_cleanliness(self) -> bool:
        """Check if root directory is clean and organized"""
        root_items = list(self.root.glob("*"))
        visible_items = [f for f in root_items if not f.name.startswith(".")]

        # Check total count
        if len(visible_items) > 25:
            self.warnings.append(
                f"Root has {len(visible_items)} visible items (recommended <25)"
            )

        # Check for test files in root
        test_files = list(self.root.glob("test_*.py"))
        if test_files:
            self.issues.append(
                f"Test files in root: {', '.join(f.name for f in test_files)}"
            )

        # Check for misplaced scripts
        scripts = [
            f for f in self.root.glob("*.sh")
            if f.name not in ["install.sh", "aget.sh"]
        ]
        if scripts:
            self.warnings.append(
                f"Consider moving scripts to scripts/: {', '.join(f.name for f in scripts)}"
            )

        # Check for misplaced Python files
        py_files = [
            f for f in self.root.glob("*.py")
            if f.name not in ["setup.py"]
        ]
        if py_files:
            self.issues.append(
                f"Python files in root: {', '.join(f.name for f in py_files)}"
            )

        return len(self.issues) == 0

    def check_artifacts(self) -> bool:
        """Check for development artifacts that shouldn't be in release"""
        found_artifacts = False

        # Migration artifacts
        for pattern in ["*.moved", "*.backup", "*.original", "*.old"]:
            artifacts = list(self.root.rglob(pattern))
            if artifacts:
                self.issues.append(
                    f"Migration artifacts ({pattern}): {len(artifacts)} files"
                )
                found_artifacts = True

        # Python cache
        pycache = list(self.root.rglob("__pycache__"))
        if pycache:
            self.issues.append(f"Python cache: {len(pycache)} __pycache__ directories")
            found_artifacts = True

        pyc_files = list(self.root.rglob("*.pyc"))
        if pyc_files:
            self.issues.append(f"Compiled Python: {len(pyc_files)} .pyc files")
            found_artifacts = True

        pytest_cache = self.root / ".pytest_cache"
        if pytest_cache.exists():
            self.issues.append("Pytest cache: .pytest_cache directory exists")
            found_artifacts = True

        # Editor artifacts
        for pattern in ["*.swp", "*.swo", "*~", ".DS_Store"]:
            editor_files = list(self.root.rglob(pattern))
            if editor_files:
                self.warnings.append(
                    f"Editor artifacts ({pattern}): {len(editor_files)} files"
                )

        # Session artifacts (templates shouldn't have these)
        session_artifacts = [
            ".session_state.json",
            ".session_state.backup",
            "SESSION_NOTES",
            "sessions",
            "workspace",
            "products"
        ]
        for artifact in session_artifacts:
            path = self.root / artifact
            if path.exists():
                self.issues.append(f"Session artifact: {artifact}")
                found_artifacts = True

        return not found_artifacts

    def check_duplicates(self) -> bool:
        """Check for duplicate files"""
        py_files = {}
        has_duplicates = False

        for f in self.root.rglob("*.py"):
            if "__pycache__" in str(f):
                continue
            name = f.name
            if name in py_files:
                self.warnings.append(
                    f"Duplicate file: {name} in:\n"
                    f"  - {f.parent.relative_to(self.root)}\n"
                    f"  - {py_files[name].relative_to(self.root)}"
                )
                has_duplicates = True
            else:
                py_files[name] = f.parent

        return not has_duplicates

    def check_essential_files(self) -> bool:
        """Verify essential files exist"""
        essential = {
            "README.md": "Main documentation",
            "LICENSE": "License information",
            "CHANGELOG.md": "Version history",
            ".gitignore": "Git ignore rules",
            "requirements.txt": "Python dependencies"
        }

        missing = []
        for file, description in essential.items():
            if not (self.root / file).exists():
                self.issues.append(f"Missing {description}: {file}")
                missing.append(file)

        return len(missing) == 0

    def check_gitignore(self) -> bool:
        """Verify .gitignore has proper entries"""
        gitignore_path = self.root / ".gitignore"
        if not gitignore_path.exists():
            self.issues.append("No .gitignore file")
            return False

        content = gitignore_path.read_text()
        required = {
            "__pycache__": "Python cache directories",
            "*.pyc": "Compiled Python files",
            ".pytest_cache": "Pytest cache",
            ".session_state": "Session state files",
            "*.moved": "Migration artifacts",
            "*.backup": "Backup files",
            "*.original": "Original file copies"
        }

        missing = []
        for pattern, description in required.items():
            if pattern not in content:
                missing.append(pattern)
                self.warnings.append(f".gitignore missing '{pattern}' ({description})")

        return len(missing) == 0

    def check_readme_privacy(self) -> bool:
        """Check README files for privacy violations"""
        privacy_issues = []

        # Patterns that suggest private information
        private_patterns = [
            r'my-[A-Z]+-aget',  # Private agent names
            r'/Users/[^/]+/',   # Personal file paths
            r'gabormelli',      # Specific username (except in LICENSE)
            r'my-.*-aget.*v2\.',  # Version info with private agents
        ]

        readme_files = list(self.root.rglob("README.md"))
        for readme in readme_files:
            if "LICENSE" in str(readme):
                continue

            content = readme.read_text()
            for pattern in private_patterns:
                import re
                if re.search(pattern, content, re.IGNORECASE):
                    if not (pattern == r'gabormelli' and 'LICENSE' in content):
                        privacy_issues.append(f"Privacy concern in {readme.name}: pattern '{pattern}'")

        if privacy_issues:
            self.warnings.extend(privacy_issues)

        return len(privacy_issues) == 0

    def check_empty_directories(self) -> bool:
        """Check for empty directories that might be unnecessary"""
        empty_dirs = []

        for root, dirs, files in os.walk(self.root):
            # Skip .git and __pycache__
            dirs[:] = [d for d in dirs if d not in [".git", "__pycache__"]]

            path = Path(root)
            if not dirs and not files and path != self.root:
                rel_path = path.relative_to(self.root)
                empty_dirs.append(str(rel_path))

        if empty_dirs:
            self.warnings.append(
                f"Empty directories: {', '.join(empty_dirs)}"
            )

        return len(empty_dirs) == 0

    def run_all_checks(self) -> Tuple[bool, int, int]:
        """Run all hygiene checks"""
        self.issues = []
        self.warnings = []

        checks = [
            ("Root cleanliness", self.check_root_cleanliness),
            ("Development artifacts", self.check_artifacts),
            ("Duplicate files", self.check_duplicates),
            ("Essential files", self.check_essential_files),
            (".gitignore coverage", self.check_gitignore),
            ("README privacy", self.check_readme_privacy),
            ("Empty directories", self.check_empty_directories)
        ]

        print("\nRunning hygiene checks...")
        print("-" * 40)

        all_passed = True
        for name, check in checks:
            try:
                passed = check()
                status = "✅" if passed else "❌"
                print(f"{status} {name}")
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"❌ {name} - Error: {e}")
                self.issues.append(f"{name} check failed: {e}")
                all_passed = False

        return all_passed, len(self.issues), len(self.warnings)

    def auto_clean(self, dry_run: bool = True) -> List[str]:
        """Automatically clean fixable issues"""
        actions = []

        print("\n🔧 Cleaning fixable issues...")
        print("-" * 40)

        # Clean Python cache
        for cache_dir in self.root.rglob("__pycache__"):
            action = f"Remove {cache_dir.relative_to(self.root)}"
            actions.append(action)
            if not dry_run:
                shutil.rmtree(cache_dir, ignore_errors=True)

        for pyc in self.root.rglob("*.pyc"):
            action = f"Remove {pyc.relative_to(self.root)}"
            actions.append(action)
            if not dry_run:
                pyc.unlink(missing_ok=True)

        # Remove pytest cache
        pytest_cache = self.root / ".pytest_cache"
        if pytest_cache.exists():
            action = "Remove .pytest_cache"
            actions.append(action)
            if not dry_run:
                shutil.rmtree(pytest_cache, ignore_errors=True)

        # Clean artifacts
        artifact_patterns = ["*.moved", "*.backup", "*.original", "*.old"]
        for pattern in artifact_patterns:
            for file in self.root.rglob(pattern):
                action = f"Remove {file.relative_to(self.root)}"
                actions.append(action)
                if not dry_run:
                    file.unlink(missing_ok=True)

        # Remove session artifacts
        session_items = [
            ".session_state.json",
            ".session_state.backup",
            "SESSION_NOTES",
            "sessions",
            "workspace",
            "products"
        ]
        for item in session_items:
            path = self.root / item
            if path.exists():
                action = f"Remove {item}"
                actions.append(action)
                if not dry_run:
                    if path.is_dir():
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        path.unlink(missing_ok=True)

        # Move test files to tests/
        tests_dir = self.root / "tests"
        if tests_dir.exists():
            for test_file in self.root.glob("test_*.py"):
                action = f"Move {test_file.name} to tests/"
                actions.append(action)
                if not dry_run:
                    test_file.rename(tests_dir / test_file.name)

        if dry_run:
            print(f"Would perform {len(actions)} cleaning actions (use --fix to apply)")
        else:
            print(f"Performed {len(actions)} cleaning actions")

        return actions

    def calculate_score(self) -> int:
        """Calculate hygiene score (0-100)"""
        if not self.issues and not self.warnings:
            return 100

        # Start at 100, deduct points
        score = 100
        score -= len(self.issues) * 10  # Issues are serious
        score -= len(self.warnings) * 3  # Warnings are minor

        return max(0, score)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Check and fix release hygiene for AGET templates"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix issues (removes artifacts)"
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode - exit with error if issues found"
    )
    args = parser.parse_args()

    print("=" * 50)
    print("🧹 AGET Release Hygiene Checker v1.0")
    print("=" * 50)

    checker = HygieneChecker()

    # Run checks
    passed, issue_count, warning_count = checker.run_all_checks()

    # Report results
    print("\n" + "=" * 50)
    print("📊 RESULTS")
    print("=" * 50)

    if checker.issues:
        print(f"\n❌ Issues Found ({issue_count}):")
        for issue in checker.issues:
            print(f"  • {issue}")

    if checker.warnings:
        print(f"\n⚠️  Warnings ({warning_count}):")
        for warning in checker.warnings:
            print(f"  • {warning}")

    # Auto-fix if requested
    if args.fix and checker.issues:
        actions = checker.auto_clean(dry_run=False)
        if actions:
            print("\n✅ Fixed:")
            for action in actions:
                print(f"  • {action}")

            # Re-run checks after fixing
            print("\n🔄 Re-checking after fixes...")
            passed, issue_count, warning_count = checker.run_all_checks()

    # Calculate and display score
    score = checker.calculate_score()
    print(f"\n📈 Hygiene Score: {score}/100")

    if score == 100:
        print("🎉 Perfect! Template is clean and ready for release.")
    elif score >= 90:
        print("✅ Good! Minor issues only.")
    elif score >= 70:
        print("⚠️  Acceptable, but should be improved.")
    else:
        print("❌ Poor hygiene. Significant cleanup needed.")

    # Exit code for CI
    if args.ci and not passed:
        print("\n❌ CI check failed - hygiene issues detected")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()