# AGET Update Protocol

## For Your Private aget-aget Repository

**Note**: "aget-aget" refers to YOUR private experimentation repository,
which could be named anything (aget-lab, company-aget-private, etc.)

## For THE Official aget-aget Repository (Reference Implementation)

### Update Frequency
- **Beta releases**: Immediately
- **Stable releases**: Within 24 hours
- **Critical fixes**: ASAP

### Update Process
```bash
# In aget-aget repository
cd ~/github/aget-aget

# Pull latest from aget-cli-agent-template
git pull https://github.com/gmelli/aget-cli-agent-template.git main

# Or if using AGET patterns directly
python3 -m aget migrate . --from-version latest

# Test core workflows
python3 -m aget apply session/wake
python3 -m aget apply session/wind_down

# Document experience
python3 -m aget evolution --type discovery "Updated to v2.0.0-beta: [findings]"
```

### Responsibilities as First Adopter
1. **Test new features immediately**
2. **Report issues before they reach others**
3. **Document upgrade experience**
4. **Provide feedback for improvements**

## For Other AGET Users

### Update Frequency
- **Stable releases**: When convenient
- **Security fixes**: Within 1 week
- **Major versions**: After reviewing changelog

### Conservative Update Process
```bash
# Check current version
python3 -m aget --version

# Review changes
curl -s https://raw.githubusercontent.com/gmelli/aget-cli-agent-template/main/CHANGELOG.md

# Update when ready
git pull  # or reinstall
```

## Version Compatibility Matrix

| aget-cli-agent-template | aget-aget must be | Other users can be |
|------------------------|-------------------|-------------------|
| v2.0.0-beta           | v2.0.0-beta       | v1.9+ |
| v2.0.0                | v2.0.0            | v1.9+ |
| v2.1.0                | v2.1.0            | v2.0+ |

## The Principle

> **"aget-aget must always be running what we're asking others to run"**

This ensures:
- We experience our own medicine first
- Issues are caught by us, not users
- The feedback loop is immediate
- Trust is built through demonstration