#!/usr/bin/env python3
"""
One-shot batch ingest for B.1 State Capacity & Institutional Regeneration sources.
Pipes pre-defined metadata answers to ingest-research.py so each PDF is processed
non-interactively. Run from the repo root.

Usage:
    python3 scripts/batch-ingest-b1.py
    python3 scripts/batch-ingest-b1.py --dry-run   # print commands only
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "scripts" / "ingest-research.py"
B1_DIR = (
    REPO_ROOT
    / "research-library"
    / "incoming"
    / "Operating-System-Adversarial-Review-Literature"
    / "Prescriptions"
    / "B.1 State Capacity & Institutional Regeneration"
)

# Each entry: (pdf_filename, citation_key, [answers in prompt order])
# Prompt order: Authors, Title, Institution, City, Year, URL, Tags
SOURCES = [
    (
        "1. Aneja & Xu — Strengthening State Capacity.pdf",
        "aneja-xu-civil-service-state-capacity-2024",
        [
            "Aneja, Abhay, and Guo Xu",
            "Strengthening State Capacity: Civil Service Reform and Public Sector Performance",
            "American Economic Review",
            "Nashville, TN",
            "2024",
            "",  # URL — blank
            "civil-service-reform,state-capacity,pendleton-act,bureaucratic-autonomy,turnover,merit-based-hiring,institutional-regeneration",
        ],
    ),
    (
        "2. Christiansen & Klitgaard — Behind the Veil of Vagueness.pdf",
        "christiansen-klitgaard-veil-of-vagueness-2010",
        [
            "Christiansen, Thomas, and Robert Klitgaard",
            "Behind the Veil of Vagueness: Success and Failure in Institutional Reforms",
            "Journal of Public Policy",
            "Cambridge",
            "2010",
            "",
            "institutional-reform,veto-players,strategic-ambiguity,reform-sequencing,designated-losers,Denmark",
        ],
    ),
    (
        "3. Angelova et al. — Veto Player Theory and Reform Making in Western Europe.pdf",
        "angelova-veto-player-reform-2018",
        [
            "Angelova, Mariyana, Thomas König, and Sven-Oliver Proksch",
            "Veto Player Theory and Reform Making in Western Europe",
            "European Journal of Political Research",
            "Oxford",
            "2018",
            "",
            "veto-players,reform-making,Western-Europe,minimal-winning-coalition,crisis-driven-reform,ideological-distance",
        ],
    ),
    (
        "B.1 - Andrews, Pritchet, Woolcock - Escaping Capability Traps.pdf",
        "andrews-pritchett-woolcock-pdia-2012",
        [
            "Andrews, Matt, Lant Pritchett, and Michael Woolcock",
            "Escaping Capability Traps through Problem Driven Iterative Adaptation (PDIA)",
            "Harvard Kennedy School / Center for International Development",
            "Cambridge, MA",
            "2012",
            "",
            "capability-traps,isomorphic-mimicry,PDIA,iterative-adaptation,authorizing-environment,institutional-regeneration",
        ],
    ),
    (
        "B.1 - Huber and McCarty.pdf",
        "huber-mccarty-delegation-reform-2004",
        [
            "Huber, John D., and Nolan McCarty",
            "Bureaucratic Capacity, Delegation, and Political Reform",
            "American Political Science Review",
            "Washington, D.C.",
            "2004",
            "",
            "bureaucratic-capacity,delegation,political-reform,low-capacity-trap,formal-model,institutional-reform,bad-equilibrium,comprehensive-reform",
        ],
    ),
    (
        "B.1 : B.2 Outsourcing Bureaucracy.pdf",
        "rich-outsourcing-bureaucracy-2023",
        [
            "Rich, Jessica A. J.",
            "Outsourcing Bureaucracy to Evade Accountability: How Public Servants Build Shadow State Capacity",
            "American Political Science Review",
            "Washington, D.C.",
            "2023",
            "",
            "state-capacity,accountability,outsourcing,shadow-capacity,bureaucratic-effectiveness,accountability-capacity-tension,Brazil,pockets-of-effectiveness",
        ],
    ),
]


def run_ingest(pdf_path: Path, key: str, answers: list[str], dry_run: bool) -> bool:
    stdin_text = "\n".join(answers) + "\n"
    cmd = [
        sys.executable,
        str(SCRIPT),
        str(pdf_path),
        "--key", key,
    ]
    if dry_run:
        print(f"\n[DRY RUN] {key}")
        print(f"  PDF:  {pdf_path.name}")
        print(f"  stdin: {repr(stdin_text)}")
        return True

    print(f"\n{'─' * 60}")
    print(f"Ingesting: {key}")
    result = subprocess.run(
        cmd,
        input=stdin_text,
        capture_output=False,
        text=True,
        cwd=REPO_ROOT,
        env={**__import__("os").environ, "PYTHONPATH": str(REPO_ROOT / "scripts")},
    )
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ok, failed = 0, 0
    for filename, key, answers in SOURCES:
        pdf_path = B1_DIR / filename
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
    print(f"Done. {ok} ingested, {failed} failed/missing.")


if __name__ == "__main__":
    main()
