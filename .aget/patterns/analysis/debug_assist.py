#!/usr/bin/env python3
"""Debugging Assistance Pattern

Analyzes errors and provides root cause hypotheses + fix strategies.
Includes concrete Python traceback example for demonstration.

Part of template-developer-aget v2.7.0.
"""

import re
from typing import Dict, Any, List


# Error pattern library
ERROR_PATTERNS = {
    r"AttributeError.*'NoneType'": "null_pointer_exception",
    r"KeyError": "missing_dict_key",
    r"IndexError": "list_index_out_of_range",
    r"TypeError.*not callable": "calling_non_function",
    r"TypeError.*missing.*argument": "missing_function_argument",
    r"ImportError|ModuleNotFoundError": "import_error",
    r"ValueError": "value_error",
    r"RuntimeError.*coroutine.*never awaited": "async_await_missing"
}


def recognize_error_pattern(error_type: str, error_message: str) -> str:
    """Classify error into known pattern.

    Args:
        error_type: Exception class name
        error_message: Error message

    Returns:
        Pattern name or "unknown_pattern"
    """
    error_full = f"{error_type}: {error_message}"

    for pattern_regex, pattern_name in ERROR_PATTERNS.items():
        if re.search(pattern_regex, error_full):
            return pattern_name

    return "unknown_pattern"


def extract_variable_from_message(error_message: str) -> str:
    """Extract variable name from error message.

    Args:
        error_message: Error message

    Returns:
        Variable name or empty string
    """
    # Pattern: 'NoneType' object has no attribute 'X'
    match = re.search(r"has no attribute '(\w+)'", error_message)
    if match:
        return match.group(1)

    # Pattern: 'X' (for KeyError)
    match = re.search(r"'(\w+)'", error_message)
    if match:
        return match.group(1)

    return ""


def generate_null_pointer_hypotheses(error_message: str, code_context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate hypotheses for null pointer exceptions.

    Args:
        error_message: Error message
        code_context: Code context dict

    Returns:
        List of hypotheses (ranked by confidence)
    """
    hypotheses = []

    # Extract variable/attribute
    attr = extract_variable_from_message(error_message)

    # Hypothesis 1: Variable is None (high confidence)
    hypotheses.append({
        "rank": 1,
        "confidence": "high",
        "cause": f"Object attribute '{attr}' is None",
        "evidence": [
            f"Attempted to access .{attr} on None object",
            "No null check before attribute access",
            "Possible: Database field allows NULL, or object not initialized"
        ],
        "fix_strategy": f"""Add null check before accessing attribute:

```python
if obj and obj.{attr}:
    # Use obj.{attr}
    pass
else:
    # Handle None case (raise error or use default)
    raise ValueError('Object or attribute is None')
```""",
        "prevention": "Add validation at data source (database constraint or model validation)"
    })

    # Hypothesis 2: Object not loaded properly (medium confidence)
    hypotheses.append({
        "rank": 2,
        "confidence": "medium",
        "cause": "Parent object not loaded/initialized properly",
        "evidence": [
            "Object might be None due to failed retrieval",
            "No validation in object loading code"
        ],
        "fix_strategy": """Validate object exists before use:

```python
obj = get_object(id)
if not obj:
    raise ValueError(f'Object {id} not found')
# Now safe to use obj
```""",
        "prevention": "Add existence checks in data access layer"
    })

    return hypotheses


def generate_missing_key_hypotheses(error_message: str, code_context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate hypotheses for missing dictionary key errors.

    Args:
        error_message: Error message
        code_context: Code context dict

    Returns:
        List of hypotheses
    """
    hypotheses = []

    key = extract_variable_from_message(error_message)

    hypotheses.append({
        "rank": 1,
        "confidence": "high",
        "cause": f"Key '{key}' missing from dictionary",
        "evidence": [
            f"Dictionary access dict['{key}'] failed",
            "Key might be optional or API response changed"
        ],
        "fix_strategy": f"""Use .get() with default value:

```python
# Instead of: value = data['{key}']
value = data.get('{key}', default_value)

# Or validate key exists:
if '{key}' in data:
    value = data['{key}']
else:
    raise ValueError('Required key {key} missing')
```""",
        "prevention": "Use schema validation (Pydantic, marshmallow) at API boundaries"
    })

    return hypotheses


def create_investigation_path(error_pattern: str, hypotheses: List[Dict[str, Any]]) -> List[str]:
    """Generate step-by-step investigation path.

    Args:
        error_pattern: Classified error pattern
        hypotheses: List of hypotheses

    Returns:
        Investigation steps
    """
    steps = []

    if error_pattern == "null_pointer_exception":
        steps = [
            "1. Add debug print to confirm value is None: print(repr(obj))",
            "2. Check data source: Query database/API to see if field can be null",
            "3. Review object initialization: Trace where object is created/loaded",
            "4. Add validation: Implement null check at appropriate location"
        ]
    elif error_pattern == "missing_dict_key":
        steps = [
            "1. Print dictionary keys: print(dict.keys()) to see available keys",
            "2. Check API documentation: Verify if key is always present or optional",
            "3. Review recent API changes: Did API response format change?",
            "4. Implement defensive access: Use .get() with default or validation"
        ]
    else:
        steps = [
            "1. Reproduce error in isolated test case",
            "2. Add debug logging around error location",
            "3. Check input data for unexpected values",
            "4. Review recent code changes in error area"
        ]

    return steps


def analyze(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Assist with debugging by analyzing errors.

    Args:
        input_data: Analysis parameters
            - error_type: Exception class name
            - error_message: Error message
            - stack_trace: Stack trace (optional)
            - code_context: Context dict (file, function, line, code_snippet)
            - language: Programming language

    Returns:
        dict: Analysis results
            - status: "success" | "error"
            - error_pattern: str (classified pattern)
            - confidence: str (high/medium/low)
            - root_cause_hypotheses: list (ranked)
            - investigation_path: list (debugging steps)
            - similar_errors: list
            - recommendations: list
    """
    # Extract parameters
    error_type = input_data.get("error_type", "")
    error_message = input_data.get("error_message", "")
    code_context = input_data.get("code_context", {})
    language = input_data.get("language", "python")

    if not error_type or not error_message:
        return {
            "status": "error",
            "message": "error_type and error_message are required"
        }

    # Recognize error pattern
    error_pattern = recognize_error_pattern(error_type, error_message)

    # Generate hypotheses based on pattern
    if error_pattern == "null_pointer_exception":
        hypotheses = generate_null_pointer_hypotheses(error_message, code_context)
        confidence = "high"
    elif error_pattern == "missing_dict_key":
        hypotheses = generate_missing_key_hypotheses(error_message, code_context)
        confidence = "high"
    else:
        # Generic hypothesis for unknown patterns
        hypotheses = [{
            "rank": 1,
            "confidence": "medium",
            "cause": "Error cause needs investigation",
            "evidence": ["Pattern not in known error library"],
            "fix_strategy": "Investigate error context and recent code changes",
            "prevention": "Add error handling and validation"
        }]
        confidence = "medium"

    # Create investigation path
    investigation_path = create_investigation_path(error_pattern, hypotheses)

    # Generate recommendations
    recommendations = []
    if hypotheses:
        top_hypothesis = hypotheses[0]
        recommendations.append({
            "priority": "high",
            "action": top_hypothesis["fix_strategy"].split("\n")[0],  # First line
            "rationale": top_hypothesis["cause"]
        })

    return {
        "status": "success",
        "error_pattern": error_pattern,
        "confidence": confidence,
        "root_cause_hypotheses": hypotheses,
        "investigation_path": investigation_path,
        "similar_errors": [],  # Placeholder for codebase-wide search
        "recommendations": recommendations
    }


# ============================================================================
# CONCRETE EXAMPLE: Python AttributeError with NoneType
# (Meta-supervision requirement from Gate 2 review)
# ============================================================================

def demonstrate_null_pointer_debugging():
    """Concrete example: Debugging AttributeError with NoneType.

    This demonstrates the pattern analysis on a realistic Python error scenario.
    """
    # Sample error scenario
    error_scenario = {
        "error_type": "AttributeError",
        "error_message": "'NoneType' object has no attribute 'split'",
        "stack_trace": """Traceback (most recent call last):
  File "app.py", line 28, in <module>
    process_email(123)
  File "app.py", line 12, in process_email
    email_parts = user.email.split('@')
AttributeError: 'NoneType' object has no attribute 'split'""",
        "code_context": {
            "file": "app.py",
            "function": "process_email",
            "line": 12,
            "code_snippet": "email_parts = user.email.split('@')"
        },
        "language": "python"
    }

    # Analyze error
    result = analyze(error_scenario)

    # Display analysis
    print("=" * 60)
    print("CONCRETE EXAMPLE: Python AttributeError Analysis")
    print("=" * 60)
    print()
    print(f"Error: {error_scenario['error_type']}: {error_scenario['error_message']}")
    print()
    print(f"Pattern: {result['error_pattern']}")
    print(f"Confidence: {result['confidence']}")
    print()
    print("Root Cause Hypotheses (ranked):")
    print()
    for hypothesis in result['root_cause_hypotheses']:
        print(f"{hypothesis['rank']}. {hypothesis['cause']} ({hypothesis['confidence']} confidence)")
        print(f"   Evidence:")
        for evidence in hypothesis['evidence']:
            print(f"     - {evidence}")
        print(f"   Fix Strategy:")
        for line in hypothesis['fix_strategy'].split('\n')[:5]:  # First 5 lines
            print(f"     {line}")
        print()

    print("Investigation Path:")
    for step in result['investigation_path']:
        print(f"  {step}")
    print()
    print("=" * 60)

    return result


if __name__ == "__main__":
    # Run concrete example demonstration
    demonstrate_null_pointer_debugging()

    print("\nPattern can be used for other errors:")
    print()

    # Example 2: KeyError
    result2 = analyze({
        "error_type": "KeyError",
        "error_message": "'email'",
        "code_context": {
            "file": "api.py",
            "line": 45,
            "code_snippet": "email = data['email']"
        }
    })
    print(f"KeyError analysis: {result2['error_pattern']} ({result2['confidence']} confidence)")
    print(f"Fix: {result2['root_cause_hypotheses'][0]['fix_strategy'].split(chr(10))[0]}")
