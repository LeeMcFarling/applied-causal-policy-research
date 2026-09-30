# Applied Causal Policy Research Architecture

**Policy proposals and regulations are usually written as standalone documents, each responding to a specific problem; the systems they are deployed into, and the regulatory environment they collectively create, are anything but standalone.**

**This repository asks what becomes possible when we borrow the techniques of software engineering and treat policies and regulations as connected, testable, and revisable parts of a larger system. In particular, it demonstrates how a machine-readable policy architecture can support dependency analysis, adversarial research review, causal evaluation, and administrative workflow modeling.**


| Capability | The question it answers | Guided walkthrough |
|---|---|---|
| **Machine-readable architecture** | *What is our climate policy missing? Are there dependencies in manufacturing, trade, or finance that we haven't caught, and that could sink this energy policy?* | [Architecture](./walkthroughs/01-machine-readable-policy-architecture.md) |
| **Adversarial research integration** | *How does our housing policy hold up against the relevant research from think tanks, universities, and policy organizations? Where are the largest gaps and divergences?* | [Research integration](./walkthroughs/02-research-integration-and-adversarial-revision.md) |
| **Causal evaluation by design** | *Can a policy carry its own evaluation architecture from day one, producing the comparisons and evidence needed to decide whether it should scale, change, or stop?* | [Causal evaluation](./walkthroughs/03-causal-evaluation-inside-policy-design.md) |
| **GovOps** | *What are the exact, word-for-word differences in housing regulation across all 50 states, and what operational workflows do those differences produce? Can we see them in a real-time dashboard? Which regulatory landscape delivers the fastest, cheapest, and safest results?* | [Process-legible law](./walkthroughs/04-govops-and-process-legible-law.md) |


> **Note: the policy examples above are illustrative.** The methodology on display here is the conversion of policy documents into machine-readable objects, not the individual policy positions contained in the samples. The intent is for a future team to use this architecture to develop its own policies and implementation choices.

## A 10-Minute Tour

1. **How the system works:** The [architecture reference](./ARCHITECTURE.md) shows how policy briefs are written as markdown documents and linked to one another through YAML metadata, which gives the collection database-level mechanics. That front matter includes stable IDs, dependencies, audience tags, and phase gates, among other fields.
2. **Portfolio-level analysis:** The [sample project status report](./PROJECT_STATUS.md) shows how that database structure enables automated gap and maturity analysis across the whole platform.
3. **Retrieval-augmented generation (RAG) for adversarial review:** Policies should be tested against the latest research from think tanks, universities, and other organizations, and this platform makes that process systematic. Users drop research into an ingestion folder; scripts then process it and generate an adversarial review. The output includes Chicago-style references to the source research, along with the alignment, divergences, gaps, and scope differences between that research and the policy proposal, each claim backed by page references in both documents. To see it in action, follow this [adversarial review](./research-library/reviews/community-stabilization-violence-research-review.md) of a policy proposal, the [independent grading receipt](./research-library/reviews/validation/community-stabilization-violence-research-review-grading.md) produced with LLM-as-judge methods, and the [revised brief](./samples/Policy_Domains/Housing_and_Public_Infrastructure/community-stabilization-framework.md) that resulted.
4. **The scientific method, applied to public policy:** The [regional wage pilot](./samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md) shows how a causal evaluation framework can be written into the structure of a policy itself: econometric evaluation plus pre-written criteria to scale or sunset. This is meant to address two common failures: promising pilots that never scale, and poorly performing policies that linger long after they have been disproven.
5. **The system applied to regulation:** The [GovOps brief](./samples/Operating-System/govops-rmc-tech-layer.md) shows how the same YAML linkage can be applied to regulatory environments through a dual schema, enabling efficiency comparisons between states, optimization, and regulatory sandbox design.

Each capability above has its own narrative walkthrough describing how it works in detail; see the [walkthroughs index](./walkthroughs/README.md).

## Why Do We Need Machine-Readable Policy Systems?

Hyperscale organizations routinely run production platforms that serve billions of people, span hundreds of millions of lines of code, and are maintained by thousands of engineers working simultaneously around the world. These platforms sit on top of hundreds of billions of dollars' worth of infrastructure, and they must continuously improve their operations, models, and systems while staying live for billions of users every minute of every day.

The methods these organizations use to pull this off are virtually identical across Amazon, Microsoft, Google, Meta, and their peers: version control, structured review, dependency management, staged deployment, observability, controlled experimentation, and continuous revision. When I became interested in government reform, however, I was struck by how absent these disciplines were from government.

In many ways, public policy (laws, regulations, procedures, and so on) functions as civilizational software. If you want to build a house, you follow a sequence of building instructions specified by law; if you want to start a business, you follow a different procedure, specified by statute. Unlike the companies above, though, government has no real tooling to manage this complexity.

Instead, policies are drafted, debated, and enacted as one-off documents, with no dependency graphs, no staged rollouts, no observability, and no structured mechanism for revision once the evidence comes in. A great policy can succeed in Dallas without any mechanism to notice that success and scale it elsewhere. Likewise, a bad policy can be implemented without any structured way to test it, or to roll it back when it fails to meet its stated goals.

In other words:

> How can the technocratic execution of the private sector be adapted to public policy while preserving the democratic safeguards we have come to expect from our institutions: due process, democratic authorization, legal accountability, and so on?

This project investigates whether the tools developed to manage that kind of complexity (version control, dependency management, peer review, and experimentation among them) can be adapted into a continuously learning system for public policy. To be clear, it does **not** argue that government should operate like a technology company. These systems are useful only if they increase a government's ability to deliver on its own promises without sacrificing democratic accountability.

## Demonstrations

### 1. How to Implement a Machine-Readable Platform Architecture

> How can hundreds of text-based policies (or laws, or regulations) be maintained as a single coherent, queryable, and auditable system, rather than as a collection of disconnected papers?

The architecture section walks through how YAML front matter, adapted from Docusaurus documentation standards, can be applied to public policy. That one structural choice enables gap and dependency analysis, adversarial research review, and maturity tracking through phase gates.

- [Architecture reference](./ARCHITECTURE.md): how the machine-readable system is applied to policy briefs, and how a platform's architecture enables the analysis described above.
- [Project status](./PROJECT_STATUS.md): an example of the status report the platform generates once the architecture is in place, including sample maturity matrices, gap analysis, and cross-domain status.
- [YAML front-matter guide](./AI_Integrations/YAML_FRONTMATTER_GUIDE.md): how to use the machine-readable schema to add and track metadata across a policy platform.
- [Housing domain overview](./samples/Policy_Domains/Housing_and_Public_Infrastructure/overview-housing-and-urban-architecture.md): a worked example of the system in practice within a single policy domain.
- [Housing maturity tracker](./samples/Policy_Domains/Housing_and_Public_Infrastructure/_MATURITY_TRACKER.md): how the system integrates multiple housing briefs to answer questions like "What gaps exist in our housing policies? Which documents still need research validation? How mature is this domain within the policy stack?" Trackers like this one then roll up across domains (e.g., healthcare, housing, fiscal policy) into the project-wide status document above.

**Note:** The IDs at the top of each document function as foreign keys to other briefs; in this way, each document declares its own gaps, dependencies, and related instruments. "Audience" tags support voter breakdowns, so the platform's stated goals can be queried quickly for any segment of the population (as those questions inevitably come up). Phase-gating logic tracks where each domain sits in its sequence (healthcare may be in expert review, for example, while criminal justice is in another stage altogether), and the maturity tracker documents record the gaps, gates, and sequencing of the larger system.

### 2. Research Integration and Adversarial Review

> How can we use modern technology to stress-test policy proposals against research from think tanks, universities, and policy organizations before the platform goes public?

Every policy platform in recent memory has met skepticism from at least one organization or national stakeholder. This demonstration shows how research can be ingested ahead of time to separate genuine critiques, which call for changes to the underlying policy architecture, from critiques that can be rebutted.

To do this, the platform provides a folder into which an organization can drop PDFs of studies, case studies, meta-analyses, and other research. When prompted, the platform extracts the text from those documents and uses it to run an adversarial review against one or more briefs in the platform.

The resulting review first documents the difference in scope between the policies under review and the research being used to test them. It then identifies alignment, gaps, divergences, and open questions, each with page numbers.

Next, the review, the source research, and the underlying platform documents are passed to a different model, from a different provider, which produces an independent grading receipt. That receipt states whether the review passes or fails; a failing review goes back for a second pass with updated instructions.

When the process is complete, it leaves behind a documented step-by-step analysis, the adversarial review itself, and a decision log recording which critiques were rebutted and why, along with which changes to the underlying policy they forced.

**An example:**

1. [Ingested 17A source record](./research-library/sources/17a-reducing-violent-crime-2026.md): a sample case study from a leading government consulting and technology firm, used to adversarially review a community stabilization framework from the Housing and Urban Infrastructure domain.
2. [Adversarial research review](./research-library/reviews/community-stabilization-violence-research-review.md): the review generated by the process, including the decision log that came out of the analysis and the final grade from the independent grading receipt.
3. [Independent grading receipt](./research-library/reviews/validation/community-stabilization-violence-research-review-grading.md): the grading receipt generated from the review.
4. [Revised community-stabilization brief](./samples/Policy_Domains/Housing_and_Public_Infrastructure/community-stabilization-framework.md): the final policy document incorporating the review's recommendations. Because the platform is version-controlled with Git, the revision carries a line-by-line diff of the before and after, along with metadata on who made each change and when.

Under the hood, the initial review uses retrieval-augmented generation to pre-process the research: chunking it, vectorizing it, and comparing it to the relevant targets in the policy platform. A second model from a different provider then acts as a judge, grading the first model's report against (1) the vectorized research, (2) the policy platform documents, and (3) the adversarial report itself, using a standardized rubric. Finally, a human in the loop validates every page reference, the grading report, and the adversarial review, and decides whether the platform needs to change.

Importantly, this process is an early pre-validation step, meant to establish directional validity before formal expert review. At this stage, the chain of custody is the most important thing it produces. Later reviewers can see which sources were used to validate which pieces of the platform, along with the page references, notes, scope, gaps, alignment, and divergences; ***just as importantly, they can see how the platform's authors responded to that information.***

In brief, the chain of custody takes the following form:

> Source research (pre-digested) + initial policy brief → first-model adversarial review → cross-provider rubric audit → human-in-the-loop review and decision record → brief revision


### 3. Causal Analysis Embedded into Policy Design

The [regional wage pilot](./samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md) demonstrates how a policy proposal can be structured to generate the very data needed to decide whether it should scale or sunset. The proposal includes a bounded intervention (rolled out to pre-designated jurisdictions first), statistically matched treatment and control groups (which determine where the pilot takes place in the first place), independent research review (so the government is not grading its own work), and pre-specified paths for when to scale, revise, pause, or stop.

Although the wage policy is only an example, the reusable idea is to build the scientific method into policy design from the start, so that government gets better at learning whether its proposals actually work. This system would, of course, still need an impartial measurement authority, viable jurisdictions, and ethical safeguards.

### 4. The Same Process Applied to Law and Regulation

**Question demonstrated:** Can law and regulation be represented in terms of both their legal authority and the administrative processes they create?

This demonstration takes the concepts introduced above (version control, causal analysis, experimental design, and legibility) and applies them to the architecture of regulation itself. It documents how legal text can be tied digitally to the processes it creates, how regulatory landscapes can be compared across jurisdictions, and how that text can be optimized for both protective outcomes and permitting throughput.

**Start with the [GovOps technical brief](./samples/Operating-System/govops-rmc-tech-layer.md).**

**What to notice:** The dual-schema design explicitly maps a regulation's legal text to the permitting workflows it generates. The brief then shows how that structure can be used to compare regulatory regimes across states and jurisdictions, to model how changes to the text might affect timelines, and to design sandboxes that test new regulatory changes before a broader rollout.


## What Is Included, and What Is Not

This public extract contains enough material to:

- inspect the machine-readable schema and dependency model
- examine sample maturity and gap-analysis outputs
- trace one research-to-revision cycle
- review one causally designed pilot
- inspect one GovOps implementation concept.

It intentionally does not reproduce entire policy domains, since doing so would shift attention away from the development methodology and toward agreement or disagreement with particular political positions.

Because the architecture was developed against a considerably larger private corpus:

- some dependency IDs point to briefs that are not public
- some trackers summarize areas whose underlying files are absent
- the research index retains context for sources not included here
- repository-wide scans require the private directory tree

These seams are documented rather than concealed; the relationships they preserve are evidence that the examples came from a larger operating structure.

## Levels of Evidence in This Repository

To keep the distinction explicit:

| Level | Meaning |
|---|---|
| **Illustrative question** | A plain-language example of what the architecture is meant to help a team answer |
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

- **Structured documentation:** use machine-readable schemas so that relationships and design choices are transparent and inspectable.
- **Adversarial review:** stress-test each proposal against the available evidence, rather than citing only what corroborates a viewpoint.
- **Phase discipline:** run each proposal through a phase-gated cycle that includes architectural coherence checks along with adversarial and expert review; a proposal's "maturity" is tied to explicit gate conditions.
- **Causal specificity:** tie individual policies to independent causal analysis.
- **Human authority:** use automation to lower coordination costs, while reserving policy design decisions for people.


## Status

This is a demonstration repository built from extracts of a larger work in progress; the walkthroughs and policy briefs are offered for critique and analysis. See [PROJECT_STATUS.md](./PROJECT_STATUS.md) for an example status report, and [ARCHITECTURE.md](./ARCHITECTURE.md) for a more detailed description of the system.
