# AGET Test Suite

## Overview

Test suite for AGET agents, covering contract validation and agent-specific functionality.

## Contract Tests (v2.5) ⭐

Contract tests validate the "contract" between agent components and the AGET framework.

### Wake Protocol Contract (`test_wake_contract.py`)

**Purpose**: Validate that wake protocol correctly reports agent identity, version, and capabilities.

**Tests** (4):
1. `test_wake_protocol_reports_agent_name` - Agent name present and valid
2. `test_wake_protocol_reports_version` - Version in X.Y.Z format
3. `test_wake_protocol_reports_capabilities` - Capabilities structure valid (if present)
4. `test_wake_protocol_reports_domain` - Domain specified (if present)

**Contract Requirements**:
- agent_name must be present and non-empty
- aget_version must follow X.Y.Z format
- capabilities (if present) must be a dictionary
- domain (if present) must be a non-empty string

### Identity Contract (`test_identity_contract.py`)

**Purpose**: Validate that agent identity remains consistent and separate from operational context.

**Tests** (3):
1. `test_identity_consistency_version_json_vs_manifest` - Version consistency across metadata files
2. `test_identity_no_conflation_with_directory_name` - Identity matches location
3. `test_identity_persistence_across_invocations` - Stable identity fields vs operational state

**Contract Requirements**:
- version.json version must match agent_manifest.yaml version (if manifest exists)
- agent_name must match directory name (identity = location)
- Identity fields (agent_name, aget_version, created) must be stable
- Operational fields (current_session, last_wake_time, active_task) must NOT be in version.json

## Running Tests

### Run All Tests
```bash
python3 -m pytest tests/ -v
```

### Run Contract Tests Only
```bash
python3 -m pytest tests/test_wake_contract.py tests/test_identity_contract.py -v
```

### Run Specific Test File
```bash
python3 -m pytest tests/test_wake_contract.py -v
```

### Run with Coverage
```bash
python3 -m pytest tests/ --cov=.aget --cov-report=term-missing
```

## Adding Tests

### Agent-Specific Tests

Create test files for your agent's specific functionality:
- `test_<feature>_integration.py` - Integration tests
- `test_<feature>_isolated.py` - Unit tests with mocks
- `test_<feature>_error_scenarios.py` - Error handling tests

### Test Naming Convention

- Test files: `test_*.py`
- Test functions: `def test_<description>():`
- Use clear, descriptive names
- Include docstrings explaining what's tested

## Requirements

- Python 3.11+
- pytest 8.0+
- pytest-mock (for mocked tests, optional)

## Contract Tests Philosophy

Contract tests validate the "contract" between agent components:
- **Wake Protocol**: Agent must report identity/capabilities correctly
- **Identity Contract**: Agent identity must be stable and consistent

These are **minimal** tests (not comprehensive), designed to catch contract violations early.

## Troubleshooting

### Tests Fail After Version Update

If contract tests fail after version promotion:
1. Check version.json and agent_manifest.yaml for consistency
2. Verify agent_name matches directory name
3. Ensure stable identity fields are present

### Import Errors

If tests can't import patterns:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / ".aget" / "patterns"))
```

---

**Template Version**: v2.5.0
**Last Updated**: 2025-10-06
**Framework**: AGET v2.5 validation standards
