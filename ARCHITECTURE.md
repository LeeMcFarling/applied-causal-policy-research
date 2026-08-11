# Policy Research Architecture

## Purpose

This document describes the technical and organizational architecture demonstrated by this repository. The system is designed to help a policy team maintain a large body of work as a coherent, inspectable, and revisable whole.

The included briefs are extracts from a larger private platform. Their policy content is illustrative. A future team would determine its own priorities, substantive positions, safeguards, and implementation choices. The reusable subject of this document is the development method.

## Design Goals

The architecture is intended to make several questions answerable across a large policy portfolio:

- What does each proposal depend on?
- Which proposals or institutions must be developed first?
- Where do different domains interact or conflict?
- Which audiences are affected?
- How mature is each proposal, and what prevents it from advancing?
- What outside evidence supports, qualifies, or contradicts its mechanisms?
- How will implementation generate credible evidence?
- What result would cause a proposal to scale, change, or stop?

The repository supports those questions through structured policy objects, explicit relationships, maturity gates, research receipts, and evaluation requirements.

## Four-Layer Model

The complete source platform organizes work into four functional layers:

| Layer | Function |
|---|---|
| **L1 — Foundations** | Shared theories, assumptions, causal mechanisms, and design constraints |
| **L2 — Operating System** | Institutions and processes that translate authorization into execution and accountability |
| **L3 — Infrastructure** | Shared technical capabilities used across institutions and policy domains |
| **L4 — Policy Domains** | Substantive policy instruments grouped by area of application |

The layers are a dependency model, not a claim that every team must organize its work this way. Their purpose is to prevent domain proposals from silently assuming that institutional or technical capabilities already exist.

## The Policy Object

Each brief is both a human-readable Markdown document and a machine-readable object. YAML front matter supplies a common schema:

```yaml
---
id: regional-wage-modernization-pilot
title: Regional Wage Modernization Pilot
domain: Labor_and_Economic_Security
subdomain: Wage_Modernization
policy_type: Pilot Program
status: Draft
phase: 1
layer: 4
version: 0.1
audiences:
  - rural-america
  - veterans
  - working-class
dependencies:
  - doda-regional-wage-heatmap
  - benefits-gradient-modernization
related_instruments:
  - worker-classification-parity
tags:
  - regional-pilot
  - evidence-gated
---
```

The prose explains the proposal. The metadata identifies it, locates it within the larger architecture, and exposes relationships that repository tooling can inspect.

### Stable identifiers and relationships

The `id` is the stable key for a policy object. Other briefs refer to that key through fields such as `dependencies` and `related_instruments`.

Those references support:

- missing-key detection;
- dependency graphs;
- downstream-impact analysis;
- cross-domain relationship maps;
- sequencing checks; and
- identification of shared institutional bottlenecks.

A hard dependency means that the downstream proposal cannot operate as designed without the upstream object. A related instrument indicates a meaningful relationship without imposing the same gate.

### Audience and classification fields

Audience tags support filtered views of a single source of truth rather than separate copies of the same proposal. Domain, subdomain, policy type, layer, and topical tags support aggregation and gap analysis.

The schema is documented in the [YAML front-matter guide](./AI_Integrations/YAML_FRONTMATTER_GUIDE.md). A future team could add, remove, or redefine fields to match its governance needs.

## Maturity and Phase Gates

Briefs advance through a 10-phase development model:

| Phase | Focus |
|---|---|
| **0** | Problem framing and constraints |
| **1** | Structured exploration |
| **2** | Architecture and decision rules |
| **3** | Research integration and stress testing |
| **4** | Pilot target and initial authorization analysis |
| **5** | Phasing and implementation design |
| **6** | Publication-ready draft |
| **7** | External expert review |
| **8** | Revision and incorporation |
| **9** | Public communication |

Phase is intended to describe completed work, not confidence or political priority. Advancement depends on explicit gate conditions. A polished document cannot skip unresolved dependencies, research review, implementation design, or evaluation planning simply because it reads well.

Hard dependencies constrain sequencing: a downstream brief should not be treated as more implementation-ready than the upstream capabilities required to operate it.

## Portfolio Status and Gap Analysis

Maturity trackers aggregate policy objects by domain or layer. They summarize:

- current phase;
- blocking dependencies;
- incomplete metadata;
- critical, structural, and enhancement gaps;
- recent revisions; and
- next actions.

This turns status reporting into a view of the repository rather than a separate narrative that must be maintained by hand. The public [project status report](./PROJECT_STATUS.md) and included maturity trackers are sample outputs from the larger system.

## Research Integration

At the research-integration phase, an outside source moves through a traceable workflow:

> Source ingestion → Scope definition → Adversarial review → Independent grading → Decision record → Brief revision

The review distinguishes:

- findings directly supported by the source;
- inferences made by the policy team;
- relevant gaps;
- genuine divergences;
- open questions; and
- explicit decisions to revise or retain the design.

The goal is not to automate substantive judgment or claim that research produces a single correct policy. It is to preserve the chain of reasoning between evidence and design.

The public repository includes one complete worked example in the [research library](./research-library/index.md).

## Evaluation Inside Policy Design

Where appropriate, proposals can specify their evaluation architecture before implementation:

- unit of analysis;
- treatment definition;
- comparison or identification strategy;
- baseline and measurement window;
- primary and secondary outcomes;
- implementation-fidelity measures;
- adverse-effect thresholds;
- independent review; and
- scale, revision, pause, or sunset gates.

This does not make every decision reducible to a treatment effect. Rights, distribution, democratic commitments, legal constraints, and implementation feasibility remain substantive considerations. The architecture makes the evidentiary component explicit and connects results to predefined decisions.

The [regional wage pilot](./samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md) is the included example.

## GovOps and Process Legibility

The GovOps example extends structured representation from policy documents to administrative implementation. It pairs:

- a **legal schema** describing authority, obligations, applicability, and amendment history; with
- a **workflow schema** describing actors, inputs, decisions, sequence, duration, outputs, and exception paths.

Links between the two preserve traceability from a workflow step to its legal authority. This supports cross-jurisdictional comparison, workflow observability, and bounded testing of alternative implementations without treating speed as the only objective or allowing a workflow model to supersede law.

The [GovOps technical brief](./samples/Operating-System/govops-rmc-tech-layer.md) is the included example.

## Human and Automated Responsibilities

Automation can assist with schema validation, missing-key detection, dependency mapping, research organization, comparison, and status reporting. It does not determine the team's values, authorize policy, resolve contested evidence, or replace legal and democratic judgment.

The intended division of responsibility is:

| Automated assistance | Human responsibility |
|---|---|
| Parse and validate metadata | Define the schema and its meaning |
| Find missing or circular references | Decide whether a relationship is substantively valid |
| Organize evidence and candidate tensions | Evaluate evidence and make policy judgments |
| Produce status and gap views | Set priorities and allocate work |
| Monitor predefined measures | Authorize scaling, revision, or termination |

## Public Extract Boundary

This repository contains enough material to inspect four capabilities:

1. machine-readable architecture;
2. research-to-revision traceability;
3. causal evaluation embedded in a policy pilot; and
4. legal/workflow representation through GovOps.

The complete private platform contains approximately 313 briefs across 18 policy domains. Consequently:

- some dependency IDs point to briefs not included here;
- some trackers summarize areas whose underlying files are private;
- the research index retains catalog context for sources not included in the extract; and
- repository-wide scans require directories absent from this public sample.

These seams are documented rather than concealed because the preserved relationships help demonstrate that the examples came from a larger operating structure.

## Where to Continue

- [README](./README.md) — purpose, scope, and guided navigation
- [Walkthrough 1](./walkthroughs/01-machine-readable-policy-architecture.md) — accessible architecture case study
- [YAML front-matter guide](./AI_Integrations/YAML_FRONTMATTER_GUIDE.md) — field-level schema reference
- [Project status](./PROJECT_STATUS.md) — sample portfolio reporting and gap analysis
- [Research-library index](./research-library/index.md) — research integration example
