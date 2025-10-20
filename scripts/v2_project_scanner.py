#!/usr/bin/env python3
"""
Project Scanner for AGET v2 Baseline
Scans projects to establish migration baseline for v2 development.
Part of Sprint 001 / Gate 1.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class ProjectScanner:
    """Scans projects for AGET adoption and migration readiness."""

    def __init__(self):
        self.results = {
            "scan_date": datetime.now().isoformat(),
            "scanner_version": "1.0.0",
            "projects": {}
        }

    def scan_project(self, project_path: str) -> Dict[str, Any]:
        """Scan a single project for AGET patterns."""
        path = Path(project_path)
        if not path.exists():
            return {"error": f"Path does not exist: {project_path}"}

        project_name = path.name
        scan = {
            "path": str(path.absolute()),
            "name": project_name,
            "has_agents_md": False,
            "has_claude_md": False,
            "has_scripts_dir": False,
            "has_session_protocol": False,
            "has_housekeeping": False,
            "has_aget_dir": False,
            "has_git": False,
            "patterns_found": [],
            "migration_complexity": "unknown",
            "v1_adoption_level": 0,
            "cross_project_risks": [],
            "notes": []
        }

        # Check for key files
        agents_md = path / "AGENTS.md"
        claude_md = path / "CLAUDE.md"
        scripts_dir = path / "scripts"
        aget_dir = path / ".aget"
        git_dir = path / ".git"

        if agents_md.exists():
            scan["has_agents_md"] = True
            scan["v1_adoption_level"] += 30
            scan["patterns_found"].append("agents-config")

            # Check for dangerous cross-project symlinks
            if agents_md.is_symlink():
                target = agents_md.resolve()
                if not str(target).startswith(str(path)):
                    scan["cross_project_risks"].append(
                        f"⚠️ AGENTS.md symlinks to {target} (cross-project dependency!)"
                    )
                    scan["migration_complexity"] = "critical"

        if claude_md.exists():
            scan["has_claude_md"] = True
            scan["v1_adoption_level"] += 20
            scan["patterns_found"].append("claude-config")
            # Check if it's a symlink to AGENTS.md
            if claude_md.is_symlink():
                target = claude_md.resolve()
                if target.name == "AGENTS.md" and target.parent == path:
                    scan["notes"].append("CLAUDE.md → AGENTS.md symlink (✅ correct)")
                else:
                    scan["cross_project_risks"].append(
                        f"⚠️ CLAUDE.md symlinks to {target} (cross-project dependency!)"
                    )
                    scan["migration_complexity"] = "critical"

        if scripts_dir.exists() and scripts_dir.is_dir():
            scan["has_scripts_dir"] = True
            scan["v1_adoption_level"] += 10

            # Check for specific protocols
            session_script = scripts_dir / "session_protocol.py"
            if session_script.exists():
                scan["has_session_protocol"] = True
                scan["v1_adoption_level"] += 20
                scan["patterns_found"].append("session-management")

            housekeeping = scripts_dir / "housekeeping_protocol.py"
            if housekeeping.exists():
                scan["has_housekeeping"] = True
                scan["v1_adoption_level"] += 10
                scan["patterns_found"].append("housekeeping")

        if aget_dir.exists() and aget_dir.is_dir():
            scan["has_aget_dir"] = True
            scan["v1_adoption_level"] += 10
            scan["patterns_found"].append("aget-state")

        if git_dir.exists():
            scan["has_git"] = True

        # Determine migration complexity
        adoption = scan["v1_adoption_level"]
        if adoption == 0:
            scan["migration_complexity"] = "new_install"
            scan["notes"].append("No AGET v1 detected - fresh v2 install")
        elif adoption < 30:
            scan["migration_complexity"] = "minimal"
            scan["notes"].append("Partial v1 - easy migration")
        elif adoption < 60:
            scan["migration_complexity"] = "moderate"
            scan["notes"].append("Significant v1 usage - standard migration")
        else:
            scan["migration_complexity"] = "complete"
            scan["notes"].append("Full v1 adoption - careful migration needed")

        # Special checks for critical projects
        if project_name == "GM-RKB":
            scan["notes"].append("⚠️ CRITICAL: Production RKB agent - test thoroughly")
            scan["migration_complexity"] = "critical"
        elif project_name == "CCB":
            scan["notes"].append("Active development project - good test case")
        elif project_name == "aget-cli-agent-template":
            scan["notes"].append("Dogfood project - must work perfectly")
            scan["migration_complexity"] = "dogfood"

        return scan

    def scan_all(self, projects: List[str]) -> None:
        """Scan all specified projects."""
        for project in projects:
            print(f"Scanning {project}...")
            self.results["projects"][Path(project).name] = self.scan_project(project)

    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics."""
        projects = self.results["projects"]
        summary = {
            "total_projects": len(projects),
            "v1_adopted": sum(1 for p in projects.values() if p.get("v1_adoption_level", 0) > 0),
            "ready_for_v2": sum(1 for p in projects.values() if p.get("migration_complexity") in ["new_install", "minimal"]),
            "critical_projects": sum(1 for p in projects.values() if "CRITICAL" in str(p.get("notes", []))),
            "patterns_coverage": {},
            "migration_effort": {
                "new_install": 0,
                "minimal": 0,
                "moderate": 0,
                "complete": 0,
                "critical": 0,
                "dogfood": 0
            }
        }

        # Count pattern coverage
        all_patterns = set()
        for project in projects.values():
            patterns = project.get("patterns_found", [])
            for pattern in patterns:
                all_patterns.add(pattern)
                summary["patterns_coverage"][pattern] = summary["patterns_coverage"].get(pattern, 0) + 1

        # Count migration effort
        for project in projects.values():
            complexity = project.get("migration_complexity", "unknown")
            if complexity in summary["migration_effort"]:
                summary["migration_effort"][complexity] += 1

        self.results["summary"] = summary
        return summary

    def save_results(self, output_path: str) -> None:
        """Save results to JSON file."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\nResults saved to: {output}")

    def print_report(self) -> None:
        """Print human-readable report."""
        print("\n" + "="*60)
        print("AGET v2 PROJECT SCANNER BASELINE REPORT")
        print("="*60)

        for name, project in self.results["projects"].items():
            print(f"\n📁 {name}")
            print(f"   Path: {project.get('path', 'unknown')}")
            print(f"   v1 Adoption: {project.get('v1_adoption_level', 0)}%")
            print(f"   Migration: {project.get('migration_complexity', 'unknown')}")

            patterns = project.get('patterns_found', [])
            if patterns:
                print(f"   Patterns: {', '.join(patterns)}")

            notes = project.get('notes', [])
            for note in notes:
                print(f"   📝 {note}")

            risks = project.get('cross_project_risks', [])
            for risk in risks:
                print(f"   🚨 RISK: {risk}")

        if "summary" in self.results:
            summary = self.results["summary"]
            print("\n" + "-"*60)
            print("SUMMARY")
            print("-"*60)
            print(f"Total Projects: {summary['total_projects']}")
            print(f"Using v1: {summary['v1_adopted']}")
            print(f"Ready for v2: {summary['ready_for_v2']}")
            print(f"Critical: {summary['critical_projects']}")

            print("\nMigration Effort Distribution:")
            for complexity, count in summary['migration_effort'].items():
                if count > 0:
                    print(f"  {complexity}: {count} project(s)")

            print("\nPattern Coverage:")
            for pattern, count in summary['patterns_coverage'].items():
                print(f"  {pattern}: {count} project(s)")

        print("\n" + "="*60)


def main():
    """Main entry point."""
    # Define projects to scan - use relative paths
    projects = [
        ".",
        "../CCB",
        "../GM-RKB"
    ]

    scanner = ProjectScanner()
    scanner.scan_all(projects)
    scanner.generate_summary()
    scanner.print_report()

    # Save results
    output_path = "./.aget/v2-baseline.json"
    scanner.save_results(output_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())