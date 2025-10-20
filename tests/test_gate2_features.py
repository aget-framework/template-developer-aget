"""
Test Gate 2 Features - Pattern Library Foundation
Tests for aget apply, aget list, and pattern registry.
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from aget.config.commands.apply import ApplyCommand
from aget.config.commands.list import ListCommand
from aget.config.commands.init import InitCommand
from aget.patterns import registry


class TestPatternRegistry(unittest.TestCase):
    """Test pattern registry system."""

    def test_scan_patterns(self):
        """Test that registry can scan patterns directory."""
        patterns = registry.scan_patterns()

        # Should find multiple categories
        self.assertGreater(len(patterns), 0)

        # Should find session patterns
        self.assertIn('session', patterns)

        # Session should have wake pattern
        session_patterns = patterns['session']['patterns']
        pattern_names = [p['name'] for p in session_patterns]
        self.assertIn('wake', pattern_names)

    def test_list_patterns(self):
        """Test pattern listing."""
        pattern_list = registry.list_patterns()

        # Should return list of pattern IDs
        self.assertIsInstance(pattern_list, list)

        # Should include session/wake
        self.assertIn('session/wake', pattern_list)

        # Should be sorted
        self.assertEqual(pattern_list, sorted(pattern_list))

    def test_get_pattern(self):
        """Test getting specific pattern info."""
        # Valid pattern
        info = registry.get_pattern('session/wake')
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'wake')
        self.assertEqual(info['category'], 'session')

        # Invalid pattern
        info = registry.get_pattern('invalid/pattern')
        self.assertIsNone(info)

    def test_load_pattern(self):
        """Test loading pattern module."""
        module = registry.load_pattern('session/wake')

        # Should load module
        self.assertIsNotNone(module)

        # Should have apply_pattern function
        self.assertTrue(hasattr(module, 'apply_pattern'))


class TestApplyCommand(unittest.TestCase):
    """Test aget apply command."""

    def setUp(self):
        """Create temporary test directory."""
        self.test_dir = Path(tempfile.mkdtemp())
        try:
            self.original_cwd = Path.cwd()
        except (FileNotFoundError, OSError):
            # Previous test left us in deleted directory
            import os
            os.chdir("/tmp")
            self.original_cwd = Path.cwd()

        # Initialize test project
        init_cmd = InitCommand()
        init_cmd.execute(args=[str(self.test_dir)])

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir)

    def test_apply_without_agents_md(self):
        """Test apply command without AGENTS.md."""
        # Remove AGENTS.md
        (self.test_dir / "AGENTS.md").unlink()

        cmd = ApplyCommand()
        with patch('pathlib.Path.cwd', return_value=self.test_dir):
            result = cmd.execute(args=['session/wake'])

        self.assertFalse(result['success'])
        self.assertIn('No AGENTS.md found', result['error'])

    def test_apply_invalid_pattern(self):
        """Test applying non-existent pattern."""
        cmd = ApplyCommand()
        with patch('pathlib.Path.cwd', return_value=self.test_dir):
            result = cmd.execute(args=['invalid/pattern'])

        self.assertFalse(result['success'])
        self.assertIn('not found', result['error'])

    def test_apply_valid_pattern(self):
        """Test applying valid pattern."""
        cmd = ApplyCommand()
        with patch('pathlib.Path.cwd', return_value=self.test_dir):
            result = cmd.execute(args=['session/wake'])

        self.assertTrue(result['success'])
        self.assertEqual(result['pattern'], 'session/wake')

        # Should create session state file
        state_file = self.test_dir / ".session_state.json"
        self.assertTrue(state_file.exists())

    def test_apply_list_mode(self):
        """Test apply command with no arguments (list mode)."""
        cmd = ApplyCommand()
        with patch('pathlib.Path.cwd', return_value=self.test_dir):
            result = cmd.execute(args=[])

        self.assertTrue(result['success'])
        self.assertIn('patterns', result)
        self.assertIsInstance(result['patterns'], list)


class TestListCommand(unittest.TestCase):
    """Test aget list command."""

    def setUp(self):
        """Create temporary test directory."""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir)

    def test_list_patterns(self):
        """Test listing available patterns."""
        cmd = ListCommand()
        with patch('pathlib.Path.cwd', return_value=self.test_dir):
            result = cmd.execute(args=[])

        self.assertTrue(result['success'])
        self.assertIn('patterns', result)

        # Should find session/wake
        self.assertIn('session/wake', result['patterns'])

    def test_list_with_installed(self):
        """Test listing with installed patterns."""
        # Create state file with installed patterns
        state_dir = self.test_dir / ".aget"
        state_dir.mkdir(exist_ok=True)
        state_file = state_dir / "state.json"
        state_data = {
            'installed_patterns': ['session/wake', 'bridge/extract_output']
        }
        state_file.write_text(json.dumps(state_data))

        cmd = ListCommand()
        with patch('pathlib.Path.cwd', return_value=self.test_dir):
            result = cmd.execute(args=[])

        self.assertTrue(result['success'])
        self.assertEqual(len(result['installed']), 2)
        self.assertIn('session/wake', result['installed'])


class TestBridgePattern(unittest.TestCase):
    """Test bridge pattern functionality."""

    def setUp(self):
        """Create test project with outputs."""
        self.test_dir = Path(tempfile.mkdtemp())

        # Initialize project
        init_cmd = InitCommand()
        init_cmd.execute(args=[str(self.test_dir)])

        # Create sample output
        outputs_dir = self.test_dir / "outputs"
        outputs_dir.mkdir(exist_ok=True)

        # Create substantial Python file
        test_script = outputs_dir / "test_tool.py"
        test_script.write_text("""#!/usr/bin/env python3
'''Test tool for processing data.'''

import json

def process_data(input_file):
    '''Process input data and return results.'''
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Process data
    results = []
    for item in data:
        if item.get('active'):
            results.append(item)

    return results

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: test_tool.py <input.json>")
        sys.exit(1)

    results = process_data(sys.argv[1])
    print(f"Processed {len(results)} active items")
""")

    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir)

    def test_bridge_pattern_scan(self):
        """Test bridge pattern can scan outputs."""
        from patterns.bridge.extract_output import OutputExtractor

        extractor = OutputExtractor(self.test_dir)
        candidates = extractor.scan_outputs()

        # Should find our test tool
        self.assertGreater(len(candidates), 0)

        # First candidate should be our tool
        self.assertEqual(candidates[0]['name'], 'test_tool.py')
        self.assertEqual(candidates[0]['category'], 'tools')

    def test_bridge_pattern_extract(self):
        """Test extracting an output."""
        from patterns.bridge.extract_output import OutputExtractor

        extractor = OutputExtractor(self.test_dir)
        target_dir = self.test_dir / "Outputs"

        result = extractor.extract(
            'outputs/test_tool.py',
            target_dir,
            manifest=True
        )

        self.assertTrue(result['success'])
        self.assertEqual(result['output_name'], 'test-tool.py')

        # Check file was copied
        output_file = target_dir / 'test-tool.py'
        self.assertTrue(output_file.exists())

        # Check manifest was created
        manifest_file = target_dir / 'test-tool.py.manifest.json'
        self.assertTrue(manifest_file.exists())


class TestEndToEndWorkflow(unittest.TestCase):
    """Test complete Gate 2 workflow."""

    def setUp(self):
        """Create test environment."""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.test_dir)

    def test_full_workflow(self):
        """Test init -> list -> apply -> bridge workflow."""
        # Step 1: Initialize
        init_cmd = InitCommand()
        result = init_cmd.execute(args=[str(self.test_dir)])
        self.assertTrue(result['success'])

        # Verify directories created
        self.assertTrue((self.test_dir / "workspace").exists())
        self.assertTrue((self.test_dir / "data").exists())
        self.assertTrue((self.test_dir / ".aget" / "evolution").exists())

        # Step 2: List patterns
        list_cmd = ListCommand()
        with patch('pathlib.Path.cwd', return_value=self.test_dir):
            result = list_cmd.execute(args=[])

        self.assertTrue(result['success'])
        self.assertIn('session/wake', result['patterns'])

        # Step 3: Apply session pattern
        apply_cmd = ApplyCommand()
        with patch('pathlib.Path.cwd', return_value=self.test_dir):
            result = apply_cmd.execute(args=['session/wake'])

        self.assertTrue(result['success'])

        # Step 4: Apply bridge pattern
        with patch('pathlib.Path.cwd', return_value=self.test_dir):
            result = apply_cmd.execute(args=['bridge/extract_output'])

        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()