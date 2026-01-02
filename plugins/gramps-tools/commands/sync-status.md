---
description: Check Gramps Desktop ↔ Web sync status
allowed-tools: [Bash, Read, WebFetch]
argument-hint: ""
---

# Sync Status

Check the synchronization status between Gramps Desktop and Gramps Web.

## Instructions

1. Check if Gramps Web is running:
   ```bash
   curl -s http://localhost:5000/api/health || echo "Gramps Web not running"
   ```

2. Get last sync timestamp from Gramps Web API (if running)

3. Check last modification of local Gramps database

4. Compare timestamps to determine sync status

## Status Report

Generate a sync status report:

```
# Gramps Sync Status
Date: [timestamp]

## Services
| Service | Status | Last Modified |
|---------|--------|---------------|
| Gramps Desktop | [running/stopped] | [timestamp] |
| Gramps Web | [running/stopped] | [timestamp] |

## Sync Status
Status: [IN_SYNC / OUT_OF_SYNC / UNKNOWN]

### Details
- Desktop last modified: [timestamp]
- Web last sync: [timestamp]
- Time delta: [duration]

## Recommendations
[Based on status, suggest actions]
```

## Gramps Web API

If Gramps Web is running at `http://localhost:5000`:

- Health check: `GET /api/health`
- Tree info: `GET /api/trees/` (requires auth)

**Credentials location**: `~/.config/grampsweb/credentials.json`

See `gramps` skill > `lib/web-api.md` for authentication pattern.

## Tips

- Sync after each editing session
- Use Gramps Desktop's "Gramps Web Sync" addon
- Check Docker status: `docker ps | grep grampsweb`
