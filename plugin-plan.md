# Genealogy Plugins Marketplace Architecture

## Decisions

| Question | Answer |
|----------|--------|
| Location | `~/code/personal/genealogy-plugins/` (separate git repo) |
| Plugins | All 4 plugins included in initial implementation |
| Hook behavior | Blocking with helpful feedback |
| Project registry | Full read/write integration with `~/Genealogy/projects/` |

## Overview

Create a **genealogy-plugins** marketplace following the cc-plugins pattern, with multiple focused plugins that users can enable/disable independently. Migrate existing skills from `~/.claude/skills/` into the appropriate plugins.

## Marketplace Structure

```
~/code/personal/genealogy-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── gramps-tools/          # Tree maintenance, backups, data quality
│   ├── research-workflow/     # Research sessions, planning, registry integration
│   ├── evidence-analysis/     # Source analysis, GPS, citations
│   └── obsidian-genealogy/    # Obsidian vault integration
├── CLAUDE.md
└── README.md
```

---

## Plugin 1: gramps-tools

**Purpose**: Tree maintenance, backups, data quality audits, sync verification

### Skills (1)
| Skill | Source | Description |
|-------|--------|-------------|
| gramps | ~/.claude/skills/gramps/ | XML structure, database queries, Web API, data model |

### Commands (4)
| Command | Description | Key Arguments |
|---------|-------------|---------------|
| `/gramps-tools:audit` | Run data quality audit | `--type` (orphans, citations, dates, completeness) |
| `/gramps-tools:backup` | Trigger backup workflow | `--verify`, `--push` |
| `/gramps-tools:sync-status` | Check Desktop ↔ Web sync | none |
| `/gramps-tools:export` | Export tree in various formats | `--format` (xml, gedcom, web) |

### Agents (1)
| Agent | Trigger | Tools |
|-------|---------|-------|
| data-quality-auditor | Audit requests, data cleanup | Bash, Read, Grep, Glob |

### Hooks (1)
| Event | Purpose |
|-------|---------|
| PostToolUse (Bash) | Log Gramps CLI/backup operations |

---

## Plugin 2: research-workflow

**Purpose**: Structured research sessions, planning, progress tracking with project registry integration

### Skills (1)
| Skill | Source | Description |
|-------|--------|-------------|
| research-planning | ~/.claude/skills/research-planning/ | Research questions, record selection, locality research |

### Commands (5)
| Command | Description | Key Arguments |
|---------|-------------|---------------|
| `/research-workflow:plan` | Create research plan for a question | `<question>` |
| `/research-workflow:session` | Start structured research session | `--person`, `--question` |
| `/research-workflow:log` | Update research log entry | `--session`, `--finding` |
| `/research-workflow:status` | View active research projects | none |
| `/research-workflow:project` | Create/update project in registry | `--create`, `--phase`, `--status` |

### Agents (1)
| Agent | Trigger | Tools |
|-------|---------|-------|
| research-planner | Research planning requests | Read, Write, Grep, Glob, WebSearch |

### Hooks (0)
None initially

### Project Registry Integration

The research-workflow plugin integrates with `~/Genealogy/projects/`:

- **Read**: `/research-workflow:status` reads `_registry.md` and project state files
- **Write**: `/research-workflow:project --create` scaffolds new project directories following existing template structure
- **Update**: Session commands update `current-state.json` and create session logs in `sessions/`

Registry path: `~/Genealogy/projects/_registry.md`
Project template: `~/Genealogy/projects/_templates/`

---

## Plugin 3: evidence-analysis

**Purpose**: Source analysis, GPS-compliant proof building, citation generation

### Skills (4)
| Skill | Source | Description |
|-------|--------|-------------|
| source-analysis | ~/.claude/skills/source-analysis/ | Mills' classification system |
| evidence-explained | ~/.claude/skills/evidence-explained/ | EE citation methodology |
| genealogical-proof-standard | ~/.claude/skills/genealogical-proof-standard/ | GPS five elements |
| dna-evidence | ~/.claude/skills/dna-evidence/ | DNA + documentary integration |

### Commands (4)
| Command | Description | Key Arguments |
|---------|-------------|---------------|
| `/evidence-analysis:cite` | Generate EE-style citation | `<source-description>` |
| `/evidence-analysis:analyze` | Classify source/information/evidence | `<source>` |
| `/evidence-analysis:proof` | Build GPS-compliant proof argument | `--claim`, `--sources` |
| `/evidence-analysis:dna` | Analyze DNA match for relationship | `--cm`, `--shared-matches` |

### Agents (2)
| Agent | Trigger | Tools |
|-------|---------|-------|
| proof-builder | Proof argument requests | Read, Write, Grep, Glob |
| source-classifier | Source analysis requests | Read, Grep |

### Hooks (1)
| Event | Purpose |
|-------|---------|
| PreToolUse (Write) | Validate citation format in genealogy files |

---

## Plugin 4: obsidian-genealogy

**Purpose**: Obsidian vault integration for genealogy research notes

### Skills (1)
| Skill | Source | Description |
|-------|--------|-------------|
| obsidian-genealogy | NEW | Vault structure, frontmatter patterns, Canvas Roots |

### Commands (3)
| Command | Description | Key Arguments |
|---------|-------------|---------------|
| `/obsidian-genealogy:person` | Create/update person note | `--gramps-id` or `<name>` |
| `/obsidian-genealogy:validate` | Validate frontmatter in vault | `--type` (person, source, place) |
| `/obsidian-genealogy:sync` | Sync Gramps data to Obsidian | `--dry-run` |

### Agents (0)
None

### Hooks (1)
| Event | Purpose |
|-------|---------|
| PostToolUse (Write) | Validate frontmatter schema for Obsidian .md files |

---

## Shared Utilities (lib/)

Each plugin with hooks will have a `lib/` directory for shared shell utilities:
- `lib/logging.sh` - Consistent log formatting
- `lib/validation.sh` - Common validation functions

---

## Component Counts Summary

| Plugin | Skills | Commands | Agents | Hooks |
|--------|--------|----------|--------|-------|
| gramps-tools | 1 | 4 | 1 | 1 |
| research-workflow | 1 | 5 | 1 | 0 |
| evidence-analysis | 4 | 4 | 2 | 1 |
| obsidian-genealogy | 1 | 3 | 0 | 1 |
| **Total** | **7** | **16** | **4** | **3** |

---

## Implementation Order

1. **Phase 1**: Marketplace scaffold + gramps-tools (highest infrastructure value)
2. **Phase 2**: evidence-analysis (core genealogy methodology, 4 skills)
3. **Phase 3**: research-workflow (session management + registry)
4. **Phase 4**: obsidian-genealogy (vault integration)

---

## Consistency Standards

All components will follow these patterns:

### Skill Structure
```
skills/<skill-name>/
├── SKILL.md          # Main skill with triggers and core content
└── lib/              # Reference files (4-6 per skill)
    ├── INDEX.yaml
    └── *.md
```

### Command Frontmatter
```yaml
---
description: Brief description for /help
allowed-tools: [Tool1, Tool2]
argument-hint: "--flag <value>"
---
```

### Agent Frontmatter
```yaml
---
name: agent-name
description: When to trigger this agent
model: opus|sonnet|haiku
tools: [Tool1, Tool2]
---
```

### Hook Scripts
```bash
#!/bin/bash
# Hook: <EventType> - <Purpose>
# Matcher: <pattern>

source "${CLAUDE_PLUGIN_ROOT}/lib/logging.sh"
# Implementation...
```

---

## Detailed Implementation Steps

### Step 1: Create Marketplace Scaffold
```bash
mkdir -p ~/code/personal/genealogy-plugins/.claude-plugin
mkdir -p ~/code/personal/genealogy-plugins/plugins
```

Create files:
- `~/code/personal/genealogy-plugins/.claude-plugin/marketplace.json`
- `~/code/personal/genealogy-plugins/CLAUDE.md`
- `~/code/personal/genealogy-plugins/README.md`
- Initialize git repo

### Step 2: Create gramps-tools Plugin
```
plugins/gramps-tools/
├── .claude-plugin/plugin.json
├── commands/
│   ├── audit.md
│   ├── backup.md
│   ├── sync-status.md
│   └── export.md
├── agents/
│   └── data-quality-auditor.md
├── skills/
│   └── gramps/           # Move from ~/.claude/skills/gramps/
│       ├── SKILL.md
│       └── lib/
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── log-gramps-ops.sh
└── lib/
    └── logging.sh
```

### Step 3: Create evidence-analysis Plugin
```
plugins/evidence-analysis/
├── .claude-plugin/plugin.json
├── commands/
│   ├── cite.md
│   ├── analyze.md
│   ├── proof.md
│   └── dna.md
├── agents/
│   ├── proof-builder.md
│   └── source-classifier.md
├── skills/
│   ├── source-analysis/      # Move from ~/.claude/skills/
│   ├── evidence-explained/   # Move from ~/.claude/skills/
│   ├── genealogical-proof-standard/  # Move from ~/.claude/skills/
│   └── dna-evidence/         # Move from ~/.claude/skills/
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── validate-citation.sh
└── lib/
    └── validation.sh
```

### Step 4: Create research-workflow Plugin
```
plugins/research-workflow/
├── .claude-plugin/plugin.json
├── commands/
│   ├── plan.md
│   ├── session.md
│   ├── log.md
│   ├── status.md
│   └── project.md
├── agents/
│   └── research-planner.md
├── skills/
│   └── research-planning/    # Move from ~/.claude/skills/
└── lib/
    └── registry.sh           # Project registry utilities
```

### Step 5: Create obsidian-genealogy Plugin
```
plugins/obsidian-genealogy/
├── .claude-plugin/plugin.json
├── commands/
│   ├── person.md
│   ├── validate.md
│   └── sync.md
├── skills/
│   └── obsidian-genealogy/   # NEW skill
│       ├── SKILL.md
│       └── lib/
│           ├── frontmatter-schema.md
│           ├── vault-structure.md
│           └── canvas-roots.md
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── validate-frontmatter.sh
└── lib/
    └── validation.sh
```

### Step 6: Validation & Testing
1. Run plugin-validator agent on each plugin
2. Test each command manually
3. Verify hooks trigger correctly
4. Test skill activation via trigger phrases

### Step 7: Installation
```bash
# Add marketplace
/plugin marketplace add ~/code/personal/genealogy-plugins

# Install plugins
/plugin install gramps-tools@genealogy-plugins
/plugin install evidence-analysis@genealogy-plugins
/plugin install research-workflow@genealogy-plugins
/plugin install obsidian-genealogy@genealogy-plugins
```

---

## Source Files to Migrate

| Source | Destination |
|--------|-------------|
| `~/.claude/skills/gramps/` | `plugins/gramps-tools/skills/gramps/` |
| `~/.claude/skills/source-analysis/` | `plugins/evidence-analysis/skills/source-analysis/` |
| `~/.claude/skills/evidence-explained/` | `plugins/evidence-analysis/skills/evidence-explained/` |
| `~/.claude/skills/genealogical-proof-standard/` | `plugins/evidence-analysis/skills/genealogical-proof-standard/` |
| `~/.claude/skills/dna-evidence/` | `plugins/evidence-analysis/skills/dna-evidence/` |
| `~/.claude/skills/research-planning/` | `plugins/research-workflow/skills/research-planning/` |

---

## Key Integration Points

| Integration | Plugin | Method |
|-------------|--------|--------|
| Gramps Web API | gramps-tools | Bash with curl, keychain auth |
| Gramps CLI | gramps-tools | Bash with gramps command |
| Backup script | gramps-tools | Calls ~/.local/bin/gramps-backup.sh |
| Project registry | research-workflow | Read/write ~/Genealogy/projects/ |
| Obsidian vault | obsidian-genealogy | Read/write ~/Genealogy/Obsidian/ |
| Git exports | gramps-tools | Read ~/Genealogy/git-exports/ |
