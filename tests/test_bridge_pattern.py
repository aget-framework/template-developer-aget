"""Test the bridge pattern with mock agent data."""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '.')
from patterns.bridge.extract_output import OutputExtractor


def create_mock_agent(tmpdir: Path):
    """Create a mock agent with outputs for testing."""
    # Ensure base directory exists
    tmpdir.mkdir(parents=True, exist_ok=True)

    # Create agent structure
    (tmpdir / "outputs").mkdir()
    (tmpdir / "data").mkdir()
    (tmpdir / ".aget" / "evolution").mkdir(parents=True)

    # Create mock outputs
    outputs = [
        ("outputs/cost_analyzer.py", """#!/usr/bin/env python3
'''Analyzes OpenAI API costs from usage logs.'''
import json
import sys
from datetime import datetime

def analyze_costs(log_file):
    with open(log_file) as f:
        logs = json.load(f)

    total_cost = sum(log.get('cost', 0) for log in logs)
    return {
        'total_cost': total_cost,
        'analyzed_at': datetime.now().isoformat()
    }

if __name__ == '__main__':
    result = analyze_costs(sys.argv[1])
    print(json.dumps(result, indent=2))
"""),
        ("outputs/README.md", """# Cost Analyzer

A tool to analyze OpenAI API costs from usage logs.

## Usage
```bash
python cost_analyzer.py usage_logs.json
```
"""),
        ("outputs/temp.txt", "temporary file"),  # Should be filtered out (too small)
        ("outputs/.hidden.py", "hidden file"),  # Should be filtered
        ("outputs/data_processor.js", """// Process data files
const fs = require('fs');

function processData(inputFile) {
    const data = JSON.parse(fs.readFileSync(inputFile));
    // Transform data
    return data.map(item => ({
        ...item,
        processed: true,
        timestamp: new Date().toISOString()
    }));
}

module.exports = { processData };
"""),
        ("outputs/config.yaml", """# Configuration for agent
api:
  endpoint: https://api.openai.com/v1
  timeout: 30

settings:
  max_retries: 3
  log_level: info
"""),
    ]

    for path, content in outputs:
        file_path = tmpdir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

    # Create test file for cost_analyzer
    test_file = tmpdir / "tests" / "test_cost_analyzer.py"
    test_file.parent.mkdir(exist_ok=True)
    test_file.write_text("# Test file for cost analyzer")

    return tmpdir


def test_scan_outputs():
    """Test scanning outputs for valuable content."""
    print("Testing output scanning...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        agent_path = create_mock_agent(Path(tmpdir))
        extractor = OutputExtractor(agent_path)

        # Scan outputs
        candidates = extractor.scan_outputs()

        print(f"✅ Found {len(candidates)} valuable outputs")

        # Check that valuable files are found
        names = [c['name'] for c in candidates]
        assert "cost_analyzer.py" in names, "Should find cost_analyzer.py"
        assert "data_processor.js" in names, "Should find data_processor.js"
        assert "config.yaml" in names, "Should find config.yaml"

        # Check that non-valuable files are filtered
        assert "temp.txt" not in names, "Should filter small temp files"
        assert ".hidden.py" not in names, "Should filter hidden files"

        # Check value scoring
        cost_analyzer = next(c for c in candidates if c['name'] == 'cost_analyzer.py')
        assert cost_analyzer['value_score'] > 50, "Cost analyzer should have high value (has docs and tests)"

        print(f"✅ Value scoring works (cost_analyzer score: {cost_analyzer['value_score']})")

        # Display candidates
        print("\nTop candidates by value:")
        for candidate in candidates[:3]:
            print(f"  - {candidate['name']}: score={candidate['value_score']}, category={candidate['category']}")


def test_extract_output():
    """Test extracting an output to create a public Output."""
    print("\nTesting output extraction...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        agent_path = create_mock_agent(tmpdir / "test-agent")
        target_dir = tmpdir / "Outputs"

        extractor = OutputExtractor(agent_path)

        # Extract the cost analyzer
        result = extractor.extract(
            "outputs/cost_analyzer.py",
            target_dir,
            manifest=True
        )

        assert result['success'], f"Extraction failed: {result}"
        print(f"✅ Extracted successfully to {result['target']}")

        # Check Output was created
        output_file = Path(result['target'])
        assert output_file.exists(), "Output file should exist"
        assert output_file.name == "cost-analyzer.py", "Should transform name"
        print(f"✅ Name transformed: cost_analyzer.py → {output_file.name}")

        # Check manifest was created
        manifest_file = target_dir / "cost-analyzer.py.manifest.json"
        assert manifest_file.exists(), "Manifest should exist"

        manifest = json.loads(manifest_file.read_text())
        assert manifest['public_product'] == True
        assert manifest['category'] == 'tool'
        print(f"✅ Manifest created with metadata")

        # Check evolution was recorded
        evolution_files = list((agent_path / ".aget" / "evolution").glob("*-extraction.md"))
        assert len(evolution_files) > 0, "Should record extraction in evolution"
        print(f"✅ Extraction recorded in evolution")

        # Display extraction summary
        print(f"\nExtraction Summary:")
        print(f"  Original: {manifest['original_path']}")
        print(f"  Output: {manifest['output_name']}")
        print(f"  Category: {manifest['category']}")
        print(f"  Value Score: {manifest['value_score']}")


def test_naming_transformation():
    """Test that names are transformed appropriately."""
    print("\nTesting name transformations...")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        agent_path = Path(tmpdir) / "my-agent"
        agent_path.mkdir(parents=True)
        extractor = OutputExtractor(agent_path)

        # Test transformations
        test_cases = [
            ("outputs/my_tool.py", "my-tool.py"),
            ("outputs/data_processor.js", "data-processor.js"),
            ("outputs/config.toml", "my-agent-config.toml"),  # Generic name gets prefix
            ("outputs/README.md", "README.md"),  # Docs keep original name
        ]

        for input_path, expected_name in test_cases:
            # Create dummy file
            file_path = agent_path / input_path
            file_path.parent.mkdir(exist_ok=True)
            file_path.write_text("test content " * 20)  # Make it big enough

            actual_name = extractor._generate_output_name(file_path)
            print(f"  {Path(input_path).name} → {actual_name}")
            assert actual_name == expected_name, f"Expected {expected_name}, got {actual_name}"

    print("✅ All naming transformations correct")


if __name__ == "__main__":
    print("🌉 Bridge Pattern Tests")
    print("=" * 40)

    test_scan_outputs()
    test_extract_output()
    test_naming_transformation()

    print("\n" + "=" * 40)
    print("✅ ALL TESTS PASSED")
    print("\nBridge pattern successfully:")
    print("  - Scans outputs for valuable content")
    print("  - Calculates value scores")
    print("  - Extracts outputs as public Outputs")
    print("  - Transforms names appropriately")
    print("  - Creates manifests for traceability")
    print("  - Records extractions in evolution")