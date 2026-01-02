# Gramps Web API

Reference for the Gramps Web REST API.

## Overview

Gramps Web provides a RESTful API for programmatic access to genealogical data.

- **Documentation**: https://gramps-project.github.io/gramps-web-api/
- **Local endpoint**: `http://localhost:5000/api/`

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

## Authentication

### Python Standard Library (Recommended)

Use Python stdlib (no external dependencies) with credentials file:

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

### Token-Based Auth (curl)
```bash
# Get authentication token
curl -X POST http://localhost:5000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Response: {"access_token": "...", "refresh_token": "..."}
```

### Using the Token
```bash
curl http://localhost:5000/api/people/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Token Refresh
Access tokens expire. Use the refresh token to get a new access token:
```bash
curl -X POST http://localhost:5000/api/token/refresh/ \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

## API Endpoints

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
GET    /api/citations/                 # List all citations
GET    /api/citations/{handle}         # Get specific citation
```

### Places
```
GET    /api/places/                    # List all places
GET    /api/places/{handle}            # Get specific place
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

## Error Handling

### Common Errors
```json
{"error": "Object not found", "status": 404}
{"error": "Unauthorized", "status": 401}
{"error": "Validation error", "status": 422}
```

### Rate Limiting
- No built-in rate limiting (self-hosted)
- Consider nginx proxy for production

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:5000/api"
TOKEN = "your_access_token"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Get all people
response = requests.get(f"{BASE_URL}/people/", headers=headers)
people = response.json()

# Get specific person with profile
response = requests.get(
    f"{BASE_URL}/people/_abc123?profile=all",
    headers=headers
)
person = response.json()

# Search
response = requests.get(
    f"{BASE_URL}/search/?query=Shaffer",
    headers=headers
)
results = response.json()
```

## Security Considerations

- Run behind Tailscale VPN (no public exposure)
- Use strong passwords
- Regular backups before major changes
- Enable HTTPS in production
