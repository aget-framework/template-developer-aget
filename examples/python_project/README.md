# Example: Python Project with CLI Agent Template

This example shows a typical Python project using the standard template.

## Project Structure

```
my-python-project/
├── CLAUDE.md           # CLI agent configuration
├── Makefile            # Command shortcuts
├── requirements.txt    # Python dependencies
├── scripts/
│   ├── session_protocol.py
│   └── housekeeping_protocol.py
├── src/
│   └── my_module/
│       └── __init__.py
├── tests/
│   └── test_my_module.py
└── docs/
    └── README.md
```

## Installation

```bash
# From the cli-agent-template root directory
python installer/install.py ../my-python-project --template standard
```

## Usage with CLI Agent

```
You: wake up
Agent: [Shows project status, git info, test results]

You: Let's add a new feature to calculate fibonacci
Agent: [Creates new function with tests]

You: run tests
Agent: [Runs pytest, shows results]

You: documentation check
Agent: [Analyzes docs, gives grade B, suggests improvements]

You: wind down
Agent: [Commits changes, saves session notes, runs final tests]
```

## Real-World Benefits

1. **Consistent Workflow** - Same commands work across all projects
2. **No Context Loss** - Session notes preserve what you worked on
3. **Safety First** - Dry-run by default, git checkpoints
4. **Quality Maintenance** - Automatic documentation and test checks