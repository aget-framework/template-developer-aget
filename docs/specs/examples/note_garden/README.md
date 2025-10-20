# Example: Personal Note Garden

> A complete example showing how to go from idea to working software using specifications

## The Story

**Sarah's Problem**: "I take notes everywhere - meetings, books, podcasts. But I can never find them later. I want a simple tool that helps me connect ideas across all my notes."

**Traditional Approach**: Days of coding, database design, UI frameworks...

**AGET Approach**: 45 minutes from idea to working prototype

## Step 1: Write What You Want (10 minutes)

Sarah creates `FUNCTIONAL_REQUIREMENTS.md`:

```markdown
# Note Garden - Functional Requirements

## Core Features

### FR-001: Capture Notes Quickly
**User Story**: As a busy person, I want to capture thoughts instantly
**Acceptance Criteria**:
- Single command to create note
- Auto-timestamp
- Optional tags
- Works offline

### FR-002: Connect Related Ideas
**User Story**: As a learner, I want to see connections between notes
**Acceptance Criteria**:
- Auto-detect similar topics
- Show related notes when viewing
- Build knowledge graph over time

### FR-003: Rediscover Forgotten Notes
**User Story**: As a forgetful human, I want to resurface old insights
**Acceptance Criteria**:
- Daily "on this day" reminder
- Random note of the day
- Spaced repetition for important notes

### FR-004: Search Everything
**User Story**: As a researcher, I want to find notes by any criteria
**Acceptance Criteria**:
- Full-text search
- Search by date range
- Search by tags
- Search by connections
```

## Step 2: Define the Rules (5 minutes)

Sarah creates `BUSINESS_RULES.md`:

```markdown
# Note Garden - Business Rules

### BR-001: Privacy First
**Rule**: All notes stored locally, never leave device
**Rationale**: Personal thoughts should stay personal

### BR-002: Plain Text Forever
**Rule**: Notes stored as markdown files
**Rationale**: No lock-in, readable in 50 years

### BR-003: Automatic Organization
**Rule**: System organizes notes, user just writes
**Rationale**: Reduce friction, increase capture

### BR-004: Growing Connections
**Rule**: More notes = more connections = more value
**Rationale**: Network effect for personal knowledge
```

## Step 3: Sketch the Data (5 minutes)

Sarah creates `DATA_SPECIFICATIONS.md`:

```markdown
# Note Garden - Data Specifications

## Note Structure
```yaml
id: unique-timestamp-based
title: extracted from first line
content: markdown text
tags: []
created: ISO timestamp
modified: ISO timestamp
connections: [] # IDs of related notes
```

## File Organization
```
notes/
├── 2025/
│   ├── 09/
│   │   ├── 25/
│   │   │   ├── 20250925-140523-meeting-notes.md
│   │   │   └── 20250925-153012-book-quote.md

.note-garden/
├── index.json     # searchable index
├── graph.json     # connection graph
└── config.json    # user preferences
```
```

## Step 4: AI Builds It (20 minutes)

Sarah tells her AI assistant:

> "Build a CLI tool based on these specifications using Python. Make it simple and fast."

The AI generates:

### `note_garden.py` - Core functionality
```python
#!/usr/bin/env python3
"""Note Garden - Personal knowledge management"""

import json
import datetime
from pathlib import Path
from typing import List, Dict

class NoteGarden:
    def __init__(self, base_path: Path = Path.home() / "notes"):
        self.base_path = base_path
        self.index_path = base_path / ".note-garden"
        self._ensure_structure()

    def capture(self, content: str, tags: List[str] = None):
        """FR-001: Capture notes quickly"""
        timestamp = datetime.datetime.now()
        note_id = timestamp.strftime("%Y%m%d-%H%M%S")

        # BR-002: Plain text forever
        note = {
            'id': note_id,
            'title': content.split('\n')[0][:50],
            'content': content,
            'tags': tags or [],
            'created': timestamp.isoformat(),
            'connections': self._find_connections(content)
        }

        # BR-003: Automatic organization
        self._save_note(note)
        self._update_index(note)
        return note_id

    def connect(self, note_id: str):
        """FR-002: Connect related ideas"""
        # Auto-detect similar topics using simple keyword matching
        # (AI made this smarter with TF-IDF)
        pass

    def rediscover(self):
        """FR-003: Rediscover forgotten notes"""
        # Show notes from this day in previous years
        # Return random note for serendipity
        pass

    def search(self, query: str):
        """FR-004: Search everything"""
        # Full-text search across all notes
        # (AI implemented with whoosh or sqlite FTS)
        pass
```

### `cli.py` - Command interface
```python
import click
from note_garden import NoteGarden

@click.group()
def cli():
    """Your personal note garden 🌱"""
    pass

@cli.command()
@click.argument('content')
@click.option('--tags', '-t', multiple=True)
def note(content, tags):
    """Capture a quick note"""
    garden = NoteGarden()
    note_id = garden.capture(content, list(tags))
    click.echo(f"✨ Planted note {note_id}")

@cli.command()
def today():
    """See what you wrote on this day"""
    garden = NoteGarden()
    notes = garden.rediscover()
    for note in notes:
        click.echo(f"📝 {note['title']}")

@cli.command()
@click.argument('query')
def find(query):
    """Search your notes"""
    garden = NoteGarden()
    results = garden.search(query)
    for note in results:
        click.echo(f"🔍 {note['title']}")
```

## Step 5: Use It Immediately (5 minutes)

```bash
# Install
pip install -e .

# Start capturing
note "Just learned about AGET - specs before code!"
note "Meeting with team: decided to use Python" -t work -t python
note "Book: 'Building a Second Brain' - capture everything" -t books

# Rediscover
note today
> 📝 Last year: "Started learning Python"
> 📝 Random insight: "Ideas connect in unexpected ways"

# Search
note find "python"
> 🔍 Meeting with team: decided to use Python
> 🔍 Started learning Python
```

## The Power of This Approach

### What Just Happened?
1. **10 minutes**: Sarah wrote what she wanted in plain English
2. **20 minutes**: AI built a working implementation
3. **5 minutes**: Sarah was using her new tool
4. **Total: 35 minutes** from idea to usage

### What Sarah Owns
- **The specifications** - Her unique requirements and rules
- **The concept** - Her vision of a note garden
- **The workflow** - How she wants to work

### What AI Provided
- **Implementation details** - Database, search algorithms
- **Best practices** - Error handling, file organization
- **Boilerplate** - CLI setup, configuration

## Try It Yourself

1. Copy the specifications above
2. Tell your AI: "Build this note garden tool"
3. Watch it come to life
4. Modify specs to match your needs
5. Have AI update the implementation

## Key Insights

### Specifications are Freedom
- Change your mind? Update the spec
- Want a web version? Same specs, different implementation
- Switch languages? Specs remain valid

### AI as Implementation Partner
- You provide vision and rules
- AI handles technical details
- Together, you build faster

### Progressive Enhancement
Start simple, grow complex:
- Day 1: Basic notes
- Week 1: Add connections
- Month 1: Add visualizations
- Year 1: Full knowledge management system

---

*This example shows how AGET enables rapid prototyping through specifications. The code is real, the tool works, and it took less than an hour to create.*