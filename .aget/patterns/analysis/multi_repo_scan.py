#!/usr/bin/env python3
"""Multi-Repository Scanning Pattern

Discovers and analyzes multiple repositories for cross-repo patterns,
consistency checking, and duplicate code detection.

Part of template-developer-aget v2.7.0.
"""

import os
import yaml
from pathlib import Path
from typing import List, Dict, Any


def discover_repositories(base_path: str, config_path: str = None, scan_mode: str = "auto") -> List[str]:
    """Discover repositories based on mode (auto vs configured).

    Args:
        base_path: Base directory to scan (e.g., ~/github)
        config_path: Path to repos.yaml configuration file
        scan_mode: "auto" or "configured"

    Returns:
        List of repository paths
    """
    repos = []

    if scan_mode == "configured" and config_path and os.path.exists(config_path):
        # Load from configuration file
        with open(config_path) as f:
            config = yaml.safe_load(f)

        if "repos" in config:
            # Check for explicit include list
            include_list = config["repos"].get("include", [])
            exclude_list = config["repos"].get("exclude", [])

            if include_list:
                # Use explicit include list
                repos = [os.path.expanduser(repo) for repo in include_list]
            else:
                # Fallback to auto-scan with exclusions
                repos = auto_scan_repos(base_path, exclude_list)
        else:
            # Config exists but malformed, fallback to auto-scan
            repos = auto_scan_repos(base_path, [])
    else:
        # Auto-scan mode (zero-config)
        repos = auto_scan_repos(base_path, [])

    return repos


def auto_scan_repos(base_path: str, excluded: List[str] = None) -> List[str]:
    """Auto-discover git repositories in base_path.

    Args:
        base_path: Directory to scan
        excluded: List of patterns to exclude

    Returns:
        List of discovered repository paths
    """
    if excluded is None:
        excluded = []

    # Default exclusions
    default_exclusions = ["vendor", "archive", "node_modules", "*-archive"]
    all_exclusions = default_exclusions + excluded

    repos = []
    base_path_expanded = os.path.expanduser(base_path)

    if not os.path.exists(base_path_expanded):
        return repos

    for item in os.listdir(base_path_expanded):
        item_path = os.path.join(base_path_expanded, item)

        # Check if directory
        if not os.path.isdir(item_path):
            continue

        # Check if excluded
        if is_excluded(item, all_exclusions):
            continue

        # Check if git repository
        if os.path.exists(os.path.join(item_path, ".git")):
            repos.append(item_path)

    return sorted(repos)


def is_excluded(name: str, exclusions: List[str]) -> bool:
    """Check if name matches any exclusion pattern.

    Args:
        name: Directory name to check
        exclusions: List of exclusion patterns

    Returns:
        True if excluded, False otherwise
    """
    for pattern in exclusions:
        if pattern.startswith("*"):
            # Wildcard pattern (simple suffix match)
            if name.endswith(pattern[1:]):
                return True
        elif pattern.endswith("*"):
            # Wildcard pattern (simple prefix match)
            if name.startswith(pattern[:-1]):
                return True
        else:
            # Exact match
            if name == pattern:
                return True
    return False


def detect_language(repo_path: str) -> str:
    """Auto-detect primary language of repository.

    Args:
        repo_path: Path to repository

    Returns:
        Language name (python, javascript, go, etc.) or "unknown"
    """
    extension_to_language = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".go": "go",
        ".rb": "ruby",
        ".java": "java",
        ".rs": "rust"
    }

    file_counts = {}

    # Count files by extension
    for ext in extension_to_language.keys():
        count = 0
        for root, dirs, files in os.walk(repo_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ["node_modules", "vendor", ".git", "__pycache__"]]
            count += sum(1 for f in files if f.endswith(ext))

        if count > 0:
            file_counts[ext] = count

    if not file_counts:
        return "unknown"

    # Return language with most files
    primary_ext = max(file_counts, key=file_counts.get)
    return extension_to_language[primary_ext]


def analyze(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze multiple repositories for patterns and consistency.

    Args:
        input_data: Analysis parameters
            - scan_mode: "auto" or "configured"
            - base_path: Base directory (default: ~/github)
            - config_path: Path to repos.yaml (optional)
            - analysis_type: "consistency" | "patterns" | "duplicates"

    Returns:
        dict: Analysis results
            - status: "success" | "error"
            - repos_discovered: int
            - repos_analyzed: int
            - repositories: list (repo metadata)
            - consistency_analysis: dict (if analysis_type == "consistency")
            - recommendations: list
    """
    # Extract parameters
    scan_mode = input_data.get("scan_mode", "auto")
    base_path = input_data.get("base_path", "~/github")
    config_path = input_data.get("config_path", ".aget/config/repos.yaml")
    analysis_type = input_data.get("analysis_type", "consistency")

    # Discover repositories
    repos = discover_repositories(base_path, config_path, scan_mode)

    if not repos:
        return {
            "status": "error",
            "message": f"No repositories found in {base_path}",
            "repos_discovered": 0
        }

    # Gather repository metadata
    repositories = []
    for repo_path in repos:
        repo_name = os.path.basename(repo_path)
        language = detect_language(repo_path)
        repositories.append({
            "name": repo_name,
            "path": repo_path,
            "language": language
        })

    # Perform analysis based on type
    result = {
        "status": "success",
        "repos_discovered": len(repos),
        "repos_analyzed": len(repos),
        "repositories": repositories
    }

    if analysis_type == "consistency":
        # Analyze consistency across repositories
        consistency = analyze_consistency(repositories)
        result["consistency_analysis"] = consistency
        result["recommendations"] = generate_consistency_recommendations(consistency)
    elif analysis_type == "patterns":
        # Recognize shared patterns
        patterns = recognize_patterns(repositories)
        result["patterns"] = patterns
    elif analysis_type == "duplicates":
        # Detect duplicate code
        duplicates = find_duplicate_code(repositories)
        result["duplicate_code"] = duplicates
        result["recommendations"] = generate_duplicate_recommendations(duplicates)

    return result


def analyze_consistency(repositories: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze consistency across repositories.

    Args:
        repositories: List of repo metadata

    Returns:
        Consistency analysis results
    """
    # Group repositories by language
    languages = {}
    for repo in repositories:
        lang = repo["language"]
        languages.setdefault(lang, []).append(repo["name"])

    # Identify shared patterns (simplified version)
    shared_patterns = []
    inconsistencies = []

    # Language consistency
    if len(languages) == 1:
        lang = list(languages.keys())[0]
        shared_patterns.append({
            "pattern": f"Language: {lang}",
            "repos": list(languages.values())[0],
            "status": "consistent"
        })
    else:
        inconsistencies.append({
            "aspect": "Programming language",
            "variants": languages,
            "recommendation": "Consider standardizing on single language for related projects"
        })

    return {
        "shared_patterns": shared_patterns,
        "inconsistencies": inconsistencies
    }


def recognize_patterns(repositories: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Recognize architectural patterns across repositories.

    Args:
        repositories: List of repo metadata

    Returns:
        Pattern recognition results
    """
    # Simplified pattern recognition
    languages = {}
    for repo in repositories:
        lang = repo["language"]
        languages[lang] = languages.get(lang, 0) + 1

    return {
        "languages": languages,
        "total_repos": len(repositories)
    }


def find_duplicate_code(repositories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find duplicate code blocks across repositories.

    Args:
        repositories: List of repo metadata

    Returns:
        List of duplicate code findings
    """
    # Simplified duplicate detection (placeholder)
    # Full implementation would use difflib or similar
    duplicates = []

    # For template purposes, this is a structural placeholder
    # Real implementation would:
    # 1. Collect code files from all repos
    # 2. Calculate similarity between file pairs
    # 3. Report high-similarity matches (>80%)

    return duplicates


def generate_consistency_recommendations(consistency: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate recommendations based on consistency analysis.

    Args:
        consistency: Consistency analysis results

    Returns:
        List of recommendations
    """
    recommendations = []

    for inconsistency in consistency.get("inconsistencies", []):
        recommendations.append({
            "priority": "medium",
            "action": f"Standardize {inconsistency['aspect']}",
            "rationale": inconsistency["recommendation"]
        })

    return recommendations


def generate_duplicate_recommendations(duplicates: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Generate recommendations based on duplicate code findings.

    Args:
        duplicates: Duplicate code findings

    Returns:
        List of recommendations
    """
    recommendations = []

    for duplicate in duplicates:
        recommendations.append({
            "priority": "high",
            "action": f"Extract duplicate code to shared library",
            "scope": ", ".join(duplicate.get("repos", []))
        })

    return recommendations


if __name__ == "__main__":
    # Example usage
    result = analyze({
        "scan_mode": "auto",
        "base_path": "~/github",
        "analysis_type": "consistency"
    })

    print(f"Discovered {result['repos_discovered']} repositories")
    print(f"Analyzed {result['repos_analyzed']} repositories")
    for repo in result.get("repositories", []):
        print(f"  - {repo['name']} ({repo['language']})")
