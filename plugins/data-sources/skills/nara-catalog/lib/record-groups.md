# NARA Record Groups for Genealogical Research

## Primary Genealogical Record Groups

### RG 15 — Department of Veterans Affairs
**Key content**: Pension application files (Revolutionary War, War of 1812, Civil War, Indian Wars)
**Microfilm**: M804 (Rev War), M805 (selected states), T288 (War of 1812)
**Digital status**: Heavily digitized via Fold3 partnership. Many images available directly through NARA S3.
**Research value**: Pension files contain depositions with family details, ages, residences, service history, and witness testimony — often the richest narrative source for pre-1850 research.

### RG 29 — Bureau of the Census
**Key content**: Population schedules, enumeration district (ED) maps and descriptions
**Digital status**: 1940 and 1950 censuses fully on AWS S3. Earlier censuses via partners (Ancestry/FamilySearch).
**Note**: Search returns ED-level items; use AWS S3 for direct image access to 1940/1950 censuses.

### RG 36 — U.S. Customs Service
**Key content**: Passenger arrival lists (ship manifests), 1820–1982
**Digital status**: Partially digitized. Most images via Ancestry.

### RG 49 — Bureau of Land Management (General Land Office)
**Key content**: Federal land patents, homestead files, bounty land warrants
**Note**: BLM GLO website (glorecords.blm.gov) has CSV bulk downloads. NARA holds case files for failed applications.

### RG 85 — Immigration and Naturalization Service
**Key content**: Naturalization records, alien registration files
**Digital status**: Varies by court/state. FamilySearch has many.

### RG 94 — Adjutant General's Office
**Key content**: Military service records (compiled service records, muster rolls), Confederate applications for pardon
**Digital status**: Compiled service records increasingly digitized. Pardon applications often have personal detail.

### RG 109 — War Department Collection of Confederate Records
**Key content**: Confederate military records, compiled service records
**Digital status**: Largely digitized via Fold3.

### RG 110 — Provost Marshal General's Bureau (Civil War)
**Key content**: Civil War draft records, deserter files
**Digital status**: Partially digitized.

### RG 147 — Selective Service System
**Key content**: WWI and WWII draft registration cards
**Digital status**: WWI — FamilySearch/Ancestry. WWII — NARA bulk downloads available.

### RG 217 — General Accounting Office
**Key content**: Bounty land warrant applications, land claims
**Digital status**: Limited digitization.

## Less Common but Useful Record Groups

| RG | Name | Use Case |
|----|------|----------|
| 21 | District Courts | Naturalization, civil/criminal cases |
| 26 | Coast Guard | Merchant marine records |
| 48 | Interior Department | Dawes Rolls, Indian affairs |
| 75 | Bureau of Indian Affairs | Tribal records, allotments |
| 92 | Quartermaster General | Burial records, post records |
| 153 | Judge Advocate General (Army) | Court martial records |
| 163 | Selective Service (WWII) | Draft classification records |
| 393 | Continental/Confederation Congress | Pre-Constitution records |

## Useful Search Patterns

```python
# Rev War pension for specific person
searcher.search('"Richardson" "Revolutionary War Pension"', level='fileUnit')

# War of 1812 pension by state
searcher.search_record_group(15, '"War of 1812" Virginia', level='fileUnit')

# Confederate pardon applications
searcher.search_record_group(94, '"Richardson" "Confederate" "Pardon"')

# Census ED maps for a county
searcher.search_record_group(29, '"Hardy County" "enumeration district"')

# Bounty land warrants
searcher.search_record_group(217, '"Richardson" Virginia')
```
