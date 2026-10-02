# Research Library Index

This library contains one complete source-to-review chain: a single research source, ingested and embedded through the RAG pipeline, reviewed against a policy brief, and independently graded by a model from a different provider. Machine-readable metadata for the source lives in [`index.yaml`](./index.yaml).

---

## How to use this library

1. **Ingest a source:** `python3 scripts/ingest-research.py research-library/incoming/report.pdf`
2. **Embed it:** `python3 scripts/embed-research.py --key <citation-key>`
3. **Retrieve evidence:** `python3 scripts/query-research.py "your question" --top-k 8`
4. **Run a review:** Provide a model with the retrieved source passages and the brief(s); follow `reviews/_REVIEW_TEMPLATE.md`, including page references on every cited claim and a completed Citation Verification table; save to `reviews/<topic>-research-review.md`
5. **Grade the review:** Provide a model from a different provider with the review, the source, and the brief(s); follow `reviews/validation/_GRADING_TEMPLATE.md` to grade the review's *fidelity* to that material (not the quality of the brief or the literature, which is the review's own job); save to `reviews/validation/<topic>-research-review-grading.md`
6. **Verify by hand:** Once the graded review is accepted, check every page-referenced claim against the original PDF and read through the full review before marking it complete
7. **Cite inline:** Add page-level Chicago footnotes to the brief for specific claims, and record the brief and review in the source's `index.yaml` entry

---

## Source

- [17a-reducing-violent-crime-2026](./sources/17a-reducing-violent-crime-2026.md) — Eichenbaum, Joe. *Reducing Violent Crime Without New Budget, New Staff, or More Arrests: A Pragmatic Guide for City Leaders*. New York: 17A, 2026. (42 pp.)

---

## Review

| Topic | Source | Briefs | Status |
|-------|--------|--------|--------|
| [Community Stabilization & Environmental Violence Reduction](./reviews/community-stabilization-violence-research-review.md) | 17a-reducing-violent-crime-2026 | community-stabilization-framework · violence-interruption · homelessness-prevention · built-environment-community-anchors · land-use-stabilization | Pass 3 graded **Pass with revisions** (2026-09-16); human page-level verification pending. Pass 2 was graded **Fail — re-run** after the grader caught a fabricated claim and several citation errors. See the [grading report](./reviews/validation/community-stabilization-violence-research-review-grading.md). |
