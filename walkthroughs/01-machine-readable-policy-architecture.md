---
title: "Walkthrough 1: Machine-Readable Policy Architecture"
subtitle: "From a collection of proposals to a coherent, queryable system"
status: Rough Draft
---

# Machine-Readable Policy Architecture

## The idea in one sentence

A policy platform can be maintained more like a complex engineered system: each proposal has a stable identity, declares its relationships to other proposals, advances through explicit maturity gates, and contributes to a continuously updated picture of the whole.

> **What this is:** A demonstration of repository structure and policy-development workflow.
>
> **What this is not:** A recommendation that another team adopt the policies contained in the source platform.

## The problem

Large policy agendas are usually assembled as collections of papers. Individual proposals may be thoughtful, but the collection is difficult to reason about as a system. A housing proposal may depend on a financing mechanism developed elsewhere. A wage proposal may affect benefit eligibility. An infrastructure promise may assume permitting capacity that does not exist. Those relationships often remain implicit until implementation exposes them.

The resulting questions are difficult to answer reliably:

- Which proposals depend on institutions that have not yet been created?
- Which reforms must precede others?
- Where do two domains make incompatible assumptions?
- Which audiences are affected by a proposal?
- Which parts of the agenda are mature, and which are still conceptual?
- Where are the largest unaddressed gaps?

A conventional table of contents cannot answer those questions. The repository therefore treats each brief as both a human-readable document and a machine-readable object.

## The demonstrated method

Every policy object begins with YAML front matter. The prose explains the proposal; the metadata explains where the proposal sits in the larger system.

```yaml
---
id: regional-wage-modernization-pilot
title: Regional Wage Modernization Pilot
domain: Labor_and_Economic_Security
subdomain: Wage_Modernization
phase: 1
layer: 4
audiences:
  - rural-america
  - veterans
  - working-class
dependencies:
  - doda-regional-wage-heatmap
  - benefits-gradient-modernization
tags:
  - regional-pilot
  - evidence-gated
---
```

The fields are not decorative labels. They make several repository-wide operations possible.

### Stable identity and foreign-key relationships

The `id` gives each proposal a durable identity. Fields such as `dependencies` and `related_instruments` refer to those IDs, creating relationships analogous to foreign keys in a database.

That permits automated questions such as:

- What breaks if this instrument is delayed?
- Which proposals depend on the same institution?
- Does a brief refer to an ID that does not exist?
- Is a supposedly standalone proposal actually downstream of several unfinished reforms?

### Phase discipline

Each brief is assigned a maturity phase. Early phases define the problem and architecture. Later phases require research integration, pilot design, implementation planning, external review, and revision.

The critical feature is not the number of phases. It is that advancement is tied to observable conditions. A brief cannot become “implementation ready” merely because its prose is polished. Its dependencies, evidence, legal vehicle, evaluation plan, and unresolved risks must mature with it.

### Audience and cross-domain analysis

Audience tags make it possible to generate views of the platform for different affected groups without maintaining separate, drifting copies of the same policy. Domain and subdomain fields support aggregation. Dependency graphs reveal cross-domain seams that conventional organizational charts obscure.

### Gap analysis

Maturity trackers summarize what exists, what is missing, which dependencies are blocking progress, and what work should happen next. In a complete repository, these records support platform-level gap analysis rather than relying on institutional memory.

## Worked example: housing as a connected domain

The included housing extracts show multiple levels of the architecture:

1. The [housing system overview](../samples/Policy_Domains/Housing_and_Public_Infrastructure/overview-housing-and-urban-architecture.md) describes how individual instruments fit together.
2. The [zoning function ladder](../samples/Policy_Domains/Housing_and_Public_Infrastructure/zoning-function-ladder.md) demonstrates a single instrument with declared dependencies and related initiatives.
3. The [community-stabilization framework](../samples/Policy_Domains/Housing_and_Public_Infrastructure/community-stabilization-framework.md) shows a more mature brief that has passed through research integration.
4. The [housing maturity tracker](../samples/Policy_Domains/Housing_and_Public_Infrastructure/_MATURITY_TRACKER.md) summarizes domain status and gaps.

The references to policies not included in this public extract are intentionally preserved. They show that the visible briefs were removed from a larger relational system rather than written as isolated portfolio pieces.

> **Suggested figure:** A small dependency graph with the housing overview at the center, three included briefs in color, and omitted upstream/downstream IDs in gray. Caption: “The extracts preserve their position within the larger policy graph.”

## What this demonstration establishes

The extracts establish that policy documents can be represented in a form that supports both substantive reading and computational maintenance. They demonstrate a plausible mechanism for:

- dependency validation;
- phase-aware sequencing;
- audience-specific views;
- cross-domain gap detection;
- shared metadata standards; and
- portfolio-level status reporting.

## What it does not establish

The demonstration does not prove that the particular schema is complete, that every dependency has been correctly identified, or that structured metadata can resolve substantive political disagreement. A graph can expose a dependency; it cannot decide whether the underlying policy is wise.

The public extract also cannot run every repository-wide validation because much of the private source tree is intentionally absent.

## What a future team owns

A future team would decide:

- its policy priorities and substantive positions;
- the metadata fields appropriate to its workflow;
- the meaning and gate conditions of each maturity phase;
- who may create, review, approve, or retire policy objects;
- how disagreements and exceptions are recorded; and
- which automated checks should block publication or implementation.

The reusable idea is not this platform's answers. It is the ability to make a large body of policy work coherent, inspectable, and maintainable.

## Underlying evidence

- [Architecture reference](../ARCHITECTURE.md)
- [Project status and sample gap analysis](../PROJECT_STATUS.md)
- [YAML front-matter guide](../AI_Integrations/YAML_FRONTMATTER_GUIDE.md)
- [Housing maturity tracker](../samples/Policy_Domains/Housing_and_Public_Infrastructure/_MATURITY_TRACKER.md)
