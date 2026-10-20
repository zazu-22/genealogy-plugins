# genealogy-governance

Runs the genealogy repo's own Claude hooks in sessions that start **above** the
clone, such as a multi-repo cloud thread (cwd `/home/user`, clones beneath it).
Those sessions never load `genealogy/.claude/settings.json`, so without this
plugin none of its hooks run.

The plugin holds no copy of the hook logic. Each entry in `hooks/hooks.json`
calls `scripts/run-genealogy-hook.py <script>`, which finds the genealogy
clone (walking up from the payload cwd, `CLAUDE_PROJECT_DIR`, and the process
cwd, trying each directory and its `genealogy/` child) and runs
`<clone>/.claude/hooks/<script>` at its real path, with the payload, stdout,
stderr, and exit code passed through unchanged.

| Event | Script (in genealogy/.claude/hooks) |
|-------|-------------------------------------|
| SessionStart | `governance-arrival.sh`, `journal-last-entry.sh`, `compact-recovery.mjs` |
| SessionStart | `scripts/install-git-hooks.sh` (pre-commit tree-export guard; silent unless it fails) |
| PreToolUse `Write\|Edit` | `research-write-guard.py` |
| TaskCompleted | `task-completed-qc.py` (exit 2 blocks) |
| SubagentStart | `subagent-start-governance.sh` |
| PostToolUse `Agent` | `governance-concern-handler.sh` |
| SubagentStop, Stop | `governance-background-concern.py` (records a background subagent's concern, delivers it at the parent's next Stop; inert until the clone has the script) |

`PreCompact` (`pre-compact.mjs`) is left out: it copies the transcript into the
clone, which an ephemeral container discards.

## Safety

- **No double runs.** If `CLAUDE_PROJECT_DIR` is the clone and its
  `settings.json` already registers the script (a session started inside the
  clone, as on the Mac), the wrapper does nothing.
- **Identity, not just shape.** A discovered clone must be a git checkout
  (its own `.git`) whose `origin` is `zazu-22/genealogy`. A directory committed
  inside another repo that merely looks like the clone is never run.
- **Fail-open**, like the scripts: no clone found means exit 0 and no output.
- **Kill switch:** `GENEALOGY_GOVERNANCE_DISABLE=1`.
- **Override location:** `GENEALOGY_REPO_DIR=/path/to/genealogy` (trusted as
  given; use it for a fork or another remote).

## Checking that it fired

Every invocation appends one tab-separated line (time, event, script, clone,
outcome) to `${XDG_STATE_HOME:-~/.local/state}/genealogy-governance/hooks.log`:

```bash
tail ~/.local/state/genealogy-governance/hooks.log
```

## Tests

`python3 -m unittest discover -s tests -p 'test_*.py'` from the repo root.
