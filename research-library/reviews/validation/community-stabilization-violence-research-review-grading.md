---
review-graded: research-library/reviews/community-stabilization-violence-research-review.md
sources-graded:
  - 17a-reducing-violent-crime-2026
briefs-graded:
  - community-stabilization-framework
grading-model: OpenAI GPT-5 family
grading-date: 2026-09-16
fidelity-verdict: Pass with revisions
---

# Fidelity Grading Report: Community Stabilization & Environmental Violence Reduction (Pass 3)

**Review graded:** `research-library/reviews/community-stabilization-violence-research-review.md`

**Source graded:** `17a-reducing-violent-crime-2026` (42-page PDF, full-text source record, and 42 page-bounded RAG chunks)

**Brief graded:** `community-stabilization-framework`

**Grading model:** OpenAI GPT-5 family, independent from the recorded review author, Claude Sonnet 5 (Anthropic)

**Prepared:** 2026-09-16

---

## Purpose & Scope of This Grading Pass

This report grades the corrected Pass 3 review for fidelity, template compliance, citation accuracy, and coverage. It does not re-litigate the review's policy judgments.

The grading used the primary 42-page PDF, the regenerated full-text Markdown record, and all 42 page-bounded JSONL chunks. The RAG page metadata is internally consistent: each JSONL object has matching `page_start` and `page_end` values from 1 through 42. The available policy brief and two cited reference documents were checked directly.

Only `community-stabilization-framework.md` exists among the five briefs listed in the review frontmatter. The four unavailable briefs therefore remain outside the validated scope of this report.

---

## 1. Source Material Fidelity

| # | Review claim | Section | Cited page | What the source actually says | Match | Notes |
|---|---|---|---|---|---|---|
| 1 | Violent crime means homicide, robbery, and non-family aggravated assault | Source Scope | p. 23 | Appendix A gives exactly this definition and contrasts it with UCR | Full | Important scope correction added in Pass 3. |
| 2 | Across nine cities, roughly 3–5% of geography accounts for 20% of violent crime; distress indicators overlap | Aligned 1 | p. 3; pp. 27–29 | P. 3 states both claims exactly | Full | Appendix D supports the multi-city analysis generally, although pp. 27–29 do not independently restate the 3–5% statistic. |
| 3 | Lot greening reduced gun violence 29%; lighting reduced outdoor nighttime crime 39% | Aligned 2 | p. 11 | Both estimates and study descriptions appear on p. 11 | Full | Generalizability is appropriately caveated. |
| 4 | The problem is detection and coordination rather than resources | Aligned 3 | p. 10; pp. 11–14 | Exact framing is on p. 10 and operational elaboration follows | Full | Platform inference is clearly separated from source evidence. |
| 5 | 17A supports 90-day system launch, not 90-day completed visible repair | Aligned 4 | p. 18 | Source says launch in 90 days and measurable outcomes in 180 days | Full | Correctly distinguishes the brief's stronger design target. |
| 6 | One-time treatment and cadence slippage are among four unranked pitfalls | Aligned 5 | p. 21 | P. 21 presents four common pitfalls without ranking them | Full | Corrects the prior “primary failure mode” overstatement. |
| 7 | 50–100 sites, the 50-versus-500 maxim, and 20–30 areas are distinct figures | Aligned 6 | pp. 13, 15, 18 | Those figures appear on the cited pages in the described roles | Full | Correctly distinguishes operational list, maxim, and trend-based target. |
| 8 | Dallas is observational; only the Next 30% tier is statistically significant | Gap 1 | pp. 16, 31, 34–35 | Source gives the selection caveat and IRR results exactly as summarized | Full | Sample sizes, intervals, and p-values are accurate. |
| 9 | Ongoing maintenance funding is unspecified | Gap 2 | pp. 18–21 | Source relies on redirected existing capacity and does not define a post-exit funding mechanism | Full | Valid absence claim. |
| 10 | Federal involvement is unaddressed | Gap 3 | whole document | Report is city-focused and does not assess federal coordination | Full | Valid silence, though this is better understood as outside the paper's governmental frame than an internal omission. |
| 11 | Dallas open-data pulls differed by 22–25%; source recommends versioning and archival safeguards | Gap 4 | pp. 41–42 | Appendix I reports the discrepancy and four safeguards | Full | DoDA implications are clearly identified as review inference. |
| 12 | Trend classification and concentration tiers are different systems that the source blurs on p. 16 | Gap 7 | pp. 16, 23, 34–39 | Appendix F uses volume-ranked tiers; Appendix G uses Wheeler trend classes; p. 16 rhetorically equates them | Full | This is a strong and accurate adversarial finding. |
| 13 | Typical-city churn is one-third to one-half; 28–49% is not a valid unified range | Divergence 1 | p. 3; p. 28 | P. 3 gives the summary; p. 28 shows city/tier-specific newly-concentrated values | Full | Correctly diagnoses how the unsupported range was constructed. |
| 14 | Buckner/Peavy remained unresolved and was expected to require months | Divergence 2 | pp. 14–15 | The source lists options considered, a promise to return, and expected repeat visits | Full | Prior fabricated resolution is fully corrected. |
| 15 | Dallas used Monday targeting and Tuesday operational meetings | Divergence 3 | p. 13 | Exact day-names and functions appear on p. 13 | Full | Accurate. |
| 16 | The significant Next 30% result does not directly test the 1–3% worsening population | Open Question 1 | pp. 9–10, 16, 34–35 | Source reports separate classifications and never cross-tabulates the two populations | Full | Correctly left open. |
| 17 | Predictive models are not required to start | Decision 2 | p. 19 | Exact quotation appears on p. 19 | Full | Source and platform phases are distinguished. |
| 18 | Buckner/Peavy provides an unresolved combined-signal example | Decision 3 | pp. 14–15 | Source supports the unresolved factual description | Full | The conclusion favoring a handoff is labeled as platform reasoning. |

**Spot-check coverage:** All 20 rows in the review's Citation Verification table were checked. All PDF pages cited by those rows were compared with the corresponding JSONL chunks and primary PDF extraction. Absence claims were checked against their stated ranges or the complete document.

**Summary:** Pass 3 corrects the prior review's material source errors. No fabricated source outcome, reversed statistic, or consequential page mismatch remains. The source-facing grade is reduced slightly only for minor scope phrasing: the review says the authors “state directly” that several topics such as third spaces, youth programming, and anti-gentrification are excluded, when most are inferred absences rather than express exclusions.

---

## 2. Brief Fidelity

| # | Review claim about the brief | Section | What the brief actually says | Match | Notes |
|---|---|---|---|---|---|
| 1 | The brief targets visible repair within 90 days | Aligned 4 | It says visible corridor repair is designed to finish within 90 days | Full | Correctly treated as stronger than 17A's launch claim. |
| 2 | The brief still contains the unsupported 28–49% churn range | Divergence 1 / Revision Notes | The body says 28–49%; footnote 11 cites 17A pp. 7–9 | Full | Correctly flagged for revision. |
| 3 | The brief still calls cadence slippage the primary failure across comparable implementations | Revision Notes | The Weekly Cadence section makes that exact claim | Full | Correctly flagged as an overstatement. |
| 4 | The brief has a combined-signal protocol | Divergence 2 | Detection, activation, dual deployment, and resolution are specified | Full | Accurate. |
| 5 | The brief has no manual override for the 2–3-cycle homelessness delay | Decision 4 | No manual-escalation path or independent emergency-outreach safeguard is specified | Full | Corrects the prior invented mitigation. |
| 6 | The brief attributes a combined multi-indicator/Poisson method to 17A/CPAL | Gap 7 / Revision Notes | The DoDA backend section makes that attribution | Full | Review correctly flags that the source presents the elements separately. |
| 7 | The brief does not specify DoDA data-versioning safeguards | Gap 4 | Weekly pulls are described, but archival/version validation is absent | Full | Accurate. |
| 8 | 17A participation is time-bounded and DoDA is expected to build equivalent capability internally | Decision 3 Response | The brief limits 17A to “initial” pilot assessments/site selection but does not state a capability-transfer plan or that DoDA must build an equivalent internal function | Partial | “Initial” supports limited operational scope; “DoDA expected to build equivalent capability internally” and “time-bounded by design” are not actually specified. |
| 9 | Five platform briefs are covered | Frontmatter/header | Only the community-stabilization brief is present in the supplied repository | Unverifiable | The other four cannot be treated as validated. |

**Summary:** The corrected review is highly faithful to the available brief and now identifies rather than repeats its unsupported claims. Decision 3 retains one brief-description overstatement, and the claimed five-brief scope remains unsupported by available files.

---

## 3. Template Compliance

| Requirement | Present & followed | Notes |
|---|---|---|
| Source Scope stated first and used to gate Gaps | Partial | Scope is explicit, but Gaps 5–6 are cross-document/brief documentation issues rather than source-scope gaps. Gap 3 is an expected silence under the city-government frame. |
| Aligned Findings use “consistent with / supports” language | Yes | No “validates platform” drift remains. |
| Aligned Findings distinguish source evidence from platform inference | Yes | Particularly strong in Findings 1, 3, 4, and 6. |
| Divergences follow source → platform → justification | Yes | All three contain the required elements. |
| At least one genuine alternative interpretation appears | Yes | Exceptional-team explanation, tier mismatch, STZ timescale tension, and implementation complexity all qualify. |
| Each Design Decision has Challenge + Response | Yes | All four decisions comply structurally. |
| Citation Verification table has one row per cited claim | Partial | All principal source claims are represented, but the p. 23 definitional-scope claim and some repeated reference-document claims lack distinct rows despite the table's assertion that every claim is covered. |
| Every cited body claim has a page reference | Partial | PDF claims are page-cited. Local Markdown documents use section locators because they have no page model; several brief claims use named sections rather than pages. |

**Summary:** The review now follows the template's substantive disciplines. Remaining compliance issues are narrow: mixed-purpose items in Gaps and an overbroad claim that the Citation Verification table contains literally every cited occurrence.

---

## 4. Citation Accuracy (Page-Level)

| Citation Verification # | Page cited | Page(s) where content actually appears | Accurate |
|---|---|---|---|
| 1 | p. 3; pp. 27–29 | p. 3 for exact claim; Appendix D supports multi-city context | Yes, with superfluous appendix range |
| 2 | p. 11 | p. 11 | Yes |
| 3 | p. 10; pp. 11–14 | p. 10; pp. 11–14 | Yes |
| 4 | p. 18 | p. 18 | Yes |
| 5 | p. 21 | p. 21 | Yes |
| 6 | pp. 13, 15, 18 | pp. 13, 15, 18 | Yes |
| 7 | p. 16; p. 31; pp. 34–35 | p. 16; p. 31; pp. 34–35 | Yes |
| 8 | pp. 18–21 | pp. 18–21 | Yes for absence search |
| 9 | whole document | whole document | Yes for absence search |
| 10 | pp. 41–42 | pp. 41–42 | Yes |
| 11 | Local sections | Named sections | Yes as section locators |
| 12 | Overview §VI | Overview §VI | Yes as section locator |
| 13 | p. 16; pp. 36–39; pp. 34–35 | p. 16; pp. 36–39; pp. 34–35 | Yes |
| 14 | p. 3; p. 28 | p. 3; p. 28 | Yes |
| 15 | pp. 14–15 | pp. 14–15 | Yes |
| 16 | p. 13 | p. 13 | Yes |
| 17 | pp. 9–10, 16, 34–35 | pp. 8–10, 16, 34–35 | Yes |
| 18 | p. 19 | p. 19 | Yes |
| 19 | pp. 14–15 | pp. 14–15 | Yes |
| 20 | Brief sections | Named sections | Yes for absence search |

**Summary:** All 20 table rows lead to the correct supporting page or local-document section. Row 1's appendix range is unnecessary but not misleading. The rebuilt page-bounded RAG output resolves the prior page-location failures.

---

## 5. Coverage — What the Review May Have Missed

**Sections/chapters sampled that the review does not substantively cite:**

- Appendix B, pp. 23–24 — national historical trend context — relevant: limited; omission is reasonable because the brief does not depend on the national trend series.
- Appendix C, pp. 25–26 — baseline-selection methodology — relevant: yes; indirectly covered through the review's tier/churn discussion, but a direct citation would strengthen Gap 7.
- Appendix E.3, p. 31 — homicide-specific results — relevant: yes; the source contains a literal placeholder stating the detailed homicide table will be added when final data is confirmed. The review does not flag this incompleteness, although it also does not rely on the homicide claim.
- Appendix H, pp. 39–41 — data sources and references — relevant: moderate; the unfinished “[Additional references to be added as drafting continues]” marker is evidence that the source itself is a working paper. This does not undermine the claims the review uses, but it is worth noting in a source-quality discussion.

**Missed alignments:** No major omitted alignment materially changes the review. Appendix C's persistent-cell methodology supports the review's insistence on separating baseline and trend classifications.

**Missed divergences or gaps:** The unfinalized homicide table on p. 31 is the clearest omission. If the brief or future review uses the statement that homicide effects were stronger, it should be treated as unverified until the underlying table is supplied.

**Missed brief content:** No major available-brief claim bearing directly on 17A is now ignored. The review catches the churn error, cadence overstatement, attribution problem, data-integrity omission, crime-definition boundary, and 90/180-day mismatch.

---

## 6. Adversarial Rigor Check

- **Did the review surface an inconvenient finding?** Yes. It identifies the concentration-tier/trend-class mismatch, two non-significant Dallas tiers, data-source instability, the unresolved Buckner/Peavy case, and the brief's unsupported claims.
- **Are alternatives considered?** Yes. It considers exceptional personnel versus replicable architecture, short-cycle targeting versus long-horizon corridors, and the coordination costs of early homelessness-system involvement.
- **Does it treat uncertain findings as settled?** No material instance remains. It accurately distinguishes statistically significant, directionally favorable but non-significant, observational, and unresolved findings.

The Pass 3 review is genuinely adversarial. It now criticizes both the platform and the source's own category blending instead of treating the source as internally flawless.

---

## Fidelity Verdict

| Dimension | Grade |
|---|---|
| Source material fidelity | A- |
| Brief fidelity | B+ |
| Template compliance | B+ |
| Citation accuracy | A |
| Coverage completeness | B+ |
| Adversarial rigor | A |

**Overall fidelity verdict:** **Pass with revisions**

Pass 3 is suitable to use as a research receipt after the limited revisions below. None requires re-running the review from scratch.

**Required fixes before this review can be treated as fully validated:**

1. Restrict `briefs:` and “Platform briefs covered” to `community-stabilization-framework`, or add the four missing brief files and validate all claims attributed to them.
2. Correct Decision 3's Response. The available brief limits 17A to initial pilot activity, but does not say DoDA will build equivalent capability internally or expressly define the dependency as time-bounded. State only what the brief says, or add the transfer/sunset mechanism to the brief.
3. Move Gaps 5–6 into Notes for Brief Revision or label them explicitly as cross-document coherence findings; they are not gaps in 17A within its stated scope.
4. Add a Citation Verification row for the Appendix A violent-crime definition, and either add separate rows for cited reference-document occurrences or narrow the table preamble from “every claim” to “every distinct principal claim.”
5. Note the unfinalized homicide-results placeholder on p. 31 if retaining or later relying on the source's claim that homicide effects were stronger.

**Recommended, non-blocking clarification:** Revise “the authors state this directly” in Source Scope so it distinguishes expressly excluded structural interventions from topics that are merely absent from the report.

*This verdict grades the review's fidelity to its source material and process, not the platform's design decisions. A human reviewer makes the final decision about changes to the review or brief.*
