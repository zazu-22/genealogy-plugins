---
description: Analyze and classify a genealogical source
allowed-tools: [Read, Grep]
argument-hint: "<source-description-or-path>"
---

# Analyze Source

Classify a genealogical source according to Evidence Explained methodology and evaluate its evidential value.

## Instructions

1. **Load the `source-analysis` skill** for classification methodology

2. **Identify source characteristics**:

### Originality Classification
| Category | Definition | Example |
|----------|------------|---------|
| **Original** | First recording of information | Parish register, original certificate |
| **Derivative** | Copy, abstract, or extract | Transcription, database, index |
| **Authored** | Analysis or narrative | Published genealogy, biography |

### Information Classification
| Category | Definition | Example |
|----------|------------|---------|
| **Primary** | Reported by participant/witness | Parent reporting child's birth |
| **Secondary** | Reported by someone not present | Death certificate birth date |
| **Indeterminate** | Informant unknown | Census ages |

### Evidence Classification
| Category | Definition | Example |
|----------|------------|---------|
| **Direct** | Answers the question explicitly | Marriage certificate for marriage date |
| **Indirect** | Requires inference | Age at death to calculate birth year |
| **Negative** | Absence of expected information | No marriage record in expected jurisdiction |

3. **Assess source quality** considering:
   - When was the information recorded relative to the event?
   - Who provided the information?
   - What was their relationship to the event?
   - What biases might affect accuracy?

## Output Format

```markdown
# Source Analysis

## Source
**Description:** [source description]
**Citation:** [EE-style citation if available]

## Classification

| Dimension | Classification | Rationale |
|-----------|----------------|-----------|
| Originality | [Original/Derivative/Authored] | [Why] |
| Information | [Primary/Secondary/Indeterminate] | [Why] |
| Evidence | [Direct/Indirect/Negative] | [Why] |

## Quality Assessment

### Strengths
- [Strength 1]
- [Strength 2]

### Limitations
- [Limitation 1]
- [Limitation 2]

### Informant Analysis
- **Likely informant:** [who]
- **Relationship to event:** [description]
- **Knowledge basis:** [how they knew]
- **Potential biases:** [if any]

## Evidential Value

**For proving:** [what this source can help prove]
**Limitations:** [what it cannot prove alone]
**Corroboration needed:** [what other sources would strengthen this]

## Recommendations
- [How to use this source in research]
- [What to look for to corroborate]
```

## Database Registration

After classification, register the GPS analysis in the research database.

**Pre-flight check:**
```sql
SELECT * FROM evidence_classifications WHERE src_id = 'SRC-NNN';
```

**INSERT template (one row per research question):**
```sql
INSERT INTO evidence_classifications (src_id, rq_id, source_type, info_type, evidence_type, weight)
VALUES ('SRC-NNN', 'RQ-N', 'original', 'primary', 'direct', 'High');
-- source_type: original | derivative | authored
-- info_type: primary | secondary | undetermined
-- evidence_type: direct | indirect | negative
-- weight: High | Medium | Low | Negative | Undetermined
```

**Dolt commit:**
```sql
CALL DOLT_ADD('-A');
CALL DOLT_COMMIT('-m', 'research(RP-YYYY-NNN): classify SRC-NNN');
```

Use `just eval-backlog <RP-ID>` to see sources needing classification.

## Tips

- A source can have different classifications for different facts
- Even secondary information can be valuable when corroborated
- Note the specific fact being evaluated, not just the source generally
