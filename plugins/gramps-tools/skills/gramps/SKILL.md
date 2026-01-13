---
name: gramps
description: Working with Gramps genealogy software - XML structure, database queries, Web API, data model, and best practices. Use when analyzing Gramps exports, querying the database, understanding data structure, or following Gramps methodology.
---

# Gramps Genealogy Software

Expert knowledge for working with Gramps, the open-source genealogy application.

## IMPORTANT: API-First Workflow

**Primary method for Gramps database access:** Gramps Web REST API

| Aspect | Details |
|--------|---------|
| **API Endpoint** | `http://localhost:5000/api/` |
| **Credentials** | `~/.config/grampsweb/credentials.json` |
| **Authentication** | JWT token via `/api/token/` |

**Why API over CLI/XML:**
- Gramps CLI (`gramps` command) is unreliable on macOS
- XML import creates duplicates (adds data, doesn't merge)
- API allows incremental, verifiable changes with undo support
- Transaction history enables rollback via `/api/transactions/history/{id}/undo`

**Data Access Methods:**

| Method | Use Case | Preference |
|--------|----------|------------|
| REST API | Single record CRUD, searches, queries | **Primary** |
| API Export | Bulk XML export via `/api/exporters/gramps` | Secondary (bulk analysis) |
| CLI Export | User-managed backup scripts only | Legacy |

See [lib/web-api.md](lib/web-api.md) for full API documentation.

## Recommended Implementation Library

**For all Gramps Web API interactions, use the GrampsAPIClient library.**

The gramps_plugins project includes a production-ready API client at:
`~/code/personal/gramps_plugins/lib/gramps_web_client/`

### Why Use GrampsAPIClient

- **Automatic authentication** - Loads credentials from `~/.config/grampsweb/credentials.json`
- **JWT token refresh** - Handles expired tokens transparently
- **Type-safe methods** - Clean, typed interfaces for common operations
- **Dry-run mode** - Test operations safely without modifying data
- **Error handling** - Comprehensive exception handling with typed errors
- **Pagination support** - Built-in limit/offset for large datasets

### Installation

For projects in `~/Genealogy`:

```bash
cd ~/Genealogy/<project>
uv add --editable ~/code/personal/gramps_plugins
```

### Quick Example

```python
from gramps_web_client import GrampsAPIClient

# Automatic credential loading
client = GrampsAPIClient()

# Fetch sources with pagination
sources = client.get_sources(limit=10, offset=0)

# Update a source
client.update_source(handle, {"title": "New Title"})

# Dry-run mode for testing
client = GrampsAPIClient(dry_run=True)
client.create_source(data)  # Logs but doesn't execute
```

### Real-World Examples

See production usage in:
- `tools/census_migration/cli.py` - Census source migration
- `tools/census_migration/migrator.py` - Bulk updates
- `tools/census_migration/deduplicator.py` - Citation merging

**Always prefer GrampsAPIClient over raw urllib/requests code.**

## Critical Limitation: Notes Cannot Have Citations

**Gramps notes cannot be formally cited.** The Gramps DTD defines notes as `(text, style*, tagref*)` - there is no `citationref` element allowed. This means:

- GEDCOM notes with source references (2 SOUR @Sxx@) **lose those links on import**
- You cannot attach citations to notes in Gramps
- Research analysis notes require alternative approaches

**Workarounds for Research Notes:**
1. **Cite sources on relevant events** - If a note analyzes birth year evidence, cite those sources on the Birth event instead
2. **Move analysis to Obsidian** - Use Obsidian for proof arguments with proper footnotes (see `obsidian-genealogy` skill)
3. **Inline text references** - Add source IDs as text within the note (e.g., "per 1900 Census [S0003]")

See [lib/data-model.md](lib/data-model.md#note-citation-limitation) for full details.

## When This Skill Applies

- **Querying or modifying Gramps data via REST API** (primary method)
- Working with Gramps Web API endpoints
- Analyzing Gramps XML exports for bulk operations
- Understanding Gramps data model and primitives
- Following Gramps best practices for data entry

## Core Concepts

### Primary Objects
Gramps organizes genealogical data into **primary objects**:

| Object | Purpose | Key Attributes |
|--------|---------|----------------|
| Person | Individual in the tree | gender, names, events, attributes |
| Family | Connects parents to children | relationship type, father, mother, children |
| Event | Dated occurrences | type, date, place, participants |
| Place | Geographic locations | name, coordinates, hierarchy |
| Source | Documentary evidence | title, author, publication info |
| Citation | Specific reference to a source | page/detail, confidence, source link |
| Repository | Where sources are held | name, type, address |
| Note | Text annotations | styled text, links |
| Media | Files (photos, documents) | file path, attributes |
| Tag | Colored labels | name, color, priority |

### Handle System
Every object has a unique **handle** (internal ID) used for cross-references:
- Handles are stable identifiers (e.g., `_1011e191a5cf4cdac1ddc8d618bd`)
- Links use `hlink` attribute to reference handles
- IDs (e.g., `I0001`, `F0001`) are user-facing but not used for linking

### Source-Citation Model
Gramps separates sources from citations:
- **Source**: The document itself (e.g., "1900 U.S. Census")
- **Citation**: Specific reference (e.g., page number, entry details)
- One source can have many citations
- Citations link to events/persons, not sources directly

## Quick Reference

### File Formats
- `.gramps` - Gzipped XML (primary export format)
- `.gpkg` - Portable package (XML + media in tar.gz)
- Database: SQLite at `~/.local/share/containers/grampsweb/db/`

### Project-Specific Info
- Tree name: "Shaffer-Richardson"
- Backups: `~/Genealogy/Exports/gramps-backups/`
- Gramps Web: `http://localhost:5000` (Docker container)

## Reference Materials

For detailed information, see:

| Topic | File | Keywords |
|-------|------|----------|
| XML Format | [lib/xml-structure.md](lib/xml-structure.md) | xml, export, elements, tags, DTD |
| Database Schema | [lib/database-schema.md](lib/database-schema.md) | sqlite, tables, queries, SQL |
| Web API | [lib/web-api.md](lib/web-api.md) | REST, endpoints, docker, sync |
| Data Model | [lib/data-model.md](lib/data-model.md) | person, family, event, primitives |
| Best Practices | [lib/best-practices.md](lib/best-practices.md) | methodology, data entry, standards |

## Related Skills

- `source-analysis` - Evaluating sources and evidence
- `evidence-explained` - Citation formatting
- `genealogical-proof-standard` - Proof methodology
