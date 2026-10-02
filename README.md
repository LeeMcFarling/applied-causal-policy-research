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

- **Stable IDs as primary keys.** Each `id` is unique across the corpus, and the `dependencies` field refers to other briefs by ID, so relationships between proposals behave like foreign keys in a database.

- **Phase Gating Maturity.** The machine readable nature of this setup allows us to set phase gates (has the healthcare domain been reviewed against case studies and research, have we worked out the logistics of how to implement this from day 1 - day 100, etc.).

When this is applied in concert with the document IDs and database dynamics stored above, we can map dependencies across the entire corpus (As a hypothetical example, 11 out of 16 healthcare domain documents are blocked until we validate a piece of technology they rely on in another domain).

- **Automated Checks.** These relationships can be tracked and enforced with python scripts. For example, [`tracker_check.py`](./scripts/tracker_check.py) verifies that every document ID is unique, every reference resolves to another document in the corpus (or a logged planned one), every phase respects its dependency caps, and every domain tracker agrees with the briefs it summarizes. [`maturity_scan.py`](./scripts/maturity_scan.py) rolls the metadata up by domain.

To go deeper on how this architecture works and how it can enable teams to work on their projects, visit [walkthrough](./walkthroughs/01-machine-readable-policy-architecture.md),  [YAML schema guide](./AI_Integrations/YAML_FRONTMATTER_GUIDE.md), and [sample domain tracker](./samples/Policy_Domains/Housing_and_Public_Infrastructure/_MATURITY_TRACKER.md) to get the specifics. 


## Part 2: RAG Pipeline with Cross-Provider Validation

When a solution to a problem is proposed, we need a structured way to evaluate whether it will fix the problem or not. While an independent expert review is the gold standard (and the phase gating of this platform prevents any document from maturing until such a review is reached), early drafts still need a structured method for evaluating whether a proposal is consistent with reaseach and existing case studies, or whether proposed policies contradict established facts. Large language models are good at processing a large amount of textual information at once (the kind of capability we'd need in this exercise) but they are also plagued by hallucinations, and innaccuracies. Worse, a model asked to check a proposal against the evidence can produce a review that *sounds* fluent and plausible, but contains innaccuracies that: cite made-up sources, incorrectly assume a source supports a claim when it does not, or contains information that is just plain wrong. 

For this pipeline, a Retrieval Augmented Generation (RAG) layer is made. A user sources articles, research, case studies, or similar policies that have been implemented in other countries and ingests this research into a structured pipeline. The text is extracted, chunked by page, and embedded in a vector store. This supplies a language model with a pre-processed library to reference any existing policies against, and when it's combined with strict rubrics, llm-as-judge checks, and human-in-the-loop confirmation we end up with a structured review of how each ingested research article compares to the policy proposal (where research aligns, where it diverges, and differences in scope between the two documents), with each claim tied back to a specific page in the source material. 

To ensure accuracy, a second model double checks everything in the review against a rubric that includes six categories (source material fidelity, policy brief fidelity, template compliance, citation accuracy, coverage, and adversarial rigor), and the process continues until a passing grade on all six categories is achieved.

### How Each Step Works

> Source PDF → page-bounded chunks → local embeddings → retrieval with page context → adversarial review (model A) → independent grading (model B, different provider) → human page-level verification → revised brief

1. **Ingest** ([`ingest-research.py`](./scripts/ingest-research.py)): extracts text from a PDF page by page with `pdfplumber`, collects citation metadata, and writes three artifacts: a byte-for-byte copy of the original, a human-readable extraction, and a JSONL file of chunk records. Each source is registered in [`index.yaml`](./research-library/index.yaml).
2. **Embed** ([`embed-research.py`](./scripts/embed-research.py)): embeds every chunk with a local `sentence-transformers` model (`BAAI/bge-large-en-v1.5` by default) and upserts it into a persistent Chroma vector store.
3. **Retrieve** ([`query-research.py`](./scripts/query-research.py)): embeds a query, finds the most relevant chunks, and expands each hit with its neighboring chunks, joined against `index.yaml` for full citation details.
4. **Review:** a model writes an adversarial review of the proposal using a fixed [review template](./research-library/reviews/_REVIEW_TEMPLATE.md). The review first defines what the source sets out to establish, then records aligned findings, gaps, divergences, and open questions, each tied to a page.
5. **Grade:** a model from a different provider audits the review against the source, the review, and the revised brief using a fixed [grading rubric](./research-library/reviews/validation/_GRADING_TEMPLATE.md): source fidelity, selective emphasis, framing neutrality, brief accuracy, and missing challenges. A failing review goes back for another pass.
6. **Verify:** a human opens the original PDF and checks every page-referenced claim before the review is marked complete. 

The output of this process is a review a human can trust for a pre-validation step, and policy revision with citations, page numbers, and a clear headed picture of where current literature supports the direction, where it's silent, and where review is needed. 


### A live Example: 

An example of a housing and urban development policy proposal is included, with a RAG adversarial review. The policy is reviewed against a 42-page guide to reducing violent crime including case studies in Dallas ([source record](./research-library/sources/17a-reducing-violent-crime-2026.md). That source was pre-processed and chunked according to page (with the records stored here: [chunked records](./research-library/rag/17a-reducing-violent-crime-2026.jsonl)). And the pre-validation process is conducted from start to finish against a community-stabilization policy  in three review passes:

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
