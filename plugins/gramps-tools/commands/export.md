---
description: Export Gramps tree in various formats
allowed-tools: [Bash, Read]
argument-hint: "--format <xml|gedcom|web>"
---

# Export Tree

Export the Gramps family tree in various formats.

## Formats

| Format | Description | Output |
|--------|-------------|--------|
| `xml` | Uncompressed Gramps XML | `.gramps` file |
| `gedcom` | GEDCOM 5.5.1 for sharing | `.ged` file |
| `web` | Narrated Web Site | HTML folder |

## Instructions

### XML Export
```bash
gramps -O "Shaffer-Richardson" -e ~/Genealogy/Exports/family-tree.gramps -f gramps-xml
```

### GEDCOM Export
```bash
gramps -O "Shaffer-Richardson" -e ~/Genealogy/Exports/family-tree.ged -f gedcom
```

### Web Export
```bash
gramps -O "Shaffer-Richardson" -e ~/Genealogy/Exports/web/ -f navwebpage
```

## Export Locations

| Type | Destination |
|------|-------------|
| Backups (XML) | `~/Genealogy/git-exports/` |
| Sharing (GEDCOM) | `~/Genealogy/Exports/` |
| Publishing (Web) | `~/Genealogy/Exports/web/` |

## Output

Report export status:

```
# Export Report
Date: [timestamp]
Tree: Shaffer-Richardson
Format: [format]

## Status: [SUCCESS/FAILED]

## Details
- Output: [path]
- File size: [size]
- Duration: [time]

## Contents (for GEDCOM/XML)
- Persons: [count]
- Families: [count]
- Sources: [count]
- Places: [count]
```

## Tips

- Use XML for backups (version-control friendly)
- Use GEDCOM for sharing with other software
- Use Web for publishing family history online
- Always use uncompressed XML for meaningful git diffs
