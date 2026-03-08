---
name: loc-gov
description: Search Library of Congress free APIs — Chronicling America newspapers (12M+ pages with OCR text), plus manuscript, map, and photo collections. Use for historical newspaper mentions, county maps, manuscript finding aids, and historical photographs. Includes rate limiting to avoid 1-hour API blocks.
---

# Library of Congress API Integration

Access Chronicling America newspapers and loc.gov digital collections.
No authentication required. Rate limited to 15 req/min (server enforces 20/min with 1-hour block).

## Quick Start — Newspapers

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.loc_gov_client import NewspaperSearcher
searcher = NewspaperSearcher()
count = searcher.count(query='Richardson', state='virginia', date_start='1850', date_end='1900')
print(f'Found {count} newspaper pages')
result = searcher.search(query='Richardson', state='virginia', date_start='1850', date_end='1900', count=5)
for r in result.get('results', [])[:5]:
    print(f'  {r.get(\"date\", \"?\")} — {r.get(\"title\", \"?\")[:60]}')
"
```

## Quick Start — Collections

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.loc_gov_client import CollectionSearcher
searcher = CollectionSearcher()
result = searcher.search_maps(query='Augusta County', state='virginia', date_start='1780', date_end='1850', count=5)
for r in result.get('results', [])[:5]:
    title = r.get('title', '?')
    if isinstance(title, list): title = title[0]
    print(f'  {title[:70]}')
"
```

## CRITICAL: Rate Limiting

- **Limit**: 15 requests/minute (conservative; server cap is 20)
- **Penalty**: 1-hour block if exceeded
- **Rate limiter**: Automatic, file-based at `~/.cache/loc-gov-ratelimit.json`
- **Cross-process safe**: Uses file locking (`fcntl.flock()`)
- **Check status**: `searcher.client.rate_limit_status()`

The rate limiter is built into the client — you do not need to add sleep() calls.
If you see a 429 response, STOP and wait. The client will retry automatically.

## Key Points

- **Newspapers**: Chronicling America — 12M+ digitized pages with OCR text
- **Collections**: Manuscripts, maps, photos, and named collections
- **OCR quality**: Historical newspaper OCR is imperfect; search by keywords not exact phrases
- **Result cap**: loc.gov limits to 10,000 results per query — narrow with dates/location
- **Proximity search**: `search_person()` finds names within N words of each other
- **State filter note**: In proximity searches (`qs`/`ops`), state filtering may be less reliable than in standard queries

See `lib/` for detailed API reference and rate limit information.
