#!/usr/bin/env python3
"""Coding Standards Compliance Pattern

Checks code against coding standards (built-in + custom).
Implements precedence order: repo-specific > agent-level > built-in.

Part of template-developer-aget v2.7.0.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple


# Built-in standards knowledge
BUILT_IN_STANDARDS = {
    "python": {
        "name": "PEP-8",
        "max_line_length": 79,
        "common_violations": {
            "E501": "Line too long",
            "E722": "Bare except clause",
            "F841": "Unused variable",
            "E701": "Multiple statements on one line",
            "W293": "Blank line contains whitespace"
        }
    },
    "javascript": {
        "name": "ESLint recommended",
        "common_violations": {
            "no-unused-vars": "Unused variable",
            "no-console": "Console statement in production code",
            "eqeqeq": "Use === instead of =="
        }
    },
    "go": {
        "name": "gofmt + Effective Go",
        "common_violations": {
            "formatting": "Code not gofmt formatted",
            "error-handling": "Unhandled error return"
        }
    }
}


def determine_standards(repo_path: str, language: str, custom_standards_path: str = None) -> Tuple[Dict[str, Any], str]:
    """Determine which standards to apply based on precedence order.

    Precedence: repo-specific > agent-level > built-in

    Args:
        repo_path: Path to repository being analyzed
        language: Programming language
        custom_standards_path: Path to agent-level custom standards

    Returns:
        Tuple of (standards dict, source description)
    """
    # Priority 1: Repo-specific standards
    repo_standards_path = os.path.join(repo_path, ".coding-standards.md")
    if os.path.exists(repo_standards_path):
        with open(repo_standards_path) as f:
            content = f.read()
        return parse_custom_standards(content, language), f"Custom (repo-specific: {repo_standards_path})"

    # Priority 2: Agent-level custom standards
    if custom_standards_path and os.path.exists(custom_standards_path):
        with open(custom_standards_path) as f:
            content = f.read()
        return parse_custom_standards(content, language), f"Custom (agent-level: {custom_standards_path})"

    # Priority 3: Built-in standards
    if language in BUILT_IN_STANDARDS:
        return BUILT_IN_STANDARDS[language], f"{BUILT_IN_STANDARDS[language]['name']} (built-in)"

    # No standards found
    return {}, "No standards available"


def parse_custom_standards(content: str, language: str) -> Dict[str, Any]:
    """Parse custom standards from markdown file.

    Args:
        content: Markdown content
        language: Programming language

    Returns:
        Standards dictionary
    """
    standards = {
        "name": "Custom standards",
        "rules": []
    }

    # Extract max line length if specified
    line_length_match = re.search(r"[Mm]ax line length:\s*(\d+)", content)
    if line_length_match:
        standards["max_line_length"] = int(line_length_match.group(1))

    # Extract other rules (simplified parsing)
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("-") or line.startswith("*"):
            # Bullet point rule
            rule = line.lstrip("-*").strip()
            if rule:
                standards["rules"].append(rule)

    return standards


def check_file_against_standards(file_path: str, standards: Dict[str, Any], language: str) -> List[Dict[str, Any]]:
    """Check single file against standards.

    Args:
        file_path: Path to file
        standards: Standards dictionary
        language: Programming language

    Returns:
        List of violations
    """
    violations = []

    if not os.path.exists(file_path):
        return violations

    with open(file_path) as f:
        lines = f.readlines()

    # Check max line length
    max_line_length = standards.get("max_line_length", 79)
    for line_num, line in enumerate(lines, 1):
        # Remove newline for length check
        line_content = line.rstrip("\n")
        if len(line_content) > max_line_length:
            violations.append({
                "code": "E501",
                "severity": "error",
                "file": os.path.basename(file_path),
                "line": line_num,
                "message": f"Line too long ({len(line_content)} > {max_line_length} characters)",
                "fix_example": "Break line at appropriate point"
            })

    # Language-specific checks
    if language == "python":
        violations.extend(check_python_specific(file_path, lines))

    return violations


def check_python_specific(file_path: str, lines: List[str]) -> List[Dict[str, Any]]:
    """Python-specific standard checks.

    Args:
        file_path: Path to file
        lines: File lines

    Returns:
        List of violations
    """
    violations = []
    file_name = os.path.basename(file_path)

    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip()

        # E722: Bare except clause
        if re.match(r"^\s*except\s*:\s*$", line_content):
            violations.append({
                "code": "E722",
                "severity": "warning",
                "file": file_name,
                "line": line_num,
                "message": "Bare except clause",
                "fix_example": "Use 'except Exception as e:' instead of 'except:'"
            })

        # F841: Unused variable (simplified detection)
        # This would require more sophisticated analysis in production
        unused_match = re.match(r"^\s*(\w+)\s*=\s*.+", line_content)
        if unused_match and line_num < len(lines) - 1:
            var_name = unused_match.group(1)
            # Check if variable is used in next few lines (simplified)
            used = False
            for check_line in lines[line_num:min(line_num + 5, len(lines))]:
                if var_name in check_line and "=" not in check_line:
                    used = True
                    break

            if not used and var_name not in ["_", "self"]:
                # This is a simplification; real linting is more sophisticated
                pass  # Skip for now to avoid false positives

        # W293: Blank line contains whitespace
        if line_content == "" and line.rstrip() != line.rstrip("\n\r"):
            violations.append({
                "code": "W293",
                "severity": "info",
                "file": file_name,
                "line": line_num,
                "message": "Blank line contains whitespace",
                "fix_example": "Remove trailing whitespace"
            })

    return violations


def calculate_compliance_rating(violations: List[Dict[str, Any]], lines_checked: int) -> float:
    """Calculate compliance rating (0-10 scale).

    Args:
        violations: List of violations
        lines_checked: Total lines checked

    Returns:
        Compliance rating (0-10)
    """
    if lines_checked == 0:
        return 10.0

    # Violations per 1000 lines
    violation_density = (len(violations) / lines_checked) * 1000

    # Rating: 10 - (density / 10), capped at 0
    rating = max(0.0, 10.0 - (violation_density / 10.0))

    return round(rating, 1)


def analyze(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check coding standards compliance.

    Args:
        input_data: Analysis parameters
            - repo_path: Path to repository (or single file)
            - language: Programming language
            - standards: "auto" | standard name | custom path
            - custom_standards_path: Path to agent-level standards (optional)
            - severity_filter: "all" | "error" | "warning" (optional)

    Returns:
        dict: Analysis results
            - status: "success" | "error"
            - compliance_rating: float (0-10)
            - standards_applied: str
            - violations: list
            - violation_summary: dict
            - recommendations: list
    """
    # Extract parameters
    repo_path = input_data.get("repo_path", ".")
    language = input_data.get("language", "python")
    custom_standards_path = input_data.get("custom_standards_path")
    severity_filter = input_data.get("severity_filter", "all")

    # Determine which standards to apply
    standards, standards_source = determine_standards(repo_path, language, custom_standards_path)

    if not standards:
        return {
            "status": "error",
            "message": f"No standards found for language: {language}"
        }

    # Find files to check
    files_to_check = []
    if os.path.isfile(repo_path):
        # Single file
        files_to_check = [repo_path]
    else:
        # Directory - find all files of language
        extension_map = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "go": ".go"
        }
        ext = extension_map.get(language, ".py")

        for root, dirs, files in os.walk(repo_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ["node_modules", "vendor", ".git", "__pycache__", "venv"]]
            for file in files:
                if file.endswith(ext):
                    files_to_check.append(os.path.join(root, file))

    # Check each file
    all_violations = []
    total_lines = 0

    for file_path in files_to_check:
        violations = check_file_against_standards(file_path, standards, language)
        all_violations.extend(violations)

        # Count lines
        with open(file_path) as f:
            total_lines += sum(1 for _ in f)

    # Filter by severity if requested
    if severity_filter != "all":
        all_violations = [v for v in all_violations if v["severity"] == severity_filter]

    # Calculate compliance rating
    compliance_rating = calculate_compliance_rating(all_violations, total_lines)

    # Summarize violations
    violation_summary = {
        "error": sum(1 for v in all_violations if v["severity"] == "error"),
        "warning": sum(1 for v in all_violations if v["severity"] == "warning"),
        "info": sum(1 for v in all_violations if v["severity"] == "info"),
        "total": len(all_violations)
    }

    # Generate recommendations
    recommendations = generate_recommendations(all_violations)

    return {
        "status": "success",
        "compliance_rating": compliance_rating,
        "standards_applied": standards_source,
        "violations": all_violations[:20],  # Limit to first 20 for brevity
        "violation_summary": violation_summary,
        "recommendations": recommendations,
        "metadata": {
            "files_checked": len(files_to_check),
            "lines_checked": total_lines
        }
    }


def generate_recommendations(violations: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Generate recommendations based on violations.

    Args:
        violations: List of violations

    Returns:
        List of recommendations
    """
    recommendations = []

    # Group violations by code
    violation_counts = {}
    for v in violations:
        code = v.get("code", "unknown")
        violation_counts[code] = violation_counts.get(code, 0) + 1

    # Recommend fixes for most common violations
    for code, count in sorted(violation_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
        priority = "high" if count > 5 else "medium"
        recommendations.append({
            "priority": priority,
            "message": f"Fix {count} {code} violations",
            "action": f"Review and correct {code} issues across codebase"
        })

    return recommendations


if __name__ == "__main__":
    # Example usage
    result = analyze({
        "repo_path": ".",
        "language": "python",
        "standards": "auto"
    })

    print(f"Compliance Rating: {result['compliance_rating']}/10")
    print(f"Standards: {result['standards_applied']}")
    print(f"Violations: {result['violation_summary']['total']}")
