# Futures Project — Primary Control Document

**Version:** 1.1  
**Last Updated:** 2026-08-02  
**Audience:** AI assistants and automated tooling working within the Futures Project repository

---

## Purpose

This document is the authoritative coordination and control layer for the entire Futures Project. It defines first-principles orientation, system design rules, phase discipline, and dependency constraints that govern all policy domains and subdomains.

This document does **not** propose policy, design programs, or prescribe messaging. Its role is to constrain, align, and sequence work so that ambition does not exceed execution capacity.

---

## First-Principles Orientation

The Futures Project is an institution-building effort operating under conditions of political, fiscal, and informational uncertainty. Policy is treated as system design rather than moral arbitration or ideological signaling.

**Core principles:**
- Institutional durability over rhetorical completeness
- Modularity and fault tolerance over elegance
- Separation of strategy, decision rules, and tactics
- Constraints (legal, fiscal, political) are binding
- Reversible, staged change preferred to brittle transformation

**Explicit non-assumptions:**
- No expectation of consensus
- No reliance on perfect actors or compliance
- No requirement that new technology succeed for core reforms to function

---

## Phase Model (Global)

All briefs, subdomains, and domains are assigned a phase. No artifact may claim a phase it has not met the gate conditions for. A brief cannot exceed the phase of its hard dependencies.

| Phase | Name | Gate Conditions |
|-------|------|-----------------|
| **0** | Problem Framing & Strategic Constraints | Problem correctly scoped; non-obvious constraints (legal, fiscal, political) documented |
| **1** | Structured Exploration | Options surveyed; analogues reviewed; mechanism alternatives compared |
| **2** | Architecture & Decision Rules | Core design decisions made; mechanism specified; internally consistent |
| **3** | Research Integration & Stress Testing | Existing literature reviewed; platform position stress-tested against it; divergences documented with rationale |
| **4** | Pilot Target & Day One Designation | EO-pilotable assessment completed; if EO-capable: pilot design specified (sites, timeline, metrics, personnel) and `eo-pilot-target: true` set in YAML; if legislation-required: minimum legislative vehicle and any available Day One administrative action identified; scaling pathway defined |
| **5** | Phasing & Implementation Design | Execution sequence, cost estimates, agency requirements, legislative vehicle defined |
| **6** | Publication-Ready Draft | Citations complete (Chicago footnotes); prose clean; audience-specific versions ready |
| **7** | Expert Review | External feedback gathered from domain practitioners |
| **8** | Revision & Incorporation | Feedback incorporated or explicitly rebutted with documented rationale |
| **9** | Public Messaging | Framing, rebuttal prep, earned media strategy |

**Phase 3 note**: Phase 3 requires documented engagement with peer-reviewed literature or research from institutions such as RAND, Brookings, Urban Institute, Niskanen Center, Grattan Institute, or CSBA. Ingested research is stored in `research-library/sources/`; review outputs go to `research-library/reviews/`.

**Phase 4 note**: Phase 4 is universal — every brief reaching Phase 4 must answer "What can be done on Day One without legislation?" EO-capable briefs produce a pilot specification with existing authority identified. Legislation-required briefs document the minimum vehicle and any administrative preparation actions available immediately. Briefs that are EO-pilotable should set `eo-pilot-target: true` and `day-one-action:` in YAML frontmatter.

---

## Layer Architecture

The repository is organized into four layers. Every brief carries a `layer:` field in its YAML frontmatter.

| Layer | Value | Directory | Role |
|-------|-------|-----------|------|
| Foundations | `1` | `guiding-principles/Foundations/` | Psychological and civilizational theory — why societies destabilize, what conditions reduce that risk |
| Operating-System | `2` | `guiding-principles/Operating-System/` | Execution instruments: Execution Corps, DoDA, PCA, RMC, congressional OS interface |
| Infrastructure | `3` | `guiding-principles/Infrastructure/` | Technical backbone: SSI, UPI, cybersecurity, AI governance, information integrity |
| Policy Domains | `4` | `guiding-principles/Policy_Domains/` | 18 substantive policy domains |

Layer 1 provides the theoretical grounding. Each subsequent layer enables the next. Most reform platforms operate only at Layer 4; this one builds the layers underneath first.

---

## Dependency & Fault-Tolerance Rules

- Domains are logically independent — failure in one must not cascade into others
- Cross-domain links must be explicit (via the `dependencies:` YAML field, using slugs)
- Dependency types:
  - **Hard** — blocking; the dependent brief cannot advance in phase without the dependency; requires a fallback design to be documented
  - **Soft** — coordination needed but not blocking
  - **Optional integration** — beneficial but not required

---

## Audience Tagging

All Phase 2+ briefs carry an `audiences:` YAML field. Two-axis taxonomy:

**Domestic constituencies** (11): `working-class`, `black-community`, `latino-community`, `rural-america`, `young-workers`, `seniors`, `veterans`, `small-business`, `women`, `immigrants`, `native-communities`

**Ideological** (4): `conservative-crossover`, `progressive-base`, `economic-populist`, `fiscal-hawk`

**International** (5): `allied-democracies`, `indo-pacific`, `gulf-partners`, `global-south`, `multilateral-institutions`

Only tag audiences where the brief has a genuine argument. A brief tagged both `conservative-crossover` and `progressive-base` signals genuine crossover potential.

---

## Messaging Separation Rule

Messaging (Phase 8) is downstream of design (Phases 0–4).

Design changes only through formal phase rollback — you cannot change the mechanism to suit the messaging. If the messaging is failing, the problem is either that the design has a genuine flaw (fix the design, re-enter the phase gate) or that the communication approach needs work (Phase 8 work).

---

## Citation Standard

Phase 5+ briefs use Chicago Notes-Bibliography footnotes in markdown:

```markdown
The payroll cap has not been raised since 1983.[^1]

[^1]: Robert J. Myers, *Social Security*, 4th ed. (Philadelphia: Pension Research Council, 1993), 212.
```

No separate bibliography file is needed. Generating properly formatted Chicago footnotes from a reference list is a trivial LLM task.

---

## Key Files

| File | Purpose |
|------|---------|
| `AI_Integrations/YAML_FRONTMATTER_GUIDE.md` | Authoritative reference for all YAML fields, phase gates, layer values, audience taxonomy |
| `AI_Integrations/AUTOMATION_README.md` | Script usage: PDF export, maturity scanning, Phase 3 research ingestion workflow |
| `AI_Integrations/MATURITY_TRACKER_TEMPLATE.md` | Template for domain-level `_MATURITY_TRACKER.md` files |
| `PROJECT_STATUS.md` | Full domain matrix, subdomain detail, gap analysis, recent activity |
| `research-library/index.md` | Source catalog for Phase 3 research integration |

---

## Governance of Change

Changes to this document are rare, versioned, and must explicitly surface tradeoffs. Phase model changes require updating: this document, `YAML_FRONTMATTER_GUIDE.md`, `MATURITY_TRACKER_TEMPLATE.md`, `AUTOMATION_README.md`, and all `_MATURITY_TRACKER.md` files across domains.
