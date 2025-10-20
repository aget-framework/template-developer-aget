"""
Quality Agent - Advisory test and quality checker for AGET
Future home of quality enforcement (post-v2.0)
"""

from pathlib import Path
from typing import Dict, List, Tuple
import json


class QualityChecker:
    """Advisory quality checker - will gain enforcement in v2.1"""

    def __init__(self, strict: bool = False):
        self.strict = strict
        self.issues = []
        self.warnings = []

    def check_tests(self, project_path: Path) -> Dict:
        """Check test coverage and quality"""
        results = {
            "has_test_infrastructure": False,
            "has_actual_tests": False,
            "test_count": 0,
            "has_data_tests": False,
            "risk_level": "UNKNOWN"
        }

        # Check for test infrastructure
        test_dirs = ["tests", "test"]
        for test_dir in test_dirs:
            if (project_path / test_dir).exists():
                results["has_test_infrastructure"] = True

                # Count actual test files
                test_files = list((project_path / test_dir).glob("test_*.py"))
                results["test_count"] = len(test_files)

                # Check if tests have content (not just placeholders)
                for test_file in test_files:
                    content = test_file.read_text()
                    if "def test_" in content and "pass" not in content:
                        results["has_actual_tests"] = True

                    # Check for data-specific tests
                    if any(term in content for term in ["data", "json", "corruption", "integrity"]):
                        results["has_data_tests"] = True

        # Assess risk level
        if self._manages_data(project_path):
            if not results["has_data_tests"]:
                results["risk_level"] = "CRITICAL"
                self.issues.append("Managing data without data integrity tests")
            elif results["test_count"] == 0:
                results["risk_level"] = "HIGH"
                self.warnings.append("Test infrastructure exists but no tests")
            else:
                results["risk_level"] = "LOW"
        else:
            results["risk_level"] = "MEDIUM" if results["test_count"] == 0 else "LOW"

        return results

    def _manages_data(self, project_path: Path) -> bool:
        """Check if project manages persistent data"""
        data_indicators = [
            "data",
            "state",
            "sessions",
            ".json",
            "capture",
            "journal"
        ]

        for indicator in data_indicators:
            if (project_path / indicator).exists():
                return True

            # Check in code for data operations
            for py_file in project_path.glob("**/*.py"):
                if py_file.stat().st_size < 100000:  # Skip huge files
                    try:
                        content = py_file.read_text()
                        if any(term in content for term in ["json.dump", "json.load", "write", "save"]):
                            return True
                    except:
                        pass

        return False

    def generate_report(self, results: Dict) -> str:
        """Generate human-readable quality report"""
        report = []
        report.append("=== AGET Quality Report ===\n")

        # Test Coverage Section
        report.append("Test Coverage:")
        if results["has_test_infrastructure"]:
            report.append(f"  ✓ Test infrastructure exists")
        else:
            report.append(f"  ✗ No test infrastructure found")

        if results["has_actual_tests"]:
            report.append(f"  ✓ {results['test_count']} actual test file(s) found")
        else:
            report.append(f"  ✗ No actual tests (possible test theater)")

        if results["has_data_tests"]:
            report.append(f"  ✓ Data integrity tests found")
        elif results["risk_level"] in ["CRITICAL", "HIGH"]:
            report.append(f"  ✗ No data integrity tests (RISKY)")

        # Risk Assessment
        report.append(f"\nRisk Level: {results['risk_level']}")

        # Issues and Warnings
        if self.issues:
            report.append("\nCritical Issues:")
            for issue in self.issues:
                report.append(f"  ⚠️  {issue}")

        if self.warnings:
            report.append("\nWarnings:")
            for warning in self.warnings:
                report.append(f"  ⚡ {warning}")

        # Recommendations
        if results["risk_level"] in ["CRITICAL", "HIGH"]:
            report.append("\nImmediate Action Required:")
            report.append("  1. Write at least one data integrity test")
            report.append("  2. Test that data operations don't corrupt state")
            report.append("  3. Run: aget quality explain why-tests-matter")

        # Enforcement note (future)
        if not self.strict:
            report.append("\nNote: Running in advisory mode (use --strict to enforce)")

        return "\n".join(report)

    def enforce(self, results: Dict) -> bool:
        """Return whether project passes quality standards"""
        if not self.strict:
            return True  # Advisory mode always passes

        # Strict mode requirements (v2.1+)
        if results["risk_level"] == "CRITICAL":
            return False

        if results["has_test_infrastructure"] and not results["has_actual_tests"]:
            return False  # Test theater not allowed

        return True


# Future: This will be called by `aget quality check`
def check_quality(project_path: Path = Path("."), strict: bool = False) -> int:
    """Main entry point for quality checking"""
    checker = QualityChecker(strict=strict)
    results = checker.check_tests(project_path)

    print(checker.generate_report(results))

    if strict and not checker.enforce(results):
        print("\n❌ Quality standards not met")
        return 1

    return 0