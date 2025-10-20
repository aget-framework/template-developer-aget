# Release Hygiene Protocol

**Created**: 2025-09-28
**Purpose**: Ensure releases are clean, professional, and artifact-free
**Lesson From**: v2.1.0 near-miss with 51 items in root directory

## The Problem We Almost Released

```
v2.1.0-dev initial state:
- 9 .moved files (migration artifacts)
- 2 backup files (.original, .backup)
- 21 __pycache__ directories
- 106 .pyc files
- 4 test files in root directory
- Duplicate migration scripts
- Session artifacts in template
- Total: 51 items in root (should be ~20)
```

## Release Hygiene Checklist

### 1. Root Directory Cleanliness
```bash
# Should have <25 items in root
ls -1 | wc -l

# Check for misplaced files
ls -1 *.py  # Test files? Should be in tests/
ls -1 *.sh  # Scripts? Should be in scripts/
```

### 2. Remove Development Artifacts
```bash
# Migration artifacts
find . -name "*.moved" -delete
find . -name "*.backup" -delete
find . -name "*.original" -delete
find . -name "*.old" -delete

# Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
rm -rf .pytest_cache/

# Editor artifacts
find . -name "*.swp" -delete
find . -name "*.swo" -delete
find . -name "*~" -delete
find . -name ".DS_Store" -delete

# Session artifacts (templates shouldn't have these)
rm -f .session_state.json
rm -f .session_state.backup
rm -rf SESSION_NOTES/
rm -rf sessions/
rm -rf workspace/
rm -rf products/
```

### 3. Check for Duplicates
```bash
# Find duplicate Python files
find . -name "*.py" -exec basename {} \; | sort | uniq -d

# Check for migration scripts in multiple locations
ls -la scripts/*migration* scripts/migrations/*
```

### 4. Verify File Organization
```bash
# Test files should be in tests/
[ -z "$(ls test_*.py 2>/dev/null)" ] && echo "✓ No test files in root"

# Scripts should be in scripts/
[ -z "$(ls *.sh 2>/dev/null | grep -v install.sh | grep -v aget.sh)" ] && echo "✓ Scripts organized"

# Documentation should be in docs/ (except README, LICENSE, etc.)
ls -1 *.md | grep -v "README\|LICENSE\|CHANGELOG\|CONTRIBUTING\|SECURITY\|AGENTS\|CLAUDE"
```

### 5. Verify Essential Files
```bash
for file in README.md LICENSE CHANGELOG.md .gitignore; do
  [ -f "$file" ] && echo "✓ $file" || echo "✗ Missing: $file"
done
```

### 6. Check .gitignore Coverage
```bash
# Ensure .gitignore includes:
grep -q "__pycache__" .gitignore || echo "Add __pycache__ to .gitignore"
grep -q "*.pyc" .gitignore || echo "Add *.pyc to .gitignore"
grep -q "*.moved" .gitignore || echo "Add *.moved to .gitignore"
grep -q ".session_state" .gitignore || echo "Add .session_state* to .gitignore"
```

## Automated Hygiene Script

Create `scripts/aget_release_hygiene.py`:

```python
#!/usr/bin/env python3
"""
Release Hygiene Checker for AGET Templates
Ensures the template is clean and ready for release
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

class HygieneChecker:
    def __init__(self, root_path: Path = Path.current()):
        self.root = root_path
        self.issues = []
        self.warnings = []

    def check_root_cleanliness(self) -> bool:
        """Check if root directory is clean"""
        root_items = list(self.root.glob("*"))

        # Check total count
        if len(root_items) > 25:
            self.warnings.append(f"Root has {len(root_items)} items (should be <25)")

        # Check for test files in root
        test_files = list(self.root.glob("test_*.py"))
        if test_files:
            self.issues.append(f"Test files in root: {', '.join(f.name for f in test_files)}")

        # Check for misplaced scripts
        scripts = [f for f in self.root.glob("*.sh")
                  if f.name not in ["install.sh", "aget.sh"]]
        if scripts:
            self.issues.append(f"Scripts in root: {', '.join(f.name for f in scripts)}")

        return len(self.issues) == 0

    def check_artifacts(self) -> bool:
        """Check for development artifacts"""
        artifacts = {
            "Migration artifacts": ["*.moved", "*.backup", "*.original", "*.old"],
            "Python cache": ["__pycache__", "*.pyc", "*.pyo", ".pytest_cache"],
            "Editor files": ["*.swp", "*.swo", "*~", ".DS_Store"],
            "Session data": [".session_state.json", ".session_state.backup",
                           "SESSION_NOTES", "sessions", "workspace", "products"]
        }

        for category, patterns in artifacts.items():
            found = []
            for pattern in patterns:
                if "*" in pattern:
                    found.extend(self.root.rglob(pattern))
                else:
                    path = self.root / pattern
                    if path.exists():
                        found.append(path)

            if found:
                self.issues.append(f"{category}: {len(found)} items found")

        return len(self.issues) == 0

    def check_duplicates(self) -> bool:
        """Check for duplicate files"""
        py_files = {}
        for f in self.root.rglob("*.py"):
            name = f.name
            if name in py_files:
                self.warnings.append(f"Duplicate: {name} in {f.parent} and {py_files[name]}")
            else:
                py_files[name] = f.parent

        return len(self.warnings) == 0

    def check_essential_files(self) -> bool:
        """Verify essential files exist"""
        essential = [
            "README.md", "LICENSE", "CHANGELOG.md",
            ".gitignore", "requirements.txt"
        ]

        for file in essential:
            if not (self.root / file).exists():
                self.issues.append(f"Missing essential file: {file}")

        return len(self.issues) == 0

    def check_gitignore(self) -> bool:
        """Verify .gitignore has proper entries"""
        gitignore_path = self.root / ".gitignore"
        if not gitignore_path.exists():
            self.issues.append("No .gitignore file")
            return False

        content = gitignore_path.read_text()
        required = [
            "__pycache__", "*.pyc", "*.pyo",
            ".pytest_cache", ".session_state",
            "*.moved", "*.backup", "*.original"
        ]

        missing = [r for r in required if r not in content]
        if missing:
            self.warnings.append(f".gitignore missing: {', '.join(missing)}")

        return len(missing) == 0

    def run_all_checks(self) -> Tuple[bool, List[str], List[str]]:
        """Run all hygiene checks"""
        self.issues = []
        self.warnings = []

        checks = [
            ("Root cleanliness", self.check_root_cleanliness),
            ("Development artifacts", self.check_artifacts),
            ("Duplicate files", self.check_duplicates),
            ("Essential files", self.check_essential_files),
            (".gitignore coverage", self.check_gitignore)
        ]

        results = []
        for name, check in checks:
            try:
                passed = check()
                results.append((name, passed))
            except Exception as e:
                self.issues.append(f"{name} check failed: {e}")
                results.append((name, False))

        all_passed = all(passed for _, passed in results)
        return all_passed, self.issues, self.warnings

    def auto_clean(self, dry_run: bool = True) -> List[str]:
        """Automatically clean fixable issues"""
        actions = []

        # Clean Python cache
        for cache in self.root.rglob("__pycache__"):
            action = f"Remove {cache}"
            actions.append(action)
            if not dry_run:
                shutil.rmtree(cache)

        for pyc in self.root.rglob("*.pyc"):
            action = f"Remove {pyc}"
            actions.append(action)
            if not dry_run:
                pyc.unlink()

        # Clean artifacts
        for pattern in ["*.moved", "*.backup", "*.original", "*.old"]:
            for file in self.root.rglob(pattern):
                action = f"Remove {file}"
                actions.append(action)
                if not dry_run:
                    file.unlink()

        # Move test files
        test_files = list(self.root.glob("test_*.py"))
        if test_files and (self.root / "tests").exists():
            for test_file in test_files:
                action = f"Move {test_file.name} to tests/"
                actions.append(action)
                if not dry_run:
                    test_file.rename(self.root / "tests" / test_file.name)

        return actions

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Check release hygiene")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues")
    parser.add_argument("--ci", action="store_true", help="CI mode (exit 1 on issues)")
    args = parser.parse_args()

    checker = HygieneChecker()

    print("=" * 50)
    print("AGET Release Hygiene Check")
    print("=" * 50)

    # Run checks
    passed, issues, warnings = checker.run_all_checks()

    # Report results
    if issues:
        print("\n❌ Issues Found:")
        for issue in issues:
            print(f"  - {issue}")

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if args.fix:
        print("\n🔧 Auto-fixing issues...")
        actions = checker.auto_clean(dry_run=False)
        for action in actions:
            print(f"  - {action}")

    if passed and not warnings:
        print("\n✅ All hygiene checks passed!")
        return 0
    else:
        print(f"\n📊 Hygiene Score: {70 if not issues else 40}%")
        if args.ci:
            return 1
        return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Integration with Pre-Release

Add to `scripts/aget_pre_release.sh`:

```bash
echo "10. Checking release hygiene..."
if python3 scripts/aget_release_hygiene.py --ci; then
    echo "✅ Release hygiene passed"
else
    echo "❌ Release hygiene failed"
    echo "   Run: python3 scripts/aget_release_hygiene.py --fix"
    ((errors++))
fi
```

## Lessons Learned

1. **Functional ≠ Clean**: Code can work perfectly but still be messy
2. **Templates Accumulate Cruft**: Development naturally creates artifacts
3. **Visual Inspection Matters**: Human review catches what automation misses
4. **Hygiene is Part of Quality**: A clean release is a professional release

## When to Run

1. **Before Every Release**: Part of release checklist
2. **After Major Refactoring**: Ensure no artifacts left
3. **Weekly During Development**: Prevent accumulation
4. **In CI/CD Pipeline**: Automated check on PR

## Prevention Better Than Cure

### Development Practices
- Run `git clean -fdx` periodically (careful!)
- Use virtual environments for Python
- Configure .gitignore properly from start
- Don't commit cache files

### Release Process
```
Develop → Test → Battle-test → HYGIENE CHECK → Release
                                      ↑
                                 (Don't skip!)
```

---
*"A clean template is a happy template"*