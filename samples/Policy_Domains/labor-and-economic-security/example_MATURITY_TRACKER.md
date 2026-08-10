# Domain Maturity Tracker: Labor_and_Economic_Security

**Last Updated:** 2026-05-19
**Overall Domain Phase:** 4–5
**Domain Owner:** TBD

---

## Phase Model Reference

- **Phase 0** – Problem Framing & Strategic Constraints
- **Phase 1** – Structured Exploration
- **Phase 2** – Architecture & Decision Rules
- **Phase 3** – Research Integration & Stress Testing
- **Phase 4** – Phasing & Implementation Design
- **Phase 5** – Publication-Ready Draft
- **Phase 6** – Expert Review
- **Phase 7** – Revision & Incorporation
- **Phase 8** – Public Messaging

---

## Domain Overview

**Purpose:**
Fix the structural failures that divorced American workers from the productivity gains of the economy they built — through wage restoration, benefits continuity, income smoothing, credential mobility, worker governance, and portable wealth formation. Each instrument does useful work independently; the full stack becomes dramatically more powerful when SSI, UPI, IRS modernization, and DoDA heatmap are live.

**Key Questions:**
- How do we guarantee every earned dollar leaves a household ahead (benefits cliff elimination)?
- How do we make work credentials portable without rebuilding the licensing system from scratch?
- How do we give workers formal standing in the decisions that determine their economic futures?

**Success Criteria:**
- Benefits gradient: zero households worse off for earning more across the federal stack
- Regional wage pilot: evidence-gated rollout with DoDA-certified evaluation before expansion
- Worker classification parity: dependent contractor arbitrage closed; payroll contributions normalized
- Credential portability: SSI-backed verification eliminates state-line licensing limbo

---

## Subdomain Status Matrix [SAMPLE OUTPUT]

| Subdomain | Phase | File Count | Word Count (est.) | Key Gaps | Dependencies | Next Action | Target Date |
|-----------|-------|------------|-------------------|----------|--------------|-------------|-------------|
| Domain_Overview | 4 | 1 | ~3,500 | — | SSI, DoDA heatmap | Prose complete | — |
| Wage_Modernization | 2 | 1 | ~4,000 | YAML modernization needed; sidebar_position missing; v0.1 | doda-regional-wage-heatmap, public-capital-authority | Fix YAML to domain standard | TBD |
| Income_Support | 4 | 1 | ~3,000 | — | doda-regional-wage-heatmap, healthcare-reform-sec-architecture | Prose complete  | — |
| Income_Smoothing | 4 | 1 | ~2,500 | — | irs-modernization-automated-income-attestation, upi-privacy-preserving-payment-rail | Prose complete | — |
| Wealth_Building | 4 | 1 | ~2,000 | — | universal-superannuation-system, worker-classification-parity | Prose complete | — |

---

## Cross-Domain Files in This Folder

| File | Declared Domain | Declared Subdomain | Notes |
|------|-----------------|--------------------|-------|
| credential-portability-and-competency-recognition.md | Economic_Prosperity | Labor_Mobility | Lives here; tracked under Economic_Prosperity/Labor_Mobility |

---

## Dependency Map

### Hard Dependencies (Blocking)
| This Domain Requires | From Domain | Status | Risk Level |
|---------------------|-------------|--------|------------|
| SSI credential infrastructure | Technology_and_Data | Phase 2 | Medium — pilots work without it; full capability requires it |

### Soft Dependencies (Coordination)
| This Domain Benefits From | From Domain | Status | Notes |
|--------------------------|-------------|--------|-------|
| Severe Event Coverage (SEC) architecture | Healthcare | Phase 2 | Benefits gradient Medicaid bridge destination |

### Provides To (Downstream Impact)
| Other Domain | What We Provide | Criticality |
|--------------|-----------------|-------------|
| Economic_Prosperity | Wage floor stabilization, labor cost predictability, workforce mobility | High |
| Healthcare | Medicaid bridge design, portable HTA contributions, worker financial stability | High |
| Housing | Stable income = stable housing; STZ corridor workforce pipeline | High |
| Manufacturing / IDP | Credential portability for domestic and allied-nation workforce | Medium |

---

## Gap Analysis [SAMPLE OUTPUT]

### Tier 1: Critical Gaps (Missing Foundation)
- [x] **Benefits cliff elimination** — Benefits Gradient Modernization Act: 60-cent floor, regional calibration, Medicaid bridge 
- [x] **Worker classification** — Dependent contractor arbitrage closed; payroll contribution parity 
- [x] **Income smoothing** — Real-time EITC/CTC delivery: replaces annual lump-sum with continuous stabilization 

### Tier 2: Structural Gaps (Incomplete Coverage) 
- [x] **Workforce stabilization pilots** — workforce-stabilization-pilot.md: transitional housing/workforce integration for people who've fallen out of the labor market; cross-domain with Social/Homelessness stack 
- [ ] **NLRA / union policy relationship** — How does these policies interact with existing collective bargaining rights? 

### Tier 3: Enhancement Gaps (Nice-to-Have)
- [ ] **Gig worker organizing infrastructure** — Classification parity closes the cost arbitrage but doesn't address collective voice for independent workers — Target: Phase 3

---

## Phase Advancement Checklist [SAMPLE OUTPUT]

### Requirements for Phase 5 (External Validation) — Active Next Step
- [x] Full instrument stack documented and sequenced (overview v0.3 complete)
- [x] Employer-facing communication drafted (employer letter v0.3)
- [x] Workforce stabilization brief developed (workforce-stabilization-pilot.md v0.2) 
- [x] Enforcement architecture defined (labor-stack-enforcement-framework-v0.2.md) 

---

## YAML Issues Log [SAMPLE OUTPUT]

| File | Issue | Priority |
|------|-------|----------|
| regional-wage-modernization-pilot.md | Old YAML format: domain `"Labor, Wages, and Economic Security"` (wrong) | High |
| worker-classification-partity.md | Filename typo: "partity" should be "parity" | Low — functional, may affect slug/link |

---

## Recent Activity Log [SAMPLE OUTPUT]

| Date | Subdomain | Change | Phase Impact |
|------|-----------|--------|--------------|
| 2026-05-19 | Enforcement, Workforce_Transition | Tracker updated: 1 new files added (labor-stack-enforcement-framework-v0.2.md ~3,159 words) | 1 Tier 1 gaps closed |

---

## Notes & Context [SAMPLE OUTPUT]

- New standalone domain — previously combined under two domains
- Employer letter at Phase 5 — external stakeholder communication already drafted
- Wage_Modernization subdomain (regional-wage-modernization-pilot.md) needs YAML standardization — currently uses old non-standard format
