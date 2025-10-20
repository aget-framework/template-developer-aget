"""
Agent-assisted migration command for AGET v2.
Designed to be run by CLI coding agents who can make intelligent decisions.
"""

from pathlib import Path
from typing import Any, Dict, List

from aget.base import BaseCommand


class MigrateCommand(BaseCommand):
    """Intelligent migration guided by CLI agent."""

    def execute(self, args: List[str]) -> Dict[str, Any]:
        """Execute migration with agent guidance."""
        if '--help' in args or not args:
            return self.show_help()

        project_path = Path(args[0]) if args else Path.cwd()

        # Generate migration instructions for the agent
        instructions = self.generate_agent_instructions(project_path)

        return {
            'success': True,
            'message': instructions,
            'requires_agent': True
        }

    def generate_agent_instructions(self, project_path: Path) -> str:
        """Generate instructions for the CLI agent to perform migration."""

        return f"""
# AGET Migration Instructions for CLI Agent

You are about to migrate {project_path.name} to AGET v2. Follow these steps:

## 1. Analyze Existing Configuration
Read the existing CLAUDE.md, AGENTS.md, or README.md files and identify:
- Project name and purpose
- Custom workflows or commands
- Important context or principles
- Current state or features
- Any project-specific instructions

## 2. Determine Project Type
Based on your analysis, determine if this is:
- **agent**: Autonomous agent with workspace/products split
- **tool**: Traditional tool/library
- **hybrid**: Both agent and tool capabilities
- **minimal**: Just basic configuration

## 3. Create Merged Configuration
Create a new AGENTS.md that includes:

### From Original (Preserve):
- Project overview/description
- Custom commands or workflows
- Domain-specific context
- Important notes or warnings
- Current state or features

### From AGET (Add):
```markdown
## Session Management Protocols

### Wake Up Protocol
When user says "wake up" or "hey":
- Show current directory and status
- Check git status
- Report readiness

### Wind Down Protocol
When user says "wind down" or "save work":
- Commit changes
- Create session notes
- Show completion

### Sign Off Protocol
When user says "sign off" or "all done":
- Quick save and exit
- No questions

## Housekeeping Protocols

### Tidy Up
When user says "tidy up" or "housekeeping":
- Clean temp files and caches
- Show space freed

### Check Documentation
When user says "check docs":
- Analyze documentation quality
- Report issues

### Health Check
When user says "health check" or "sanity check":
- Check system status
- Report any issues

## Directory Structure
[Explain actual structure based on project]

## Vocabulary Note
- `workspace/` = Private workspace for exploration
- `products/` = Public products for distribution
```

## 4. Organize Files
Based on project type, move files to appropriate directories:
- Analysis/exploration scripts → workspace/
- Public libraries/tools → products/
- Source code → src/
- Tests → tests/
- Documentation → docs/

## 5. Create Universal Configs
Ensure all these files exist with same content:
- AGENTS.md (primary)
- CLAUDE.md (symlink or copy)
- .cursorrules (copy)
- If needed: .aider.conf.yml

## 6. Validate Migration
Check that:
- [ ] Project context is preserved
- [ ] AGET protocols are added
- [ ] Directory structure makes sense
- [ ] All config files are synchronized
- [ ] Tests still pass

## 7. Create Migration Report
Document what was:
- Preserved from original
- Added from AGET
- Moved or reorganized
- Any issues or warnings

## Agent Decision Points

At each step, use your judgment to:
1. **Preserve valuable project documentation** - Don't lose context!
2. **Add AGET capabilities** - Enable new commands
3. **Organize sensibly** - workspace/ vs products/ based on purpose
4. **Maintain compatibility** - Ensure existing workflows still work

## Example Merging Decision

If you see:
```
## Project Overview
A Spotify data analysis toolkit for personal music insights.

## Commands
- Run analysis: python analyze.py
```

Keep this and add AGET protocols after it. The result has both!

---

Remember: You're not replacing, you're enhancing. When in doubt, preserve and add rather than replace.
"""

    def show_help(self) -> Dict[str, Any]:
        """Show help for migrate command."""
        return {
            'success': True,
            'message': """aget migrate - Intelligent project migration to AGET v2

Usage:
  aget migrate [path]    # Migrate project at path
  aget migrate          # Migrate current directory

This command provides instructions for CLI agents to perform
intelligent migration that preserves custom content while adding
AGET capabilities.

The agent will:
1. Analyze existing configuration
2. Preserve custom content
3. Add AGET protocols
4. Organize files appropriately
5. Create universal configs

Example:
  aget migrate ../my-project
"""
        }

    def tier_basic(self, **kwargs) -> Dict[str, Any]:
        """Basic tier implementation."""
        args = kwargs.get('args', [])
        return self.execute(args)