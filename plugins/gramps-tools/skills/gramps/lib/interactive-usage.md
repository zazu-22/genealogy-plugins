# Interactive GrampsAPIClient Usage

Guide for using GrampsAPIClient for ad-hoc queries and modifications without creating a dedicated project.

## Use Case

This pattern is for **Claude Code interactive sessions** where you need to:
- Query Gramps data in response to user questions
- Make quick modifications to the tree
- Test API operations
- Explore data without scaffolding a full project

## Quick Start

```bash
cd ~/code/gramps_plugins && uv run python3 -c "
from gramps_web_client import GrampsAPIClient

client = GrampsAPIClient()  # Auto-loads credentials
sources = client.get_sources()
print(f'Total sources: {len(sources)}')
"
```

## Why This Pattern Works

| Requirement | Solution |
|-------------|----------|
| **Dependencies** | `uv run` manages the virtual environment automatically |
| **Credentials** | GrampsAPIClient loads from `~/.config/grampsweb/credentials.json` |
| **No project setup** | Run directly from gramps_plugins directory |
| **Clean output** | Results print to stdout for user visibility |

## Common Patterns

### Query Data

```bash
cd ~/code/gramps_plugins && uv run python3 -c "
from gramps_web_client import GrampsAPIClient

client = GrampsAPIClient()

# Get all sources
sources = client.get_sources()
for source in sources[:5]:
    print(f'{source[\"title\"]} (handle: {source[\"handle\"][:8]}...)')
"
```

### Search People

```bash
cd ~/code/gramps_plugins && uv run python3 -c "
from gramps_web_client import GrampsAPIClient

client = GrampsAPIClient()

# Get all people
people = client.get_people()
print(f'Total people: {len(people)}')

# Find specific person
for person in people:
    if 'Smith' in person.get('primary_name', {}).get('surname_list', [{}])[0].get('surname', ''):
        name = person['primary_name']
        print(f'{name.get(\"first_name\", \"\")} {name[\"surname_list\"][0][\"surname\"]}')
"
```

### Create Objects (Dry-Run First)

```bash
# Step 1: Dry-run to verify
cd ~/code/gramps_plugins && uv run python3 -c "
from gramps_web_client import GrampsAPIClient

client = GrampsAPIClient(dry_run=True)  # Safe mode

person_data = {
    'primary_name': {
        'first_name': 'John',
        'surname_list': [{'surname': 'Smith'}]
    }
}

result = client.create_person(person_data)
print('Dry-run successful - no changes made')
"

# Step 2: Execute for real
cd ~/code/gramps_plugins && uv run python3 -c "
from gramps_web_client import GrampsAPIClient

client = GrampsAPIClient()  # Live mode

person_data = {
    'primary_name': {
        'first_name': 'John',
        'surname_list': [{'surname': 'Smith'}]
    }
}

result = client.create_person(person_data)
print(f'Created person with handle: {result[\"handle\"]}')
"
```

### Update Objects

```bash
cd ~/code/gramps_plugins && uv run python3 -c "
from gramps_web_client import GrampsAPIClient

client = GrampsAPIClient()

# Find source by title
sources = client.get_sources()
target = next((s for s in sources if '1900 Census' in s.get('title', '')), None)

if target:
    handle = target['handle']
    client.update_source(handle, {'title': '1900 U.S. Census, Updated'})
    print(f'Updated source {handle[:8]}...')
"
```

### Error Handling

```bash
cd ~/code/gramps_plugins && uv run python3 -c "
from gramps_web_client import GrampsAPIClient
from gramps_web_client.exceptions import GrampsAPIError

client = GrampsAPIClient()

try:
    sources = client.get_sources()
    print(f'Success: {len(sources)} sources')
except GrampsAPIError as e:
    print(f'API Error: {e}')
except Exception as e:
    print(f'Error: {e}')
"
```

## Known Limitations

### Pagination Parameters

The Gramps Web API may not support `limit`/`offset` parameters on all endpoints. If you see:

```
API error 422: {"error":{"code":422,"message":"query: limit: Unknown field."}}
```

**Solution:** Fetch all results and slice in Python:

```python
sources = client.get_sources()  # Get all
print(sources[:10])  # First 10
```

### Working Directory

**Always `cd` to `~/code/gramps_plugins`** before running `uv run`. This ensures:
- `uv` finds the `pyproject.toml` with dependencies
- The library can be imported correctly

### String Escaping

When using multi-line strings in `-c`, use proper escaping:

```bash
# Good: Use \n for newlines
uv run python3 -c "
from gramps_web_client import GrampsAPIClient
client = GrampsAPIClient()
print('Line 1')
print('Line 2')
"

# Bad: Actual newlines in -c argument can cause issues
```

## Comparison: Interactive vs Project-Based

| Aspect | Interactive (`uv run -c`) | Project-Based (`uv add --editable`) |
|--------|---------------------------|--------------------------------------|
| **Setup** | None - run immediately | Create project, add dependency |
| **Use Case** | One-off queries, quick mods | Scripts, tools, ongoing work |
| **Import** | `from gramps_web_client import ...` | `from gramps_web_client import ...` |
| **Dependencies** | Managed by uv run | Managed by project's pyproject.toml |
| **Best For** | Claude Code interactive sessions | Standalone tools (census_migration) |

## Troubleshooting

### "No module named 'gramps_web_client'"

**Problem:** Not running from the right directory or not using `uv run`

**Solution:**
```bash
cd ~/code/gramps_plugins && uv run python3 -c "..."
```

### "No module named 'requests'"

**Problem:** Trying to import directly without uv's environment

**Solution:** Use `uv run`, not raw `python3`

### "AttributeError: 'GrampsAPIClient' object has no attribute 'base_url'"

**Problem:** Trying to access internal attributes

**Solution:** Use public methods like `get_sources()`, `create_person()`, etc.

## Production Examples

For more complex usage, see standalone tools:
- `~/code/gramps_plugins/tools/census_migration/` - Full project structure
- Uses same GrampsAPIClient but with dedicated CLI, tests, docs

## When to Graduate to a Project

Consider creating a dedicated project when:
- **Script becomes reusable** - You'll run it multiple times
- **Multiple files** - Logic spans multiple modules
- **Testing needed** - Want to write unit tests
- **Configuration** - Needs settings files or CLI arguments
- **Distribution** - Others will use it

For one-off interactive queries, stick with the `uv run -c` pattern.
