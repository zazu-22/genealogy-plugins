# Gramps Data Model

Understanding Gramps primary objects and their relationships.

## Primary Objects

Gramps organizes genealogical data into ten primary object types. Each is independently stored and cross-referenced via handles.

### Object Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    GRAMPS DATA MODEL                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Person ◄──────┬──────► Family                              │
│     │          │           │                                 │
│     ▼          │           ▼                                 │
│  Event ◄───────┴────► Event (Family events)                 │
│     │                      │                                 │
│     ▼                      ▼                                 │
│  Place                  Place                                │
│     │                      │                                 │
│     └──────► Citation ◄────┘                                │
│                  │                                           │
│                  ▼                                           │
│               Source                                         │
│                  │                                           │
│                  ▼                                           │
│             Repository                                       │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Cross-cutting: Note, Media, Tag (attach to any)      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Person

Represents an individual in the family tree.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique internal identifier |
| gramps_id | User-facing ID (e.g., I0001) |
| gender | Male, Female, Unknown |
| names | List of Name objects (birth, married, aka) |
| events | References to Event objects with roles |
| families | Families where person is parent |
| parent_families | Families where person is child |
| attributes | Custom key-value pairs |

### Name Structure
```
Name
├── type (Birth Name, Married Name, Also Known As, Nickname)
├── first_name
├── surname_list
│   ├── surname
│   ├── prefix
│   └── origin_type (Inherited, Taken, Given, etc.)
├── suffix (Jr., III, etc.)
├── title (Dr., Rev., etc.)
├── call_name
└── nick
```

### Gender Values
- `0` - Female
- `1` - Male
- `2` - Unknown

## Family

Connects individuals as parents and children.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique identifier |
| gramps_id | User-facing ID (e.g., F0001) |
| father | Handle reference to father Person |
| mother | Handle reference to mother Person |
| children | List of ChildRef objects |
| relationship_type | Type of union |
| events | Family events (marriage, divorce) |

### Relationship Types
- `Married` - Legal marriage
- `Unmarried` - Partnership without marriage
- `Civil Union` - Legal civil partnership
- `Unknown` - Relationship type unknown

### Child References
```
ChildRef
├── ref (handle to Person)
├── mrel (mother relationship: Birth, Adopted, Stepchild, Foster, Unknown)
└── frel (father relationship: Birth, Adopted, Stepchild, Foster, Unknown)
```

## Event

Records occurrences in lives of individuals and families.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique identifier |
| gramps_id | User-facing ID (e.g., E0001) |
| type | Event type (Birth, Death, Marriage, etc.) |
| date | Date object (exact, range, approximate) |
| place | Handle reference to Place |
| description | Free-text description |
| participants | Via EventRef from Person/Family |

### Event Types
**Life Events**:
- Birth, Death, Burial, Cremation
- Baptism, Christening, Confirmation
- Bar Mitzvah, Bas Mitzvah

**Personal Events**:
- Occupation, Education, Religion
- Residence, Immigration, Emigration, Naturalization
- Military Service, Retirement

**Family Events**:
- Marriage, Divorce, Annulment
- Engagement, Marriage Banns, Marriage Contract
- Marriage License, Marriage Settlement

**Other**:
- Census, Probate, Will
- Property, Graduation
- Custom types allowed

### Event References
When a Person or Family references an Event:
```
EventRef
├── ref (handle to Event)
├── role (Primary, Witness, Celebrant, Informant, Bride, Groom, etc.)
└── attributes (additional context)
```

## Place

Geographic locations with hierarchical relationships.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique identifier |
| gramps_id | User-facing ID (e.g., P0001) |
| title | Formatted place name |
| names | List of PlaceName objects |
| type | Place type (Country, State, County, City, etc.) |
| coordinates | Latitude and longitude |
| parent | Handle reference to containing place |

### Place Hierarchy
```
Country (USA)
  └── State (Ohio)
       └── County (Muskingum)
            └── City (Zanesville)
                 └── Building (Court House)
```

### PlaceName Structure
```
PlaceName
├── value (the name text)
├── lang (language code: en, de, es)
└── date (when this name was used)
```

## Source

Documentary evidence for genealogical claims.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique identifier |
| gramps_id | User-facing ID (e.g., S0001) |
| title | Source title |
| author | Author/creator |
| pubinfo | Publication information |
| abbreviation | Short reference form |
| repositories | Where source is held |
| attributes | Type, medium, etc. |

### Source vs Citation
```
Source: "1900 U.S. Census"
  ├── Citation: "Page 5, Line 23, John Smith household"
  ├── Citation: "Page 12, Line 8, Mary Jones household"
  └── Citation: "Page 45, Line 1, William Brown household"
```

### GEDCOM Field Mapping (Source-Level)

| GEDCOM Field | Gramps Target | Format/Notes |
|--------------|---------------|--------------|
| `TITL` | `stitle` | Source title - direct mapping |
| `AUTH` | `sauthor` | Author/creator name |
| `PUBL` | `spubinfo` | Publisher and publication details |
| `TYPE` | `srcattribute TYPE` | Source type classification |
| `REFN` | `srcattribute REFN` | Reference/catalog numbers |
| `REPO` | `reporef` | Repository reference |
| `INTV` | `sauthor` | Interviewer = author for oral histories |

### Compound Field Formatting

**Newspapers/Periodicals** (PERI + PLAC + DATE + PAGE → spubinfo):
```
[Newspaper Name] ([City], [State]), [Date], p. [Page]
Example: The Times Recorder (Zanesville, Ohio), 14 Jun 1948, p. 7
```

**Digital Access** (URL + DATV → note):
```
Digital access: [Website] ([URL] : accessed [Date])
```

See `docs/gedcom-gramps-field-mapping.md` for complete guidance.

## Citation

Specific reference to a source for a particular fact.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique identifier |
| gramps_id | User-facing ID (e.g., C0001) |
| source | Handle reference to Source |
| page | Page/location within source |
| date | Date accessed or publication date |
| confidence | Quality rating (0-4) |

### GEDCOM Field Mapping (Citation-Level)

| GEDCOM Field | Gramps Target | Format/Notes |
|--------------|---------------|--------------|
| `TEXT` | Parse → `citation.page` | Extract enumeration details, cert numbers |
| `FILN` | `citation.page` | Certificate/file number: `certificate no. [FILN]` |
| `DETA` | Parse → `citation.page` | Roll/page/ED details |
| `PAGE` | `citation.page` or `spubinfo` | Depends on source type |

### Citation Page Formats by Source Type

**Census Records**:
```
[State], [County], [Township], ED [X-Y], Sheet [Z], Line [L], Dwelling [D], Family [F]
```

**Vital Records**:
```
certificate no. [number]
```

**Find A Grave**:
```
memorial [number] for [Name], [Cemetery]
```

### Confidence Levels
| Value | Level | Use When |
|-------|-------|----------|
| 0 | Very Low | Questionable, unverified, or user-submitted |
| 1 | Low | Derivative with potential errors |
| 2 | Normal | Derivative source, consistent with others (default) |
| 3 | High | Original record, indirect evidence |
| 4 | Very High | Original record, direct evidence, firsthand knowledge |

## Repository

Physical or virtual location where sources are held.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique identifier |
| gramps_id | User-facing ID (e.g., R0001) |
| name | Repository name |
| type | Archive, Library, Church, Website, etc. |
| address | Physical address |
| urls | Web addresses |

### Repository Reference
Sources link to repositories via:
```
RepoRef
├── ref (handle to Repository)
├── callno (call number/catalog number)
└── medium (Original, Photocopy, Microfilm, Digital, etc.)
```

## Note

Text annotations attached to any object.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique identifier |
| gramps_id | User-facing ID (e.g., N0001) |
| type | General, Research, Transcript, etc. |
| text | Styled text content |
| format | Plain text, styled, or HTML |

### Note Types
- `General` - General notes
- `Research` - Research notes and analysis
- `Transcript` - Document transcriptions
- `Source text` - Quoted source content
- `Citation` - Citation-specific notes

### Note-Citation Limitation

**Critical:** Gramps notes cannot have citations attached. This is a structural limitation in the Gramps DTD:

```
note = (text, style*, tagref*)
```

Note the absence of `citationref` in the element definition. This has important implications:

**Impact on GEDCOM Import:**
- GEDCOM notes with source references (`2 SOUR @Sxx@`) lose those links when imported into Gramps
- There is no way to preserve note→source relationships in the Gramps data model
- Users may not realize data was lost during import

**Impact on Research Workflow:**
- Research analysis notes that reference multiple sources cannot formally cite those sources within Gramps
- The Source-Citation model only flows: Person/Event → Citation → Source (not Note → Citation)

**Workarounds:**

| Approach | When to Use | Example |
|----------|-------------|---------|
| **Cite on events** | Analysis relates to specific events | Birth year analysis → cite sources on Birth event |
| **Obsidian notes** | Complex proof arguments | Full GPS-compliant proof with footnotes |
| **Inline references** | Quick informal notes | "per 1900 Census [S0003]" in note text |
| **Note linking** | Cross-reference analysis | "See Obsidian: Research/Birth-Year-Analysis.md" |

**Best Practice:** For significant research conclusions:
1. Record facts and dates in Gramps (with citations on events)
2. Write detailed analysis in Obsidian (with proper footnotes)
3. Add a Gramps note referencing the Obsidian document

### Notes vs Attributes for GEDCOM Export

**Prefer Notes** for:
- URLs and web addresses
- Access dates and digital provenance
- Location information
- Any data you want to be searchable

**Rationale** (per Gramps community):
- Notes are searchable via Gramps filters
- Source/Citation Attributes have **no GEDCOM equivalent** and won't export
- URLs change; notes allow context and explanation

**Use Attributes** for:
- Structured, typed data (e.g., TYPE, REFN)
- Data that benefits from key-value organization
- Internal categorization not needed in exports

**Digital Access Note Format**:
```
Digital access: [Website] ([URL] : accessed [Date])
```

## Media

Files associated with genealogical records.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique identifier |
| gramps_id | User-facing ID (e.g., O0001) |
| path | File path (relative to media directory) |
| mime | MIME type |
| description | Description of media |
| date | Date of media (photo date, etc.) |
| checksum | File integrity hash |

### Media References
Objects reference media via:
```
MediaRef
├── ref (handle to Media)
├── rect (crop region: x1, y1, x2, y2)
└── attributes (additional metadata)
```

## Tag

Colored labels for organization.

### Attributes
| Attribute | Description |
|-----------|-------------|
| handle | Unique identifier |
| name | Tag name |
| color | Hex color code |
| priority | Sort order |

## Handle Reference System

### How Handles Work
1. Every object has a unique handle (stable internal ID)
2. Cross-references use handle values
3. IDs (I0001, F0001) are user-facing only
4. Handles survive merge operations

### Reference Types
```
Direct references (hlink attribute):
  - place="handle"      (Event → Place)
  - sourceref="handle"  (Citation → Source)

Reference objects (complex relationships):
  - EventRef (Person/Family → Event)
  - ChildRef (Family → Person)
  - MediaRef (Any → Media)
  - RepoRef (Source → Repository)
```

## Data Integrity

### Referential Integrity
Gramps maintains referential integrity:
- Deleting a referenced object prompts for resolution
- Orphaned references are cleaned up
- Merge operations update all references

### Validation
Check for common issues:
- Persons without events
- Citations without sources
- Events without dates or places
- Sources without citations (unused)
