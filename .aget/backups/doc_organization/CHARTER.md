# AGET Framework Charter

## Identity
**aget-cli-agent-template** is the public, open-source framework that enables conversational infrastructure for CLI coding agents.

## Mission
Provide a universal, extensible framework that any team can fork and customize for their specific agent workflow needs.

## What This Repository IS
- ✅ **The Framework** - Core AGET implementation
- ✅ **Reference Patterns** - Universal, broadly-useful patterns
- ✅ **Public Standard** - The protocol all AGET instances follow
- ✅ **Fork-Friendly** - Designed to be forked and customized
- ✅ **Community-Driven** - Accepts contributions that benefit all

## What This Repository IS NOT
- ❌ **Not Experiments** - Experimental work happens in private labs
- ❌ **Not Company-Specific** - No proprietary patterns
- ❌ **Not Opinionated Workflows** - Remains neutral and extensible
- ❌ **Not The Only Way** - Encourages diverse implementations

## Design Principles
1. **Universal Usefulness** - Every pattern must benefit most users
2. **Backward Compatibility** - Never break existing forks
3. **Zero Dependencies** - Python stdlib only
4. **Fork-First Design** - Optimize for customization
5. **Protocol Over Implementation** - Define interfaces, not opinions

## Relationship Model
```
aget-cli-agent-template (This Repo)
         ├── Forked by → Organization A → their-aget-private
         ├── Forked by → Team B → custom-aget-lab
         ├── Forked by → Individual C → personal-aget
         └── Reference Lab → gmelli/aget-aget
```

## Contribution Criteria
We accept contributions that:
- Benefit >50% of users
- Are backward compatible
- Follow the protocol
- Include tests (>80% coverage)
- Are framework improvements, not workflow opinions

We redirect to private repos:
- Company-specific patterns
- Experimental features
- Opinionated workflows
- Proprietary enhancements

## Governance
- **Maintainer**: Gabor Melli (gmelli)
- **License**: MIT (fork-friendly)
- **Decisions**: Public RFC process for major changes
- **Support**: Community-driven through Issues/Discussions

## Success Metrics
- Number of active forks
- Cross-fork pattern contributions
- Protocol adoption (not just this implementation)
- Fork success stories

---
*Last Updated: 2025-09-25*
*Charter Version: 1.0*