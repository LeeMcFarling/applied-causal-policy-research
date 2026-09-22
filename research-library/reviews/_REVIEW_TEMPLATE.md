---
review-topic: topic-slug
status: Draft
last_updated: YYYY-MM-DD
grading_status: pending
sources:
  - citation-key-one
  - citation-key-two
briefs:
  - brief-slug-one
  - brief-slug-two
---

# Research Review: [Topic Name]

**Sources reviewed:** [Institution A · Institution B]  
**Platform briefs covered:** [Brief Title A · Brief Title B]  
**Prepared:** YYYY-MM-DD

---

## Source Scope

*What is this source attempting to do, and what is it explicitly not attempting? State this before evaluating anything else. The rest of the review is evaluated relative to this scope — not relative to the totality of what the platform needs.*

**What this source addresses:** [The specific question, population, intervention type, and timeframe the source investigates]

**What this source explicitly does not address:** [Topics the authors explicitly set aside, or that fall outside the study design by construction]

**Implication for this review:** Not all platform briefs will find a 1:1 match in any given source. A source's silence on third spaces, coordination models, homelessness mitigation, federal implementation, or long-term social outcomes is expected and normal when those topics are outside its scope. Out-of-scope topics are noted here and excluded from the Gaps section. Only topics that fall *within* the source's stated scope — but where the source is nonetheless silent or inconclusive — belong in Gaps.

---

## Aligned Findings

*Claims where reviewed research supports the platform position, evaluated within the source's stated scope. Use precise language: "provides evidence consistent with," "supports this mechanism," "is consistent with" — not "validates platform." Note what the source itself demonstrates vs. what the platform infers from it.*

*Every claim that cites a specific finding, statistic, or quotation must include a page reference — `[citation-key, p. X]` or `[citation-key, pp. X–Y]`. Each cited claim gets a row in the Citation Verification section below.*

- **[Finding]** — [Source(s), p. X]. [1-2 sentences on what the source found and how it aligns.] *[Optional: note the inferential step between the source finding and the platform design conclusion.]*

---

## Gaps

*Topics that fall within the source's stated scope where the source is nonetheless silent, inconclusive, or weaker than expected. Do not list out-of-scope topics here — those belong in Source Scope above.*

- **[Gap]** — [What the literature does not address, why it falls within this source's scope (cite the page range searched, e.g. `[citation-key, pp. X–Y]`, so a reviewer can confirm the silence rather than just trusting it), and what the platform's position is in the absence of evidence.]

---

## Divergences

*Points where reviewed research contradicts, qualifies, or complicates the platform position — and the platform rationale for the chosen approach.*

- **[Divergence]** — [Source(s), p. X]. [What the source says.] *platform position:* [Why we hold the position despite the divergence — mechanism difference, scope difference, empirical dispute, values priority.]

---

## Open Questions

*Unresolved empirical or design questions that future research or pilot data should answer.*

- **[Question]** — [What would resolve it and what outcome would change the platform approach.]

---

## Notes for Brief Revision

*Specific claims in the briefs that should be updated, cited, or softened based on this review.*

- [ ] Brief: [slug] — [Specific revision needed]

---

## Design Decisions & Editorial Rationale

*A critical record of how this review was acted on — what decisions were made, why, and where the platform diverged from the research and on what grounds. This section exists to answer the question "why did you make that call?" during expert review and to prevent the review process from functioning as confirmation bias dressed as validation.*

*For each significant decision: state the decision, the source position, the platform position, and the explicit justification for the divergence. Do not rationalize — engage. If the justification is "we think the evidence is insufficient," say that. If it's "we are making a values priority," say that.*

### Decision [N]: [Short label]

**Decision made:** [What was added, changed, or specified in the brief as a result of this review]

**Source position:** [What the reviewed research actually says or implies — stated neutrally, not in platform's favor]

**Platform position:** [What the platform holds]

**Justification:** [Why — mechanism difference, scope difference, values priority, empirical dispute, or something else. Be specific.]

**Anticipated challenge:** [What an adversarial reviewer would say about this decision]

**Response:** [How platform would answer that challenge]

---

## Citation Verification

*Every claim above that cites a specific source finding, statistic, or quotation — in Aligned Findings, Gaps, Divergences, or Design Decisions — gets one row here, regardless of how it was sourced in the body above. This table is the master checklist a human reviewer works through to confirm each citation actually says what the review claims it says, at the page cited. This is a citation-accuracy check, not a re-evaluation of the claim's substance: substance is argued in the sections above. Leave `Verified` unchecked until a human has opened the source at the cited page and confirmed the match.*

| # | Claim (short label) | Appears in | Source | Page(s) | Verified |
|---|---|---|---|---|---|
| 1 | [Short label] | [Aligned Findings #1] | [citation-key] | p. X | [ ] |
| 2 | [Short label] | [Gaps #1] | [citation-key] | pp. X–Y | [ ] |

*If a row fails verification (page doesn't support the claim, page is wrong, or claim overstates/understates the source), do not silently fix it — flag it in the LLM Grading Status handoff below and correct the review body with a note in Design Decisions if the correction changes a platform decision.*

---

## LLM Grading Status

*This review is subject to an independent fidelity-grading pass using a separate LLM (different provider/family), run against `research-library/reviews/validation/_GRADING_TEMPLATE.md`. That pass grades whether this review is faithful to the source material and the brief(s) — not whether the review's conclusions are correct. See `research-library/reviews/validation/` for the grading output, saved as `<this-review-filename>-grading.md`.*

| Item | Status |
|------|--------|
| Grading submitted | [ ] |
| Grading report filed | [ ] |
| Fidelity findings addressed | [ ] |
| Citation Verification rows checked off | [ ] |
| `grading_status` YAML updated | [ ] |

*Until grading is complete, this review should be treated as a working draft, not a validated research receipt.*
