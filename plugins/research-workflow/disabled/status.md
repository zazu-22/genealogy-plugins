---
description: View active research projects and status
allowed-tools: [Read, Glob]
argument-hint: ""
---

# Research Status

Display status of all research projects from the project registry.

## Instructions

1. **Read the project registry**
   - Location: `~/Genealogy/projects/_registry.md`
   - Parse the Active, Completed, and Paused project tables

2. **For each active project**, read its `current-state.json`:
   - Location: `~/Genealogy/projects/[project-name]/current-state.json`
   - Extract: status, phase, next_action, blockers

3. **Generate status report**:

```markdown
# Research Projects Status

**Updated:** [timestamp]

## Active Projects

### [Project Name]
- **Status:** 🟡 In Progress
- **Phase:** [current] of [total] - [phase name]
- **Sessions:** [completed] / [estimated]
- **Next Action:** [next_action from state]
- **Blockers:** [any blockers or "None"]

[Repeat for each active project]

## Recently Completed

| Project | Completed | Summary |
|---------|-----------|---------|
| [name] | [date] | [brief summary] |

## Paused Projects

| Project | Paused | Reason |
|---------|--------|--------|
| [name] | [date] | [reason] |

---

## Quick Actions
- `/research-workflow:session --project [name]` - Start session
- `/research-workflow:project --status [name]` - Detailed view
```

4. **Highlight urgent items**:
   - Projects with blockers
   - Projects not updated in >7 days
   - Projects nearing completion

## Output

The formatted status report above.

## Tips

- Check status at start of each research session
- Address blockers before starting new work
- Update project state after each session
