# Applied Causal Policy Research Architecture

## Why This Exists

Hyperscaled organizations routinely manage production platforms that host billions of people, are governed by 100s of millions of lines of code, managed by thousands of engineers working simultaneously, distributed across the world. This sits on top of 100s of billions of dollars worth of infrastructure, and these platforms must find a way to continuously improve their operations, production models, and other systems while their broader systems remain in production every minute of every day.

The methodologies that these hyperscalers use to do this are virtually identical across Amazon, Microsoft, Google, Meta, and other hyper-scaler organizations: version control, structured review, dependency management, staged deployment, observability, controlled experimentation, and continuous revision. When I got interested in government reform, I was struck by how absent these systems were in government. Government policy -- be that laws, regulations, procedures, and so on -- functions exactly like civilizational software. If you want to build a house, you follow a sequential set of building instructions specified via regulations. If you want to start a business, it's the same idea, just a different set of instructions. 

If we follow this logic to its natural conclusion, the federal government has the same depth and breadth of responsibilities as any other hyper-scaler, but unlike those organizations, it does not have the same tools for managing itself. Policies get drafted, debated, and enacted as one-off documents with no dependency graphs, no staged rollouts, no observability, and no structured mechanism for revising it once evidence comes in. Great policies get implemented in Dallas, but there is no automatic notification or scaling mechanism for rolling them out in other areas once they prove successful. Likewise, bad policies get implemented without a structured method for testing and rolling them back if they are unsuccessful at meeting their stated goals. 

This project therefore explores whether methodologies that emerged in hyperscale engineering organizations to manage runaway complexity — version control, dependency management, peer review, staged deployment, experimentation, and observability — can be adapted into a continuously learning system for public policy. This repository is what that question grew into.

## Scope of This Demonstration

The policy briefs included here are selected examples picked to demonstrate ways a team might structure policy dependencies, integrate adversarial research, embed causal evaluation in pilot design, and represent legal and administrative processes as legible workflows. The particular policy ideas remain drafts and should be evaluated, revised, replaced, or discarded by the teams responsible for the work.

The reusable product is the method. Future teams retain ownership of their substantive priorities, policy judgments, implementation choices, and final recommendations.

Readers who want a guided introduction can begin with the four [walkthrough drafts](./walkthroughs/README.md). Readers who want to inspect the implementation can follow each walkthrough into the underlying briefs, metadata, research receipts, trackers, scripts, and figures.

## The Core Idea: The Software Development Lifecycle, Applied to Public Policy

The core idea here is that government policy -- be that laws, regulations, what have you -- function like civilizational software. If someone wants to build a house or a business, there are legal processes, with steps, that they need to follow in order to get that done. 

| Software Engineering | Policy Architecture |
|-----------------------|-----------------|
| Module | Policy brief |
| Package | Policy domain |
| Pull request | Merge packet |
| Code review | DoDA certification |
| Testing | Regional pilots & causal evaluation |
| CI/CD | Pilot → Scale → Sunset |
| Production | Regulatory regime |

Twenty years ago this would have been prohibitively expensive — you'd need armies of analysts to read every research paper, maintain dependency graphs, compare legislation, write reviews, identify conflicts, monitor pilots, and summarize findings by hand. Today, AI integration can change the economics of that substantially. Humans still draft the policies, but AI systems can be utilized to check dependencies, find gaps, and structurally red-team the policies to see if they hold up against existing literature, in processes that are startlingly similar to unit testing code, or maintaining a codebase. In this system, humans still make every decision — AI just lowers the transaction cost of maintaining institutional memory at a scale no team of analysts from any one state could sustain manually.

*An important note:* This demonstration does not argue that government should operate like Silicon Valley. When lives are on the line, the motto cannot be *move fast and break things*. It asks which tools developed to manage complexity at scale — versioning, structured review, dependency management, continuous learning, and related disciplines — can be adapted while preserving due process, democratic authorization, and accountability. Future teams must decide where that analogy is useful and where it should end.

The underlying question ends up mattering beyond policy — it's the same question AI governance research, GovTech, civic tech, knowledge management, and computational social science are all wrestling with in their own way: how does a very large, very complex organization keep learning as it grows? Government is just one application of it.

---

## Four Demonstrations

This repository contains selected structural extracts from a much larger policy platform. Together, they demonstrate four reusable capabilities. The examples show how the methods work; they do not ask a future team to adopt the underlying policy positions.

Draft PDF narratives: [Architecture](./walkthroughs/01-machine-readable-policy-architecture.md) · [Research integration](./walkthroughs/02-research-integration-and-adversarial-revision.md) · [Causal evaluation](./walkthroughs/03-causal-evaluation-inside-policy-design.md) · [GovOps](./walkthroughs/04-govops-and-process-legible-law.md)

### 1. Machine-readable platform architecture

**Question demonstrated:** How can hundreds of policy proposals be maintained as one coherent, queryable system rather than a collection of disconnected papers?

**Start here:**

- [Architecture reference](./ARCHITECTURE.md) — the four-layer model and development system
- [Project status](./PROJECT_STATUS.md) — sample maturity matrices, gap analysis, and cross-domain status
- [YAML front-matter guide](./AI_Integrations/YAML_FRONTMATTER_GUIDE.md) — the machine-readable schema
- [Housing domain overview](./samples/Policy_Domains/Housing_and_Public_Infrastructure/overview-housing-and-urban-architecture.md) — a worked example of policies assembled into a domain
- [Housing maturity tracker](./samples/Policy_Domains/Housing_and_Public_Infrastructure/_MATURITY_TRACKER.md) — sample dependency, gap, and phase tracking

**What to notice:** Stable IDs function as foreign keys; briefs declare hard dependencies and related instruments; audience tags support targeted views; phase gates constrain sequencing; and maturity trackers expose gaps across the larger system.

### 2. Research integration and adversarial revision

**Question demonstrated:** How can external research do more than decorate a proposal with citations—how can it test the proposal and force documented changes?

**Follow the evidence chain:**

1. [Ingested 17A source record](./research-library/sources/17a-reducing-violent-crime-2026.md)
2. [Adversarial research review](./research-library/reviews/community-stabilization-violence-research-review.md)
3. [Independent grading receipt](./research-library/reviews/validation/community-stabilization-violence-research-review-grading.md)
4. [Revised community-stabilization brief](./samples/Policy_Domains/Housing_and_Public_Infrastructure/community-stabilization-framework.md)

**What to notice:** The review distinguishes direct support from inference, records gaps and divergences, anticipates counterarguments, and ends with a decision log. The revised brief then incorporates operational cadence, adaptive targeting, maintenance requirements, and combined-signal protocols derived from that review.

### 3. Causal evaluation inside policy design

**Question demonstrated:** What changes when evaluation is part of the policy itself rather than an after-the-fact study?

**Start here:** [Regional Wage Modernization Pilot](./samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md)

**What to notice:** The proposal defines a bounded pilot, treatment and comparison regions, pre-specified measures, evidence gates, escalation conditions, and a pathway to revise, scale, or stop the intervention. The specific wage proposal is illustrative; the reusable feature is the experimental structure.

### 4. GovOps and process-legible law

**Question demonstrated:** Can law and regulation be represented in terms of both legal authority and the administrative processes they create?

**Start here:** [GovOps technical brief](./samples/Operating-System/govops-rmc-tech-layer.md) or the [rendered PDF](./samples/Operating-System/GovOps-RMC-tech-layer.pdf)

**What to notice:** The dual-schema architecture connects legal clauses to workflow steps, compares implementations across jurisdictions, instruments administrative timelines, and uses controlled sandboxes to search for designs that preserve protective outcomes while reducing avoidable process time.

## What Is and Is Not Included

This public repository is an architectural blueprint and tooling showcase. It includes enough source material to inspect the schema, trace one research-to-revision cycle, examine one causally designed pilot, and review one GovOps implementation concept. The complete private source platform spans approximately 313 briefs across 18 domains and roughly 560,000 words.

Because these are extracts, some dependency IDs refer to policies that are not included here. Those references are intentionally preserved: they are evidence of the larger relational structure, not claims that every linked document is available in this sample. The included scripts likewise demonstrate the production workflow, although repository-wide scans require the private directory tree.

For access to the complete private codebase or to discuss implementation mechanics, please contact me directly.

## Technical Tooling

The presentation layer includes:

- **Automated document pipelines:** Python scripts for PDF compilation, metadata validation, and research ingestion
- **The 10-phase development model (Phases 0–9):** maturity gates tied to architectural and research dependencies
- **Maturity tracking:** scanners that parse front matter to produce status matrices and gap analyses

---

## Shared Principles

All artifacts in this repository are organized around the same core commitments:

- **Causal specificity over correlation** — claims require mechanism identification, not pattern-matching
- **Structured documentation** — every claim, dependency, and design decision is machine-readable and traceable
- **Adversarial review** — research integration is validated against the original source, not just summarized
- **Phase discipline** — documents advance through defined maturity gates with explicit gate conditions
- **Institutional legibility** — outputs are designed to be read by policymakers, researchers, and practitioners, not only specialists

---

## Domain Coverage

The full private repository spans 18 policy domains. The maturity tracker and domain index are reproduced in [`PROJECT_STATUS.md`](./PROJECT_STATUS.md). Policy documents are available upon request.
