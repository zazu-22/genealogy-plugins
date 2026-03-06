# Vault Structure Reference

Organization and conventions for the genealogy Obsidian vault.

## Directory Layout

```
~/Genealogy/Obsidian/
├── People/                 # Person notes
│   ├── Surname A-M/        # Optional grouping for large collections
│   └── Surname N-Z/
├── Sources/                # Documentary evidence
│   ├── Census/
│   ├── Vital Records/
│   ├── Church Records/
│   └── Other/
├── Places/                 # Geographic locations
│   ├── USA/
│   │   ├── Ohio/
│   │   ├── Kentucky/
│   │   └── Illinois/
│   └── Europe/
├── Events/                 # Significant occurrences
├── Research/               # Analysis and narratives
│   ├── Brick Walls/
│   ├── DNA Analysis/
│   └── Proof Arguments/
├── Canvas/                 # Visual family trees
├── Templates/              # Note templates
├── .obsidian/              # Obsidian configuration (do not edit directly)
├── CLAUDE.md               # Instructions for Claude Code
└── README.md
```

## Naming Conventions

### Person Notes
```
Firstname Lastname (birth_year-death_year).md
```

Examples:
- `John Smith (1850-1920).md`
- `Mary Jones (b. 1955).md` (living person)
- `Unknown Smith (abt 1800-bef 1850).md` (uncertain dates)

### Source Notes
```
Source Type - Jurisdiction - Year - Description.md
```

Examples:
- `Census - Muskingum OH - 1850.md`
- `Marriage Record - Franklin OH - 1875 - Smith-Jones.md`
- `Obituary - Zanesville Times - 1920-03-16.md`

### Place Notes
```
Place Name, Jurisdiction.md
```

Examples:
- `Zanesville, Muskingum County, Ohio.md`
- `Muskingum County, Ohio.md`
- `Ohio, USA.md`

## Linking Strategy

### Internal Links
Use wikilinks with display text when helpful:

```markdown
Born to [[John Smith (1850-1920)|John Smith]] and [[Mary Jones (1855-1930)|Mary]].
Resided in [[Zanesville, Muskingum County, Ohio|Zanesville]].
Source: [[Census - Muskingum OH - 1850|1850 Census]].
```

### Backlinks
Obsidian automatically tracks backlinks. Use these for:
- Finding all sources citing a person
- Discovering family connections
- Tracing research threads

### Tags
Use tags for cross-cutting categories:

```
#immigrant #civil-war #brick-wall #dna-confirmed
```

## File Organization Best Practices

1. **One person per note**: Even for children who died young
2. **Consistent naming**: Follow conventions exactly for linking
3. **Avoid duplicates**: Search before creating new notes
4. **Use aliases**: Add `aliases:` frontmatter for alternate names
5. **Geographic hierarchy**: Places from specific to general
6. **Date precision**: Use appropriate format for certainty level

## Integration Points

### With Gramps
- `gramps_id` frontmatter links to Gramps database
- Export from Gramps → Import via Canvas Roots
- Maintain both systems in sync

### With Canvas Roots
- `cr_id` field is managed by Canvas Roots
- Never manually edit Canvas Roots fields
- Re-import updates existing notes

### With Research Projects
- Link research notes to `~/Genealogy/projects/`
- Reference session logs in research narratives
- Track proof arguments to GPS standards
