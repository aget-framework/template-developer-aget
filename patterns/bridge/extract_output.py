#!/usr/bin/env python3
"""
Bridge Pattern: Extract Output
Transforms agent outputs into public Outputs (products).

This pattern identifies valuable outputs from an agent's workspace
and prepares them for public release as standalone products.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class OutputExtractor:
    """Extracts valuable outputs and transforms them into public products."""

    def __init__(self, agent_path: Path):
        """Initialize extractor with agent's path."""
        self.agent_path = Path(agent_path)
        self.outputs_dir = self.agent_path / "outputs"
        self.data_dir = self.agent_path / "data"
        self.evolution_dir = self.agent_path / ".aget" / "evolution"

    def scan_outputs(self) -> List[Dict[str, Any]]:
        """
        Scan outputs directory for potential public products.

        Returns:
            List of candidate outputs with metadata
        """
        candidates = []

        if not self.outputs_dir.exists():
            return candidates

        # Look for common patterns that indicate valuable outputs
        patterns = {
            "tools": ["*.py", "*.sh", "*.js"],  # Scripts and tools
            "data": ["*.json", "*.csv", "*.yaml"],  # Structured data
            "docs": ["*.md", "README*"],  # Documentation
            "configs": ["*.toml", "*.ini", ".*.yml"],  # Configurations
        }

        for category, globs in patterns.items():
            for pattern in globs:
                for file_path in self.outputs_dir.rglob(pattern):
                    if self._is_valuable(file_path):
                        candidates.append({
                            "path": str(file_path.relative_to(self.agent_path)),
                            "category": category,
                            "size": file_path.stat().st_size,
                            "modified": datetime.fromtimestamp(
                                file_path.stat().st_mtime
                            ).isoformat(),
                            "name": file_path.name,
                            "value_score": self._calculate_value(file_path)
                        })

        # Sort by value score
        candidates.sort(key=lambda x: x["value_score"], reverse=True)
        return candidates

    def _is_valuable(self, file_path: Path) -> bool:
        """
        Determine if an output is valuable enough to extract.

        Criteria:
        - Not temporary or cache files
        - Has meaningful content (>100 bytes)
        - Modified recently or frequently
        - Contains patterns indicating utility
        """
        # Skip temp files
        if any(part.startswith(".") for part in file_path.parts):
            if not file_path.name in [".gitignore", ".env.example"]:
                return False

        # Skip tiny files
        if file_path.stat().st_size < 100:
            return False

        # Skip build artifacts
        exclude_patterns = ["__pycache__", "node_modules", "dist", "build"]
        if any(pattern in str(file_path) for pattern in exclude_patterns):
            return False

        return True

    def _calculate_value(self, file_path: Path) -> int:
        """
        Calculate value score for an output.

        Higher scores indicate more valuable outputs:
        - Size (indicates substantial content)
        - Recency (recently modified = actively used)
        - Documentation presence
        - Test coverage
        """
        score = 0

        # Size factor (logarithmic)
        size = file_path.stat().st_size
        if size > 1000:
            score += 10
        if size > 10000:
            score += 20

        # Recency factor
        days_old = (datetime.now() - datetime.fromtimestamp(
            file_path.stat().st_mtime
        )).days
        if days_old < 7:
            score += 30
        elif days_old < 30:
            score += 10

        # Has documentation nearby
        doc_file = file_path.parent / "README.md"
        if doc_file.exists():
            score += 25

        # Has tests
        test_patterns = [
            f"test_{file_path.stem}",
            f"{file_path.stem}_test",
            f"{file_path.stem}.test"
        ]
        for pattern in test_patterns:
            if list(self.agent_path.rglob(f"*{pattern}*")):
                score += 25
                break

        return score

    def extract(self, output_path: str, target_dir: Path,
                manifest: bool = True) -> Dict[str, Any]:
        """
        Extract an output to create a public Output.

        Args:
            output_path: Path to output file relative to agent
            target_dir: Where to create the Output
            manifest: Whether to create extraction manifest

        Returns:
            Extraction result with metadata
        """
        source = self.agent_path / output_path
        if not source.exists():
            return {"success": False, "error": f"Source not found: {output_path}"}

        # Create target directory
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)

        # Determine Output name (transform from private to public naming)
        output_name = self._generate_output_name(source)

        # Copy the output
        target_file = target_dir / output_name
        shutil.copy2(source, target_file)

        # Create manifest if requested
        manifest_data = {
            "extracted_from": str(self.agent_path.name),
            "original_path": output_path,
            "output_name": output_name,
            "extraction_date": datetime.now().isoformat(),
            "value_score": self._calculate_value(source),
            "category": self._categorize(source),
            "public_product": True,
            "bridge_version": "1.0.0"
        }

        if manifest:
            manifest_file = target_dir / f"{output_name}.manifest.json"
            manifest_file.write_text(json.dumps(manifest_data, indent=2))

        # Record in evolution
        self._record_extraction(output_path, output_name)

        return {
            "success": True,
            "output_name": output_name,
            "target": str(target_file),
            "manifest": manifest_data
        }

    def _generate_output_name(self, source: Path) -> str:
        """
        Generate public Output name from private output.

        Transforms internal names to public-friendly names:
        - my_tool.py -> my-tool
        - data_processor.js -> data-processor.js
        - config.toml -> project-config.toml
        """
        name = source.name

        # Add project prefix for generic names
        generic_names = ["config", "data", "utils", "helper", "main"]
        if source.stem.lower() in generic_names:
            name = f"{self.agent_path.name}-{name}"

        # Transform underscores to hyphens for public names
        if source.suffix in [".py", ".sh", ".js"]:
            name = name.replace("_", "-")

        return name

    def _categorize(self, source: Path) -> str:
        """Categorize the output type."""
        suffix_map = {
            ".py": "tool",
            ".sh": "tool",
            ".js": "tool",
            ".json": "data",
            ".csv": "data",
            ".yaml": "config",
            ".toml": "config",
            ".md": "documentation"
        }
        return suffix_map.get(source.suffix, "other")

    def _record_extraction(self, source: str, output_name: str):
        """Record extraction event in evolution directory."""
        if not self.evolution_dir.exists():
            self.evolution_dir.mkdir(parents=True, exist_ok=True)

        evolution_file = self.evolution_dir / f"{datetime.now():%Y-%m-%d}-extraction.md"

        content = f"""# Output Extraction

**Date**: {datetime.now():%Y-%m-%d %H:%M}
**Source**: `{source}`
**Output**: `{output_name}`
**Bridge**: outputs → Outputs

## Extraction Notes
- Transformed private output to public Output
- Ready for community use
"""

        if evolution_file.exists():
            content = evolution_file.read_text() + "\n---\n\n" + content

        evolution_file.write_text(content)


def apply_pattern(project_path: Path = Path.cwd()):
    """
    Apply the bridge pattern to a project.

    This function is called by `aget apply bridge`.
    """
    try:
        extractor = OutputExtractor(project_path)

        print("🌉 Bridge Pattern: Output Extraction")
        print("-" * 40)

        # Scan for candidates
        candidates = extractor.scan_outputs()

        if not candidates:
            print("No outputs found to extract.")
            print("\nTip: Create valuable outputs in the outputs/ directory first.")
            return {"status": "success", "candidates": []}

        print(f"Found {len(candidates)} candidate outputs:\n")

        # Show top 5 candidates
        for i, candidate in enumerate(candidates[:5], 1):
            print(f"{i}. {candidate['name']} ({candidate['category']})")
            print(f"   Path: {candidate['path']}")
            print(f"   Value Score: {candidate['value_score']}")
            print()

        print("\nUse `aget extract <output_path>` to extract an output as a public Output.")

        return {"status": "success", "candidates": candidates}

    except Exception as e:
        print(f"❌ Error applying bridge pattern: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Test the pattern
    apply_pattern()