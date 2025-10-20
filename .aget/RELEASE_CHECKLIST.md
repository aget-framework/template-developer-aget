# AGET Release Checklist

## Version Update Locations

When releasing a new version, update ALL of these files:

1. **VERSION** - Main version file
2. **aget/__init__.py** - Python package version (`__version__ = "X.Y.Z"`)
3. **install.sh** - Installer version (2 places):
   - Line ~13: `# Version: X.Y.Z`
   - Line ~15: `readonly SCRIPT_VERSION="X.Y.Z"`
4. **aget/config/commands/init.py** - Template version (3 places):
   - `"aget_version": "X.Y.Z"`
   - `# AGET Standard Protocols vX.Y.Z`
   - `**Version**: X.Y.Z`
5. **CHANGELOG.md** - Add new version section

## Release Process

### 1. Pre-Release Checks
```bash
./scripts/aget_pre_release.sh
```

### 2. Update Versions
```bash
# Set new version
NEW_VERSION="X.Y.Z"

# Update all version references
echo $NEW_VERSION > VERSION
# Then manually update the files listed above
```

### 3. Update Documentation
- Update CHANGELOG.md with release notes
- Review README.md for accuracy
- Check migration guides if breaking changes

### 4. Test Installation
```bash
# Test fresh install
./install.sh /tmp/test-aget

# Test upgrade from previous version
# (backup existing, install new, verify)
```

### 5. Commit Release
```bash
git add -A
git commit -m "chore: Release v$NEW_VERSION

[Release notes here]"
```

### 6. Tag Release
```bash
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"
```

### 7. Push
```bash
git push origin main
git push origin "v$NEW_VERSION"
```

## Version Naming Convention

- **X.Y.Z** - Production releases (e.g., 2.1.0)
- **X.Y.Z-beta** - Beta releases (e.g., 2.1.0-beta)
- **X.Y.Z-alpha** - Alpha releases (e.g., 2.1.0-alpha)

## Quick Version Check Script

```bash
# Check all version references are consistent
grep -E "(2\.[0-9]+\.[0-9]+)" VERSION aget/__init__.py install.sh aget/config/commands/init.py | grep -v CHANGELOG
```

---
*Keep this checklist updated when adding new version references*