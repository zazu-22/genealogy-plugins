# WikiTree API Reference

## Client Library

Location: `~/code/genealogy_clients/lib/wikitree_client/`

Usage pattern (always `cd` first):
```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.wikitree_client import WikiTreeClient
client = WikiTreeClient()
# ... use client methods
"
```

## Methods

### search_person(last_name, ...)

Search profiles by name and vital details.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| last_name | str | Yes | Last name at birth |
| first_name | str | No | First name |
| birth_date | str | No | Birth year (YYYY) or date (YYYY-MM-DD) |
| death_date | str | No | Death year or date |
| birth_location | str | No | Birth location (state, country) |
| death_location | str | No | Death location |
| fields | str | No | Comma-separated fields (default: vital info) |
| limit | int | No | Max results (max 1000, default 100) |
| start | int | No | Pagination offset |

Returns: `{"status": int, "total": int, "matches": [...]}`

### get_person(key, fields)

Get a single profile by WikiTree ID or page name.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| key | str/int | Yes | WikiTree ID number or "Surname-1234" |
| fields | str | No | Fields to return (default: extended + family) |

Returns: Profile dict with all requested fields.

### get_bio(key)

Get biography text (wiki markup) for a profile.

### get_relatives(keys, ...)

Get parents, spouses, children, siblings for one or more profiles.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| keys | list | Yes | WikiTree IDs or page names |
| get_parents | bool | No | Include parents (default True) |
| get_spouses | bool | No | Include spouses (default True) |
| get_children | bool | No | Include children (default True) |
| get_siblings | bool | No | Include siblings (default False) |

### get_ancestors(key, depth, fields)

Get ancestors up to `depth` generations (max ~10).

### get_descendants(key, depth, fields)

Get descendants up to `depth` generations (max ~5).

### search_all(last_name, ...) -> Iterator

Auto-paginating generator that yields individual profile dicts.
Stops at `max_results` (default 1000).

## Default Fields

```
Id, Name, FirstName, MiddleName, LastNameAtBirth, LastNameCurrent,
BirthDate, BirthDateDecade, BirthLocation,
DeathDate, DeathDateDecade, DeathLocation,
Gender, IsLiving, Privacy
```

## Extended Fields (for get_person)

Default fields plus: `Father, Mother, Spouses, Children, DataStatus, Connected, Manager`
