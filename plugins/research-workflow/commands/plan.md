---
description: Create a research plan for a genealogical question
allowed-tools: [Read, Write, Grep, Glob, WebSearch]
argument-hint: "<research-question>"
---

# Create Research Plan

Create a structured research plan for a specific genealogical question.

## Instructions

1. Analyze the research question to understand:
   - What fact or relationship needs to be established
   - What is already known
   - What sources might provide evidence

2. Load the `research-planning` skill for methodology guidance

3. Create a research plan following the structure:

```markdown
# Research Plan: [Question]

**Created:** [date]
**Researcher:** [user]
**Status:** Draft

## Research Question
[Clear statement of what needs to be determined]

## Known Facts
- [Fact 1 with source]
- [Fact 2 with source]
- [What we're building from]

## Hypothesis
[Proposed answer to test]

## Research Strategy

### Phase 1: [Category]
**Objective:** [What we hope to find]

| Source Type | Repository | Priority |
|-------------|------------|----------|
| [Source 1] | [Where] | High/Med/Low |
| [Source 2] | [Where] | High/Med/Low |

### Phase 2: [Category]
[Continue as needed]

## Success Criteria
- [ ] [What would prove the hypothesis]
- [ ] [What would disprove it]
- [ ] [Minimum acceptable evidence]

## Potential Obstacles
- [Obstacle 1]: [Mitigation strategy]
- [Obstacle 2]: [Mitigation strategy]
```

4. Consider sources based on:
   - Time period of research question
   - Geographic location
   - Record survival rates
   - Availability (online vs. on-site)

## Output

Save the plan to the current directory as `research-plan-[topic].md` or present for review.

## Tips

- Start with most accessible sources
- Plan for both proving AND disproving the hypothesis
- Consider FAN club (Friends, Associates, Neighbors)
- Include DNA evidence if relationship question
