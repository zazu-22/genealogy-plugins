---
name: wikitree
description: Search WikiTree's 37M+ free genealogical profiles. Use when looking up surname distributions, finding potential matches for research subjects, or exploring connected family trees. Covers profile search, ancestor/descendant traversal, and biography retrieval.
---

# WikiTree API Integration

Search WikiTree's collaborative genealogy database of 37M+ profiles.
No authentication required. All public profiles are accessible.

## Quick Start

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.wikitree_client import WikiTreeClient
client = WikiTreeClient()
result = client.search_person('Shaffer', birth_location='Virginia', limit=10)
print(f'Found {result[\"total\"]} profiles')
for m in result['matches'][:5]:
    print(f'  {m[\"Name\"]} — {m[\"FirstName\"]} {m[\"LastNameAtBirth\"]} b.{m.get(\"BirthDate\",\"?\")} {m.get(\"BirthLocation\",\"?\")}')
"
```

## Key Points

- **Rate limit**: 1 request/second (enforced by client)
- **App ID**: `SRGenealogy` (included automatically)
- **All requests**: POST to `https://api.wikitree.com/api.php`
- **Response format**: JSON array `[{status, ...}]`
- **Privacy**: Only public profiles are returned; living people are excluded

## Important

WikiTree data is user-contributed and collaborative. Treat results as **leads
for verification**, not as authoritative sources. Always cross-reference with
primary records before incorporating into research conclusions.

See `lib/` for detailed API reference and search patterns.
