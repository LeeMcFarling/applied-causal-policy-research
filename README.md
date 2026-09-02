# Applied Causal Policy Research Architecture

**While policy proposals and regulations are usually written as standalone documents responding to specific problems, the systems that they are deployed into, interact with, and the broader regulatory environment that they collectively create are anything but.** 

**This repository instead asks what becomes possible when we use software engineering techniques to treat policy proposals and regulations as connected, testable, and revisable parts of a larger system. Furthermore, this project demonstrates how a machine-readable policy development architecture could be used to enable dependency analysis, adversarial research reviews, causal analysis, and administrative workflow modeling.**


| Capability | The question it answers | Guided walkthrough |
|---|---|---|
| **Machine-readable architecture** | *What is our climate policy missing? Are there dependencies from manufacturing, trade, or finance we haven't caught that will sink this energy policy?* | [Architecture](./walkthroughs/01-machine-readable-policy-architecture.md) |
| **Adversarial research integration** | *How does our housing policy compare with the relevant research from think tanks, universities, and policy organizations? Where are the strongest gaps and deviations?* | [Research integration](./walkthroughs/02-research-integration-and-adversarial-revision.md) |
| **Causal evaluation by design** | *Can a policy carry its own evaluation architecture from day one—producing the comparisons and evidence needed to decide whether it should scale, change, or stop?* | [Causal evaluation](./walkthroughs/03-causal-evaluation-inside-policy-design.md) |
| **GovOps** | *What are the exact word-for-word regulatory differences in housing policy across all 50 states? What are the operational workflow differences that result? How can we see these differences in a real-time dashboard? What regulatory landscape leads to the fastest, cheapest, and *safest* results?* | [Process-legible law](./walkthroughs/04-govops-and-process-legible-law.md) |


> **Note: The policy examples above are illustrative.** These methods were developed and operationalized against a larger private policy corpus. This repository includes selected artifacts that allow readers to inspect the architecture without requiring them to navigate—or agree with—the source platform's substantive political positions.

The policy examples are therefore illustrative. The reusable product is the methodology, not the particular housing, wage, or regulatory positions contained in the samples. A future team would use the architecture to develop its own priorities, safeguards, implementation choices, and final recommendations.

## The 10-minute Tour: 

1. **How the System Works:** Open the [architecture reference](./ARCHITECTURE.md) to see how policy briefs are structured as markdown documents and linked to each other through YAML metadata to enable database level mechanics. This YAML frontmatter includes: Stable IDs, dependencies, audience tags, and phase gates, and so on. 
2. **Portfolio Level Analysis:** The [sample project status report](./PROJECT_STATUS.md) demonstrates how the database structure enables automated gap and maturity analysis using codebase software. 
3. **Retrieval Augmented Generation (RAG) Assisted Adversarial Review:** Policies should be compared against the latest research from Think Tanks, Universities, and other organizations. This platform allows this process to occur systematically by giving users a folder to ingest research along with scripts to process that research and generate an adversarial review including the Chicago Style references of the provided research, along with alignment, divergences, gaps, scope differences, and so on with page references between the documents. As an example, follow this [adversarial review](./research-library/reviews/community-stabilization-violence-research-review.md) of a policy proposal, along with an [independent grading receipt](./research-library/reviews/validation/community-stabilization-violence-research-review-grading.md) using LLM-as-judge methods, and a [revised brief](./samples/Policy_Domains/Housing_and_Public_Infrastructure/community-stabilization-framework.md) that resulted from the review.
4. **Scientific Method - for Public Policy:** To see how causal evaluation frameworks can be written into the structure of a policy itself [regional wage pilot](./samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md) with econometric evaluation and pre-written scale, or sunset criteria to mitigate the common flaw of promising pilots not scaling, or poorly-performing policies sticking around long after they've been disproven. 
5. **The System Applied: How to Map Regulations to the Operations they Produce:** Browse the [rendered GovOps brief](./samples/Operating-System/GovOps-RMC-tech-layer.pdf) for how the YAML metadata linkage above can be applied to regulatory environments with a dual-schema to enable efficiency comparisson between states, optimization, and regulatory sandbox design.

Each capability above has it's own narrative walkthrough that describes how it works in detail. For more information, click [walkthroughs](./walkthroughs/README.md). 

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

**Note:** The IDs at the top of each document function as foreign keys to other policy briefs. In this way, each document declares its own gaps, dependencies, and related instruments. Additionally, ‘audience’ tags support voter breakdowns, letting us quickly query the platform’s stated goals for segments of the population (as questions inevitably come up). Finally, phase gating logic allows us to track the sequencing of each domain (i.e. healthcare may be in expert review, while criminal justice might be in another stage altogether), and maturity_tracker documents track the gaps, phase gating, and sequencing of the larger system. 

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

The initial review is generated by using Retrieval Augmented Generation to pre-process the research: chunk it, vectorize it, and then compare it to relevant targets in the policy platform. A second model from a different provider is then used as a judge to grade how the first model generated the report using: 1) the vectorized research documents 2) the policy platform documents 3) the adversarial report using a standardized rubric. A human-in-the-loop then validates all page references, the grading report, and the adversarial review—and determines whether changes to the policy platform are necessary. 

Importantly, this process is treated as an early pre-validation step, and is used to determine directional validity before expert review later on. For this early pre-validation step, the chain of custody is the most important artifact that this should produce. Later on, reviewers can see which sources were used to validate which pieces of the platform, and then review the page sources, notes, scope, gaps, alignment, divergences, etc. ***Along with how the platform authors responded to the information***.   

Briefly this chain of custody will take the following form:

> Source Research (pre-digested) + Initial Policy Brief → First-model adversarial review → Cross-provider rubric audit → Human in the loop review and decision record → Brief revision


### 3. Embedding Causal Analysis into Policy Design

The [regional wage pilot](./samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md) is meant to demonstrate how a policy proposal can be structured in order to generate the data needed for its scale or sunset. As an example, the proposal includes a bounded intervention (rolled out to pre-designated jurisdictions first), statistically approximated treatment and control groups (which are used to determine where it takes place in the first place), independent research review (to prevent the government from grading its own work), and pre-specified paths detailing when to scale, revise, pause, or stop the intervention. 

While the wage policy is used as an example, the reusable idea is to bake the scientific method into policy design from the get-go in order to make the government more efficient at evaluating whether its proposals actually work. As a disclaimer, this system would still need a non-partial measurement authority, viable jurisdiction, ethical safeguards, etc. 

### 4. GovOps and process-legible law

**Question demonstrated:** Can law and regulation be represented in terms of both legal authority and the administrative processes they create?

This demonstration takes the same concepts introduced above -- whether version control, causal analysis, experimental design, legibility, etc. -- and applies them to government regulatory architecture. It documents how legal text documents can be tied digitally to the processes they create, how the regulatory landscape can be compared across jurisdictions in the country, and how this legal text can be optimized to produce a maximally efficient regulatory landscape in terms of both protective outcomes and permitting throughput. 

**Start with the [GovOps technical brief](./samples/Operating-System/govops-rmc-tech-layer.md)

**What to notice:** The dual-schema design explicitly maps the legal text of a regulation with the permitting workflows that it generates. The proposal then shows how this structure can be used to compare regulatory regimes across states / jurisdictions, map how changes to text might effect timelines, and how sandbox designs could be utilized to test new regulatory changes before broader roll out. 


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

This is a demonstration repository built from extracts of a larger work in progress. As such, the walktrhoughs and policy briefs are intended for critique and analysis. See [PROJECT_STATUS.md](./PROJECT_STATUS.md) for an example report, and the [ARCHITECTURE.md](./ARCHITECTURE.md) for a more detailed description into the system. 
