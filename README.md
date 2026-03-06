# Genealogy Plugins

A Claude Code plugin marketplace for genealogical research, integrating Gramps, Evidence Explained methodology, and GPS-compliant proof building.

## Plugins

| Plugin | Description |
|--------|-------------|
| **gramps-tools** | Tree maintenance, backups, data quality audits, sync verification |
| **research-workflow** | Research planning reference material and methodology |
| **evidence-analysis** | Source analysis, GPS-compliant proofs, Evidence Explained citations |

## Archived Plugins

| Plugin | Reason |
|--------|--------|
| **obsidian-genealogy** | Research migrated to markdown + Dolt database (2026-03) |

## Installation

```bash
# Add marketplace
/plugin marketplace add ~/code/genealogy-plugins

# Install individual plugins
/plugin install gramps-tools@genealogy-plugins
/plugin install evidence-analysis@genealogy-plugins
/plugin install research-workflow@genealogy-plugins
```

## Requirements

- Gramps Desktop and/or Gramps Web
- Research database: Dolt server on localhost:3307

## Structure

```
genealogy-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── gramps-tools/
│   ├── research-workflow/
│   └── evidence-analysis/
├── disabled/
│   └── obsidian-genealogy/
├── CLAUDE.md
└── README.md
```
