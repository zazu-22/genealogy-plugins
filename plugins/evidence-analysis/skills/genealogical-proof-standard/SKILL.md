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

## Implementing GPS in Practice

Each GPS element has a natural home across the research infrastructure:

### Element 1: Reasonably Exhaustive Search

| Task | System | Details |
|------|--------|---------|
| Document sources searched | Research files | `log.md` search documentation |
| Record negative searches | Research files | List sources searched with no results |
| Track repositories checked | Database | `sources` table with status tracking |

### Element 2: Complete, Accurate Citations

| Task | System | Details |
|------|--------|---------|
| Create source records | Gramps | Full metadata per Evidence Explained |
| Register sources | Database | `INSERT INTO sources` via `just register` |
| Attach citations to events | Gramps | Link via API or UI |
| Format footnotes | Research files | Full EE format in evidence.md |

### Element 3: Analysis and Correlation

| Task | System | Details |
|------|--------|---------|
| Classify sources | Database | `evidence_classifications` table |
| Create evidence table | Research files | evidence.md per-source sections |
| Set confidence levels | Gramps | Citation confidence (0-4) |

### Element 4: Conflicting Evidence Resolution

| Task | System | Details |
|------|--------|---------|
| Identify conflicts | Research files | Evidence table reveals discrepancies |
| Explain conflicts | Research files | Analysis section of evidence.md |
| Adjust confidence | Gramps | Lower confidence for unreliable sources |

### Element 5: Soundly Reasoned Conclusion

| Task | System | Details |
|------|--------|---------|
| State conclusion | Research files | Proof argument in `proof-arguments/` |
| Update Gramps data | Gramps | Set dates/facts per conclusion |

### Quick Reference: Where Each Element Lives

| GPS Element | Primary System | Secondary System |
|-------------|----------------|------------------|
| 1. Exhaustive search | Research files (log.md) | Database (source inventory) |
| 2. Complete citations | Gramps (source/citation) | Database (source register) |
| 3. Analysis/correlation | Database (classifications) | Research files (evidence.md) |
| 4. Conflict resolution | Research files (analysis) | Gramps (confidence) |
| 5. Written conclusion | Research files (proof argument) | Gramps (data + note link) |

## Reference Materials

For detailed information, see:

| Topic | File | Keywords |
|-------|------|----------|
| Exhaustive Research | [lib/exhaustive-research.md](lib/exhaustive-research.md) | completeness, sources, negative |
| Evidence Correlation | [lib/evidence-correlation.md](lib/evidence-correlation.md) | analysis, comparison, weight |
| Conflict Resolution | [lib/contradiction-resolution.md](lib/contradiction-resolution.md) | discrepancies, conflicts, explanation |
| Proof Arguments | [lib/proof-arguments.md](lib/proof-arguments.md) | writing, reasoning, conclusions |

## Related Skills

- `source-analysis` - Classifying sources and evidence
- `evidence-explained` - Citation methodology
- `research-planning` - Planning exhaustive research
- `gramps` - Recording conclusions in Gramps
