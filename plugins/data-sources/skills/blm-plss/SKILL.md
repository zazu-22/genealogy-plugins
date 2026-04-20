---
name: blm-plss
description: Query the BLM National PLSS CadNSDI ArcGIS REST service — Public Land Survey System townships, sections, aliquots, principal meridians, and state boundaries. Use for resolving township/range/section identifiers, looking up which PLSS unit contains a lat/lon point, fetching survey geometry, or seeding geo-infra `locations` rows. No authentication required.
---

# BLM National PLSS CadNSDI Integration

Query the Bureau of Land Management's National PLSS Cadastral Publication Data
Standard via its ArcGIS REST MapServer. No authentication. Server cap: 2000
records per request (handled transparently by the client).

Service: `https://gis.blm.gov/arcgis/rest/services/Cadastral/BLM_Natl_PLSS_CadNSDI/MapServer`

## When to use

- Resolving township/range/section text (e.g., "T5N R7W") to canonical PLSSID
- Looking up which PLSS section/aliquot contains a known lat/lon
- Bulk-seeding geo-infra `locations` rows for a county or research area
- Fetching survey polygon geometry for mapping or adjacency analysis
- Verifying a deed/patent's PLSS recital against the authoritative survey grid

## Quick Start — Township + Section Lookup

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.blm_plss_client import PLSSClient
c = PLSSClient()
# Coshocton USMD T5N R7W — PRINMERCD=48 is 'Base Line of the US Military Survey'
twp = c.query_townships(state='OH', meridian='48', twp='5N', rng='7W', format='json')
for f in twp['features']:
    a = f['attributes']
    print(f\"PLSSID={a['PLSSID']} TWNSHPLAB={a['TWNSHPLAB']}\")
secs = c.query_sections(state='OH', meridian='48', twp='5N', rng='7W', format='json')
print(f'sections: {len(secs[\"features\"])}')
"
```

## Quick Start — Point Lookup (lat/lon → containing aliquot)

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.blm_plss_client import PLSSClient
c = PLSSClient()
# Returns Intersected/aliquot features intersecting the point (geometry on by default)
hits = c.locate_point(lat=40.345, lon=-82.012, layer='aliquot', format='json')
for f in hits['features']:
    a = f['attributes']
    print(f\"{a.get('PLSSID')} S{a.get('FRSTDIVNO')} \"
          f\"qsec={a.get('QSEC')} qqsec={a.get('QQSEC')} lot={a.get('GOVLOT')}\")
"
```

## Quick Start — Identifier Lookup

```python
cd ~/code/genealogy_clients && uv run python3 -c "
from lib.blm_plss_client import PLSSClient
c = PLSSClient()
# Resolve a known PLSSID (e.g., from another agency's data)
data = c.get_by_plssid('OH480050N0070W0', layer='township', geometry=True, format='json')
print(data['features'][0]['attributes']['TWNSHPLAB'])
"
```

## CLI

```bash
# Attribute query
python -m blm_plss_client query --state OH --meridian 48 --twp 5N --rng 7W --layer section --format geojson

# With geometry
python -m blm_plss_client query --state OH --meridian 48 --twp 5N --rng 7W --layer township --geometry --output twp.geojson

# Point lookup
python -m blm_plss_client locate --lat 40.345 --lon -82.012 --layer aliquot

# By PLSSID
python -m blm_plss_client by-plssid OH480050N0070W0

# Cache management
python -m blm_plss_client clear-cache
```

## Layers

| ID | Name | Description | Use |
|----|------|-------------|-----|
| 0 | State Boundaries | Census 2017 state polygons | Bounding-box pre-filter |
| 1 | PLSS Township | Standard 6×6 mile (or USMD 5×5 mile) survey townships | Jurisdictional spine |
| 2 | PLSS Section | First Division (sections 1–36 or 1–25) | Section-level lookup |
| 3 | PLSS Intersected | Atomic-level features (aliquots where published) | Finest grain |

## CRITICAL: Coverage Gaps

**Ohio (and other Eastern states) lack sub-section subdivisions in BLM CadNSDI.**
The Intersected layer for OH USMD (PRINMERCD=48) and OH non-USMD (e.g., PRINMERCD=38)
contains section-level features only — `QSEC`, `QQSEC`, `GOVLOT`, `SECDIVLAB` are NULL.
Western states (WY, MT, etc.) have full aliquot coverage.

**For Ohio aliquots, derive from source documents** (patents, deeds, surveys), not BLM bulk data.
The geo-infra project's `locations` aliquot rows are correctly created from source attestations
during evidence ingest, not from this client.

**USMD townships are 5×5 = 25 sections, not 36.** Don't validate USMD imports against the
standard 36-section count.

## Caching

- Default cache: `~/.cache/blm_plss/` with 30-day TTL
- Cache key: SHA-1 of canonicalized URL + sorted params
- Bypass with `PLSSClient(no_cache=True)` or CLI `--no-cache`
- Clear with `client.clear_cache()` or `python -m blm_plss_client clear-cache`

## Pagination

Service caps each response at 2000 records. The client handles pagination
transparently via `resultOffset` and `exceededTransferLimit`. For large pulls
(state-level Township queries, ~1000 features for Ohio), expect multiple
underlying requests.

## Key Fields by Layer

**Township (layer 1):** PLSSID, TWNSHPLAB, TWNSHPNO, TWNSHPDIR, RANGENO, RANGEDIR,
PRINMERCD, PRINMER, STATEABBR, SRVNAME, SECSRVNAME, STEWARD

**Section (layer 2):** PLSSID (parent township), FRSTDIVID, FRSTDIVNO, FRSTDIVTYP,
FRSTDIVLAB, SURVTYP, SOURCEDATE

**Intersected (layer 3):** All Township + Section fields plus SECDIVID, SECDIVTYP,
SECDIVNO, SECDIVLAB, QSEC, QQSEC, GOVLOT, GISACRE, RECRDAREATX, RECRDAREANO

## Spatial Reference

- Default input/output: EPSG:4326 (WGS84 lat/lon) — what the client uses
- Service native: EPSG:102100 (Web Mercator) — converted automatically
- Override via `in_sr=`, `out_sr=` on low-level `query()` if needed

## See Also

- `~/code/genealogy_clients/lib/blm_plss_client/` for source
- `scripts/import_blm_plss.py` for the geo-infra bulk-import driver (consumes
  this client's GeoJSON output)

- `governance/codes/RC-015-canonical-location-and-geo-temporal-evidence-lifecycle.md`
  for the rules governing how PLSS data lands in the `locations` schema
