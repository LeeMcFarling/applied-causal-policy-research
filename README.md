# Applied Causal Policy Research Architecture

**Policy proposals and regulations are usually written as standalone documents. What becomes possible when we treat them more like code instead? Connected, testable, and revisable parts of a larger system? More technically, this repository demonstrates a machine-readable policy-development architecture linking dependency analysis, adversarial research review, causal evaluation, and administrative workflow modeling.**


| Capability | The question it answers | Guided walkthrough |
|---|---|---|
| **Machine-readable architecture** | *What is our climate policy missing? Are there dependencies from manufacturing, trade, or finance we haven't caught that will sink this energy policy?* | [Architecture](./walkthroughs/01-machine-readable-policy-architecture.md) |
| **Adversarial research integration** | *How does our housing policy compare with the relevant research from think tanks, universities, and policy organizations? Where are the strongest gaps and deviations?* | [Research integration](./walkthroughs/02-research-integration-and-adversarial-revision.md) |
| **Causal evaluation by design** | *Can a policy carry its own evaluation architecture from day one—producing the comparisons and evidence needed to decide whether it should scale, change, or stop?* | [Causal evaluation](./walkthroughs/03-causal-evaluation-inside-policy-design.md) |
| **GovOps** | *What are the exact word-for-word regulatory differences in housing policy across all 50 states? What are the operational workflow differences that result? How can we see these differences in a real-time dashboard? What regulatory landscape leads to the fastest, cheapest, and *safest* results?* | [Process-legible law](./walkthroughs/04-govops-and-process-legible-law.md) |


> **Note: The policy examples above are illustrative.** These methods were developed and operationalized against a larger private policy corpus. This repository includes selected artifacts that allow readers to inspect the architecture without requiring them to navigate—or agree with—the source platform's substantive political positions.

The policy examples are therefore illustrative. The reusable product is the methodology, not the particular housing, wage, or regulatory positions contained in the samples. A future team would use the architecture to develop its own priorities, safeguards, implementation choices, and final recommendations.

## A 90-Second Tour

1. **See the system:** Open the [architecture reference](./ARCHITECTURE.md) to see how Markdown briefs become linked policy objects through YAML metadata, stable IDs, dependencies, audience tags, and phase gates.
2. **See the portfolio view:** Scan the [sample project status report](./PROJECT_STATUS.md) to see how the architectural structure enables maturity matrices and gap analysis.
3. **See evidence change a policy:** Follow one source through an [adversarial review](./research-library/reviews/community-stabilization-violence-research-review.md), an [independent grading receipt](./research-library/reviews/validation/community-stabilization-violence-research-review-grading.md), and the [revised brief](./samples/Policy_Domains/Housing_and_Public_Infrastructure/community-stabilization-framework.md).
4. **See evaluation written into policy:** Open the [regional wage pilot](./samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md) and jump to “Econometric Evaluation” and “Evaluation Gates.”
5. **See law mapped to operations:** Browse the [rendered GovOps brief](./samples/Operating-System/GovOps-RMC-tech-layer.pdf) for the legal/workflow schema, cross-jurisdictional comparison, and regulatory sandbox design.

For a narrative introduction, start with the [four walkthroughs](./walkthroughs/README.md). For implementation detail, follow their links into the underlying metadata, briefs, research receipts, trackers, scripts, and figures.

## Why This Exists

Hyperscale organizations routinely manage production platforms that host billions of people, comprise hundreds of millions of lines of code, and are managed by thousands of engineers working simultaneously across the world. These platforms sit on top of hundreds of billions of dollars' worth of infrastructure and must continuously improve their operations, production models, and other systems while remaining in production for billions of users every minute of every day.

The methodologies that these hyperscalers use to do this are virtually identical across Amazon, Microsoft, Google, Meta, and other hyperscale organizations: version control, structured review, dependency management, staged deployment, observability, controlled experimentation, and continuous revision. When I became interested in government reform, however, I was struck by how absent these systems were in government. 

Government policy -- be that laws, regulations, procedures, and so on -- functions like civilizational software. If you want to build a house, you follow a sequential set of building instructions specified via law. If you want to start a business, you follow a different procedure, according to statute. But unlike the software companies specified earlier, the government does not have the tools to manage this complexity.

Policies get drafted, debated, and enacted as one-off documents with no dependency graphs, no staged rollouts, no observability, and no structured mechanism for revising it once evidence comes in. Great policies get implemented in Dallas, but there is no automatic notification or scaling mechanism for rolling them out in other areas once they prove successful. Likewise, bad policies get implemented without a structured method for testing and rolling them back if they are unsuccessful at meeting their stated goals. 

This project asks a bounded question:

> Which of those disciplines can be adapted to public policy while preserving due process, democratic authorization, legal accountability, and human judgment?

This project therefore explores whether methodologies that emerged in hyperscale engineering organizations to manage complexity — version control, dependency management, peer review, staged deployment, experimentation, and observability — can be adapted into a continuously learning system for public policy. Note: It does **not** argue that government should operate like a technology company. The analogy is useful only where it improves legibility, learning, and accountability without displacing public values or lawful authority.

## What the Four Examples Demonstrate

### 1. A Machine-Readable Platform Architecture

> How can hundreds of text-based policies (or laws, regulations, etc.) be maintained as a single coherent, queryable, and auditable system rather than a collection of disconnected papers? 

The architecture section demonstrates this capability -- walking through how YAML front matter adapted from Docusaurus documentation standards can be applied to public policy to enable gap and dependency analysis, adversarial research review, project and development maturity tracking (through phase-gating), and so on. 

- [Architecture reference](./ARCHITECTURE.md) — Documents how this machine-readable system is applied to policy briefs and how the architecture of a policy platform can enable the analysis described earlier. 
- [Project status](./PROJECT_STATUS.md) — This document shows an example output from a policy platform when the architecture is applied and the resulting system is used to generate a status report. It contains sample maturity matrices, gap analysis, and cross-domain status.
- [YAML front-matter guide](./AI_Integrations/YAML_FRONTMATTER_GUIDE.md) — An example of how to use the YAML machine-readable schema to track and add metadata to a policy platform. 
- [Housing domain overview](./samples/Policy_Domains/Housing_and_Public_Infrastructure/overview-housing-and-urban-architecture.md) — This document serves as a worked example of how this system is used in practice within a sample policy domain. 
- [Housing maturity tracker](./samples/Policy_Domains/Housing_and_Public_Infrastructure/_MATURITY_TRACKER.md) — This document serves as an example of how the system described earlier can integrate multiple housing policy briefs to answer questions like: "What gaps exist in our housing policies? Which documents still need to be validated with research? How mature is this domain within our policy stack?" The results of this tracker are then used to integrate multiple policy domains (e.g., Healthcare, Housing, Fiscal Policy) into a project-wide status document detailed earlier. 

**Note:** Stable IDs function as foreign keys; briefs declare hard dependencies and related instruments; audience tags support targeted views; phase gates constrain sequencing; and maturity trackers expose gaps across the larger system.

### 2. Research integration and Adversarial Review

> How do we use modern technology to stress-test our policy proposals against research from think tanks, policy organizations, universities, and other organizations before the platform goes public? 

The idea here is that every policy platform in recent memory is met with skepticism from at least one organization or nationwide stakeholder. This demonstration shows how research can be ingested ahead of time to distinguish what is a genuine critique that necessitates a change to the underlying policy architecture, and what can be rebutted. 

This section therefore contains a folder into which an organization can drop PDF files for studies, research, case studies, meta-analyses, and so on. From there (when prompted), the platform strips out the text from those documents for analysis and uses that text for an adversarial review against one or more documents in the platform itself. 

This adversarial review generates a file that documents the differences in scope between the policies being reviewed and the research being used to stress-test them. From there, it distinguishes alignment, gaps, divergences, and open questions (with page numbers) that can be used in the adversarial review. 

From there, the review, the adversarial research, and the underlying policy-platform documents are used to generate an independent grading receipt (from a different model, from a different provider) indicating whether the adversarial review passes or fails (and subsequently needs a second pass with updated instructions). 

When complete, the process ends with a documented step-by-step analysis, the adversarial review of the policy corpus, and a decision log from the user documenting which critiques are rebutted and why, along with which changes to the underlying infrastructure were necessitated.

**The included documents demonstrate an evidence chain:**

1. [Ingested 17A source record](./research-library/sources/17a-reducing-violent-crime-2026.md) - A sample case study ingested from a leading government consulting and technology firm. The case study is used for an adversarial review of a community stabilization framework from the 'Housing and Urban Infrastructure' domain. 
2. [Adversarial research review](./research-library/reviews/community-stabilization-violence-research-review.md) - The adversarial research review generated by the process, including a documented decision log that resulted from the analysis and the final grade from the independent grading receipt. 
3. [Independent grading receipt](./research-library/reviews/validation/community-stabilization-violence-research-review-grading.md) - The independent grading receipt generated from the review. 
4. [Revised community-stabilization brief](./samples/Policy_Domains/Housing_and_Public_Infrastructure/community-stabilization-framework.md) - The final policy document that incorporates the advice from the adversarial review. Because Git - Version Control technology is used, this is incorporated with a diff showing a line-by-line before and after of the review, with metadata including the user who made the changes and timestamps. 

The initial research review is audited in a separate pass by a model from a different provider. The second model applies a standardized rubric maintained by the automation workflow and produces a grading receipt for human review. This separation helps surface source-fidelity, inferential, and framing problems; it does not eliminate correlated model errors or substitute for independent expert assessment.

The important artifact is the chain of custody from evidence to design—not a claim that one source validates the whole proposal:

> Source → First-model adversarial review → Cross-provider rubric audit → Human decision record → Brief revision

### 3. Causal evaluation inside policy design

> How do we build causal analysis directly into policy design itself? 

The [regional wage pilot](./samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md) demonstrates how a proposal can define its learning architecture before implementation: a bounded intervention, treatment and comparison regions, pre-specified measures, independent research review, evidence gates, and paths to scale, revise, pause, or stop.

The wage policy itself is an example. The reusable idea is to decide how a policy will generate credible evidence before asking the public to live with it at scale.

The architecture enables the evaluation workflow; implementation would still require appropriate authority, viable comparison units, sufficient statistical power, administrative data, ethical safeguards, and human adjudication.

### 4. GovOps and process-legible law

**Question demonstrated:** Can law and regulation be represented in terms of both legal authority and the administrative processes they create?

This demonstration takes the same concepts introduced above -- whether version control, causal analysis, experimental design, legibility, etc. -- and applies them to government regulatory architecture. It documents how legal text documents can be tied digitally to the processes they create, how the regulatory landscape can be compared across jurisdictions in the country, and how this legal text can be optimized to produce a maximally efficient regulatory landscape in terms of both protective outcomes and permitting throughput. 

**Start here:** [GovOps technical brief](./samples/Operating-System/govops-rmc-tech-layer.md) or the [rendered PDF](./samples/Operating-System/GovOps-RMC-tech-layer.pdf)

**What to notice:** The dual-schema architecture connects legal clauses to workflow steps, compares implementations across jurisdictions, instruments administrative timelines, and uses controlled sandboxes to search for designs that preserve protective outcomes while reducing avoidable process time.


## What Is Included—and What Is Not

This public extract contains enough material to:

- inspect the machine-readable schema and dependency model;
- examine sample maturity and gap-analysis outputs;
- trace one research-to-revision cycle;
- review one causally designed pilot; and
- inspect one GovOps implementation concept.

It intentionally does not reproduce entire substantive policy domains. Doing so would shift attention from the development methodology toward agreement or disagreement with particular political policies.

Because the architecture was developed against a considerably larger private corpus:

- some dependency IDs point to briefs that are not public;
- some trackers summarize areas whose underlying files are absent;
- the research index retains context for sources not included here; and
- repository-wide scans require the private directory tree.

Those seams are documented rather than concealed because the preserved relationships demonstrate that the examples came from a larger operating structure.

## Levels of Evidence in This Repository

To keep the distinction explicit:

| Level | Meaning |
|---|---|
| **Illustrative question** | A plain-language example of what the architecture is intended to help a team answer |
| **Enabled capability** | An operation supported by the schemas, workflows, and tooling |
| **Included demonstration** | An artifact or end-to-end example readers can inspect in this public repository |
| **Operational scale** | The larger private corpus against which the methods were developed and exercised |

## Repository Map

```text
README.md                  The entry point and guided tour
ARCHITECTURE.md            Technical and organizational system
PROJECT_STATUS.md          Sample portfolio status and gap analysis
walkthroughs/              Four short narrative case studies
samples/                   Inspectable policy and GovOps examples
research-library/          Source, adversarial review, and grading receipt
AI_Integrations/           Schema and workflow documentation
scripts/                   Ingestion, validation, tracking, and PDF tooling
```

## Core Commitments

- **Structured Documentation** - Utilize machine-readable schemas to make relationships and designs both transparent and inspectable. 
- **Adversarial Review** - Stress test each proposal's design against the available evidence instead of citing things that corroborate a viewpoint. 
- **Phase Discipline** - Run each proposal through a structured phase-gated cycle that incorporates architectural coherence checks as well as adversarial and expert review. Phase 'maturity' is tied to explicit gate conditions. 
- **Causal Specificity** - Tie individual policies to independent causal analysis. 
- **Human Authority** - Use automation to lower coordination costs. Human authority is reserved for policy design decisions. 


## Status

This is a demonstration repository built from extracts of a larger work in progress. The walkthroughs and briefs are drafts intended for critique. See [PROJECT_STATUS.md](./PROJECT_STATUS.md) for the sample maturity model and [ARCHITECTURE.md](./ARCHITECTURE.md) for the system description.
