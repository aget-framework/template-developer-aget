# Quick Start Guide

**Get your CLI coding agent up and running in under 5 minutes** 🚀

This guide will help you install and use the CLI Agent Template to transform your codebase into a conversational development environment. By the end, you'll have AI agents that understand commands like "hey", "tidy up", and "save work".

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** - Check with: `python3 --version`
- **Git** (recommended) - Check with: `git --version`
- **A CLI coding agent** - Claude Code, Cursor, Aider, or similar
- **5 minutes** - That's all you need!
- **macOS or Linux** - Windows support via WSL

> 💡 **New to CLI agents?** These are AI assistants that can read your code and execute commands. Popular options include [Claude Code](https://claude.ai/code), [Cursor](https://cursor.sh), and [Aider](https://aider.chat).

## Installation

### Option 1: Interactive Install (Recommended for First-Time Users)

Run the installer without any arguments for a guided experience:

```bash
curl -sSL https://raw.githubusercontent.com/gmelli/aget-cli-agent-template/main/install.sh | bash
```

The interactive installer will:
- ✅ Check prerequisites automatically
- ✅ Let you choose your installation directory
- ✅ Help you select the right template
- ✅ Confirm before making changes

### Option 2: Quick Install (One Command)

For experienced users who want the standard template immediately:

```bash
# Install in current directory
curl -sSL https://raw.githubusercontent.com/gmelli/aget-cli-agent-template/main/install.sh | bash -s . standard

# Or install in a specific directory
curl -sSL https://raw.githubusercontent.com/gmelli/aget-cli-agent-template/main/install.sh | bash -s ~/myproject standard
```

### Option 3: Clone and Customize

For developers who want to modify the templates:

```bash
# Clone the repository
git clone https://github.com/gmelli/aget-cli-agent-template
cd aget-cli-agent-template

# Run interactive installer
./install.sh

# Or specify options
./install.sh --prefix ~/myproject --template standard
```

### Verify Installation

After installation, verify everything is working:

```bash
# Check that files were installed
ls -la AGENTS.md scripts/

# Test the session protocol
python3 scripts/aget_session_protocol.py status

# Expected output:
# ✅ Session state initialized
# Ready for commands
```

## Your First Session (5-Minute Tutorial)

Let's walk through a complete workflow with your newly empowered CLI agent:

### Step 1: Open Your CLI Agent

Launch your preferred CLI coding assistant (Claude Code, Cursor, etc.) in the project directory where you installed the templates.

### Step 2: Wake Up the Agent

Tell your agent:
```
hey
```

**What happens:** The agent reads AGENTS.md, checks your project status, shows recent changes, and prepares for work.

**Expected output:**
```
## Status Report
📅 Last session: 2 hours ago
📍 Working directory: /Users/you/myproject
🔄 Git status: 3 uncommitted changes
✅ Ready for tasks.
```

### Step 3: Check Project Health

Tell your agent:
```
health check
```

**What happens:** Runs diagnostics to ensure Python, Git, and dependencies are properly configured.

**Expected output:**
```
Running emergency diagnostics...
✅ Python 3.11.0
✅ Git repository OK
✅ Critical files present
System Status: OK
```

### Step 4: Clean Up

Tell your agent:
```
tidy up
```

**What happens:** Identifies and optionally removes temporary files, caches, and other clutter.

**Expected output:**
```
Found items to clean:
  • 42 __pycache__ files (2.1 MB)
  • 5 .DS_Store files
  • 3 old log files

Clean these files? [y/N]:
```

### Step 5: End Your Session

Tell your agent:
```
save work
```

**What happens:** Commits changes, creates session notes, and preserves your work context.

**Expected output:**
```
Creating session notes...
Committing changes...
Session preserved.
```

## Understanding What Was Installed

After installation, your project has these new files:

```
your-project/
├── AGENTS.md                     # Universal agent configuration
├── CLAUDE.md                     # Symlink for backward compatibility
├── scripts/
│   ├── session_protocol.py       # Session management (wake/wind/sign-off)
│   ├── housekeeping_protocol.py  # Cleaning and diagnostics
│   └── recovery_protocol.py      # Emergency recovery tools
├── .cli_agent_manifest           # Installation tracking
└── .session_state.json          # Session persistence (auto-created)
```

### Key Files Explained

- **AGENTS.md**: The "brain" - tells agents what commands are available
- **scripts/**: Python scripts that execute the actual commands
- **.session_state.json**: Tracks session history and context

## Choose Your Template

### 🟢 Minimal (5 patterns)
**Best for:** Small projects, learning the system
```bash
./install.sh --template minimal
```
**Includes:** Basic session management only

### 🟡 Standard (15+ patterns) - RECOMMENDED
**Best for:** Most development projects
```bash
./install.sh --template standard
```
**Includes:** Session + housekeeping + documentation tools

### 🔴 Advanced (25+ patterns)
**Best for:** Production projects with CI/CD needs
```bash
./install.sh --template advanced
```
**Includes:** Everything + deployment + testing automation

## Common Commands Reference

Once installed, your CLI agent understands these conversational commands:

| Command | What it does |
|---------|-------------|
| `hey` | Initialize session, show project status |
| `save work` | Save work, commit changes, create notes |
| `all done` | Quick commit and push |
| `tidy up` | Clean temporary files and caches |
| `deep clean` | Deep cleanup with archiving |
| `health check` | Run system diagnostics |
| `check docs` | Analyze documentation quality |

## Troubleshooting

### Installation Issues

<details>
<summary>❌ "Python 3 is not installed"</summary>

Install Python 3.8 or higher:
- **macOS**: `brew install python3`
- **Ubuntu/Debian**: `sudo apt-get install python3`
- **Other**: Visit [python.org](https://python.org)
</details>

<details>
<summary>❌ "Permission denied"</summary>

The installer needs write access to the target directory:
```bash
# Check permissions
ls -la /path/to/target

# Fix if needed
chmod 755 /path/to/target
```
</details>

<details>
<summary>❌ "Command not found: curl"</summary>

Install curl or use wget:
```bash
# Using wget instead
wget -qO- https://raw.githubusercontent.com/gabormelli/aget-cli-agent-template/main/install.sh | bash

# Or install curl
# macOS: brew install curl
# Linux: sudo apt-get install curl
```
</details>

### Runtime Issues

<details>
<summary>⚠️ Agent doesn't understand commands</summary>

Make sure your agent reads the AGENTS.md file:
1. The file must be in the project root
2. Tell the agent explicitly: "Read AGENTS.md"
3. Then try the command again
</details>

<details>
<summary>⚠️ "No module named 'yaml'" error</summary>

Install Python dependencies:
```bash
pip3 install pyyaml gitpython
```
</details>

## Next Steps

Now that you're up and running:

1. **Learn more about patterns** → [PATTERNS_EXPLAINED.md](PATTERNS_EXPLAINED.md)
2. **Understand the why** → [WHY_THIS_MATTERS.md](WHY_THIS_MATTERS.md)
3. **See real examples** → [examples/](../examples/)
4. **Customize for your needs** → [CONTRIBUTING.md](../CONTRIBUTING.md)
5. **Get help** → [GitHub Issues](https://github.com/gabormelli/aget-cli-agent-template/issues)

## Quick Tips

- 🎯 **Start small**: Use the minimal template first, upgrade later
- 🔄 **Regular sessions**: Use "hey" and "save work" to maintain context
- 📝 **Document as you go**: The patterns help maintain good documentation
- 🧹 **Clean regularly**: Run "tidy up" weekly to keep projects tidy
- 🚀 **Experiment**: Try creating your own patterns in the scripts/ directory

---

**Need help?** Open an issue on [GitHub](https://github.com/gabormelli/aget-cli-agent-template/issues) or check our [comprehensive docs](../README.md).

**Ready to contribute?** We welcome improvements! See [CONTRIBUTING.md](../CONTRIBUTING.md).

---
*Making CLI coding agents better collaborators, one pattern at a time.* ✨