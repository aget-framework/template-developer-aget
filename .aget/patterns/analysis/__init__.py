"""Code Analysis Patterns

Collection of patterns for code quality, standards, debugging, and spec consistency analysis.

Patterns:
- code_quality: Code quality assessment (complexity, maintainability, debt, smells)
- standards_check: Coding standards compliance checking (PEP-8, ESLint, custom)
- debug_assist: Debugging assistance (error analysis, fix strategies)
- spec_consistency: Spec-to-code consistency detection (gaps, drift)
- multi_repo_scan: Multi-repository discovery and analysis

All patterns follow common interface:
    def analyze(input_data: dict) -> dict

Part of template-developer-aget v2.7.0.
"""

__all__ = [
    "code_quality",
    "standards_check",
    "debug_assist",
    "spec_consistency",
    "multi_repo_scan"
]
