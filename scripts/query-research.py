#!/usr/bin/env python3
"""
Query the local Chroma vector store built by embed-research.py, then expand
hits back into surrounding chunks from the canonical JSONL and join against
index.yaml for full citation info.

Embeddings only ever answer "where is this probably discussed" -- this script
is what actually retrieves the evidence, from the canonical chunk files, not
from anything cached in the vector store itself.

Usage:
    python3 scripts/query-research.py "vacant lot greening and crime rates"
    python3 scripts/query-research.py "..." --tag violent-crime --top-k 8

Requires:
    pip3 install sentence-transformers chromadb ruamel.yaml --break-system-packages
"""

from __future__ import annotations

import argparse
import sys

from research_lib import (
    DEFAULT_EMBEDDING_MODEL,
    INDEX_YAML,
    QUERY_INSTRUCTION,
    VECTOR_STORE_DIR,
    collection_name_for,
    format_context,
    get_model,
    load_index,
    load_merged_windows,
    merge_hit_windows,
)


def get_collection(model_name: str):
    """
    Fails closed: querying against a collection that doesn't exist (e.g. a
    typo in --model, or embedding was never run) prints a clear error rather
    than silently creating an empty collection and returning "No results.",
    which would look like a content gap instead of an operational mistake.
    """
    try:
        import chromadb
    except ImportError:
        print("Error: chromadb not installed. Run: pip3 install chromadb --break-system-packages")
        sys.exit(1)
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    collection_name = collection_name_for(model_name)
    try:
        return client.get_collection(name=collection_name)
    except Exception:
        print(
            f"Vector collection '{collection_name}' does not exist.\n"
            f"Run: python3 scripts/embed-research.py --model {model_name}"
        )
        sys.exit(1)


def eligible_keys_for_tag(index: dict, tag: str) -> list[str]:
    """Tag semantics live in index.yaml, not in the vector store's
    comma-joined metadata string -- filter the citation-key universe here,
    then let Chroma filter by citation_key, which is a real scalar field."""
    return [
        key
        for key, entry in index.get("sources", {}).items()
        if tag in (entry.get("tags") or [])
    ]


def main():
    parser = argparse.ArgumentParser(description="Query the research-library vector store")
    parser.add_argument("query")
    parser.add_argument("--model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--radius", type=int, default=1, help="chunks of context on each side of a hit")
    parser.add_argument("--tag", help="restrict results to sources carrying this tag (per index.yaml)")
    args = parser.parse_args()

    index = load_index(INDEX_YAML)

    where = None
    if args.tag:
        eligible = eligible_keys_for_tag(index, args.tag)
        if not eligible:
            print(f"No sources in index.yaml carry tag '{args.tag}'.")
            return
        where = {"citation_key": {"$in": eligible}}

    model = get_model(args.model)
    collection = get_collection(args.model)

    query_vector = model.encode([QUERY_INSTRUCTION + args.query], normalize_embeddings=True)[0].tolist()

    results = collection.query(query_embeddings=[query_vector], n_results=args.top_k, where=where)

    ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not ids:
        print("No results.")
        return

    hits = list(zip(ids, metadatas, distances))

    print(f"\n{len(hits)} vector hit(s):")
    for chunk_id, meta, dist in hits:
        print(f"  {meta['citation_key']}  chunk {meta['chunk_index']}  (distance {dist:.4f})")

    # Merge overlapping expansion windows so adjacent hits in the same
    # source (e.g. chunks 27 and 28 both scoring highly) don't produce
    # duplicated, overlapping passages once expanded.
    windows = merge_hit_windows(hits, radius=args.radius)
    merged_records = load_merged_windows(windows)

    print(f"\n{'=' * 70}")
    print("EXPANDED EVIDENCE")
    print("=" * 70)
    print(format_context(merged_records, index))


if __name__ == "__main__":
    main()
