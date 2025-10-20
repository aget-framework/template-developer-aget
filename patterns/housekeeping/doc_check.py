#!/usr/bin/env python3
"""
Documentation Check Pattern - Assess documentation quality and completeness.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple


class DocumentationChecker:
    """Check documentation quality and completeness."""

    def __init__(self, project_path: Path = Path.cwd()):
        """Initialize documentation checker."""
        self.project_path = Path(project_path)
        self.required_docs = {
            'README': ['README.md', 'README.rst', 'README.txt', 'README'],
            'LICENSE': ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'COPYING'],
            'CONTRIBUTING': ['CONTRIBUTING.md', 'CONTRIBUTING.rst'],
            'CHANGELOG': ['CHANGELOG.md', 'CHANGELOG.rst', 'HISTORY.md', 'NEWS.md']
        }
        self.quality_indicators = {
            'installation': ['install', 'setup', 'getting started', 'quick start'],
            'usage': ['usage', 'how to', 'example', 'tutorial'],
            'api': ['api', 'reference', 'methods', 'functions'],
            'contributing': ['contribute', 'development', 'pull request'],
            'testing': ['test', 'testing', 'pytest', 'unittest']
        }

    def execute(self) -> Dict[str, Any]:
        """
        Execute documentation check.

        Returns:
            Documentation assessment with grade and recommendations
        """
        result = {
            'grade': 'F',
            'score': 0,
            'max_score': 100,
            'found_docs': {},
            'missing_docs': [],
            'quality_issues': [],
            'recommendations': []
        }

        print("📚 Documentation Check")
        print("-" * 40)

        # Check for required documentation files
        docs_score = self._check_required_docs(result)

        # Check README quality if it exists
        readme_score = self._check_readme_quality(result)

        # Check for additional documentation
        extra_score = self._check_extra_docs(result)

        # Check code documentation
        code_score = self._check_code_documentation(result)

        # Calculate total score
        result['score'] = docs_score + readme_score + extra_score + code_score
        result['grade'] = self._calculate_grade(result['score'])

        # Generate recommendations
        self._generate_recommendations(result)

        # Report results
        self._report_results(result)

        return result

    def _check_required_docs(self, result: Dict[str, Any]) -> int:
        """Check for required documentation files."""
        score = 0
        max_points = {
            'README': 20,
            'LICENSE': 10,
            'CONTRIBUTING': 5,
            'CHANGELOG': 5
        }

        for doc_type, patterns in self.required_docs.items():
            found = False
            for pattern in patterns:
                doc_path = self.project_path / pattern
                if doc_path.exists():
                    result['found_docs'][doc_type] = str(doc_path.name)
                    score += max_points.get(doc_type, 0)
                    found = True
                    break

            if not found:
                result['missing_docs'].append(doc_type)

        return score

    def _check_readme_quality(self, result: Dict[str, Any]) -> int:
        """Check README quality and completeness."""
        if 'README' not in result['found_docs']:
            return 0

        readme_path = self.project_path / result['found_docs']['README']
        try:
            content = readme_path.read_text().lower()
        except (IOError, UnicodeDecodeError):
            return 0

        score = 0
        missing_sections = []

        # Check for important sections (5 points each)
        for section, keywords in self.quality_indicators.items():
            section_found = any(keyword in content for keyword in keywords)
            if section_found:
                score += 5
            else:
                missing_sections.append(section)

        if missing_sections:
            result['quality_issues'].append(
                f"README missing sections: {', '.join(missing_sections)}"
            )

        # Check README length
        lines = content.split('\n')
        if len(lines) < 10:
            result['quality_issues'].append("README is too short (< 10 lines)")
        elif len(lines) > 20:
            score += 5  # Bonus for substantial README

        # Check for code examples
        if '```' in content or '    ' in content:
            score += 5  # Has code examples

        return min(score, 30)  # Cap at 30 points

    def _check_extra_docs(self, result: Dict[str, Any]) -> int:
        """Check for additional documentation."""
        score = 0

        # Check for docs directory
        docs_dirs = ['docs', 'documentation', 'doc']
        for dir_name in docs_dirs:
            docs_path = self.project_path / dir_name
            if docs_path.exists() and docs_path.is_dir():
                # Count documentation files
                doc_files = list(docs_path.glob('*.md')) + list(docs_path.glob('*.rst'))
                if doc_files:
                    score += 10
                    result['found_docs']['docs_directory'] = dir_name
                    result['found_docs']['doc_files_count'] = len(doc_files)
                break

        # Check for API documentation
        if (self.project_path / 'API.md').exists():
            score += 5
            result['found_docs']['API'] = 'API.md'

        # Check for examples directory
        if (self.project_path / 'examples').exists():
            score += 5
            result['found_docs']['examples'] = 'examples/'

        return score

    def _check_code_documentation(self, result: Dict[str, Any]) -> int:
        """Check code documentation (docstrings, comments)."""
        score = 0
        py_files = list(self.project_path.glob('**/*.py'))

        if not py_files:
            return 0  # Not a Python project

        documented_files = 0
        total_files = 0

        for py_file in py_files[:20]:  # Sample first 20 files
            # Skip test files and __pycache__
            if '__pycache__' in str(py_file) or 'test' in py_file.name:
                continue

            total_files += 1
            try:
                content = py_file.read_text()
                # Check for docstrings
                if '"""' in content or "'''" in content:
                    documented_files += 1
            except (IOError, UnicodeDecodeError):
                pass

        if total_files > 0:
            doc_ratio = documented_files / total_files
            if doc_ratio > 0.8:
                score += 10
                result['found_docs']['code_documentation'] = f"{int(doc_ratio * 100)}%"
            elif doc_ratio > 0.5:
                score += 5
                result['found_docs']['code_documentation'] = f"{int(doc_ratio * 100)}%"
            else:
                result['quality_issues'].append(
                    f"Low code documentation ({int(doc_ratio * 100)}% of files have docstrings)"
                )

        return score

    def _calculate_grade(self, score: int) -> str:
        """Calculate letter grade from score."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    def _generate_recommendations(self, result: Dict[str, Any]):
        """Generate improvement recommendations."""
        # Missing critical files
        if 'README' in result['missing_docs']:
            result['recommendations'].append("📝 Create a README.md file")
        if 'LICENSE' in result['missing_docs']:
            result['recommendations'].append("⚖️ Add a LICENSE file")

        # README improvements
        if result['quality_issues']:
            for issue in result['quality_issues']:
                if 'missing sections' in issue:
                    result['recommendations'].append(
                        "📚 Add missing README sections (installation, usage, examples)"
                    )
                if 'too short' in issue:
                    result['recommendations'].append(
                        "✍️ Expand README with more details"
                    )

        # Advanced documentation
        if 'docs_directory' not in result['found_docs'] and result['grade'] != 'A':
            result['recommendations'].append("📁 Create a docs/ directory for detailed documentation")

        if 'examples' not in result['found_docs']:
            result['recommendations'].append("💡 Add an examples/ directory with usage examples")

    def _report_results(self, result: Dict[str, Any]):
        """Report documentation check results."""
        # Grade with color
        grade_colors = {
            'A': '\033[92m',  # Green
            'B': '\033[92m',  # Green
            'C': '\033[93m',  # Yellow
            'D': '\033[93m',  # Yellow
            'F': '\033[91m'   # Red
        }
        color = grade_colors.get(result['grade'], '\033[0m')
        reset = '\033[0m'

        print(f"\n{color}Grade: {result['grade']} ({result['score']}/100){reset}")

        # Found documentation
        if result['found_docs']:
            print("\n✅ Found Documentation:")
            for doc_type, doc_name in result['found_docs'].items():
                print(f"  - {doc_type}: {doc_name}")

        # Missing documentation
        if result['missing_docs']:
            print("\n❌ Missing Documentation:")
            for doc in result['missing_docs']:
                print(f"  - {doc}")

        # Quality issues
        if result['quality_issues']:
            print("\n⚠️ Quality Issues:")
            for issue in result['quality_issues']:
                print(f"  - {issue}")

        # Recommendations
        if result['recommendations']:
            print("\n💡 Recommendations:")
            for rec in result['recommendations']:
                print(f"  {rec}")


def apply_pattern(project_path: Path = Path.cwd()) -> Dict[str, Any]:
    """
    Apply documentation check pattern to project.

    This is called by `aget apply housekeeping/doc_check`.
    """
    checker = DocumentationChecker(project_path)
    return checker.execute()


if __name__ == "__main__":
    apply_pattern()