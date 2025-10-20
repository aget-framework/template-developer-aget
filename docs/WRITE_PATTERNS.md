# Understanding Patterns in CLI Agent Templates

## What Are Patterns?

**Patterns are reusable command workflows that teach your CLI agent specialized behaviors.**

Think of patterns as "skill modules" that your agent can learn. When you say a trigger phrase like "wake up" or "housekeeping", your agent executes a specific pattern that handles that task consistently every time.

## Why Patterns Matter

Without patterns, every interaction with your CLI agent starts from scratch:
- You explain what you want
- The agent asks clarifying questions
- You provide more details
- Eventually the task gets done (hopefully correctly)

With patterns, interactions become predictable:
- You say the trigger phrase
- The agent immediately knows exactly what to do
- The task completes the same way every time

## Pattern Architecture

```
patterns/
├── session/                 # Session management patterns
│   ├── wake_up.py          # Start working on project
│   ├── wind_down.py        # Save progress and notes
│   └── sign_off.py         # Quick commit and push
├── housekeeping/           # Maintenance patterns
│   ├── clean.py           # Remove temp files
│   ├── organize.py        # Sort project structure
│   └── archive.py         # Archive old files
└── documentation/          # Documentation patterns
    ├── check.py           # Verify docs quality
    └── update.py          # Update documentation
```

## How Patterns Work

### 1. Trigger Recognition
Your AGENT.md file defines trigger phrases:
```markdown
### Start Session (Wake Up Protocol)
When user says "hey" or "wake up", execute:
- Run: `python3 scripts/aget_session_protocol.py wake`
```

### 2. Pattern Execution
When triggered, the pattern:
1. Reads current context (working directory, git status, etc.)
2. Performs its specialized task
3. Reports results in a consistent format
4. Updates state for next time

### 3. Pattern Composition
Patterns can build on each other:
```python
# wind_down pattern calls multiple sub-patterns
def wind_down():
    run_tests()        # Test pattern
    commit_changes()   # Git pattern
    create_notes()     # Documentation pattern
    update_metrics()   # Metrics pattern
```

## Core Pattern Categories

### Session Patterns
Manage your working context across agent sessions:
- **wake_up**: Load context, show status, prepare workspace
- **wind_down**: Save work, create session notes, run tests
- **sign_off**: Quick save and push changes

### Housekeeping Patterns
Keep your project clean and organized:
- **housekeeping**: Light cleanup of temp files
- **spring_clean**: Deep cleanup with archiving
- **sanity_check**: Diagnose and fix problems

### Documentation Patterns
Maintain project documentation:
- **documentation_check**: Grade documentation quality
- **update_docs**: Refresh documentation
- **generate_readme**: Create README from code

### Recovery Patterns
Fix problems when things go wrong:
- **emergency_recovery**: Restore from backup
- **fix_permissions**: Repair file permissions
- **rollback**: Undo recent changes

## Creating Custom Patterns

### Simple Pattern Example
```python
# patterns/custom/deploy.py
def deploy_to_staging():
    """Deploy current branch to staging environment"""
    print("🚀 Deploying to staging...")

    # Check prerequisites
    if not check_tests_pass():
        print("❌ Tests must pass before deploy")
        return False

    # Run deployment
    run_command("npm run build")
    run_command("npm run deploy:staging")

    print("✅ Deployed successfully")
    return True
```

### Adding to AGENT.md
```markdown
### Deploy to Staging
When user says "deploy staging", execute:
- Run: `python3 patterns/custom/deploy.py staging`
- Reports deployment status
- Rolls back on failure
```

## Pattern Best Practices

### 1. Idempotent Operations
Patterns should be safe to run multiple times:
```python
# Good: Check before acting
if not os.path.exists(".git"):
    subprocess.run(["git", "init"])

# Bad: Assumes state
subprocess.run(["git", "init"])  # Fails if already exists
```

### 2. Dry-Run by Default
Destructive operations should preview first:
```python
def clean_files(dry_run=True):
    files_to_remove = find_temp_files()

    if dry_run:
        print(f"Would remove {len(files_to_remove)} files")
        return

    # Actually remove files
    for file in files_to_remove:
        os.remove(file)
```

### 3. Clear Status Reporting
Use consistent output formats:
```python
# Consistent status indicators
print("✅ Task completed successfully")
print("⚠️  Warning: Check needed")
print("❌ Error: Task failed")
print("ℹ️  Info: Additional context")
```

### 4. State Persistence
Save context between runs:
```python
import json

def save_state(data):
    with open(".pattern_state.json", "w") as f:
        json.dump(data, f)

def load_state():
    try:
        with open(".pattern_state.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
```

## Pattern Templates

The CLI Agent Template provides three template levels:

### Minimal Template
- Basic session patterns only
- Perfect for small projects
- ~5 patterns included

### Standard Template (Recommended)
- Full pattern suite
- Housekeeping and documentation
- ~15 patterns included

### Advanced Template
- Everything including CI/CD patterns
- Deployment and monitoring
- ~25+ patterns included

## How Patterns Are Discovered

When you say "wake up", the session pattern:
1. Scans the `patterns/` directory
2. Lists available pattern categories
3. Reports them in the status output

```
📦 Patterns available: session, housekeeping, documentation, recovery
```

This helps you remember what commands are available without checking documentation.

## Pattern Evolution

Patterns evolve through usage:

### Phase 1: Manual Commands
You type specific commands repeatedly

### Phase 2: Script Creation
You create a script to automate the commands

### Phase 3: Pattern Integration
You turn the script into a reusable pattern

### Phase 4: Community Sharing
You share your pattern for others to use

## Troubleshooting Patterns

### Pattern Not Triggering
1. Check AGENT.md has the trigger phrase
2. Verify pattern file exists and is executable
3. Test running the pattern directly

### Pattern Failing
1. Run with verbose output: `--verbose` flag
2. Check prerequisites are met
3. Review pattern logs in SESSION_NOTES/

### Pattern Conflicts
1. Ensure unique trigger phrases
2. Check pattern dependencies
3. Verify no circular imports

## Next Steps

1. **Explore existing patterns**: Look in `patterns/` directory
2. **Create a custom pattern**: Start with a simple automation
3. **Share your patterns**: Contribute back to the community
4. **Read pattern source code**: Learn from implementation

Remember: Patterns are just Python scripts that follow conventions. You can create any pattern you need for your workflow!