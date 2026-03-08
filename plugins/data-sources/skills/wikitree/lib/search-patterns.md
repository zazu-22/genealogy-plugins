# WikiTree Search Patterns for Genealogy

## Surname Survey

Start broad, then narrow. Useful for understanding surname distribution.

```python
# How many Shaffers in Virginia?
result = client.search_person('Shaffer', birth_location='Virginia')
print(f"Total Shaffer profiles in Virginia: {result['total']}")

# Narrow to specific time period
result = client.search_person('Shaffer', birth_location='Virginia',
                               birth_date='1800')  # Births around 1800
```

## Specific Ancestor Search

```python
# Search for a specific person
result = client.search_person('Richardson', first_name='Daniel',
                               birth_location='Virginia',
                               birth_date='1760')
for m in result['matches']:
    print(f"{m['Name']} b.{m.get('BirthDate','?')} {m.get('BirthLocation','?')}")
```

## Family Reconstruction

Once you find a candidate profile, explore their family:

```python
# Get the profile with family links
person = client.get_person('Richardson-12345')
print(f"Father: {person.get('Father')}")
print(f"Mother: {person.get('Mother')}")

# Get all relatives in one call
relatives = client.get_relatives(['Richardson-12345'],
                                  get_siblings=True)
```

## Ancestor Tree Exploration

```python
# Get 5 generations of ancestors
ancestors = client.get_ancestors('Richardson-12345', depth=5)
for a in ancestors:
    print(f"{a.get('Name')} b.{a.get('BirthDate','?')}")
```

## Cross-Reference Strategy

1. Search WikiTree for surname + location + approximate dates
2. Note WikiTree IDs of potential matches
3. Check biographies for source citations: `client.get_bio(wiki_id)`
4. Verify claims against primary records (census, vital records, deeds)
5. WikiTree profiles often cite sources — follow those to original records

## Limitations

- **User-contributed data**: Quality varies widely
- **Privacy**: Living people are excluded from search results
- **Search precision**: Location matching is fuzzy — "Virginia" may include West Virginia
- **Date matching**: Birth date search is approximate (+/-5 years typical)
- **No record images**: WikiTree has profiles, not source documents
