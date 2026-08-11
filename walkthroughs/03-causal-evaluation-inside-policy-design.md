---
title: "Walkthrough 3: Causal Evaluation Inside Policy Design"
subtitle: "Designing a policy to learn before it scales"
status: Rough Draft
---

# Causal Evaluation Inside Policy Design

## The idea in one sentence

A policy can be written as a bounded, evidence-gated intervention whose comparison strategy, measurements, decision thresholds, and stopping conditions exist before implementation begins.

> **What this is:** A demonstration of causal evaluation embedded in a policy proposal.
>
> **What this is not:** An endorsement of the proposed wage level, regional formula, or institutional arrangement.

## The problem

Evaluation is often appended to policy after the important choices have already been made. Programs launch nationally, data systems arrive late, success criteria remain vague, and evaluators are asked whether the policy “worked” without a credible counterfactual.

That makes several questions difficult or impossible to answer:

- What would have happened without the intervention?
- Which outcomes were selected before results were known?
- How large must an effect be to justify expansion?
- Which adverse effects should pause or terminate the program?
- Was a disappointing result caused by the policy mechanism or poor implementation?
- Can a successful result generalize beyond the pilot sites?

The regional wage example shows how those questions can become part of the policy architecture itself.

## The demonstrated design

The [Regional Wage Modernization Pilot](../samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md) proposes a geographically bounded wage-floor experiment. Its substantive details are illustrative. Its structure is the demonstration.

### 1. Define a bounded intervention

The proposal does not begin with universal implementation. It defines a limited pilot, a staged onramp, regional calibration, and institutional support intended to make the treatment observable and reversible.

Bounding the intervention reduces the risk of learning only after a national commitment has become politically or administratively irreversible.

### 2. Specify the unit of analysis

The proposal uses commuting zones and regional labor markets rather than assuming that state boundaries describe the relevant economy. That choice connects the intervention to the geography in which workers and firms actually interact.

The broader lesson is that the unit of analysis should follow the mechanism. A future team might choose counties, firms, school districts, watersheds, hospitals, or individuals depending on the policy.

### 3. Build a comparison strategy

The evaluation design pairs treatment regions with comparison regions using pre-treatment characteristics and trends. It also proposes border analysis and regression-discontinuity logic where geographically adjacent areas experience different treatment conditions.

Multiple strategies matter because every design has weaknesses. Regional matching can leave residual confounding. Border discontinuities may be contaminated by commuting and firm relocation. Agreement across methods increases confidence; disagreement reveals where additional investigation is needed.

### 4. Pre-specify outcomes

The proposal identifies measures such as:

- employment and labor-force participation;
- earnings and hours;
- firm creation, survival, and closure;
- prices and business activity;
- benefit use and fiscal effects; and
- distributional outcomes across workers, sectors, and regions.

Pre-specification limits the temptation to define success after observing which metrics moved favorably.

### 5. Distinguish policy effects from implementation quality

A pilot can fail because its theory is wrong or because it was never implemented as designed. The architecture therefore needs both outcome measures and implementation measures: treatment intensity, timing, compliance, administrative performance, and exposure.

This distinction prevents two opposite errors—protecting a failed theory by blaming implementation indefinitely, or discarding a promising mechanism because delivery collapsed.

### 6. Establish decision gates

The proposal connects evidence to action. Results can trigger continuation, revision, expansion, pause, or sunset rather than producing a report that decision-makers are free to ignore.

A complete gate should specify:

- the outcome and measurement window;
- the minimum meaningful effect;
- unacceptable harms;
- data-quality requirements;
- who certifies the result; and
- what action follows each result.

### 7. Separate evaluation from authorization

Independent researchers and review panels assess the design and evidence. They do not make the final democratic decision. Evidence informs whether the proposal cleared its predefined test; elected or otherwise authorized institutions decide whether it should become permanent policy.

> **Suggested figure:** A horizontal lifecycle: Design → Pre-register → Match → Pilot → Measure → Independent review → Scale / Revise / Stop. Show feedback arrows from “Revise” to “Design.”

## What this demonstration establishes

The wage pilot shows that causal inference can shape policy language before enactment. It demonstrates how a proposal can define:

- a treatment;
- a comparison strategy;
- pre-treatment baselines;
- outcome and implementation measures;
- independent review;
- evidence gates; and
- explicit scale, revision, and sunset paths.

## What it does not establish

The draft does not prove that the proposed wage intervention will succeed. A design written on paper may still confront spillovers, political selection, noncompliance, insufficient sample size, measurement error, or weak external validity.

Nor should every public decision be reduced to a single estimated treatment effect. Distribution, rights, democratic commitments, and implementation feasibility remain substantive considerations.

## What a future team owns

A future team would decide:

- the intervention and affected population;
- the ethically and legally permissible assignment method;
- primary and secondary outcomes;
- minimum detectable and substantively meaningful effects;
- harm thresholds and stopping rules;
- evaluation independence and data access;
- the authority attached to an evaluation result; and
- whether the evidence supports scaling in a different context.

The reusable principle is simple: decide how the policy will learn before asking the public to live with it at scale.

## Underlying evidence

- [Regional Wage Modernization Pilot](../samples/Policy_Domains/labor-and-economic-security/regional-wage-modernization-pilot.md)
- [Labor maturity tracker](../samples/Policy_Domains/labor-and-economic-security/example_MATURITY_TRACKER.md)
- [Phase and metadata guide](../AI_Integrations/YAML_FRONTMATTER_GUIDE.md)
