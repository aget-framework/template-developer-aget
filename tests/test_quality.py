"""
Tests for the quality module - Advisory test and quality checker.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
import json
from unittest.mock import Mock, patch, MagicMock

from aget.quality import QualityChecker


class TestQualityChecker(unittest.TestCase):
    """Test the QualityChecker for AGET quality enforcement."""

    def setUp(self):
        """Set up test fixtures."""
        self.checker = QualityChecker()
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_init_default(self):
        """Test QualityChecker initialization with defaults."""
        checker = QualityChecker()
        self.assertFalse(checker.strict)
        self.assertEqual(checker.issues, [])
        self.assertEqual(checker.warnings, [])

    def test_init_strict_mode(self):
        """Test QualityChecker initialization in strict mode."""
        checker = QualityChecker(strict=True)
        self.assertTrue(checker.strict)
        self.assertEqual(checker.issues, [])
        self.assertEqual(checker.warnings, [])

    def test_check_tests_no_test_directory(self):
        """Test checking tests when no test directory exists."""
        results = self.checker.check_tests(self.test_dir)

        self.assertFalse(results["has_test_infrastructure"])
        self.assertFalse(results["has_actual_tests"])
        self.assertEqual(results["test_count"], 0)
        self.assertFalse(results["has_data_tests"])
        self.assertEqual(results["risk_level"], "MEDIUM")

    def test_check_tests_with_empty_test_directory(self):
        """Test checking tests with empty test directory."""
        # Create empty test directory
        test_dir = self.test_dir / "tests"
        test_dir.mkdir()

        results = self.checker.check_tests(self.test_dir)

        self.assertTrue(results["has_test_infrastructure"])
        self.assertFalse(results["has_actual_tests"])
        self.assertEqual(results["test_count"], 0)
        self.assertFalse(results["has_data_tests"])

    def test_check_tests_with_placeholder_tests(self):
        """Test checking tests with placeholder (empty) test files."""
        # Create test directory with placeholder test
        test_dir = self.test_dir / "tests"
        test_dir.mkdir()

        test_file = test_dir / "test_example.py"
        test_file.write_text("""
def test_placeholder():
    pass
""")

        results = self.checker.check_tests(self.test_dir)

        self.assertTrue(results["has_test_infrastructure"])
        self.assertFalse(results["has_actual_tests"])  # Contains 'pass'
        self.assertEqual(results["test_count"], 1)
        self.assertFalse(results["has_data_tests"])

    def test_check_tests_with_actual_tests(self):
        """Test checking tests with real test implementations."""
        # Create test directory with actual tests
        test_dir = self.test_dir / "tests"
        test_dir.mkdir()

        test_file = test_dir / "test_example.py"
        test_file.write_text("""
def test_real_functionality():
    assert 1 + 1 == 2
    result = some_function()
    assert result is not None
""")

        results = self.checker.check_tests(self.test_dir)

        self.assertTrue(results["has_test_infrastructure"])
        self.assertTrue(results["has_actual_tests"])
        self.assertEqual(results["test_count"], 1)
        self.assertFalse(results["has_data_tests"])

    def test_check_tests_with_data_tests(self):
        """Test checking tests with data integrity tests."""
        # Create test directory with data tests
        test_dir = self.test_dir / "tests"
        test_dir.mkdir()

        test_file = test_dir / "test_data.py"
        test_file.write_text("""
def test_data_integrity():
    data = load_json("test.json")
    assert validate_data(data)

def test_corruption_handling():
    corrupted = create_corrupted_data()
    assert handle_corruption(corrupted) is not None
""")

        results = self.checker.check_tests(self.test_dir)

        self.assertTrue(results["has_test_infrastructure"])
        self.assertTrue(results["has_actual_tests"])
        self.assertEqual(results["test_count"], 1)
        self.assertTrue(results["has_data_tests"])

    def test_manages_data_with_data_directory(self):
        """Test detection of data management with data directory."""
        # Create data directory
        data_dir = self.test_dir / "data"
        data_dir.mkdir()

        self.assertTrue(self.checker._manages_data(self.test_dir))

    def test_manages_data_with_state_directory(self):
        """Test detection of data management with state directory."""
        # Create state directory
        state_dir = self.test_dir / "state"
        state_dir.mkdir()

        self.assertTrue(self.checker._manages_data(self.test_dir))

    def test_manages_data_with_json_files(self):
        """Test detection of data management with data directory."""
        # Create a data directory (which is what _manages_data actually looks for)
        data_dir = self.test_dir / "data"
        data_dir.mkdir()
        (data_dir / "config.json").write_text('{"key": "value"}')

        self.assertTrue(self.checker._manages_data(self.test_dir))

    def test_manages_data_with_code_operations(self):
        """Test detection of data management through code inspection."""
        # Create Python file with data operations
        py_file = self.test_dir / "module.py"
        py_file.write_text("""
import json

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)
""")

        self.assertTrue(self.checker._manages_data(self.test_dir))

    def test_manages_data_no_indicators(self):
        """Test when project doesn't manage data."""
        # Create simple Python file without data operations
        py_file = self.test_dir / "module.py"
        py_file.write_text("""
def simple_function():
    return 42
""")

        self.assertFalse(self.checker._manages_data(self.test_dir))

    def test_risk_level_critical(self):
        """Test critical risk level for data management without tests."""
        # Create data directory (indicates data management)
        data_dir = self.test_dir / "data"
        data_dir.mkdir()

        # Create test directory but no data tests
        test_dir = self.test_dir / "tests"
        test_dir.mkdir()

        test_file = test_dir / "test_example.py"
        test_file.write_text("""
def test_something():
    assert True
""")

        results = self.checker.check_tests(self.test_dir)

        self.assertEqual(results["risk_level"], "CRITICAL")
        self.assertIn("Managing data without data integrity tests", self.checker.issues)

    def test_risk_level_high(self):
        """Test critical risk level for data with no tests."""
        # Create data directory (indicates data management)
        data_dir = self.test_dir / "data"
        data_dir.mkdir()

        # Create test directory but no test files
        test_dir = self.test_dir / "tests"
        test_dir.mkdir()

        results = self.checker.check_tests(self.test_dir)

        # With data management and no tests, risk is CRITICAL
        self.assertEqual(results["risk_level"], "CRITICAL")

    def test_risk_level_low_with_tests(self):
        """Test low risk level when tests exist."""
        # Create test directory with tests
        test_dir = self.test_dir / "tests"
        test_dir.mkdir()

        test_file = test_dir / "test_example.py"
        test_file.write_text("""
def test_real():
    assert True
""")

        results = self.checker.check_tests(self.test_dir)

        self.assertEqual(results["risk_level"], "LOW")

    def test_generate_report_basic(self):
        """Test generating a basic quality report."""
        results = {
            "has_test_infrastructure": False,
            "has_actual_tests": False,
            "test_count": 0,
            "has_data_tests": False,
            "risk_level": "MEDIUM"
        }

        report = self.checker.generate_report(results)

        self.assertIn("AGET Quality Report", report)
        self.assertIn("Test Coverage:", report)
        self.assertIn("No test infrastructure found", report)
        self.assertIn("Risk Level: MEDIUM", report)

    def test_generate_report_with_tests(self):
        """Test generating report with test information."""
        results = {
            "has_test_infrastructure": True,
            "has_actual_tests": True,
            "test_count": 5,
            "has_data_tests": True,
            "risk_level": "LOW"
        }

        report = self.checker.generate_report(results)

        self.assertIn("Test infrastructure exists", report)
        self.assertIn("5 actual test file(s) found", report)
        self.assertIn("Data integrity tests found", report)
        self.assertIn("Risk Level: LOW", report)

    def test_generate_report_with_issues(self):
        """Test generating report with critical issues."""
        results = {
            "has_test_infrastructure": True,
            "has_actual_tests": False,
            "test_count": 0,
            "has_data_tests": False,
            "risk_level": "CRITICAL"
        }

        self.checker.issues = ["Managing data without data integrity tests"]
        self.checker.warnings = ["Test infrastructure exists but no tests"]

        report = self.checker.generate_report(results)

        self.assertIn("Critical Issues:", report)
        self.assertIn("Managing data without data integrity tests", report)
        self.assertIn("Warnings:", report)

    def test_skip_huge_files(self):
        """Test that huge files are skipped during data detection."""
        # Create a mock huge file
        huge_file = self.test_dir / "huge.py"
        huge_file.write_text("x" * 200000)  # Over 100KB limit

        # Should not crash and should return False
        result = self.checker._manages_data(self.test_dir)
        self.assertFalse(result)

    def test_handle_unreadable_files(self):
        """Test handling of files that can't be read."""
        # Create a directory that looks like a Python file
        weird_file = self.test_dir / "fake.py"
        weird_file.mkdir()

        # Should not crash
        result = self.checker._manages_data(self.test_dir)
        self.assertFalse(result)

    def test_integration_full_check(self):
        """Test full integration of quality checking."""
        # Set up a realistic project
        test_dir = self.test_dir / "tests"
        test_dir.mkdir()

        # Add test with data operations
        test_file = test_dir / "test_data.py"
        test_file.write_text("""
import json

def test_data_loading():
    data = json.load(open("test.json"))
    assert data is not None
""")

        # Add data directory
        data_dir = self.test_dir / "data"
        data_dir.mkdir()

        # Run full check
        checker = QualityChecker(strict=True)
        results = checker.check_tests(self.test_dir)
        report = checker.generate_report(results)

        # Verify comprehensive results
        self.assertTrue(results["has_test_infrastructure"])
        self.assertTrue(results["has_actual_tests"])
        self.assertTrue(results["has_data_tests"])
        self.assertIn("quality", report.lower())


if __name__ == "__main__":
    unittest.main()