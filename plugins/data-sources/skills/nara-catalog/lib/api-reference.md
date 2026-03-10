# NARA Catalog API v2 Reference

## Base URL

`https://catalog.archives.gov/api/v2/`

## Authentication

Header-based: `x-api-key: YOUR_KEY`

Credentials stored in `~/.config/nara/credentials.json`:
```json
{"api_key": "YOUR_KEY", "tier": "default", "monthly_limit": 10000}
```

## Endpoints

### Search Records

`GET /records/search`

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Keyword search. Supports quoted phrases: `"Hardy County"` |
| `naId` | integer | Fetch specific record by National Archives Identifier |
| `limit` | integer | Results per page (max 100, default 10) |
| `offset` | integer | Pagination offset |
| `levelOfDescription` | string | Filter: `item`, `fileUnit`, `series`, `recordGroup`, `collection` |
| `recordGroupNumber` | integer | Filter by NARA Record Group number |

### Response Structure

```json
{
  "body": {
    "hits": {
      "total": {"value": 12345, "relation": "eq"},
      "hits": [
        {
          "_id": "53866079",
          "_score": 100.67,
          "_source": {
            "metadata": {
              "controlGroup": {"type": "recordGroup", "naId": 344}
            },
            "record": {
              "naId": 53866079,
              "title": "...",
              "levelOfDescription": "fileUnit",
              "recordType": "description",
              "generalRecordsTypes": ["Textual Records"],
              "accessRestriction": {"status": "Unrestricted"},
              "useRestriction": {"status": "Unrestricted"},
              "digitalObjects": [
                {
                  "objectUrl": "https://s3.amazonaws.com/NARAprodstorage/...",
                  "objectFilename": "...",
                  "objectType": "Image (JPG)",
                  "objectId": "53866080"
                }
              ],
              "onlineResources": [
                {"url": "https://www.fold3.com/image/...", "description": "Fold3"}
              ],
              "microformPublications": [
                {"identifier": "M804", "title": "...", "note": "Roll 114."}
              ],
              "ancestors": [
                {"naId": 344, "title": "Records of VA", "levelOfDescription": "recordGroup"}
              ]
            }
          }
        }
      ]
    }
  }
}
```

## Search Syntax

- **Quoted phrases**: `"Hardy County"` — exact match
- **Multiple terms**: `Richardson Virginia` — all terms present
- **Combined**: `"Richardson" "Hardy County" Virginia pension`

## Python Client

```python
from lib.nara_catalog_client import CatalogSearcher

searcher = CatalogSearcher()

# Basic search
result = searcher.search('"Richardson" Virginia', limit=10)

# Person search (auto-quotes terms)
result = searcher.search_person("Richardson", state="Virginia", county="Hardy County")

# Record group search
result = searcher.search_record_group(15, '"Richardson" Virginia')

# Fetch specific record
record = searcher.get_record(53866079)

# Check quota
print(searcher.client.quota_status())
```

## Quota Management

- Monthly limit: 10,000 queries (resets on the 1st)
- Tracked locally in `~/.cache/nara-catalog-usage.json`
- Cross-process safe (file locking)
- `searcher.client.quota_status()` returns `{month, used, remaining, monthly_limit}`
