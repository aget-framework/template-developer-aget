# Example: Meeting Insights - Business Productivity Tool

> Transform meeting chaos into actionable insights in 40 minutes

## The Story

**Priya's Problem**: "I'm in 15+ meetings per week. By Friday, I can't remember what was decided on Monday. I need something that captures decisions and tracks follow-ups automatically."

**Traditional Approach**: Enterprise software, complex integrations, IT approval...

**AGET Approach**: 40 minutes to a working solution

## Step 1: Define the Business Need (10 minutes)

Priya creates `FUNCTIONAL_REQUIREMENTS.md`:

```markdown
# Meeting Insights - Functional Requirements

## Core Capabilities

### FR-001: Quick Meeting Capture
**User Story**: As a busy manager, I need to log meetings in seconds
**Acceptance Criteria**:
- Voice or text input
- Auto-detect participants from calendar
- Tag meeting type (standup, 1-on-1, review)
- Timestamp automatically

### FR-002: Extract Action Items
**User Story**: As a team lead, I need to track commitments
**Acceptance Criteria**:
- Auto-identify action items from notes
- Assign owners
- Set due dates
- Send reminders

### FR-003: Decision Tracking
**User Story**: As a stakeholder, I need to recall what was decided
**Acceptance Criteria**:
- Highlight key decisions
- Link to supporting documents
- Show decision history
- Track decision changes

### FR-004: Smart Summaries
**User Story**: As an executive, I need quick weekly insights
**Acceptance Criteria**:
- Weekly digest email
- Decisions made this week
- Upcoming deadlines
- Meeting time analytics
- Participant engagement metrics

### FR-005: Search Everything
**User Story**: As a team member, I need to find past discussions
**Acceptance Criteria**:
- Search by participant
- Search by topic
- Search by date range
- Search by decision/action
```

## Step 2: Business Rules (7 minutes)

```markdown
# Meeting Insights - Business Rules

### BR-001: Privacy First
**Rule**: Meeting content never leaves company systems
**Implementation**: Local storage, optional private cloud

### BR-002: Automatic Processing
**Rule**: Zero manual data entry after initial capture
**Why**: Reduce friction, increase adoption

### BR-003: Integration Light
**Rule**: Work with existing tools, don't replace them
**How**: Export to Slack, Email, Calendar

### BR-004: Action Accountability
**Rule**: Every action item has an owner and date
**Enforcement**: Can't save without these fields

### BR-005: Meeting Hygiene
**Rule**: Flag meetings without clear outcomes
**Metric**: Meetings should have decisions OR actions

### BR-006: Time Awareness
**Rule**: Alert when meetings exceed time budget
**Threshold**: >30% of work week in meetings
```

## Step 3: Data Model (8 minutes)

```markdown
# Meeting Insights - Data Specifications

## Meeting Record
```json
{
  "id": "2025-09-25-standup",
  "title": "Daily Standup",
  "date": "2025-09-25T09:00:00",
  "duration_minutes": 15,
  "participants": ["Priya", "Alex", "Sam", "Jordan"],
  "type": "standup",
  "notes": "Raw meeting notes...",
  "decisions": [],
  "actions": [],
  "insights": {},
  "tags": ["product", "sprint-23"]
}
```

## Decision Object
```json
{
  "id": "DEC-2025-09-25-001",
  "decision": "Launch feature flag for beta users",
  "made_by": "Priya",
  "rationale": "Reduce risk, gather feedback",
  "date": "2025-09-25",
  "related_actions": ["ACT-001", "ACT-002"],
  "status": "active"
}
```

## Action Item
```json
{
  "id": "ACT-2025-09-25-001",
  "action": "Set up feature flag in LaunchDarkly",
  "owner": "Alex",
  "due_date": "2025-09-27",
  "status": "pending",
  "meeting_ref": "2025-09-25-standup",
  "created": "2025-09-25T09:15:00",
  "reminders_sent": 0
}
```

## Analytics
```json
{
  "week_of": "2025-09-22",
  "total_meetings": 15,
  "total_hours": 12.5,
  "decisions_made": 8,
  "actions_created": 23,
  "actions_completed": 19,
  "top_participants": ["Priya:15", "Alex:12", "Sam:8"],
  "meeting_efficiency": 0.73
}
```
```

## Step 4: AI Builds the System (15 minutes)

Priya tells AI:

> "Build this meeting insights tool in Python. Use simple JSON storage and create both CLI and web interface."

### `meeting_insights.py` - Core System
```python
import json
import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path
import re

@dataclass
class ActionItem:
    """Represents a follow-up action from a meeting"""
    action: str
    owner: str
    due_date: str
    status: str = "pending"

class MeetingInsights:
    """FR-001 to FR-005: Complete meeting management"""

    def __init__(self, data_dir: Path = Path.home() / ".meetings"):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.meetings_file = data_dir / "meetings.json"
        self.actions_file = data_dir / "actions.json"

    def capture_meeting(self, notes: str, participants: List[str] = None):
        """FR-001: Quick meeting capture"""
        meeting = {
            'id': datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
            'date': datetime.datetime.now().isoformat(),
            'participants': participants or self.detect_participants(notes),
            'notes': notes,
            'decisions': self.extract_decisions(notes),
            'actions': self.extract_actions(notes),
            'type': self.classify_meeting(notes)
        }

        # BR-004: Every action needs owner and date
        meeting['actions'] = self.ensure_action_completeness(meeting['actions'])

        # BR-005: Flag meetings without outcomes
        if not meeting['decisions'] and not meeting['actions']:
            meeting['flag'] = 'No clear outcomes'

        self.save_meeting(meeting)
        return meeting

    def extract_decisions(self, notes: str) -> List[Dict]:
        """FR-003: Auto-identify decisions"""
        decisions = []
        # Look for decision patterns
        patterns = [
            r'decided:?\s*(.*)',
            r'decision:?\s*(.*)',
            r'will\s+(\w+.*)',
            r'agreed\s+to\s+(.*)'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, notes, re.IGNORECASE)
            for match in matches:
                decisions.append({
                    'decision': match.strip(),
                    'confidence': 0.8
                })

        return decisions

    def extract_actions(self, notes: str) -> List[Dict]:
        """FR-002: Extract action items"""
        actions = []
        # Look for action patterns
        patterns = [
            r'@(\w+)\s+will\s+(.*?)(?:\.|$)',
            r'action:?\s*(\w+)\s+(.*?)(?:\.|$)',
            r'TODO:?\s*(.*?)(?:\.|$)',
            r'follow.?up:?\s*(.*?)(?:\.|$)'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, notes, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    owner = match[0] if len(match) > 1 else 'unassigned'
                    action = match[1] if len(match) > 1 else match[0]
                else:
                    owner = 'unassigned'
                    action = match

                actions.append({
                    'action': action.strip(),
                    'owner': owner,
                    'due_date': self.extract_date(action) or self.default_due_date(),
                    'status': 'pending'
                })

        return actions

    def generate_weekly_summary(self) -> Dict:
        """FR-004: Smart summaries"""
        meetings = self.load_meetings()
        week_start = datetime.datetime.now() - datetime.timedelta(days=7)

        week_meetings = [
            m for m in meetings
            if datetime.datetime.fromisoformat(m['date']) > week_start
        ]

        # BR-006: Time awareness
        total_hours = sum(m.get('duration_minutes', 30) for m in week_meetings) / 60

        summary = {
            'week_of': week_start.strftime('%Y-%m-%d'),
            'total_meetings': len(week_meetings),
            'total_hours': total_hours,
            'time_alert': total_hours > 12,  # >30% of 40-hour week
            'decisions': [],
            'pending_actions': [],
            'completed_actions': []
        }

        for meeting in week_meetings:
            summary['decisions'].extend(meeting.get('decisions', []))

            for action in meeting.get('actions', []):
                if action['status'] == 'pending':
                    summary['pending_actions'].append(action)
                else:
                    summary['completed_actions'].append(action)

        # BR-005: Meeting hygiene metrics
        meetings_with_outcomes = sum(
            1 for m in week_meetings
            if m.get('decisions') or m.get('actions')
        )
        summary['meeting_efficiency'] = meetings_with_outcomes / len(week_meetings) if week_meetings else 0

        return summary

    def search(self, query: str, search_type: str = 'all') -> List[Dict]:
        """FR-005: Search everything"""
        meetings = self.load_meetings()
        results = []

        for meeting in meetings:
            if search_type in ['all', 'participants']:
                if any(query.lower() in p.lower() for p in meeting.get('participants', [])):
                    results.append(meeting)

            if search_type in ['all', 'content']:
                if query.lower() in meeting.get('notes', '').lower():
                    results.append(meeting)

            if search_type in ['all', 'decisions']:
                for decision in meeting.get('decisions', []):
                    if query.lower() in decision.get('decision', '').lower():
                        results.append(meeting)
                        break

        return results

    def send_reminders(self):
        """BR-003: Integration with existing tools"""
        actions = self.get_pending_actions()
        today = datetime.date.today()

        for action in actions:
            due = datetime.datetime.strptime(action['due_date'], '%Y-%m-%d').date()
            if due <= today:
                # In production, integrate with Slack/Email
                print(f"⏰ Reminder for {action['owner']}: {action['action']} (Due: {action['due_date']})")
```

### `cli.py` - Command Interface
```python
import click
from meeting_insights import MeetingInsights

@click.group()
def cli():
    """Meeting Insights - Never lose a decision again"""
    pass

@cli.command()
@click.option('--participants', '-p', multiple=True)
def meeting(participants):
    """Quick meeting capture"""
    insights = MeetingInsights()

    print("Enter meeting notes (Ctrl-D when done):")
    notes = []
    try:
        while True:
            notes.append(input())
    except EOFError:
        pass

    meeting_notes = '\n'.join(notes)
    result = insights.capture_meeting(meeting_notes, list(participants))

    print(f"\n✓ Meeting captured: {result['id']}")
    print(f"📋 Decisions found: {len(result['decisions'])}")
    print(f"✅ Actions extracted: {len(result['actions'])}")

    if result.get('flag'):
        print(f"⚠️ {result['flag']}")

@cli.command()
def summary():
    """Weekly insights summary"""
    insights = MeetingInsights()
    summary = insights.generate_weekly_summary()

    print("\n📊 Weekly Meeting Insights")
    print(f"{'='*40}")
    print(f"Meetings: {summary['total_meetings']}")
    print(f"Time in meetings: {summary['total_hours']:.1f} hours")

    if summary['time_alert']:
        print("⚠️ Meeting time exceeds 30% of work week!")

    print(f"\n📌 Decisions made: {len(summary['decisions'])}")
    print(f"✅ Actions completed: {len(summary['completed_actions'])}")
    print(f"⏳ Actions pending: {len(summary['pending_actions'])}")
    print(f"🎯 Meeting efficiency: {summary['meeting_efficiency']:.0%}")

@cli.command()
@click.argument('query')
def find(query):
    """Search past meetings"""
    insights = MeetingInsights()
    results = insights.search(query)

    print(f"\n🔍 Found {len(results)} meetings matching '{query}':")
    for meeting in results[:5]:
        print(f"  • {meeting['date'][:10]} - {len(meeting['participants'])} participants")
```

## Step 5: Immediate Value (5 minutes)

```bash
# Capture a meeting
$ meeting-insights meeting -p Priya -p Alex -p Sam
Enter meeting notes (Ctrl-D when done):
Discussed Q4 roadmap priorities
@Alex will set up feature flags by Friday
@Sam will prepare user research report
Decided: Launch beta to 10% users next week
^D

✓ Meeting captured: 20250925-103000
📋 Decisions found: 1
✅ Actions extracted: 2

# Get weekly summary
$ meeting-insights summary

📊 Weekly Meeting Insights
========================================
Meetings: 15
Time in meetings: 12.5 hours
⚠️ Meeting time exceeds 30% of work week!

📌 Decisions made: 8
✅ Actions completed: 19
⏳ Actions pending: 4
🎯 Meeting efficiency: 87%

# Find specific discussion
$ meeting-insights find "feature flags"

🔍 Found 3 meetings matching 'feature flags':
  • 2025-09-25 - 3 participants
  • 2025-09-23 - 5 participants
  • 2025-09-20 - 2 participants
```

## The Business Impact

### Time Saved
- **Before**: 2 hours/week organizing meeting notes
- **After**: 5 minutes/week reviewing summary
- **ROI**: 100+ hours/year recovered

### Decision Clarity
- No more "What did we decide?"
- Clear accountability trail
- Historical context preserved

### Meeting Quality
- Metrics drive better meetings
- Fewer meetings without outcomes
- Time awareness prevents overload

### Team Alignment
- Everyone knows their actions
- Decisions are transparent
- Progress is visible

---

*This example shows how AGET enables professionals to build custom productivity tools that solve their specific pain points without waiting for IT or buying expensive software.*