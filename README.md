# Machine-Readable Policy Corpus and RAG Validation Pipeline

**Large policy agendas are usually assempled from collections of standalone research, and then made to work together after the fact. And although they can be made to fit together, they often do not share a common architecture. Additionally, review depends heavily on people that can make a policy sound persuasive while there could be critical flaws in it underlying evidence base.** 

This repository takes the opposite approach: It treats policy systems as an integrated system built to work together from the ground up. And it uses this machine readable structure to automatically pull and review relevent research and use it to stress test any policy proposed. 


## Part 1: Machine-Readable Policy Architecture

The first part of this concept takes database concepts and applies it to each policy document themselves. Every brief has a stable ID, declares what it depends on, and carries a maturity phase that python scripts can automatically grade and verify. This helps an incoming government determine what their gaps and dependencies are between their own policy domains *as they are writing them*, as well as estimating how many people they will need, where, when, and why in order to accomplish their stated goals. 

Every brief is a markdown document that opens with YAML front matter based on the *Docusaurus* documentation standard that Meta developed along with Git based version control. This allows documents to declare what they depend on, makes versioning explicit (with audit trails), while allowing the entire policy corpus to be searched, iterated over, and AI enabled in order to allow database and software engineering functionality principles to apply to policy development. 

**As an overview:** Each document opens with a series of YAML fields that look like the following. These declare the document id (which is refered to in other docs), the domain, the subdomain, phase gates, versions (tracked in Git with line-by-line diff functionality of who changed what and when), as well as dependencies. 

Below is a simplified version of this 'front matter' 

```yaml
---
id: community-stabilization-framework
domain: housing-and-public-infrastructure
subdomain: Prevention_Layer
phase: 1  # capped by crisis-response-infrastructure; gate-met phase without cap: 3
version: 0.1
dependencies:
  - crisis-response-infrastructure
  - special-transit-zones
  - housing-supply-stabilization-overlay
---
```

- **'Primary Key' Logic.** Across the corpus, each document is given a 'primary key' like ID field, and this is used both as a unique identifier, and as a foreign key like connection to this document in other briefs. This enables us to connect multiple related policies together the way related fields are tied in a database. 

- **Phase Gating Maturity.** The machine readable nature of this setup allows us to set phase gates (has the healthcare domain been reviewed against case studies and research, have we worked out the logistics of how to implement this from day 1 - day 100, etc.).

When this is applied in concert with the document IDs and database dynamics stored above, we can map dependencies across the entire corpus (As a hypothetical example, 11 out of 16 healthcare domain documents are blocked until we validate a piece of technology they rely on in another domain).

- **Automated Checks.** These relationships can be enforced with python scripts and used to track the documents over time. For example, [`tracker_check.py`](./scripts/tracker_check.py) verifies that every document ID is unique, and that every connection between documents is correct. From there, these connections are used identify dependencies between documents, and this is rolled up into portfolio level mechanics for the entire corpus (i.e. "How is our healthcare domain doing?" through the, [`maturity_scan.py`](./scripts/maturity_scan.py) function. 

To go deeper on how this architecture works and how it can enable teams to work on their projects, visit [walkthrough](./walkthroughs/01-machine-readable-policy-architecture.md),  [YAML schema guide](./AI_Integrations/YAML_FRONTMATTER_GUIDE.md), and [sample domain tracker](./samples/Policy_Domains/Housing_and_Public_Infrastructure/_MATURITY_TRACKER.md) to get the specifics. 


## Part 2: RAG Pipeline with Cross-Provider Validation

When a solution to a problem is proposed, we need a structured way to evaluate whether it will fix the problem or not. While an independent expert review is the gold standard (and the phase gating of this platform prevents any document from maturing until such a review is reached), early drafts still need a structured method for evaluating whether a proposal is consistent with research and existing case studies, or whether proposed policies contradict established facts. Large language models are good at processing a large amount of textual information at once (the kind of capability we'd need in this exercise) but they are also plagued by hallucinations, and inaccuracies. Specific pitfalls that we need to avoid are: citing made-up sources, incorrectly stating that a source supports a claim when it actually doesn't, or citing 'facts' that are just plain incorrect. 

Therefore, in order to ensure accuracy, we retrofitted a Retrieval Augmented Generation (RAG) pipeline into a red-team analysis. This works by feeding a collection of research, case studies and precedents into a folder. From there, the text is extracted, chunked and embedded into a vector store where it acts as a library for a model to cross-reference. 

We then tell that model to conduct a red-team analysis of our policies using Chicago style citations and page numbers for each claim, and use an LLM-as-judge framework to grade the outcome and iterate until a passing grade is received. 

The outcome is a list of everywhere where your policy aligns with established research, where it diverges (where the research does not support your claims), where the gaps are (does the research support our diagnosis, but not our prescription, for example?), scope differences (has research only supported this mechanism in a city-sized-scale while we are proposing to roll it up nationwide?), and remaining open questions (i.e. Do we need to find more research before this step is complete?).

### How Each Step Works

The pipeline broadly follows this pathway: 

> Source PDF → page-bounded chunks → local embeddings → retrieval with page context → adversarial review (model A) → independent grading (model B, different provider) → human page-level verification → revised brief

1. **Ingest:** The first step, ([`ingest-research.py`](./scripts/ingest-research.py)), extracts the original text from a PDF page by page with `pdfplumber`, collects citation metadata, and writes three documents: a byte-for-byte copy of the original, a human-readable extraction, and a JSONL file of chunk records. Each of these sources is registered in [`index.yaml`](./research-library/index.yaml).
2. **Embed:** From there, ([`embed-research.py`](./scripts/embed-research.py)) embeds every chunk with a local `sentence-transformers` model, and store in a Chroma vector model. We used (`BAAI/bge-large-en-v1.5`) here by default because it's a small model that we can deploy locally, uses fewer tokens, so we don't have to deal with any API costs.  
3. **Retrieve:** Then we build out a query engine with ([`query-research.py`](./scripts/query-research.py)) to navigate the library, find the relevant 'chunks', and use our index for a full citation details.
4. **Review:** From there, a model writes an adversarial review of the proposal a pre-coordinated [review template](./research-library/reviews/_REVIEW_TEMPLATE.md), which sets up our grading process for the LLM-as-judge framework. 
5. **LLM-as-Judge:** Next, a model from a different provider audits the review against it's sources (research and the drafted policy proposal), and the review template, using a set  [grading rubric](./research-library/reviews/validation/_GRADING_TEMPLATE.md). The review is graded for fidelity and other metrics, and a failing review is fed back into the system for another pass.
6. **Verify:** Once the process is complete, it generates an output review where every claim has a page level citation. Here we can look up and verify each citation is accurate, and then ready through the review and the grading passes, and re-appraoch our policy accordingly.  


### A live Example: 

As a live example of this process in action, a housing and urban development policy proposal is included, with a RAG adversarial review. The policy is reviewed against a 42-page guide to reducing violent crime including case studies in Dallas ([source record](./research-library/sources/17a-reducing-violent-crime-2026.md). That source was pre-processed and chunked according to page (with the records stored here: [chunked records](./research-library/rag/17a-reducing-violent-crime-2026.jsonl)). And the pre-validation process is conducted from start to finish against a community-stabilization policy  in three review passes:

| Pass | What happened | Grade |
|---|---|---|
| **1** | Initial review, written before page-level citation checks existed. | Graded; superseded |
| **2** | A citation-verification table was added, but every page reference was built from a short markdown excerpt of the source rather than the full 42-page PDF. | **Fail: re-run.** The grader, checking against the primary PDF, caught page and statistic errors and a fabricated claim: the review said a case study was "resolved through sustained code enforcement," when the source (p. 15) reports it unresolved. |
| **3** | Retrieval was rebuilt around page-bounded chunks of the full PDF, and the review was re-verified against the primary document. | **Pass with revisions** |

That second pass is the reason the validation chain exists. The review was fluent, well-structured, and wrong in ways that only a check against the primary source could catch.

The full evidence chain:

1. [Adversarial research review](./research-library/reviews/community-stabilization-violence-research-review.md) (authored by Claude Sonnet 5), including its pass history and decision log.
2. [Independent grading report](./research-library/reviews/validation/community-stabilization-violence-research-review-grading.md) (graded by an OpenAI GPT-5-family model).
3. [Revised policy brief](./samples/Policy_Domains/Housing_and_Public_Infrastructure/community-stabilization-framework.md) incorporating the review's findings.

For a narrative walkthrough of the same example, see [Research Integration and Adversarial Revision](./walkthroughs/02-research-integration-and-adversarial-revision.md).

>**As a heavy note:** As stated in part one, briefs are designed to work together, in this case, a single community stabilization is reviewed, but the policy platform it was pulled from contains homelessness stabilization domains, a criminal justice domain, and a broader housing and urban development domain, and redesigned federal government instututions (EC and DoDa, etc.). The review rightfully flags that the community stabilization brief connects to these documents but this repo doesn't contain them. A true grading pass would target and pull in additional reasearch to validate these additional pieces as well, by design. **In order to avoid dumping 50+ pages of extra policy material that is secondary to the RAG pipeline demonstration, they are not included here.**


## Quick Start

```bash
pip install pdfplumber sentence-transformers chromadb ruamel.yaml

# 1. Ingest a PDF (prompts for citation metadata)
python3 scripts/ingest-research.py research-library/incoming/report.pdf --key author-topic-2026

# 2. Embed it
python3 scripts/embed-research.py --key author-topic-2026

# 3. Retrieve evidence for a question, with surrounding page context
python3 scripts/query-research.py "vacant lot greening and violent crime" --top-k 8 --radius 1
```

The review and grading steps are run with the templates in `research-library/reviews/`; see [`AUTOMATION_README.md`](./AI_Integrations/AUTOMATION_README.md) for the full workflow, including the grading prompt and the human sign-off procedure.

## Repository Map

```text
scripts/
  ingest-research.py     PDF → page-bounded chunks, source record, index entry
  embed-research.py      chunks → local embeddings → Chroma vector store
  query-research.py      query → ranked chunks with page context and citations
  research_lib.py        shared paths, I/O, and model/collection naming
research-library/
  originals/             byte-for-byte source PDFs
  sources/               human-readable extractions
  rag/                   canonical chunk records (JSONL)
  vector-store/          local Chroma store
  reviews/               adversarial reviews and the review template
  reviews/validation/    cross-provider grading reports and the grading rubric
  index.yaml             source catalog and pipeline status
  tracker_check.py       corpus integrity and phase-cap verification
  maturity_scan.py       domain-level maturity roll-up
samples/                 sample briefs and domain trackers
walkthroughs/            narrative walkthroughs of both parts
AI_Integrations/         schema and workflow documentation
```

## Scope

Both tools were developed as part of a larger, private policy-research project, and the policy examples are illustrative. Some dependency IDs in the sample briefs point to briefs that are not public, and the integrity scripts expect the full private directory tree. The repository is about the method: making a large body of documents structurally verifiable, and making AI-assisted research reviews traceable, independently graded, and checkable against their sources.
