---
name: gramps
description: Working with Gramps genealogy software - XML structure, database queries, Web API, data model, and best practices. Use when analyzing Gramps exports, querying the database, understanding data structure, or following Gramps methodology.
---

# Gramps Genealogy Software

Expert knowledge for working with Gramps, the open-source genealogy application.

## When This Skill Applies

- Analyzing or modifying Gramps XML exports (.gramps files)
- Querying the Gramps SQLite database
- Working with Gramps Web API
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
