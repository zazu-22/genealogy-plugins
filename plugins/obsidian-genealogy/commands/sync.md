---
description: Sync Gramps data to Obsidian vault
allowed-tools: [Read, Write, Grep, Glob, Bash]
argument-hint: "[--dry-run]"
---

# Sync Gramps to Obsidian

Synchronize data from Gramps XML export to Obsidian person notes.

## Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Show what would be synced without making changes |

## Instructions

1. **Load the `obsidian-genealogy` skill**. If the `gramps` skill is available (from gramps-tools plugin), load it too. Otherwise, use this essential Gramps XML context:
   - Gramps XML uses `<person>`, `<family>`, `<event>` elements
   - Each person has a unique `handle` attribute and human-readable `id` (e.g., "I0001")
   - Names are in `<name><first>` and `<name><surname>` elements
   - Events link to persons via `<eventref>` with `hlink` to event handle
   - Birth/death are event types within `<event type="Birth">` etc.

2. **Read Gramps export**:
   - Location: `~/Genealogy/git-exports/family-tree.gramps`
   - Parse XML to extract persons, families, events

3. **Scan existing Obsidian notes**:
   - Location: `~/Genealogy/Obsidian/People/`
   - Index by gramps_id and cr_id

4. **For each person in Gramps**:
   - Check if matching Obsidian note exists (by gramps_id)
   - If exists, compare and note differences
   - If not exists, mark as new

5. **Generate sync plan**:

```markdown
# Sync Plan

## New Notes to Create
| Gramps ID | Name | Dates |
|-----------|------|-------|
| I0001 | John Smith | 1850-1920 |

## Notes to Update
| File | Field | Current | New |
|------|-------|---------|-----|
| John Smith.md | birth_date | 1850 | 1850-03-15 |

## No Changes Needed
[count] notes are already in sync

## Conflicts
| File | Issue |
|------|-------|
| [note] | Has cr_id (Canvas Roots managed) |
```

6. **If not --dry-run, apply changes**:
   - Create new person notes using template
   - Update frontmatter in existing notes
   - Preserve user-added content in note body
   - Skip Canvas Roots managed notes (have cr_id)

## Sync Rules

### What Gets Synced
- Name (including alternate names)
- Birth date and place
- Death date and place
- Parent links (as wikilinks)
- Spouse links
- Children links

### What's Preserved
- Research notes in body
- User-added frontmatter fields
- Tags and categories
- Source links added manually

### What's Skipped
- Notes with `cr_id` (Canvas Roots manages these)
- Media/photos (not in XML)
- Detailed event data beyond vitals

## Output

```markdown
# Sync Complete

**Date:** [timestamp]
**Mode:** [dry-run/applied]

## Results
- Notes created: [N]
- Notes updated: [N]
- Notes unchanged: [N]
- Notes skipped (Canvas Roots): [N]

## Created
- [[John Smith (1850-1920)]]

## Updated
- [[Mary Jones (1855-1930)]]: Updated death_date

## Skipped
- [[James Smith (1820-1890)]]: Has cr_id (Canvas Roots managed)
```

## Tips

- Run with --dry-run first to review changes
- Canvas Roots notes are skipped to avoid conflicts
- Back up vault before first sync
- Consider using Canvas Roots instead for full import
