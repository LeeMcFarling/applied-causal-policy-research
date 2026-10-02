#!/usr/bin/env python3
"""
Ingest a research document (PDF) into the platform research library.

Usage:
    python3 scripts/ingest-research.py path/to/report.pdf
    python3 scripts/ingest-research.py path/to/report.pdf --key rand-superannuation-2019
    python3 scripts/ingest-research.py --reingest rand-superannuation-2019

Workflow:
  1. Extracts text per page from the PDF using pdfplumber
  2. Prompts for citation metadata (authors, title, institution, city, year, URL, tags)
  3. Chunks the extraction by page (splitting oversized pages, never merging
     across a page boundary) so every RAG record carries an exact page
     reference -- this is what lets a review cite a page and have it be
     checkable, instead of inferred from a table of contents
  4. Writes:
       research-library/originals/<key>.pdf   (byte-for-byte copy of the input)
       research-library/rag/<key>.jsonl       (canonical chunk records)
       research-library/sources/<key>.md      (human-readable extraction)
  5. Adds/updates the source's entry in research-library/index.yaml

--reingest <key> re-extracts an already-ingested source from its stored
original (research-library/originals/<key>.pdf) using the current extraction
settings, reusing the citation metadata already in index.yaml instead of
prompting for it. Use it after changing extraction or chunking; then re-embed
with `embed-research.py --key <key>`.

Does NOT touch research-library/index.md -- that file is hand-curated prose
for this sample repository, not a generated view. Run
research_lib.regenerate_index_md() yourself if this project's index.md is
meant to be a generated listing instead.

After ingestion:
    python3 scripts/embed-research.py --key <key>
    python3 scripts/query-research.py "some question" --tag <a-tag>
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pdfplumber

from research_lib import (
    CURRENT_CHUNKER_VERSION,
    DEFAULT_MAX_CHARS,
    DEFAULT_OVERLAP_CHARS,
    EXTRACT_X_TOLERANCE,
    FUSED_TOKEN_MIN_LETTERS,
    FUSED_TOKEN_WARN_RATIO,
    INDEX_YAML,
    ORIGINALS_DIR,
    RAG_DIR,
    SOURCES_DIR,
    load_index,
    save_index,
    fused_token_ratio,
    write_rag_records,
)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def extract_pages(pdf_path: Path) -> list[tuple[int, str]]:
    """Returns [(page_number, text), ...], 1-indexed, skipping blank pages."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        print(f"  Extracting {total} pages...", end="", flush=True)
        for i, page in enumerate(pdf.pages):
            text = page.extract_text(x_tolerance=EXTRACT_X_TOLERANCE)
            if text and text.strip():
                pages.append((i + 1, text.strip()))
            if (i + 1) % 10 == 0:
                print(f" {i + 1}...", end="", flush=True)
    print(" done.")
    return pages


def check_extraction(pages: list[tuple[int, str]]) -> list[int]:
    """
    Flags pages whose text looks like fused words (long runs of letters with
    no spaces), which usually means the PDF's spacing defeated the extractor.
    Returns the flagged page numbers so they can be recorded in index.yaml.
    """
    flagged = [n for n, text in pages if fused_token_ratio(text) > FUSED_TOKEN_WARN_RATIO]
    if flagged:
        print(f"  WARNING: {len(flagged)} page(s) have more than {FUSED_TOKEN_WARN_RATIO:.0%} of tokens "
              f"with fused runs of {FUSED_TOKEN_MIN_LETTERS}+ letters: {flagged}")
        print("  Check these pages in the source record before embedding.")
    else:
        print("  Extraction check: no pages with fused-word runs above threshold.")
    return flagged


def chunk_by_page(
    key: str,
    pages: list[tuple[int, str]],
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap_chars: int = DEFAULT_OVERLAP_CHARS,
) -> list[dict]:
    """
    One chunk per page by default. A page longer than max_chars is split into
    multiple overlapping chunks, but a chunk never spans two pages -- every
    record's page_start == page_end, so a citation to a chunk is a citation
    to one specific, checkable page, not a range inferred from context.
    """
    records: list[dict] = []
    for page_num, text in pages:
        if len(text) <= max_chars:
            records.append({"page_start": page_num, "page_end": page_num, "text": text})
            continue
        start = 0
        while start < len(text):
            end = min(start + max_chars, len(text))
            piece = text[start:end].strip()
            if piece:
                records.append({"page_start": page_num, "page_end": page_num, "text": piece})
            if end == len(text):
                break
            start = end - overlap_chars

    for i, record in enumerate(records):
        record["chunk_index"] = i
        record["citation_key"] = key
        record["id"] = f"{key}__{i:04d}"
    return records


def build_source_md(key: str, chicago: str, url: str, accessed: str, pages: list[tuple[int, str]]) -> str:
    body = "\n\n".join(f"<!-- Page {n} -->\n{text}" for n, text in pages)
    return f"""---
citation-key: {key}
chicago: "{chicago}"
url: {url or 'TBD'}
accessed: {accessed}
---

## Citation

{chicago}

---

## Content

{body}
"""


def prompt(label: str, default: str = "") -> str:
    if default:
        val = input(f"  {label} [{default}]: ").strip()
        return val if val else default
    return input(f"  {label}: ").strip()


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def parse_authors(authors: str) -> list[str]:
    """
    Splits a Chicago-style author string into one entry per author:
    "Aneja, Abhay, and Guo Xu" -> ["Aneja, Abhay", "Guo Xu"]. The first author
    is inverted ("Last, First"), so its comma must not be treated as a separator;
    later authors are separated by commas and/or a final "and".
    """
    authors = authors.strip()
    if not authors:
        return []
    groups = re.split(r",?\s+and\s+", authors)
    head = [part.strip() for part in groups[0].split(",") if part.strip()]
    names = [f"{head[0]}, {head[1]}"] + head[2:] if len(head) >= 2 else head
    names += [g.strip() for g in groups[1:] if g.strip()]
    return names


def build_chicago(authors: str, title: str, institution: str, city: str, year: str, url: str) -> str:
    chicago = f"{authors}. *{title}*. {city}: {institution}, {year}."
    if url:
        chicago += f" {url}."
    return chicago


def upsert_index_entry(
    key: str,
    *,
    title: str,
    authors: str,
    institution: str,
    city: str,
    year: str,
    chicago: str,
    url: str,
    accessed: str,
    tags: list[str],
    pdf_path: Path,
    sha256: str,
    pages: int,
    chunks: int,
    flagged_pages: list[int],
) -> None:
    index = load_index(INDEX_YAML)
    sources = index["sources"]
    existing = sources.get(key, {})
    sources[key] = {
        "title": title,
        "authors": parse_authors(authors),
        "institution": institution,
        "publication_place": city,
        "publication_date": year,
        "chicago": chicago,
        "url": url or None,
        "accessed": accessed,
        "tags": tags,
        "briefs": existing.get("briefs", []),
        "reviews": existing.get("reviews", []),
        "claims": existing.get("claims", []),
        "source": {
            "type": "pdf",
            "file": f"research-library/originals/{key}.pdf",
            "extracted": f"research-library/sources/{key}.md",
            "rag": f"research-library/rag/{key}.jsonl",
            "sha256": sha256,
        },
        "ingestion": {
            "extractor": "pdfplumber",
            "extractor_version": __import__("pdfplumber").__version__,
            "extracted_at": accessed,
            "pages": pages,
            "chunks": chunks,
            "chunker_version": CURRENT_CHUNKER_VERSION,
            "x_tolerance": EXTRACT_X_TOLERANCE,
            "flagged_pages": flagged_pages,
        },
        "status": {
            "phase_3_review": existing.get("status", {}).get("phase_3_review", "pending"),
            "extraction": "complete",
            "embedding": "pending",
        },
    }
    save_index(index, INDEX_YAML)


def reingest(key: str) -> None:
    """Re-extract an existing source from its stored original, keeping its metadata."""
    index = load_index(INDEX_YAML)
    entry = index["sources"].get(key)
    if entry is None:
        print(f"No source with key {key!r} in {INDEX_YAML.name}.")
        sys.exit(1)
    pdf = ORIGINALS_DIR / f"{key}.pdf"
    if not pdf.exists():
        print(f"Stored original not found: {pdf}")
        sys.exit(1)

    print(f"\nRe-ingesting: {key}")
    print("─" * 50)
    pages = extract_pages(pdf)
    if not pages:
        print("  No extractable text found in this PDF.")
        sys.exit(1)
    flagged = check_extraction(pages)

    records = chunk_by_page(key, pages)
    print(f"  {len(pages)} pages -> {len(records)} chunks (page-bounded, max {DEFAULT_MAX_CHARS} chars/chunk)")
    write_rag_records(key, records, RAG_DIR)
    print(f"  Written: research-library/rag/{key}.jsonl")

    md_path = SOURCES_DIR / f"{key}.md"
    md_path.write_text(
        build_source_md(key, entry["chicago"], entry.get("url") or "", str(entry.get("accessed", "")), pages),
        encoding="utf-8",
    )
    print(f"  Written: research-library/sources/{md_path.name}")

    # Update only what extraction determines; citation metadata, briefs,
    # reviews, and claims are left exactly as they were.
    entry["source"]["sha256"] = sha256_of(pdf)
    ingestion = entry["ingestion"]
    ingestion["extractor_version"] = pdfplumber.__version__
    ingestion["extracted_at"] = date.today().isoformat()
    ingestion["x_tolerance"] = EXTRACT_X_TOLERANCE
    ingestion["pages"] = len(pages)
    ingestion["chunks"] = len(records)
    ingestion["chunker_version"] = CURRENT_CHUNKER_VERSION
    ingestion["flagged_pages"] = flagged
    entry["status"]["extraction"] = "complete"
    entry["status"]["embedding"] = "pending"
    save_index(index, INDEX_YAML)
    print(f"  Updated: research-library/index.yaml ({key}); embedding marked pending")
    print(f"\nNext: python3 scripts/embed-research.py --key {key}\n")


def main():
    parser = argparse.ArgumentParser(description="Ingest a PDF into the platform research library")
    parser.add_argument("input", nargs="?", help="Path to PDF")
    parser.add_argument("--key", help="Citation key slug (auto-generated if omitted)")
    parser.add_argument("--reingest", metavar="KEY",
                        help="Re-extract an existing source from its stored original, keeping its metadata")
    args = parser.parse_args()

    if args.reingest:
        reingest(args.reingest)
        return
    if not args.input:
        parser.error("a PDF path is required unless --reingest is given")

    src = Path(args.input).resolve()
    if not src.exists():
        print(f"File not found: {src}")
        sys.exit(1)
    if src.suffix.lower() != ".pdf":
        print("Only PDF input is supported by this script.")
        sys.exit(1)

    print(f"\nIngesting: {src.name}")
    print("─" * 50)

    print("\nCitation metadata (press Enter to skip optional fields):\n")
    authors = prompt("Authors (Last, First[, and First Last])")
    title = prompt("Title")
    institution = prompt("Institution (e.g. RAND Corporation)")
    city = prompt("City of publication", "Washington, D.C.")
    year = prompt("Year")
    url = prompt("URL (optional)")
    topics_in = prompt("Topics (comma-separated, e.g. superannuation,retirement)")
    tags = [t.strip() for t in topics_in.split(",") if t.strip()]

    accessed = date.today().isoformat()

    if args.key:
        key = args.key
    else:
        inst_short = slugify(institution.split()[0]) if institution else "source"
        title_short = "-".join(slugify(title).split("-")[:3]) if title else "document"
        key = f"{inst_short}-{title_short}-{year}" if year else f"{inst_short}-{title_short}"

    chicago = build_chicago(authors, title, institution, city, year, url)

    print(f"\n  Citation key: {key}")
    print(f"  Chicago:      {chicago[:80]}...")

    sha256 = sha256_of(src)
    pages = extract_pages(src)
    if not pages:
        print("  No extractable text found in this PDF (scanned image with no OCR layer?).")
        sys.exit(1)
    flagged = check_extraction(pages)

    records = chunk_by_page(key, pages)
    print(f"  {len(pages)} pages -> {len(records)} chunks (page-bounded, max {DEFAULT_MAX_CHARS} chars/chunk)")

    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
    dest_pdf = ORIGINALS_DIR / f"{key}.pdf"
    shutil.copy2(src, dest_pdf)

    rag_path = write_rag_records(key, records, RAG_DIR)
    print(f"  Written: {rag_path.relative_to(rag_path.parent.parent.parent)}")

    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    md_path = SOURCES_DIR / f"{key}.md"
    md_path.write_text(build_source_md(key, chicago, url, accessed, pages), encoding="utf-8")
    print(f"  Written: research-library/sources/{md_path.name}")

    upsert_index_entry(
        key,
        title=title,
        authors=authors,
        institution=institution,
        city=city,
        year=year,
        chicago=chicago,
        url=url,
        accessed=accessed,
        tags=tags,
        pdf_path=dest_pdf,
        sha256=sha256,
        pages=len(pages),
        chunks=len(records),
        flagged_pages=flagged,
    )
    print(f"  Updated: research-library/index.yaml ({key})")

    print(f"""
Next steps:
  1. Review the extraction in:
       research-library/sources/{md_path.name}
  2. Embed it into the vector store:
       python3 scripts/embed-research.py --key {key}
  3. Spot-check retrieval:
       python3 scripts/query-research.py "some question about {key}" --tag {tags[0] if tags else '<tag>'}
""")


if __name__ == "__main__":
    main()
