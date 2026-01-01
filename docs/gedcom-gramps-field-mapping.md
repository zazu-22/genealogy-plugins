# GEDCOM to Gramps Field Mapping Best Practices

This document provides authoritative guidance for mapping GEDCOM source/citation fields to Gramps, following Evidence Explained methodology and Gramps community best practices.

**Last Updated**: 2026-01-01
**Research Sources**:
- Evidence Explained (4th Edition) by Elizabeth Shown Mills
- [Gramps GEPS 018: Evidence Style Sources](https://www.gramps-project.org/wiki/index.php/GEPS_018:_Evidence_style_sources)
- [Gramps Citations Wiki](https://www.gramps-project.org/wiki/index.php/Citations)
- [Gramps Community Forum Discussions](https://gramps.discourse.group/t/adding-media-and-citations-scanned-sources-digital-only-sources-discussion/5240)
- [Evidence Explained Chapter 6: Census Records](https://www.evidenceexplained.com/content/chapter-6-census-records)

---

## Core Principles

### 1. Source vs. Citation Division

| Level | Contains | Examples |
|-------|----------|----------|
| **Source** | Stable, unchanging information about the original material | Author, title, publisher, publication info |
| **Citation** | Instance-specific reference data | Page number, access date, enumeration district, confidence |

### 2. Notes vs. Attributes

**Prefer Notes over Attributes for**:
- URLs and web addresses
- Access dates and digital provenance
- Location information
- Any data you want to be searchable

**Rationale** (per Gramps community):
- Notes are searchable via Gramps filters
- Source/Citation Attributes have **no GEDCOM equivalent** and won't export
- URLs change; notes allow context and explanation

**Use Attributes for**:
- Structured, typed data (e.g., TYPE, REFN)
- Data that benefits from key-value organization
- Internal categorization not needed in exports

---

## Complete Field Mapping Reference

### Source-Level Fields

| GEDCOM Field | Gramps Target | Format/Notes |
|--------------|---------------|--------------|
| `TITL` | `stitle` | Source title - direct mapping |
| `AUTH` | `sauthor` | Author/creator name |
| `PUBL` | `spubinfo` | Publisher and publication details |
| `TYPE` | `srcattribute TYPE` | Source type classification |
| `REFN` | `srcattribute REFN` | Reference/catalog numbers |
| `REPO` | `reporef` | Repository reference |

### Compound Fields (Require Formatting)

| GEDCOM Fields | Gramps Target | Format Pattern |
|---------------|---------------|----------------|
| `PERI` + `PLAC` + `DATE` + `PAGE` | `spubinfo` | Newspaper: `[PERI] ([PLAC]), [DATE], p. [PAGE]` |
| `INTV` | `sauthor` | Interviewer = author for oral histories |
| `LOCA` + `DATV` | `note` | `Digital access: [LOCA] (accessed [DATV])` |
| `URL` + `DATV` | `note` | `Digital access: [URL] (accessed [DATV])` |

### Citation-Level Fields

| GEDCOM Field | Gramps Target | Format/Notes |
|--------------|---------------|--------------|
| `TEXT` | Parse → `citation.page` | Extract enumeration details, cert numbers, etc. |
| `FILN` | `citation.page` | Certificate/file number: `certificate no. [FILN]` |
| `DETA` | Parse → `citation.page` | Roll/page/ED details |
| `PAGE` | `citation.page` or `spubinfo` | Depends on source type |

---

## Source Type Specific Patterns

### 1. Newspaper/Periodical Articles

**Evidence Explained Pattern**:
```
"[Headline]," [Newspaper Name] ([City, State]), [date], p. [X], col. [Y];
digital image, [Website] (URL : accessed [date]).
```

**Gramps Mapping**:

| Element | Gramps Field | Source |
|---------|--------------|--------|
| Headline | `stitle` | GEDCOM TITL |
| Newspaper + City + Date + Page | `spubinfo` | GEDCOM PERI + PLAC + DATE + PAGE |
| Reporter/byline | `sauthor` | GEDCOM AUTH (if present) |
| Digital access info | `note` | GEDCOM LOCA + DATV |

**spubinfo Format**:
```
[Newspaper Name] ([City], [State]), [Date], p. [Page]
```

**Example**:
```
The Times Recorder (Zanesville, Ohio), 14 Jun 1948, p. 7
```

**Consolidation**: NO - Each article is a distinct source

---

### 2. Census Records

**Evidence Explained Pattern** (Chapter 6):
```
[Year] U.S. census, [State], [County], [Township], population schedule,
ED [X], sheet [Y], dwelling [D], family [F], line [L], [Name];
digital image, [Website] (URL : accessed [date]).
```

**Gramps Mapping**:

| Element | Gramps Field | Notes |
|---------|--------------|-------|
| Census year + title | `stitle` | `[Year] United States Federal Census` |
| Location + enumeration details | `citation.page` | From GEDCOM TEXT or DETA |
| NARA microfilm info | `reporef` | Repository reference |

**citation.page Format**:
```
[State], [County], [Township], ED [X-Y], Sheet [Z], Line [L], Dwelling [D], Family [F]
```

**Key Points**:
- Include full hyphenated ED numbers (e.g., "ED 102-24" not just "ED 24")
- Use stamped page numbers only if sheet numbers are illegible
- Pre-1880 censuses: use page/dwelling/family only (no ED)

**Consolidation**: YES - One source per census year

---

### 3. Vital Records (Birth/Death/Marriage Certificates)

**Evidence Explained Pattern**:
```
[Jurisdiction], [record type], [name], [date],
certificate/file no. [X]; [Repository or digital source].
```

**Gramps Mapping**:

| Element | Gramps Field | Source |
|---------|--------------|--------|
| Record set title | `stitle` | `[State] [Type], [Year Range]` or individual |
| Certificate number | `citation.page` | GEDCOM FILN |
| Repository | `reporef` | Vital records office or digital source |

**citation.page Format**:
```
certificate no. [number]
```

**Example**:
```
certificate no. 26138
```

**Consolidation**: Varies - Can consolidate by state/type or keep individual

---

### 4. Oral History / Interviews

**Evidence Explained Pattern**:
```
[Informant Name], interview by [Interviewer], [date], [location];
[recording/transcript details].
```

**Gramps Mapping**:

| Element | Gramps Field | Source |
|---------|--------------|--------|
| Interview title | `stitle` | `Interview with [Informant Name]` |
| Interviewer | `sauthor` | GEDCOM INTV |
| Date and location | `spubinfo` | GEDCOM DATE + PLAC |
| Recording details | `note` | Additional context |

**Key Point**: The interviewer is the "author" who recorded the information. The informant is named in the title.

**Consolidation**: NO - Each interview is distinct

---

### 5. Find A Grave / Cemetery Databases

**Evidence Explained Pattern**:
```
Find A Grave, database and images (https://www.findagrave.com :
accessed [date]), memorial [number] for [Name] ([birth]–[death]),
[Cemetery], [City], [County], [State].
```

**Gramps Mapping**:

| Element | Gramps Field | Notes |
|---------|--------------|-------|
| Database name | `stitle` | `Find A Grave` |
| Memorial details | `citation.page` | `memorial [number] for [Name], [Cemetery]` |
| Access info | `note` | URL and access date |

**Consolidation**: YES - One source for all Find A Grave entries

---

### 6. Books / Published Genealogies

**Evidence Explained Pattern**:
```
[Author], [Title] (Publisher, Place, Year), page [X].
```

**Gramps Mapping**:

| Element | Gramps Field | Source |
|---------|--------------|--------|
| Book title | `stitle` | GEDCOM TITL |
| Author | `sauthor` | GEDCOM AUTH |
| Publisher info | `spubinfo` | GEDCOM PUBL |
| Page reference | `citation.page` | Specific page(s) |

**Consolidation**: NO - Each book is distinct

---

## Digital Access Documentation

### Format for Notes

When a source was accessed digitally, create a note with this format:

```
Digital access: [Website/Platform] ([URL] : accessed [Date])
```

**Examples**:
```
Digital access: Newspapers.com (http://www.newspapers.com/image/19309759/ : accessed 23 Jun 2014)

Digital access: FamilySearch (https://www.familysearch.org/ark:/61903/1:1:ABCD-1234 : accessed 15 Jan 2024)
```

### Why Notes, Not Attributes?

Per Gramps community consensus:

1. **Searchability**: Notes can be searched via Gramps filters; attributes cannot
2. **GEDCOM Export**: Source Attributes have no GEDCOM equivalent
3. **URL Longevity**: URLs change; notes allow adding context ("previously at...")
4. **Best Practice**: "Record your references in a way that will still be relevant in many years. URLs are useful now but don't last."

---

## Confidence Levels

Map source quality to Gramps confidence:

| Level | Value | Use When |
|-------|-------|----------|
| Very High | 4 | Original record, direct evidence, firsthand knowledge |
| High | 3 | Original record, indirect evidence |
| Normal | 2 | Derivative source, consistent with others (default) |
| Low | 1 | Derivative with potential errors |
| Very Low | 0 | Questionable, unverified, or user-submitted |

---

## Consolidation Decision Framework

### Consolidate Sources When:
- Same creating entity (e.g., U.S. Census Bureau for all federal censuses)
- Same database concept (e.g., all Find A Grave entries)
- Same index/collection (e.g., SSDI, state death indexes)
- Differences can be captured in citation details

### Keep Sources Separate When:
- Different publishers/creators (e.g., city directories from different publishers)
- Each is a distinct publication (e.g., books, newspaper articles)
- Physical documents you possess (e.g., certificates, interview recordings)
- The item itself is unique (e.g., wills, obituaries)

### Consolidation Summary Table

| Source Type | Consolidate? | Title Pattern |
|-------------|--------------|---------------|
| Federal Census | Yes, by year | `[Year] United States Federal Census` |
| State Census | Yes | `[State] State Census, [Year Range]` |
| Vital Record Index | Yes | `[State] [Type], [Year Range]` |
| Individual Certificate | No | `[Person Name] [Record Type]` |
| City Directory | No | `[City], [State], City Directory, [Year]` |
| Newspaper Article | No | `[Headline]` |
| Cemetery (database) | Yes | `Find A Grave` or `BillionGraves` |
| Cemetery (headstone) | Cemetery-level | `[Cemetery], [City], [County], [State]` |
| Interview | No | `Interview with [Person]` |
| SSDI | Yes | `U.S. Social Security Death Index` |

---

## Implementation Notes for Plugin Developers

### Parsing GEDCOM TEXT Fields

The TEXT field often contains embedded citation details that need extraction:

**Census Example**:
```
Ancestry.com. 1920 United States Federal Census [database on-line]. Provo, UT, USA:
Ancestry.com Operations Inc, 2010. Roll: T624_453; Page: 13A; Enumeration District: 0171
```

**Regex Patterns**:
```python
ED_PATTERN = r'Enumeration District[:\s]+(\d+[-\d]*)'
SHEET_PATTERN = r'[Ss]heet[:\s]+(\d+[AB]?)'
LINE_PATTERN = r'[Ll]ine[:\s]+(\d+)'
DWELLING_PATTERN = r'[Dd]welling[:\s]+(\d+)'
FAMILY_PATTERN = r'[Ff]amily[:\s]+(\d+)'
ROLL_PATTERN = r'[Rr]oll[:\s]+([A-Z]?\d+[-_]?\d*)'
PAGE_PATTERN = r'[Pp]age[:\s]+(\d+[AB]?)'
```

### Formatting spubinfo for Newspapers

```python
def format_newspaper_spubinfo(peri: str, plac: str, date: str, page: str) -> str:
    """Format newspaper publication info per Evidence Explained."""
    # Parse place into city, state
    city, state = parse_place(plac)  # Implementation varies

    # Format date (convert to readable format)
    formatted_date = format_date(date)  # e.g., "14 Jun 1948"

    # Build spubinfo
    if city and state:
        location = f"({city}, {state})"
    elif plac:
        location = f"({plac})"
    else:
        location = ""

    parts = [peri]
    if location:
        parts.append(location)
    parts.append(formatted_date)
    if page:
        parts.append(f"p. {page}")

    return ", ".join(filter(None, parts))
```

### Creating Digital Access Notes

```python
def create_digital_access_note(loca: str, url: str, datv: str) -> str:
    """Create a digital access note per EE format."""
    access_point = url or loca
    if not access_point:
        return ""

    # Try to extract website name from URL
    website = extract_website_name(access_point)  # e.g., "Newspapers.com"

    if datv:
        return f"Digital access: {website} ({access_point} : accessed {datv})"
    else:
        return f"Digital access: {website} ({access_point})"
```

---

## References

- Mills, Elizabeth Shown. *Evidence Explained: Citing History Sources from Artifacts to Cyberspace*. 4th ed. Baltimore: Genealogical Publishing Co., 2024.
- [Evidence Explained QuickTips](https://www.evidenceexplained.com/)
- [Gramps Project Wiki](https://gramps-project.org/wiki/)
- [Gramps Discourse Forum](https://gramps.discourse.group/)
