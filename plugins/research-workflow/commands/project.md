---
description: Create or update a project in the registry
allowed-tools: [Read, Write, Edit, Bash, Glob]
argument-hint: "--create <name> | --phase <N> | --status <status>"
---

# Manage Research Project

Create a new research project or update an existing one in the registry.

## Options

| Flag | Description |
|------|-------------|
| `--create <name>` | Create new project with given name |
| `--phase <N>` | Update current phase number |
| `--status <status>` | Set status (in_progress, paused, completed) |
| `--blocker <text>` | Add a blocker |
| `--resolve-blocker` | Clear blockers |

## Creating a New Project

1. **Generate project directory name**: `YYYY-MM-<slug>`
   - Use current year-month
   - Convert project name to kebab-case slug

2. **Create project structure** using templates:
   ```
   ~/Genealogy/projects/YYYY-MM-project-slug/
   ├── README.md           # From _templates/project-readme.md
   ├── current-state.json  # From _templates/current-state.json
   ├── plan.md             # Research plan
   ├── decisions.md        # Decision log
   └── sessions/           # Session logs directory
   ```

3. **Initialize current-state.json**:
   ```json
   {
     "project_id": "YYYY-MM-project-slug",
     "status": "in_progress",
     "created": "YYYY-MM-DD",
     "last_updated": "YYYY-MM-DD",
     "phase": {
       "current": 0,
       "total": 0,
       "name": "Planning"
     },
     "sessions": {
       "completed": 0,
       "total_estimated": 0
     },
     "next_action": "Create research plan",
     "blockers": []
   }
   ```

4. **Update the registry** (`~/Genealogy/projects/_registry.md`):
   - Add row to Active Projects table
   - Include link to project directory

## Updating a Project

1. **Locate project** by name or current directory

2. **Update current-state.json** with changes:
   - Phase updates: increment phase.current, update phase.name
   - Status changes: update status field
   - Blockers: add to or clear blockers array

3. **Update registry** if status changed:
   - Move between Active/Completed/Paused tables
   - Update status emoji

4. **Update last_updated timestamp**

## Output

For create:
```
# Project Created

**Project:** [name]
**Directory:** ~/Genealogy/projects/[slug]/
**Status:** 🟡 In Progress

Files created:
- README.md
- current-state.json
- plan.md
- decisions.md
- sessions/

Next: Create research plan with `/research-workflow:plan`
```

For update:
```
# Project Updated

**Project:** [name]
**Change:** [what was updated]
**New State:** [summary]
```

## Tips

- Use descriptive project names
- Set realistic phase counts
- Update status after each session
- Document decisions in decisions.md
