---
description: Update research log with a finding
allowed-tools: [Read, Write, Edit]
argument-hint: "--session <N> --finding <description>"
---

# Log Research Finding

Add a finding or note to an active research session log.

## Options

| Flag | Description |
|------|-------------|
| `--session <N>` | Session number (default: most recent) |
| `--finding <text>` | Description of finding to log |

## Instructions

1. **Locate the session log**
   - Check `~/Genealogy/projects/[active-project]/sessions/` for session files
   - Or check current directory for `session-*.md`
   - Find most recent or specified session number

2. **Determine finding type** from content:
   - Source consulted
   - Discovery/evidence found
   - Question raised
   - Negative search result

3. **Append to appropriate section** of session log:

   For source consulted:
   ```markdown
   ### [Source Name]
   - **Repository:** [where]
   - **Search terms:** [terms]
   - **Findings:** [summary]
   - **Citation:** [EE-style citation if evidence found]
   ```

   For discovery:
   ```markdown
   - [timestamp] [Discovery description] (Source: [reference])
   ```

   For question:
   ```markdown
   - [New question arising from this finding]
   ```

4. **Update session metadata** if significant finding:
   - Add to Discoveries section
   - Note in project's `current-state.json` if applicable

## Output

Confirm the log entry:

```
# Finding Logged

**Session:** [N]
**Type:** [source/discovery/question]
**Added to:** [section name]

Entry:
> [what was logged]
```

## Tips

- Log immediately while context is fresh
- Include source references even for small findings
- Note your reasoning, not just facts
- Negative searches are valuable - log them too
