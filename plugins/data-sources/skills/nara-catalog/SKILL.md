---
name: nara-catalog
description: Search the National Archives (NARA) Catalog API v2 — archival descriptions, digital object URLs, pension files, census metadata, military records, land records. Use when looking up NARA holdings, finding digitized record images, identifying record groups, or searching for specific persons in federal records. Requires API key (10K queries/month).
---

# NARA Catalog API v2 Integration

Search the National Archives online catalog for archival descriptions and digital objects.
API key required (stored in `~/.config/nara/credentials.json`). Rate: 10,000 queries/month.

## Quick Start — Search

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.nara_catalog_client import CatalogSearcher
searcher = CatalogSearcher()
result = searcher.search('\"Richardson\" \"Hardy County\" Virginia', limit=5)
print(f'Found {result[\"total\"]} records')
for r in result['results']:
    print(f'  [{r[\"naid\"]}] {r[\"level\"]}: {r[\"title\"][:100]}')
    if r['digital_objects']:
        print(f'    {len(r[\"digital_objects\"])} images available')
"
```

## Quick Start — Person Search

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.nara_catalog_client import CatalogSearcher
searcher = CatalogSearcher()
result = searcher.search_person('Richardson', state='Virginia', limit=5, level='fileUnit')
print(f'Found {result[\"total\"]} file units')
for r in result['results']:
    print(f'  [{r[\"naid\"]}] {r[\"title\"][:100]}')
"
```

## Quick Start — Record Group Search

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.nara_catalog_client import CatalogSearcher
searcher = CatalogSearcher()
# RG 15 = Veterans Affairs (pension files)
result = searcher.search_record_group(15, '\"Richardson\" Virginia', limit=5)
for r in result['results']:
    print(f'  [{r[\"naid\"]}] {r[\"title\"][:100]}')
    if r['digital_objects']:
        print(f'    First image: {r[\"digital_objects\"][0][\"url\"][:80]}')
"
```

## Key Points

- **Authentication**: `x-api-key` header; key from `~/.config/nara/credentials.json`
- **Monthly quota**: 10,000 queries tracked in `~/.cache/nara-catalog-usage.json`
- **Check quota**: `searcher.client.quota_status()` — shows used/remaining
- **Search syntax**: Supports quoted phrases (`"Hardy County"`), boolean operators
- **Levels**: `item`, `fileUnit`, `series`, `recordGroup`, `collection`
- **Digital objects**: Many records have direct S3 image URLs (free, no paywall)
- **Partner links**: Some images behind Fold3/Ancestry paywalls (in `online_resources`)

## Genealogically Important Record Groups

| RG | Name | Key Content |
|----|------|-------------|
| 15 | Veterans Affairs | Pension files (Rev War, War of 1812, Civil War) |
| 29 | Bureau of the Census | Census schedules, ED maps |
| 36 | U.S. Customs Service | Passenger arrival lists |
| 49 | Bureau of Land Management | Land patents, homestead files |
| 85 | Immigration & Naturalization | Naturalization records |
| 94 | Adjutant General's Office | Military service records |
| 109 | War Department | Civil War records |
| 110 | Provost Marshal General | Civil War draft records |
| 147 | Selective Service | WWI/WWII draft registration |
| 217 | General Accounting Office | Bounty land warrants |

## Result Fields

Each result includes:

- `naid` — National Archives Identifier (unique)
- `title` — Archival description title
- `level` — Hierarchy level (item/fileUnit/series/recordGroup)
- `digital_objects` — List of image URLs (S3 direct links when available)
- `online_resources` — Partner platform links (Fold3, Ancestry)
- `ancestors` — Parent series/record group hierarchy
- `microfilm` — Microfilm publication identifiers (M804, T778, etc.)
- `access_restriction` / `use_restriction` — Access status

## Important Notes

- **Free images**: Digital objects with `objectUrl` pointing to `s3.amazonaws.com/NARAprodstorage` are freely accessible
- **Paywall images**: Online resources linking to fold3.com or ancestry.com require subscriptions
- **Metadata only**: The API returns metadata and image URLs — not document content or OCR text
- **NAID persistence**: NAIDs are stable identifiers for citations

See `lib/` for detailed API reference and record group documentation.
