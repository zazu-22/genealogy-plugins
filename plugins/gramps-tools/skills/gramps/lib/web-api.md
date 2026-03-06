# Gramps Web API

Reference for the Gramps Web REST API.

## Overview

Gramps Web provides a RESTful API for programmatic access to genealogical data.

- **Documentation**: https://gramps-project.github.io/gramps-web-api/
- **Local endpoint**: `http://localhost:5000/api/`

## Recommended: GrampsAPIClient Library

**Always use GrampsAPIClient for Gramps Web API interactions.**

Library location: `~/code/gramps_plugins/lib/gramps_web_client/`

### Installation

```bash
cd ~/Genealogy/<project>
uv add --editable ~/code/gramps_plugins
```

### Quick Start

```python
from gramps_web_client import GrampsAPIClient

# Automatic credential loading from ~/.config/grampsweb/credentials.json
client = GrampsAPIClient()

# Get sources with pagination
sources = client.get_sources(limit=10, offset=0)

# Get specific source
source = client.get_source(handle)

# Create new source
new_source = client.create_source({
    "_class": "Source",
    "title": "1900 U.S. Census"
})

# Update source (full object not required - client handles merge)
client.update_source(handle, {"title": "Updated Title"})

# Delete source
client.delete_source(handle)
```

### Dry-Run Mode

Test operations safely without modifying data:

```python
client = GrampsAPIClient(dry_run=True)

# All operations log but don't execute
client.create_source(data)  # Logs: "DRY RUN: Would create source"
client.update_source(handle, data)  # No actual changes
```

### Error Handling

```python
from gramps_web_client import GrampsAPIClient, NotFoundError, AuthenticationError

client = GrampsAPIClient()

try:
    source = client.get_source("invalid_handle")
except NotFoundError:
    print("Source not found")
except AuthenticationError:
    print("JWT token expired or invalid")
```

### Pagination

```python
# Get all sources in batches
offset = 0
limit = 100

while True:
    batch = client.get_sources(limit=limit, offset=offset)
    if not batch:
        break

    for source in batch:
        print(source["title"])

    offset += limit
```

### Available Methods

| Method | Purpose |
|--------|---------|
| `get_sources(limit, offset)` | List sources with pagination |
| `get_source(handle)` | Get specific source |
| `create_source(data)` | Create new source |
| `update_source(handle, data)` | Update source (automatic full object merge) |
| `delete_source(handle)` | Delete source |
| `get_citations(limit, offset)` | List citations with pagination |
| `get_citation(handle)` | Get specific citation |
| `update_citation(handle, data)` | Update citation |
| `add_tag_to_citation(citation_handle, tag_handle)` | Add tag to citation |
| `remove_tag_from_citation(citation_handle, tag_handle)` | Remove tag |

### Real-World Examples

Production usage in `~/code/gramps_plugins/`:

- **Census migration**: `tools/census_migration/cli.py`
  - Bulk source updates with dry-run validation
  - Transaction auditing
  - Pagination for large datasets

- **Source updates**: `tools/census_migration/migrator.py`
  - Automatic full object merge handling
  - Error recovery
  - Progress tracking

- **Citation deduplication**: `tools/census_migration/deduplicator.py`
  - Citation merging with conflict resolution
  - Tag management
  - Batch operations

## Container Management

### Docker Commands
```bash
# Start Gramps Web
cd ~/.config/containers/grampsweb && docker compose up -d

# Stop
docker compose down

# View logs
docker logs -f grampsweb

# Restart
docker compose restart
```

### Container Paths
```
~/.config/containers/grampsweb/docker-compose.yml  # Configuration
~/.local/share/containers/grampsweb/db/            # Database
~/.local/share/containers/grampsweb/media/         # Media files
~/.local/share/containers/grampsweb/users/         # User database
```

## Credentials

API credentials are stored at `~/.config/grampsweb/credentials.json` (encrypted via chezmoi with age):

```json
{
  "local": {
    "url": "http://localhost:5000",
    "username": "...",
    "password": "..."
  },
  "remote": {
    "url": "http://jasons-mac-studio:5000",
    "username": "...",
    "password": "..."
  }
}
```

GrampsAPIClient loads these automatically. Specify environment with:

```python
client = GrampsAPIClient(environment="remote")  # Default: "local"
```

## Common Operations

All examples use GrampsAPIClient. For raw urllib patterns, see [Advanced: Raw urllib](#advanced-raw-urllib).

### Creating and Linking Citations

```python
from gramps_web_client import GrampsAPIClient

client = GrampsAPIClient()

# 1. Create citation
citation_data = {
    "_class": "Citation",
    "source_handle": source_handle,
    "page": "Page 5, Line 23",
    "confidence": 2  # Normal confidence
}
result = client.create_citation(citation_data)  # Returns full object with handle
citation_handle = result["handle"]

# 2. Get event to update
event = client.get_event(event_handle)

# 3. Add citation
if "citation_list" not in event:
    event["citation_list"] = []
event["citation_list"].append(citation_handle)

# 4. Update event
client.update_event(event_handle, event)
```

### Confidence Levels

| Value | Level | When to Use |
|-------|-------|-------------|
| 0 | Very Low | Unverified user-submitted data, questionable sources |
| 1 | Low | Derivative with potential errors, distant hearsay |
| 2 | Normal | Derivative source, consistent with others (default) |
| 3 | High | Original record, indirect evidence |
| 4 | Very High | Original record, direct evidence, firsthand knowledge |

See `source-analysis` skill for mapping Mills' evidence classification.

### Batch Operations with Dry-Run

```python
# Test migration with dry-run first
client = GrampsAPIClient(dry_run=True)

for source in sources_to_migrate:
    new_title = transform_title(source["title"])
    client.update_source(source["handle"], {"title": new_title})
    # Logs but doesn't execute

# Verify output, then run for real
client = GrampsAPIClient(dry_run=False)
for source in sources_to_migrate:
    new_title = transform_title(source["title"])
    client.update_source(source["handle"], {"title": new_title})
```

## API Endpoints Reference

For direct API access (when library methods don't exist):

### People
```
GET    /api/people/                    # List all people
GET    /api/people/{handle}            # Get specific person
GET    /api/people/{handle}/profile    # Get person with profile info
POST   /api/people/                    # Create person
PUT    /api/people/{handle}            # Update person
DELETE /api/people/{handle}            # Delete person
```

### Families
```
GET    /api/families/                  # List all families
GET    /api/families/{handle}          # Get specific family
POST   /api/families/                  # Create family
PUT    /api/families/{handle}          # Update family
DELETE /api/families/{handle}          # Delete family
```

### Events
```
GET    /api/events/                    # List all events
GET    /api/events/{handle}            # Get specific event
POST   /api/events/                    # Create event
PUT    /api/events/{handle}            # Update event
DELETE /api/events/{handle}            # Delete event
```

### Sources & Citations
```
GET    /api/sources/                   # List all sources
GET    /api/sources/{handle}           # Get specific source
POST   /api/sources/                   # Create source
PUT    /api/sources/{handle}           # Update source
DELETE /api/sources/{handle}           # Delete source
GET    /api/citations/                 # List all citations
GET    /api/citations/{handle}         # Get specific citation
POST   /api/citations/                 # Create citation
PUT    /api/citations/{handle}         # Update citation
DELETE /api/citations/{handle}         # Delete citation
```

### Places
```
GET    /api/places/                    # List all places
GET    /api/places/{handle}            # Get specific place
POST   /api/places/                    # Create place
PUT    /api/places/{handle}            # Update place
```

### Media
```
GET    /api/media/                     # List all media objects
GET    /api/media/{handle}             # Get media metadata
GET    /api/media/{handle}/file        # Download media file
POST   /api/media/{handle}/file        # Upload media file
```

### Search
```
GET    /api/search/?query=Smith        # Full-text search
GET    /api/search/?query=Smith&object_type=person
```

### Export
```
GET    /api/exporters/gramps           # Export to Gramps XML
GET    /api/exporters/gedcom           # Export to GEDCOM
```

### Transactions (Undo/History)
```
GET    /api/transactions/              # List transactions
GET    /api/transactions/history       # Revision history
POST   /api/transactions/history/{id}/undo  # Undo a transaction
```

## Query Parameters

### Pagination
```
GET /api/people/?page=1&pagesize=20
```

GrampsAPIClient uses `limit` and `offset` parameters internally.

### Filtering
```
GET /api/people/?gramps_id=I0001
GET /api/events/?type=Birth
```

### Profile Expansion
```
GET /api/people/{handle}?profile=all
GET /api/people/{handle}?profile=self,events,families
```

## Response Format

### Person Object
```json
{
  "handle": "_abc123",
  "gramps_id": "I0001",
  "gender": 1,
  "primary_name": {
    "first_name": "John",
    "surname_list": [{"surname": "Smith"}]
  },
  "birth_ref_index": 0,
  "event_ref_list": [...],
  "parent_family_list": [...],
  "family_list": [...]
}
```

### Event Object
```json
{
  "handle": "_xyz789",
  "gramps_id": "E0001",
  "type": {"_class": "EventType", "string": "Birth"},
  "date": {"_class": "Date", "dateval": [0, 0, 1850, false, 3, 15]},
  "place": "_place_handle",
  "description": ""
}
```

## Sync with Desktop

### Gramps Web Sync Addon
The desktop Gramps application can sync with Gramps Web using the "Gramps Web Sync" addon.

**Setup**:

1. Install addon in Gramps Desktop
2. Configure with Gramps Web URL and credentials
3. Sync handles bidirectional updates

**Conflict Resolution**:

- Desktop changes take priority by default
- Manual review for complex conflicts

## Security Considerations

- Run behind Tailscale VPN (no public exposure)
- Use strong passwords
- Regular backups before major changes
- Enable HTTPS in production

## Advanced: Raw urllib

**Only use raw urllib for standalone scripts without library access.**

For all other cases, use GrampsAPIClient (see top of document).

### Authentication with urllib

```python
import json
import urllib.request

# Read credentials
with open('/Users/jasonshaffer/.config/grampsweb/credentials.json') as f:
    creds = json.load(f)['local']

# Get JWT token
url = f"{creds['url']}/api/token/"
data = json.dumps({"username": creds['username'], "password": creds['password']}).encode()
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as resp:
    token = json.loads(resp.read())['access_token']

# Use token in subsequent requests
headers = {"Authorization": f"Bearer {token}"}

# Example: Get all people
req = urllib.request.Request(f"{creds['url']}/api/people/", headers=headers)
with urllib.request.urlopen(req) as resp:
    people = json.loads(resp.read())
```

### Full Object Required for PUT

The Gramps Web API requires the **full object** for PUT updates, not partial updates.

**Correct pattern:**
```python
# 1. Get full object
req = urllib.request.Request(f"{BASE_URL}/api/events/{event_handle}", headers=headers)
with urllib.request.urlopen(req) as resp:
    event = json.loads(resp.read())

# 2. Modify the field you need
event['citation_list'].append(new_citation_handle)

# 3. Send full object back
req = urllib.request.Request(
    f"{BASE_URL}/api/events/{event_handle}",
    data=json.dumps(event).encode(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method='PUT'
)
urllib.request.urlopen(req)
```

**This will NOT work:**
```python
# Partial update - FAILS
req = urllib.request.Request(
    f"{BASE_URL}/api/events/{event_handle}",
    data=json.dumps({"citation_list": [citation_handle]}).encode(),
    headers=headers,
    method='PUT'
)
# Error: "Unknown classes: Event, citation_list"
```

**Note**: GrampsAPIClient handles full object merging automatically. This is only an issue with raw urllib.

### Common Mistakes

| Mistake | Result | Solution |
|---------|--------|----------|
| Sending partial object | "Unknown classes" error | GET full object first, modify, PUT back |
| Missing `_class` field | Validation error | Include `_class` in all objects |
| Wrong handle format | Object not found | Use full handle from GET response |
| Expired JWT token | 401 Unauthorized | Refresh token or use GrampsAPIClient (auto-refresh) |
