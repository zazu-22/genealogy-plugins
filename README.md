# Genealogy Plugins

A Claude Code plugin marketplace for genealogical research, integrating Gramps, Evidence Explained methodology, and Obsidian.

## Plugins

| Plugin | Description |
|--------|-------------|
| **gramps-tools** | Tree maintenance, backups, data quality audits, sync verification |
| **research-workflow** | Structured research sessions, planning, project registry integration |
| **evidence-analysis** | Source analysis, GPS-compliant proofs, Evidence Explained citations |
| **obsidian-genealogy** | Obsidian vault integration with Canvas Roots compatibility |

## Installation

```bash
# Add marketplace
/plugin marketplace add ~/code/personal/genealogy-plugins

# Install individual plugins
/plugin install gramps-tools@genealogy-plugins
/plugin install evidence-analysis@genealogy-plugins
/plugin install research-workflow@genealogy-plugins
/plugin install obsidian-genealogy@genealogy-plugins
```

## Requirements

- Gramps Desktop and/or Gramps Web
- Obsidian with Canvas Roots plugin (for obsidian-genealogy)
- Project registry at `~/Genealogy/projects/`

## Structure

```
genealogy-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── gramps-tools/
│   ├── research-workflow/
│   ├── evidence-analysis/
│   └── obsidian-genealogy/
├── CLAUDE.md
└── README.md
```
