#!/usr/bin/env python3
"""
Ingest a research document (PDF or existing text) into the platform research library.

Usage:
    python3 scripts/ingest-research.py path/to/report.pdf
    python3 scripts/ingest-research.py path/to/report.pdf --key rand-superannuation-2019

Workflow:
  1. Extracts text from PDF using pdfplumber
  2. Prompts for citation metadata (institution, title, authors, year, URL)
  3. Generates Chicago citation
  4. Writes formatted .md to research-library/sources/
  5. Adds entry to research-library/index.md

After ingestion, run a Phase 3 review pass:
    - Provide Claude with the source .md + relevant platform brief(s)
    - Ask for the four-section review (aligned, gaps, divergences, open questions)
    - Save output to research-library/reviews/<topic>-research-review.md
    - Add inline citations to the brief using footnote syntax
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SOURCES_DIR = REPO_ROOT / "research-library" / "sources"
INDEX_FILE = REPO_ROOT / "research-library" / "index.md"


def extract_pdf_text(pdf_path: Path) -> str:
    try:
        import pdfplumber
    except ImportError:
        print("Error: pdfplumber not installed. Run: pip3 install pdfplumber --break-system-packages")
        sys.exit(1)

    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        print(f"  Extracting {total} pages...", end="", flush=True)
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                pages.append(f"<!-- Page {i+1} -->\n{text.strip()}")
            if (i + 1) % 10 == 0:
                print(f" {i+1}...", end="", flush=True)
    print(" done.")
    return "\n\n".join(pages)


def prompt(label: str, default: str = "") -> str:
    if default:
        val = input(f"  {label} [{default}]: ").strip()
        return val if val else default
    val = input(f"  {label}: ").strip()
    return val


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def build_chicago(authors: str, title: str, institution: str,
                  city: str, year: str, url: str) -> str:
    # Format: Last, First[, and First Last]. *Title*. City: Institution, Year. URL.
    chicago = f"{authors}. *{title}*. {city}: {institution}, {year}."
    if url:
        chicago += f" {url}."
    return chicago


def build_source_doc(key: str, institution: str, chicago: str, url: str,
                     accessed: str, topics: list, content: str) -> str:
    topics_yaml = "\n".join(f"  - {t}" for t in topics) if topics else "  - general"

    return f"""---
citation-key: {key}
institution: {institution}
chicago: "{chicago}"
url: {url or 'TBD'}
accessed: {accessed}
topics:
{topics_yaml}
briefs: []
phase-3-review: TBD
---

## Citation

{chicago}

---

## Content

{content}
"""


def update_index(key: str, institution: str, chicago: str, topics: list,
                 out_path: Path):
    entry = f"- [{key}]({out_path.relative_to(REPO_ROOT)}) — {institution} — {', '.join(topics) if topics else 'general'}\n"

    if not INDEX_FILE.exists():
        INDEX_FILE.write_text(
            "# Research Library Index\n\n"
            "Sources are listed below. See `reviews/` for Phase 3 review outputs.\n\n"
            "## Sources\n\n"
        )

    content = INDEX_FILE.read_text()
    if "## Sources" not in content:
        content += "\n## Sources\n\n"

    if key not in content:
        idx = content.find("## Sources") + len("## Sources\n\n")
        content = content[:idx] + entry + content[idx:]
        INDEX_FILE.write_text(content)
        print(f"  Added to index.")


def main():
    parser = argparse.ArgumentParser(
        description="Ingest a research document into the platform research library"
    )
    parser.add_argument("input", help="Path to PDF or text file")
    parser.add_argument("--key", help="Citation key slug (auto-generated if omitted)")
    parser.add_argument("--no-extract", action="store_true",
                        help="Skip PDF extraction (use for already-converted text)")
    args = parser.parse_args()

    src = Path(args.input).resolve()
    if not src.exists():
        print(f"File not found: {src}")
        sys.exit(1)

    print(f"\nIngesting: {src.name}")
    print("─" * 50)

    # Metadata prompts
    print("\nCitation metadata (press Enter to skip optional fields):\n")
    authors   = prompt("Authors (Last, First[, and First Last])")
    title     = prompt("Title")
    institution = prompt("Institution (e.g. RAND Corporation)")
    city      = prompt("City of publication", "Santa Monica" if "rand" in institution.lower() else "Washington, D.C.")
    year      = prompt("Year")
    url       = prompt("URL (optional)")
    topics_in = prompt("Topics (comma-separated, e.g. superannuation,retirement)")
    topics    = [t.strip() for t in topics_in.split(",") if t.strip()]

    accessed  = date.today().isoformat()

    # Generate key
    if args.key:
        key = args.key
    else:
        inst_short = slugify(institution.split()[0]) if institution else "source"
        title_short = "-".join(slugify(title).split("-")[:3]) if title else "document"
        key = f"{inst_short}-{title_short}-{year}" if year else f"{inst_short}-{title_short}"

    chicago = build_chicago(authors, title, institution, city, year, url)

    print(f"\n  Citation key: {key}")
    print(f"  Chicago:      {chicago[:80]}...")

    # Extract content
    if src.suffix.lower() == ".pdf" and not args.no_extract:
        content = extract_pdf_text(src)
    else:
        content = src.read_text(encoding="utf-8")

    # Write source document
    out_path = SOURCES_DIR / f"{key}.md"
    if out_path.exists():
        overwrite = input(f"\n  {out_path.name} already exists. Overwrite? [y/N] ").strip().lower()
        if overwrite != "y":
            print("  Skipped.")
            sys.exit(0)

    doc = build_source_doc(key, institution, chicago, url, accessed, topics, content)
    out_path.write_text(doc, encoding="utf-8")
    print(f"\n  Written: research-library/sources/{out_path.name}")

    # Update index
    update_index(key, institution, chicago, topics, out_path)

    print(f"""
Next steps:
  1. Review the extracted text in:
       research-library/sources/{out_path.name}
  2. Add relevant brief slugs to the 'briefs:' field in its frontmatter
  3. Run a Phase 3 review pass:
       - Provide Claude with this source + the relevant platform brief(s)
       - Ask for the four-section review (aligned findings, gaps, divergences, open questions)
       - Save the review to:
           research-library/reviews/<topic>-research-review.md
  4. Add inline citations to the brief using footnote syntax:
       [^1]: {chicago[:60]}...
""")


if __name__ == "__main__":
    main()
