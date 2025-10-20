# Transition Plan: Moving Development to aget-aget

## Overview

This document outlines the transition from developing AGET in `aget-cli-agent-template` (public) to developing in `aget-aget` (private innovation lab).

## Current State (September 25, 2025)

- **aget-cli-agent-template**: v2.0-alpha ready for October 7 release
- **aget-aget**: Created but missing fundamental patterns
- **Development**: Still happening in public repository

## Transition Timeline

### Phase 1: v2.0 Release (Now - October 7, 2025)
**Stay in aget-cli-agent-template**

1. Complete v2.0 release preparation
2. Test with early adopters
3. Fix any critical bugs
4. Tag and release v2.0 on October 7
5. Announce availability

**Rationale**: Don't disrupt release momentum

### Phase 2: Post-Release Setup (October 8-14, 2025)
**Prepare aget-aget for development**

1. **Copy Fundamentals to aget-aget**
   ```bash
   # Copy core patterns (but not all)
   cp -r aget-cli-agent-template/patterns/session aget-aget/patterns/
   cp aget-cli-agent-template/scripts/aget_*.py aget-aget/scripts/
   ```

2. **Set Up Development Environment**
   ```bash
   # Add AGET's mission to aget-aget
   echo "Parent: AGET's mission..." >> aget-aget/docs/MISSION.md

   # Create development branches
   cd aget-aget
   git checkout -b dev/v2.1
   ```

3. **Establish Sync Pipeline**
   ```bash
   # Set up graduation workflow
   mkdir aget-aget/.github/workflows
   # Create graduation.yml for automated testing
   ```

### Phase 3: First Development Cycle (October 15-31, 2025)
**Begin v2.1 development in aget-aget**

1. **Morning Routine Changes**
   ```bash
   # Old (before October 15)
   cd aget-cli-agent-template
   wake up

   # New (after October 15)
   cd aget-aget
   wake up
   ```

2. **Development Workflow**
   - All new features in aget-aget/workspace/
   - Test thoroughly in private
   - Document in evolution/
   - Graduate to AGET when ready

3. **Graduation Process**
   ```bash
   # In aget-aget (develop and test)
   workspace/new_feature.py

   # When ready (graduate to AGET)
   cp workspace/new_feature.py ../aget-cli-agent-template/patterns/
   cd ../aget-cli-agent-template
   git add . && git commit -m "feat: Graduate new_feature from aget-aget"
   git push && git tag v2.1.0-beta
   ```

### Phase 4: Full Transition (November 1, 2025+)
**aget-aget becomes primary**

1. **Directory Structure**
   ```
   github/
   ├── aget-cli-agent-template/  # Public releases only
   │   ├── README.md             # User documentation
   │   ├── patterns/             # Stable patterns
   │   └── releases/             # Tagged versions
   │
   └── aget-aget/                # Active development
       ├── workspace/            # Experiments
       ├── patterns/             # Testing ground
       ├── products/             # Ready to graduate
       └── .aget/evolution/      # Decision history
   ```

2. **Release Workflow**
   - Develop in aget-aget (weeks/months)
   - Test with private projects
   - Graduate stable features to aget-cli-agent-template
   - Tag and release publicly

## Key Principles

### What Stays in aget-cli-agent-template
- **Stable releases** (v2.0, v2.1, etc.)
- **Public documentation** (GET_STARTED.md, etc.)
- **User-facing content**
- **GitHub releases and tags**

### What Moves to aget-aget
- **Active development** (all new features)
- **Experiments** (wild ideas, breaking changes)
- **Internal documentation** (already moved)
- **Failed attempts** (learning experiences)

### What Gets Synchronized
- **Graduated features** (aget-aget → AGET)
- **Critical fixes** (may go direct to AGET)
- **Security patches** (immediate sync)

## Migration Checklist

### Before October 7 (v2.0 Release)
- [ ] Complete all v2.0 features
- [ ] Test migration guide
- [ ] Validate all patterns
- [ ] Tag v2.0 release

### October 8-14 (Setup Week)
- [ ] Copy fundamentals to aget-aget
- [ ] Set up aget-aget scripts/
- [ ] Configure graduation workflow
- [ ] Test wake/wind-down in aget-aget

### October 15 (Transition Day)
- [ ] Last commit in aget-cli-agent-template
- [ ] Switch to aget-aget for daily work
- [ ] First feature in aget-aget
- [ ] Verify graduation pipeline

### November 1 (Full Transition)
- [ ] All development in aget-aget
- [ ] Graduation process smooth
- [ ] v2.1 features accumulating
- [ ] Public AGET stable

## Benefits of This Approach

1. **Freedom to Experiment**
   - Break things in private
   - Try radical changes
   - Fail without embarrassment

2. **Quality Gatekeeper**
   - Only proven features go public
   - Users get stable releases
   - Reputation protected

3. **Clear Separation**
   - Development vs. Release
   - Experimental vs. Stable
   - Private vs. Public

4. **Innovation Velocity**
   - No fear of breaking users
   - Rapid experimentation
   - Bold architectural changes

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Forgetting to graduate good features | Weekly review of aget-aget products/ |
| Diverging too far from AGET | Fundamental standards enforcement |
| Lost work in private repo | GitHub private backup + local backups |
| Confusion about where to work | Clear date-based transition |

## Success Metrics

- **October 7**: v2.0 successfully released from aget-cli-agent-template
- **October 15**: First commit in aget-aget as primary
- **November 1**: First graduated feature from aget-aget to AGET
- **December 1**: v2.1 released with 5+ graduated features

## The New Reality (Post-Transition)

```
Morning: cd aget-aget && wake up
Work:    Experiment freely in workspace/
Test:    Validate in aget-aget
Graduate: Copy proven features to aget-cli-agent-template
Release:  Tag in public AGET
```

## Final Note

This transition embodies AGET's philosophy:
- **Private exploration** (aget-aget)
- **Selective public value** (graduated features)
- **Quality through iteration** (test before release)

After October 7, aget-cli-agent-template becomes the **storefront**, while aget-aget becomes the **workshop**.

---

*Transition Plan Created: September 25, 2025*
*Target Completion: November 1, 2025*