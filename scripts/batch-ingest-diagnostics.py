#!/usr/bin/env python3
"""
Batch ingest for Diagnostics PDFs (Fukuyama, Kludgeocracy, Clean Water Act).
Run from the repo root.

Usage:
    python3 scripts/batch-ingest-diagnostics.py
    python3 scripts/batch-ingest-diagnostics.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "scripts" / "ingest-research.py"
DIAG = (
    REPO_ROOT
    / "research-library"
    / "incoming"
    / "Operating-System-Adversarial-Review-Literature"
    / "Diagnostics"
)

# Prompt order: Authors, Title, Institution, City, Year, URL, Tags
SOURCES = [
    (
        "Kludgeocracy.pdf",
        "teles-kludgeocracy-2012",
        [
            "Teles, Steven M.",
            "Kludgeocracy: The American Way of Policy",
            "New America Foundation",
            "Washington, D.C.",
            "2012",
            "",
            "kludgeocracy,complexity,policy-accumulation,institutional-design,state-capacity,reform,operating-system,administrative-state",
        ],
    ),
    (
        "Consequences of the Clean Water Act and the Demand for Water Quality.pdf",
        "keiser-shapiro-clean-water-act-2018",
        [
            "Keiser, David A., and Joseph S. Shapiro",
            "Consequences of the Clean Water Act and the Demand for Water Quality",
            "Center for Agricultural and Rural Development, Iowa State University",
            "Ames, IA",
            "2018",
            "",
            "clean-water-act,environmental-regulation,regulatory-effectiveness,water-quality,causal-identification,policy-evaluation",
        ],
    ),
    (
        "Political Order and Decay by Fukuyama 2014.pdf",
        "fukuyama-political-order-decay-2014",
        [
            "Fukuyama, Francis",
            "Political Order and Political Decay: From the Industrial Revolution to the Globalization of Democracy",
            "Farrar, Straus and Giroux",
            "New York, NY",
            "2014",
            "",
            "state-capacity,rule-of-law,accountability,political-decay,institutional-development,democracy,bureaucracy,operating-system,reform",
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
    args = parser.parse_args()

    ok, failed = 0, 0
    for filename, key, answers in SOURCES:
        pdf_path = DIAG / filename
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
