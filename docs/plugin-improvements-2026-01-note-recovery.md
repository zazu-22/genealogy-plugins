# Plugin Improvements: Learnings from Note-Source Recovery Project

**Date:** 2026-01-02
**Project:** Note-Source Recovery (2026-01-note-source-recovery)
**Context:** While recovering source references from GEDCOM notes that were lost during Gramps import, several gaps in plugin documentation and functionality were identified.

---

## Executive Summary

The plugins are generally helpful but have gaps in three areas:
1. **Critical Gramps limitations** not prominently documented
2. **Cross-system workflows** (Gramps↔Obsidian) not covered
3. **Mapping between methodologies** (Mills → Gramps confidence) missing

---

## 1. Gramps Plugin (gramps-tools)

### Issue 1.1: Note-Citation Limitation Not Documented

**Problem:** The most significant limitation discovered is that **Gramps notes cannot have citations**. This is a structural limitation in the Gramps DTD (`note = text, style*, tagref*`). Users migrating from GEDCOM lose all note→source references.

**Impact:** Users waste time trying to attach citations to notes, or don't realize data was lost during import.

**Recommendation:** Add prominent warning to `gramps` skill and `lib/data-model.md`:

```markdown
## Critical Limitation: Notes Cannot Have Citations

Gramps notes are defined as `(text, style*, tagref*)` in the DTD - there is no
`citationref` element allowed. This means:

- GEDCOM notes with source references (2 SOUR @Sxx@) lose those links on import
- You cannot formally cite sources from notes in Gramps
- Research analysis must use alternative approaches (see below)

### Workarounds for Research Notes

1. **Cite sources on relevant events** - If a note analyzes birth year evidence,
   cite those sources on the Birth event instead
2. **Move analysis to Obsidian** - Use Obsidian for proof arguments with proper
   footnotes
3. **Inline text references** - Add source IDs as text within the note
   (e.g., "per 1900 Census [S0003]")
```

### Issue 1.2: API Update Pattern Not Clear

**Problem:** The web-api.md documentation doesn't explain that PUT requires the full object, not just changed fields. Trial and error was needed to discover this.

**Recommendation:** Add to `lib/web-api.md`:

```markdown
## Update Patterns

### Full Object Required for PUT
The Gramps Web API requires the **full object** for PUT updates, not partial updates.

**Correct pattern:**
```python
# 1. Get full object
event = GET /api/events/{handle}

# 2. Modify the field you need
event['citation_list'].append(new_citation_handle)

# 3. Send full object back
PUT /api/events/{handle} with event
```

**This will NOT work:**
```python
# Partial update - FAILS
PUT /api/events/{handle} with {"citation_list": [...]}
# Error: "Unknown classes: Event, citation_list"
```
```

### Issue 1.3: Citation→Event Linking Example Missing

**Problem:** No concrete example of creating a citation and linking it to an event.

**Recommendation:** Add to `lib/web-api.md`:

```markdown
## Creating and Linking Citations

### Complete Example: Add Citation to Existing Event

```python
import json, urllib.request

# Assume token and headers already set up

# 1. Create citation
citation_data = {
    "_class": "Citation",
    "source_handle": "abc123...",  # Source handle
    "page": "Page 5, Line 23",
    "confidence": 2  # 0-4 scale
}
req = urllib.request.Request(
    f"{BASE_URL}/api/citations/",
    data=json.dumps(citation_data).encode(),
    headers=headers,
    method='POST'
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
# Response is a list with transaction info
citation_handle = result[0]['handle']

# 2. Get the event to update
req = urllib.request.Request(f"{BASE_URL}/api/events/{event_handle}", headers=headers)
event = json.loads(urllib.request.urlopen(req).read())

# 3. Add citation to event's citation_list
event['citation_list'].append(citation_handle)

# 4. Update event with full object
req = urllib.request.Request(
    f"{BASE_URL}/api/events/{event_handle}",
    data=json.dumps(event).encode(),
    headers=headers,
    method='PUT'
)
urllib.request.urlopen(req)
```
```

---

## 2. Source Analysis Plugin (evidence-analysis)

### Issue 2.1: No Mapping to Gramps Confidence Levels

**Problem:** The source-analysis skill explains Mills' classification (original/derivative, primary/secondary, direct/indirect) but doesn't map these to Gramps' citation confidence levels (0-4).

**Recommendation:** Add to `lib/evaluation-checklist.md` or create new `lib/gramps-confidence-mapping.md`:

```markdown
## Mapping Evidence Quality to Gramps Confidence

Gramps uses a 0-4 confidence scale for citations. Here's how to map Mills'
evidence classification to Gramps confidence:

| Evidence Type | Mills Classification | Gramps Confidence | Example |
|---------------|---------------------|-------------------|---------|
| Direct + Primary + Original | Best possible | 4 (Very High) | Birth certificate signed by attending physician |
| Direct + Primary + Derivative | Strong | 3 (High) | Certified copy of birth certificate |
| Direct + Secondary | Good | 2-3 (Normal/High) | Death certificate stating birth date |
| Indirect + Primary | Moderate | 2 (Normal) | Census record (age → birth year) |
| Indirect + Secondary | Weaker | 1-2 (Low/Normal) | Newspaper article stating age |
| Circumstantial | Requires corroboration | 1 (Low) | Absence from tax list |

### Decision Framework

Ask these questions:
1. Does the source **directly state** the fact? (Direct vs Indirect)
2. Was the informant **present at the event**? (Primary vs Secondary)
3. Is this the **original record** or a copy? (Original vs Derivative)

More "yes" answers = higher confidence.
```

---

## 3. Obsidian Genealogy Plugin (obsidian-genealogy)

### Issue 3.1: No Research Note Schema

**Problem:** The frontmatter-schema.md covers Person, Source, Place, and Event notes but not Research/Proof Argument notes. We had to invent a schema during the project.

**Recommendation:** Add to `lib/frontmatter-schema.md`:

```markdown
## Research Note Schema

For proof arguments, evidence analysis, and research conclusions.

```yaml
---
type: research
research_id: "R-2026-001"           # Unique ID (R-YEAR-SEQUENCE)
subject_gramps_id: "I0083"          # Primary person being researched
subject_name: "John William Barry"
topic: "Birth Year Analysis"        # What question does this answer?
conclusion: "1862 based on preponderance of evidence"
status: complete | in_progress | abandoned
sources_cited:                      # Gramps source IDs used
  - S0003
  - S0028
  - S0029
created: 2026-01-02
last_updated: 2026-01-02
---
```

### Research Note Body Structure

```markdown
# [Topic]: [Subject Name]

## Research Question
[Clear statement of what you're trying to determine]

## Evidence Summary
[Table or list of sources with what each says]

## Analysis
[Evaluation of evidence quality, conflicts, resolution]

## Conclusion
[Final determination with reasoning]

---
## Notes
[Footnotes with full citations]

## Gramps Data
- Person: [gramps_id]
- Relevant Event: [event_id]
- Gramps Note: [note_id] (if any)
```

### Research ID Scheme

Use `R-YYYY-NNN` format:
- `R` = Research document type
- `YYYY` = Year created
- `NNN` = Sequential number (001, 002, etc.)

This enables:
- Easy cross-referencing from Gramps notes
- Unique identification across the vault
- Chronological organization
```

### Issue 3.2: Gramps↔Obsidian Workflow Not Documented

**Problem:** The Canvas Roots documentation explains import but doesn't describe the recommended workflow for research analysis that spans both systems.

**Recommendation:** Add to `lib/canvas-roots.md` or create new `lib/research-workflow.md`:

```markdown
## Research Workflow: Gramps + Obsidian

### When to Use Each System

| Data Type | System | Reason |
|-----------|--------|--------|
| Vital dates, relationships | Gramps | Structured data, exports |
| Source records | Gramps | Formal citations, sharing |
| Events with citations | Gramps | Linked to people/families |
| Research narratives | Obsidian | Narrative flexibility, footnotes |
| Proof arguments | Obsidian | Complex analysis, GPS compliance |
| Evidence evaluation | Obsidian | Weighing conflicting sources |

### Recommended Workflow for Research Analysis

1. **Record sources in Gramps** - Create source records with full metadata
2. **Cite sources on events** - Link citations to Birth, Death, etc.
3. **Write analysis in Obsidian** - Create research note with R-YYYY-NNN ID
4. **Reference from Gramps** - Update Gramps note to point to Obsidian

### Example: Birth Year Analysis

**In Gramps:**
- Birth event has citations from 6 census records, 2 newspapers
- Person note says: "Birth year analysis complete. Conclusion: 1862.
  See Obsidian: Research/Birth Year Analysis - John Barry (R-2026-001).md"

**In Obsidian:**
- Full analysis with evidence table
- Discussion of conflicting sources
- Conclusion with reasoning
- Proper footnotes

### What Canvas Roots Does NOT Sync

- Note content from Gramps
- Citations attached to events
- Custom attributes

These must be managed manually or via API scripts.
```

---

## 4. GPS Plugin (genealogical-proof-standard)

### Issue 4.1: No Implementation Guide

**Problem:** The GPS skill explains the five elements but doesn't show how to implement proof arguments in Gramps+Obsidian.

**Recommendation:** Add implementation section:

```markdown
## Implementing GPS in Gramps + Obsidian

### Element 1: Reasonably Exhaustive Search
- Document in Obsidian research note under "Sources Consulted"
- List sources searched, even if nothing found

### Element 2: Complete, Accurate Citations
- Create source records in Gramps
- Use Evidence Explained format in source metadata
- Cite on relevant events in Gramps

### Element 3: Analysis and Correlation
- Write analysis in Obsidian research note
- Create evidence table comparing sources
- Use Mills' classification for each source

### Element 4: Conflicting Evidence Resolution
- Document conflicts in Obsidian
- Explain why you accepted/rejected each source
- Use confidence levels on Gramps citations

### Element 5: Soundly Reasoned Conclusion
- State conclusion clearly in Obsidian
- Update Gramps data to reflect conclusion
- Reference Obsidian research note from Gramps
```

---

## 5. General: Cross-Plugin Integration

### Issue 5.1: No Cross-Reference Between Skills

**Problem:** The skills operate in isolation. Users don't know when to use which skill together.

**Recommendation:** Add a "Related Workflows" section to each skill showing common combinations:

```markdown
## Common Skill Combinations

| Task | Primary Skill | Supporting Skills |
|------|--------------|-------------------|
| Evaluate a new source | source-analysis | evidence-explained (citation) |
| Build proof argument | genealogical-proof-standard | source-analysis, obsidian |
| Import GEDCOM data | gramps | obsidian (Canvas Roots) |
| Create research note | obsidian | gps, source-analysis |
| Cite sources properly | evidence-explained | gramps (API) |
```

---

## Implementation Priority

| Priority | Change | Plugin | Effort |
|----------|--------|--------|--------|
| **High** | Document note-citation limitation | gramps | Low |
| **High** | Add research note schema | obsidian | Low |
| **High** | Add confidence mapping | source-analysis | Low |
| **Medium** | Add API update patterns | gramps | Medium |
| **Medium** | Add Gramps↔Obsidian workflow | obsidian | Medium |
| **Medium** | Add GPS implementation guide | gps | Medium |
| **Low** | Add cross-plugin integration | all | Low |

---

## Files to Modify

### gramps-tools plugin
- `skills/gramps/README.md` - Add prominent warning about note limitations
- `skills/gramps/lib/data-model.md` - Add Note limitation section
- `skills/gramps/lib/web-api.md` - Add update patterns and citation example

### evidence-analysis plugin
- `skills/source-analysis/lib/evaluation-checklist.md` - Add Gramps confidence mapping

### obsidian-genealogy plugin
- `skills/obsidian-genealogy/lib/frontmatter-schema.md` - Add Research Note schema
- `skills/obsidian-genealogy/lib/canvas-roots.md` - Add Gramps↔Obsidian workflow

### research-workflow plugin
- `skills/research-planning/README.md` - Add GPS implementation section

---

## Source References

- Gramps DTD: https://github.com/gramps-project/gramps/blob/master/gramps/plugins/lib/grampsxml.dtd
- Gramps Web API: https://gramps-project.github.io/gramps-web-api/
- Gramps Discourse - Obsidian: https://gramps.discourse.group/t/genealogy-research-in-obsidian-for-those-who-want-to-try/8926
- GEPS 018: https://www.gramps-project.org/wiki/index.php/GEPS_018:_Evidence_style_sources

---

## IMPLEMENTATION INSTRUCTIONS FOR AGENT

**IMPORTANT:** When implementing the changes described in this document, you MUST complete ALL items in the implementation plan. After completing implementation, you are REQUIRED to fill out the validation checklist below with explicit YES/NO responses for each item.

### Implementation Tasks

Work through each section above and implement the recommended changes. Use the markdown snippets provided as starting points, adapting them to fit the existing structure of each file.

### MANDATORY COMPLETION VALIDATION

After implementation is complete, copy this checklist and provide an explicit YES or NO for each item. Do not use partial responses or qualifications - each item must be definitively YES or NO.

```
IMPLEMENTATION VALIDATION CHECKLIST
===================================

GRAMPS-TOOLS PLUGIN:

1. Note-citation limitation warning added to skills/gramps/README.md?
   [ ] YES / NO

2. Note limitation section added to skills/gramps/lib/data-model.md with:
   - DTD explanation (note = text, style*, tagref*)
   - Impact on GEDCOM import
   - Three workaround options documented
   [ ] YES / NO

3. API update pattern section added to skills/gramps/lib/web-api.md with:
   - Full object requirement explained
   - Correct pattern example
   - Common error example
   [ ] YES / NO

4. Citation creation and linking example added to skills/gramps/lib/web-api.md with:
   - Complete Python code example
   - Create citation step
   - Link to event step
   [ ] YES / NO

EVIDENCE-ANALYSIS PLUGIN:

5. Gramps confidence mapping table added to skills/source-analysis with:
   - Mills classification → Gramps confidence (0-4)
   - At least 6 evidence type rows
   - Decision framework questions
   [ ] YES / NO

OBSIDIAN-GENEALOGY PLUGIN:

6. Research note schema added to skills/obsidian-genealogy/lib/frontmatter-schema.md with:
   - YAML frontmatter template
   - research_id field (R-YYYY-NNN format)
   - subject_gramps_id, topic, conclusion fields
   [ ] YES / NO

7. Research note body structure documented with:
   - Section headings template
   - Research Question section
   - Evidence Summary section
   - Analysis and Conclusion sections
   [ ] YES / NO

8. Gramps↔Obsidian workflow added to skills/obsidian-genealogy with:
   - "When to use each system" table
   - Recommended workflow steps
   - What Canvas Roots does NOT sync
   [ ] YES / NO

RESEARCH-WORKFLOW PLUGIN:

9. GPS implementation guide added with:
   - How to implement each of 5 GPS elements
   - Gramps vs Obsidian responsibilities for each
   [ ] YES / NO

CROSS-PLUGIN:

10. Related skills/workflows section added to at least 2 plugins?
    [ ] YES / NO

===================================
SUMMARY:
- Items completed: ___/10
- Items not completed: ___/10

If any items are NO, explain why and what alternative was implemented:

_______________________________________________
_______________________________________________
_______________________________________________
```

### Validation Rules

1. **Do not mark YES unless the change is fully implemented** - partial implementations are NO
2. **If you deviate from the recommendation**, explain the alternative in the summary
3. **All 10 items should be YES** for complete implementation
4. **If an item cannot be implemented**, document the blocker and notify the user

### After Validation

Once the checklist is complete:
1. Commit all changes with message: "Implement plugin improvements from note-source-recovery learnings"
2. Report the completed checklist to the user
3. If any items are NO, discuss next steps
