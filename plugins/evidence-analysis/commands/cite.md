---
description: Generate an Evidence Explained-style citation
allowed-tools: [Read, WebSearch]
argument-hint: "<source-description>"
---

# Generate Citation

Create a properly formatted citation following Elizabeth Shown Mills' Evidence Explained methodology.

## Instructions

1. **Load the `evidence-explained` skill** for citation patterns

2. **Analyze the source description** to determine:
   - Source category (census, vital, church, land, etc.)
   - Whether original or derivative
   - Repository type (archive, online database, family possession)

3. **Gather required citation elements**:
   - Creator (author, agency, compiler)
   - Title (document, collection, database name)
   - Publication facts (where/when published)
   - Location (repository, URL)
   - Specific location (page, entry, item number)

4. **Format the citation** in three forms:

### Source List Entry (Bibliography)
Full citation for source list/bibliography.

### First Reference Note (Footnote)
Complete citation for first use in footnotes.

### Subsequent Note (Short Form)
Shortened form for repeat references.

## Citation Patterns by Type

### Census Records
```
[Year] U.S. Census, [State], [County], [Township/City],
page [X], dwelling [N], family [N], [Name]; digital image,
[Website] ([URL] : accessed [date]), citing NARA microfilm [series], roll [N].
```

### Vital Records
```
[Jurisdiction], [Record Type], [Name] [event], [date],
certificate [N]; [Repository], [Location].
```

### Church Records
```
[Church Name], [Record Type], [location], [Name] entry, [date];
[Repository holding records], [Location].
```

### Online Database
```
"[Database name]," database with images, [Website]
([URL] : accessed [date]), entry for [Name], [event], [date];
citing [original source if known].
```

## Output Format

```markdown
# Citation: [Brief Source Description]

## Source List Entry
[Full bibliographic entry]

## First Reference Note
[Complete footnote citation]

## Subsequent Note
[Short form for later references]

## Citation Notes
- **Source Category:** [EE category]
- **Originality:** [Original/Derivative]
- **Information Type:** [Primary/Secondary/Indeterminate]

## For Gramps

### Source-Level Fields
| Field | Value |
|-------|-------|
| **Source Title (`stitle`):** | [title for source record] |
| **Author (`sauthor`):** | [author/creator] |
| **Publication Info (`spubinfo`):** | [publisher, location, date] |
| **Repository:** | [repository name] |

### Citation-Level Fields
| Field | Value |
|-------|-------|
| **Page (`citation.page`):** | [page/entry specifics] |
| **Confidence:** | [0-4 rating] |

### Digital Access Note
```
Digital access: [Website] ([URL] : accessed [Date])
```

**Important**: Use Notes, not Attributes, for digital access info - Attributes don't export to GEDCOM.

## GEDCOM Import Note

When generating citations from GEDCOM data, check **ALL** data fields in priority order:

1. **DETA** - Most specific enumeration details (Roll/Page/ED)
2. **FILN** - Certificate or file numbers
3. **TEXT** - Database citations (often generic descriptions)
4. **LOCA** - Only if contains citation-level refs (microfilm, FHL numbers)

**Why this order matters**: DETA often contains more specific data than TEXT. Many Ancestry exports put generic database descriptions in TEXT while the actual enumeration details are in DETA.

See `docs/gedcom-gramps-field-mapping.md` for complete extraction patterns and code examples.

## Tips

- When in doubt, include more information
- Always note access date for online sources
- Distinguish between the record and its image
- Layer citations for derivative sources (image of microfilm of original)
- Use Notes for URLs/access dates (they export to GEDCOM; Attributes don't)
- See `docs/gedcom-gramps-field-mapping.md` for complete field mapping guidance
