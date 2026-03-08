# loc.gov Collections Reference

## Client Library

Location: `~/code/genealogy_clients/lib/loc_gov_client/`

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.loc_gov_client import CollectionSearcher
searcher = CollectionSearcher()
# ... use searcher methods
"
```

## Methods

### search_manuscripts(query, state, date_start, date_end, facets, ...)

Search manuscript collections (letters, diaries, legal documents).

### search_maps(query, state, date_start, date_end, facets, ...)

Search map collections (county maps, survey plats, military maps).

### search_photos(query, state, date_start, date_end, facets, ...)

Search photograph collections.

### search_collection(collection_slug, query, ...)

Search a specific named collection by its URL slug.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_slug | str | Yes | URL slug (e.g., "civil-war-maps") |
| query | str | No | Search terms |
| state | str | No | State filter |
| date_start | str | No | Start year |
| date_end | str | No | End year |
| facets | dict | No | Additional facet filters |

### list_collections(query, page, count)

Browse available collections.

### get_item_citation(item_url) -> str | None

Get the ready-made citation from a loc.gov item.

## Common Parameters (all search methods)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | str | "" | Search terms |
| state | str | "" | State filter (e.g., "virginia") |
| date_start | str | "" | Start year |
| date_end | str | "" | End year |
| facets | dict | None | Extra facets as key:value pairs |
| page | int | 1 | Result page number |
| count | int | 25 | Results per page (max 100) |

## Facets

Facets provide structured filtering. Common genealogical facets:

| Facet Key | Example Values |
|-----------|---------------|
| location | virginia, augusta county |
| original-format | manuscript, map, photo |
| subject | genealogy, land grants |
| contributor | library of virginia |
| language | english |

Pass as dict: `facets={"subject": "land grants"}`

## Genealogically Useful Collections

| Collection | Slug | Content |
|------------|------|---------|
| Civil War Maps | civil-war-maps | Military and county maps 1861-1865 |
| Sanborn Maps | sanborn-maps | Town fire insurance maps (detail) |
| Panoramic Maps | panoramic-maps | Bird's-eye views of towns |
| American Colonization Society | american-colonization-society | Records of colonization efforts |

Use `list_collections(query="virginia")` to discover more.
