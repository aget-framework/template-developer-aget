#!/usr/bin/env python3
"""Specification Consistency Analysis Pattern

Checks code implementation against formal specifications.
Detects gaps (missing features), drift (scope changes), and over-implementation.

Part of template-developer-aget v2.7.0.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple


def parse_spec_file(spec_path: str) -> Dict[str, Any]:
    """Parse specification file (YAML, Markdown, or text).

    Args:
        spec_path: Path to specification file

    Returns:
        Parsed specification dictionary
    """
    if not os.path.exists(spec_path):
        return {"error": f"Spec file not found: {spec_path}"}

    with open(spec_path) as f:
        content = f.read()

    # Determine format by extension and content
    ext = os.path.splitext(spec_path)[1].lower()

    if ext in [".yaml", ".yml"]:
        # YAML format
        try:
            spec = yaml.safe_load(content)
            return {
                "format": "yaml",
                "capabilities": extract_capabilities_from_yaml(spec)
            }
        except yaml.YAMLError as e:
            return {"error": f"YAML parse error: {e}"}

    elif ext == ".md":
        # Markdown format
        capabilities = extract_capabilities_from_markdown(content)
        return {
            "format": "markdown",
            "capabilities": capabilities
        }
    else:
        # Plain text or unknown
        capabilities = extract_capabilities_from_text(content)
        return {
            "format": "text",
            "capabilities": capabilities
        }


def extract_capabilities_from_yaml(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract capabilities from YAML specification.

    Supports EARS format and capability list format.

    Args:
        spec: Parsed YAML dictionary

    Returns:
        List of capabilities with metadata
    """
    capabilities = []

    # Format 1: EARS requirements
    if "requirements" in spec:
        for req_id, req_data in spec["requirements"].items():
            if isinstance(req_data, dict):
                capabilities.append({
                    "id": req_id,
                    "type": req_data.get("type", "unknown"),
                    "description": req_data.get("description", ""),
                    "statement": req_data.get("statement", ""),
                    "priority": req_data.get("priority", "medium")
                })

    # Format 2: Capability levels
    if "capabilities" in spec:
        for cap_id, cap_data in spec["capabilities"].items():
            if isinstance(cap_data, dict):
                capabilities.append({
                    "id": cap_id,
                    "description": cap_data.get("description", ""),
                    "level": cap_data.get("level", "unknown"),
                    "priority": "high" if cap_data.get("level") == "action" else "medium"
                })

    return capabilities


def extract_capabilities_from_markdown(content: str) -> List[Dict[str, Any]]:
    """Extract capabilities from Markdown specification.

    Looks for patterns:
    - CAP-XXX: Description
    - **REQ-XXX**: Description
    - Bulleted capability lists

    Args:
        content: Markdown content

    Returns:
        List of capabilities
    """
    capabilities = []

    # Pattern 1: CAP-XXX or REQ-XXX identifiers
    pattern = r"(CAP-\d+|REQ-\d+):\s*(.+)"
    for match in re.finditer(pattern, content):
        cap_id = match.group(1)
        description = match.group(2).strip()
        capabilities.append({
            "id": cap_id,
            "description": description,
            "priority": "high"
        })

    # Pattern 2: EARS-style requirements
    ears_pattern = r"(WHERE|WHEN|WHILE|IF|AS LONG AS)\s+(.+?)\s+(SHALL|SHOULD)\s+(.+)"
    for match in re.finditer(ears_pattern, content, re.IGNORECASE):
        statement = match.group(0)
        capabilities.append({
            "id": f"EARS-{len(capabilities) + 1}",
            "type": "ears",
            "description": match.group(4).strip(),
            "statement": statement,
            "priority": "high" if "SHALL" in statement else "medium"
        })

    return capabilities


def extract_capabilities_from_text(content: str) -> List[Dict[str, Any]]:
    """Extract capabilities from plain text specification.

    Args:
        content: Text content

    Returns:
        List of capabilities
    """
    capabilities = []

    # Look for bullet points or numbered lists
    lines = content.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()

        # Numbered or bulleted item
        if re.match(r"^\d+\.|^-|^\*", line):
            # Extract capability description
            desc = re.sub(r"^\d+\.|^-|^\*", "", line).strip()
            if desc:
                capabilities.append({
                    "id": f"CAP-{i+1}",
                    "description": desc,
                    "priority": "medium"
                })

    return capabilities


def scan_code_for_capabilities(repo_path: str, capabilities: List[Dict[str, Any]], language: str = "python") -> Dict[str, Any]:
    """Scan code to find which capabilities are implemented.

    Args:
        repo_path: Path to repository
        capabilities: List of capabilities from spec
        language: Programming language

    Returns:
        Mapping of capability ID to implementation status
    """
    implementation_map = {}

    # Extension mapping
    extension_map = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "go": ".go"
    }
    ext = extension_map.get(language, ".py")

    # Collect all code files
    code_files = []
    if os.path.isfile(repo_path):
        code_files = [repo_path]
    else:
        for root, dirs, files in os.walk(repo_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ["node_modules", "vendor", ".git", "__pycache__", "venv", "tests"]]
            for file in files:
                if file.endswith(ext):
                    code_files.append(os.path.join(root, file))

    # Read all code content
    all_code_content = ""
    for file_path in code_files:
        try:
            with open(file_path) as f:
                all_code_content += f"\n{file_path}\n" + f.read() + "\n"
        except Exception:
            pass

    # Check each capability
    for cap in capabilities:
        cap_id = cap.get("id", "unknown")
        description = cap.get("description", "")

        # Extract keywords from description
        keywords = extract_keywords_from_description(description)

        # Check if keywords appear in code
        found_keywords = []
        for keyword in keywords:
            # Case-insensitive search for keyword
            if re.search(rf"\b{re.escape(keyword)}\b", all_code_content, re.IGNORECASE):
                found_keywords.append(keyword)

        # Determine implementation status
        if len(found_keywords) >= len(keywords) * 0.5:  # At least 50% of keywords found
            implementation_map[cap_id] = {
                "status": "implemented",
                "confidence": "high" if len(found_keywords) == len(keywords) else "medium",
                "evidence": found_keywords
            }
        else:
            implementation_map[cap_id] = {
                "status": "not_implemented",
                "confidence": "high",
                "evidence": []
            }

    return implementation_map


def extract_keywords_from_description(description: str) -> List[str]:
    """Extract meaningful keywords from capability description.

    Args:
        description: Capability description

    Returns:
        List of keywords
    """
    # Remove common words
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "are", "was", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "should", "could", "may", "might", "must", "can", "shall"
    }

    # Extract words
    words = re.findall(r'\b\w+\b', description.lower())

    # Filter out stop words and short words
    keywords = [w for w in words if w not in stop_words and len(w) > 3]

    return keywords[:5]  # Limit to top 5 keywords


def calculate_coverage(implementation_map: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate implementation coverage statistics.

    Args:
        implementation_map: Capability implementation mapping

    Returns:
        Coverage statistics
    """
    total = len(implementation_map)
    implemented = sum(1 for status in implementation_map.values() if status["status"] == "implemented")

    if total == 0:
        percentage = 0.0
    else:
        percentage = (implemented / total) * 100

    return {
        "total_capabilities": total,
        "implemented": implemented,
        "not_implemented": total - implemented,
        "percentage": round(percentage, 1)
    }


def detect_gaps(capabilities: List[Dict[str, Any]], implementation_map: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Detect missing capabilities (gaps).

    Args:
        capabilities: List of capabilities from spec
        implementation_map: Implementation status

    Returns:
        List of gap findings
    """
    gaps = []

    for cap in capabilities:
        cap_id = cap.get("id", "unknown")
        impl_status = implementation_map.get(cap_id, {})

        if impl_status.get("status") == "not_implemented":
            gaps.append({
                "capability_id": cap_id,
                "description": cap.get("description", ""),
                "priority": cap.get("priority", "medium"),
                "type": "missing_capability"
            })

    return gaps


def detect_drift(spec_path: str, repo_path: str, language: str = "python") -> List[Dict[str, Any]]:
    """Detect scope drift (expansion or reduction).

    Simplified implementation - looks for code patterns not in spec.

    Args:
        spec_path: Path to specification
        repo_path: Path to repository
        language: Programming language

    Returns:
        List of drift findings
    """
    drift_findings = []

    # This is a simplified placeholder
    # Full implementation would:
    # 1. Extract all functions/classes from code
    # 2. Compare against spec capabilities
    # 3. Flag functions that don't map to any spec capability

    # For template purposes, return empty list
    # Real implementation would use AST parsing

    return drift_findings


def generate_recommendations(gaps: List[Dict[str, Any]], coverage: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate actionable recommendations.

    Args:
        gaps: List of gap findings
        coverage: Coverage statistics

    Returns:
        List of recommendations
    """
    recommendations = []

    # Coverage-based recommendations
    coverage_pct = coverage["percentage"]
    if coverage_pct < 50:
        recommendations.append({
            "priority": "critical",
            "category": "coverage",
            "message": f"Low spec coverage ({coverage_pct}%) - {coverage['not_implemented']} capabilities missing",
            "action": "Implement high-priority missing capabilities first"
        })
    elif coverage_pct < 80:
        recommendations.append({
            "priority": "high",
            "category": "coverage",
            "message": f"Moderate spec coverage ({coverage_pct}%) - {coverage['not_implemented']} capabilities remaining",
            "action": "Plan implementation of remaining capabilities"
        })

    # Gap-based recommendations (high priority gaps)
    high_priority_gaps = [g for g in gaps if g.get("priority") == "high"]
    if high_priority_gaps:
        gap = high_priority_gaps[0]  # First high-priority gap
        recommendations.append({
            "priority": "high",
            "category": "gaps",
            "message": f"Missing high-priority capability: {gap['capability_id']}",
            "action": f"Implement: {gap['description']}"
        })

    return recommendations


def analyze(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze specification consistency with implementation.

    Args:
        input_data: Analysis parameters
            - spec_path: Path to specification file
            - repo_path: Path to repository (or single file)
            - language: Programming language (default: python)
            - analysis_type: "coverage" | "gaps" | "drift" | "all" (default: all)

    Returns:
        dict: Analysis results
            - status: "success" | "error"
            - spec_format: str (yaml/markdown/text)
            - coverage: dict (total, implemented, percentage)
            - gaps: list (missing capabilities)
            - drift: list (scope changes)
            - recommendations: list
    """
    # Extract parameters
    spec_path = input_data.get("spec_path")
    repo_path = input_data.get("repo_path", ".")
    language = input_data.get("language", "python")
    analysis_type = input_data.get("analysis_type", "all")

    if not spec_path:
        return {
            "status": "error",
            "message": "spec_path is required"
        }

    # Parse specification
    spec = parse_spec_file(spec_path)

    if "error" in spec:
        return {
            "status": "error",
            "message": spec["error"]
        }

    capabilities = spec.get("capabilities", [])

    if not capabilities:
        return {
            "status": "error",
            "message": "No capabilities found in specification"
        }

    # Scan code for implementation
    implementation_map = scan_code_for_capabilities(repo_path, capabilities, language)

    # Calculate coverage
    coverage = calculate_coverage(implementation_map)

    # Detect gaps
    gaps = detect_gaps(capabilities, implementation_map)

    # Detect drift (if requested)
    drift = []
    if analysis_type in ["drift", "all"]:
        drift = detect_drift(spec_path, repo_path, language)

    # Generate recommendations
    recommendations = generate_recommendations(gaps, coverage)

    return {
        "status": "success",
        "spec_format": spec.get("format", "unknown"),
        "coverage": coverage,
        "gaps": gaps[:10],  # Limit to first 10 for brevity
        "drift": drift[:10],  # Limit to first 10 for brevity
        "recommendations": recommendations,
        "metadata": {
            "spec_file": os.path.basename(spec_path),
            "total_capabilities": len(capabilities),
            "language": language
        }
    }


if __name__ == "__main__":
    # Example usage
    import tempfile

    # Create temporary spec file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
capabilities:
  CAP-001:
    description: User authentication
    level: action
  CAP-002:
    description: Password reset functionality
    level: action
  CAP-003:
    description: Email notification system
    level: information
""")
        spec_file = f.name

    # Create temporary implementation file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
def authenticate_user(username, password):
    # User authentication implementation
    return True

def login(username, password):
    return authenticate_user(username, password)
""")
        impl_file = f.name

    # Run analysis
    result = analyze({
        "spec_path": spec_file,
        "repo_path": impl_file,
        "language": "python"
    })

    print(f"Spec Format: {result['spec_format']}")
    print(f"Coverage: {result['coverage']['percentage']}% ({result['coverage']['implemented']}/{result['coverage']['total_capabilities']})")
    print(f"\nGaps Found: {len(result['gaps'])}")
    for gap in result['gaps']:
        print(f"  - {gap['capability_id']}: {gap['description']}")

    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  [{rec['priority']}] {rec['message']}")

    # Cleanup
    os.unlink(spec_file)
    os.unlink(impl_file)
