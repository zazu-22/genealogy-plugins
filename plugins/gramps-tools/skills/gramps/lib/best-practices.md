# Gramps Best Practices

Standards and methodology for high-quality genealogical data in Gramps.

## Data Entry Standards

### Names

**Full Names**:
- Enter first names as recorded in sources
- Use consistent capitalization (Title Case)
- Record nicknames in the "Nick" field, not in parentheses
- Use separate name records for different name forms

**Example**:
```
Birth Name:     John William SMITH
Also Known As:  Jack SMITH
Married Name:   John William SMITH (unchanged for males typically)
Nickname field: Jack (not "(Jack)")
```

**Surname Conventions**:
- Uppercase surnames in displays is optional (Gramps setting)
- Record maiden names for women as Birth Name
- Add married names as separate name records with type "Married Name"

**Prefixes and Suffixes**:
- Prefixes: von, van, de, O' → in surname prefix field
- Suffixes: Jr., Sr., III, PhD → in suffix field
- Titles: Dr., Rev., Col. → in title field

### Dates

**Standard Format**:
- Gramps accepts multiple formats; use consistently
- Preferred: `15 Mar 1850` (day month year)
- Acceptable: `1850-03-15` (ISO format)

**Uncertain Dates**:
| Situation | Gramps Date Type | Example |
|-----------|-----------------|---------|
| Exact date known | Regular | 15 Mar 1850 |
| Approximate | About | about 1850 |
| Before a date | Before | before 1850 |
| After a date | After | after 1850 |
| Date range | Range | between 1850 and 1860 |
| Date span | Span | from Jan 1850 to Dec 1850 |
| Text only | Text | "Spring 1850" |

**Date Quality**:
- Don't guess exact dates; use qualifiers
- Record date as stated in source, add calculated date as separate note
- Conflicting dates should use the most reliable source

### Places

**Hierarchy**:
Always build place hierarchy from specific to general:
```
Zanesville (City)
  └── Muskingum County (County)
       └── Ohio (State)
            └── USA (Country)
```

**Place Names**:
- Use historical names appropriate to the time period
- Add alternate names with date ranges
- Include postal codes where relevant

**Coordinates**:
- Add coordinates for specific locations (cemeteries, buildings)
- Use decimal degrees (not degrees/minutes/seconds)
- Verify accuracy with mapping tools

**Place Types**:
Select the most specific applicable type:
- Country, State, Province, Region
- County, Department, District
- City, Town, Village, Parish
- Building, Farm, Cemetery, Church

### Events

**One Event Per Occurrence**:
- Don't combine multiple events
- Each birth, marriage, death gets its own event

**Event Descriptions**:
- Use description field for additional detail
- Don't duplicate information available elsewhere
- Example: Occupation description = "President, Bloomer Candy Company"

**Roles**:
- Primary: The main subject of the event
- Witness: Observed/attested but not subject
- Informant: Provided information about event
- Celebrant: Officiated (for ceremonies)

## Source Documentation

### Source Structure

**Every fact needs a citation**:
- Birth dates → Citation to birth record or equivalent
- Names → Citation to source where name appears
- Relationships → Citation establishing the connection

**Source vs. Citation**:
```
Source: Create ONE source per distinct original
  Example: "1900 United States Federal Census"

Citation: Create per specific reference
  Example: "Ohio, Muskingum County, ED 123, Sheet 5, Line 23"
```

### Source Types

Classify sources using the TYPE attribute:
- `Census` - Population enumeration
- `Vital Record` - Birth, marriage, death certificates
- `Church Record` - Baptism, marriage, burial registers
- `Newspaper` - Obituaries, announcements
- `Probate` - Wills, estate records
- `Military` - Service records, pension files
- `Land Record` - Deeds, grants
- `Interview` - Oral history

### Source Title Patterns

Align source titles with Evidence Explained methodology and decide consolidation level:

| Source Type | Title Pattern | Consolidate? |
|-------------|--------------|--------------|
| Federal Census | `[Year] United States Federal Census` | Yes, one per year |
| State Census | `[State] State Census, [Year Range]` | Yes |
| Vital Index/DB | `[State] [Type], [Year Range]` | Yes |
| City Directory | `[City], [State], City Directory, [Year]` | No (each is distinct) |
| Newspaper | `[Headline]` | No (each is distinct) |
| Cemetery | `[Cemetery], [City], [County], [State]` | Cemetery-level |
| Interview | `Interview with [Person]` | No |
| Find A Grave | `Find A Grave` | Yes (one source) |
| SSDI | `U.S. Social Security Death Index, [Years]` | Yes (one source) |
| Social Media | `[Person], Personal Page, [Platform]` | No |

**Consolidation Rationale**:
- **Consolidate**: Same creating entity, same database concept, differences in citations
- **Keep separate**: Different publishers, distinct publications, physical documents

### Citation Best Practices

**Page/Location Field**:
Include enough detail to find the exact entry:
```
Page 5, Line 23, Dwelling 42, Family 45
Roll 1234, Frame 567
Volume 12, Page 345
```

**Confidence Levels**:
- 4 (Very High): Original record, direct evidence
- 3 (High): Original record, indirect evidence
- 2 (Normal): Derivative source, consistent with other sources
- 1 (Low): Derivative with potential errors
- 0 (Very Low): Questionable or unsupported

**Access Information**:

**IMPORTANT: Use Notes, Not Attributes** for digital access information:

Per Gramps community best practices, prefer Notes over Attributes for:
- URLs and web addresses
- Access dates and digital provenance
- Location information

**Rationale**:
- Notes are searchable via Gramps filters
- Source/Citation Attributes have **no GEDCOM equivalent** and won't export
- URLs change; notes allow context (e.g., "previously at...")
- Best practice: "Record your references in a way that will still be relevant in many years. URLs are useful now but don't last."

**Use Attributes** only for:
- Structured, typed data (e.g., TYPE, REFN)
- Data that benefits from key-value organization
- Internal categorization not needed in GEDCOM exports

**Digital Access Note Format**:
```
Digital access: [Website] ([URL] : accessed [Date])
```

**Examples**:
```
Digital access: Newspapers.com (http://www.newspapers.com/image/19309759/ : accessed 23 Jun 2014)

Digital access: FamilySearch (https://www.familysearch.org/ark:/61903/1:1:ABCD-1234 : accessed 15 Jan 2024)
```

See `docs/gedcom-gramps-field-mapping.md` for complete GEDCOM-Gramps field mapping guidance

## Relationship Recording

### Family Types

**Use Appropriate Relationship**:
- Married: Legal/religious ceremony documented
- Unmarried: Children born without marriage documentation
- Civil Union: Legal partnership other than marriage
- Unknown: Relationship cannot be determined

### Child Relationships

**Mother/Father Relationship Types**:
- Birth: Biological child
- Adopted: Legal adoption
- Stepchild: Child of spouse from prior relationship
- Foster: Temporary care
- Unknown: Relationship unclear

**Recording Adoptions**:
- Create two family records if both biological and adoptive parents known
- Birth family: frel=Birth, mrel=Birth
- Adoptive family: frel=Adopted, mrel=Adopted

### Handling Conflicts

**Multiple Marriages**:
- Create separate Family records for each marriage
- Link person to multiple families via "parentin"

**Unknown Parents**:
- Create family with only one parent if other unknown
- Don't create placeholder persons

## Notes and Research

### Note Types

**General Notes**:
- Observations about the person/family
- Context not fitting elsewhere

**Research Notes**:
- Analysis and reasoning
- Questions to investigate
- Search strategies attempted

**Transcripts**:
- Exact text from sources
- Preserve original spelling/grammar
- Indicate illegible portions with [?] or [illegible]

### Research Documentation

**Document Your Process**:
- Record searches with negative results
- Note sources consulted that didn't help
- Track research questions

**Add Context**:
- Historical background
- Migration patterns
- Family circumstances

## Media Best Practices

### File Organization

**Directory Structure**:
```
Media/
├── Documents/      # Certificates, records
├── Photos/         # Photographs
├── DNA/           # DNA results, reports
└── Research/      # Research materials
```

### File Naming

**Consistent Convention**:
```
SURNAME_Given_Type_YYYY.ext
SMITH_John_BirthCert_1850.jpg
JONES_Mary_Portrait_1920.jpg
```

### Linking Media

**Attach to Most Specific Object**:
- Birth certificate → Birth event
- Marriage photo → Marriage event
- Portrait → Person
- Family photo → Family

**Use Regions**:
- Crop to specific individual in group photos
- Reference same image multiple times with different crops

## Tags for Organization

### Suggested Tags

| Tag | Color | Purpose |
|-----|-------|---------|
| Needs Research | Red | Incomplete/questionable |
| DNA Confirmed | Green | DNA evidence supports |
| Brick Wall | Orange | Research stuck |
| Review | Yellow | Needs verification |
| Complete | Blue | Fully documented |

### Tag Workflow

1. New persons get "Needs Research"
2. As sources added, move toward "Review"
3. After verification, apply "Complete"
4. Problem areas get "Brick Wall"

## Quality Checks

### Regular Audits

**Check for**:
- Persons without birth/death events
- Events without dates
- Events without places
- Citations with low confidence
- Sources without citations (orphaned)
- Duplicate persons/places

**Use Gramps Tools**:
- Verify > Integrity > Verify the Data
- Tools > Utilities > Unused Objects
- Tools > Family Tree Processing > Check and Repair

### Before Export

1. Run integrity check
2. Review low-confidence citations
3. Verify media paths are valid
4. Check for private data flags

## Import/Export (API-First Workflow)

### Primary Method: GrampsAPIClient

**Always use GrampsAPIClient for Gramps Web API interactions.**

All Gramps data modifications should use the GrampsAPIClient library:

```python
from gramps_web_client import GrampsAPIClient

# Automatic credential loading from ~/.config/grampsweb/credentials.json
client = GrampsAPIClient()

# Create a new source
source_data = {
    "_class": "Source",
    "title": "1900 United States Federal Census",
    "author": "U.S. National Archives and Records Administration"
}
result = client.create_source(source_data)
print(f"Created source with handle: {result['handle']}")

# Update a source (automatic full object merge)
client.update_source(handle, {"title": "Updated Title"})

# Get sources with pagination
sources = client.get_sources(limit=100, offset=0)
for source in sources:
    print(f"{source['gramps_id']}: {source['title']}")
```

### Dry-Run Testing

Always test migrations and bulk operations with dry-run mode first:

```python
# Test the operation
client = GrampsAPIClient(dry_run=True)
for source in sources_to_update:
    client.update_source(source["handle"], {"title": new_title})
    # Logs: "DRY RUN: Would update source..."

# Verify the output, then execute for real
client = GrampsAPIClient(dry_run=False)
for source in sources_to_update:
    client.update_source(source["handle"], {"title": new_title})
```

### Error Handling

Use typed exceptions for robust error handling:

```python
from gramps_web_client import GrampsAPIClient, NotFoundError, AuthenticationError

client = GrampsAPIClient()

try:
    source = client.get_source(handle)
except NotFoundError:
    print(f"Source {handle} not found")
except AuthenticationError:
    print("Authentication failed - check credentials")
```

### Real-World Example: Census Migration

See production usage in `~/code/personal/gramps_plugins/tools/census_migration/`:

```python
# Example from migrator.py
client = GrampsAPIClient(dry_run=args.dry_run)

for source in sources_to_migrate:
    # Update source title to EE-compliant format
    new_title = f"{year} United States Federal Census - {state}"

    try:
        result = client.update_source(source["handle"], {"title": new_title})
        print(f"✓ Updated {source['gramps_id']}")
    except Exception as e:
        print(f"✗ Failed to update {source['gramps_id']}: {e}")
```

### Undo Support

API changes can be undone via transaction history (requires direct API call - not yet in GrampsAPIClient):

```python
# For undo operations, use direct API (not yet wrapped by client)
# See web-api.md for transaction history patterns
```

### Gramps CLI (Deprecated for Claude Code)

**WARNING**: The Gramps CLI is unreliable on macOS and XML import creates duplicates.

The following CLI patterns are **deprecated for Claude Code use**:
- `gramps -O "tree" -e file.gramps -f gramps-xml` - Use API export instead
- `gramps -O "tree" -i file.gramps` - **DO NOT USE** - creates duplicates
- `gramps -C "tree"` - Create via API or Gramps Desktop

CLI may still be used for:
- User-maintained backup scripts (external to Claude Code)
- Desktop-only operations performed manually by the user
