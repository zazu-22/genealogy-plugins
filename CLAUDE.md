# CLAUDE.md

Instructions for Claude Code when working in the genealogy-plugins marketplace.

## Overview

This is a Claude Code plugin marketplace containing genealogy research plugins for:
- **gramps-tools**: Gramps tree maintenance, backups, audits
- **research-workflow**: Research session management, project registry
- **evidence-analysis**: Evidence Explained citations, GPS methodology
- **obsidian-genealogy**: Obsidian vault integration

## Key Paths

| Resource | Path |
|----------|------|
| Gramps Web | `http://localhost:5000` |
| Gramps backups | `~/Genealogy/git-exports/` |
| Project registry | `~/Genealogy/projects/_registry.md` |
| Obsidian vault | `~/Genealogy/Obsidian/` |
| Media files | `~/Genealogy/Media/` |

## Plugin Development

When modifying plugins:
1. Test locally with `claude --plugin-dir ./plugins/plugin-name`
2. Use `${CLAUDE_PLUGIN_ROOT}` for all intra-plugin paths
3. Follow kebab-case naming for all files and directories
4. Skills use `SKILL.md` with YAML frontmatter

## Genealogy Standards

- **Citations**: Follow Elizabeth Shown Mills' Evidence Explained format
- **Proof**: Apply Genealogical Proof Standard (GPS) five elements
- **Sources**: Use Gramps source-citation model (source → citation → event)
