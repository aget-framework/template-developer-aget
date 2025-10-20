# Why CLI Agent Templates Matter

## The Problem

When you use CLI coding agents (Claude Code, Cursor, Aider), you repeatedly face:

1. **Context Loss** - "What were we working on yesterday?"
2. **Inconsistent Commands** - Different shortcuts in each project
3. **No Safety Rails** - Accidental deletions, lost work
4. **Manual Repetition** - Same setup tasks every time

## The Solution

CLI Agent Templates provide **conversational infrastructure** that makes agents immediately productive:

### Real Conversation Example

**Without Templates:**
```
You: Help me clean up this project
Agent: What specific files need cleaning? Should I delete __pycache__?
You: Yes, and also old logs
Agent: Which logs are old? What's the cutoff date?
You: [Frustrated typing of specific commands...]
```

**With Templates:**
```
You: tidy up
Agent: Running housekeeping protocol (dry-run)...
       Would remove: 127 __pycache__ files
       Would remove: 23 .pyc files
       Would clean: 3.2MB temp files
       Run with --no-dry-run to execute? (y/n)
```

## Immediate Benefits

### 1. Zero Learning Curve
Your CLI agent already knows:
- `hey` - Start working
- `run tests` - Execute test suite
- `deep clean` - Deep cleanup
- `health check` - Fix problems

### 2. Safety by Default
- **Dry-run first** - See changes before they happen
- **Git checkpoints** - Undo any operation
- **Progressive permissions** - Read → Modify → Delete

### 3. Project Memory
Session notes track:
- What you worked on
- What tests passed/failed
- What documentation needs updating
- Where you left off

## ROI for Developers

### Measurable Time Savings*
- **Context restoration** - Instant project status vs manual review
- **Automated housekeeping** - One command vs multiple manual cleanups
- **Consistent workflows** - Standardized commands across all projects
- **Session continuity** - Pick up exactly where you left off

*Actual savings vary by project size and complexity. These patterns eliminate repetitive manual tasks.

### Quality Improvements
- Documentation stays current (automatic checks)
- Tests run consistently (part of workflow)
- Git history stays clean (conventional commits)
- Codebase stays organized (regular housekeeping)

## Who Benefits Most

1. **Solo Developers** - Personal assistant for routine tasks
2. **Teams** - Standardized workflows across projects
3. **Open Source Maintainers** - Consistent contribution experience
4. **Learning Developers** - Best practices built-in

## Getting Started Takes 1 Minute

```bash
# Install with defaults (standard template)
curl -sSL https://raw.githubusercontent.com/gmelli/aget-cli-agent-template/main/install.sh | bash

# Or choose your template level:
curl -sSL https://raw.githubusercontent.com/gmelli/aget-cli-agent-template/main/install.sh | bash -s . minimal
```

Then just say "hey" to your CLI agent. That's it.