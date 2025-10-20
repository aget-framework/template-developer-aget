"""
Content merger for AGET migration - preserves custom content.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ContentMerger:
    """Intelligently merge AGET protocols with existing custom content."""

    def __init__(self):
        """Initialize with section markers."""
        self.aget_sections = [
            "Session Management Protocols",
            "Housekeeping Protocols",
            "Directory Structure",
            "Vocabulary Note",
            "Available Patterns"
        ]

        self.preserved_sections = [
            "Project Overview",
            "Project Context",
            "Key Context",
            "Working Principles",
            "Current State",
            "Important Commands",
            "Custom",  # Any section with "Custom" in name
            "Specific", # Any section with "Specific" in name
        ]

    def extract_sections(self, content: str) -> Dict[str, str]:
        """Extract sections from markdown content."""
        sections = {}
        current_section = "HEADER"
        current_content = []

        for line in content.split('\n'):
            # Detect section headers (## or ###)
            if line.startswith('##'):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)

                # Start new section
                current_section = line.strip('#').strip()
                current_content = [line]
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def classify_sections(self, sections: Dict[str, str]) -> Tuple[Dict, Dict, Dict]:
        """Classify sections into AGET, custom, and mergeable."""
        aget_sections = {}
        custom_sections = {}
        mergeable_sections = {}

        for section_name, content in sections.items():
            # Check if it's an AGET section
            is_aget = any(aget in section_name for aget in self.aget_sections)

            # Check if it should be preserved
            is_custom = any(
                preserved in section_name
                for preserved in self.preserved_sections
            )

            if is_aget:
                aget_sections[section_name] = content
            elif is_custom or section_name == "HEADER":
                custom_sections[section_name] = content
            else:
                # Could be merged or replaced
                mergeable_sections[section_name] = content

        return aget_sections, custom_sections, mergeable_sections

    def merge_contents(self, existing_content: str, aget_content: str) -> str:
        """Merge existing content with AGET template content."""

        # Extract sections from both
        existing_sections = self.extract_sections(existing_content)
        aget_sections = self.extract_sections(aget_content)

        # Classify existing sections
        _, custom_sections, mergeable = self.classify_sections(existing_sections)
        aget_required, _, _ = self.classify_sections(aget_sections)

        # Build merged content
        merged = []

        # 1. Start with custom header/overview if exists
        if "HEADER" in custom_sections:
            merged.append(custom_sections["HEADER"])
            merged.append("")

        # 2. Add project-specific context sections
        for section_name in ["Project Overview", "Project Context", "Key Context"]:
            if section_name in custom_sections:
                merged.append(custom_sections[section_name])
                merged.append("")

        # 3. Add AGET protocol sections
        merged.append("## Session Management Protocols")
        if "Session Management Protocols" in aget_required:
            merged.append(aget_required["Session Management Protocols"])
        merged.append("")

        merged.append("## Housekeeping Protocols")
        if "Housekeeping Protocols" in aget_required:
            merged.append(aget_required["Housekeeping Protocols"])
        merged.append("")

        # 4. Add custom working principles and commands
        for section_name in ["Working Principles", "Important Commands", "Current State"]:
            if section_name in custom_sections:
                merged.append(custom_sections[section_name])
                merged.append("")

        # 5. Add directory structure and vocabulary
        if "Directory Structure" in aget_required:
            merged.append(aget_required["Directory Structure"])
            merged.append("")

        if "Vocabulary Note" in aget_required:
            merged.append(aget_required["Vocabulary Note"])
            merged.append("")

        # 6. Add any remaining custom sections
        for section_name, content in custom_sections.items():
            if section_name not in ["HEADER", "Project Overview", "Project Context",
                                   "Key Context", "Working Principles",
                                   "Important Commands", "Current State"]:
                merged.append(content)
                merged.append("")

        # 7. End with AGET footer
        if "Available Patterns" in aget_required:
            merged.append(aget_required["Available Patterns"])

        merged.append("")
        merged.append("---")
        merged.append("*Enhanced with AGET v2 - https://github.com/gmelli/aget-cli-agent-template*")

        return '\n'.join(merged)

    def merge_files(self, existing_path: Path, template_path: Path,
                   output_path: Optional[Path] = None) -> str:
        """Merge existing file with AGET template."""

        existing_content = existing_path.read_text() if existing_path.exists() else ""
        template_content = template_path.read_text()

        merged = self.merge_contents(existing_content, template_content)

        if output_path:
            output_path.write_text(merged)

        return merged


# Example usage for testing
if __name__ == "__main__":
    merger = ContentMerger()

    # Test with sample content
    existing = """# Claude Code Instructions - Musical AI Collaborator

## Project Overview
What started as a Spotify data analysis toolkit has evolved into a Musical AI Collaborator.

## Working Principles
- Gap Handling: Provide actionable remedies
- Response Format: [Gap] → [Remedy] → [Context]

## Session Management
- "Wind down": Save work
"""

    aget_template = """# Agent Configuration

## Session Management Protocols

### Wake Up Protocol
When user says "wake up" or "hey":
- Show status
- Report readiness

## Directory Structure
- workspace/ - Private work
- products/ - Public outputs
"""

    result = merger.merge_contents(existing, aget_template)
    print(result)