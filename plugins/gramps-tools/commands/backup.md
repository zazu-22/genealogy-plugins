---
description: Trigger Gramps backup workflow
allowed-tools: [Bash, Read]
argument-hint: "[--verify] [--push]"
---

# Gramps Backup

Trigger a backup of the Gramps family tree to the git-exports repository.

## API-First Notice

**Preferred method**: Use the API to export and back up the tree. The CLI approach below is preserved for compatibility with existing backup scripts but should not be used for new implementations.

## Options

| Flag | Description |
|------|-------------|
| `--verify` | Verify backup integrity after creation |
| `--push` | Push to remote repository after commit |

## Instructions

### Preferred: API-Based Backup

1. Use GrampsAPIClient for reliable API access (see `gramps` skill > `lib/web-api.md`)

2. Export via API:
   ```python
   from gramps_web_client import GrampsAPIClient

   # Automatic credential loading
   client = GrampsAPIClient()

   # Export to Gramps XML
   # Note: Export functionality not yet in GrampsAPIClient
   # Use direct API call for now:
   import urllib.request
   token = client._get_auth_token()
   req = urllib.request.Request(
       f"{client.credentials.url}/api/exporters/gramps",
       headers={"Authorization": f"Bearer {token}"}
   )
   with urllib.request.urlopen(req) as resp:
       with open('/Users/jasonshaffer/Genealogy/git-exports/family-tree.gramps', 'wb') as f:
           f.write(resp.read())
   ```

   **Note**: Export endpoints will be added to GrampsAPIClient in a future update.

3. Commit to git:
   ```bash
   cd ~/Genealogy/git-exports
   git add -A
   git commit -m "Backup: $(date +%Y-%m-%d)"
   ```

### Legacy: Script-Based Backup

If the backup script exists at `~/.local/bin/gramps-backup.sh`, it may be executed:

```bash
~/.local/bin/gramps-backup.sh
```

**Note**: This approach uses CLI commands which are unreliable on macOS. Prefer the API method above.

### Legacy: Manual CLI Backup (Deprecated)

**WARNING**: CLI is unreliable on macOS. Use only if API is unavailable.

```bash
# Export from Gramps (deprecated)
gramps -O "Shaffer-Richardson" -e ~/Genealogy/git-exports/family-tree.gramps -f gramps-xml

# Commit to git
cd ~/Genealogy/git-exports
git add -A
git commit -m "Backup: $(date +%Y-%m-%d)"
```

### Push to Remote

If `--push` flag is set:
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
