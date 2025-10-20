# AGET Pattern Best Practices

*Last Updated: 2025-09-24*

## Overview

This guide provides best practices for developing, testing, and using AGET patterns. Following these practices ensures patterns are reliable, composable, and maintainable.

## Pattern Development Guidelines

### 1. Structure and Organization

**Directory Structure**
```
patterns/
├── <category>/           # Logical grouping
│   ├── __init__.py      # Make it a package
│   ├── <pattern>.py     # Pattern implementation
│   └── README.md        # Category documentation
```

**File Naming**
- Use lowercase with underscores: `wake_protocol.py`
- Be descriptive but concise: `migration_cleanup.py`
- Group related patterns in same category

### 2. Pattern Implementation

**Entry Points**
Every pattern should have a clear entry point:
```python
def main(args=None):
    """Main entry point for CLI usage."""
    pass

# Or for class-based patterns:
class PatternName:
    def run(self, **kwargs):
        """Run the pattern."""
        pass
```

**Return Values**
Patterns should return structured dictionaries:
```python
def pattern_function():
    return {
        'success': True,          # Required
        'message': 'Completed',   # Recommended
        'data': {},              # Optional data
        'execution_time': 1.5    # Performance metric
    }
```

**Error Handling**
```python
try:
    # Pattern logic
    return {'success': True, 'data': result}
except Exception as e:
    return {
        'success': False,
        'error': str(e),
        'error_type': type(e).__name__
    }
```

### 3. Safety and Idempotency

**Dry Run Mode**
Always support dry-run for destructive operations:
```python
def cleanup_pattern(dry_run=True):
    if dry_run:
        print("DRY RUN - No changes will be made")
        # Show what would happen
    else:
        # Actually perform changes
```

**Confirmation Prompts**
For critical operations:
```python
if not dry_run and not force:
    response = input("This will delete files. Continue? (y/N): ")
    if response.lower() != 'y':
        return {'success': False, 'message': 'Cancelled by user'}
```

**Idempotency**
Patterns should be safe to run multiple times:
```python
# Check if already done
if Path('.aget/initialized').exists():
    return {'success': True, 'message': 'Already initialized'}

# Do the work
initialize()

# Mark as done
Path('.aget/initialized').touch()
```

### 4. Performance Requirements

**<2 Second Rule**
All patterns must complete in under 2 seconds:
```python
import time

def pattern_function():
    start = time.time()

    # Pattern logic here

    execution_time = time.time() - start
    if execution_time > 2.0:
        print(f"⚠️  Pattern took {execution_time:.2f}s (>2s limit)")

    return {
        'success': True,
        'execution_time': execution_time
    }
```

**Optimization Tips**
- Cache expensive operations
- Use generators for large datasets
- Limit file scanning depth
- Batch operations when possible

### 5. Composability

**Clean Interfaces**
Patterns should work standalone and in combination:
```python
# Good - can be called from other patterns
def wake_protocol(quiet=False):
    result = perform_wake()
    if not quiet:
        print(result['message'])
    return result

# Bad - prints directly, hard to compose
def wake_protocol():
    print("Waking up...")
    perform_wake()
```

**State Management**
Use `.aget/` directory for state:
```python
STATE_FILE = Path('.aget/session_state.json')

def save_state(data):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, indent=2))

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}
```

## Testing Patterns

### Unit Tests

Every pattern should have tests:
```python
# tests/test_pattern_name.py
import pytest
from patterns.category.pattern_name import pattern_function

def test_pattern_success():
    result = pattern_function()
    assert result['success'] == True

def test_pattern_dry_run():
    result = pattern_function(dry_run=True)
    assert result['success'] == True
    # Verify no changes were made

def test_pattern_error_handling():
    with pytest.raises(ValueError):
        pattern_function(invalid_param='bad')
```

### Integration Tests

Test pattern combinations:
```python
def test_morning_routine():
    # Wake up
    wake_result = wake_protocol()
    assert wake_result['success']

    # Validate
    validate_result = validate_config()
    assert validate_result['success']

    # Check state consistency
    state = load_state()
    assert state['session_active'] == True
```

## Common Pitfalls to Avoid

### 1. Hard-Coded Paths
❌ **Bad**:
```python
config_file = '/Users/john/project/config.json'
```

✅ **Good**:
```python
config_file = Path('.') / 'config.json'
```

### 2. Silent Failures
❌ **Bad**:
```python
try:
    risky_operation()
except:
    pass  # Silent failure
```

✅ **Good**:
```python
try:
    risky_operation()
except Exception as e:
    return {'success': False, 'error': str(e)}
```

### 3. Destructive Defaults
❌ **Bad**:
```python
def cleanup(force=True):  # Dangerous default
    if force:
        delete_everything()
```

✅ **Good**:
```python
def cleanup(dry_run=True, force=False):  # Safe defaults
    if not dry_run and force:
        delete_everything()
```

### 4. Blocking Operations
❌ **Bad**:
```python
def slow_pattern():
    time.sleep(10)  # Blocks for 10 seconds
```

✅ **Good**:
```python
def fast_pattern():
    # Use async or background tasks for long operations
    # Or break into smaller chunks
```

## Pattern Categories

### Session Patterns
- **Purpose**: Manage agent work sessions
- **Examples**: wake, wind_down, sign_off
- **Best Practice**: Always save state between sessions

### Housekeeping Patterns
- **Purpose**: Maintain project health
- **Examples**: cleanup, doc_check, migration_cleanup
- **Best Practice**: Always support dry-run mode

### Bridge Patterns
- **Purpose**: Transform private outputs to public products
- **Examples**: extract_output, publish_results
- **Best Practice**: Preserve privacy while sharing value

### Meta Patterns
- **Purpose**: Manage multiple projects
- **Examples**: project_scanner, bulk_update
- **Best Practice**: Handle project variations gracefully

## Performance Optimization

### Caching Strategy
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(path):
    # This will be cached
    return analyze_directory(path)
```

### Lazy Loading
```python
class PatternWithDependencies:
    def __init__(self):
        self._heavy_resource = None

    @property
    def heavy_resource(self):
        if self._heavy_resource is None:
            self._heavy_resource = load_heavy_resource()
        return self._heavy_resource
```

### Batch Processing
```python
def process_files(files, batch_size=100):
    for i in range(0, len(files), batch_size):
        batch = files[i:i + batch_size]
        process_batch(batch)
```

## Documentation Requirements

Each pattern should include:

1. **Docstring** with purpose and usage
2. **Parameter descriptions** with types
3. **Return value documentation**
4. **Example usage** in docstring or README
5. **Performance characteristics** if relevant

Example:
```python
def cleanup_pattern(path: Path = Path('.'), dry_run: bool = True) -> dict:
    """
    Clean temporary files and caches from project.

    Args:
        path: Project root path (default: current directory)
        dry_run: If True, show what would be cleaned without deleting

    Returns:
        Dictionary with:
        - success: Operation success status
        - files_cleaned: Number of files removed
        - space_recovered: Bytes freed
        - execution_time: Time taken in seconds

    Example:
        >>> result = cleanup_pattern(dry_run=False)
        >>> print(f"Cleaned {result['files_cleaned']} files")

    Performance: O(n) where n is number of files
    Typical execution: <0.5 seconds for typical project
    """
```

## Version Compatibility

Patterns should maintain backward compatibility:

```python
def pattern_v2(new_param=None, **kwargs):
    """V2 with new parameter, backward compatible."""
    # Support old calling convention
    if 'old_param' in kwargs:
        new_param = transform_old_to_new(kwargs['old_param'])

    # New logic here
```

## Security Considerations

1. **Never expose secrets** in logs or outputs
2. **Validate inputs** to prevent injection attacks
3. **Use safe file operations** (avoid shell=True)
4. **Respect .gitignore** when scanning files
5. **Sanitize data** before sharing publicly

## Summary Checklist

Before releasing a pattern, ensure:

- [ ] Has clear entry point (main() or run())
- [ ] Returns structured dictionary with 'success' key
- [ ] Completes in <2 seconds
- [ ] Supports dry-run mode (if destructive)
- [ ] Has comprehensive error handling
- [ ] Includes unit tests
- [ ] Has complete documentation
- [ ] Works standalone and composed
- [ ] Maintains backward compatibility
- [ ] Follows security best practices

---

*Following these practices ensures AGET patterns are reliable, fast, and safe for all users.*