#!/usr/bin/env python3
"""
Policy Research Repository — Maturity Tracker Automation Script

Scans the policy repository and updates maturity trackers for each domain.

Usage:
    python maturity_scan.py [command] [options]

Commands:
    scan            Scan all domains and update maturity trackers
    report          Generate overall project status report
    gaps            Analyze and report gaps across all domains
    validate        Check for phase violations and missing required fields
"""

import os
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional

# ─── Configuration ────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = REPO_ROOT / "guiding-principles" / "Policy_Domains"
TRACKER_FILENAME = "_MATURITY_TRACKER.md"
PROJECT_STATUS_FILE = REPO_ROOT / "PROJECT_STATUS.md"

# ─── Phase Model (0–9) ────────────────────────────────────────────────────────
PHASES = {
    0: "Problem Framing",
    1: "Structured Exploration",
    2: "Architecture & Decision Rules",
    3: "Research Integration & Stress Testing",
    4: "Pilot Target & Day One Designation",
    5: "Phasing & Implementation Design",
    6: "Publication-Ready Draft",
    7: "Expert Review",
    8: "Revision & Incorporation",
    9: "Public Messaging",
}

# Phase gate requirements — fields/conditions that must be present at each phase
PHASE_GATES = {
    4: {
        "required_fields": ["eo-pilot-target"],
        "description": "Phase 4 requires eo-pilot-target field (true/false)",
    },
    5: {
        "required_fields": ["eo-pilot-target"],
        "description": "Phase 5 requires eo-pilot-target field",
    },
    6: {
        "required_fields": ["eo-pilot-target"],
        "requires_citations": True,
        "description": "Phase 6+ requires eo-pilot-target and inline citations ([^N])",
    },
    7: {
        "required_fields": ["eo-pilot-target"],
        "requires_citations": True,
        "description": "Phase 7 requires eo-pilot-target and inline citations",
    },
    8: {
        "required_fields": ["eo-pilot-target"],
        "requires_citations": True,
        "description": "Phase 8 requires eo-pilot-target and inline citations",
    },
    9: {
        "required_fields": ["eo-pilot-target"],
        "requires_citations": True,
        "description": "Phase 9 requires eo-pilot-target and inline citations",
    },
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def extract_frontmatter(file_path: Path) -> Optional[Dict]:
    """Extract YAML frontmatter from a markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1]) or {}
    except Exception as e:
        print(f"  Warning: Could not parse frontmatter in {file_path.name}: {e}")
    return None


def extract_body(file_path: Path) -> str:
    """Return the document body (everything after the frontmatter)."""
    try:
        content = file_path.read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return parts[2]
        return content
    except Exception:
        return ""


def count_words(file_path: Path) -> int:
    """Count words in the body of a markdown file."""
    body = extract_body(file_path)
    body = re.sub(r"[#*`\[\]()_~]", "", body)
    return len(body.split())


def has_citations(file_path: Path) -> bool:
    """Check for at least one Chicago-style footnote ([^N]: ...)."""
    body = extract_body(file_path)
    return bool(re.search(r"\[\^[^\]]+\]:", body))


def is_policy_file(f: Path) -> bool:
    """True for markdown files that are policy briefs (not trackers, not READMEs)."""
    return (
        f.suffix == ".md"
        and f.name != TRACKER_FILENAME
        and not f.name.startswith("_")
        and f.name.lower() != "readme.md"
    )


# ─── Domain Scanning ──────────────────────────────────────────────────────────

def scan_domain(domain_path: Path) -> Dict:
    """
    Recursively scan a domain directory.
    Returns a dict of per-file data and aggregate metrics.
    """
    domain_name = domain_path.name

    # Recursive scan — policy files can live in nested subdirectories
    md_files = [f for f in domain_path.rglob("*.md") if is_policy_file(f)]

    files_data = []
    subdomains: Dict[str, Dict] = defaultdict(lambda: {
        "files": [],
        "total_words": 0,
        "phases": set(),
        "dependencies": [],
        "layers": set(),
    })

    for md_file in md_files:
        fm = extract_frontmatter(md_file)
        word_count = count_words(md_file)
        citations = has_citations(md_file)

        phase = 0
        subdomain = md_file.parent.name if md_file.parent != domain_path else domain_name
        layer = None
        eo_pilot_target = None
        day_one_action = None
        deps = []

        if fm:
            phase = int(fm.get("phase", 0))
            subdomain = fm.get("subdomain", subdomain)
            layer = fm.get("layer")
            eo_pilot_target = fm.get("eo-pilot-target")
            day_one_action = fm.get("day-one-action")
            deps = fm.get("dependencies", []) or []

        files_data.append({
            "path": md_file,
            "name": md_file.name,
            "phase": phase,
            "subdomain": subdomain,
            "layer": layer,
            "word_count": word_count,
            "has_citations": citations,
            "eo_pilot_target": eo_pilot_target,
            "day_one_action": day_one_action,
            "dependencies": deps,
            "frontmatter": fm,
        })

        subdomains[subdomain]["files"].append(md_file.name)
        subdomains[subdomain]["total_words"] += word_count
        subdomains[subdomain]["phases"].add(phase)
        subdomains[subdomain]["dependencies"].extend(deps)
        if layer:
            subdomains[subdomain]["layers"].add(layer)

    return {
        "name": domain_name,
        "path": domain_path,
        "file_count": len(md_files),
        "files_data": files_data,
        "subdomains": dict(subdomains),
        "total_words": sum(f["word_count"] for f in files_data),
    }


def calculate_domain_phase(domain_data: Dict) -> int:
    """Domain phase = minimum phase across all files (conservative)."""
    phases = [f["phase"] for f in domain_data["files_data"]]
    return min(phases) if phases else 0


# ─── Validation ───────────────────────────────────────────────────────────────

def validate_file(file_data: Dict) -> List[str]:
    """Return a list of gate violations for a single file."""
    violations = []
    phase = file_data["phase"]
    name = file_data["name"]

    gate = PHASE_GATES.get(phase)
    if not gate:
        return violations  # No gate requirements for this phase

    fm = file_data["frontmatter"] or {}

    # Check required YAML fields
    for field in gate.get("required_fields", []):
        if field not in fm or fm[field] is None:
            violations.append(f"{name} (Phase {phase}): missing required field `{field}`")

    # Check citations requirement
    if gate.get("requires_citations") and not file_data["has_citations"]:
        violations.append(f"{name} (Phase {phase}): Phase 6+ requires at least one footnote citation ([^N]: ...)")

    # Phase 4 specific: if eo-pilot-target is True, day-one-action should be set
    if phase >= 4:
        eo = fm.get("eo-pilot-target")
        if eo is True and not fm.get("day-one-action"):
            violations.append(f"{name} (Phase {phase}): eo-pilot-target is true but day-one-action is not set")

    return violations


# ─── Tracker Generation ───────────────────────────────────────────────────────

def update_maturity_tracker(domain_data: Dict):
    """Write or update the _MATURITY_TRACKER.md for a domain."""
    tracker_path = domain_data["path"] / TRACKER_FILENAME
    domain_name = domain_data["name"]
    overall_phase = calculate_domain_phase(domain_data)

    # Preserve manual notes from existing tracker
    manual_notes = ""
    if tracker_path.exists():
        existing = tracker_path.read_text(encoding="utf-8")
        if "## Notes" in existing and "_Auto-generated" in existing:
            manual_notes = existing.split("_Auto-generated", 1)[1].split("\n\n", 1)[-1]

    # Subdomain table
    table_rows = []
    for subdomain_name, sd in sorted(domain_data["subdomains"].items()):
        phase = min(sd["phases"]) if sd["phases"] else 0
        file_count = len(sd["files"])
        word_count = sd["total_words"]
        layers = ", ".join(f"L{l}" for l in sorted(sd["layers"])) or "—"

        status = "Not started"
        if file_count > 0 and word_count < 500:
            status = "Stub"
        elif file_count > 0:
            status = f"Phase {phase} — {PHASES.get(phase, '?')}"

        next_action = "Create initial file" if file_count == 0 else f"Advance to Phase {min(phase + 1, 9)}"

        table_rows.append(
            f"| {subdomain_name} | {phase} | {layers} | {file_count} | {word_count:,} | {status} | {next_action} |"
        )

    table = "\n".join(table_rows) if table_rows else \
        "| No subdomains yet | 0 | — | 0 | 0 | Not started | Initialize domain |"

    # Violation list
    all_violations = []
    for fd in domain_data["files_data"]:
        all_violations.extend(validate_file(fd))

    violation_text = ""
    if all_violations:
        violation_text = "\n".join(f"- ⚠️  {v}" for v in all_violations)
    else:
        violation_text = "- ✅ No phase gate violations detected"

    content = f"""# Domain Maturity Tracker: {domain_name}

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Overall Domain Phase:** {overall_phase} — {PHASES.get(overall_phase, '?')}
**Total Files:** {domain_data['file_count']}
**Total Words:** {domain_data['total_words']:,}

---

## Phase Model Reference

| Phase | Name |
|-------|------|
| 0 | Problem Framing |
| 1 | Structured Exploration |
| 2 | Architecture & Decision Rules |
| 3 | Research Integration & Stress Testing |
| 4 | Pilot Target & Day One Designation |
| 5 | Phasing & Implementation Design |
| 6 | Publication-Ready Draft |
| 7 | Expert Review |
| 8 | Revision & Incorporation |
| 9 | Public Messaging |

---

## Subdomain Status

| Subdomain | Phase | Layer | Files | Words | Status | Next Action |
|-----------|-------|-------|-------|-------|--------|-------------|
{table}

---

## Phase Gate Validation

{violation_text}

---

## Notes

_Auto-generated — add manual notes below this line:_

{manual_notes}"""

    tracker_path.write_text(content, encoding="utf-8")
    print(f"  ✓ {domain_name}")


# ─── Commands ─────────────────────────────────────────────────────────────────

def cmd_scan():
    """Scan all domains, update maturity trackers, regenerate PROJECT_STATUS.md."""
    print(f"\nScanning domains in {DOMAINS_DIR.relative_to(REPO_ROOT)}...\n")

    if not DOMAINS_DIR.exists():
        print(f"Error: domains directory not found at {DOMAINS_DIR}")
        sys.exit(1)

    domain_dirs = [d for d in DOMAINS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    all_domains = []

    for d in sorted(domain_dirs):
        domain_data = scan_domain(d)
        all_domains.append(domain_data)
        update_maturity_tracker(domain_data)

    _write_project_status(all_domains)
    total_words = sum(d["total_words"] for d in all_domains)
    total_files = sum(d["file_count"] for d in all_domains)
    print(f"\nDone — {len(all_domains)} domains · {total_files} files · {total_words:,} words")


def cmd_gaps():
    """Report gaps by tier across all domains."""
    print(f"\nGap analysis — {DOMAINS_DIR.relative_to(REPO_ROOT)}\n")

    domain_dirs = [d for d in DOMAINS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]

    tier1, tier2, tier3 = [], [], []

    for d in sorted(domain_dirs):
        dd = scan_domain(d)
        fc, wc = dd["file_count"], dd["total_words"]
        phase = calculate_domain_phase(dd)

        if fc == 0:
            tier1.append(dd["name"])
        elif fc <= 2 or wc < 1000:
            tier2.append((dd["name"], phase, fc, wc))
        elif wc < 5000:
            tier3.append((dd["name"], phase, fc, wc))

    print("## Tier 1 — No coverage")
    for n in tier1:
        print(f"  - {n}")

    print("\n## Tier 2 — Skeletal (≤2 files or <1k words)")
    for n, ph, fc, wc in tier2:
        print(f"  - {n}  [Phase {ph}]  {fc} files · {wc:,} words")

    print("\n## Tier 3 — Thin (<5k words)")
    for n, ph, fc, wc in tier3:
        print(f"  - {n}  [Phase {ph}]  {fc} files · {wc:,} words")

    if not (tier1 or tier2 or tier3):
        print("  No gaps detected across tracked thresholds.")


def cmd_validate():
    """Check all files for phase gate violations."""
    print(f"\nValidating phase gates — {DOMAINS_DIR.relative_to(REPO_ROOT)}\n")

    domain_dirs = [d for d in DOMAINS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    all_violations = []

    for d in sorted(domain_dirs):
        dd = scan_domain(d)
        for fd in dd["files_data"]:
            violations = validate_file(fd)
            for v in violations:
                all_violations.append((dd["name"], v))

    if all_violations:
        print(f"Found {len(all_violations)} violation(s):\n")
        current_domain = None
        for domain, v in all_violations:
            if domain != current_domain:
                print(f"  {domain}:")
                current_domain = domain
            print(f"    ⚠️  {v}")
    else:
        print("✅ No phase gate violations found.")


def _write_project_status(all_domains: List[Dict]):
    """Regenerate PROJECT_STATUS.md (summary table only — preserves manual sections)."""
    # Read existing file to preserve manual sections
    existing = ""
    if PROJECT_STATUS_FILE.exists():
        existing = PROJECT_STATUS_FILE.read_text(encoding="utf-8")

    # Build the auto-generated domain table
    table_rows = []
    for d in sorted(all_domains, key=lambda x: x["name"]):
        phase = calculate_domain_phase(d)
        fc = d["file_count"]
        wc = d["total_words"]
        subs = len(d["subdomains"])
        flag = "🟢" if fc > 5 else "🟡" if fc > 0 else "🔴"
        table_rows.append(
            f"| {d['name']} | {phase} | {PHASES.get(phase,'?')} | {fc} | {wc:,} | {subs} | {flag} |"
        )

    table = "\n".join(table_rows)

    # Phase distribution
    phase_dist = defaultdict(int)
    for d in all_domains:
        phase_dist[calculate_domain_phase(d)] += 1
    dist_text = "\n".join(
        f"- **Phase {p} — {PHASES.get(p,'?')}:** {phase_dist[p]} domain(s)"
        for p in sorted(phase_dist)
    )

    auto_block = f"""<!-- AUTO-GENERATED: maturity_scan.py — do not edit below this line -->
**Last scan:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Domains:** {len(all_domains)} · **Files:** {sum(d['file_count'] for d in all_domains)} · **Words:** {sum(d['total_words'] for d in all_domains):,}

| Domain | Phase | Phase Name | Files | Words | Subdomains | Status |
|--------|-------|------------|-------|-------|------------|--------|
{table}

### Phase Distribution

{dist_text}
<!-- END AUTO-GENERATED -->"""

    # Replace the auto-generated block if it exists, otherwise append
    if "<!-- AUTO-GENERATED:" in existing:
        updated = re.sub(
            r"<!-- AUTO-GENERATED:.*?<!-- END AUTO-GENERATED -->",
            auto_block,
            existing,
            flags=re.DOTALL,
        )
    else:
        updated = existing.rstrip() + "\n\n" + auto_block + "\n"

    PROJECT_STATUS_FILE.write_text(updated, encoding="utf-8")
    print(f"\n  ✓ PROJECT_STATUS.md updated")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command in ("scan", "report"):
        cmd_scan()
    elif command == "gaps":
        cmd_gaps()
    elif command == "validate":
        cmd_validate()
    else:
        print(f"Unknown command: {command}")
        print("Available: scan, report, gaps, validate")
        sys.exit(1)
