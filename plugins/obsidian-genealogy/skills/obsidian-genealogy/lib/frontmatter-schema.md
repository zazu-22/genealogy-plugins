# Frontmatter Schema Reference

Complete YAML frontmatter specifications for genealogy vault notes.

## Person Note Schema

```yaml
---
# Required fields
type: person
gramps_id: "I0001"         # Gramps person ID

# Canvas Roots (if imported)
cr_id: "abc123"            # Canvas Roots unique ID - NEVER DELETE

# Dates (ISO 8601 preferred, flexible formats accepted)
birth_date: 1850-03-15     # or "about 1850" or "before 1850"
death_date: 1920-07-22     # omit for living persons
birth_place: "[[Zanesville, Muskingum County, Ohio]]"
death_place: "[[Columbus, Franklin County, Ohio]]"

# Family links (wikilinks)
father: "[[John Smith (1820-1890)]]"
mother: "[[Mary Jones (1825-1900)]]"
spouse:
  - "[[Jane Doe (1855-1930)]]"
children:
  - "[[Child One (1875-1950)]]"
  - "[[Child Two (1878-1960)]]"

# Optional metadata
gender: male | female | unknown
occupation: "Farmer"
religion: "Methodist"
aliases:
  - "Johnny Smith"
  - "J. Smith"
tags:
  - immigrant
  - civil-war-veteran
---
```

## Source Note Schema

```yaml
---
type: source
source_type: census | vital | church | land | newspaper | military | probate | tax | directory | other

# Evidence Explained classification
ee_category: "Chapter 6: Census Records"
ee_section: "6.20 Federal Population Schedules"

# Repository
repository: "[[National Archives]]"
repository_location: "Washington, D.C."
call_number: "NARA M432, Roll 123"

# Gramps/GEDCOM field mappings
stitle: "1850 U.S. Census"              # GEDCOM TITL → Gramps source title
sauthor: "U.S. Bureau of the Census"    # GEDCOM AUTH → Gramps author
spubinfo: "Washington, D.C.: NARA"      # GEDCOM PUBL → Gramps publication info

# Legacy fields (alternative to stitle/sauthor/spubinfo)
title: "1850 U.S. Census"
creator: "U.S. Bureau of the Census"
publication_date: 1850
jurisdiction: "Muskingum County, Ohio"

# Access information (use for notes, not attributes in Gramps)
access_date: 2024-01-15
access_method: digital | microfilm | original
url: "https://www.ancestry.com/..."
citing: "NARA microfilm M432, roll 123"

# Quality assessment
originality: original | derivative
informativeness: primary | secondary | indeterminate
reliability: high | medium | low

# Consolidation guidance
consolidate: true | false    # true for census, Find A Grave, SSDI; false for newspapers, books
---
```

### GEDCOM-Gramps Field Mapping Reference

| GEDCOM Field | Gramps Target | Frontmatter Key |
|--------------|---------------|-----------------|
| `TITL` | `stitle` | `stitle` or `title` |
| `AUTH` | `sauthor` | `sauthor` or `creator` |
| `PUBL` | `spubinfo` | `spubinfo` |
| `TYPE` | Source attribute | `source_type` |
| `REPO` | Repository ref | `repository` |

**Important**: When syncing to Gramps:
- Digital access info (URL, access_date) should become **Notes**, not Attributes
- Source Attributes don't export to GEDCOM
- Use the `digital_access` note format: `Digital access: [Website] ([URL] : accessed [Date])`

See `docs/gedcom-gramps-field-mapping.md` for complete guidance.

## Place Note Schema

```yaml
---
type: place

# Hierarchical location (specific to general)
hierarchy: "Zanesville, Muskingum County, Ohio, USA"
short_name: "Zanesville"

# Geographic coordinates
coordinates: [39.9404, -82.0132]

# Jurisdictional history
historical_names:
  - name: "Westbourne"
    years: "1797-1801"
jurisdictional_changes:
  - date: 1804
    change: "Ohio became a state"
  - date: 1803
    change: "Muskingum County formed from Washington County"

# Research information
available_records:
  - "Vital records (1867-present)"
  - "Land records (1800-present)"
  - "Probate records (1804-present)"
repositories:
  - "[[Muskingum County Courthouse]]"
  - "[[Ohio History Connection]]"

# Geographic context
parent_place: "[[Muskingum County, Ohio]]"
fips_code: "39119"
---
```

## Event Note Schema

```yaml
---
type: event
event_type: birth | death | marriage | burial | immigration | naturalization | military | occupation | residence | other

date: 1850-03-15
place: "[[Zanesville, Muskingum County, Ohio]]"

# Participants
participants:
  - person: "[[John Smith (1820-1890)]]"
    role: principal
  - person: "[[Mary Jones (1825-1900)]]"
    role: spouse

# Evidence
sources:
  - "[[1850 Census - Muskingum County]]"
  - "[[Smith Family Bible]]"
---
```

## Research Note Schema

For proof arguments, evidence analysis, and research conclusions. Use this for GPS-compliant research documentation that lives in Obsidian.

```yaml
---
type: research
research_id: "R-2026-001"              # Unique ID (R-YEAR-SEQUENCE)
subject_gramps_id: "I0083"             # Primary person being researched
subject_name: "John William Barry"     # Human-readable name
topic: "Birth Year Analysis"           # What question does this answer?
conclusion: "1862 based on preponderance of evidence"
status: complete | in_progress | abandoned

# Source references (Gramps source IDs used in analysis)
sources_cited:
  - S0003
  - S0028
  - S0029

# Optional: Link to related Gramps data
gramps_note_id: "N0045"                # If there's a corresponding Gramps note
gramps_event_id: "E0123"               # Related event in Gramps

# Metadata
created: 2026-01-02
last_updated: 2026-01-02
tags:
  - proof-argument
  - birth-research
---
```

### Research Note Body Structure

Use this template for consistent, GPS-compliant research documentation:

```markdown
# [Topic]: [Subject Name]

## Research Question
[Clear statement of what you're trying to determine]

Example: "What was John William Barry's birth year? Census records show conflicting
ages across multiple decades."

## Evidence Summary

| Source | Date | States | Classification | Confidence |
|--------|------|--------|----------------|------------|
| 1870 Census | Jun 1870 | Age 8 (b. ~1862) | Primary/Indirect | Normal |
| 1880 Census | Jun 1880 | Age 17 (b. ~1863) | Primary/Indirect | Normal |
| Death Cert | 1945 | Born 1862 | Secondary/Direct | Low |

## Analysis
[Evaluation of evidence quality, conflicts, resolution]

- The 1870 census is closest to the birth event and thus most reliable
- The death certificate informant was a child who may not have known exact birth year
- All sources cluster around 1862-1863; discrepancy is within normal census variance

## Conclusion
[Final determination with reasoning]

John William Barry was born in 1862, based on the preponderance of evidence.
The 1870 census (age 8) is given greatest weight as the earliest record.

---

## Notes
[Footnotes with full citations using Evidence Explained format]

[1]: 1870 U.S. Census, Muskingum County, Ohio, population schedule...
[2]: Ohio, Deaths, 1908-1953, certificate no. 12345...

## Gramps Data
- Person: I0083
- Birth Event: E0123
- Gramps Note: N0045 (points to this research document)
```

### Research ID Scheme

Use `R-YYYY-NNN` format for unique identification:
- `R` = Research document type prefix
- `YYYY` = Year created
- `NNN` = Sequential number (001, 002, etc.)

**Benefits:**
- Easy cross-referencing from Gramps notes (e.g., "See Obsidian: R-2026-001")
- Unique identification across the vault
- Chronological organization
- Sortable and searchable

**File Naming Convention:**
```
Research/[Topic] - [Subject Name] (R-YYYY-NNN).md
Example: Research/Birth Year Analysis - John William Barry (R-2026-001).md
```

## Date Formats

Obsidian genealogy notes accept flexible date formats:

| Format | Example | Use Case |
|--------|---------|----------|
| ISO 8601 | `1850-03-15` | Exact dates |
| Year only | `1850` | Approximate year |
| About | `about 1850` | Estimated dates |
| Before/After | `before 1850` | Terminus dates |
| Between | `between 1848 and 1852` | Date ranges |
| Quarter | `Q2 1850` | Quarter precision |
