# Developer Domain Vocabulary

**Version**: 1.0.0
**Status**: Active
**Owner**: template-developer-aget
**Created**: 2026-01-10
**Scope**: Template vocabulary (DRIVES instance behavior per L481)
**Archetype**: Developer

---

## Meta

```yaml
vocabulary:
  meta:
    domain: "development"
    version: "1.0.0"
    owner: "template-developer-aget"
    created: "2026-01-10"
    theoretical_basis:
      - "L481: Ontology-Driven Agent Creation"
      - "L482: Executable Ontology - SKOS+EARS Grounding"
    archetype: "Developer"
```

---

## Concept Scheme

```yaml
Developer_Vocabulary:
  skos:prefLabel: "Developer Vocabulary"
  skos:definition: "Vocabulary for developer domain agents"
  skos:hasTopConcept:
    - Developer_Core_Concepts
  rdf:type: skos:ConceptScheme
```

---

## Core Concepts

### Code_Quality

```yaml
Code_Quality:
  skos:prefLabel: "Code Quality"
  skos:definition: "Attributes that make code maintainable and reliable"
  skos:broader: Developer_Core_Concepts
  skos:inScheme: Developer_Vocabulary
```

### Implementation

```yaml
Implementation:
  skos:prefLabel: "Implementation"
  skos:definition: "Translation of design into working code"
  skos:broader: Developer_Core_Concepts
  skos:inScheme: Developer_Vocabulary
```

### Testing

```yaml
Testing:
  skos:prefLabel: "Testing"
  skos:definition: "Verification that code behaves as expected"
  skos:broader: Developer_Core_Concepts
  skos:inScheme: Developer_Vocabulary
```

### Refactoring

```yaml
Refactoring:
  skos:prefLabel: "Refactoring"
  skos:definition: "Improving code structure without changing behavior"
  skos:broader: Developer_Core_Concepts
  skos:inScheme: Developer_Vocabulary
```

### Technical_Debt

```yaml
Technical_Debt:
  skos:prefLabel: "Technical Debt"
  skos:definition: "Accumulated cost of shortcuts in codebase"
  skos:broader: Developer_Core_Concepts
  skos:inScheme: Developer_Vocabulary
```

---

## Extension Points

Instances extending this template vocabulary should:
1. Add domain-specific terms under appropriate broader concepts
2. Maintain SKOS compliance (prefLabel, definition, broader/narrower)
3. Reference foundation L-docs where applicable
4. Use `research_status` for terms under investigation

---

## References

- L481: Ontology-Driven Agent Creation
- L482: Executable Ontology - SKOS+EARS Grounding
- R-REL-015: Template Ontology Conformance
- AGET_VOCABULARY_SPEC.md

---

*Developer_VOCABULARY.md v1.0.0 — SKOS-compliant template vocabulary*
*Generated: 2026-01-10*
