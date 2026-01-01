---
description: Create or update an Obsidian person note
allowed-tools: [Read, Write, Edit, Grep, Glob]
argument-hint: "--gramps-id <ID> | <person-name>"
---

# Person Note

Create or update a person note in the Obsidian genealogy vault.

## Options

| Flag | Description |
|------|-------------|
| `--gramps-id <ID>` | Look up person by Gramps ID |
| `<person-name>` | Person's name to create/find |

## Instructions

1. **Load the `obsidian-genealogy` skill** for vault conventions

2. **Locate or create the person note**:
   - Search `~/Genealogy/Obsidian/People/` for existing note
   - Match by name or gramps_id in frontmatter
   - If creating new, use naming convention: `Firstname Lastname (birth_year-death_year).md`

3. **If using --gramps-id**, extract data from Gramps:
   - Read `~/Genealogy/git-exports/family-tree.gramps`
   - Find person by handle or ID
   - Extract: name, dates, events, family links

4. **Create/update frontmatter**:
   ```yaml
   ---
   type: person
   gramps_id: [ID if known]
   birth_date: [date]
   death_date: [date if deceased]
   birth_place: "[[Place Name]]"
   death_place: "[[Place Name]]"
   father: "[[Father Name (dates)]]"
   mother: "[[Mother Name (dates)]]"
   spouse:
     - "[[Spouse Name (dates)]]"
   children:
     - "[[Child Name (dates)]]"
   ---
   ```

5. **Create/preserve note body**:
   - If new note, create sections: Biography, Sources, Research Notes
   - If existing, preserve user-added content
   - Update only data sections if syncing from Gramps

## Note Template

```markdown
---
type: person
gramps_id: [ID]
birth_date: [date]
death_date: [date]
father: "[[Father]]"
mother: "[[Mother]]"
---

# [Full Name] ([birth]-[death])

## Vital Facts

| Event | Date | Place | Source |
|-------|------|-------|--------|
| Birth | [date] | [[Place]] | [[Source]] |
| Death | [date] | [[Place]] | [[Source]] |

## Family

**Parents:**
- Father: [[Father Name]]
- Mother: [[Mother Name]]

**Spouse(s):**
- [[Spouse Name]] (married [date])

**Children:**
1. [[Child Name]]

## Biography

[Narrative about this person's life]

## Sources

- [[Source 1]]
- [[Source 2]]

## Research Notes

[Notes about ongoing research, questions, brick walls]
```

## Output

Report what was created/updated:

```
# Person Note

**Action:** [Created/Updated]
**File:** ~/Genealogy/Obsidian/People/[filename].md
**Gramps ID:** [ID if linked]

## Summary
- Name: [full name]
- Dates: [birth]-[death]
- Parents: [linked/unknown]
- Spouse(s): [count]
- Children: [count]
```

## Tips

- Preserve existing research notes when updating
- Use wikilinks for all person/place/source references
- Keep gramps_id synced with Gramps database
- Don't duplicate Canvas Roots-managed notes
