---
description: Validate frontmatter in Obsidian vault notes
allowed-tools: [Read, Grep, Glob]
argument-hint: "--type <person|source|place> | --all"
---

# Validate Vault

Validate frontmatter and structure of notes in the Obsidian genealogy vault.

## Options

| Flag | Description |
|------|-------------|
| `--type person` | Validate only person notes |
| `--type source` | Validate only source notes |
| `--type place` | Validate only place notes |
| `--all` | Validate all note types |

## Instructions

1. **Load the `obsidian-genealogy` skill** for schema reference

2. **Scan the appropriate directory**:
   - Person notes: `~/Genealogy/Obsidian/People/`
   - Source notes: `~/Genealogy/Obsidian/Sources/`
   - Place notes: `~/Genealogy/Obsidian/Places/`

3. **For each note, validate**:

### Person Notes
- [ ] Has `type: person` in frontmatter
- [ ] Has `gramps_id` or `cr_id` (linked to data source)
- [ ] Filename matches convention: `Name (dates).md`
- [ ] Date formats are valid
- [ ] Wikilinks for family relationships are valid

### Source Notes
- [ ] Has `type: source` in frontmatter
- [ ] Has `source_type` field
- [ ] Has `citation` or EE-style reference
- [ ] Has `access_date` for digital sources

### Place Notes
- [ ] Has `type: place` in frontmatter
- [ ] Has `hierarchy` field (specific → general)
- [ ] Follows naming convention

4. **Check for common issues**:
   - Broken wikilinks (referenced notes don't exist)
   - Duplicate notes for same person
   - Missing required fields
   - Invalid date formats

## Output Format

```markdown
# Vault Validation Report

**Date:** [timestamp]
**Scope:** [type or "all"]
**Notes Scanned:** [count]

## Summary

| Type | Valid | Issues | Missing Fields |
|------|-------|--------|----------------|
| Person | [N] | [N] | [N] |
| Source | [N] | [N] | [N] |
| Place | [N] | [N] | [N] |

## Issues Found

### Critical (Must Fix)
- [ ] **[filename]**: [issue description]
- [ ] **[filename]**: [issue description]

### Warnings (Should Fix)
- [ ] **[filename]**: [issue description]

### Suggestions
- [optional improvement]

## Broken Links

| Note | Broken Link | Suggestion |
|------|-------------|------------|
| [note] | [[Missing Person]] | Create note or fix link |

## Duplicate Detection

| Person | Notes |
|--------|-------|
| [name] | [list of potential duplicate files] |
```

## Tips

- Run validation after bulk imports
- Fix critical issues before warnings
- Check broken links for typos vs. missing notes
- Consider creating missing linked notes
