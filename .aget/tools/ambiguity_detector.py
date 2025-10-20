#!/usr/bin/env python3
"""
Ambiguity Detector - Intelligence Component for Experiment #2 Option C

Learns from Experiment #1 ambiguity patterns and proactively flags
potential ambiguities during spec creation.

Created: 2025-09-29 by my-AGET-aget (coordinator)
Experiment: Option C - Learning from Ambiguity
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple


class AmbiguityDetector:
    """Detects potential ambiguities in capability statements."""

    def __init__(self, corpus_path: str):
        """Load ambiguity patterns from corpus."""
        with open(corpus_path, 'r') as f:
            self.corpus = yaml.safe_load(f)
        self.patterns = self.corpus['ambiguity_patterns']

    def analyze_capability(self, capability: Dict) -> List[Dict]:
        """
        Analyze a capability and return list of ambiguity flags.

        Args:
            capability: Dict with 'statement', 'type', etc.

        Returns:
            List of ambiguity flags with suggested clarifications
        """
        flags = []
        statement = capability.get('statement', '')
        cap_type = capability.get('type', '')

        # Check each ambiguity pattern
        for pattern in self.patterns:
            if self._matches_pattern(statement, cap_type, pattern):
                flags.append({
                    'pattern_id': pattern['id'],
                    'pattern_name': pattern['pattern_name'],
                    'description': pattern['description'],
                    'suggested_clarifications': pattern['suggested_clarifications'],
                    'confidence': self._calculate_confidence(statement, pattern),
                    'evidence': pattern.get('evidence', {})
                })

        return flags

    def _matches_pattern(self, statement: str, cap_type: str, pattern: Dict) -> bool:
        """Check if statement matches ambiguity pattern."""
        pattern_id = pattern['id']

        if pattern_id == 'AMB-001':  # WHERE without specification
            return self._check_where_pattern(statement, cap_type)

        elif pattern_id == 'AMB-002':  # Implied data structure
            return self._check_structure_pattern(statement)

        elif pattern_id == 'AMB-003':  # Temporal without units
            return self._check_temporal_pattern(statement)

        elif pattern_id == 'AMB-004':  # Missing error handling
            return self._check_error_handling_pattern(statement)

        return False

    def _check_where_pattern(self, statement: str, cap_type: str) -> bool:
        """Detect WHERE pattern without location/format specification."""
        if cap_type != 'optional':
            return False

        has_where = bool(re.search(r'\bWHERE\b', statement, re.IGNORECASE))
        if not has_where:
            return False

        # Check for missing specifications
        has_location = bool(re.search(r'(/[\w/]+/|in \w+_Path|at \w+_Location)', statement))
        has_format = bool(re.search(r'\b(JSON|CSV|XML|JPEG|PNG|TXT|YAML)\b', statement, re.IGNORECASE))

        # Flag if WHERE present but missing location AND format
        return not (has_location or has_format)

    def _check_structure_pattern(self, statement: str) -> bool:
        """Detect composite structure references without definition."""
        composite_indicators = [
            r'\bComposite_\w+',
            r'\bManifest\b',
            r'\b\w+_Structure\b',
            r'\b\w+_Record\b',
            r'\b\w+_Keys\b'  # Plural often indicates composite
        ]

        for indicator in composite_indicators:
            if re.search(indicator, statement):
                # Check if statement includes structure definition
                has_definition = bool(re.search(r'(format|fields|structure|schema)', statement, re.IGNORECASE))
                if not has_definition:
                    return True

        return False

    def _check_temporal_pattern(self, statement: str) -> bool:
        """Detect temporal logic without clear units/thresholds."""
        temporal_keywords = r'\b(WITHIN|AFTER|BEFORE|DURING)\b'
        if not re.search(temporal_keywords, statement, re.IGNORECASE):
            return False

        # Check if time units specified
        has_units = bool(re.search(r'(hours?|minutes?|seconds?|days?|weeks?)', statement, re.IGNORECASE))

        # Check if numeric threshold present
        has_number = bool(re.search(r'\d+', statement))

        # Flag if temporal keyword present but missing units or numbers
        return not (has_units and has_number)

    def _check_error_handling_pattern(self, statement: str) -> bool:
        """Detect data processing without error handling spec."""
        processing_keywords = r'\b(parse|extract|process|validate|transform)\b'
        if not re.search(processing_keywords, statement, re.IGNORECASE):
            return False

        # Check if error handling mentioned
        error_handling = r'\b(error|fail|invalid|malformed|validate|log)\b'
        has_error_spec = bool(re.search(error_handling, statement, re.IGNORECASE))

        # Flag if processing present but no error handling
        return not has_error_spec

    def _calculate_confidence(self, statement: str, pattern: Dict) -> float:
        """Calculate confidence score (0.0-1.0) for ambiguity flag."""
        # Simple heuristic: more trigger keywords = higher confidence
        keywords = pattern.get('trigger_keywords', [])
        matches = sum(1 for kw in keywords if kw.lower() in statement.lower())

        if matches == 0:
            return 0.5  # Matched pattern logic but no keywords
        elif matches == 1:
            return 0.7
        elif matches >= 2:
            return 0.9

        return 0.6

    def generate_report(self, capabilities: List[Dict], flags_log: List[Dict]) -> str:
        """Generate ambiguity detection report."""
        total_caps = len(capabilities)
        total_flags = len(flags_log)
        flags_by_pattern = {}

        for flag_entry in flags_log:
            for flag in flag_entry['flags']:
                pattern_id = flag['pattern_id']
                flags_by_pattern[pattern_id] = flags_by_pattern.get(pattern_id, 0) + 1

        report = f"""# Ambiguity Detection Report

**Total Capabilities Analyzed**: {total_caps}
**Total Flags Raised**: {total_flags}
**Flagging Rate**: {total_flags/total_caps*100:.1f}%

## Flags by Pattern

"""
        for pattern_id, count in sorted(flags_by_pattern.items()):
            pattern_name = next(p['pattern_name'] for p in self.patterns if p['id'] == pattern_id)
            report += f"- **{pattern_id}** ({pattern_name}): {count} flags\n"

        report += "\n## Human Decision Summary\n\n"

        accepted = sum(1 for fe in flags_log for f in fe['flags'] if fe.get('human_decision') == 'accepted')
        rejected = sum(1 for fe in flags_log for f in fe['flags'] if fe.get('human_decision') == 'rejected')
        modified = sum(1 for fe in flags_log for f in fe['flags'] if fe.get('human_decision') == 'modified')

        report += f"- **Accepted**: {accepted} ({accepted/total_flags*100:.1f}%)\n"
        report += f"- **Rejected (false positive)**: {rejected} ({rejected/total_flags*100:.1f}%)\n"
        report += f"- **Modified**: {modified} ({modified/total_flags*100:.1f}%)\n"

        false_positive_rate = rejected / total_flags * 100 if total_flags > 0 else 0
        report += f"\n**False Positive Rate**: {false_positive_rate:.1f}% (target: <20%)\n"

        return report


def test_detector():
    """Test ambiguity detector on example capabilities."""
    # Use production corpus location (v2.2.0 standard)
    corpus_path = '.aget/intelligence/ambiguity_corpus.yaml'
    if not Path(corpus_path).exists():
        # Fallback to experiment location for testing
        corpus_path = '.aget/experiments/option_c/ambiguity_corpus.yaml'

    detector = AmbiguityDetector(corpus_path)

    test_cases = [
        {
            'id': 'TEST-001',
            'type': 'optional',
            'statement': 'WHERE Recipe_Images are available, the SYSTEM shall store Image_Files',
            'expected_flags': ['AMB-001']  # WHERE without specification
        },
        {
            'id': 'TEST-002',
            'type': 'optional',
            'statement': 'WHERE Recipe_Images are available, the SYSTEM shall store Image_Files in /data/images/ as JPEG',
            'expected_flags': []  # Should NOT flag (has location + format)
        },
        {
            'id': 'TEST-003',
            'type': 'ubiquitous',
            'statement': 'The SYSTEM shall generate Recipe_Composite_Keys',
            'expected_flags': ['AMB-002']  # Implied structure
        },
        {
            'id': 'TEST-004',
            'type': 'conditional',
            'statement': 'IF Recipe is popular recently, THEN mark as Trending',
            'expected_flags': ['AMB-003']  # Vague temporal logic
        },
        {
            'id': 'TEST-005',
            'type': 'event-driven',
            'statement': 'WHEN parsing Recipe_File, the SYSTEM shall extract Recipe_Data',
            'expected_flags': ['AMB-004']  # Missing error handling
        }
    ]

    print("=== Ambiguity Detector Test ===\n")

    for test in test_cases:
        flags = detector.analyze_capability(test)
        flag_ids = [f['pattern_id'] for f in flags]

        status = "✓ PASS" if flag_ids == test['expected_flags'] else "✗ FAIL"
        print(f"{status} {test['id']}")
        print(f"  Statement: {test['statement'][:60]}...")
        print(f"  Expected: {test['expected_flags']}")
        print(f"  Got: {flag_ids}")

        if flag_ids:
            print(f"  Flags raised:")
            for flag in flags:
                print(f"    - {flag['pattern_id']}: {flag['pattern_name']} (confidence: {flag['confidence']:.2f})")
        print()

    return detector


if __name__ == '__main__':
    test_detector()