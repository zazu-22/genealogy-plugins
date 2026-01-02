# Canvas Roots Integration

Working with the Canvas Roots Obsidian plugin for GEDCOM/Gramps integration.

## Overview

Canvas Roots is an Obsidian community plugin that:
- Imports GEDCOM files into Obsidian notes
- Creates visual family tree canvases
- Maintains robust linking via unique IDs
- Supports re-syncing when source data changes

## Installation

1. Open Obsidian Settings → Community Plugins
2. Browse and search for "Canvas Roots"
3. Install and enable the plugin
4. Configure import settings as needed

## Importing GEDCOM

### From Gramps

1. Export from Gramps:
   ```
   Family Trees → Export → GEDCOM
   ```

2. In Obsidian:
   ```
   Command Palette → Canvas Roots: Import GEDCOM
   ```

3. Select the exported `.ged` file

4. Canvas Roots creates:
   - Person notes in `People/` directory
   - Family relationship links
   - Visual canvas (optional)

### Import Options

| Option | Recommended | Purpose |
|--------|-------------|---------|
| Create person notes | Yes | Generate individual markdown files |
| Include events | Yes | Birth, death, marriage dates |
| Create canvas | Optional | Visual tree diagram |
| Link style | Wikilinks | Obsidian-native linking |

## The cr_id Field

Canvas Roots assigns a unique `cr_id` to each imported person:

```yaml
---
type: person
cr_id: "abc123def456"  # Canvas Roots ID
gramps_id: "I0001"     # Gramps ID
---
```

### Critical Rules

1. **Never delete cr_id**: Canvas Roots uses it to identify notes during re-sync
2. **Never manually edit cr_id**: It's managed by Canvas Roots
3. **Preserve on manual edits**: When editing person notes, keep cr_id intact

### Re-sync Behavior

When you re-import a GEDCOM:
- Notes with matching `cr_id` are updated
- New persons get new notes
- Deleted persons' notes remain (manual cleanup needed)

## Manual Edits

You can safely add to Canvas Roots-imported notes:

### Safe to Add
- Research narratives in the note body
- Additional frontmatter fields (not cr_id)
- Links to source notes
- Tags and categories
- Evidence analysis sections

### Example Enhancement

```markdown
---
type: person
cr_id: "abc123"
gramps_id: "I0001"
birth_date: 1850-03-15
# Your additions below are safe
occupation: "Farmer"
religion: "Methodist"
research_status: "brick-wall"
---

# John Smith (1850-1920)

## Canvas Roots Data
Father: [[James Smith (1820-1890)]]
Mother: [[Mary Jones (1825-1900)]]

## Research Notes
<!-- Your research narratives here -->

John appears in the 1850 census as an infant...

## Evidence
- [[Census - Muskingum OH - 1850]]
- [[Smith Family Bible]]

## Open Questions
- Where was he between 1870-1880?
- Connection to Smith family in Kentucky?
```

## Troubleshooting

### Duplicate Notes Created
- Check if `cr_id` was accidentally deleted
- Canvas Roots couldn't match the note
- Manually merge and restore `cr_id`

### Links Not Working
- Verify person note filenames match link format
- Check for special characters in names
- Use aliases for alternate name formats

### Re-import Not Updating
- Confirm source GEDCOM has changes
- Check `cr_id` field is present
- Clear Obsidian cache and retry

## Workflow Integration

### When to Use Each System

| Data Type | System | Reason |
|-----------|--------|--------|
| Vital dates, relationships | Gramps | Structured data, GEDCOM exports, sharing |
| Source records | Gramps | Formal citations, linked to events |
| Events with citations | Gramps | Linked to people/families, queryable |
| Research narratives | Obsidian | Narrative flexibility, markdown |
| Proof arguments | Obsidian | Complex analysis, GPS compliance, footnotes |
| Evidence evaluation | Obsidian | Weighing conflicting sources |
| DNA analysis | Obsidian | Complex narrative format |

### Recommended Workflow for Research Analysis

When doing significant research that requires analyzing multiple sources:

1. **Record sources in Gramps** - Create source records with full metadata
2. **Cite sources on events** - Link citations to Birth, Death, Census, etc.
3. **Write analysis in Obsidian** - Create research note with R-YYYY-NNN ID
4. **Reference from Gramps** - Update Gramps note to point to Obsidian document

### Example: Birth Year Analysis

**In Gramps:**
- Birth event (E0123) has citations from 6 census records, 2 newspapers
- Person note (N0045) says:
  ```
  Birth year analysis complete. Conclusion: 1862.
  See Obsidian: Research/Birth Year Analysis - John Barry (R-2026-001).md
  ```

**In Obsidian:**
- Full GPS-compliant analysis in `Research/Birth Year Analysis - John Barry (R-2026-001).md`
- Evidence table comparing all sources
- Discussion of conflicting ages
- Conclusion with reasoning
- Proper footnotes in Evidence Explained format

### What Canvas Roots Does NOT Sync

Be aware of these limitations - manual management or API scripts required:

| Data | Synced? | Notes |
|------|---------|-------|
| Person names, dates | Yes | Basic vital info imports |
| Family relationships | Yes | Parent-child, spouse links |
| Note content from Gramps | **No** | Gramps notes don't import |
| Citations on events | **No** | Must check Gramps directly |
| Custom attributes | **No** | Not in GEDCOM export |
| Media files | **No** | File links only |

### Bidirectional Workflow Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                     GRAMPS (Structured Data)                 │
│  Sources → Citations → Events → People/Families             │
│                          ↓                                   │
│  Note: "See Obsidian: R-2026-001"                           │
└─────────────────────────────────────────────────────────────┘
                           ↓ Export GEDCOM
                           ↓ Import via Canvas Roots
┌─────────────────────────────────────────────────────────────┐
│                    OBSIDIAN (Research Notes)                 │
│  Research/R-2026-001.md                                     │
│  - Full proof argument                                       │
│  - Evidence table                                            │
│  - Footnotes: [1] 1870 Census... [2] Death cert...          │
│  - gramps_id: I0083, gramps_note_id: N0045                  │
└─────────────────────────────────────────────────────────────┘
```

### Sync Strategy

| Data Type | Manage In | Reason |
|-----------|-----------|--------|
| Vital dates | Gramps | Structured data, exports |
| Family links | Gramps | Relationship modeling |
| Research notes | Obsidian | Narrative flexibility |
| Source citations | Both | Gramps for data, Obsidian for analysis |
| DNA analysis | Obsidian | Complex narrative format |
