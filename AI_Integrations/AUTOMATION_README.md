# Policy Maturity Tracking Automation

This system automates policy domain tracking and gap analysis for the policy platform.

## Overview

The automation consists of:
1. **Maturity Tracker Template** - Standardized tracking document for each domain
2. **Automation Script** - Python script to scan repo and update trackers
3. **YAML Front Matter** - Metadata standard for all policy files

## File Structure

```
repo/
├── docs/
│   ├── Climate_and_Energy/
│   │   ├── _MATURITY_TRACKER.md          # Auto-generated tracker
│   │   ├── Decarbonization.md             # Policy file
│   │   └── Grid_Modernization.md          # Policy file
│   ├── Healthcare/
│   │   ├── _MATURITY_TRACKER.md
│   │   └── [policy files...]
│   └── [other domains...]
├── PROJECT_STATUS.md                       # Overall project status (auto-generated)
├── maturity_scan.py                        # Automation script
└── MATURITY_TRACKER_TEMPLATE.md           # Template for new domains
```

## YAML Front Matter Standard

Every policy markdown file should include this front matter:

```yaml
---
domain: Climate_and_Energy
subdomain: Decarbonization
phase: 2
dependencies:
  - type: hard
    target: Budget.Carbon_Revenue
    reason: Need revenue mechanism for carbon pricing
  - type: soft
    target: Public_Infrastructure.Grid
    reason: Coordination on grid upgrades
status: in_progress
last_updated: 2025-01-25
author: [optional]
---
```

### Front Matter Fields

- **domain**: Top-level policy domain (matches directory name)
- **subdomain**: Specific area within domain
- **phase**: Current phase (0-8) following the Phase Model
- **dependencies**: Array of dependencies with type (hard/soft/optional), target, and reason
- **status**: `draft`, `in_progress`, `review`, `complete`
- **last_updated**: Date of last significant update
- **author**: (Optional) Who's working on this

## Commands for Claude Code

### 1. Scan All Domains and Update Trackers

```bash
python maturity_scan.py scan
```

This will:
- Scan all domain directories
- Count files and words per subdomain
- Extract phase information from front matter
- Update `_MATURITY_TRACKER.md` in each domain
- Generate `PROJECT_STATUS.md` with overall status

### 2. Generate Project Status Report

```bash
python maturity_scan.py report
```

Creates a comprehensive status report showing:
- Total domains, files, and words
- Phase distribution
- Links to all domain trackers

### 3. Analyze Gaps

```bash
python maturity_scan.py gaps
```

Outputs gap analysis in three tiers:
- **Tier 1**: Missing domains (no files)
- **Tier 2**: Skeletal domains (1-2 files or <1000 words)
- **Tier 3**: Domains that could expand (<5000 words)

### 4. Validate Phase Discipline

```bash
python maturity_scan.py validate
```

(Coming soon) - Will check for:
- Phase violations (files claiming higher phase than dependencies)
- Missing required elements for phase advancement
- Dependency conflicts

## Typical Claude Code Workflow

When asked to "scan the repo for gaps":

1. Run: `python maturity_scan.py scan`
2. Read the generated `PROJECT_STATUS.md`
3. Run: `python maturity_scan.py gaps`
4. Summarize findings in tier format
5. Recommend priority domains based on analysis

When asked to "update maturity trackers":

1. Run: `python maturity_scan.py scan`
2. Confirm updates were successful
3. Report any new gaps or phase changes

When creating a new domain:

1. Create domain directory: `mkdir docs/New_Domain`
2. Copy template: `cp MATURITY_TRACKER_TEMPLATE.md docs/New_Domain/_MATURITY_TRACKER.md`
3. Edit template to fill in domain-specific information
4. Create first policy file with proper front matter
5. Run: `python maturity_scan.py scan`

## Automation Capabilities

The script automatically:

- ✅ Counts files per subdomain
- ✅ Counts total words (excluding front matter)
- ✅ Extracts phase from front matter
- ✅ Identifies dependencies
- ✅ Calculates overall domain phase (minimum across subdomains)
- ✅ Flags gaps (no files, minimal content)
- ✅ Preserves manual notes in trackers
- ✅ Generates project-wide status report

## What Claude Code Should Do

**When scanning:**
- Run the automation script
- Read generated reports
- Summarize findings in user-friendly format
- Highlight priority gaps

**When asked about a specific domain:**
- Navigate to domain directory
- Read `_MATURITY_TRACKER.md`
- Check actual policy files for detail
- Report status and recommend next actions

**When creating new content:**
- Ensure proper YAML front matter
- Run scan after creation to update trackers
- Check for phase violations

## Integration with User Workflow

1. **User works** to research and draft policy content
2. **User commits new markdown files** to repo with proper front matter
3. **User asks Claude Code** to "scan for updates"
4. **Claude Code runs** `maturity_scan.py scan`
5. **Claude Code reports** new status and any gaps
6. **User returns** for next research/writing task

## Configuration

Edit these variables in `maturity_scan.py` to match your repo structure:

```python
REPO_ROOT = Path(".")  # Adjust to your repo root
DOMAINS_DIR = REPO_ROOT / "docs"  # Adjust to where your policy domains are
TRACKER_FILENAME = "_MATURITY_TRACKER.md"
PROJECT_STATUS_FILE = REPO_ROOT / "PROJECT_STATUS.md"
```

---

## PDF Export

Policy briefs can be exported directly to print-quality PDFs using the scripts in `scripts/`.

### Export a single brief

```bash
python3 scripts/export-brief.py guiding-principles/Policy_Domains/Healthcare/care-delivery-market-design.md
```

Output defaults to the same location as the source file (`brief-name.pdf`). Override with `-o`:

```bash
python3 scripts/export-brief.py path/to/brief.md -o exports/brief.pdf --open
```

### Batch export a domain

```bash
python3 scripts/export-domain.py Healthcare
python3 scripts/export-domain.py Budget_and_Fiscal_Policy --phase 4 -o exports/
python3 scripts/export-domain.py --all --phase 2
```

`--phase N` filters to briefs at phase N or above. Output lands in `exports/<domain>/` by default.

### How it works

- **YAML**: Docusaurus-specific fields (`slug`, `sidebar_*`, `id`) are stripped before pandoc sees the file. `last_updated` maps to `date`. `description` renders as a shaded abstract block on the cover page.
- **SVG figures**: Converted to PNG via Chrome headless at export time. Original SVG is untouched.
- **HTML figures**: The script looks for a companion `.png` next to the `.html` file and swaps it in for print. If no PNG exists, it inserts a bracketed note pointing to the interactive version.
- **Chicago citations**: Use markdown footnote syntax — `[^1]` inline, `[^1]: Author, *Title*, etc.` at the bottom of the file. Pandoc renders these as proper footnotes; no separate bibliography file needed.

### Figure conventions

```
Policy_Domains/
  Healthcare/
    assets/
      sec-market-architecture.svg     ← reference as ./assets/sec-market-architecture.svg
      revenue-flow-interactive.html   ← web-only interactive figure
      revenue-flow-interactive.png    ← companion for PDF export
```

### Unlock full typographic template

The template degrades gracefully on a basic TeX Live install. For headers, section rules, and Chicago-style footnote formatting, install the full package set:

```bash
sudo tlmgr install titlesec mdframed footmisc booktabs caption setspace fancyhdr enumitem microtype
```

No other changes needed — the template auto-detects and enables the packages.

### Requirements

- pandoc (`brew install pandoc` if missing)
- xelatex (included with MacTeX — `brew install --cask mactex-no-gui` for full package support)
- Google Chrome (already installed; used for SVG and HTML figure rendering)

---

## Phase 3: Research Integration

Phase 3 is the process of reviewing existing literature against platform briefs. The output is two things:
1. **Inline citations** in briefs for specific empirical claims (Chicago footnotes, page-level)
2. **Review documents** in `research-library/reviews/` that serve as adversarial receipts — showing exactly how the platform engages the independent research

### Ingest a source document

Drop PDFs in `research-library/incoming/`, then run:

```bash
python3 scripts/ingest-research.py research-library/incoming/rand-report.pdf
```

The script will:
- Extract text from the PDF using pdfplumber
- Prompt for citation metadata (authors, title, institution, year, URL, topics)
- Generate a Chicago citation string
- Write `research-library/sources/<citation-key>.md` with a YAML header and the full extracted text
- Add the source to `research-library/index.md`

To specify a citation key explicitly:

```bash
python3 scripts/ingest-research.py research-library/incoming/report.pdf --key rand-superannuation-2023
```

### Run a Phase 3 review pass

After ingesting, give Claude the source file and the relevant platform brief(s) and ask for a review using the standard template:

> "Review `research-library/sources/rand-superannuation-2023.md` against the superannuation brief. Use the review template at `research-library/reviews/_REVIEW_TEMPLATE.md`. Save the output to `research-library/reviews/superannuation-research-review.md`."

**Important scoping principle:** Not every source will be a 1:1 match to a single platform brief, and no source is expected to validate everything platform proposes. Before writing the Aligned Findings, Gaps, and Divergences sections, complete the `## Source Scope` section first. This defines what the source is and isn't attempting — and the rest of the review is evaluated relative to that, not relative to the totality of what the platform needs.

A source being silent on third spaces, coordination models, homelessness mitigation, federal implementation design, or long-term social outcomes is expected and normal if those topics are outside its scope. List out-of-scope topics in Source Scope and exclude them from Gaps. Only topics within the source's stated scope that remain unaddressed belong in Gaps.

Use the template at `research-library/reviews/_REVIEW_TEMPLATE.md` as the output format.

### Add inline citations to briefs

After the review, update the brief with Chicago footnotes for specific claims:

```markdown
Retirement assets in Australia's superannuation system grew to AU$3.5 trillion by 2023.[^1]

[^1]: Grattan Institute. *Super Savings: Foundational Principles of Superannuation*. Melbourne: Grattan Institute, 2023. https://grattan.edu.au/report/super-savings/.
```

Add the brief slug to the source's `briefs:` field and mark `phase-3-review:` with the review file path.

### Research library structure

```
research-library/
  incoming/          ← drop zone for PDFs before ingestion
  sources/           ← ingested sources, one .md per document
  reviews/           ← topic-based review documents (adversarial receipts)
  reviews/validation/← LLM grading reports (one per review, different LLM family)
  index.md           ← catalog: sources → briefs → reviews
```

---

## Phase 3.5: Independent Fidelity and Balance Audit

After each Phase 3 review is complete, the review undergoes a grading pass using a **separate LLM from a different provider or model family** than the one that produced the review. This step exists to answer the question that will arise during expert review: *"How do you know the AI-assisted research integration isn't just confirming the author's priors?"*

The policy platform was written and drafted according to a specific worldview. An AI assistant working within that framing — trained on the project's own materials and guided by the author's framing throughout — can develop systematic blind spots that mirror the author's priors. This is not a failure of the AI; it is a structural feature of any tool used within a closed epistemic loop. The grading step introduces an independent reviewer into that loop — not to eliminate interpretive assumptions (no model is free of them) but to surface the cases where two independent reviewers, operating from different priors, arrive at the same concern.

### What to submit to the grading LLM

Provide the grading LLM with all three of the following in a single prompt:
1. **The original source** — full extracted text from the ingested PDF (from `research-library/sources/<key>.md`)
2. **The research review document** — the four-section review from `research-library/reviews/`
3. **The edited brief** — the post-review version of the relevant platform brief(s)

### Grading prompt

```
You are performing an independent fidelity and balance audit of a policy research review. Your task is to evaluate whether the review and subsequent brief edits accurately represent the source material — not to assess whether the underlying policy is correct.

Before evaluating anything else, read the `## Source Scope` section of the review. The review is evaluated relative to the source's stated scope, not relative to the totality of what the policy platform needs. A source being silent on topics outside its stated scope is expected. Do not flag out-of-scope silences as omissions or missing challenges.

Specifically, identify:

1. SOURCE FIDELITY — Does the review accurately represent what the source says? Flag any place where the review overstates, understates, or mischaracterizes a finding.

2. SELECTIVE EMPHASIS — Are there findings in the source that the review omitted or minimized that would challenge the policy brief's position? List them.

3. FRAMING NEUTRALITY — In the "Divergences" section, the review describes tensions between the source and the platform position. Does the "platform position" framing appear to genuinely engage with the tension, or to rationalize a pre-determined conclusion? Flag cases where the rationalization appears weak relative to the source evidence.

4. BRIEF ACCURACY — Do the edits made to the policy brief accurately implement what the research review recommends? Flag any cases where the brief appears to have adopted a finding selectively or partially.

5. MISSING CHALLENGES — What challenges to the policy brief's position does the source raise that neither the review nor the brief addresses at all?

Do not evaluate whether the policy is good. Only evaluate whether the review and brief edits are accurate and balanced representations of what the source says and implies.
```

### Output format

Save the grading report to `research-library/reviews/validation/<review-name>-grading.md` using this structure:

```markdown
---
review: [review filename]
grading-model: [model used, e.g. "GPT-4o" or "Gemini 1.5 Pro"]
grading-date: YYYY-MM-DD
---

## Source Fidelity
[findings]

## Selective Emphasis
[findings]

## Framing Neutrality
[findings]

## Brief Accuracy
[findings]

## Missing Challenges
[findings]

## Summary Assessment
[1-paragraph overall judgment]
```

Update the review document's `grading_status:` YAML field to `complete` once the report is filed. If a grading pass is deliberately waived (e.g., the source is supplementary and low-stakes), set `grading_status: waived-with-rationale` and add a one-sentence explanation in the review's YAML.

### Why a different LLM family?

Different model families have different training data, reinforcement learning objectives, and systematic reasoning tendencies. Running the grading pass with a different model family reduces the likelihood that the same interpretive assumptions or blind spots are reproduced across both stages.

The purpose of this pass is not to determine which policy position is "correct." Instead, it independently evaluates whether:

- the research review accurately represents the source material;
- the edited policy brief faithfully implements the review's recommendations;
- important contrary findings have been omitted or minimized; and
- points of disagreement between the source and the policy platform are represented fairly rather than rationalized.

Disagreement between model families is treated as a useful signal for human review rather than an error requiring automatic resolution. Where multiple independent reviewers identify the same concern, confidence that the issue warrants manual examination increases. Where reviewers disagree, the disagreement itself becomes part of the project's documented research record.

Accordingly, the grading pass should be understood as an **independent fidelity and balance audit**, not as a validation of the underlying policy proposal.

The grading report is advisory rather than authoritative. Its purpose is to surface potential misrepresentations, omissions, or framing issues for human consideration. Final editorial judgment remains with the project author, who may accept, reject, or partially incorporate the recommendations with documented rationale.

---

## Requirements

```bash
pip install pyyaml pdfplumber
```

## Notes

- The automation **preserves manual notes** added to trackers below the auto-generated sections
- Domain phase is calculated as **minimum phase across all subdomains** (conservative approach)
- Empty directories are flagged as Phase 0
- The script is **idempotent** - safe to run multiple times
