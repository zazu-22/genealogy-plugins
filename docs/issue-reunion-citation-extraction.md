# Issue: Incomplete Citation-Level Data Extraction from Reunion GEDCOM

**Date**: 2026-01-01
**Discovered During**: Source Metadata Recovery Project, Session 4
**Project Location**: `~/Genealogy/projects/2025-12-source-metadata/`
**Severity**: Design gap affecting data recovery completeness

---

## Executive Summary

During a GEDCOM-to-Gramps migration, we discovered that citation-level data can exist in **multiple GEDCOM fields** (TEXT, DETA, FILN, LOCA), not just TEXT. Additionally, **all sources** (both consolidated and surviving) can contain citation-level data that needs extraction. Our initial approach incorrectly:

1. Only processed TEXT field for citation page data
2. Only processed consolidated sources, ignoring surviving sources
3. Conflated source mapping type with data field availability

This resulted in missing ~264 citations worth of recoverable data on the first pass.

---

## The Core Problem: Reunion's Flat Model

Reunion (and many GEDCOM sources) use a **flat model** where each source record contains data from all three Gramps layers:

```
Reunion Source = Repository info + Source info + Citation info
```

When migrating to Gramps' **hierarchical model**:

```
Gramps Repository → Gramps Source → Gramps Citation
```

We must carefully extract each piece of data to its correct layer. The challenge is that **citation-level data can appear in multiple GEDCOM fields**, and the field used varies by source type and data entry practices.

---

## Citation-Level Data in GEDCOM Fields

### Fields That Can Contain Citation Data

| GEDCOM Field | Typical Content | Citation-Level Data |
|--------------|-----------------|---------------------|
| `TEXT` | Database citation, full reference | ED, Sheet, Line, Page, certificate numbers |
| `DETA` | Detailed enumeration info | Roll, Page, ED (often more specific than TEXT) |
| `FILN` | File/certificate number | Certificate numbers, page references |
| `LOCA` | Location/access info | Microfilm numbers, FHL refs (sometimes) |
| `PAGE` | Page reference | Page numbers |

### Examples of Each

**TEXT** (common for Ancestry citations):
```
Ancestry.com. 1920 United States Federal Census [database on-line].
Provo, UT, USA: Ancestry.com Operations Inc, 2010.
Year: 1920; Census Place: Zanesville, Ohio; Roll: T625_1234; Page: 5A; ED: 102
```

**DETA** (more specific enumeration, often for surviving sources):
```
Roll: T624_453; Page: 13A; Enumeration District: 0171
```

**FILN** (certificate numbers):
```
Certificate #26138
page 206, no. 411
Volume 6, page 450-452
```

**LOCA** (sometimes contains citation-level microfilm refs):
```
FHL microfilm: 1374466
NARA microfilm publication M593
```

---

## The Flawed Approach

### What We Did Wrong

**Flaw 1**: Only processed TEXT field
- Ignored DETA, FILN, LOCA even when they contained citation-level data
- Many surviving sources have enumeration details in DETA, not TEXT

**Flaw 2**: Only processed consolidated sources
- Assumed surviving (1:1) sources didn't need citation-level extraction
- In reality, surviving sources often have DETA/FILN that should become `citation.page`

**Flaw 3**: Conflated mapping type with field selection
- The consolidated/surviving distinction describes **source relationships**
- It does NOT determine **which GEDCOM fields contain citation data**

### The Impact

| Missed Category | Sources | Citations |
|-----------------|---------|-----------|
| Surviving sources with DETA | 7 | 73 |
| Surviving sources with FILN | 9 | 39 |
| Consolidated sources with DETA | 4 | 51 |
| Consolidated sources with FILN | 1 | 4 |
| Consolidated sources with LOCA | 3 | 47 |
| Surviving sources with LOCA | ~10 | ~50 |
| **Total Missed** | | **~264** |

---

## The Correct Approach

### Field Priority for Citation Extraction

When extracting citation page data, check fields in this order:

```python
def extract_citation_page(gedcom_data):
    """Extract citation page data from GEDCOM fields."""

    # 1. DETA first (most specific enumeration details)
    if gedcom_data.deta:
        result = extract_from_deta(gedcom_data.deta)
        if result:
            return result

    # 2. FILN (certificate/page numbers)
    if gedcom_data.filn:
        result = format_filn(gedcom_data.filn)
        if result:
            return result

    # 3. TEXT (database citations)
    if gedcom_data.text:
        result = extract_from_text(gedcom_data.text)
        if result:
            return result

    # 4. LOCA (only if contains citation-level refs)
    if gedcom_data.loca and is_citation_level_loca(gedcom_data.loca):
        result = extract_from_loca(gedcom_data.loca)
        if result:
            return result

    return None

def is_citation_level_loca(loca):
    """Distinguish citation-level refs from repository descriptions."""
    loca_lower = loca.lower()
    return any([
        'microfilm' in loca_lower,
        'fhl' in loca_lower,
        'nara' in loca_lower,
        loca.startswith('http') and '/record/' in loca,  # Specific record URLs
    ])
```

### Process ALL Sources, Not Just Consolidated

```python
# WRONG: Only process consolidated
for source in sources:
    if source.mapping_type == 'consolidated':
        extract_citation_data(source)

# CORRECT: Process all sources with citations needing data
for source in sources:
    for citation in source.citations:
        if not citation.page:
            citation.page = extract_citation_page(source.gedcom_data)
```

---

## Agent Task: Evaluate Plugin Changes

Please evaluate whether the `genealogy-plugins` marketplace needs updates to prevent this issue in future migrations. Consider:

### 1. Documentation Updates

**File**: `docs/gedcom-gramps-field-mapping.md`

Current documentation covers field mapping but may not emphasize:
- [ ] The need to check ALL fields for citation-level data
- [ ] That DETA often contains more specific data than TEXT
- [ ] That LOCA may contain citation-level refs (microfilm, FHL)
- [ ] The distinction between source mapping type and data availability

### 2. Evidence Analysis Plugin

**Location**: `plugins/evidence-analysis/`

Evaluate whether the `/analyze` or `/cite` skills should:
- [ ] Warn when DETA/FILN data exists but TEXT is being processed
- [ ] Provide guidance on LOCA field interpretation
- [ ] Include field priority recommendations

### 3. Gramps Tools Plugin

**Location**: `plugins/gramps-tools/`

Evaluate whether the `/audit` skill should:
- [ ] Check for citations missing page data when GEDCOM source has DETA/FILN
- [ ] Flag potential data extraction gaps
- [ ] Include a "GEDCOM field coverage" audit

### 4. Research Workflow Plugin

**Location**: `plugins/research-workflow/`

Evaluate whether research planning should:
- [ ] Include GEDCOM field analysis in migration planning
- [ ] Track which fields were processed vs. available

### 5. New Skill Consideration

Should there be a dedicated skill for GEDCOM-to-Gramps migration guidance?
- GEDCOM field inventory
- Extraction gap analysis
- Citation-level data validation

---

## Key Lessons to Encode

1. **Reunion's flat model combines three Gramps layers** - Each source contains repository + source + citation data that must be properly separated.

2. **Citation data can exist in multiple GEDCOM fields** - TEXT, DETA, FILN, and LOCA can all contain citation-level information.

3. **DETA often has the most specific data** - For census records especially, DETA frequently contains Roll/Page/ED when TEXT only has generic database info.

4. **Source mapping type ≠ data availability** - Whether a source was consolidated or survived describes relationships, not which fields have extractable data.

5. **LOCA requires filtering** - May contain citation-level refs (microfilm) or repository descriptions. Must distinguish.

---

## Reference Files

- Issue discovered: `~/Genealogy/projects/2025-12-source-metadata/plan.md` (Phase 4.5)
- Lessons learned: `~/Genealogy/projects/2025-12-source-metadata/current-state.json`
- Field mapping: `docs/gedcom-gramps-field-mapping.md`
- Session notes: `~/Genealogy/projects/2025-12-source-metadata/sessions/session-04.md`

---

## Expected Outcome

After reviewing this issue, provide:

1. **Assessment**: Which plugins/skills need updates?
2. **Recommendations**: Specific changes to prevent this issue
3. **Implementation Plan**: If changes are needed, what's the scope?
4. **Documentation Updates**: What should be added to existing docs?
