# YAML Frontmatter Standard

Every policy brief in `guiding-principles/` requires YAML frontmatter. This guide is the authoritative reference for all field definitions and valid values.

---

## Full Template

```yaml
---
id: kebab-case-unique-identifier
title: "Full Title of the Brief"
sidebar_label: Short Label
sidebar_position: 1
slug: /layer-folder/brief-slug
domain: Domain_Name
subdomain: Subdomain_Name
policy_type: Policy Framework
status: Draft
phase: 2
layer: 4
version: 0.1
last_updated: 2026-01-01
tags:
  - subject-tag
  - another-tag
audiences:
  - working-class
  - economic-populist
dependencies:
  - brief-slug-one
  - brief-slug-two
description: >
  One or two sentence summary of what this brief proposes and why it matters.
---
```

---

## Field Definitions

### `id` (required)
Unique identifier in kebab-case. Must be unique across the entire corpus — used by Docusaurus for internal linking.

```yaml
id: superannuation-employer-contribution-portability
```

### `title` (required)
Full human-readable title. Used as the document heading and in PDF export.

### `sidebar_label` (optional)
Shorter label for Docusaurus sidebar navigation. Use when the full title is too long.

### `slug` (required)
URL path for Docusaurus. Format: `/layer-folder/brief-name`

| Layer | Prefix |
|-------|--------|
| Foundations (L1) | `/foundations/` |
| Operating-System (L2) | `/operating-system/` |
| Infrastructure (L3) | `/infrastructure/` |
| Policy Domains (L4) | `/domain-name/` |

### `domain` (required)
Top-level domain. Must match the directory name.

**Valid domains:**
- `Foundations` — Layer 1
- `Operating-System` — Layer 2
- `Infrastructure` — Layer 3
- `Healthcare`, `Budget_and_Fiscal_Policy`, `Democratic_Integrity`, `Manufacturing`, `Housing_and_Public_Infrastructure`, `Immigration`, `Labor_and_Economic_Security`, `Agriculture`, `National_Security`, `Trade_Policy`, `Climate_Risk`, `Education`, `Social`, `Energy`, `Sports_and_Cultural_Institutions`, `United-Nations-and-Global-Institutional-Reform` — Layer 4

### `subdomain` (optional)
Specific area within the domain. Used for grouping in maturity trackers and Docusaurus sidebar.

### `phase` (required)
Current development phase. Be conservative — don't claim a phase until requirements are met.

| Phase | Name | Gate condition |
|-------|------|----------------|
| **0** | Problem Framing & Strategic Constraints | Problem correctly scoped, non-obvious constraints documented |
| **1** | Structured Exploration | Options surveyed, analogues reviewed, mechanism alternatives compared |
| **2** | Architecture & Decision Rules | Core design decisions made, mechanism specified, internally consistent |
| **3** | Research Integration & Stress Testing | Existing literature reviewed, platform stress-tested against it, divergences documented with rationale |
| **4** | Pilot Target & Day One Designation | EO-pilotable assessment completed; if EO-capable: pilot design specified and `eo-pilot-target: true` set; if not: minimum legislative vehicle and Day One administrative actions identified |
| **5** | Phasing & Implementation Design | Execution sequence, cost estimates, agency requirements, legislative vehicle |
| **6** | Publication-Ready Draft | Citations complete, prose clean, audience-specific versions ready |
| **7** | Expert Review | External feedback gathered |
| **8** | Revision & Incorporation | Feedback incorporated or explicitly rebutted |
| **9** | Public Messaging | Framing, rebuttal prep, earned media strategy |

**Rules:**
- A brief cannot exceed the phase of its hard dependencies
- Phase 3 requires documented engagement with RAND, Brookings, Urban Institute, or equivalent research
- Phase 4 requires an EO-pilotable assessment for every brief reaching Phase 4 — not only EO-capable ones
- Phase 6+ requires Chicago-style citations via markdown footnotes (`[^1]`)

### `layer` (required)
Architectural layer. Set automatically based on directory location — verify it matches.

| Value | Layer | Directory |
|-------|-------|-----------|
| `1` | Psychological Foundations | `Foundations/` or domain `foundations/` subfolder |
| `2` | Operating System | `Operating-System/` |
| `3` | Infrastructure | `Infrastructure/` |
| `4` | Policy Domains | `Policy_Domains/` |

### `status` (required)
- `Draft` — initial or rough
- `In Progress` — actively being developed
- `Review` — complete enough for feedback
- `Complete` — finished for current phase

### `version` (required)
Semantic version. Increment minor (0.x) for content updates, major (x.0) for full rewrites.

### `audiences` (required for Phase 2+)
Cross-cutting political and constituency audiences. Used by campaigns to pull all briefs relevant to a specific room or stakeholder group. List only audiences where this brief has a genuine argument — do not tag aspirationally.

**Domestic constituencies:**
| Tag | Briefing context |
|-----|-----------------|
| `working-class` | Union halls, manufacturing towns, wage/benefits conversations |
| `black-community` | NAACP, Urban League, CBC, Black church networks |
| `latino-community` | UnidosUS, LULAC, agricultural worker events |
| `rural-america` | Farm Bureau, rural hospitals, broadband, ag committees |
| `young-workers` | College campuses, first-job voters, superannuation/401k stakes |
| `seniors` | AARP, Social Security solvency, long-term care |
| `veterans` | VFW, DAV, procurement reform |
| `small-business` | Chamber events, right to repair, regulatory burden |
| `women` | Maternal health, pay equity, childcare, caregiver policy |
| `immigrants` | Legal pathway, labor contribution, enforcement reform |
| `native-communities` | Tribal sovereignty, land and water rights, treaty |

**Ideological audiences:**
| Tag | Who it targets |
|-----|---------------|
| `conservative-crossover` | Right-leaning independents — market design, individual ownership, fiscal discipline |
| `progressive-base` | Left base activation — inequality, universal coverage, criminal justice |
| `economic-populist` | Cross-ideological working class — anti-monopoly, anti-Wall Street, trade fairness |
| `fiscal-hawk` | Deficit hawks, independent voters, moderate Democrats — fiscal seriousness |

**International audiences:**
| Tag | Who it targets |
|-----|---------------|
| `allied-democracies` | NATO, G7, Five Eyes, democratic defense partners |
| `indo-pacific` | Japan, South Korea, Australia, Taiwan, ASEAN partners |
| `gulf-partners` | Gulf states, GDIC participants, Middle East regional partners |
| `global-south` | African Union, ASEAN developing states, Latin America, non-aligned |
| `multilateral-institutions` | UN, IMF, WTO, WHO reform constituencies |

**Dual-tagging signal:** A brief tagged both `conservative-crossover` and `progressive-base` has genuine crossover potential — it can lead in almost any room.

### `tags` (optional)
Subject-matter tags for search and filtering. Lowercase kebab-case. These describe what the brief is about, not who it's for.

```yaml
tags:
  - superannuation
  - retirement
  - payroll
  - capital-formation
```

### `dependencies` (optional but recommended)
Slugs of briefs this one depends on. Used for dependency mapping and phase validation.

```yaml
dependencies:
  - ssi-self-sovereign-identity-framework
  - upi-privacy-preserving-payment-rail
  - department-of-data-and-accountability
```

**Dependency types** (if you need to distinguish):
- Hard — blocking; this brief cannot advance without the dependency
- Soft — coordination needed but not blocking

### `eo-pilot-target` (required for Phase 4+)
Boolean. Whether this brief has a Day One executive-action-pilotable implementation that does not require Congressional legislation or new appropriations.

```yaml
eo-pilot-target: true   # EO-capable: pilot design is specified in the brief
eo-pilot-target: false  # Legislation-required: Day One admin actions documented instead
```

Set in Phase 4. If `true`, the brief must include a pilot design section specifying sites, personnel, timeline, metrics, and the existing executive authority being used.

### `day-one-action` (required for Phase 4+)
Short description (1–2 sentences) of what can be done on Day One — either the EO pilot specification or the administrative preparation action available without legislation.

```yaml
# EO-capable example:
day-one-action: "5-city Crime Reduction Council pilot via DoDA deployment authority and EC field deployment."

# Legislation-required example:
day-one-action: "Issue executive guidance directing HHS to prioritize coverage continuity; convene interagency working group on implementation design."
```

### `description` (required for Phase 2+)
One to two sentences summarizing what the brief proposes and why it matters. Appears as the shaded abstract block in PDF export and as the Docusaurus card subtitle.

---

## Figures and Citations

### Figures
Store in an `assets/` subfolder next to the brief or at the domain level:

```
Policy_Domains/Healthcare/
  assets/
    sec-market-architecture.svg    ← reference as ./assets/name.svg
    revenue-model-interactive.html ← web-only (needs .png companion for PDF)
    revenue-model-interactive.png  ← PDF fallback
```

Reference in markdown:
```markdown
![Figure 1: SEC Market Architecture](./assets/sec-market-architecture.svg)
```

### Citations (Chicago Notes-Bibliography)
Use markdown footnotes. No separate bibliography file needed.

```markdown
The payroll cap has not been raised since 1983.[^1]

[^1]: Robert J. Myers, *Social Security*, 4th ed. (Philadelphia: Pension Research Council, 1993), 212.
```

Generating properly formatted Chicago footnotes from a reference list is a trivial LLM task — provide the references and ask for the formatted footnotes.

---

## PDF Export

```bash
# Single brief
python3 scripts/export-brief.py path/to/brief.md

# All Phase 5+ briefs in a domain (publication-track)
python3 scripts/export-domain.py Healthcare --phase 5

# All Phase 4+ briefs (pilot-designated and above)
python3 scripts/export-domain.py Healthcare --phase 4

# All domains
python3 scripts/export-domain.py --all --phase 2 -o exports/
```

See `AI_Integrations/AUTOMATION_README.md` for full export documentation.

---

## Minimal Valid Example

```yaml
---
id: care-delivery-market-design
title: "Care Delivery Market Design"
slug: /healthcare/care-delivery-market-design
domain: Healthcare
subdomain: Care_Delivery_and_Insurance
phase: 2
layer: 4
version: 0.3
status: Draft
last_updated: 2026-03-01
audiences:
  - working-class
  - conservative-crossover
  - progressive-base
description: >
  Designs a three-tier healthcare market separating routine care,
  severe event coverage, and emergency services by economic structure.
---
```
