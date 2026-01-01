# Gramps Database Schema

Reference for the Gramps SQLite database structure.

## Database Location

```
~/.local/share/containers/grampsweb/db/        # Gramps Web container
~/.gramps/grampsdb/[tree-name]/                # Gramps Desktop (varies by OS)
```

## Architecture

Gramps uses SQLite with a hybrid storage model:
- **Metadata** stored in structured tables
- **Object data** stored as pickled Python objects in BLOBs
- All data accessible via XML export (recommended for querying)

## Primary Tables

### person
```sql
CREATE TABLE person (
    handle TEXT PRIMARY KEY,
    gramps_id TEXT,
    gender INTEGER,
    primary_name TEXT,    -- Pickled Name object
    alternate_names TEXT, -- Pickled list
    death_ref_index INTEGER,
    birth_ref_index INTEGER,
    event_ref_list TEXT,  -- Pickled references
    family_list TEXT,
    parent_family_list TEXT,
    media_list TEXT,
    address_list TEXT,
    attribute_list TEXT,
    urls TEXT,
    lds_ord_list TEXT,
    citation_list TEXT,
    note_list TEXT,
    change INTEGER,       -- Unix timestamp
    tag_list TEXT,
    private INTEGER
);
```

### family
```sql
CREATE TABLE family (
    handle TEXT PRIMARY KEY,
    gramps_id TEXT,
    father_handle TEXT,
    mother_handle TEXT,
    child_ref_list TEXT,  -- Pickled child references
    type INTEGER,         -- Relationship type
    event_ref_list TEXT,
    media_list TEXT,
    attribute_list TEXT,
    lds_ord_list TEXT,
    citation_list TEXT,
    note_list TEXT,
    change INTEGER,
    tag_list TEXT,
    private INTEGER
);
```

### event
```sql
CREATE TABLE event (
    handle TEXT PRIMARY KEY,
    gramps_id TEXT,
    the_type INTEGER,     -- Event type enum
    date TEXT,            -- Pickled Date object
    description TEXT,
    place TEXT,           -- Place handle
    citation_list TEXT,
    note_list TEXT,
    media_list TEXT,
    attribute_list TEXT,
    change INTEGER,
    tag_list TEXT,
    private INTEGER
);
```

### place
```sql
CREATE TABLE place (
    handle TEXT PRIMARY KEY,
    gramps_id TEXT,
    title TEXT,
    long TEXT,            -- Longitude
    lat TEXT,             -- Latitude
    place_ref_list TEXT,  -- Parent place references
    name TEXT,            -- Pickled PlaceName
    alt_names TEXT,
    place_type INTEGER,
    code TEXT,
    alt_loc TEXT,
    urls TEXT,
    media_list TEXT,
    citation_list TEXT,
    note_list TEXT,
    change INTEGER,
    tag_list TEXT,
    private INTEGER
);
```

### source
```sql
CREATE TABLE source (
    handle TEXT PRIMARY KEY,
    gramps_id TEXT,
    title TEXT,
    author TEXT,
    pubinfo TEXT,
    abbrev TEXT,
    note_list TEXT,
    media_list TEXT,
    attribute_list TEXT,
    reporef_list TEXT,
    change INTEGER,
    tag_list TEXT,
    private INTEGER
);
```

### citation
```sql
CREATE TABLE citation (
    handle TEXT PRIMARY KEY,
    gramps_id TEXT,
    date TEXT,            -- Pickled Date object
    page TEXT,
    confidence INTEGER,   -- 0-4 scale
    source_handle TEXT,
    note_list TEXT,
    media_list TEXT,
    attribute_list TEXT,
    change INTEGER,
    tag_list TEXT,
    private INTEGER
);
```

## Querying the Database

### Basic Queries

**Count records**:
```sql
SELECT COUNT(*) FROM person;
SELECT COUNT(*) FROM family;
SELECT COUNT(*) FROM event;
SELECT COUNT(*) FROM source;
```

**Find person by ID**:
```sql
SELECT handle, gramps_id, gender FROM person WHERE gramps_id = 'I0001';
```

**List all sources**:
```sql
SELECT gramps_id, title, author FROM source ORDER BY title;
```

**Recent changes**:
```sql
SELECT gramps_id, title, datetime(change, 'unixepoch') as modified
FROM source
ORDER BY change DESC
LIMIT 10;
```

### Relationship Queries

**Family connections**:
```sql
SELECT
    f.gramps_id as family_id,
    p1.gramps_id as father_id,
    p2.gramps_id as mother_id
FROM family f
LEFT JOIN person p1 ON f.father_handle = p1.handle
LEFT JOIN person p2 ON f.mother_handle = p2.handle;
```

**Events for a person** (complex due to pickled data):
```sql
-- Better to use XML export for this type of query
```

## Limitations

### Pickled Data
Most relationship data is stored as pickled Python objects:
- Not directly queryable with SQL
- Requires Python to deserialize
- **Recommendation**: Use XML export for complex queries

### Best Approach
For data analysis:
1. Export to XML (uncompressed)
2. Use Python/xpath for complex queries
3. Or use Gramps Web API for structured access

## Backup Considerations

**Direct SQLite backup**:
```bash
# NOT recommended for archival
sqlite3 ~/.gramps/grampsdb/tree/sqlite.db ".backup backup.db"
```

**Recommended approach**:
```bash
# Export to XML for version control
gramps -O "Tree-Name" -e export.gramps -f gramps-xml
```

## Connection Example

```python
import sqlite3

db_path = "~/.local/share/containers/grampsweb/db/sqlite.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Simple query
cursor.execute("SELECT gramps_id, title FROM source LIMIT 5")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")

conn.close()
```

## Integrity Checks

```sql
-- Check for orphaned citations
SELECT c.gramps_id
FROM citation c
LEFT JOIN source s ON c.source_handle = s.handle
WHERE s.handle IS NULL;

-- Check for events without dates
SELECT gramps_id, description FROM event WHERE date IS NULL;
```
