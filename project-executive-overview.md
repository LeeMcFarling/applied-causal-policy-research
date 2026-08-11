# Policy Research Project  - Computational Governance

**What if you could ingest research from every major think tank and research organization in the country, stress-test it against a complete policy platform, and use that synthesis to build the reform architecture that the next administration actually needs?**

That is the central question this repository is designed to answer.

This is a machine-readable policy repository encompassing four integrated layers of governance reform — foundational theory, institutional redesign, technological infrastructure, and domain policy — built to work coherently together as a single system. Every document is structured for both human reading and computational analysis: YAML-indexed, phase-gated, cross-referenced by dependency, tagged by audience, and validated against independent research.

> **Demonstration scope:** The included briefs are excerpts selected to demonstrate the repository's methods. They are not a ready-made agenda or a substitute for a future team's judgment. The architecture is intended to help teams develop, test, connect, and revise their own policies; those teams retain responsibility for the substance and final decisions.

---

## The Problem This Is Trying to Solve

Any administration taking office in 2029 faces a specific dilemma.

Voters have repeatedly signaled that they need real change — in healthcare, wages, housing, and the basic credibility of democratic governance. And a rising share of the electorate has made clear that anything other than genuinely populist governance will not be tolerated.

The track record on populism, however, has not been kind. Economic analysis has projected that populist governments routinely produce economic growth approximately 10% lower than their counterfactuals, and populist leaders tend to stay in power at twice the rate of their peers.[^1] Meeting this moment requires a platform that is *populist in ambition* — with changes that are real and felt quickly — and *extraordinarily regimented in execution* to avoid the failures of similar movements in the past.

That administration also inherits a specific set of structural constraints, many of which are approaching historic levels for the United States:

- A debt-to-GDP ratio near the post-WWII peak,[^2] which both limits headroom and makes the fiscal status quo untenable
- Wealth concentration nearing historic peaks, with the political instability that historically accompanies it[^3]
- A radicalization and partisan violence dynamic that cannot be addressed through communication alone[^4]
- Democratic institutions under stress from electoral, regulatory, and revolving-door capture

And four decades of previous governance has produced a hollowed industrial base, suppressed wages, and a working population with every rational reason to distrust the people asking for their vote. A platform that doesn't take that seriously will not survive contact with the electorate it needs to deliver a governing majority. The window for delivering this change is probably one presidential term.

Any platform that seeks to solve these problems must work to solve each layer simultaneously. It cannot merely be a collection of policy papers, but rather a complete and integrated reform architecture — designed to deliver changes voters feel in the first year while sequencing the structural reforms that compound over two, four, and eight years.Additionally, each reform across every domain must be phase-gated, stress-tested against existing research, and built into a system that reflects the gaps and dependencies that reflect how these reforms function in real life. 

This project seeks to elucidate that backend structure so that any future administration has the legibility to see how it's labor domain effects its healthcare reforms -- how it's national security reforms effect its industrial policy -- and how each of those reforms compare to current research. 

---

## How This Repository Works

The first key to unlocking this functionality lies in the structure of the reform proposals themselves. Each proposal has a machine readable structure with YAML frontmatter that allows each specific policy to be connected to each other via traditional foreign-key links, tagged with audiences, implementation strategies, dependencies, gaps, versioning, phasing, and more. 

An example of this machine readable structure is below: 

```yaml
---
title: "Regional Wage Modernization Pilot"
domain: Labor_and_Economic_Security
subdomain: Wage_Modernization
phase: 1
layer: 4
version: 0.1
audiences:
  - working-class
  - rural-america
  - veterans
dependencies:
  - doda-regional-wage-heatmap
  - public-capital-authority
description: >
  Establishes a controlled, evidence-gated pathway for raising regional wage
  floors — calibrated by commuting zone, phased in through a multi-year onramp,
  and scaled only after DoDA-certified evaluation against matched comparison
  regions.
---
```

As stated earlier, these fields enable automatic dependency mapping, phase validation, audience targeting, maturity assessment, and cross-domain gap analysis across all briefs in the repository.

### The 9-Phase Development Model

Every brief is assigned a development phase with explicit gate conditions:

| Phase | Name | What It Requires |
|-------|------|-----------------|
| 0 | Problem Framing | Problem scoped, constraints documented |
| 1 | Structured Exploration | Options surveyed, analogues reviewed |
| 2 | Architecture & Decision Rules | Mechanism specified, internally consistent |
| 3 | Research Integration | Literature reviewed, divergences documented |
| 4 | Pilot & Day One Designation | Tagged with implementation constraints re: EO, congressional mandate, etc. | 
| 5 | Phasing & Implementation Design | Execution sequence, cost estimates, legislative vehicle |
| 6 | Publication-Ready Draft | Citations complete, prose clean |
| 7 | Expert Review | External feedback gathered |
| 8 | Revision & Incorporation | Feedback incorporated or rebutted |
| 9 | Public Messaging | Framing, rebuttal prep, earned media |

A brief cannot exceed the phase of its hard dependencies. Phase 3 is now active: ingested research from RAND, Brookings, Niskanen, Urban Institute, and others is processed through a structured review pipeline that produces adversarial receipts — documenting what the research confirms, where it's silent, where it diverges, and what remains unresolved.

### Validation Layers

The repository builds in three independent stress-test layers:

1. **Red-team testing**: LLM-driven simulation of adversarial review from both right-leaning and left-leaning perspectives, identifying the strongest objections to each mechanism
2. **Research pre-validation**: Structured comparison against peer-reviewed literature and institutional research (RAND, Brookings, Niskanen, Urban Institute, Grattan, CSBA) — documented in `research-library/reviews/`
3. **Expert review**: Phase 6 external feedback from domain practitioners before any brief reaches publication

The goal is that by the time any brief becomes public-facing, it has been stress-tested against the strongest available counterarguments and the best available evidence — and all divergences are documented transparently.

### Modular Publication

Each brief is designed to stand alone. The repository is modular by design so that individual domains, subdomains, or specific instruments can be published, shared with experts, or adapted independently — without requiring the entire platform to be released or finalized.

---

## The Four Layers

The platform is organized into four layers, each enabling the next. Most reform platforms only operate at Layer 4. This one builds the layers underneath first, because a great policy deployed into a broken government, on outdated infrastructure, without understanding how different populations will experience it, produces the same failures we've seen over the past several decades.

### Layer 1 — Theory (`guiding-principles/Foundations/`)

The theoretical backbone addresses why societies destabilize, what structural conditions reduce that risk, and how policy instruments should be designed to reduce radicalization rather than accelerate it.

The starting point is decades of research in Terror Management Theory: when people feel existentially threatened, they pull toward their own groups, grow suspicious of outsiders, and become more receptive to strongman narratives.[^5] Critically, an attack on one's worldview — including seeing one's beliefs criticized online — triggers the same psychological responses as mortality reminders.[^6] These responses map directly onto the radicalization pattern playing out across the United States.

This platform treats that research as a design constraint. For any contested issue, the design process starts by identifying the underlying threats people are reacting to — economic insecurity, cultural displacement, institutional betrayal — and builds instruments that directly address those instead of splitting the difference between opposing positions. Where a policy would be experienced as a threat to the psychological anchors people rely on, the design is changed. Not because the intent was wrong, but because a policy that triggers the defensive response it was designed to address has already failed on its own terms.

The same logic applies institutionally: stable societies provide citizens with diversified pathways toward economic stability, meaning, belonging, and contribution. When those pathways collapse — through recession, culture wars, or institutional failure — populations become susceptible to authoritarian appeals. This platform is designed to rebuild those conditions.

### Layer 2 — The Operating System (`guiding-principles/Operating-System/`)

The United States government is constantly and simultaneously accused of being too large, too small, too expensive, too complex, and too ineffective at producing outcomes. Agencies have accumulated procedural complexity as a defense against decades of past abuses, bringing their operational throughput to a crawl. Programs persist because they were authorized, not because they work. Jurisdiction is fragmented across federal, state, and local levels without proper interfacing. Accountability is indirect, delayed, and filtered through a partisan media environment. The result: a government highly capable of sabotaging its own activity and nearly incapable of producing anything quickly or at scale.[^8]

This platform treats that as a systems engineering problem. The Operating System layer creates new institutional machinery to translate democratic mandates into measurable outcomes — not by replacing Congress, but by giving it tools that actually work.

**The Execution Corps** is the primary engine: deployable institutional units engineered by inverting the contractor model — instead of private contractors embedding in government, government deploys directly to the physical and bureaucratic sites where it's trying to build. Each Corps unit is bounded by Congressional charter, sunset-mandated when the mission is complete, and built with anti-capture features from day one: non-renewable leadership terms, mandatory rotations, contractor-inversion rules, and cooling-off periods.

**The Regulatory Modernization Corps (RMC)** treats regulation as critical software — version-controlled, dependency-mapped, testable in sandbox corridors before changes are merged into the regulatory codebase. When a blocker surfaces, the RMC resolves it in real time rather than waiting years for a legislative correction.

**The Public Capital Authority (PCA)** replaces two broken deployment mechanisms — an appropriations process that micromanages every dollar and a tax code that functions as a shadow budget no one can fully model — with a development bank that deploys capital through instruments that are explicit, auditable, and designed to recycle taxpayer dollars rather than consume them.

**The Department of Data and Accountability (DoDA)** is the independent measurement body that certifies whether execution instruments have hit their predefined performance thresholds. Congress writes the test. Execution instruments run the experiment. DoDA grades the result. It is this certification that triggers whether systems scale or sunset — and it is this body that publishes standardized dashboards legible to Congress, press, and public.

### Layer 3 — Infrastructure (`guiding-principles/Infrastructure/`)

Government cannot function effectively in the 21st century because it is built on technology from the mid-20th century. The infrastructure layer does four things: modernizes front-door service delivery, upgrades identity verification so it doesn't require broadcasting sensitive information, creates payment rails that don't require transmitting raw financial credentials, and deploys modern fraud detection on the back end rather than adding procedural overhead that slows legitimate users and fails to stop fraud.

**Self-Sovereign Identity (SSI)** replaces the SSN system's centralized legacy architecture with a decentralized identity framework built on W3C standards[^9] and NIST guidelines[^10] already in production across the EU Digital Identity Framework.[^11] It enables everything from real-time benefits eligibility to pharmaceutical pricing attestation to immigration compliance — without privacy exposure, fraud risk, or administrative overhead.

**The Unified Payment Interface (UPI)** applies the same principles to payments: built on the peer-to-peer settlement architecture that India's UPI has operated at scale since 2016,[^12] but routed through SSI rails rather than centralized databases. Users keep their existing accounts; they stop needing to transmit the underlying numbers to make or receive payments.

**The Immutable Government Ledger** applies the fraud detection logic that financial institutions already use at scale — scanning billions of transactions in real time — to government spending. Every dollar gets tied to a cryptographic SSI attestation at the moment it's spent. The ledger is immutable: a loophole exploited today commits transaction fingerprints to a permanent record that every future iteration of fraud detection models will scan.

### Layer 4 — Policy Domains (`guiding-principles/Policy_Domains/`)

The substantive content: ~313 briefs across 18 domains. Every reform is designed according to the theory, deployed through the operating system, and built to run on the infrastructure.

| Domain | Phase | Files |
|--------|-------|-------|
| Labor_and_Economic_Security | 4–5 | 12 |
| Healthcare | 4 | 32 |
| Social | 2 | 24 |
| Manufacturing | 2 | 28 |
| Education | 2 | 18 |
| Democratic_Integrity | 2 | 15 |
| National_Security | 2 | 37 |
| Budget_and_Fiscal_Policy | 2 | 16 |
| Housing_and_Public_Infrastructure | 2 | 20 |
| Trade_Policy | 2 | 8 |
| Agriculture | 2 | 8 |
| Energy | 2 | 7 |
| Climate_Risk | 2 | 4 |
| Immigration | 1–2 | 14 |
| United-Nations-and-Global-Institutional-Reform | 1–2 | 7 |
| Sports_and_Cultural_Institutions | 1 | — |

---

## Repository Structure

```
applied-causal-policy-research/
├── README.md                          ← This file
├── PROJECT_STATUS.md                  ← Full domain matrix, gap analysis, recent activity
├── TECHNICAL_OVERVIEW.md              ← Human-facing architecture reference
│
├── guiding-principles/
│   ├── Foundations/                  ← L1: Theory stack
│   ├── Operating-System/             ← L2: Execution instruments 
│   ├── Infrastructure/               ← L3: Technical backbone
│   └── Policy_Domains/               ← L4: 18 policy domains
│       ├── Healthcare/
│       ├── Labor_and_Economic_Security/
│       ├── Manufacturing/
│       └── [15 more domains...]
│
├── research-library/
│   ├── incoming/                      ← PDF drop zone
│   ├── sources/                       ← Ingested research (PDF→MD with Chicago citation YAML)
│   ├── reviews/                       ← Adversarial review documents (4-section format)
│   └── index.md                       ← Source catalog
│
├── scripts/
│   ├── export-brief.py               ← Single brief → PDF (xelatex, Chicago footnotes)
│   ├── export-domain.py              ← Batch export by domain + phase filter
│   ├── ingest-research.py            ← PDF → research-library/sources/ (pdfplumber)
│   ├── maturity_scan.py              ← Scan repo, update maturity trackers
│   └── templates/
│       └── policy-brief.tex       ← LaTeX template (Georgia/Helvetica, navy cover)
│
└── AI_Integrations/
    ├── YAML_FRONTMATTER_GUIDE.md     ← Authoritative field reference (phases, layers, audiences)
    ├── AUTOMATION_README.md          ← Script usage, Phase 3 workflow, PDF export
    └── PRIMARY_CONTROL_DOC.md        ← AI session context and workflow instructions
```

---

## Working with the Repository

### Export a brief to PDF
```bash
python3 scripts/export-brief.py guiding-principles/Policy_Domains/Healthcare/care-delivery-market-design.md --open
```

### Batch export a domain
```bash
python3 scripts/export-domain.py Labor_and_Economic_Security --phase 4
```

### Ingest a research source
```bash
python3 scripts/ingest-research.py research-library/incoming/rand-report.pdf
```

### Scan the repository and update maturity trackers
```bash
python3 scripts/maturity_scan.py scan
```

### Requirements
```bash
pip install pyyaml pdfplumber
brew install pandoc
brew install --cask mactex-no-gui  # for PDF export
```

---

## Current Status

**18 domains | 4 layers**

Most domains are at Phase 2 (Architecture & Decision Rules) — mechanisms are specified and internally consistent. Healthcare and Labor are the furthest ahead at Phase 5 (Phasing & Implementation Design). Phase 3 research integration is now active; the Community Stabilization brief is the first to reach Phase 4 (Pilot Target & Day One Designation) with a fully specified 5-city executive pilot.

See [PROJECT_STATUS.md](./PROJECT_STATUS.md) for the full domain matrix, subdomain breakdown, gap analysis, and recent activity.

---

## Experimental Governance Philosophy

The platform proposes to govern itself by the same principles it advocates. Reforms are phase-gated: no brief advances to Phase 4 (Pilot Target) without completing Phase 3 research integration, and no brief reaches Phase 5 without answering "what can be done on Day One via executive action." No execution instrument scales without a predefined performance threshold certified by an independent body. No domain overview gets published without the underlying brief stack being sufficiently developed.

The goal is a platform that can be handed to an external expert in any domain and survive adversarial scrutiny — not because it has all the answers, but because it documents its reasoning, acknowledges its uncertainties, and shows its work.

---

## Notes

[^1]: Funke, M., Schularick, M., & Trebesch, C. (2023). Populist Leaders and the Economy. *The American Economic Review*, 113(12), 3249–3288. https://doi.org/10.1257/aer.20202045

[^2]: U.S. Department of the Treasury, Bureau of the Fiscal Service, "Understanding the National Debt," Fiscal Data, accessed May 26, 2026, https://fiscaldata.treasury.gov/americas-finance-guide/national-debt/

[^3]: Emmanuel Saez and Gabriel Zucman, "Wealth Inequality in the United States since 1913: Evidence from Capitalized Income Tax Data," NBER Working Paper No. 20625, National Bureau of Economic Research, October 2014.

[^4]: Ned Parker and Peter Eisler, "New Cases of Political Violence Roil US Ahead of Contentious Election," Reuters, October 21, 2024, https://www.reuters.com/world/us/new-cases-political-violence-roil-us-ahead-contentious-election-2024-10-21/

[^5]: Tom Pyszczynski, "Terror Management of Fear, Hate, Political Conflict, and Political Violence: A Review," *Testing, Psychometrics, Methodology in Applied Psychology* 20, no. 4 (2013): 313–326.

[^6]: Schimel J, Hayes J, Williams T, Jahrig J. Is death really the worm at the core? Converging evidence that worldview threat increases death-thought accessibility. *J Pers Soc Psychol.* 2007 May;92(5):789–803.

[^7]: Klein, E., & Thompson, D. (2025). *Abundance: How Progress Takes Power and Plenty Defeats Populism.* Avid Reader Press.

[^8]: Fukuyama, F. (2014). *Political Order and Political Decay.* Farrar, Straus and Giroux.

[^9]: World Wide Web Consortium, *Verifiable Credentials Data Model v2.0*, W3C Recommendation, May 15, 2025, https://www.w3.org/TR/vc-data-model-2.0/

[^10]: National Institute of Standards and Technology, *Digital Identity Guidelines*, NIST Special Publication 800-63-4, 2025.

[^11]: European Parliament and Council of the European Union, Regulation (EU) 2024/1183, April 30, 2024.

[^12]: Reserve Bank of India, "UPI Product Statistics," National Payments Corporation of India, accessed 2026.
