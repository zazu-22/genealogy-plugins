---
description: Analyze and classify a genealogical source
allowed-tools: [Read, Grep, Bash, Agent]
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
SELECT ec.* FROM evidence_classifications ec
JOIN sources s ON ec.src_id = s.src_id
WHERE s.local_id = 'SRC-NNN' AND s.project_id = 'RP-YYYY-NNN';
```

**INSERT template (one row per research question):**
```sql
INSERT INTO evidence_classifications (src_id, rq_id, source_type, info_type, evidence_type, weight)
SELECT s.src_id, 'RP-YYYY-NNN:RQ-N', 'original', 'primary', 'direct', 'High'
FROM sources s WHERE s.local_id = 'SRC-NNN' AND s.project_id = 'RP-YYYY-NNN';
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

## Cross-Reference Check

After GPS classification is registered, perform a cross-reference check against
sibling sources — sources linked to the same research questions.

**Algorithm:**

1. Get all RQs linked to the evaluated source via `source_rq`
2. Get all other sources linked to those RQs:
   ```sql
   SELECT DISTINCT s2.local_id, s2.description, s2.record_type, ec.evidence_type
   FROM source_rq sr1
   JOIN source_rq sr2 ON sr1.rq_id = sr2.rq_id AND sr1.src_id != sr2.src_id
   JOIN sources s2 ON sr2.src_id = s2.src_id
   LEFT JOIN evidence_classifications ec ON s2.src_id = ec.src_id AND sr2.rq_id = ec.rq_id
   WHERE sr1.src_id = (SELECT src_id FROM sources WHERE local_id = 'SRC-NNN' AND project_id = 'RP-YYYY-NNN')
   ORDER BY s2.local_id;
   ```

3. Check: does the newly evaluated source's finding resolve, change, or
   conflict with any sibling's existing evidence or classification?

4. If implications found: create a beads issue for each actionable implication
   and record in `cross_ref_findings`

**Update processing checklist:**
```sql
UPDATE sources SET processing_checklist = JSON_SET(
  COALESCE(processing_checklist, '{}'),
  '$.cross_ref_checked', CAST('true' AS JSON),
  '$.cross_ref_findings', CAST('"SRC-066 confirms intestate"' AS JSON)
) WHERE src_id = (SELECT src_id FROM sources WHERE local_id = 'SRC-NNN' AND project_id = 'RP-YYYY-NNN');
```

Use `null` for `cross_ref_findings` when no implications are found.

## Claim Evidence Linking (Optional)

After GPS classification, optionally link the source to existing claims via
`claim_evidence`. This connects source-level analysis to formal assertions.

**Check existing claims for the same RQs:**
```sql
SELECT c.claim_label, LEFT(c.statement, 60) AS Statement, c.status
FROM claims c
JOIN source_rq sr ON c.rq_id = sr.rq_id
JOIN sources s ON sr.src_id = s.src_id
WHERE s.local_id = 'SRC-NNN' AND s.project_id = 'RP-YYYY-NNN';
```

**Link evidence to a claim:**
```sql
INSERT INTO claim_evidence (claim_id, src_id, polarity, reasoning, aspect)
SELECT c.claim_id, s.src_id, 'supports',
  'Brief reasoning why this source supports/contradicts the claim',
  'general'
FROM claims c, sources s
WHERE c.claim_label = 'CLM-NNN' AND c.project_id = 'RP-YYYY-NNN'
  AND s.local_id = 'SRC-NNN' AND s.project_id = 'RP-YYYY-NNN';
```

Do NOT create claims here — use the `/claim` skill for claim creation.
This step only links already-existing claims to the evaluated source.

## Tips

- A source can have different classifications for different facts
- Even secondary information can be valuable when corroborated
- Note the specific fact being evaluated, not just the source generally
