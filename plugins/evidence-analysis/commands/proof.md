---
description: Build a GPS-compliant proof argument
allowed-tools: [Read, Write, Grep, Glob]
argument-hint: "--claim <statement> [--sources <list>]"
---

# Build Proof Argument

Construct a Genealogical Proof Standard (GPS) compliant proof argument for a genealogical claim.

## GPS Five Elements

1. **Reasonably exhaustive search** - Consulted all relevant sources
2. **Complete citations** - Full Evidence Explained citations
3. **Skilled analysis** - Proper source and evidence evaluation
4. **Resolution of conflicts** - Addressed contradictory evidence
5. **Sound conclusion** - Logical argument from evidence to conclusion

## Database-First Evidence Inventory

Before building a proof argument, query the research database for the evidence inventory:

```bash
just evidence-summary <RP-ID> <RQ>
```

Or query directly:
```sql
SELECT s.src_id, s.description, ec.source_type, ec.info_type, ec.evidence_type, ec.weight
FROM evidence_classifications ec
JOIN sources s ON ec.src_id = s.src_id
WHERE ec.rq_id = 'RQ-N'
ORDER BY ec.weight DESC;
```

Check for unclassified sources:
```sql
SELECT s.src_id, s.description
FROM source_rq sq JOIN sources s ON sq.src_id = s.src_id
LEFT JOIN evidence_classifications ec ON s.src_id = ec.src_id AND sq.rq_id = ec.rq_id
WHERE sq.rq_id = 'RQ-N' AND ec.id IS NULL;
```

The database classifications are authoritative; evidence.md prose provides the analytical narrative.

## Instructions

1. **Load the `genealogical-proof-standard` skill**

2. **State the claim clearly**
   - Specific, testable assertion
   - Identifies relationship or fact to prove

3. **Document the search** (Element 1)
   - List all sources consulted
   - Note repositories searched
   - Include negative searches

4. **Provide citations** (Element 2)
   - EE-style citations for each source
   - Complete enough to relocate

5. **Analyze each source** (Element 3)
   - Classify: original/derivative, primary/secondary, direct/indirect
   - Evaluate informant reliability
   - Extract relevant facts

6. **Address conflicts** (Element 4)
   - Identify contradictory information
   - Explain resolution with reasoning
   - Weight of evidence analysis

7. **Build the argument** (Element 5)
   - Logical progression from evidence to conclusion
   - Address alternative hypotheses
   - State confidence level

## Output Format

```markdown
# Proof Argument: [Claim Statement]

## Claim
[Clear statement of what is being proven]

## Background
[Context needed to understand the claim]

## Search Summary (GPS Element 1)

### Sources Consulted
| Source | Repository | Result |
|--------|------------|--------|
| [source] | [where] | [found/not found] |

### Negative Searches
- [What was searched but yielded no results]

## Evidence Analysis (GPS Elements 2 & 3)

### Source 1: [Name]
**Citation:** [Full EE citation]
**Classification:** [Original/Primary/Direct, etc.]
**Relevant Information:**
> [Quoted or summarized content]

**Analysis:** [Evaluation of reliability and relevance]

[Repeat for each source]

## Conflict Resolution (GPS Element 4)

### Conflict: [Description]
| Source | States | Classification |
|--------|--------|----------------|
| [source 1] | [fact] | [quality] |
| [source 2] | [different fact] | [quality] |

**Resolution:** [How conflict is resolved with reasoning]

## Conclusion (GPS Element 5)

### Evidence Summary
[Brief recap of key evidence points]

### Reasoning
[Logical argument connecting evidence to conclusion]

### Alternative Hypotheses Considered
- [Alternative 1]: [Why rejected]
- [Alternative 2]: [Why rejected]

### Conclusion
[Statement of proven fact with confidence level]

**Confidence:** [High/Medium/Low]
**Based on:** [Summary of strongest evidence]
```

## Tips

- A proof can be a narrative essay or structured argument
- Even negative evidence (absence) can be powerful
- Address all reasonable alternatives
- Be explicit about reasoning, not just facts
