# Session Management Patterns

Patterns for managing development sessions across CLI agent conversations.

## Available Patterns

### wake_up
**Trigger**: "wake up"
**Purpose**: Initialize a new development session
**Actions**:
- Display working directory and git status
- Show recent session history
- List available patterns
- Report test status
- Check documentation grade

### wind_down
**Trigger**: "wind down"
**Purpose**: Gracefully end a development session
**Actions**:
- Commit all changes with descriptive message
- Create session notes with summary
- Run test suite
- Update session metrics
- Archive old session notes (>30 days)

### sign_off
**Trigger**: "sign off"
**Purpose**: Quick save and push
**Actions**:
- Fast commit with timestamp
- Push to remote repository
- Update session state
- No tests or extensive checks

## Usage Examples

```bash
# Start your day
You: wake up
Agent: [Shows project status, recent changes, ready for work]

# Take a break
You: wind down
Agent: [Commits changes, saves notes, runs tests]

# End of day
You: sign off
Agent: [Quick commit and push]
```

## When to Use Each Protocol

### Wind Down vs Sign Off Decision Guide

#### Use `wind down` ONLY when:
- **Taking a short break** (lunch, meeting, will continue soon)
- **Experimental/risky changes** (not ready for team visibility)
- **Incomplete work** (tests failing, feature half-done)
- **Feature branch work** (working privately, not ready to share)
- **No internet connection** (can't push but want to save)

#### Use `wind down` THEN `sign off` when:
- **End of work day** (done for today, work is stable)
- **Completed milestone** (feature done, tests passing)
- **Before extended break** (weekend, vacation, holidays)
- **Switching machines** (need to pull work elsewhere)
- **Important checkpoint** (just fixed difficult bug, don't want to lose it)

#### Use `sign off` ONLY when:
- **Tiny changes** (typo fix, one-line change)
- **Already committed manually** (just need to push)
- **Emergency departure** (need to leave immediately)

### Common Scenarios

| Scenario | Command(s) | Why |
|----------|-----------|-----|
| "Going to lunch" | `wind down` | Will continue after, local save sufficient |
| "Done for the day" | `wind down` → `sign off` | Full backup to remote |
| "Fixed a typo" | `sign off` | Quick push, no need for full process |
| "Risky refactor attempt" | `wind down` | Keep experimental work local |
| "Power outage warning!" | `sign off` | Emergency backup to remote |
| "Weekend starting" | `wind down` → `sign off` | Extended break, need remote backup |
| "Switching to laptop" | `wind down` → `sign off` | Need to pull from other machine |

### Key Differences

| Aspect | wind down | sign off |
|--------|-----------|----------|
| **Commits** | Yes, with detailed message | Yes, with timestamp |
| **Tests** | Runs full test suite | No tests |
| **Session notes** | Creates detailed notes | Minimal notes |
| **Push to remote** | No | Yes |
| **Time taken** | ~30 seconds | ~5 seconds |
| **Use case** | Checkpoint work | Backup work |

## State Management

Session state is persisted in `.session_state.json`:
```json
{
  "session_count": 42,
  "total_commits": 156,
  "last_session_time": "2025-09-21T10:30:00",
  "last_session_end": "2025-09-21T18:45:00",
  "project_created": "2025-09-01T08:00:00"
}
```

## Session Notes

Session notes are organized by date:
```
SESSION_NOTES/
├── 2025-09-21/
│   ├── session_1030.md
│   └── session_1845.md
└── archive/
    └── 2025-08-15/
```

## Customization

Edit `scripts/aget_session_protocol.py` to:
- Add custom status checks
- Modify commit message format
- Change session note template
- Add project-specific commands

## Integration Points

- **Git**: Automatic commits and pushes
- **Testing**: Runs test suite on wind-down
- **Documentation**: Checks documentation quality
- **Metrics**: Tracks session duration and productivity