---
name: genealogical-proof-standard
description: The Genealogical Proof Standard (GPS) five elements for establishing reliable conclusions. Use when evaluating research completeness, building proof arguments, resolving contradictions, or writing proof statements.
---

# Genealogical Proof Standard (GPS)

Expert knowledge for applying the Board for Certification of Genealogists' standard for establishing reliable genealogical conclusions.

## When This Skill Applies

- Evaluating whether research is complete enough for conclusions
- Building proof arguments for genealogical claims
- Resolving contradictory evidence
- Writing proof summaries and arguments
- Assessing the reliability of existing conclusions

## The Five Elements

Every sound genealogical conclusion must meet all five elements:

| # | Element | Key Question |
|---|---------|--------------|
| 1 | **Reasonably exhaustive research** | Have I searched all relevant sources? |
| 2 | **Complete, accurate citations** | Can others verify my sources? |
| 3 | **Thorough analysis and correlation** | Have I evaluated all evidence? |
| 4 | **Resolution of conflicts** | Have I explained contradictions? |
| 5 | **Sound, written conclusion** | Is my reasoning clear and logical? |

## Quick Assessment

### Is Your Research GPS-Compliant?

**Element 1 - Exhaustive Research**:
- [ ] Searched all record types likely to contain relevant information
- [ ] Checked multiple repositories
- [ ] Explored variant name spellings
- [ ] Documented negative searches

**Element 2 - Complete Citations**:
- [ ] Every fact has a source citation
- [ ] Citations identify repository/location
- [ ] Sufficient detail to relocate source
- [ ] Access information for digital sources

**Element 3 - Analysis and Correlation**:
- [ ] Classified each source (original/derivative)
- [ ] Assessed information quality (primary/secondary)
- [ ] Identified evidence type (direct/indirect/negative)
- [ ] Compared evidence across sources

**Element 4 - Conflict Resolution**:
- [ ] Identified all conflicting evidence
- [ ] Explained likely cause of each conflict
- [ ] Justified which evidence is more reliable
- [ ] Acknowledged unresolvable conflicts

**Element 5 - Written Conclusion**:
- [ ] Clearly states the conclusion
- [ ] Explains reasoning step by step
- [ ] Addresses all evidence (supporting and conflicting)
- [ ] Written coherently for others to evaluate

## When You Have Proof

You have **proof** (not just evidence) when:
- All five GPS elements are satisfied
- The conclusion is supported by the preponderance of evidence
- No reasonable alternative explanation remains
- The reasoning would convince a skeptical peer

## Implementing GPS in Gramps + Obsidian

Each GPS element has a natural home in either Gramps or Obsidian:

### Element 1: Reasonably Exhaustive Search

| Task | System | Details |
|------|--------|---------|
| Document sources searched | Obsidian | Research note "Sources Consulted" section |
| Record negative searches | Obsidian | List sources searched with no results |
| Track repositories checked | Obsidian | Include physical and online repositories |

**In Obsidian research note:**
```markdown
## Sources Consulted
- [x] 1870-1920 U.S. Census (all found)
- [x] Ohio vital records (birth not found - records start 1908)
- [x] Muskingum County probate (estate file found)
- [ ] Church records (not yet searched)
```

### Element 2: Complete, Accurate Citations

| Task | System | Details |
|------|--------|---------|
| Create source records | Gramps | Full metadata per Evidence Explained |
| Attach citations to events | Gramps | Link via API or UI |
| Format footnotes | Obsidian | Full EE format in research notes |

**In Gramps:** Source → Citation → Event linkage
**In Obsidian:** Full footnote format in Notes section

### Element 3: Analysis and Correlation

| Task | System | Details |
|------|--------|---------|
| Classify sources | Both | Use `source-analysis` skill |
| Create evidence table | Obsidian | Compare what each source says |
| Set confidence levels | Gramps | Citation confidence (0-4) |

**Evidence table in Obsidian:**
```markdown
| Source | Date | Birth Year | Classification | Confidence |
|--------|------|------------|----------------|------------|
| 1870 Census | 1870 | ~1862 | Primary/Indirect | Normal (2) |
```

### Element 4: Conflicting Evidence Resolution

| Task | System | Details |
|------|--------|---------|
| Identify conflicts | Obsidian | Evidence table reveals discrepancies |
| Explain conflicts | Obsidian | Analysis section of research note |
| Adjust confidence | Gramps | Lower confidence for unreliable sources |

**In Obsidian:**
```markdown
## Conflict Resolution
The 1880 census shows age 17 (b. ~1863), conflicting with other records.
This is likely informant error - the census was taken in June, possibly
before his birthday, and informants often rounded ages.
```

### Element 5: Soundly Reasoned Conclusion

| Task | System | Details |
|------|--------|---------|
| State conclusion | Obsidian | Conclusion section of research note |
| Update Gramps data | Gramps | Set dates/facts per conclusion |
| Link systems | Both | Gramps note → Obsidian research ID |

**In Gramps:**
- Update Birth event date to concluded year
- Add note: "Birth year determined via analysis. See Obsidian: R-2026-001"

**In Obsidian:**
```markdown
## Conclusion
John William Barry was born in 1862, based on preponderance of evidence.
```

### Quick Reference: Where Each Element Lives

| GPS Element | Primary System | Secondary System |
|-------------|----------------|------------------|
| 1. Exhaustive search | Obsidian (documentation) | Gramps (source records) |
| 2. Complete citations | Gramps (source→citation) | Obsidian (footnotes) |
| 3. Analysis/correlation | Obsidian (evidence table) | Gramps (confidence levels) |
| 4. Conflict resolution | Obsidian (analysis) | Gramps (confidence) |
| 5. Written conclusion | Obsidian (proof argument) | Gramps (data + note link) |

## Reference Materials

For detailed information, see:

| Topic | File | Keywords |
|-------|------|----------|
| Exhaustive Research | [lib/exhaustive-research.md](lib/exhaustive-research.md) | completeness, sources, negative |
| Citation Standards | [lib/complete-citations.md](lib/complete-citations.md) | documentation, verification |
| Evidence Correlation | [lib/evidence-correlation.md](lib/evidence-correlation.md) | analysis, comparison, weight |
| Conflict Resolution | [lib/contradiction-resolution.md](lib/contradiction-resolution.md) | discrepancies, conflicts, explanation |
| Proof Arguments | [lib/proof-arguments.md](lib/proof-arguments.md) | writing, reasoning, conclusions |

## Related Skills

- `source-analysis` - Classifying sources and evidence
- `evidence-explained` - Citation methodology
- `research-planning` - Planning exhaustive research
- `obsidian-genealogy` - Research note schemas and workflows
- `gramps` - Recording conclusions and linking to Obsidian
