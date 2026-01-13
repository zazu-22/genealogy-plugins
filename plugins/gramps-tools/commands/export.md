---
description: Export Gramps tree in various formats
allowed-tools: [Bash, Read]
argument-hint: "--format <xml|gedcom|web>"
---

# Export Tree

Export the Gramps family tree in various formats.

## API-First Notice

**Preferred method**: Use the Gramps Web API for exports. The CLI commands below are deprecated for Claude Code use but preserved for reference.

### API Export Endpoints

| Format | API Endpoint | Notes |
|--------|-------------|-------|
| XML (Gramps) | `GET /api/exporters/gramps` | Primary backup format |
| GEDCOM | `GET /api/exporters/gedcom` | For sharing with other software |
| Web | Not available via API | Use Gramps Desktop |

## Formats

| Format | Description | Output |
|--------|-------------|--------|
| `xml` | Uncompressed Gramps XML | `.gramps` file |
| `gedcom` | GEDCOM 5.5.1 for sharing | `.ged` file |
| `web` | Narrated Web Site | HTML folder |

## Instructions

### Preferred: API Export

```python
from gramps_web_client import GrampsAPIClient
import urllib.request

# Automatic credential loading
client = GrampsAPIClient()

# Note: Export functionality not yet in GrampsAPIClient
# Use direct API call with client's auth token:
token = client._get_auth_token()

# XML Export
req = urllib.request.Request(
    f"{client.credentials.url}/api/exporters/gramps",
    headers={"Authorization": f"Bearer {token}"}
)
with urllib.request.urlopen(req) as resp:
    with open('/Users/jasonshaffer/Genealogy/Exports/family-tree.gramps', 'wb') as f:
        f.write(resp.read())

# GEDCOM Export
req = urllib.request.Request(
    f"{client.credentials.url}/api/exporters/gedcom",
    headers={"Authorization": f"Bearer {token}"}
)
with urllib.request.urlopen(req) as resp:
    with open('/Users/jasonshaffer/Genealogy/Exports/family-tree.ged', 'wb') as f:
        f.write(resp.read())
```

**Note**: Export endpoints will be added to GrampsAPIClient in a future update.

### Legacy: CLI Export (Deprecated)

**WARNING**: CLI is unreliable on macOS. Use API instead.

#### XML Export
```bash
# Deprecated for Claude Code - use API instead
gramps -O "Shaffer-Richardson" -e ~/Genealogy/Exports/family-tree.gramps -f gramps-xml
```

#### GEDCOM Export
```bash
# Deprecated for Claude Code - use API instead
gramps -O "Shaffer-Richardson" -e ~/Genealogy/Exports/family-tree.ged -f gedcom
```

#### Web Export
```bash
# No API alternative - use Gramps Desktop for web export
gramps -O "Shaffer-Richardson" -e ~/Genealogy/Exports/web/ -f navwebpage
```

## Export Locations

| Type | Destination |
|------|-------------|
| Backups (XML) | `~/Genealogy/git-exports/` |
| Sharing (GEDCOM) | `~/Genealogy/Exports/` |
| Publishing (Web) | `~/Genealogy/Exports/web/` |

## Output

Report export status:

```
# Export Report
Date: [timestamp]
Tree: Shaffer-Richardson
Format: [format]

## Status: [SUCCESS/FAILED]

## Details
- Output: [path]
- File size: [size]
- Duration: [time]

## Contents (for GEDCOM/XML)
- Persons: [count]
- Families: [count]
- Sources: [count]
- Places: [count]
```

## Tips

- Use XML for backups (version-control friendly)
- Use GEDCOM for sharing with other software
- Use Web for publishing family history online
- Always use uncompressed XML for meaningful git diffs

## GEDCOM Export Considerations

### What Exports
- Source title, author, publication info (stitle, sauthor, spubinfo)
- Citation page details
- Notes attached to sources/citations
- Repository references

### What Does NOT Export
- **Source/Citation Attributes** - have no GEDCOM equivalent
- Custom attribute types beyond standard GEDCOM fields

### Best Practices Before GEDCOM Export

1. **Use Notes for digital access information** instead of Attributes:
   ```
   Digital access: [Website] ([URL] : accessed [Date])
   ```

2. **Verify source consolidation** follows Evidence Explained patterns:
   - One source per census year (citations have ED/sheet/line)
   - One source for Find A Grave (citations have memorial numbers)
   - Separate sources for each newspaper article, book, interview

3. **Check citation page formats** are complete:
   - Census: `[State], [County], [Township], ED [X-Y], Sheet [Z], Line [L]`
   - Vital: `certificate no. [number]`
   - Cemetery: `memorial [number] for [Name], [Cemetery]`

See `docs/gedcom-gramps-field-mapping.md` for complete field mapping guidance.
