---
description: Trigger Gramps backup workflow
allowed-tools: [Bash, Read]
argument-hint: "[--verify] [--push]"
---

# Gramps Backup

Trigger a backup of the Gramps family tree to the git-exports repository.

## Options

| Flag | Description |
|------|-------------|
| `--verify` | Verify backup integrity after creation |
| `--push` | Push to remote repository after commit |

## Instructions

1. Check if the backup script exists at `~/.local/bin/gramps-backup.sh`

2. If script exists, execute it:
   ```bash
   ~/.local/bin/gramps-backup.sh
   ```

3. If script doesn't exist, perform manual backup:
   ```bash
   # Export from Gramps
   gramps -O "Shaffer-Richardson" -e ~/Genealogy/git-exports/family-tree.gramps -f gramps-xml

   # Commit to git
   cd ~/Genealogy/git-exports
   git add -A
   git commit -m "Backup: $(date +%Y-%m-%d)"
   ```

4. If `--push` flag is set:
   ```bash
   cd ~/Genealogy/git-exports
   git push origin main
   ```

5. If `--verify` flag is set:
   - Check file exists and has content
   - Validate XML structure
   - Compare person count with previous backup

## Output

Report backup status:

```
# Gramps Backup Report
Date: [timestamp]
Tree: Shaffer-Richardson

## Status: [SUCCESS/FAILED]

## Details
- Export location: ~/Genealogy/git-exports/family-tree.gramps
- File size: [size]
- Git commit: [hash]
- Pushed to remote: [yes/no]

## Verification (if requested)
- XML valid: [yes/no]
- Person count: [count]
- Delta from last backup: [+/-N]
```

## Tips

- Run backups before making significant changes
- The automated backup runs weekly (Sunday 2am)
- Check `~/.local/share/gramps-backup.log` for history
