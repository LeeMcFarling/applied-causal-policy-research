#!/usr/bin/env python3
"""
Measure retrieval quality against a hand-labeled question set.

Each question in the set lists the source pages that actually answer it
(identified from the source text, not from retrieval output). This script runs
every question through the same query path as query-research.py and reports:

  hit@k   share of questions with at least one relevant page in the top k pages
  MRR     mean reciprocal rank of the first relevant page (0 if not in the top 10)

Results are ranked by distinct page: when several chunks from one page score
highly, the page counts once, at its best rank. This keeps the metric comparable
across chunking schemes that produce one chunk per page or several.

Usage:
    python3 scripts/eval-retrieval.py
    python3 scripts/eval-retrieval.py --questions research-library/eval/17a-retrieval-questions.yaml
    python3 scripts/eval-retrieval.py --vector-store path/to/other/store --label "before fix"
    python3 scripts/eval-retrieval.py --out research-library/eval/results.md

Requires:
    pip3 install sentence-transformers chromadb ruamel.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from research_lib import (
    DEFAULT_EMBEDDING_MODEL,
    QUERY_INSTRUCTION,
    REPO_ROOT,
    VECTOR_STORE_DIR,
    collection_name_for,
    get_model,
)

DEFAULT_QUESTIONS = REPO_ROOT / "research-library" / "eval" / "17a-retrieval-questions.yaml"
MAX_RANK = 10
CHUNKS_TO_SCAN = 60  # enough raw chunk hits to fill MAX_RANK distinct pages


def load_questions(path: Path) -> dict:
    from ruamel.yaml import YAML
    with path.open(encoding="utf-8") as f:
        return YAML(typ="safe").load(f)


def distinct_pages(pages: list[int]) -> list[int]:
    """Collapse repeated pages to their first (best-ranked) occurrence."""
    seen, out = set(), []
    for page in pages:
        if page not in seen:
            seen.add(page)
            out.append(page)
    return out


def first_relevant_rank(pages: list[int], relevant: set[int]) -> int | None:
    """1-based rank of the first retrieved page that answers the question."""
    for rank, page in enumerate(pages, start=1):
        if page in relevant:
            return rank
    return None


def evaluate(questions: dict, store: Path, model_name: str) -> list[dict]:
    import chromadb
    collection = chromadb.PersistentClient(path=str(store)).get_collection(collection_name_for(model_name))
    model = get_model(model_name)
    key = questions["citation_key"]
    rows = []
    for item in questions["questions"]:
        vector = model.encode([QUERY_INSTRUCTION + item["question"]], normalize_embeddings=True)[0].tolist()
        n = min(CHUNKS_TO_SCAN, collection.count())
        result = collection.query(query_embeddings=[vector], n_results=n, where={"citation_key": key})
        pages = distinct_pages([m["page_start"] for m in result["metadatas"][0]])[:MAX_RANK]
        rows.append({
            "question": item["question"],
            "relevant": sorted(item["relevant_pages"]),
            "retrieved": pages,
            "rank": first_relevant_rank(pages, set(item["relevant_pages"])),
        })
    return rows


def summarize(rows: list[dict], ks=(1, 3, 5)) -> dict:
    n = len(rows)
    summary = {f"hit@{k}": sum(1 for r in rows if r["rank"] and r["rank"] <= k) / n for k in ks}
    summary["MRR"] = sum(1 / r["rank"] for r in rows if r["rank"]) / n
    return summary


def to_markdown(rows: list[dict], summary: dict, label: str) -> str:
    lines = [f"### {label}", "", "| Metric | Value |", "|---|---|"]
    lines += [f"| {k} | {v:.2f} |" for k, v in summary.items()]
    lines += ["", "| Question | Relevant pages | Top 3 retrieved | Rank of first relevant |", "|---|---|---|---|"]
    for r in rows:
        rank = r["rank"] if r["rank"] else f">{MAX_RANK}"
        lines.append(f"| {r['question']} | {r['relevant']} | {r['retrieved'][:3]} | {rank} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Evaluate retrieval against a labeled question set")
    parser.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS)
    parser.add_argument("--vector-store", type=Path, default=VECTOR_STORE_DIR)
    parser.add_argument("--model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--label", default="Current vector store")
    parser.add_argument("--out", type=Path, help="append the results table to this markdown file")
    args = parser.parse_args()

    questions = load_questions(args.questions)
    rows = evaluate(questions, args.vector_store, args.model)
    summary = summarize(rows)
    md = to_markdown(rows, summary, args.label)
    print(md)
    if args.out:
        with args.out.open("a", encoding="utf-8") as f:
            f.write(md + "\n")


if __name__ == "__main__":
    main()
