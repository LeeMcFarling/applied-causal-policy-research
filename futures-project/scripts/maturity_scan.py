#!/usr/bin/env python3
"""
this project - Maturity Tracker Automation Script

This script scans the policy repository and updates maturity trackers for each domain.
It can be run by Claude Code to automate bookkeeping and gap analysis.

Usage:
    python maturity_scan.py [command] [options]

Commands:
    scan            Scan all domains and update maturity trackers
    init [domain]   Initialize a new maturity tracker for a domain
    report          Generate overall project status report
    gaps            Analyze and report gaps across all domains
    validate        Check for phase violations and dependency issues
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

# Configuration
REPO_ROOT = Path(".")  # Adjust to your repo root
DOMAINS_DIR = REPO_ROOT / "docs"  # Adjust to where your policy domains are
TRACKER_FILENAME = "_MATURITY_TRACKER.md"
PROJECT_STATUS_FILE = REPO_ROOT / "PROJECT_STATUS.md"

# Phase definitions
PHASES = {
    0: "Problem Framing",
    1: "Strategic Constraints",
    2: "Structured Exploration",
    3: "Outcomes & Decision Rules",
    4: "Sequencing & Execution Design",
    5: "External Validation",
    6: "Messaging & Rebuttal"
}


def extract_frontmatter(file_path: Path) -> Optional[Dict]:
    """Extract YAML frontmatter from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1])
    except Exception as e:
        print(f"Warning: Could not parse frontmatter in {file_path}: {e}")
    
    return None


def count_words(file_path: Path) -> int:
    """Count words in a markdown file (excluding frontmatter)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        
        # Remove markdown syntax and count
        content = re.sub(r'[#*`\[\]()_~]', '', content)
        words = len(content.split())
        return words
    except Exception as e:
        print(f"Warning: Could not count words in {file_path}: {e}")
        return 0


def scan_domain(domain_path: Path) -> Dict:
    """Scan a domain directory and gather metrics."""
    domain_name = domain_path.name
    
    # Find all markdown files (excluding tracker)
    md_files = [
        f for f in domain_path.glob("*.md") 
        if f.name != TRACKER_FILENAME and not f.name.startswith('_')
    ]
    
    # Organize by subdomain (from frontmatter or filename)
    subdomains = defaultdict(lambda: {
        'files': [],
        'total_words': 0,
        'phases': set(),
        'dependencies': []
    })
    
    for md_file in md_files:
        frontmatter = extract_frontmatter(md_file)
        word_count = count_words(md_file)
        
        # Determine subdomain
        subdomain = "Uncategorized"
        phase = 0
        
        if frontmatter:
            subdomain = frontmatter.get('subdomain', subdomain)
            phase = frontmatter.get('phase', 0)
            deps = frontmatter.get('dependencies', [])
            if deps:
                subdomains[subdomain]['dependencies'].extend(deps)
        
        subdomains[subdomain]['files'].append(md_file.name)
        subdomains[subdomain]['total_words'] += word_count
        subdomains[subdomain]['phases'].add(phase)
    
    return {
        'name': domain_name,
        'path': domain_path,
        'file_count': len(md_files),
        'subdomains': dict(subdomains),
        'total_words': sum(s['total_words'] for s in subdomains.values())
    }


def calculate_domain_phase(domain_data: Dict) -> int:
    """Calculate overall domain phase based on subdomains."""
    if not domain_data['subdomains']:
        return 0
    
    # Take minimum phase across all subdomains
    all_phases = []
    for subdomain_data in domain_data['subdomains'].values():
        if subdomain_data['phases']:
            all_phases.append(min(subdomain_data['phases']))
        else:
            all_phases.append(0)
    
    return min(all_phases) if all_phases else 0


def update_maturity_tracker(domain_data: Dict):
    """Update or create maturity tracker for a domain."""
    tracker_path = domain_data['path'] / TRACKER_FILENAME
    domain_name = domain_data['name']
    overall_phase = calculate_domain_phase(domain_data)
    
    # Read existing tracker if it exists
    existing_content = ""
    if tracker_path.exists():
        with open(tracker_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # Build subdomain status table
    table_rows = []
    for subdomain_name, subdomain_data in sorted(domain_data['subdomains'].items()):
        file_count = len(subdomain_data['files'])
        word_count = subdomain_data['total_words']
        phase = min(subdomain_data['phases']) if subdomain_data['phases'] else 0
        
        # Determine gaps
        gaps = "In progress" if file_count > 0 else "Not started"
        if word_count < 500 and file_count > 0:
            gaps = "Minimal content"
        
        # Extract dependencies
        deps = subdomain_data['dependencies']
        dep_summary = "None"
        if deps:
            dep_summary = ", ".join([f"{d.get('target', 'Unknown')}" for d in deps[:2]])
            if len(deps) > 2:
                dep_summary += f" +{len(deps)-2} more"
        
        next_action = "Create initial file" if file_count == 0 else f"Advance to Phase {phase + 1}"
        
        table_rows.append(
            f"| {subdomain_name} | {phase} | {file_count} | {word_count:,} | {gaps} | {dep_summary} | {next_action} | TBD |"
        )
    
    table = "\n".join(table_rows) if table_rows else "| No subdomains yet | 0 | 0 | 0 | Not started | None | Initialize domain | TBD |"
    
    # Create or update tracker
    content = f"""# Domain Maturity Tracker: {domain_name}

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}  
**Overall Domain Phase:** {overall_phase}  
**Total Files:** {domain_data['file_count']}  
**Total Words:** {domain_data['total_words']:,}

---

## Phase Model Reference

- **Phase 0** – Problem Framing
- **Phase 1** – Strategic Constraints
- **Phase 2** – Structured Exploration
- **Phase 3** – Outcomes & Decision Rules
- **Phase 4** – Sequencing & Execution Design
- **Phase 5** – External Validation
- **Phase 6** – Messaging & Rebuttal

---

## Subdomain Status Matrix

| Subdomain | Phase | File Count | Word Count | Key Gaps | Dependencies | Next Action | Target Date |
|-----------|-------|------------|------------|----------|--------------|-------------|-------------|
{table}

---

## Gap Analysis

### Auto-detected Gaps:
"""
    
    # Add gap detection
    for subdomain_name, subdomain_data in domain_data['subdomains'].items():
        if len(subdomain_data['files']) == 0:
            content += f"\n- **{subdomain_name}**: No files created yet (Phase 0)"
        elif subdomain_data['total_words'] < 500:
            content += f"\n- **{subdomain_name}**: Minimal content ({subdomain_data['total_words']} words)"
    
    if not any(len(s['files']) == 0 or s['total_words'] < 500 
               for s in domain_data['subdomains'].values()):
        content += "\n- No critical gaps detected at file level"
    
    content += "\n\n---\n\n## Notes\n\n_This tracker is auto-generated. Add manual notes below:_\n\n"
    
    # Preserve manual notes if they exist
    if "## Notes" in existing_content:
        notes_section = existing_content.split("## Notes", 1)[1]
        # Take everything after the auto-generated marker
        if "_This tracker is auto-generated" in notes_section:
            manual_notes = notes_section.split("_This tracker is auto-generated. Add manual notes below:_", 1)[1]
            content += manual_notes
    
    # Write tracker
    with open(tracker_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated tracker for {domain_name}")


def generate_project_status():
    """Generate overall project status report."""
    print("\n🔍 Scanning all domains...\n")
    
    domain_dirs = [d for d in DOMAINS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]
    all_domains = []
    
    for domain_dir in sorted(domain_dirs):
        domain_data = scan_domain(domain_dir)
        all_domains.append(domain_data)
        update_maturity_tracker(domain_data)
    
    # Create summary report
    report = f"""# this project - Overall Status Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

**Total Domains:** {len(all_domains)}  
**Total Policy Files:** {sum(d['file_count'] for d in all_domains)}  
**Total Words Written:** {sum(d['total_words'] for d in all_domains):,}

---

## Domain Status Overview

| Domain | Phase | Files | Words | Subdomains | Status |
|--------|-------|-------|-------|------------|--------|
"""
    
    for domain in sorted(all_domains, key=lambda d: d['name']):
        phase = calculate_domain_phase(domain)
        status = "🟢 Active" if domain['file_count'] > 5 else "🟡 In Progress" if domain['file_count'] > 0 else "🔴 Empty"
        
        report += f"| {domain['name']} | {phase} | {domain['file_count']} | {domain['total_words']:,} | {len(domain['subdomains'])} | {status} |\n"
    
    report += "\n---\n\n## Phase Distribution\n\n"
    
    # Count domains by phase
    phase_counts = defaultdict(int)
    for domain in all_domains:
        phase = calculate_domain_phase(domain)
        phase_counts[phase] += 1
    
    for phase in sorted(phase_counts.keys()):
        report += f"- **Phase {phase} ({PHASES[phase]}):** {phase_counts[phase]} domains\n"
    
    report += "\n---\n\n## Quick Links to Domain Trackers\n\n"
    
    for domain in sorted(all_domains, key=lambda d: d['name']):
        tracker_rel_path = f"docs/{domain['name']}/{TRACKER_FILENAME}"
        report += f"- [{domain['name']}]({tracker_rel_path})\n"
    
    # Write report
    with open(PROJECT_STATUS_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ Generated project status report: {PROJECT_STATUS_FILE}")
    print(f"\n📊 Summary: {len(all_domains)} domains, {sum(d['file_count'] for d in all_domains)} files, {sum(d['total_words'] for d in all_domains):,} words")


def analyze_gaps():
    """Analyze gaps across all domains."""
    print("\n🔍 Analyzing gaps across all domains...\n")
    
    domain_dirs = [d for d in DOMAINS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    tier1_gaps = []  # Missing domains
    tier2_gaps = []  # Skeletal domains
    tier3_gaps = []  # Domains with gaps
    
    for domain_dir in sorted(domain_dirs):
        domain_data = scan_domain(domain_dir)
        
        if domain_data['file_count'] == 0:
            tier1_gaps.append(domain_data['name'])
        elif domain_data['file_count'] <= 2 or domain_data['total_words'] < 1000:
            tier2_gaps.append((domain_data['name'], domain_data['file_count'], domain_data['total_words']))
        elif domain_data['total_words'] < 5000:
            tier3_gaps.append((domain_data['name'], domain_data['file_count'], domain_data['total_words']))
    
    print("## Tier 1: Missing Domains (No Coverage)")
    for domain in tier1_gaps:
        print(f"  - {domain}")
    
    print("\n## Tier 2: Skeletal Domains (Minimal Content)")
    for domain, files, words in tier2_gaps:
        print(f"  - {domain}: {files} files, {words:,} words")
    
    print("\n## Tier 3: Domains with Gaps (Could Expand)")
    for domain, files, words in tier3_gaps:
        print(f"  - {domain}: {files} files, {words:,} words")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python maturity_scan.py [scan|report|gaps|validate]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "scan":
        generate_project_status()
    elif command == "report":
        generate_project_status()
    elif command == "gaps":
        analyze_gaps()
    elif command == "validate":
        print("Phase validation coming soon...")
    else:
        print(f"Unknown command: {command}")
        print("Available commands: scan, report, gaps, validate")
