# Domain Maturity Tracker: [DOMAIN_NAME]

**Last Updated:** [DATE]  
**Overall Domain Phase:** [0–9]  
**Domain Owner:** [OPTIONAL]

---

## Phase Model Reference

| Phase | Name | Gate Conditions |
|-------|------|-----------------|
| **0** | Problem Framing & Strategic Constraints | Problem correctly scoped; non-obvious constraints documented |
| **1** | Structured Exploration | Options surveyed; analogues reviewed; mechanism alternatives compared |
| **2** | Architecture & Decision Rules | Core design decisions made; mechanism specified; internally consistent |
| **3** | Research Integration & Stress Testing | Literature reviewed; platform stress-tested against it; divergences documented |
| **4** | Pilot Target & Day One Designation | EO-pilotable assessment completed; if EO-capable: pilot design specified and `eo-pilot-target: true` set; if legislation-required: minimum vehicle and Day One admin actions identified; scaling pathway defined |
| **5** | Phasing & Implementation Design | Execution sequence, cost estimates, agency requirements, legislative vehicle |
| **6** | Publication-Ready Draft | Citations complete (Chicago footnotes); prose clean; audience-specific versions ready |
| **7** | Expert Review | External feedback gathered |
| **8** | Revision & Incorporation | Feedback incorporated or explicitly rebutted |
| **9** | Public Messaging | Framing, rebuttal prep, earned media strategy |

A brief cannot exceed the phase of its hard dependencies.  
Phase 3 requires documented research engagement (RAND, Brookings, Niskanen, Urban Institute, or equivalent).  
Phase 4 requires an EO-pilotable assessment for every brief — not only EO-capable ones.  
Phase 6+ requires Chicago-style citations via markdown footnotes (`[^1]`).

---

## Domain Overview

**Layer:** [1 = Foundations / 2 = Operating-System / 3 = Infrastructure / 4 = Policy Domain]

**Purpose:**  
[Brief description of what this domain covers]

**Key Questions:**  
- [Question 1]
- [Question 2]
- [Question 3]

**Success Criteria:**  
- [Criteria 1]
- [Criteria 2]

---

## Subdomain Status Matrix

| Subdomain | Phase | Files | Est. Words | Key Gaps | Next Action |
|-----------|-------|-------|------------|----------|-------------|
| [Subdomain_Name] | 0 | 0 | 0 | Not started | Create initial file |

---

## Dependency Map

### Hard Dependencies (Blocking)
| This Domain Requires | From Domain | Current Phase | Risk |
|---------------------|-------------|---------------|------|
| [Resource/Policy] | [Domain] | [Phase] | [High/Med/Low] |

### Soft Dependencies (Coordination)
| This Domain Benefits From | From Domain | Notes |
|--------------------------|-------------|-------|
| [Resource/Policy] | [Domain] | [Context] |

### Provides To (Downstream Impact)
| Other Domain | What We Provide | Criticality |
|--------------|-----------------|-------------|
| [Domain] | [Resource/Policy] | [High/Med/Low] |

---

## Research Library

*Phase 3 work for this domain. See `research-library/sources/` and `research-library/reviews/`.*

| Source | Citation Key | Topics Covered | Review Status |
|--------|-------------|----------------|---------------|
| [Institution — Title] | [citation-key] | [topics] | [TBD / In Progress / Complete] |

---

## Gap Analysis

### Tier 1: Critical Gaps (Missing Foundation)
- [ ] **[Gap Name]** — [Why it matters] — Target: Phase [X]

### Tier 2: Structural Gaps (Incomplete Coverage)
- [ ] **[Gap Name]** — [Why it matters] — Target: Phase [X]

### Tier 3: Enhancement Gaps (Nice-to-Have)
- [ ] **[Gap Name]** — [Why it matters] — Target: Phase [X]

---

## Phase Advancement Checklist

### Phase 1 — Structured Exploration
- [ ] Problem statement defined for each subdomain
- [ ] Legal constraints identified
- [ ] Fiscal constraints identified
- [ ] Political feasibility mapped
- [ ] Stakeholder landscape documented

### Phase 2 — Architecture & Decision Rules
- [ ] Alternative approaches documented and compared
- [ ] Core mechanism selected with rationale
- [ ] Internal consistency verified (no contradictions between briefs)
- [ ] Dependencies declared and typed (hard/soft)

### Phase 3 — Research Integration & Stress Testing
- [ ] Key claims mapped to specific sources (page-level citations where possible)
- [ ] Sources ingested to `research-library/sources/`
- [ ] Review document produced in `research-library/reviews/`
- [ ] Aligned findings documented
- [ ] Gaps in literature documented
- [ ] Divergences documented with FP rationale
- [ ] Open questions flagged

### Phase 4 — Pilot Target & Day One Designation
- [ ] EO-pilotable assessment documented: "What can be done on Day One without Congressional legislation or appropriation?"
- [ ] If EO-capable (`eo-pilot-target: true`):
  - [ ] Pilot design specified: sites/cities, personnel requirements, technology stack, timeline, metrics
  - [ ] Existing executive authority identified (which EO authority, which agency power, which existing appropriation)
  - [ ] `eo-pilot-target: true` and `day-one-action:` set in YAML frontmatter
  - [ ] Scaling pathway from pilot to full implementation defined
  - [ ] Sunset or transition conditions specified (when does the pilot become the default?)
- [ ] If legislation-required (`eo-pilot-target: false`):
  - [ ] Minimum legislative vehicle documented (which authorization or appropriation required)
  - [ ] Day One administrative preparation actions identified (convening, guidance, staffing, prioritization within existing authority)
  - [ ] `day-one-action:` set in YAML with the available administrative step

### Phase 5 — Phasing & Implementation Design
- [ ] Implementation timeline created
- [ ] Agency requirements specified (existing vs. new institution)
- [ ] Legislative vehicle identified
- [ ] Cost estimates developed
- [ ] Fallback plans documented

### Phase 6 — Publication-Ready Draft
- [ ] Chicago footnote citations added to all specific claims
- [ ] Prose clean and readable for target audiences
- [ ] Audience-specific framing notes added
- [ ] Description field in YAML finalized

### Phase 7 — Expert Review
- [ ] Domain practitioners identified for review
- [ ] Review materials sent
- [ ] Feedback documented

### Phase 8 — Revision & Incorporation
- [ ] Feedback incorporated or explicitly rebutted with rationale
- [ ] Version incremented

### Phase 9 — Public Messaging
- [ ] Key messages drafted
- [ ] Anticipated objections and rebuttals documented
- [ ] Communication strategy finalized

---

## Recent Activity Log

| Date | Subdomain | Change | Phase Impact |
|------|-----------|--------|--------------|
| [YYYY-MM-DD] | [Name] | [Description] | [Phase change or N/A] |

---

## Blockers & Issues

### Active Blockers
1. **[Blocker Name]** — [Description] — Blocking: [Subdomain] — ETA: [Date]

### Resolved Issues
- ~~[Issue]~~ — Resolved: [Date] — Solution: [Brief description]

---

## Notes & Context

[Any additional context, decisions, or rationale that doesn't fit above]
