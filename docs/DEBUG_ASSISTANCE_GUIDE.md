# Debugging Assistance Guide

**Template**: template-developer-aget v2.7.0
**Pattern**: `.aget/patterns/analysis/debug_assist.py`
**Purpose**: Error analysis with root cause hypotheses and fix strategies

---

## Overview

Debugging assistance provides:
- **Error Pattern Recognition**: Classify errors into known categories
- **Root Cause Analysis**: Ranked hypotheses with confidence levels
- **Fix Strategies**: Concrete code examples for each hypothesis
- **Investigation Paths**: Step-by-step debugging guide
- **Similar Error Detection**: Find related issues in codebase

**Output**: Structured analysis with actionable next steps

---

## Usage

### Basic Error Analysis
```bash
# Analyze error with stack trace
python3 .aget/patterns/analysis/debug_assist.py \
  --error-type "AttributeError" \
  --error-message "'NoneType' object has no attribute 'split'" \
  --stack-trace error_trace.txt \
  --code-file src/app.py

# Analyze with code context
python3 .aget/patterns/analysis/debug_assist.py \
  --error-type "KeyError" \
  --error-message "'email'" \
  --code-context "{'name': 'John', 'age': 30}"
```

### Interactive Use
```
User: "I'm getting AttributeError: 'NoneType' object has no attribute 'split' on line 42 of app.py"

Advisor:
1. Analyzes error pattern (null pointer exception)
2. Generates root cause hypotheses (ranked)
3. Provides fix strategies with code examples
4. Suggests investigation path
5. Searches codebase for similar errors
```

---

## Output Format

### Report Structure
```
Debug Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Error: AttributeError: 'NoneType' object has no attribute 'split'

Pattern: Null pointer exception
Confidence: High

Root Cause Hypotheses (ranked):
1. High confidence: user.email is None (database allows null)
   - Evidence: Line 42 calls user.email.split('@')
   - Fix: Add null check before split()

2. Medium confidence: user object not loaded properly
   - Evidence: No explicit null check in User.get()
   - Fix: Validate user exists before accessing attributes

Recommended Investigation Path:
1. Add print(user.email) before line 42
2. Check database for users with null email
3. Add validation in User model

Fix Strategy (Hypothesis 1):
```python
# Before (buggy)
email_parts = user.email.split('@')

# After (fixed)
if user.email:
    email_parts = user.email.split('@')
else:
    raise ValueError('User email is required')
```
```

### JSON Output
```json
{
  "status": "success",
  "error_pattern": "null_pointer_exception",
  "confidence": "high",
  "root_cause_hypotheses": [
    {
      "rank": 1,
      "confidence": "high",
      "cause": "user.email is None",
      "evidence": [...],
      "fix_strategy": "if user.email:\n    email_parts = user.email.split('@')",
      "prevention": "Add database constraint: email NOT NULL"
    }
  ],
  "investigation_path": [...],
  "similar_errors": [...],
  "recommendations": [...]
}
```

---

## Error Pattern Library

### 1. Null Pointer Exception

**Signature**: `AttributeError: 'NoneType' object has no attribute 'X'`

**Common Causes**:
- Database field allows NULL
- Object not loaded/initialized
- Function returns None on error (without explicit check)

**Example**:
```python
# Bug
user = get_user(user_id)
email = user.email.lower()  # Crashes if user.email is None

# Fix
user = get_user(user_id)
if user and user.email:
    email = user.email.lower()
else:
    raise ValueError('User or email not found')
```

**Prevention**:
- Database constraints: `NOT NULL` where appropriate
- Type hints: `Optional[str]` signals nullability
- Validation in data access layer

---

### 2. Missing Dictionary Key

**Signature**: `KeyError: 'key_name'`

**Common Causes**:
- API response missing expected field
- Configuration incomplete
- Typo in key name

**Example**:
```python
# Bug
user_data = {'name': 'John', 'age': 30}
email = user_data['email']  # KeyError if 'email' not present

# Fix (Option 1: Default value)
email = user_data.get('email', 'unknown@example.com')

# Fix (Option 2: Explicit check)
if 'email' in user_data:
    email = user_data['email']
else:
    raise ValueError('Email required in user data')
```

**Prevention**:
- Use `.get()` with defaults for optional fields
- Validate required fields at boundary (API input, file load)
- Schema validation libraries (Pydantic, marshmallow)

---

### 3. List Index Out of Range

**Signature**: `IndexError: list index out of range`

**Common Causes**:
- Empty list
- Off-by-one error
- Assuming list length without checking

**Example**:
```python
# Bug
parts = data.split(',')
first = parts[0]
second = parts[1]  # IndexError if only 1 part

# Fix
parts = data.split(',')
if len(parts) >= 2:
    first, second = parts[0], parts[1]
else:
    raise ValueError(f'Expected 2 parts, got {len(parts)}')
```

**Prevention**:
- Check `len(list)` before accessing indices
- Use slicing with defaults: `parts[1:2]` or `parts[1] if len(parts) > 1 else None`
- Iterator patterns instead of indexing

---

### 4. Calling Non-Function

**Signature**: `TypeError: 'X' object is not callable`

**Common Causes**:
- Variable shadowing function name
- Missing parentheses in function definition
- Typo (wrote `result()` instead of `result`)

**Example**:
```python
# Bug
def get_data():
    return [1, 2, 3]

data = get_data()  # Now 'data' is a list, not a function
# ... later in code ...
data = data()  # TypeError: 'list' object is not callable

# Fix
def get_data():
    return [1, 2, 3]

result = get_data()  # Use different variable name
```

**Prevention**:
- Avoid variable names that match function names
- Use descriptive variable names (`user_list`, not `users()`)
- Type hints to catch misuse

---

### 5. Unhandled Exception in Async Code

**Signature**: `RuntimeError: coroutine 'func' was never awaited`

**Common Causes**:
- Forgot `await` keyword
- Calling async function from sync context
- Missing `asyncio.run()`

**Example**:
```python
# Bug
async def fetch_data():
    return await api_call()

result = fetch_data()  # RuntimeError (forgot await)

# Fix (Option 1: In async context)
async def main():
    result = await fetch_data()

# Fix (Option 2: From sync context)
import asyncio
result = asyncio.run(fetch_data())
```

**Prevention**:
- Type hints: Return type `Coroutine[...]` signals async
- Linters: `pylint` detects missing `await`
- Consistent async/await usage throughout call chain

---

## Root Cause Analysis Process

### Step 1: Error Pattern Recognition
```python
def recognize_error_pattern(error_type, error_message):
    """Classify error into known pattern"""
    ERROR_PATTERNS = {
        r"AttributeError.*'NoneType'": "null_pointer_exception",
        r"KeyError": "missing_dict_key",
        r"IndexError": "list_index_out_of_range",
        r"TypeError.*not callable": "calling_non_function",
        # ... more patterns
    }

    for pattern_regex, pattern_name in ERROR_PATTERNS.items():
        if re.match(pattern_regex, f"{error_type}: {error_message}"):
            return pattern_name

    return "unknown_pattern"
```

### Step 2: Hypothesis Generation
```python
def generate_hypotheses(error_pattern, code_context):
    """Create ranked hypotheses based on pattern"""
    hypotheses = []

    if error_pattern == "null_pointer_exception":
        # Hypothesis 1: Variable is None
        variable = extract_variable(error_message)
        hypotheses.append({
            "rank": 1,
            "confidence": "high",
            "cause": f"{variable} is None",
            "evidence": [
                f"Line {line} accesses {variable} without check",
                check_if_field_nullable(variable)
            ],
            "fix_strategy": generate_null_check_fix(variable)
        })

        # Hypothesis 2: Object not loaded
        # ...

    return hypotheses
```

### Step 3: Fix Strategy Generation
```python
def generate_fix_strategy(hypothesis, language="python"):
    """Generate concrete fix code"""
    if "is None" in hypothesis['cause']:
        variable = extract_variable(hypothesis['cause'])

        if language == "python":
            return f"""if {variable}:
    # existing code
else:
    # handle null case (raise error or use default)"""

    # More fix patterns...
```

---

## Investigation Paths

### Null Pointer Exception Path
```
1. Confirm value is None
   → Add: print(variable_name) before error line

2. Identify source of None
   → Check database: SELECT * WHERE field IS NULL
   → Check function: Does it return None on error?

3. Determine correct fix location
   → At source (database constraint, function validation)
   → Or at usage (null check before access)

4. Implement prevention
   → Add validation/constraints
   → Update type hints (Optional[T])
```

### Missing Dictionary Key Path
```
1. Confirm key is missing
   → Print: print(dict_name.keys())

2. Identify why key is missing
   → API change? (check API docs)
   → Typo? (compare expected vs actual keys)
   → Optional field? (check schema)

3. Choose fix approach
   → Required field: Validate at input
   → Optional field: Use .get() with default

4. Implement validation
   → Schema validation (Pydantic)
   → Or explicit checks
```

---

## Concrete Example: AttributeError

### Input
```python
# error_scenario.py
class User:
    def __init__(self, name, email=None):
        self.name = name
        self.email = email

def process_email(user_id):
    user = get_user(user_id)
    email_parts = user.email.split('@')  # Line 12 - Bug here
    return email_parts

def get_user(user_id):
    return User(name="Test", email=None)
```

**Stack Trace**:
```
Traceback (most recent call last):
  File "error_scenario.py", line 20, in <module>
    process_email(123)
  File "error_scenario.py", line 12, in process_email
    email_parts = user.email.split('@')
AttributeError: 'NoneType' object has no attribute 'split'
```

---

### Analysis Output

**Error Pattern**: null_pointer_exception (high confidence)

**Root Cause Hypotheses**:

**Hypothesis 1** (High confidence):
- **Cause**: `user.email` is None (User model allows null email)
- **Evidence**:
  - Line 12 calls `user.email.split('@')` without null check
  - User class initializes `email=None` by default
  - `get_user()` returns User with `email=None`
- **Fix Strategy**:
  ```python
  if user.email:
      email_parts = user.email.split('@')
  else:
      raise ValueError('User email is required')
  ```
- **Prevention**: Enforce email as required in User model or add validation in `get_user()`

**Hypothesis 2** (Medium confidence):
- **Cause**: `user` object not loaded properly
- **Evidence**: `get_user()` doesn't validate user has email before returning
- **Fix Strategy**:
  ```python
  def get_user(user_id):
      user = fetch_user(user_id)
      if not user.email:
          raise ValueError(f'User {user_id} has no email')
      return user
  ```

---

### Investigation Path
```
1. Confirm user.email is None
   → Add: print(f"user.email = {user.email}") before line 12

2. Check if other users have this issue
   → Database: SELECT COUNT(*) FROM users WHERE email IS NULL

3. Review User model
   → Is email field required? (Currently: No)
   → Should it be? (Depends on requirements)

4. Check get_user() method
   → Does it validate email exists? (Currently: No)
   → Should it? (Yes, if email is always required)
```

---

### Similar Errors
After fixing this error, search codebase for similar patterns:
```bash
# Find all .split() calls
grep -rn "\.split(" src/

# Check each for null safety
# Review: Does variable need null check before .split()?
```

---

## Integration with Workflows

### Paste Stack Trace to Advisor
```
User: [pastes stack trace]

Traceback (most recent call last):
  File "app.py", line 42, in process_data
    result = data['config']['timeout']
KeyError: 'timeout'

Advisor:
[Analyzes error]
Error Pattern: missing_dict_key

Root Cause: 'timeout' key missing from config dict
Fix: Use data.get('config', {}).get('timeout', 30)

Investigation:
1. Check config file for 'timeout' field
2. Determine if timeout is required or optional
3. Add default value if optional, validation if required
```

---

### Pre-Implementation Bug Prevention
```
User: "I'm about to add user.profile.avatar.url to the template. Any risks?"

Advisor:
⚠️  Potential null pointer exception

Hypotheses:
- user could be None
- user.profile could be None
- user.profile.avatar could be None

Recommendation:
```python
# Safe access pattern
avatar_url = None
if user and user.profile and user.profile.avatar:
    avatar_url = user.profile.avatar.url
else:
    avatar_url = '/static/default_avatar.png'
```
```

---

## Troubleshooting

### "Pattern not recognized"
**Cause**: Error not in built-in pattern library

**Fix**: Provide more context
```bash
python3 .aget/patterns/analysis/debug_assist.py \
  --error-type "CustomException" \
  --error-message "Business rule violated" \
  --stack-trace trace.txt \
  --code-file src/business.py \
  --code-context "Additional context about what code does"
```

---

### "Low confidence hypotheses"
**Cause**: Insufficient code context

**Fix**: Provide more files
```bash
# Include related files
python3 .aget/patterns/analysis/debug_assist.py \
  --error-type "AttributeError" \
  --error-message "..." \
  --code-file src/app.py \
  --related-files src/models.py,src/database.py
```

---

## Related Guides

- **Code Quality**: `docs/CODE_QUALITY_GUIDE.md`
- **Standards Checking**: `docs/STANDARDS_CHECKING_GUIDE.md`
- **Pattern Library**: `.aget/patterns/analysis/debug_assist.py`

---

*Generated for template-developer-aget v2.7.0*
