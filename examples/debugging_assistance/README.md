# Debugging Assistance Example

Demonstrates the `debug_assist.py` pattern for error analysis and root cause investigation.

## Files

- `error_scenario.py` - Sample code that triggers `TypeError: 'NoneType' object is not subscriptable`
- `run_debug.py` - Script that analyzes the error using debug_assist pattern

## Usage

```bash
cd examples/debugging_assistance

# Run the buggy code to see the error
python3 error_scenario.py

# Run the debugging analysis
python3 run_debug.py
```

## Expected Output

The analysis provides:

1. **Error Pattern Classification**: Identifies as "null_pointer_exception" (Python equivalent)
2. **Root Cause Hypotheses**: Ranked by confidence
   - Hypothesis 1 (high confidence): Object is None, no null check
   - Hypothesis 2 (medium confidence): Object not loaded properly
3. **Fix Strategies**: Code examples for each hypothesis
4. **Investigation Path**: Step-by-step debugging guide
5. **Prevention Tips**: How to avoid in future

## Error Pattern Library

The pattern recognizes common errors:

- **null_pointer_exception**: AttributeError with 'NoneType'
- **missing_dict_key**: KeyError
- **list_index_out_of_range**: IndexError
- **calling_non_function**: TypeError "not callable"
- **missing_function_argument**: TypeError "missing argument"
- **import_error**: ImportError/ModuleNotFoundError
- **async_await_missing**: RuntimeError "coroutine never awaited"

## Learning Points

- Error patterns help categorize and understand common bugs
- Ranked hypotheses focus investigation on most likely causes
- Fix strategies provide concrete code examples
- Investigation paths give step-by-step debugging approach
- Prevention tips help avoid similar bugs in future
