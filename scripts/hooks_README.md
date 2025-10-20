# Pre-Push Hooks for AGET

Quick setup to prevent test failures from reaching GitHub.

## Quick Install

```bash
# Start with advisory mode (recommended)
python3 scripts/install_hooks.py --advisory

# Or interactive mode
python3 scripts/install_hooks.py
```

## Available Modes

### 🟢 Advisory Mode (Start Here)
- **What**: Reminds you to test, never blocks
- **When**: You're new to the project
- **Install**: `python3 scripts/install_hooks.py --advisory`

### 🟡 Critical Mode
- **What**: Blocks if critical tests fail (<10s)
- **When**: You're making important changes
- **Install**: `python3 scripts/install_hooks.py --critical`

### 🔴 Smart Mode
- **What**: Tests based on what you changed (<15s)
- **When**: You want automatic test selection
- **Install**: `python3 scripts/install_hooks.py --smart`

## Commands

```bash
# Install hook
python3 scripts/install_hooks.py --advisory  # Gentle reminder
python3 scripts/install_hooks.py --critical  # Test critical paths
python3 scripts/install_hooks.py --smart     # Smart detection

# Test your hook
python3 scripts/install_hooks.py --test

# Remove hook
python3 scripts/install_hooks.py --remove

# Skip hook once
git push --no-verify
```

## Critical Tests

Tests that run in critical mode are defined in `tests/critical.txt`:
- Core workflow test
- Session protocol test
- Installer test
- Pattern application test
- Evolution tracking test

Total runtime: ~5-8 seconds

## FAQ

**Q: How do I skip the hook once?**
```bash
git push --no-verify
```

**Q: How do I switch modes?**
```bash
python3 scripts/install_hooks.py --critical  # Switch to critical
python3 scripts/install_hooks.py --advisory  # Back to advisory
```

**Q: What if tests are too slow?**
Switch to advisory mode or use `--no-verify` when needed.

**Q: Can I customize which tests run?**
Edit `tests/critical.txt` for critical mode, or switch to smart mode.

## Gradual Adoption Plan

1. **Week 1**: Start with advisory mode
2. **Week 2**: Try critical mode for a day
3. **Week 3**: Use smart mode when comfortable
4. **Week 4**: Settle on your preferred mode

## Why This Matters

The recent CI failure was caused by a test expecting "outputs" directory while the code created "workspace" directory. This happened because:
- Test was created at 10:37 AM
- Directory renamed at 2:58 PM
- No tests run before push
- CI failed 13+ hours later

With pre-push hooks, this would have been caught immediately.

---
*Start with advisory mode - it's just a friendly reminder!*