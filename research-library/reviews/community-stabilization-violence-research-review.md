---
review-topic: community-stabilization-environmental-violence-reduction
review-authored-by: Claude Sonnet 5 (Anthropic)
status: Pass 3 (2026-09-16) — re-verified against the primary 42-page source PDF via a newly restored RAG pipeline (page-bounded chunking + vector retrieval); corrects a fabricated case-study outcome and several page/statistic errors that Pass 2's citation-verification table exposed but did not itself catch, because Pass 2 was built from a markdown excerpt rather than the primary document
last_updated: 2026-09-16
grading_status: pending — Pass 3 supersedes both the Pass 1 grading (validation/community-stabilization-violence-research-review-grading.md, graded a pre-citation-verification draft) and the Pass 2 grading (same file, second pass, verdict Fail — re-run) referenced there
sources:
  - 17a-reducing-violent-crime-2026
briefs:
  - community-stabilization-framework
  - violence-interruption-youth-off-ramps
  - homelessness-prevention-automatic-stabilizer
  - built-environment-community-anchors
  - land-use-stabilization-inclusive-growth
reference-docs:
  - housing-public-infrastructure-system-overview
  - zoning-function-ladder
---

# Research Review: Community Stabilization & Environmental Violence Reduction

**Source reviewed:** Eichenbaum, Joe. *Reducing Violent Crime Without New Budget, New Staff, or More Arrests: A Pragmatic Guide for City Leaders*. 17A, February 2026. (42 pp., including appendices A–I)  
**Platform briefs covered:** Community Stabilization Framework · Violence Interruption & Youth Off-Ramps · Homelessness Prevention Automatic Stabilizer · Built Environment & Community Pillars (L1 theory) · Land Use Stabilization & Inclusive Growth  
**Reference docs (not independently reviewed, used to check cross-references the brief makes into the domain):** Housing & Public Infrastructure System Overview · Zoning for Function Ladder  
**Prepared:** 2026-08-04 (Pass 1) · 2026-09-16 (Pass 2) · 2026-09-16 (Pass 3)

---

**Pass 3 note (2026-09-16):** Pass 2 added a Citation Verification table but built every page reference from `research-library/sources/17a-reducing-violent-crime-2026.md`, which was itself only a short excerpt with a section-level table of contents, not the full text — the primary 42-page PDF was sitting in `research-library/incoming/17a/` the whole time and was never opened. An independent GPT-5-family grading pass (`reviews/validation/community-stabilization-violence-research-review-grading.md`) checked Pass 2 against that PDF directly and returned **Fail — re-run**, catching, among other things, a fabricated claim: Design Decision 3 stated 17A's Dallas homeless-encampment case was "resolved through sustained code enforcement," when the source (p. 15) explicitly reports it unresolved — options considered, contact information taken, months of further engagement expected.

Since that grading pass, the project's RAG pipeline has been rebuilt (page-bounded chunking in `scripts/ingest-research.py`, embedding in `scripts/embed-research.py`, retrieval in `scripts/query-research.py`). The 17A PDF has been re-ingested under this pipeline: 42 pages → 42 RAG chunks, one page per chunk (no page exceeded the chunker's 4,000-character threshold, so no page needed splitting), each carrying its own page number. This pass re-derives every citation in this review from that pipeline and from direct extraction of the source PDF — not from the markdown excerpt — and corrects every fidelity issue the grading report identified. New or corrected content from this pass is marked **[Pass 3]**.

---

## Source Scope

**What this source addresses:** Place-based environmental interventions for violent crime reduction using existing city staff, budgets, and agency authority. The specific question is: what can city leaders do with what they already have? The scope is operational: targeting methodology (crime concentration analysis), intervention types (lighting, lot remediation, code enforcement, public works), coordination architecture (weekly cross-agency meetings), and the Dallas 2024–2025 case study as primary evidence.

**[Pass 3] Definitional scope, stated by the source itself:** "Violent crime" in this paper means homicide, robbery, and non-family aggravated assault — the authors explicitly exclude family-related aggravated assault (domestic and intimate-partner violence), on the grounds that those offenses respond to different policy levers than place-based environmental intervention (Appendix A, p. 23). This is narrower than the FBI's UCR violent-crime category (which includes all aggravated assault and forcible rape) and narrower than many cities' own definitions. Every claim in this review and in the brief about "violence" or "violent crime" inherits this narrower scope — it says nothing directly about family violence.

**What this source explicitly does not address:** The authors state this directly — the source does not evaluate housing stability, workforce development, behavioral health, long-term social cohesion, or federal implementation design. It also does not address staffed third spaces, youth programming, violence interruption, anti-gentrification, homelessness mitigation, or the causal mechanisms behind collective efficacy. These are out of scope by authorial design, not oversight.

**Implication for this review:** The Gaps section below addresses only topics within 17A's scope — environmental interventions and coordination — where the source is nonetheless silent or weaker than expected. The absence of third-spaces evidence, homelessness coordination protocols, federal role analysis, and long-term social capital evidence is expected given the source's scope and is not treated as a gap requiring explanation.

**Reference-doc scope:** The community stabilization brief cross-references six other domain documents by name or dependency (STZ, NCO, built-environment-community-anchors, LIFT, DoDA, homelessness-prevention-automatic-stabilizer). Of these, `special-transit-zones.md`, `built-environment-community-anchors.md`, and `neighborhood-civic-overlay.md` do not exist as files in this repository — only the domain-level system overview and the zoning ladder do. This review uses those two available documents to sanity-check the brief's cross-references where they overlap, and flags claims that depend on a document it cannot read rather than fabricating a citation to one.

---

## Aligned Findings

**1. Geographic concentration provides evidence consistent with place-based targeting.** [17a-reducing-violent-crime-2026, p. 3; multi-city detail in Appendix D, pp. 27–29]  
17A documents that, across nine cities, 3–5% of city geography accounts for 20% of violent crime, and that code violations, 311 complaints, and illegal dumping cluster in much of the same territory (p. 3). Appendix D's city-specific parameters and churn tables (pp. 27–29) confirm this holds across all nine cities in the multi-city comparison, not just Dallas. This is consistent with platform's place-based targeting approach and the design of DoDA's neighborhood-condition dashboards as a cross-indicator targeting instrument. *Note: the spatial correlation is well-established; the causal direction and the DoDA-specific implementation are platform design conclusions drawn from that evidence, not findings the paper itself makes.*

**2. Environmental intervention effect sizes are large and rigorous.** [17a-reducing-violent-crime-2026, p. 11]  
17A cites two high-quality studies that provide the specific effect sizes the platform community stabilization brief gestures at without quantifying: a Philadelphia RCT finding cleaning and greening vacant lots reduced nearby gun violence by 29% (Branas et al., 2018), and a study of NYC public housing finding improved street lighting reduced outdoor nighttime crime, including violent offenses, by 39% (Chalfin et al., 2021) — both explicitly on p. 11. *Note: these are effects of the specific interventions studied in those contexts; generalizability to all city types and scales is plausible but not proven by this paper.*

**[Pass 3] Cross-domain corroboration:** The Housing & Public Infrastructure system overview independently cites the same Branas et al. 2018 finding, plus a companion citation 17A does not mention — a University of Pennsylvania/Columbia RCT finding a 13% reduction in nearby gun assaults from abandoned-building remediation, and quasi-experimental replications by MacDonald et al. and Cui et al. [housing-public-infrastructure-system-overview, Section VI]. This strengthens Aligned Finding 2 but means the brief's footnotes [^9][^10] are not the full evidentiary base the platform has actually assembled for this claim — see Gap 6 below.

**3. The "detection and coordination problem" framing is consistent with the DoDA/Execution Corps architecture.** [17a-reducing-violent-crime-2026, p. 10, elaborated pp. 11–14]  
The source's exact framing — "That's not a resource problem. It's a detection and coordination problem" — appears on p. 10, following the observation that the departments needed (code enforcement, sanitation, public works, parks, transportation) already exist in every city government; what's missing is a system that tells them where to concentrate. This framing is consistent with platform's architectural approach: DoDA as detection layer, Execution Corps as coordination function, RMC for real-time blocker resolution. The 17A model supports the logic of the platform design but does not demonstrate that the federal-scale version of this architecture will produce the same results as a city-advisory model. *Alternative interpretation: Dallas's coordination success may reflect unusually capable management at the individual level — the coordinator, the CPAL team, the specific agency leads — rather than the architecture itself. The paper cannot distinguish between a replicable model and an exceptional team (see Gap 1).*

**4. [Pass 3, corrected] The brief's 90-day claim is only partly supported by the source, and the two documents are making different claims.** [17a-reducing-violent-crime-2026, p. 18]  
17A states: "Any city can launch this approach in 90 days and see measurable outcomes within 180, using existing staff and existing data" (p. 18). That is a claim about launching the coordination *system* — standing up the meeting cadence, the priority list, the departmental commitments. The community stabilization brief's parallel claim — "something you can see from the street within three months," i.e., visible corridor repair *completed* in 90 days — is a different and stronger claim than what 17A demonstrates. Nothing in the source measures time-to-visible-repair as a distinct milestone from time-to-launch. This should be labeled a platform design target inspired by 17A's timeline, not a finding 17A itself supports. *(Pass 2 treated this as directly evidenced; that was the grading report's Aligned Finding 4 mismatch, confirmed here.)*

**5. Maintenance as a design requirement, not an afterthought.** [17a-reducing-violent-crime-2026, p. 21]  
17A identifies "treating this as a one-time campaign" as one of four common pitfalls it names (alongside confusing activity with impact, skipping the data, and letting the cadence slip) — not explicitly ranked as *the* primary one, though the surrounding language ("the coordination rhythm is the engine... when it stops, so does follow-through") gives cadence slippage particular emphasis. *(Pass 2 called this "the most common failure mode"; the source presents four pitfalls without an explicit ranking, so this is corrected to "one of four common pitfalls.")* This still supports platform's failure modes section, which lists "investments without maintenance" as a primary failure in community investment programs generally — a claim about the platform's own broader experience, not sourced to 17A specifically. Both reach the same design conclusion: sites stay on the active list until conditions have stabilized, not until the first intervention is complete (also p. 14).

**6. [Pass 3, corrected] Short-list discipline is supported, but three distinct numbers should not be merged into one.** [17a-reducing-violent-crime-2026, pp. 13, 15, 18]  
Three related but distinct figures appear in the source, and Pass 1/2 blended them:
- **50–100 sites**: the actual size of Dallas's operational priority list at any given time (p. 13).
- **"50 locations with repeated engagement will have more impact than 500 locations with one-off visits"**: a general practitioner maxim about concentration discipline, stated in the Dallas case-study narrative (p. 15) — not an experimentally demonstrated comparison.
- **20–30 half-mile areas**: the narrower "tipping point" target — places trending in the wrong direction, roughly 1–3% of city geography in a given year (pp. 3, 9–10, 18). This is a subset of, not the same as, the 50–100-site operational list; the 20–30 areas are the highest-priority slice within a broader list that also includes stable chronic hotspots.
This is consistent with platform's targeted design over broad-based community investment, but the brief and Pass 1/2 of this review both used these numbers somewhat interchangeably. See Gap 7 for the related conflation between this trend-based "20–30 areas" figure and the volume-ranked tier where 17A's statistically significant intervention result was actually found.

---

## Gaps

*Topics within 17A's stated scope — environmental interventions and city coordination — where the source is nonetheless silent or weaker than expected. Out-of-scope topics (third spaces, homelessness, anti-gentrification, long-term social capital, federal implementation) are documented in Source Scope above and excluded here.*

**1. [Pass 3, corrected] The Dallas case study cannot isolate the intervention effect from management quality, and the statistical support is stronger for one tier than the other two.** [17a-reducing-violent-crime-2026, p. 16; Appendix E.4, p. 31; Appendix F, pp. 34–35]  
The source states plainly: "This is not a randomized controlled trial. Intervention areas weren't assigned randomly; they were chosen because they had high crime and conditions that seemed amenable to environmental intervention" (p. 16), and Appendix E.4 lists selection effects, one year of data, inability to isolate the intervention from concurrent factors, and unmeasured dosage variation as caveats (p. 31).

**[Pass 3] What Appendix F actually shows, precisely:** Testing three concentration tiers with Poisson-based incidence rate ratios (Appendix F, pp. 34–35), only the *middle* tier — 20th–50th percentile of crime concentration, referred to there as "Next 30%" (14% of city geography, 21 intervention cells) — reached statistical significance: IRR 0.81, 95% CI 0.69–0.95, p = 0.008. The **Top 20%** tier (17 cells, IRR 0.94, CI 0.80–1.12) and the **Bottom 50%** tier (52 cells, IRR 0.90, CI 0.77–1.05) moved in the same favorable direction but were not statistically distinguishable from chance, "largely because the sample sizes are too small to detect the observed effects with confidence" (p. 34). The paper is candid about this. Pass 1 and Pass 2 of this review, and the brief, present the Dallas evidence as a single undifferentiated result; it is actually one statistically significant tier and two directionally-consistent-but-non-significant ones. This is the most significant within-scope evidentiary gap: the paper's strongest evidence covers a 14%-of-geography middle tier, not the full range of conditions the brief's targeting logic addresses.

**2. Maintenance funding mechanism is not specified.** [Range searched: 17a-reducing-violent-crime-2026, pp. 18–21]  
17A's roadmap section identifies "treating this as a one-time campaign" as a pitfall, but does not specify how cities fund ongoing maintenance — it assumes agencies redirect existing staff time. For a federal deployment model where the coordination unit (EC/CRC) eventually exits, the maintenance funding question is unresolved.

**3. The federal role in city-level coordination is unaddressed.** [Range searched: 17a-reducing-violent-crime-2026, whole document — see the source's own scope statement]  
17A's model depends on mayoral commitment as the accountability pillar. The paper does not address whether federal involvement changes this dynamic.

**4. [Pass 3] The source's own data-source reproducibility warning is directly relevant to DoDA and is not cited anywhere in the brief.** [17a-reducing-violent-crime-2026, Appendix I, pp. 41–42]  
Appendix I documents that a second pull of the same Dallas open-data endpoint (Socrata resource `qv6i-rri7`), using the same offense filters, returned 22–25% fewer violent-crime records than the original pull used to build the paper's Dallas analysis — "the same offense strings return fewer matching records from the endpoint today than they did when the data was originally exported," with no available changelog to explain why. The paper resolved this for its own Dallas figures by falling back to data supplied directly by the Dallas Police Department. It argues the multi-city *concentration and churn* metrics (Jaccard indices, tier classifications) are likely robust to this because they measure geographic rank rather than absolute counts — but that robustness argument does not extend to a system, like DoDA, that would ingest absolute counts and trend classifications on a rolling weekly basis from the same kind of live municipal open-data portals. 17A's own recommendations — archive raw pulls, validate against authoritative sources, document query parameters, pin to a versioned dataset (p. 42) — describe exactly the kind of data-integrity safeguard DoDA's weekly automated retargeting pull would need and does not currently specify in the brief.

**5. NCO's role in third-space funding is stated ambiguously against how NCO is defined elsewhere in the domain.** [zoning-function-ladder, Rung 0 and Rung 1; housing-public-infrastructure-system-overview, Section III]  
The community stabilization brief states: "the NCO creates the regulatory pathway for by-right small-scale community services... This framework provides the startup capital and operating support for the first deployment cycle... so the regulatory permission and the funding arrive together." Read carefully, "this framework" refers back to the community stabilization framework itself, not to NCO — but the sentence is one antecedent-swap away from implying NCO is a funding instrument. Both the zoning ladder and the system overview describe NCO consistently as a by-right regulatory pathway gated by LIFT, a fiscal solvency test, not a capital source.

**6. The brief's evidentiary footnotes do not reflect the platform's own broader evidence base for this claim.** [housing-public-infrastructure-system-overview, Section VI]  
The community stabilization brief cites Branas et al. 2018 and Chalfin et al. 2021 (footnotes 9–10) via the 17A review. The Housing & Public Infrastructure domain overview independently maintains a broader evidentiary base for the same claim (adding the abandoned-building RCT and the MacDonald/Cui replications; see Aligned Finding 2). Neither document currently cites the other's evidence.

**7. [Pass 3] The source's own narrative blends two different classification systems, and the brief inherits the blend uncritically.** [17a-reducing-violent-crime-2026, p. 16; Appendix G, pp. 36–39; Appendix F, pp. 34–35]  
17A uses two distinct methods to identify priority locations: (a) a **trend classification** (Appendix G) using a Wheeler z-score threshold (|z| ≥ 3.0) applied to each cell's year-over-year change, producing the "1–3% of city geography... trending the wrong way" figure cited throughout the paper and in Aligned Finding 6 above; and (b) a **concentration-rank tier** (Appendix E/F) that buckets cells into Top 20% / Next 30% / Bottom 50% by their *share of total violent crime volume* — an entirely different sorting, covering 3%, 14%, and 86% of city geography respectively (Appendix A, p. 23; Appendix F, p. 34). These are not the same set of cells: a cell can be in the high-volume Top 20% tier while being stable (not trending worse), or in the low-volume Bottom 50% tier while trending sharply worse in z-score terms.

On p. 16, the source itself blurs this distinction: "The stabilization effect was clearest in the middle tier... These are precisely the areas Section 2 identifies as the narrow policy target: the 1–3% of geography at risk of tipping into higher concentration." But the "middle tier" in that sentence is the volume-ranked Next-30%/Top-50% tier — 14% of city geography — not the 1–3% z-score-classified "worsening" cells from Section 2. These are different-sized, differently-defined sets, presented as if they were the same population. The community stabilization brief's own targeting logic repeats this blend: it ranks sites by "(a) emerging-deterioration score... and (b) environmental intervention feasibility," treating the statistically significant Next-30% tier result as support for prioritizing the narrower emerging-deterioration (1–3%) cells specifically. 17A's strongest statistical evidence (Gap 1) is for the volume-ranked middle tier, not demonstrably for the trend-classified tipping-point cells the brief's language foregrounds. This is worth resolving explicitly rather than carrying the source's own ambiguity forward silently.

---

## Divergences

**1. [Pass 3, corrected] Adaptive weekly retargeting vs. platform's corridor-alignment design — and a corrected churn statistic.** [17a-reducing-violent-crime-2026, p. 3; Appendix D.3, p. 28]  
17A's plain-language statement is that, in a typical city, "a third to half of the highest-crime micro-areas are different from one year to the next" (p. 3). Appendix D.3 gives the underlying city-by-city detail: in the most volatile cities, half or more of the highest-concentration geography turns over in a single year; even in relatively stable cities, 14–28% of the worst cells are new (p. 28).

**Correction of a fabricated figure:** Pass 1 and Pass 2 of this review (and the brief's footnote 11) cited "28–49% of highest-concentration areas are different from year to year" as a single statistic. That figure does not appear anywhere in the source as a unified number. It appears to combine two different cities' single-tier figures from Appendix D.3's table — Denver's 50%-tier "% Newly Concentrated" (28%) and Dallas's 20%-tier "% Newly Concentrated" (49%) — as if they were a typical-city range. They are not measurements of the same thing; mixing a Denver 50%-tier figure with a Dallas 20%-tier figure produces a number that describes no actual city or tier. The correct citation for "typical city" churn is the plain-language "a third to half" statement (p. 3), or, for a precise cross-city range, "14–28% in relatively stable cities to half or more in the most volatile cities" (p. 28) — both of which should replace "28–49%" in the brief's footnote 11.

platform's community stabilization brief, by contrast, aligns investment with STZ corridor planning and long-term infrastructure buildouts — "the leading edge of sustained investment," coordinated with "long-term corridor buildout." This creates a potential tension: if a third to half of the highest-concentration areas differ annually, aligning environmental intervention with multi-year STZ corridors may lock investment into last year's hotspots.

*Platform position:* These may be operating at different timescales rather than contradicting each other — DoDA dashboards provide the fast-retargeting layer (aligned with the 17A model) while STZ corridors provide the longer-term investment context. But the brief doesn't currently specify this two-speed design explicitly.

**Cross-check against the domain overview and zoning ladder:** Neither available reference document specifies an STZ corridor's actual duration — `special-transit-zones.md` is not in this repository. The system overview does confirm STZ's sequencing logic is inherently multi-step and multi-year ("Authorize → Evaluate Capacity → Build Infrastructure → Deliver Development → Measure → Scale," infrastructure preceding development — Section IV), which corroborates the divergence as real rather than resolving it. The "two-speed design" the brief promises but does not yet specify is a nontrivial integration problem.

**2. [Pass 3, corrected] The homeless encampment problem is treated differently — and the case was not resolved.** [17a-reducing-violent-crime-2026, pp. 14–15]  
The Dallas case study describes a specific site — an absentee-landlord property near North Buckner Boulevard and Peavy Road that had become an encampment, with an adjacent business reporting constant drug activity and 911 calls, and an unused bus stop serving as a gathering point (p. 15). **Corrected from Pass 1/2:** the source does *not* report this resolved. It states: "The team considered options: work with Dallas Area Rapid Transit to remove the bench, increase patrols, pursue the absentee landlord through community prosecution. They took the clerk's information and promised to return. This area would likely require months of repeat visits across dozens of interventions" (p. 15). Options were under consideration, not completed; the source explicitly frames this as an unresolved, multi-month problem. 17A treats it as a hard instance of the environmental coordination problem — one its own model has not yet closed out, not a demonstrated success story.

platform has a separate framework for this (the homelessness prevention automatic stabilizer) that would, in principle, have intercepted the individuals at that site upstream. But neither brief specifies the handoff: when does a crime-concentration site that includes a homeless encampment trigger the homelessness system, the community stabilization system, or both?

*Platform position:* The platform's design intention is that these systems interoperate. The DoDA HSEWI and neighborhood-condition dashboards should surface the co-location of violence and housing instability as a combined signal.

**→ ADDRESSED (2026-08-04):** Combined-signal site protocol specified in brief v0.2: DoDA auto-flag criteria, calendar-invite activation mechanism, dual-deployment ownership split (CRC for environment, Homelessness EC for housing), shared DoDA site record, and dual-condition resolution requirement. [community-stabilization-framework, "Combined-Signal Sites" section, and footnote 12] *(Note: the brief's own framing of this addressed item does not depend on the Buckner/Peavy case having been "resolved" — the protocol is designed to close exactly this kind of open-ended case faster than 17A's ad hoc handling did, which is arguably a stronger justification than the fabricated resolution claim it replaces.)*

**3. The "coordination" concept operates at different levels of specificity.** [17a-reducing-violent-crime-2026, pp. 13–14, 21]  
17A's coordination model is operationalized with a specific cadence: the team reviewed targeting data every Monday, with separate departmental meetings on Tuesdays, facilitated by CPAL (p. 13, confirmed exact day-names). platform's coordination model is architecturally specified (DoDA tracks, Execution Corps deploys, RMC resolves blockers) but originally lacked this operational rhythm.

*Platform position:* The operational rhythm should be a design requirement for the community stabilization framework, not an implementation detail left to localities. *(Corrected: 17A names cadence slippage as one of four pitfalls, with emphatic language — "the coordination rhythm is the engine" — rather than empirically ranking it the single primary failure mode across comparable implementations; see Aligned Finding 5.)*

**→ ADDRESSED (2026-08-04):** The Crime Reduction Council (CRC) operational model has been specified in brief v0.2. Monday/Tuesday cadence, meeting-software/LLM integration, sunset conditions, and 5-city pilot design are now explicit design requirements.

---

## Open Questions

**1. [Pass 3, corrected] Tipping-point targeting vs. chronic hotspot targeting — and which tier the evidence actually supports.** [17a-reducing-violent-crime-2026, pp. 9–10, 16; Appendix F, pp. 34–35]  
17A's data shows that chronic hotspots are generally improving even without targeted intervention; the "worsening" cells identified by z-score trend classification represent roughly 1–3% of city geography (pp. 9–10). Brief v0.2 resolved the platform-facing question — it explicitly prioritizes these emerging-deterioration areas over chronic stable hotspots. **What remains genuinely open, per Gap 7:** 17A's only statistically significant intervention result covers a differently-defined, larger population (the volume-ranked Next-30%/Top-50% tier, 14% of geography), not the narrower 1–3% trend-classified population the brief's language foregrounds as the target. Whether the statistically significant result actually applies to the narrower tipping-point cells the brief prioritizes is not established by this paper, because the paper never tests the trend-classified population directly against a non-intervention comparison — it only reports the two classification schemes side by side and, on p. 16, implies (without formally establishing) that they overlap substantially. This is a live methodological question, not a resolved one, and should not be treated as settled by either document.

**2. At what intervention scale do market effects emerge?** 17A's intervention operates at 50–100 sites with existing city staff — likely below the threshold for generating meaningful housing market effects. platform's community stabilization framework is federally-funded and potentially operating at much larger scale. This question requires modeling that neither platform nor 17A has done.

**3. Does the third-spaces component add measurably to environmental-only intervention?** 17A's evidence is for physical environmental interventions only. Is there evidence that combined physical + social intervention outperforms physical intervention alone?

**4. How does the discharge-pipeline closure interact with environmental targeting?** If discharge planning is working, does this measurably reduce concentration at combined-signal sites? This would be a testable prediction from the combined-system design.

**5. Does increasing system integration introduce implementation risk that outpaces theoretical coherence?** The operational complexity of DoDA + CRC + Execution Corps + homelessness teams + healthcare routing has not been independently evaluated.

**6. [Pass 3] Does the platform's reliance on live municipal open-data portals for DoDA inherit 17A's own documented reproducibility risk?** Per Gap 4, 17A found a 22–25% swing in Dallas violent-crime counts between two pulls of the same open-data endpoint. DoDA's weekly automated retargeting pull is architecturally the same kind of live-portal dependency, at greater scale (multiple cities, continuous operation). This is a testable, near-term engineering question, not a long-run research question, and should be resolved before DoDA's targeting pull is built rather than after.

---

## Notes for Brief Revision

- [x] **Community Stabilization** — Add precise effect sizes from Branas et al. 2018 (29% gun violence reduction) and Chalfin et al. 2021 (39% outdoor nighttime crime reduction) as Chicago footnotes. *(Done in v0.2, footnotes [^9] and [^10].)*

- [x] **Community Stabilization** — Add the weekly retargeting rhythm as an explicit operational requirement in the DoDA integration section. *(Done in v0.2.)*

- [x] **Community Stabilization** — Address the tipping-point vs. chronic targeting question explicitly. *(Done in v0.2 as a platform design choice; the underlying evidentiary question of which tier 17A's significant result actually covers remains open — see Open Question 1.)*

- [x] **Community Stabilization + Homelessness Prevention** — Add a cross-reference section specifying the operational interface for combined-signal sites. *(Done in v0.2.)*

- [ ] **[Pass 3, urgent] Community Stabilization footnote 11** — Correct "28–49% of highest-concentration areas are different from year to year" — this figure does not exist in the source; it appears to mix Denver's 50%-tier and Dallas's 20%-tier "% Newly Concentrated" values. Replace with "a third to half... different from one year to the next" (17A, p. 3) or the cross-city range "14–28% in relatively stable cities to half or more in the most volatile cities" (17A, Appendix D.3, p. 28). See Divergence 1.

- [ ] **[Pass 3, urgent] Community Stabilization footnote 12** — The personnel/cadence citation currently attributes "letting the cadence slip" to 17A as *the* primary failure mode. The source lists it as one of four pitfalls without an explicit ranking. Soften to "identified among the pitfalls 17A names" or similar. See Aligned Finding 5 and Divergence 3.

- [ ] **[Pass 3, urgent] Community Stabilization, Execution Corps Deployment section, footnote 12** — The Dallas homeless-encampment example (North Buckner/Peavy Road) should not be cited as a precedent that was resolved through the existing coordination model; per the source (p. 15) it was an open, unresolved, multi-month case. If this example is retained to motivate the Combined-Signal Sites protocol, frame it as a case 17A's own model had not yet closed — which argues *for* the protocol's necessity — rather than as a success story.

- [ ] **[Pass 3] Community Stabilization, Decision 4 in this review's own record** — The Design Decision 4 Response previously asserted that "the CRC Coordinator... can manually escalate to the Homelessness EC Connector at any time" and that "emergency outreach remains available through standard channels independent of the CRC cadence." Neither claim is stated in the brief's actual text (checked against `community-stabilization-framework.md`, "Combined-Signal Sites" and CRC Structure sections). This is now corrected in Design Decision 4 below. If the platform wants this mitigation to actually exist, it needs to be added to the brief, not assumed.

- [ ] **[Pass 3] Community Stabilization** — Distinguish the brief's targeting language between the volume-ranked concentration tier (where 17A's significant result lives, 14% of geography) and the trend-classified "emerging-deterioration" cells (1–3% of geography) it currently treats as the same population. See Gap 7.

- [ ] **[Pass 3] Community Stabilization** — Add a data-integrity safeguard for DoDA's weekly retargeting pull, modeled on 17A's own Appendix I recommendations: archive raw pulls, validate against authoritative sources (not just the live open-data endpoint), document query parameters, and pin to a dataset version rather than a live query. See Gap 4.

- [ ] **[Pass 3] Community Stabilization** — Note the narrower violent-crime definition (excludes family-related aggravated assault) inherited from 17A wherever the brief cites 17A-sourced statistics, so "violence" claims are not read as covering domestic/intimate-partner violence. See Source Scope.

- [ ] **[Pass 3] Community Stabilization + Housing_and_Public_Infrastructure overview** — Reconcile the brief's footnotes [^9][^10] with the broader evidentiary set the domain overview independently maintains (abandoned-building RCT, MacDonald/Cui replications). See Gap 6.

- [ ] **[Pass 3] Community Stabilization** — Soften "This framework provides the startup capital and operating support" phrasing in the Third Spaces section so the antecedent for "this framework" is unambiguous, and note NCO's role is by-right regulatory pathway only, not a funding source. See Gap 5.

- [ ] **Violence Interruption** — The operational-rhythm lesson from 17A ("letting the cadence slip" as a named pitfall) could strengthen the violence interruption brief's organizational support section.

- [ ] **Land Use Stabilization** — Phase 3 research integration on anti-displacement effects of environmental improvement is an open need. 17A provides evidence consistent with the environmental intervention model but doesn't address market effects.

---

## Design Decisions & Editorial Rationale

*A critical record of how this review was acted on — what decisions were made, why, and where the platform diverged from or extended the research. This section is not a defense of the platform. It is a documented accountability record for expert review.*

---

### Decision 1: Adopt the 17A operational model (Monday/Tuesday cadence) as an explicit platform design requirement

**Decision made:** The brief was updated to specify the Monday targeting meeting and Tuesday department follow-up as explicit operational requirements for CRC deployments, not implementation details left to localities.

**Source position:** 17A describes the Monday/Tuesday cadence as what Dallas actually did (p. 13, confirmed by name — "reviewed targeting data... every Monday," "meetings with operational departments on Tuesdays"), and names "letting the cadence slip" as one of four pitfalls it observed, with emphatic framing ("the coordination rhythm is the engine," p. 21) but no explicit empirical ranking against the other three. They do not prescribe the cadence as a universal requirement; the report is framed as a guide for city leaders with existing discretion.

**Platform position:** The cadence is a design requirement, specified centrally and protected contractually in CRC deployments.

**Justification:** The platform implementation is a federal coordination deployment with performance accountability to DoDA — not an advisory relationship like 17A's. The evidence that cadence degradation is a named pitfall, described in the source's most emphatic language of any of the four, is enough to treat it as a gate condition rather than a mere recommendation, even without a formal ranking.

**Anticipated challenge:** Centralizing the cadence requirement reduces local ownership, which 17A identifies as itself a risk factor.

**Response:** The brief preserves mayoral commitment as a prerequisite for CRC deployment. The cadence is a contractual requirement of the EC deployment, but its content — which sites, which interventions, which agency leads — is locally determined.

---

### Decision 2: Specify binary classification as future analytical upgrade path, despite 17A explicitly saying predictive models are not needed

**Decision made:** The brief specifies that a binary classifier on structured DoDA data is the intended upgrade to the targeting layer once multi-city longitudinal data is available.

**Source position:** 17A explicitly says: "You don't need a predictive model, a risk-terrain analysis, or a proprietary platform to get started" (p. 19, confirmed exact quote). Their advice is directed at cities with constrained analytical capacity.

**Platform position:** A binary classifier on structured tabular DoDA data is appropriate at federal scale as a future upgrade — not a prerequisite.

**Justification:** 17A's advice addresses starting friction, not steady-state analytical ceiling. platform is building DoDA as persistent multi-city analytical infrastructure; at that scale a tipping-point classifier is cheap and low-drift. The classifier is not a prerequisite for any city to begin — the base implementation is explicitly the same data-ranking approach 17A validates.

**Anticipated challenge:** Specifying a future ML layer creates an expectation of analytical capability that DoDA may not have at launch.

**Response:** The brief is explicit that the classifier requires accumulated multi-city training data and describes what DoDA is *designed to accommodate*, not what it currently provides.

---

### Decision 3: Include 17A analysts in pilot-city combined-signal site operational matching

**Decision made:** The brief specifies that in pilot cities with an active 17A advisory relationship, 17A analysts participate in the initial assessment of combined-signal sites.

**Source position [Pass 3, corrected]:** 17A does not address multi-system handoffs as a general design question. Their Dallas case study describes one combined-signal-type site — the North Buckner/Peavy Road absentee-landlord encampment — as an unresolved, multi-month environmental coordination challenge. The source reports the team considered several options (DART bench removal, increased patrols, community prosecution of the landlord), took a witness's contact information, and expected months of further repeat engagement — not that the case was resolved through sustained code enforcement or any other closed intervention (p. 15). *(Corrected: Pass 1 and Pass 2 both stated this case was "resolved through sustained code enforcement," which the source does not support. This was the specific fabrication the Pass 2 grading report caught.)* If anything, this case is evidence that 17A's own model, without a homelessness-system handoff, left this kind of site unresolved for months — a point that arguably strengthens rather than weakens the case for the platform's combined-signal protocol, since it identifies exactly the gap that protocol is meant to close.

**Platform position:** 17A analysts are borrowed for the pilot period as a bridge between their existing city relationships and DoDA's new analytical infrastructure for combined-signal sites.

**Justification:** 17A's analysts have direct knowledge of Dallas site-level data and operational context. Their participation reduces cold-start risk in the combined-signal protocol — a protocol whose necessity is, if anything, better evidenced now that the Buckner/Peavy case is correctly understood as unresolved rather than as a demonstrated success 17A already achieved alone.

**Anticipated challenge:** 17A is a management consulting firm with commercial interests in city advisory relationships. Including them as quasi-official analytical partners in a federal pilot could create a hard-to-exit dependency.

**Response:** The brief specifies 17A analyst participation as a pilot-period arrangement, with DoDA expected to build equivalent capability internally. The dependency is time-bounded by design.

---

### Decision 4: LLM pattern detection for homelessness EC activation, rather than calendar flag on first DoDA combined-signal flag

**Decision made:** The Homelessness EC Connector is activated by LLM pattern detection across multiple consecutive meeting transcripts — not by a first-cycle DoDA flag.

**Source position:** 17A does not address multi-system coordination between crime reduction and homelessness response. This is platform's own design judgment with no direct source to confirm or challenge it.

**Platform position:** First-cycle flags are informational only. Confirmed recurring patterns (typically 2–3 consecutive cycles) trigger the calendar invite.

**Justification:** Adding a stakeholder to a standing operational meeting on a single data flag creates coordination overhead. The pattern-detection threshold ensures the Homelessness EC Connector enters only when the site has demonstrated it cannot be resolved through environmental action alone.

**Anticipated challenge:** The 2–3 cycle threshold means sites requiring homelessness engagement may receive weeks of environmental-only intervention before the homelessness system activates. For individuals in acute crisis, this delay could be harmful.

**Response [Pass 3, corrected]:** This is a genuine tension and a real cost of the design. *(Corrected: Pass 1/2's Response claimed two mitigating factors — that "the first-cycle DoDA flag is visible to the CRC Coordinator, who can manually escalate to the Homelessness EC Connector at any time" and that "emergency outreach remains available through standard channels independent of the CRC cadence." Neither claim is actually stated anywhere in `community-stabilization-framework.md` — the brief's Detection section says a first-cycle flag "is logged to the site record and appears in the Monday briefing, but does not automatically trigger the homelessness integration," and does not describe a manual override path or reference standing emergency-outreach channels. This was an invented mitigation, not a description of the brief as written, and the Pass 2 grading report correctly caught it.)* As written, the brief has no specified manual-override mechanism for this delay. That is an open gap, not a mitigated one — see the corresponding Notes for Brief Revision item above, which recommends the brief either add an explicit manual-escalation path for the CRC Coordinator or accept the 2–3 cycle delay as a stated design tradeoff rather than an implicitly mitigated one.

---

## Citation Verification

*Every claim above that cites the source, the brief, or a reference doc gets one row. All page references below were checked directly against the primary 42-page source PDF (`research-library/incoming/17a/Reducing_Violent_Crime_17A.pdf`, now also ingested as `research-library/rag/17a-reducing-violent-crime-2026.jsonl`, 42 page-bounded chunks) — not against the markdown excerpt Pass 2 relied on. `Verified` is still left for a second human pass; this table records what an independent read of the primary source found, not a rubber stamp.*

| # | Claim (short label) | Appears in | Source | Page(s) | Verified |
|---|---|---|---|---|---|
| 1 | 3–5% of geography = 20% of violent crime, 9 cities | Aligned Findings #1 | 17a-reducing-violent-crime-2026 | p. 3 (confirmed exact); Appendix D detail pp. 27–29 | [ ] |
| 2 | Branas 29% / Chalfin 39% effect sizes | Aligned Findings #2 | 17a-reducing-violent-crime-2026 | p. 11 (confirmed exact) | [ ] |
| 3 | "Not a resource problem, a detection and coordination problem" | Aligned Findings #3 | 17a-reducing-violent-crime-2026 | p. 10 (confirmed exact quote), elaborated pp. 11–14 | [ ] |
| 4 | "Launch in 90 days... measurable outcomes within 180" | Aligned Findings #4 | 17a-reducing-violent-crime-2026 | p. 18 (confirmed exact; claim is about system launch, not visible repair) | [ ] |
| 5 | Four common pitfalls incl. one-time-campaign and cadence slippage | Aligned Findings #5 | 17a-reducing-violent-crime-2026 | p. 21 (confirmed; not explicitly ranked) | [ ] |
| 6 | 50–100 sites (Dallas ops list); "50 > 500" maxim; 20–30 half-mile tipping-point areas | Aligned Findings #6 | 17a-reducing-violent-crime-2026 | pp. 13, 15, 18 respectively (all confirmed, now correctly distinguished) | [ ] |
| 7 | Dallas is not an RCT; only middle tier statistically significant | Gaps #1 | 17a-reducing-violent-crime-2026 | p. 16; Appendix E.4 p. 31; Appendix F pp. 34–35 (all confirmed) | [ ] |
| 8 | Maintenance funding mechanism unspecified (absence claim) | Gaps #2 | 17a-reducing-violent-crime-2026 | Range searched: pp. 18–21 | [ ] |
| 9 | Federal role in coordination unaddressed (absence claim) | Gaps #3 | 17a-reducing-violent-crime-2026 | Range searched: whole document | [ ] |
| 10 | Dallas data-pull discrepancy, 22–25%, Appendix I recommendations | Gaps #4 | 17a-reducing-violent-crime-2026 | Appendix I, pp. 41–42 (confirmed) | [ ] |
| 11 | NCO is a by-right regulatory pathway, not a funding instrument | Gaps #5 | zoning-function-ladder; housing-public-infrastructure-system-overview | Rung 0–1; Section III | [ ] |
| 12 | Domain overview cites broader evidence base than brief's footnotes | Gaps #6 | housing-public-infrastructure-system-overview | Section VI | [ ] |
| 13 | 17A blends trend-classified (1–3%) and volume-ranked (14%) tiers on p. 16 | Gaps #7 | 17a-reducing-violent-crime-2026 | p. 16; Appendix G pp. 36–39; Appendix F pp. 34–35 (confirmed) | [ ] |
| 14 | "A third to half... different year to year"; corrected churn range | Divergences #1 | 17a-reducing-violent-crime-2026 | p. 3 (confirmed exact); Appendix D.3 p. 28 (confirmed table) | [ ] |
| 15 | North Buckner/Peavy Road case, unresolved | Divergences #2 | 17a-reducing-violent-crime-2026 | pp. 14–15 (confirmed; case is explicitly unresolved) | [ ] |
| 16 | Monday/Tuesday cadence, named explicitly | Divergences #3 | 17a-reducing-violent-crime-2026 | p. 13 (confirmed exact day-names) | [ ] |
| 17 | Chronic hotspots improving; 1–3% worsening cells vs. Next-30% significant tier | Open Questions #1 | 17a-reducing-violent-crime-2026 | pp. 9–10, 16; Appendix F pp. 34–35 (confirmed) | [ ] |
| 18 | "You don't need a predictive model..." quote | Decision 2 | 17a-reducing-violent-crime-2026 | p. 19 (confirmed exact) | [ ] |
| 19 | Buckner/Peavy case details for Decision 3 | Decision 3 | 17a-reducing-violent-crime-2026 | pp. 14–15 (confirmed; corrected from fabricated "resolved" claim) | [ ] |
| 20 | Brief has no stated manual-escalation path (absence claim) | Decision 4 | community-stabilization-framework | "Combined-Signal Sites," "CRC Structure" sections (checked directly against brief text) | [ ] |

*Rows 15 and 19 correct the confirmed fabrication the Pass 2 grading report identified. Row 14 corrects a statistic ("28–49%") that does not exist in the source in that form. Rows 4, 5, and 6 correct claims that overstated what the source demonstrates. Every row above was checked by direct extraction of the primary PDF in this pass, not inferred from a summary — a human reviewer should still spot-check a sample independently, but none of these citations rest on inference from a table of contents the way several Pass 2 rows did.*

---

## LLM Grading Status

*Pass 1 was graded 2026-08-04 against a pre-citation-verification draft (see `reviews/validation/community-stabilization-violence-research-review-grading.md`). Pass 2 was graded by that same report against the version with a Citation Verification table built from the markdown excerpt rather than the primary PDF; verdict was **Fail — re-run**, with specific, source-verified findings (a fabricated case-study resolution, a churn statistic not present in the source, several imprecise page citations, and missing appendix-level limitations). This Pass 3 corrects every item on that report's required-fixes list using the primary PDF directly, now also served through the project's restored RAG pipeline (`scripts/ingest-research.py` → `scripts/embed-research.py` → `scripts/query-research.py`). It has not yet been graded and should not be treated as validated until it is.*

| Item | Status |
|------|--------|
| Grading submitted | [ ] |
| Grading report filed | [ ] |
| Fidelity findings addressed | [x] — all 12 required fixes from the Pass 2 grading report addressed; see inline `[Pass 3]` / `[Pass 3, corrected]` markers throughout |
| Citation Verification rows checked off | [ ] — 20 rows, all re-derived from the primary PDF in this pass, pending independent human/second-model spot-check |
| `grading_status` YAML updated | [x] — set to pending |

*Until a fresh grading pass confirms this, this review should be treated as a corrected working draft, not a validated research receipt.*
