#!/usr/bin/env python3
"""
Batch-export all briefs in a domain (or all domains) to PDF.

Usage:
    python3 scripts/export-domain.py Healthcare
    python3 scripts/export-domain.py Budget_and_Fiscal_Policy --phase 2
    python3 scripts/export-domain.py --all
    python3 scripts/export-domain.py --all --phase 4 -o exports/

Options:
    --phase N    Only export briefs at phase N or above
    --all        Export all domains
    -o DIR       Output directory (default: exports/<domain>/)
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOMAINS_ROOT = REPO_ROOT / "guiding-principles" / "Policy_Domains"
EXPORT_SCRIPT = Path(__file__).parent / "export-brief.py"


def get_phase(md_file: Path) -> int:
    """Read phase from YAML frontmatter, return 0 if not found."""
    try:
        content = md_file.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if line.startswith("phase:"):
                val = line.split(":", 1)[1].strip()
                return int(val)
    except Exception:
        pass
    return 0


def get_briefs(domain_path: Path, min_phase: int = 0) -> list[Path]:
    briefs = []
    for md in domain_path.rglob("*.md"):
        if md.name == "_MATURITY_TRACKER.md":
            continue
        if "deprecated" in md.parts or "old" in str(md).lower():
            continue
        if min_phase > 0 and get_phase(md) < min_phase:
            continue
        briefs.append(md)
    return sorted(briefs)


def export_brief(md: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = output_dir / md.with_suffix(".pdf").name
    result = subprocess.run([
        sys.executable, str(EXPORT_SCRIPT),
        str(md), "-o", str(out_pdf),
    ])
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(
        description="Batch export FP domain briefs to PDF"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("domain", nargs="?", help="Domain folder name")
    group.add_argument("--all", action="store_true", help="Export all domains")
    parser.add_argument("--phase", type=int, default=0,
                        help="Minimum phase to include (default: all)")
    parser.add_argument("-o", "--output-dir",
                        help="Output directory (default: exports/<domain>/)")
    args = parser.parse_args()

    if args.all:
        domains = [d for d in DOMAINS_ROOT.iterdir() if d.is_dir()]
    else:
        domain_path = DOMAINS_ROOT / args.domain
        if not domain_path.exists():
            print(f"Domain not found: {domain_path}", file=sys.stderr)
            sys.exit(1)
        domains = [domain_path]

    total_ok = total_fail = 0

    for domain_path in sorted(domains):
        briefs = get_briefs(domain_path, min_phase=args.phase)
        if not briefs:
            continue

        if args.output_dir:
            out_dir = Path(args.output_dir) / domain_path.name
        else:
            out_dir = REPO_ROOT / "exports" / domain_path.name

        print(f"\n── {domain_path.name} ({len(briefs)} briefs) ──")

        for md in briefs:
            ok = export_brief(md, out_dir)
            if ok:
                total_ok += 1
            else:
                total_fail += 1

    print(f"\nDone. {total_ok} exported, {total_fail} failed.")


if __name__ == "__main__":
    main()
