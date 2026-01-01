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

## Version Management (CRITICAL)

**ALWAYS bump version numbers when making functional changes to plugins.**

### Version Files

| Scope | File | Field |
|-------|------|-------|
| Marketplace | `.claude-plugin/marketplace.json` | `metadata.version` |
| gramps-tools | `plugins/gramps-tools/.claude-plugin/plugin.json` | `version` |
| research-workflow | `plugins/research-workflow/.claude-plugin/plugin.json` | `version` |
| evidence-analysis | `plugins/evidence-analysis/.claude-plugin/plugin.json` | `version` |
| obsidian-genealogy | `plugins/obsidian-genealogy/.claude-plugin/plugin.json` | `version` |

### When to Bump Versions

**MUST bump** (functional changes):
- Adding/modifying/removing skills, commands, agents, or hooks
- Changing plugin behavior or functionality
- Bug fixes that affect plugin operation
- Schema or API changes

**Skip version bump** (non-functional):
- Documentation updates (`docs/`, README, comments)
- Code formatting/style changes with no behavior change
- Adding/updating CLAUDE.md or other dev docs

### Versioning Rules

1. Use semantic versioning: `MAJOR.MINOR.PATCH`
2. Bump the specific plugin's version when changing that plugin
3. Bump marketplace version when:
   - Adding/removing plugins from the marketplace
   - Changing marketplace-level configuration
   - Making a release that includes multiple plugin updates
4. **Before committing**: Verify version was bumped if functional changes were made
5. **Before pushing**: Double-check version increments are staged

## Genealogy Standards

- **Citations**: Follow Elizabeth Shown Mills' Evidence Explained format
- **Proof**: Apply Genealogical Proof Standard (GPS) five elements
- **Sources**: Use Gramps source-citation model (source → citation → event)
