# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### "Target directory does not exist"
**Error**: `Error: Target directory /path/to/project does not exist`

**Solution**:
```bash
# Create the directory first
mkdir -p /path/to/project
cd /path/to/project

# Then run installer
curl -sSL https://raw.githubusercontent.com/yourusername/cli-agent-template/main/install.sh | bash
# Or with Python directly:
python3 /path/to/cli-agent-template/installer/install.py .
```

#### "Permission denied" during installation
**Error**: `PermissionError: [Errno 13] Permission denied`

**Solutions**:
1. Check directory permissions:
   ```bash
   ls -la /path/to/project
   ```
2. Use your user directory or fix permissions:
   ```bash
   sudo chown -R $(whoami) /path/to/project
   ```

#### PyYAML not installed warning
**Warning**: `Note: PyYAML not installed. Config file creation will be skipped.`

**Solution** (optional):
```bash
pip install pyyaml
# or
pip3 install pyyaml
```

### Session Protocol Issues

#### "wake up" command not working
**Problem**: Agent doesn't respond to "wake up"

**Solutions**:
1. Ensure AGENT.md exists and agent has read it:
   ```bash
   ls -la AGENT.md
   cat AGENT.md | head -20
   ```

2. Try direct command:
   ```bash
   python3 scripts/aget_session_protocol.py wake
   ```

3. Note: Makefile support coming in future release

#### Session state not persisting
**Problem**: Session count resets, history lost

**Check**:
```bash
# Look for state file
ls -la .session_state.json

# Check contents
cat .session_state.json
```

**Solutions**:
1. Check file permissions:
   ```bash
   chmod 644 .session_state.json
   ```

2. Manually create if missing:
   ```bash
   echo '{"session_count": 0, "total_commits": 0, "last_session_time": null, "last_session_end": null, "project_created": "'$(date -Iseconds)'"}' > .session_state.json
   ```

#### Git push fails during sign-off
**Error**: `⚠ Push failed or skipped`

**Solutions**:
1. Check remote configuration:
   ```bash
   git remote -v
   ```

2. Set up remote if missing:
   ```bash
   git remote add origin https://github.com/username/repo.git
   ```

3. Check branch name:
   ```bash
   git branch
   # If using master instead of main:
   git push origin master
   ```

### Housekeeping Issues

#### Documentation check gives low grade
**Problem**: Getting D or F grade consistently

**Check these files exist**:
- README.md (50-500 lines recommended)
- AGENT.md (or CLAUDE.md symlink)
- LICENSE

**Fix**:
```bash
# Create missing files
touch README.md LICENSE
echo "# Project Name" > README.md
```

#### Spring clean removes important files
**Problem**: Files disappearing after spring clean

**Prevention**:
1. ALWAYS use dry-run first:
   ```bash
   python3 scripts/aget_housekeeping_protocol.py spring-clean --dry-run
   ```

2. Check what will be removed before confirming

3. Important files should be committed to git:
   ```bash
   git add important-file.txt
   git commit -m "feat: Add important file"
   ```

### Pattern Detection Issues

#### Patterns not showing in wake up
**Problem**: "Patterns available:" shows empty or wrong list

**Solutions**:
1. Check patterns directory structure:
   ```bash
   ls -la patterns/
   ls -la patterns/*/
   ```

2. Patterns should be directories, not files:
   ```
   patterns/
   ├── session/
   ├── housekeeping/
   └── documentation/
   ```

### Testing Issues

#### Tests fail with import errors
**Error**: `ModuleNotFoundError: No module named 'scripts'`

**Solution**:
Run tests from repository root:
```bash
cd /path/to/cli-agent-template
python3 -m pytest tests/
```

#### pytest not found
**Error**: `bash: pytest: command not found`

**Solution**:
```bash
pip install pytest
# or
pip3 install pytest
```

### Template Issues

#### Wrong template installed
**Problem**: Installed minimal but wanted standard

**Solution**:
Re-run installer with correct template:
```bash
# Using curl installer:
curl -sSL https://raw.githubusercontent.com/yourusername/cli-agent-template/main/install.sh | bash -s . standard

# Or with Python:
python3 /path/to/cli-agent-template/installer/install.py . --template standard
```

Files will be updated/added as needed.

#### Customization not working
**Problem**: AGENT.md shows `{{PROJECT_NAME}}` instead of actual name

**Check**:
- Project type detection may have failed
- Manual fix:
  ```bash
  sed -i 's/{{PROJECT_NAME}}/YourProjectName/g' AGENT.md
  ```

### SESSION_NOTES Issues

#### Session notes filling up disk
**Problem**: Too many session files accumulating

**Solution**:
1. Archive runs automatically after 30 days
2. Manual cleanup:
   ```bash
   # Move old sessions to archive
   find SESSION_NOTES -type f -mtime +30 -exec mv {} SESSION_NOTES/archive/ \;
   ```

3. Delete very old archives:
   ```bash
   find SESSION_NOTES/archive -type f -mtime +90 -delete
   ```

#### Can't find recent session notes
**Problem**: Session notes seem to disappear

**Check organized structure**:
```bash
# Sessions are organized by date
ls SESSION_NOTES/2025-09-21/
ls SESSION_NOTES/$(date +%Y-%m-%d)/
```

### Platform-Specific Issues

#### Symlinks not working (Windows)
**Problem**: CLAUDE.md symlink fails on Windows

**Solution**:
The installer automatically falls back to copying:
```python
# This happens automatically in installer
if symlink_fails:
    shutil.copy2('AGENT.md', 'CLAUDE.md')
```

#### Python version issues
**Error**: `SyntaxError: f-strings are not supported`

**Solution**:
Requires Python 3.8+:
```bash
python3 --version
# If too old, upgrade Python
```

### Debug Commands

#### Check everything at once
```bash
# Run sanity check
python3 scripts/aget_housekeeping_protocol.py sanity-check
```

#### View current session status
```bash
python3 scripts/aget_session_protocol.py status
```

#### Test the installation
```bash
# From cli-agent-template directory
python3 -m pytest tests/ -v
```

#### Verify file structure
```bash
tree -L 2 -a
# or
find . -type f -name "*.py" | head -20
```

### Getting Help

1. **Check logs**: Session notes often contain clues
2. **Run tests**: `python3 -m pytest tests/` can reveal issues
3. **Use dry-run**: Always test with `--dry-run` first
4. **Read the source**: Scripts are documented and readable
5. **Learn about patterns**: See [PATTERNS_EXPLAINED.md](PATTERNS_EXPLAINED.md)
6. **Open an issue**: https://github.com/yourusername/cli-agent-template/issues

### Emergency Recovery

If everything is broken:

1. **Backup current state**:
   ```bash
   cp -r . ../backup-$(date +%Y%m%d)
   ```

2. **Reset to clean state**:
   ```bash
   rm -rf scripts/ SESSION_NOTES/ .session_state.json
   ```

3. **Reinstall**:
   ```bash
   curl -sSL https://raw.githubusercontent.com/yourusername/cli-agent-template/main/install.sh | bash
   # Or with Python:
   python3 /path/to/cli-agent-template/installer/install.py . --template standard
   ```

4. **Restore your work**:
   ```bash
   git status
   git add -A
   git commit -m "fix: Recovery after issues"
   ```

---

Remember: Most issues can be prevented by:
- Using dry-run mode first
- Reading AGENT.md carefully
- Keeping everything in git
- Running sanity checks regularly