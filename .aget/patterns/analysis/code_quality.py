#!/usr/bin/env python3
"""Code Quality Analysis Pattern

Assesses code quality across metrics: complexity, maintainability, technical debt, code smells.

Part of template-developer-aget v2.7.0.
"""

import os
import re
from typing import Dict, Any, List
from datetime import datetime


def calculate_cyclomatic_complexity(code: str) -> int:
    """Calculate cyclomatic complexity for code block.

    Simplified implementation counting decision points.

    Args:
        code: Code string

    Returns:
        Complexity score
    """
    # Count decision points (if, for, while, and, or, except, case)
    decision_keywords = [
        r'\bif\b', r'\bfor\b', r'\bwhile\b', r'\bexcept\b',
        r'\band\b', r'\bor\b', r'\bcase\b', r'\belif\b'
    ]

    complexity = 1  # Base complexity

    for keyword in decision_keywords:
        complexity += len(re.findall(keyword, code))

    return complexity


def analyze_function_complexity(file_path: str) -> List[Dict[str, Any]]:
    """Analyze complexity of functions in file.

    Args:
        file_path: Path to source file

    Returns:
        List of function complexity info
    """
    functions = []

    if not os.path.exists(file_path):
        return functions

    with open(file_path) as f:
        content = f.read()
        lines = content.split("\n")

    # Simple function detection (Python)
    current_function = None
    function_start = 0
    indent_level = 0

    for i, line in enumerate(lines):
        # Detect function definition
        func_match = re.match(r'^(\s*)def\s+(\w+)\s*\(', line)
        if func_match:
            # Save previous function if exists
            if current_function:
                func_code = "\n".join(lines[function_start:i])
                complexity = calculate_cyclomatic_complexity(func_code)
                functions.append({
                    "file": os.path.basename(file_path),
                    "function": current_function,
                    "complexity": complexity,
                    "lines": i - function_start
                })

            # Start new function
            indent_level = len(func_match.group(1))
            current_function = func_match.group(2)
            function_start = i

    # Save last function
    if current_function:
        func_code = "\n".join(lines[function_start:])
        complexity = calculate_cyclomatic_complexity(func_code)
        functions.append({
            "file": os.path.basename(file_path),
            "function": current_function,
            "complexity": complexity,
            "lines": len(lines) - function_start
        })

    return functions


def calculate_maintainability_index(complexity: float, loc: int) -> int:
    """Calculate maintainability index (0-100).

    Simplified formula based on complexity and lines of code.

    Args:
        complexity: Average cyclomatic complexity
        loc: Lines of code

    Returns:
        Maintainability index (0-100)
    """
    import math

    # Simplified MI formula
    # MI = max(0, 171 - 5.2*ln(V) - 0.23*G - 16.2*ln(LOC))
    # Simplified: MI = 100 - (complexity * 2) - (log(LOC) * 10)

    if loc == 0:
        return 100

    mi = 100 - (complexity * 2) - (math.log(max(1, loc)) * 10)
    mi = max(0, min(100, mi))  # Clamp to 0-100

    return int(mi)


def detect_technical_debt(file_content: str, file_path: str) -> List[Dict[str, Any]]:
    """Find TODO, FIXME, HACK comments.

    Args:
        file_content: File content string
        file_path: File path

    Returns:
        List of technical debt items
    """
    debt_items = []
    patterns = [r'TODO:', r'FIXME:', r'HACK:', r'XXX:']

    for line_num, line in enumerate(file_content.split("\n"), 1):
        for pattern in patterns:
            if pattern in line:
                debt_items.append({
                    "file": os.path.basename(file_path),
                    "line": line_num,
                    "type": pattern.strip(":"),
                    "text": line.strip()
                })

    return debt_items


def detect_code_smells(functions: List[Dict[str, Any]], files: List[str]) -> List[Dict[str, Any]]:
    """Detect common code smells.

    Args:
        functions: List of function complexity info
        files: List of file paths

    Returns:
        List of code smells
    """
    smells = []

    # Long methods (>50 lines)
    for func in functions:
        if func["lines"] > 50:
            smells.append({
                "type": "long_method",
                "file": func["file"],
                "function": func["function"],
                "lines": func["lines"]
            })

    # High complexity functions
    for func in functions:
        if func["complexity"] > 10:
            smells.append({
                "type": "high_complexity",
                "file": func["file"],
                "function": func["function"],
                "complexity": func["complexity"]
            })

    # Nested conditionals (detected via high complexity)
    for func in functions:
        if func["complexity"] > 15:
            smells.append({
                "type": "nested_conditionals",
                "file": func["file"],
                "function": func["function"],
                "depth": func["complexity"] - 10  # Estimated nesting depth
            })

    return smells


def calculate_overall_quality(metrics: Dict[str, Any]) -> float:
    """Calculate overall quality rating (0-10).

    Args:
        metrics: Quality metrics dict

    Returns:
        Overall quality score (0-10)
    """
    # Weighted average:
    # - Complexity: 30% (inverse: high complexity = low score)
    # - Maintainability: 40%
    # - Debt: 20% (inverse: high debt = low score)
    # - Smells: 10% (inverse: more smells = low score)

    avg_complexity = metrics["complexity"]["avg_cyclomatic"]
    complexity_score = max(0, 10 - (avg_complexity / 2))

    maintainability_index = metrics["maintainability"]["index"]
    maintainability_score = maintainability_index / 10

    debt_count = metrics["technical_debt"]["todo_count"] + metrics["technical_debt"]["fixme_count"]
    debt_score = max(0, 10 - debt_count)

    smell_count = len(metrics["code_smells"])
    smells_score = max(0, 10 - smell_count)

    overall = (
        complexity_score * 0.3 +
        maintainability_score * 0.4 +
        debt_score * 0.2 +
        smells_score * 0.1
    )

    return round(overall, 1)


def generate_recommendations(metrics: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate actionable recommendations.

    Args:
        metrics: Quality metrics

    Returns:
        List of recommendations
    """
    recommendations = []

    # High complexity functions
    high_complexity = metrics["complexity"].get("high_complexity_functions", [])
    if high_complexity:
        func = high_complexity[0]  # Most complex
        recommendations.append({
            "priority": "high",
            "category": "complexity",
            "message": f"Refactor {func['file']}::{func['function']}() (complexity: {func['complexity']})",
            "fix_strategy": "Extract nested logic into separate functions"
        })

    # Technical debt
    todo_count = metrics["technical_debt"]["todo_count"]
    fixme_count = metrics["technical_debt"]["fixme_count"]
    if todo_count + fixme_count > 0:
        recommendations.append({
            "priority": "medium",
            "category": "debt",
            "message": f"Address {todo_count + fixme_count} TODO/FIXME comments",
            "fix_strategy": "Review TODOs - resolve or delete if no longer relevant"
        })

    # Code smells
    smells = metrics["code_smells"]
    long_methods = [s for s in smells if s["type"] == "long_method"]
    if long_methods:
        smell = long_methods[0]
        recommendations.append({
            "priority": "medium",
            "category": "smells",
            "message": f"Refactor {smell['file']}::{smell['function']}() ({smell['lines']} lines)",
            "fix_strategy": "Break into smaller, focused methods"
        })

    return recommendations


def analyze(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze code quality metrics.

    Args:
        input_data: Analysis parameters
            - repo_path: Path to repository
            - language: Programming language (auto-detected if not provided)
            - metrics: List of metrics to analyze (optional)
            - threshold: Threshold values (optional)

    Returns:
        dict: Analysis results
            - status: "success" | "error"
            - overall_quality: float (0-10 rating)
            - metrics: dict (complexity, maintainability, debt, smells)
            - recommendations: list
            - metadata: dict
    """
    # Extract parameters
    repo_path = input_data.get("repo_path", ".")
    language = input_data.get("language", "python")
    metrics_to_analyze = input_data.get("metrics", ["complexity", "maintainability", "debt", "smells"])

    # Find files to analyze
    extension_map = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "go": ".go"
    }
    ext = extension_map.get(language, ".py")

    files = []
    if os.path.isfile(repo_path):
        files = [repo_path]
    else:
        for root, dirs, filenames in os.walk(repo_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ["node_modules", "vendor", ".git", "__pycache__", "venv", "tests"]]
            for filename in filenames:
                if filename.endswith(ext):
                    files.append(os.path.join(root, filename))

    if not files:
        return {
            "status": "error",
            "message": f"No {language} files found in {repo_path}"
        }

    # Analyze complexity
    all_functions = []
    total_loc = 0
    file_maintainability_indices = []  # Per-file MI for proper averaging

    for file_path in files:
        functions = analyze_function_complexity(file_path)
        all_functions.extend(functions)

        # Count lines of code
        with open(file_path) as f:
            file_loc = sum(1 for line in f if line.strip() and not line.strip().startswith("#"))
            total_loc += file_loc

        # Calculate per-file maintainability (proper approach)
        file_funcs = [f for f in functions if f["file"] == os.path.basename(file_path)]
        if file_funcs:
            file_complexity = sum(f["complexity"] for f in file_funcs) / len(file_funcs)
            file_mi = calculate_maintainability_index(file_complexity, file_loc)
            file_maintainability_indices.append(file_mi)

    # Calculate metrics
    complexities = [f["complexity"] for f in all_functions] if all_functions else [1]
    avg_complexity = sum(complexities) / len(complexities)
    max_complexity = max(complexities) if complexities else 0

    high_complexity_functions = sorted(
        [f for f in all_functions if f["complexity"] > 10],
        key=lambda x: x["complexity"],
        reverse=True
    )[:5]  # Top 5 most complex

    # Maintainability - average per-file MI (not whole-repo MI)
    maintainability_index = int(sum(file_maintainability_indices) / len(file_maintainability_indices)) if file_maintainability_indices else 0
    if maintainability_index >= 85:
        mi_status = "excellent"
    elif maintainability_index >= 65:
        mi_status = "good"
    elif maintainability_index >= 50:
        mi_status = "fair"
    else:
        mi_status = "poor"

    # Technical debt
    all_debt_items = []
    for file_path in files:
        with open(file_path) as f:
            content = f.read()
        debt_items = detect_technical_debt(content, file_path)
        all_debt_items.extend(debt_items)

    todo_items = [d for d in all_debt_items if d["type"] == "TODO"]
    fixme_items = [d for d in all_debt_items if d["type"] == "FIXME"]

    # Code smells
    code_smells = detect_code_smells(all_functions, files)

    # Compile metrics
    metrics = {
        "complexity": {
            "avg_cyclomatic": round(avg_complexity, 1),
            "max_cyclomatic": max_complexity,
            "high_complexity_functions": high_complexity_functions
        },
        "maintainability": {
            "index": maintainability_index,
            "status": mi_status
        },
        "technical_debt": {
            "todo_count": len(todo_items),
            "fixme_count": len(fixme_items),
            "items": all_debt_items[:10]  # First 10 for brevity
        },
        "code_smells": code_smells[:10]  # First 10 for brevity
    }

    # Calculate overall quality
    overall_quality = calculate_overall_quality(metrics)

    # Generate recommendations
    recommendations = generate_recommendations(metrics)

    return {
        "status": "success",
        "overall_quality": overall_quality,
        "metrics": metrics,
        "recommendations": recommendations,
        "metadata": {
            "files_analyzed": len(files),
            "lines_of_code": total_loc,
            "language": language
        }
    }


if __name__ == "__main__":
    # Example usage
    result = analyze({
        "repo_path": ".",
        "language": "python"
    })

    print(f"Overall Quality: {result['overall_quality']}/10")
    print(f"Avg Complexity: {result['metrics']['complexity']['avg_cyclomatic']}")
    print(f"Maintainability: {result['metrics']['maintainability']['index']} ({result['metrics']['maintainability']['status']})")
