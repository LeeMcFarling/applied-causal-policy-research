"""
Shared contract for the FP research library pipeline.

ingest-research.py, embed-research.py, and query-research.py (and any future
review agent) all import from here rather than redefining paths, index.yaml
I/O, RAG record I/O, or model/collection naming independently. Divergence
between those definitions across scripts is exactly the kind of bug this
module exists to make impossible.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
ORIGINALS_DIR = REPO_ROOT / "research-library" / "originals"
SOURCES_DIR = REPO_ROOT / "research-library" / "sources"
RAG_DIR = REPO_ROOT / "research-library" / "rag"
INDEX_YAML = REPO_ROOT / "research-library" / "index.yaml"
INDEX_MD = REPO_ROOT / "research-library" / "index.md"
VECTOR_STORE_DIR = REPO_ROOT / "research-library" / "vector-store"

# ---------------------------------------------------------------------------
# Versioning / model defaults
# ---------------------------------------------------------------------------

CURRENT_CHUNKER_VERSION = 2
DEFAULT_MAX_CHARS = 4000
DEFAULT_OVERLAP_CHARS = 500

DEFAULT_EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
CURRENT_EMBEDDING_VERSION = 1
# bge models are asymmetric: queries need this instruction prefix, passages
# (embedded in embed-research.py) do not.
QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "


# ---------------------------------------------------------------------------
# index.yaml (ruamel round-trip mode so hand edits survive machine writes)
# ---------------------------------------------------------------------------

def _get_yaml():
    try:
        from ruamel.yaml import YAML
    except ImportError:
        print("Error: ruamel.yaml not installed. Run: pip3 install ruamel.yaml --break-system-packages")
        sys.exit(1)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 120
    yaml.indent(mapping=2, sequence=2, offset=0)
    return yaml


def load_index(index_path: Path = INDEX_YAML) -> dict:
    yaml = _get_yaml()
    if not index_path.exists():
        return {"sources": {}}
    with index_path.open("r", encoding="utf-8") as f:
        data = yaml.load(f)
    if data is None:
        data = {}
    data.setdefault("sources", {})
    return data


def save_index(index: dict, index_path: Path = INDEX_YAML) -> None:
    yaml = _get_yaml()
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("w", encoding="utf-8") as f:
        yaml.dump(index, f)


def regenerate_index_md(index: dict, out_path: Path = INDEX_MD) -> None:
    """Generated browsing view. Never hand-edit this file -- edit index.yaml."""
    lines = [
        "# Research Library Index\n",
        "_Generated from `index.yaml`. Do not hand-edit -- edit that file instead._\n",
        "\n## Sources\n",
    ]
    for key, entry in sorted(index.get("sources", {}).items()):
        institution = entry.get("institution", "")
        tags = entry.get("tags", []) or []
        rel_md = entry.get("source", {}).get("extracted", f"research-library/sources/{key}.md")
        tag_str = ", ".join(tags) if tags else "untagged"
        lines.append(f"- [{key}]({rel_md}) — {institution} — {tag_str}\n")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# RAG records (canonical chunk storage -- the vector store is only ever a
# locator into these files, never the evidence itself)
# ---------------------------------------------------------------------------

def load_rag_records(citation_key: str, rag_dir: Path = RAG_DIR) -> list[dict]:
    path = rag_dir / f"{citation_key}.jsonl"
    records = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def write_rag_records(key: str, records: list[dict], rag_dir: Path = RAG_DIR) -> Path:
    rag_dir.mkdir(parents=True, exist_ok=True)
    out_path = rag_dir / f"{key}.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return out_path


def expand_chunk(citation_key: str, chunk_index: int, radius: int = 1) -> list[dict]:
    """Retrieve exact chunks from the canonical JSONL, independent of the
    vector store -- the vector store only ever tells us the chunk_index."""
    records = load_rag_records(citation_key)
    start = max(0, chunk_index - radius)
    end = min(len(records), chunk_index + radius + 1)
    return records[start:end]


def merge_hit_windows(hits: list[tuple], radius: int) -> dict[str, set]:
    """
    Collapse overlapping expansion windows from multiple vector hits in the
    same source into one set of chunk indices per citation_key, so adjacent
    hits (e.g. chunks 27 and 28 both scoring highly) don't produce duplicated,
    overlapping context when formatted for an LLM.
    """
    windows: dict[str, set] = {}
    for _, meta, _ in hits:
        key = meta["citation_key"]
        idx = meta["chunk_index"]
        windows.setdefault(key, set())
        for i in range(idx - radius, idx + radius + 1):
            if i >= 0:
                windows[key].add(i)
    return windows


def load_merged_windows(windows: dict[str, set]) -> list[dict]:
    """Given {citation_key: {chunk_index, ...}} from merge_hit_windows(),
    load each source's JSONL once and return the requested chunks in order,
    grouped by source."""
    all_records = []
    for citation_key, indices in windows.items():
        records = load_rag_records(citation_key)
        for i in sorted(indices):
            if 0 <= i < len(records):
                all_records.append(records[i])
    return all_records


def format_context(records: list[dict], index: dict) -> str:
    sections = []
    for r in records:
        entry = index.get("sources", {}).get(r["citation_key"], {})
        chicago = entry.get("chicago", r["citation_key"])
        pages = f"p. {r['page_start']}" if r["page_start"] == r["page_end"] else f"pp. {r['page_start']}-{r['page_end']}"
        sections.append(
            f"SOURCE: {r['citation_key']} ({pages}, chunk {r['chunk_index']})\n"
            f"CITATION: {chicago}\n\n{r['text']}"
        )
    return "\n\n---\n\n".join(sections)


# ---------------------------------------------------------------------------
# Embedding status / model+collection naming
# ---------------------------------------------------------------------------

def mark_embedding_complete(
    citation_key: str,
    embedding_model: str,
    embedding_version: int,
    embedded_chunk_count: int,
    index_path: Path = INDEX_YAML,
) -> None:
    """
    Called once every chunk for a source has successfully landed in the
    vector store. Transactional at the citation-key level: refuses to mark
    complete on a partial run, so a crash mid-batch leaves status.embedding
    at 'pending' rather than lying about it.
    """
    index = load_index(index_path)
    source = index["sources"][citation_key]
    expected = source["ingestion"]["chunks"]
    if embedded_chunk_count != expected:
        raise ValueError(
            f"Embedding incomplete for {citation_key}: "
            f"{embedded_chunk_count}/{expected} chunks"
        )
    source["ingestion"]["embedding_model"] = embedding_model
    source["ingestion"]["embedding_version"] = embedding_version
    source["status"]["embedding"] = "complete"
    save_index(index, index_path)


def needs_embedding(
    entry: dict,
    force: bool,
    model_name: str,
    embedding_version: int,
) -> bool:
    """
    Model-aware staleness check: a source embedded under a different model
    or a different embedding_version is NOT considered complete, even if
    status.embedding says so -- that status was only ever true for the
    vector space it was embedded into.
    """
    if force:
        return True
    status = entry.get("status", {})
    ingestion = entry.get("ingestion", {})
    return (
        status.get("embedding") != "complete"
        or ingestion.get("embedding_model") != model_name
        or ingestion.get("embedding_version") != embedding_version
    )


def collection_name_for(model_name: str) -> str:
    """One Chroma collection per model name, so switching embedding models
    can't silently mix incompatible vector spaces together."""
    return "chunks__" + model_name.replace("/", "__")


def get_model(model_name: str):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Error: sentence-transformers not installed. Run: pip3 install sentence-transformers --break-system-packages")
        sys.exit(1)
    return SentenceTransformer(model_name)
