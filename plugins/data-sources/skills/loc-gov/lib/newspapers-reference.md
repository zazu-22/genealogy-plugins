# Chronicling America Newspapers Reference

## Client Library

Location: `~/code/genealogy_clients/lib/loc_gov_client/`

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.loc_gov_client import NewspaperSearcher
searcher = NewspaperSearcher()
# ... use searcher methods
"
```

## Methods

### search(query, state, date_start, date_end, ...)

Search newspaper pages by keyword.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | str | No | Full-text OCR search terms |
| state | str | No | State filter, lowercase ("virginia") |
| date_start | str | No | Start year ("1850") |
| date_end | str | No | End year ("1900") |
| page | int | No | Result page (default 1) |
| count | int | No | Results per page, max 100 (default 25) |
| sort | str | No | "date_asc", "date_desc", "relevancy" |

Returns: Dict with `results`, `pagination` (total, pages, current), `facets`.

### search_person(first_name, last_name, proximity, ...)

Proximity search for a person's name.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| first_name | str | Yes | First name |
| last_name | str | Yes | Last name |
| proximity | int | No | Max words between names (default 5) |
| state | str | No | State filter |
| date_start | str | No | Start year |
| date_end | str | No | End year |

**Note**: State filtering may be less reliable with proximity searches.
The `qs`/`ops` parameter combination interacts differently with location
filters than the standard `q` parameter.

### count(query, state, date_start, date_end)

Get total result count (cheap — 1 API call, 1 result returned).

### get_page_text(page_url)

Get OCR text for a specific page. Returns text string or None.

### search_all(query, ...) -> Iterator

Auto-paginating generator yielding individual results.
Max 200 results by default (configurable).

## Search Tips

- **State names are lowercase**: `state="virginia"` not `state="Virginia"`
- **Date ranges**: Use `date_start="1850", date_end="1900"`
- **OCR quality**: Historical newspapers have imperfect OCR — try name variants
- **Result cap**: loc.gov caps at 10,000 results — narrow searches to stay under
- **Page-level results**: Client always sets `dl=page` for individual pages
