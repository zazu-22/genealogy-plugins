---
description: Run data quality audit on Gramps tree
allowed-tools: [Bash, Read, Grep, Glob]
argument-hint: "--type <orphans|citations|dates|completeness>"
---

# Data Quality Audit

Run a data quality audit on the Gramps family tree to identify issues.

## Audit Types

| Type | Description |
|------|-------------|
| `orphans` | Find people not connected to main tree |
| `citations` | Find events/facts without source citations |
| `dates` | Find invalid or inconsistent dates |
| `completeness` | Assess overall data completeness |
| `gedcom-gaps` | Find citations with empty page when GEDCOM source has DETA/FILN/LOCA |

## Instructions

1. Read the tree name from Gramps configuration or use default "Shaffer-Richardson"

2. For the requested audit type, analyze the Gramps XML export at `~/Genealogy/git-exports/family-tree.gramps`

3. Generate a summary report with:
   - Total issues found
   - Categorized list of specific problems
   - Recommended actions

## Audit Logic

### Orphans Audit
- Find persons not connected via family links
- Identify isolated family groups
- Check for persons with no events

### Citations Audit
- Find events with `<objref>` but no `<citationref>`
- Identify persons with key events (birth, death) lacking citations
- List sources with no citations referencing them

### Dates Audit
- Find dates with invalid format
- Identify death dates before birth dates
- Find parents younger than children
- Check for dates in the future

### Completeness Audit
- Calculate percentage of persons with birth dates
- Calculate percentage of persons with death dates (for deceased)
- Calculate citation coverage for events
- Identify major data gaps

### GEDCOM Gaps Audit

**Purpose**: Identify citations where Gramps `citation.page` is empty but the original GEDCOM source contains extractable data in DETA, FILN, or LOCA fields.

**Requirements**:
- Gramps XML export at `~/Genealogy/git-exports/family-tree.gramps`
- Original GEDCOM file (user must provide path)

**Process**:
1. Parse Gramps XML to find citations with empty or minimal `page` attribute
2. Parse original GEDCOM to extract source records
3. Map Gramps sources to GEDCOM sources via title matching
4. For each citation with empty page:
   - Check if corresponding GEDCOM source has DETA, FILN, or LOCA data
   - If data exists, report as "recoverable citation data"

**Check priority order** (per `docs/gedcom-gramps-field-mapping.md`):
1. DETA - Most specific enumeration details
2. FILN - Certificate/file numbers
3. LOCA - Only if contains citation-level refs (microfilm, FHL)

**Report includes**:
- Count of citations with recoverable data
- Breakdown by field type (DETA vs FILN vs LOCA)
- List of affected sources with sample extractable data
- Recommended extraction approach

## Output Format

Present findings in a structured report:

```
# Data Quality Audit: [Type]
Date: [today]
Tree: [tree name]

## Summary
- Total issues: [count]
- Severity: [critical/warning/info]

## Issues Found

### Critical
- [issue 1]
- [issue 2]

### Warnings
- [issue 1]

## Recommendations
1. [action item]
2. [action item]
```

## Tips

- Run all audit types periodically for comprehensive review
- Address critical issues before warnings
- Use the gramps skill for understanding XML structure
