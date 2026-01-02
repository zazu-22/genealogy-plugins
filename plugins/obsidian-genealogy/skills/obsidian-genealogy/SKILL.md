---
name: obsidian-genealogy
description: Working with Obsidian genealogy vaults - Canvas Roots integration, frontmatter patterns, person/source/place notes, and vault structure. Use when creating or editing person notes, linking Gramps data to Obsidian, working with Canvas Roots imports, or managing genealogy research notes.
---

# Obsidian Genealogy Vault

Expert knowledge for working with genealogy research vaults in Obsidian, integrated with Gramps via Canvas Roots.

## When This Skill Applies

- Creating or editing person notes in Obsidian
- Working with Canvas Roots GEDCOM/Gramps imports
- Managing source and place notes
- Linking research narratives to genealogical data
- Structuring frontmatter for genealogy notes

## Vault Structure

The genealogy vault follows this organization:

| Directory | Purpose | Note Type |
|-----------|---------|-----------|
| `People/` | Individual person profiles | Person notes |
| `Sources/` | Documentary evidence | Source notes |
| `Places/` | Geographic locations | Place notes |
| `Events/` | Significant occurrences | Event notes |
| `Research/` | Analysis and narratives | Research notes |
| `Canvas/` | Visual family trees | Canvas files |
| `Templates/` | Note templates | Template files |

## Person Notes

### Filename Convention
```
Firstname Lastname (birth_year-death_year).md
Firstname Lastname (b. birth_year).md  # living persons
```

### Required Frontmatter
```yaml
---
type: person
gramps_id: I0001
cr_id: unique-canvas-roots-id  # if imported via Canvas Roots
birth_date: 1850-03-15
death_date: 1920-07-22
father: "[[Father Name]]"
mother: "[[Mother Name]]"
---
```

### Linking Conventions
- Use wikilinks for family relationships: `[[Person Name]]`
- Reference sources with: `[[Source Title]]`
- Link places with: `[[Place Name]]`

## Source Notes

Follow Evidence Explained citation format:

```yaml
---
type: source
source_type: census | vital | church | land | newspaper
repository: "Name of Archive"
citation: "Full EE-style citation"
access_date: 2024-01-15
---
```

## Place Notes

Use hierarchical naming (specific → general):

```yaml
---
type: place
hierarchy: "Zanesville, Muskingum County, Ohio, USA"
coordinates: [39.9404, -82.0132]
---
```

Include:
- Historical context
- Jurisdictional changes
- Available record types
- Research repositories

## Canvas Roots Integration

Canvas Roots imports GEDCOM/Gramps XML and creates person notes automatically.

### Preserving Imports
- Never delete the `cr_id` frontmatter field
- Maintain wikilink format for relationships
- Canvas Roots uses `cr_id` for robust linking

### Re-syncing
When Gramps data changes:
1. Export fresh GEDCOM from Gramps
2. Re-import via Canvas Roots
3. Canvas Roots updates existing notes by `cr_id`

## Project-Specific Info

- Vault location: `~/Genealogy/Obsidian/`
- Family focus: Shaffer-Richardson
- Geographic focus: Ohio (Zanesville/Muskingum), Kentucky, Illinois
- Origins: Irish, Scottish, German

## Gramps Data Access

When syncing from Gramps to Obsidian:

| Operation | Recommended Method |
|-----------|-------------------|
| Full tree sync | XML export file or API export endpoint |
| Single person lookup | REST API query by gramps_id |
| Verify changes | REST API query |

See `gramps` skill (gramps-tools plugin) for API authentication and endpoints.

**Credentials**: `~/.config/grampsweb/credentials.json`

## Reference Materials

For detailed information, see:

| Topic | File | Keywords |
|-------|------|----------|
| Frontmatter Schema | [lib/frontmatter-schema.md](lib/frontmatter-schema.md) | yaml, metadata, fields |
| Vault Structure | [lib/vault-structure.md](lib/vault-structure.md) | directories, organization |
| Canvas Roots | [lib/canvas-roots.md](lib/canvas-roots.md) | import, gedcom, sync |

## Common Skill Combinations

| Task | Primary Skill | Supporting Skills |
|------|--------------|-------------------|
| Import GEDCOM data | `obsidian-genealogy` | `gramps` (export) |
| Create research note | `obsidian-genealogy` | `genealogical-proof-standard`, `source-analysis` |
| Write proof argument | `genealogical-proof-standard` | `obsidian-genealogy` (research schema) |
| Link Gramps to Obsidian | `gramps` | `obsidian-genealogy` (canvas-roots) |
| Document source analysis | `source-analysis` | `obsidian-genealogy` (evidence tables) |

## Related Skills

- `evidence-explained` - Citation formatting for source notes
- `gramps` - Source data for person notes
- `research-planning` - Structuring research narratives
- `genealogical-proof-standard` - GPS-compliant research notes
- `source-analysis` - Classifying sources for research notes
