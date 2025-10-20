# Specification Consistency Check Example

Demonstrates the `spec_consistency.py` pattern for detecting gaps between specification and implementation.

## Files

- `user_management_spec.yaml` - Specification defining 5 capabilities
- `user_management.py` - Implementation with only 2 capabilities implemented
- `run_check.py` - Script that runs spec consistency check

## Usage

```bash
cd examples/spec_consistency
python3 run_check.py
```

## Expected Output

The analysis identifies:

1. **Coverage**: 40% (2/5 capabilities implemented)
2. **Gaps**: 3 missing high-priority capabilities
   - CAP-002: Password reset functionality (high priority)
   - CAP-003: Email notification system (medium priority)
   - CAP-005: Role-based access control (high priority)
3. **Recommendations**: Implement missing high-priority capabilities first

## Spec Format Support

The pattern supports three specification formats:

### 1. YAML with Capabilities
```yaml
capabilities:
  CAP-001:
    description: User authentication
    level: action
    priority: high
```

### 2. Markdown with Identifiers
```markdown
## Requirements

CAP-001: User authentication and login
REQ-002: Password reset functionality
```

### 3. Plain Text Lists
```
1. User authentication and login
2. Password reset functionality
3. Email notification system
```

## Analysis Types

- **coverage**: Calculate implementation percentage
- **gaps**: Identify missing capabilities
- **drift**: Detect scope expansion or reduction
- **all**: Run all analyses (default)

## Learning Points

- Keyword-based matching detects implemented capabilities
- Coverage percentage shows implementation completeness
- Gap detection highlights missing features by priority
- Recommendations guide implementation planning
- Multi-format support works with various spec styles
