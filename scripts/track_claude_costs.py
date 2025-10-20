#!/usr/bin/env python3
"""
Track Claude Code costs incrementally for long-running projects.
This script demonstrates parsing /cost output for incremental tracking.
"""

import re
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

class ClaudeCostTracker:
    def __init__(self, project_dir: Path = None):
        self.project_dir = project_dir or Path.cwd()
        self.cost_log_file = self.project_dir / '.aget' / 'claude_costs.jsonl'
        self.cost_log_file.parent.mkdir(parents=True, exist_ok=True)

    def parse_cost_output(self, output: str) -> Optional[Dict]:
        """Parse the /cost command output into structured data."""
        data = {
            'timestamp': datetime.now().isoformat(),
            'project': str(self.project_dir)
        }

        # Parse total cost: $X.XXXX
        cost_match = re.search(r'Total cost:\s+\$([0-9.]+)', output)
        if cost_match:
            data['total_cost'] = float(cost_match.group(1))

        # Parse durations
        api_duration_match = re.search(r'Total duration \(API\):\s+([0-9.]+)s', output)
        if api_duration_match:
            data['api_duration_seconds'] = float(api_duration_match.group(1))

        wall_duration_match = re.search(r'Total duration \(wall\):\s+([0-9.]+)s', output)
        if wall_duration_match:
            data['wall_duration_seconds'] = float(wall_duration_match.group(1))

        # Parse code changes
        changes_match = re.search(r'(\d+) lines added, (\d+) lines removed', output)
        if changes_match:
            data['lines_added'] = int(changes_match.group(1))
            data['lines_removed'] = int(changes_match.group(2))

        # Parse model usage
        models = {}
        model_pattern = r'([a-z0-9-]+):\s+([0-9.]+)k? input, ([0-9.]+)k? output.*\(\$([0-9.]+)\)'
        for match in re.finditer(model_pattern, output):
            model_name = match.group(1).strip()
            models[model_name] = {
                'input_tokens': float(match.group(2)) * 1000,  # Convert k to actual
                'output_tokens': float(match.group(3)) * 1000,
                'cost': float(match.group(4))
            }

        if models:
            data['models'] = models

        return data if 'total_cost' in data else None

    def capture_current_cost(self) -> Optional[Dict]:
        """
        Attempt to capture current cost from Claude Code.
        Note: This requires Claude Code to be running in the current session.
        """
        # This is a placeholder - in practice, you'd need to:
        # 1. Either parse from Claude's session files if they exist
        # 2. Or have Claude periodically write costs to a file
        # 3. Or use the Claude Analytics API if available

        # For demonstration, let's simulate with the example data:
        sample_output = """Total cost:            $0.0841
Total duration (API):  7.5s
Total duration (wall): 31.7s
Total code changes:    0 lines added, 0 lines removed
Usage by model:
    claude-3-5-haiku:  4.4k input, 51 output, 0 cache read, 0 cache write ($0.0037)
     claude-opus-4-1:  4 input, 57 output, 15.1k cache read, 2.8k cache write ($0.0804)"""

        return self.parse_cost_output(sample_output)

    def save_cost_entry(self, cost_data: Dict):
        """Append cost entry to the log file."""
        with open(self.cost_log_file, 'a') as f:
            f.write(json.dumps(cost_data) + '\n')

    def get_cumulative_cost(self) -> float:
        """Calculate cumulative cost from all log entries."""
        if not self.cost_log_file.exists():
            return 0.0

        total = 0.0
        with open(self.cost_log_file) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    total += entry.get('total_cost', 0.0)
                except json.JSONDecodeError:
                    continue

        return total

    def report(self) -> str:
        """Generate a cost report for the project."""
        cumulative = self.get_cumulative_cost()

        report = f"""
## Claude Code Cost Report
Project: {self.project_dir}
Cumulative Cost: ${cumulative:.4f}
Log File: {self.cost_log_file}
"""

        # Show recent entries
        if self.cost_log_file.exists():
            entries = []
            with open(self.cost_log_file) as f:
                for line in f:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

            if entries:
                report += f"\nRecent Sessions ({min(3, len(entries))} of {len(entries)}):\n"
                for entry in entries[-3:]:
                    timestamp = entry.get('timestamp', 'Unknown')
                    cost = entry.get('total_cost', 0.0)
                    report += f"  - {timestamp}: ${cost:.4f}\n"

        return report


def main():
    """Demonstrate the cost tracking functionality."""
    tracker = ClaudeCostTracker()

    # Capture current cost (simulated)
    cost_data = tracker.capture_current_cost()

    if cost_data:
        print(f"Captured cost data: ${cost_data['total_cost']:.4f}")

        # Save to log
        tracker.save_cost_entry(cost_data)
        print(f"Saved to {tracker.cost_log_file}")

        # Show report
        print(tracker.report())
    else:
        print("Could not capture cost data")
        print("\nTo make this work in practice, you would need to:")
        print("1. Run this script periodically during your Claude session")
        print("2. Have Claude write cost data to a known location")
        print("3. Or integrate with Claude Analytics API if available")


if __name__ == "__main__":
    main()