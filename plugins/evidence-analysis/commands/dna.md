---
description: Analyze DNA match for relationship determination
allowed-tools: [Read, WebSearch, Grep]
argument-hint: "--cm <centimorgans> [--shared-matches <list>]"
---

# DNA Evidence Analysis

Analyze DNA match data to determine potential relationships and integrate with documentary evidence.

## Instructions

1. **Load the `dna-evidence` skill**

2. **Collect match information**:
   - Shared centimorgans (cM)
   - Shared segments (if available)
   - Largest segment size
   - Shared matches (clustering)
   - Known tree information

3. **Determine relationship range** using cM value:

| cM Range | Possible Relationships |
|----------|----------------------|
| 3400+ | Parent/Child, Full Sibling |
| 1700-2300 | Grandparent, Aunt/Uncle, Half-Sibling |
| 680-1150 | 1C, Great-Grandparent, Great-Aunt/Uncle |
| 200-620 | 2C, 1C1R, Great-Great-Grandparent |
| 90-180 | 3C, 2C1R, 1C2R |
| 20-85 | 4C-6C range |

4. **Analyze shared matches** to identify:
   - Which ancestral line the match belongs to
   - Common ancestor candidates
   - Cluster groupings

5. **Integrate with documentary evidence**:
   - Does DNA support or contradict paper trail?
   - What relationship would explain both?
   - Are there alternative explanations?

## Output Format

```markdown
# DNA Match Analysis

## Match Summary
- **Shared DNA:** [X] cM across [N] segments
- **Largest Segment:** [X] cM
- **Predicted Relationship:** [range from tool/calculation]

## Relationship Probabilities

Using DNA Painter's shared cM tool:

| Relationship | Probability |
|--------------|-------------|
| [relationship 1] | [X]% |
| [relationship 2] | [X]% |
| [relationship 3] | [X]% |

## Shared Match Analysis

### Shared Matches Identified
| Match | Shared cM | Known MRCA |
|-------|-----------|------------|
| [name] | [cM] | [ancestor if known] |

### Cluster Analysis
- **Cluster A (Maternal/Paternal):** [matches]
- **Likely ancestral line:** [surname/location]

## Documentary Correlation

### Hypothesis
Based on DNA and shared matches, the likely relationship is:
[Hypothesized relationship through specific ancestors]

### Supporting Documentary Evidence
- [Evidence 1 supporting this relationship]
- [Evidence 2]

### Conflicts or Questions
- [Any contradictions between DNA and documents]

## Conclusion

**Most Likely Relationship:** [relationship]
**Confidence:** [High/Medium/Low]
**Next Steps:**
1. [Action to confirm]
2. [Additional research needed]

## Tools Used
- DNA Painter Shared cM Tool: https://dnapainter.com/tools/sharedcmv4
- What Are The Odds (WATO): [if applicable]
```

## Tips

- cM ranges have significant overlap - consider all possibilities
- Shared matches are often more useful than raw cM
- Endogamy inflates cM values
- Always seek documentary confirmation of DNA hypotheses
- Consider multiple relationship paths to same ancestor
