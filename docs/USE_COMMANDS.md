# AGET Apply Command

The `aget apply` command applies reusable patterns to your project, automating common workflows and configurations.

## Usage

```bash
# List all available patterns
aget apply

# Apply a specific pattern
aget apply <category>/<pattern>

# Examples
aget apply session/wake
aget apply housekeeping/cleanup
aget apply bridge/extract_output
```

## Available Patterns

### Session Patterns

#### session/wake
Starts an agent session with comprehensive project status.

**What it does:**
- Shows last session time and session number
- Checks git repository status
- Detects available patterns
- Counts test files
- Creates/updates `.session_state.json`

**Usage:**
```bash
aget apply session/wake
```

#### session/wind_down
Gracefully ends a work session with automatic saving.

**What it does:**
- Commits uncommitted changes
- Creates session notes in `SESSION_NOTES/`
- Runs available tests
- Updates session state

**Usage:**
```bash
aget apply session/wind_down
```

#### session/sign_off
Quick save and exit without prompts.

**What it does:**
- Quick commits any changes
- Attempts to push to remote
- Minimal output for fast exit

**Usage:**
```bash
aget apply session/sign_off
```

### Housekeeping Patterns

#### housekeeping/cleanup
Removes temporary files, caches, and build artifacts.

**What it does:**
- Cleans Python artifacts (`__pycache__`, `.pyc`, `.egg-info`)
- Removes JavaScript artifacts (`node_modules`, build dirs)
- Cleans general temp files (`.DS_Store`, `.bak`, `.tmp`)
- Shows space to be freed
- Supports dry-run mode by default

**Usage:**
```bash
# Dry run (default) - shows what would be cleaned
aget apply housekeeping/cleanup

# Actually clean (when pattern is updated)
aget apply housekeeping/cleanup --no-dry-run
```

#### housekeeping/doc_check
Assesses documentation quality and completeness.

**What it does:**
- Checks for README, LICENSE, CONTRIBUTING, CHANGELOG
- Analyzes README quality (sections, examples, length)
- Grades documentation A-F
- Provides specific recommendations

**Usage:**
```bash
aget apply housekeeping/doc_check
```

**Example output:**
```
📚 Documentation Check
----------------------------------------

Grade: B (82/100)

✅ Found Documentation:
  - README: README.md
  - LICENSE: LICENSE
  - docs_directory: docs
  - code_documentation: 75%

❌ Missing Documentation:
  - CONTRIBUTING

💡 Recommendations:
  ⚖️ Add a CONTRIBUTING.md file
  📚 Add missing README sections (api)
```

### Bridge Patterns

#### bridge/extract_output
Transforms agent outputs into public products.

**What it does:**
- Scans `outputs/` directory for valuable content
- Calculates value scores based on size, recency, documentation
- Prepares outputs for extraction as public Outputs
- Creates extraction manifests for traceability

**Usage:**
```bash
aget apply bridge/extract_output
```

**Example output:**
```
🌉 Bridge Pattern: Output Extraction
----------------------------------------
Found 3 candidate outputs:

1. cost_analyzer.py (tools)
   Path: outputs/cost_analyzer.py
   Value Score: 80

2. data_processor.js (tools)
   Path: outputs/data_processor.js
   Value Score: 55

Use `aget extract <output_path>` to extract an output as a public Output.
```

### Meta Patterns

#### meta/project_scanner
Scans projects for AGET migration readiness.

**What it does:**
- Analyzes project structure
- Checks for existing agent configurations
- Assesses migration complexity
- Generates readiness report

**Usage:**
```bash
aget apply meta/project_scanner
```

## Pattern Development

To create a new pattern:

1. Create pattern file in `patterns/<category>/<pattern_name>.py`
2. Implement `apply_pattern(project_path)` function
3. Add docstring describing the pattern
4. Create tests in `tests/test_<pattern_name>.py`

### Pattern Template

```python
#!/usr/bin/env python3
"""
My Pattern - Brief description of what this pattern does.
"""

from pathlib import Path
from typing import Dict, Any

def apply_pattern(project_path: Path = Path.cwd()) -> Dict[str, Any]:
    """
    Apply my pattern to project.

    This is called by `aget apply category/my_pattern`.
    """
    # Pattern implementation
    result = {
        'success': True,
        'message': 'Pattern applied successfully'
    }

    # Do pattern work here
    print("🎯 Applying my pattern...")

    return result

if __name__ == "__main__":
    apply_pattern()
```

## Performance Requirements

All patterns must:
- Complete execution in <2 seconds
- Provide immediate user feedback
- Handle errors gracefully
- Return structured results

## Integration with AGENTS.md

Patterns can be triggered through natural language in AGENTS.md:

```markdown
# AGENTS.md

## Session Management

When user says "wake up":
- Run `aget apply session/wake`

When user says "clean up":
- Run `aget apply housekeeping/cleanup`
```

This allows AI agents to discover and use patterns automatically.

## Future Enhancements

Planned features for `aget apply`:
- Pattern parameters: `aget apply pattern --option value`
- Pattern composition: `aget apply pattern1,pattern2`
- Custom pattern directories: `aget apply --pattern-dir ./my-patterns`
- Pattern marketplace: `aget apply --from-registry pattern`

---

*The `aget apply` command is central to AGET v2's pattern-based architecture, enabling reusable workflows across projects.*