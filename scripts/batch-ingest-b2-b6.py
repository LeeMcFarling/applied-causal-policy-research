#!/usr/bin/env python3
"""
Batch ingest for B.2–B.6 research sources.
Pipes pre-defined metadata answers to ingest-research.py non-interactively.
Run from the repo root.

Usage:
    python3 scripts/batch-ingest-b2-b6.py
    python3 scripts/batch-ingest-b2-b6.py --dry-run
    python3 scripts/batch-ingest-b2-b6.py --batch B.3   # single batch only
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "scripts" / "ingest-research.py"
PRESC = (
    REPO_ROOT
    / "research-library"
    / "incoming"
    / "Operating-System-Adversarial-Review-Literature"
    / "Prescriptions"
)

B2 = PRESC / "B.2 Capture, Personnel Rotation & Institutional Knowledge"
B3 = PRESC / "B.3 Sunset, Automatic Triggers, and Temporary Governance"
B4 = PRESC / "B.4 Regulatory Experimentation, Bundling Reform Architecture"
B5 = PRESC / "B.5 Electioral Systems, Coalitions, and Public Mandates"
B6 = PRESC / "B.6 Information Integrity and Transparency"

# Each entry: (batch_label, pdf_dir, pdf_filename, citation_key, [answers in prompt order])
# Prompt order: Authors, Title, Institution, City, Year, URL, Tags
SOURCES = [
    # ── B.2 ─────────────────────────────────────────────────────────────────
    (
        "B.2", B2,
        "4. Abbink — Staff Rotation as an Anti-Corruption Policy.pdf",
        "abbink-staff-rotation-anti-corruption-2004",
        [
            "Abbink, Klaus",
            "Staff Rotation as an Anti-Corruption Policy: An Experimental Study",
            "European Journal of Political Economy",
            "Nottingham",
            "2004",
            "",
            "anti-corruption,staff-rotation,regulatory-capture,experimental-economics,bribery,institutional-design",
        ],
    ),
    (
        "B.2", B2,
        "5. Agarwal et al. — Inconsistent Regulators.pdf",
        "agarwal-inconsistent-regulators-2012",
        [
            "Agarwal, Sumit, David Lucca, Amit Seru, and Francesco Trebbi",
            "Inconsistent Regulators: Evidence from Banking",
            "Federal Reserve Bank of Chicago / NBER",
            "Chicago, IL",
            "2012",
            "",
            "regulatory-capture,banking-supervision,regulatory-inconsistency,rotation-policy,state-capacity,institutional-design",
        ],
    ),
    (
        "B.2", B2,
        "6. Walsh & Ungson — Organizational Memory.pdf",
        "walsh-ungson-organizational-memory-1991",
        [
            "Walsh, James P., and Gerardo Rivera Ungson",
            "Organizational Memory",
            "Academy of Management Review",
            "Briarcliff Manor, NY",
            "1991",
            "https://www.jstor.org/stable/258607",
            "organizational-memory,institutional-knowledge,knowledge-retention,personnel-rotation,state-capacity",
        ],
    ),
    (
        "B.2", B2,
        "7. Brown & Duguid — Organizational Learning and Communities-of-Practice.pdf",
        "brown-duguid-organizational-learning-1991",
        [
            "Brown, John Seely, and Paul Duguid",
            "Organizational Learning and Communities-of-Practice: Toward a Unified View of Working, Learning, and Innovation",
            "Organization Science",
            "Catonsville, MD",
            "1991",
            "https://www.jstor.org/stable/2634938",
            "organizational-learning,communities-of-practice,tacit-knowledge,institutional-knowledge,knowledge-transfer",
        ],
    ),
    (
        "B.2", B2,
        "Argote & Fahrenkopf — Knowledge Transfer in Organizations.pdf",
        "argote-fahrenkopf-knowledge-transfer-2016",
        [
            "Argote, Linda, and Erin Fahrenkopf",
            "Knowledge Transfer in Organizations: The Roles of Members, Tasks, Tools, and Networks",
            "Organizational Behavior and Human Decision Processes",
            "Pittsburgh, PA",
            "2016",
            "",
            "knowledge-transfer,organizational-learning,institutional-knowledge,personnel-rotation,state-capacity,networks",
        ],
    ),
    (
        "B.2", B2,
        "B.2 - Makkai & Braithwaite -- In and out the Revolving Door.pdf",
        "makkai-braithwaite-revolving-door-1992",
        [
            "Makkai, Toni, and John Braithwaite",
            "In and Out the Revolving Door: Making Sense of Regulatory Capture",
            "Journal of Public Policy",
            "Cambridge",
            "1992",
            "",
            "regulatory-capture,revolving-door,regulatory-enforcement,institutional-design,anti-capture,personnel-rotation",
        ],
    ),
    # ── B.3 ─────────────────────────────────────────────────────────────────
    (
        "B.3", B3,
        "    Ranchordas — Sunset Clauses and Experimental Legislation Blessing or Curse.pdf",
        "ranchordas-sunset-clauses-2014",
        [
            "Ranchordas, Sofia",
            "Sunset Clauses and Experimental Legislation: Blessing or Curse for Innovation",
            "Tilburg University",
            "Tilburg",
            "2014",
            "https://research.tilburguniversity.edu/en/publications/77232cd7-d329-408e-91c1-1fefefdba42d",
            "sunset-clauses,experimental-legislation,regulatory-experimentation,temporary-governance,innovation,legislative-design",
        ],
    ),
    (
        "B.3", B3,
        "8. Beetsma et al. — Independent Fiscal Councils.pdf",
        "beetsma-independent-fiscal-councils-2018",
        [
            "Beetsma, Roel M.W.J., et al.",
            "Independent Fiscal Councils: Recent Trends and Performance",
            "International Monetary Fund",
            "Washington, D.C.",
            "2018",
            "",
            "fiscal-councils,independent-oversight,automatic-triggers,fiscal-governance,institutional-design,accountability",
        ],
    ),
    (
        "B.3", B3,
        "9. Jones & Quandt — An Iridescent Sunset.pdf",
        "jones-quandt-iridescent-sunset-2025",
        [
            "Jones, Tanner, and Ryan Quandt",
            "An Iridescent Sunset: An Empirical Analysis of Sunset Legislation",
            "Journal of Regulatory Economics",
            "New York, NY",
            "2025",
            "https://doi.org/10.1007/s11149-025-09498-5",
            "sunset-legislation,regulatory-review,automatic-triggers,temporary-governance,good-government,empirical-analysis",
        ],
    ),
    (
        "B.3", B3,
        "Dzuida & Loeper - Sunset Provisions.pdf",
        "dziuda-loeper-sunset-provisions-2024",
        [
            "Dziuda, Wioletta, and Antoine Loeper",
            "Sunset Provisions",
            "University of Chicago / Universidad Carlos III de Madrid",
            "Chicago, IL",
            "2024",
            "",
            "sunset-provisions,temporary-legislation,legislative-inertia,automatic-triggers,policy-expiration,regulatory-reform",
        ],
    ),
    # ── B.4 ─────────────────────────────────────────────────────────────────
    (
        "B.4", B4,
        "10. Wang & Zhou — Effectiveness of Regulatory Sandboxes.pdf",
        "wang-zhou-regulatory-sandboxes-2026",
        [
            "Wang, Yanqing, and Zijian Zhou",
            "Effectiveness of Regulatory Sandboxes in Financial Services: A Systematic Review",
            "Regulation & Governance",
            "London",
            "2026",
            "",
            "regulatory-sandboxes,fintech,regulatory-experimentation,innovation,financial-services,systematic-review",
        ],
    ),
    (
        "B.4", B4,
        "fahy- case-study-of-the-uks-regulatory-sandbox.pdf",
        "fahy-regulatory-sandbox-fintech-2022",
        [
            "Fahy, Lauren",
            "Regulator Reputation and Stakeholder Participation: A Case Study of the UK's Regulatory Sandbox for Fintech",
            "European Journal of Risk Regulation",
            "Cambridge",
            "2022",
            "",
            "regulatory-sandboxes,fintech,stakeholder-participation,regulator-reputation,regulatory-experimentation,UK",
        ],
    ),
    # ── B.5 ─────────────────────────────────────────────────────────────────
    (
        "B.5", B5,
        "11. Vowles, Banducci & Karp — Forecasting and Evaluating the Consequences of Electoral Change in New Zealand.pdf",
        "vowles-electoral-change-nz-2006",
        [
            "Vowles, Jack, Susan A. Banducci, and Jeffrey A. Karp",
            "Forecasting and Evaluating the Consequences of Electoral Change in New Zealand",
            "Acta Politica",
            "London",
            "2006",
            "",
            "electoral-systems,mixed-member-proportional,coalition-government,New-Zealand,electoral-reform,public-mandates",
        ],
    ),
    (
        "B.5", B5,
        "12. Gerber:Lupia:McCubbins — implementation of voter initiatives.pdf",
        "gerber-lupia-mccubbins-voter-initiatives-2011",
        [
            "Gerber, Elisabeth R., Arthur Lupia, and Mathew D. McCubbins",
            "Direct Democracy, Indirect Results: When Does Government Limit the Impact of Voter Initiatives?",
            "Political Research Quarterly",
            "Ann Arbor, MI",
            "2011",
            "https://ssrn.com/abstract=1002821",
            "direct-democracy,voter-initiatives,implementation,legislative-compliance,public-mandates,electoral-systems",
        ],
    ),
    # ── B.6 ─────────────────────────────────────────────────────────────────
    (
        "B.6", B6,
        "13. Martel & Rand — Fact-checker Warning Labels.pdf",
        "martel-rand-warning-labels-2023",
        [
            "Martel, Cameron, and David G. Rand",
            "Misinformation Warning Labels Are Widely Effective: A Review of Warning Effects and Their Moderating Features",
            "Current Opinion in Psychology",
            "Amsterdam",
            "2023",
            "",
            "misinformation,warning-labels,fact-checking,information-integrity,belief-correction,platform-governance",
        ],
    ),
    (
        "B.6", B6,
        "14. Ecker et al. — misinformation:correction review.pdf",
        "swire-ecker-misinformation-correction-2018",
        [
            "Swire, Briony, and Ullrich Ecker",
            "Misinformation and its Correction: Cognitive Mechanisms and Recommendations for Mass Communication",
            "University of Western Australia",
            "Perth",
            "2018",
            "",
            "misinformation,belief-correction,cognitive-mechanisms,information-integrity,mass-communication,debunking",
        ],
    ),
    (
        "B.6", B6,
        "15. Wang & Guan — Can Sunlight Disperse Mistrust?.pdf",
        "wang-guan-sunlight-mistrust-2023",
        [
            "Wang, Qiushi, and Zhen Guan",
            "Can Sunlight Disperse Mistrust? A Meta-Analysis of the Effect of Transparency on Citizens' Trust in Government",
            "Journal of Public Administration Research and Theory",
            "Oxford",
            "2023",
            "https://doi.org/10.1093/jopart/muac040",
            "transparency,government-trust,information-integrity,meta-analysis,public-administration,sunlight-provisions",
        ],
    ),
]


def run_ingest(pdf_path: Path, key: str, answers: list[str], dry_run: bool) -> bool:
    stdin_text = "\n".join(answers) + "\n"
    cmd = [sys.executable, str(SCRIPT), str(pdf_path), "--key", key]
    if dry_run:
        exists = "✓" if pdf_path.exists() else "MISSING"
        print(f"  [{exists}] {key}")
        print(f"    PDF: {pdf_path.name}")
        return pdf_path.exists()

    print(f"\n{'─' * 60}")
    print(f"Ingesting: {key}")
    result = subprocess.run(
        cmd,
        input=stdin_text,
        capture_output=False,
        text=True,
        cwd=REPO_ROOT,
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "scripts")},
    )
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--batch", help="run only this batch (e.g. B.3)")
    args = parser.parse_args()

    sources = SOURCES
    if args.batch:
        sources = [s for s in SOURCES if s[0] == args.batch]
        if not sources:
            print(f"No sources found for batch '{args.batch}'. Valid: B.2 B.3 B.4 B.5 B.6")
            sys.exit(1)

    ok, failed = 0, 0
    current_batch = None
    for batch, pdf_dir, filename, key, answers in sources:
        if batch != current_batch:
            current_batch = batch
            print(f"\n{'═' * 60}")
            print(f"  {batch}")
            print(f"{'═' * 60}")

        pdf_path = pdf_dir / filename
        if not pdf_path.exists():
            print(f"  MISSING: {filename}")
            failed += 1
            continue
        if run_ingest(pdf_path, key, answers, args.dry_run):
            ok += 1
        else:
            print(f"  FAILED: {key}")
            failed += 1

    print(f"\n{'=' * 60}")
    if args.dry_run:
        print(f"Dry run: {ok} found, {failed} missing.")
    else:
        print(f"Done. {ok} ingested, {failed} failed/missing.")


if __name__ == "__main__":
    main()
