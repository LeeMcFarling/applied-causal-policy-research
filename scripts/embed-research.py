#!/usr/bin/env python3
"""
Embed pending sources into a local Chroma vector store using a local
sentence-transformers model (default: BAAI/bge-large-en-v1.5).

Decoupled from ingestion (scripts/ingest-research.py). Walks index.yaml for
sources that are stale for the target model/version -- not embedded yet, or
embedded under a different model or embedding_version than the one this run
is using -- embeds every chunk in their RAG JSONL, upserts into a local
persistent Chroma collection, and marks each source complete via
mark_embedding_complete() -- transactionally, so a partial run leaves
status.embedding untouched at 'pending' rather than lying.

Usage:
    python3 scripts/embed-research.py                # embed everything stale
    python3 scripts/embed-research.py --key some-key  # (re)embed one source
    python3 scripts/embed-research.py --force         # re-embed everything

Requires:
    pip3 install sentence-transformers chromadb ruamel.yaml --break-system-packages
"""

from __future__ import annotations

import argparse
import sys

from research_lib import (
    CURRENT_EMBEDDING_VERSION,
    DEFAULT_EMBEDDING_MODEL,
    INDEX_YAML,
    VECTOR_STORE_DIR,
    collection_name_for,
    get_model,
    load_index,
    load_rag_records,
    mark_embedding_complete,
    needs_embedding,
)


def get_collection(model_name: str):
    try:
        import chromadb
    except ImportError:
        print("Error: chromadb not installed. Run: pip3 install chromadb --break-system-packages")
        sys.exit(1)
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    # get_or_create is correct here (unlike query-research.py, which fails
    # closed): embedding is the step that's supposed to create the collection.
    return client.get_or_create_collection(
        name=collection_name_for(model_name), metadata={"hnsw:space": "cosine"}
    )


def embed_source(key: str, entry: dict, model, collection, embedding_model_name: str, batch_size: int) -> bool:
    records = load_rag_records(key)
    if not records:
        print(f"  [{key}] no RAG records found (run ingest-research.py first), skipping")
        return False

    texts = [r["text"] for r in records]
    ids = [r["id"] for r in records]
    tags = entry.get("tags", []) or []
    # Chroma metadata values must be scalar (str/int/float/bool) -- tags are
    # joined here. Tag *filtering* at query time reads from index.yaml
    # directly rather than parsing this back out (see query-research.py).
    metadatas = [
        {
            "citation_key": r["citation_key"],
            "chunk_index": r["chunk_index"],
            "page_start": r["page_start"],
            "page_end": r["page_end"],
            "tags": ",".join(tags),
        }
        for r in records
    ]

    # bge documents/passages get no instruction prefix -- only queries do
    # (see QUERY_INSTRUCTION in research_lib.py / query-research.py).
    vectors = model.encode(texts, batch_size=batch_size, normalize_embeddings=True, show_progress_bar=False)

    collection.upsert(ids=ids, embeddings=vectors.tolist(), metadatas=metadatas)

    mark_embedding_complete(
        citation_key=key,
        embedding_model=embedding_model_name,
        embedding_version=CURRENT_EMBEDDING_VERSION,
        embedded_chunk_count=len(records),
        index_path=INDEX_YAML,
    )
    return True


def main():
    parser = argparse.ArgumentParser(description="Embed pending research-library sources into a local Chroma store")
    parser.add_argument("--model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--force", action="store_true", help="re-embed every source, not just stale ones")
    parser.add_argument("--key", help="embed only this citation key")
    args = parser.parse_args()

    index = load_index(INDEX_YAML)
    sources = index.get("sources", {})

    if args.key:
        if args.key not in sources:
            print(f"'{args.key}' not found in index.yaml")
            sys.exit(1)
        candidates = {args.key: sources[args.key]}
    else:
        candidates = {
            k: v
            for k, v in sources.items()
            if needs_embedding(v, args.force, args.model, CURRENT_EMBEDDING_VERSION)
        }

    if not candidates:
        print("Nothing to embed.")
        return

    print(f"Loading model: {args.model} (first run will download weights)")
    model = get_model(args.model)
    collection = get_collection(args.model)

    done, failed = 0, 0
    for key, entry in candidates.items():
        chunk_count = entry.get("ingestion", {}).get("chunks", "?")
        print(f"Embedding {key} ({chunk_count} chunks)...")
        try:
            if embed_source(key, entry, model, collection, args.model, args.batch_size):
                done += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            failed += 1

    skipped = len(candidates) - done - failed
    print(f"\nDone. {done} source(s) embedded, {failed} failed, {skipped} skipped.")


if __name__ == "__main__":
    main()
