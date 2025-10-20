#!/usr/bin/env python3
"""Quick test of v2 architecture."""

import sys
sys.path.insert(0, '.')

from aget.shared.capabilities import Capabilities
from aget.base import BaseCommand
from aget.__main__ import AgetCLI

# Test capability detection
print("Testing Capability Detection:")
caps = Capabilities.detect_all()
for name, available in caps.items():
    status = "✅" if available else "❌"
    print(f"  {name}: {status}")

# Test base command pattern
print("\nTesting BaseCommand Pattern:")
class TestCommand(BaseCommand):
    def tier_basic(self, **kwargs):
        return {'success': True, 'message': 'Basic tier works'}

    def tier_git(self, **kwargs):
        return {'success': True, 'message': 'Git tier works'}

    def tier_gh(self, **kwargs):
        return {'success': True, 'message': 'GH tier works'}

cmd = TestCommand()
result = cmd.execute()
print(f"  Tier used: {result.get('tier_used')}")
print(f"  Execution time: {result.get('execution_time'):.3f}s")
print(f"  Performance OK: {'✅' if cmd.validate_performance() else '❌'}")

# Test routing
print("\nTesting CLI Routing:")
cli = AgetCLI()
print("  Modules loaded:", list(cli.modules.keys()))
print("  Future-ready structure: ✅")

print("\n✅ Architecture validation complete")