---
description: Start a structured research session
allowed-tools: [Read, Write, Grep, Glob, Bash]
argument-hint: "--person <name> | --question <question>"
---

# Start Research Session

Begin a structured research session with tracking and logging.

## Options

| Flag | Description |
|------|-------------|
| `--person <name>` | Focus session on a specific person |
| `--question <question>` | Focus on a specific research question |

## Instructions

1. **Determine session context**
   - Check for active project in `~/Genealogy/projects/`
   - If within a project, use project's session directory
   - Otherwise, use standalone session tracking

2. **Create session log**

   Location: `~/Genealogy/projects/[project]/sessions/session-NN.md` or current directory

   ```markdown
   # Research Session [NN]

   **Date:** [today]
   **Focus:** [person or question]
   **Duration:** [start time] - [ongoing]

   ## Objectives
   - [ ] [Objective 1]
   - [ ] [Objective 2]

   ## Sources Consulted

   ### [Source 1]
   - **Repository:** [where accessed]
   - **Search terms:** [what searched]
   - **Findings:** [summary]
   - **Evidence:** [what was found or "negative search"]

   ## Discoveries
   - [Key finding 1]
   - [Key finding 2]

   ## Questions Raised
   - [New question from research]

   ## Next Steps
   - [ ] [Follow-up action]

   ## Session Notes
   [Detailed notes as session progresses]
   ```

3. **If within a project**, update `current-state.json`:
   - Increment session count
   - Update last_session field
   - Set session as in_progress

4. **Load relevant skills** based on session focus:
   - Person research → gramps, source-analysis
   - Evidence work → evidence-explained, genealogical-proof-standard
   - DNA → dna-evidence

## Output

Report session initialization:

```
# Session Started

**Session:** [number]
**Focus:** [person/question]
**Log:** [path to session log]

Ready to research. Use `/research-workflow:log` to record findings.
```

## Tips

- Set clear, achievable objectives
- Log negative searches (what you didn't find)
- Take breaks every 90 minutes
- Summarize findings before ending session
