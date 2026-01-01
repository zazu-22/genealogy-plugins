# Frontmatter Schema Reference

Complete YAML frontmatter specifications for genealogy vault notes.

## Person Note Schema

```yaml
---
# Required fields
type: person
gramps_id: "I0001"         # Gramps person ID

# Canvas Roots (if imported)
cr_id: "abc123"            # Canvas Roots unique ID - NEVER DELETE

# Dates (ISO 8601 preferred, flexible formats accepted)
birth_date: 1850-03-15     # or "about 1850" or "before 1850"
death_date: 1920-07-22     # omit for living persons
birth_place: "[[Zanesville, Muskingum County, Ohio]]"
death_place: "[[Columbus, Franklin County, Ohio]]"

# Family links (wikilinks)
father: "[[John Smith (1820-1890)]]"
mother: "[[Mary Jones (1825-1900)]]"
spouse:
  - "[[Jane Doe (1855-1930)]]"
children:
  - "[[Child One (1875-1950)]]"
  - "[[Child Two (1878-1960)]]"

# Optional metadata
gender: male | female | unknown
occupation: "Farmer"
religion: "Methodist"
aliases:
  - "Johnny Smith"
  - "J. Smith"
tags:
  - immigrant
  - civil-war-veteran
---
```

## Source Note Schema

```yaml
---
type: source
source_type: census | vital | church | land | newspaper | military | probate | tax | directory | other

# Evidence Explained classification
ee_category: "Chapter 6: Census Records"
ee_section: "6.20 Federal Population Schedules"

# Repository
repository: "[[National Archives]]"
repository_location: "Washington, D.C."
call_number: "NARA M432, Roll 123"

# Citation components
title: "1850 U.S. Census"
creator: "U.S. Bureau of the Census"
publication_date: 1850
jurisdiction: "Muskingum County, Ohio"

# Access information
access_date: 2024-01-15
access_method: digital | microfilm | original
url: "https://www.ancestry.com/..."
citing: "NARA microfilm M432, roll 123"

# Quality assessment
originality: original | derivative
informativeness: primary | secondary | indeterminate
reliability: high | medium | low
---
```

## Place Note Schema

```yaml
---
type: place

# Hierarchical location (specific to general)
hierarchy: "Zanesville, Muskingum County, Ohio, USA"
short_name: "Zanesville"

# Geographic coordinates
coordinates: [39.9404, -82.0132]

# Jurisdictional history
historical_names:
  - name: "Westbourne"
    years: "1797-1801"
jurisdictional_changes:
  - date: 1804
    change: "Ohio became a state"
  - date: 1803
    change: "Muskingum County formed from Washington County"

# Research information
available_records:
  - "Vital records (1867-present)"
  - "Land records (1800-present)"
  - "Probate records (1804-present)"
repositories:
  - "[[Muskingum County Courthouse]]"
  - "[[Ohio History Connection]]"

# Geographic context
parent_place: "[[Muskingum County, Ohio]]"
fips_code: "39119"
---
```

## Event Note Schema

```yaml
---
type: event
event_type: birth | death | marriage | burial | immigration | naturalization | military | occupation | residence | other

date: 1850-03-15
place: "[[Zanesville, Muskingum County, Ohio]]"

# Participants
participants:
  - person: "[[John Smith (1820-1890)]]"
    role: principal
  - person: "[[Mary Jones (1825-1900)]]"
    role: spouse

# Evidence
sources:
  - "[[1850 Census - Muskingum County]]"
  - "[[Smith Family Bible]]"
---
```

## Date Formats

Obsidian genealogy notes accept flexible date formats:

| Format | Example | Use Case |
|--------|---------|----------|
| ISO 8601 | `1850-03-15` | Exact dates |
| Year only | `1850` | Approximate year |
| About | `about 1850` | Estimated dates |
| Before/After | `before 1850` | Terminus dates |
| Between | `between 1848 and 1852` | Date ranges |
| Quarter | `Q2 1850` | Quarter precision |
