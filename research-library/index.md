# Research Library Index

Sources ingested for Phase 3 research integration. This excerpt includes one complete source-to-review chain. Additional catalog entries are retained below to show the breadth of the larger research queue, but their source files and reviews are not part of this public sample.

---

## How to use this library

1. **Ingest a source:** `python3 scripts/ingest-research.py research-library/incoming/report.pdf`
2. **Link briefs:** Add relevant brief slugs to the `briefs:` field in the source frontmatter
3. **Run a review:** Provide Claude with source `.md` + brief(s); follow `reviews/_REVIEW_TEMPLATE.md`, including page references on every cited claim and a completed Citation Verification table; save to `reviews/<topic>-research-review.md`
4. **Grade the review:** Provide a different-provider LLM the review, the RAG-processed source, and the brief(s); follow `reviews/validation/_GRADING_TEMPLATE.md` to grade the review's *fidelity* to that material (not the brief's or literature's quality — that's the review's own job); save to `reviews/validation/<topic>-research-review-grading.md`
5. **Cite inline:** Add footnotes to the brief for specific claims (page-level, Chicago format)
6. **Update index:** Mark `phase-3-review:` in source frontmatter once a review exists

---

## Included Demonstration Source

<!-- Sources added here by ingest-research.py -->
- [17a-reducing-violent-crime-2026](./sources/17a-reducing-violent-crime-2026.md) — 17A — community-stabilization, violent-crime, environmental-intervention, place-based-strategy, coordination

## Referenced Research Queue — Files Not Included in This Extract

- pennpraxis-civic-infrastructure-2018 — PennPraxis / William Penn Foundation — civic-assets, public-space, governance, third-spaces, anti-displacement, maintenance
- fukuyama-political-order-decay-2014 — Fukuyama (2014) — state-capacity, political-decay, institutional-development, repatrimonialization, vetocracy, bureaucracy, interest-groups, rule-of-law
- aneja-xu-civil-service-state-capacity-2024 — Aneja & Xu (2024) — civil-service-reform, state-capacity, merit-based hiring, institutional regeneration
- christiansen-klitgaard-veil-of-vagueness-2010 — Christiansen & Klitgaard (2010) — institutional reform, veto players, strategic ambiguity, reform sequencing
- angelova-veto-player-reform-2018 — Angelova et al. (2018) — veto players, reform making, coalition structure, crisis-driven reform
- andrews-pritchett-woolcock-pdia-2012 — Andrews, Pritchett & Woolcock (2012) — capability traps, iterative adaptation, authorizing environments
- huber-mccarty-delegation-reform-2004 — Huber & McCarty (2004) — bureaucratic capacity, delegation, reform traps, formal modeling
- rich-outsourcing-bureaucracy-2023 — Rich (2023) — accountability-capacity tension, outsourcing, pockets of effectiveness

---

## Reviews

| Topic | Sources | Briefs | Status |
|-------|---------|--------|--------|
| [Community Stabilization & Environmental Violence Reduction](./reviews/community-stabilization-violence-research-review.md) | 17a-reducing-violent-crime-2026 | community-stabilization-framework · violence-interruption · homelessness-prevention · built-environment-community-anchors · land-use-stabilization | Pass 3 submitted 2026-09-16 (re-ingested via the restored RAG pipeline; corrects a fabrication and several citation errors an independent grading pass caught in Pass 2), pending fresh LLM grading — [Pass 2 grading (verdict: Fail — re-run)](./reviews/validation/community-stabilization-violence-research-review-grading.md) is superseded |
| Civic Infrastructure — Governance, Public Space, and Community Anchors | pennpraxis-civic-infrastructure-2018 | built-environment-community-anchors · neighborhood-civic-overlay · community-stabilization-framework · land-use-stabilization-inclusive-growth | Draft (not included) |
| Political Order and Decay — OS / Democratic Integrity / L3 Stress Test | fukuyama-political-order-decay-2014 | regulatory-modernization-corps · execution-corps-spec · institutional-modernization-corps · public-capital-authority · government-operating-system-upgrade · democratic-integrity-sequencing · candidate-nutrition-label · cde-framework · digital-nutrition-label | Revision submitted (not included) |
| B.1 — Institutional Regeneration and State Capacity Reform | aneja-xu-2024 · christiansen-klitgaard-2010 · angelova-2018 · andrews-pritchett-woolcock-2012 · huber-mccarty-2004 · rich-2023 | execution-corps-spec · regulatory-modernization-corps · institutional-modernization-corps · department-of-data-and-accountability · government-operating-system-upgrade | Draft (not included) |
