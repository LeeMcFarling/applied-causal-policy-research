#!/usr/bin/env python3
"""
Run the adversarial review and the cross-provider grading as one loop.

Each round:
  1. A Claude reviewer writes (or revises) an adversarial review of a policy brief
     against one research source, following reviews/_REVIEW_TEMPLATE.md. It gathers
     evidence through a `search_source` tool backed by this repository's retrieval
     pipeline, so every page it cites comes from a retrieved, page-bounded chunk.
  2. An OpenAI grader, from a different provider, grades the review's fidelity
     against the full source text, the brief, and reviews/validation/_GRADING_TEMPLATE.md,
     returning a structured verdict for each of the template's six dimensions.
  3. If the review passes (overall verdict "Pass" and every dimension passes), the
     loop stops. Otherwise the grader's findings and required fixes go back to the
     reviewer for the next round, up to --max-rounds.

Every round's review and grading are written to a run directory so the whole
exchange can be audited. The loop never marks a review complete: a passing review
still goes to human page-level verification (AUTOMATION_README.md, Phase 3.6).

Usage:
    python3 scripts/review-loop.py \\
        --source 17a-reducing-violent-crime-2026 \\
        --brief samples/Policy_Domains/Housing_and_Public_Infrastructure/community-stabilization-framework.md

    python3 scripts/review-loop.py --source ... --brief ... --dry-run   # offline, no API calls

Requires (live runs):
    pip3 install anthropic openai
    ANTHROPIC_API_KEY (or an `ant auth login` profile) and OPENAI_API_KEY
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from research_lib import (
    DEFAULT_EMBEDDING_MODEL,
    INDEX_YAML,
    QUERY_INSTRUCTION,
    REPO_ROOT,
    SOURCES_DIR,
    VECTOR_STORE_DIR,
    collection_name_for,
    format_context,
    load_index,
    load_merged_windows,
    merge_hit_windows,
)

REVIEW_TEMPLATE = REPO_ROOT / "research-library" / "reviews" / "_REVIEW_TEMPLATE.md"
GRADING_TEMPLATE = REPO_ROOT / "research-library" / "reviews" / "validation" / "_GRADING_TEMPLATE.md"
RUNS_DIR = REPO_ROOT / "research-library" / "reviews" / "runs"

DEFAULT_REVIEWER_MODEL = "claude-opus-5-5"
DEFAULT_GRADER_MODEL = "gpt-5"
DEFAULT_MAX_ROUNDS = 3
MAX_TOOL_STEPS = 40  # reviewer tool calls allowed per round before giving up

# The six dimensions of reviews/validation/_GRADING_TEMPLATE.md.
DIMENSIONS = [
    "Source material fidelity",
    "Brief fidelity",
    "Template compliance",
    "Citation accuracy",
    "Coverage completeness",
    "Adversarial rigor",
]
VERDICTS = ["Pass", "Pass with revisions", "Fail"]

GRADING_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["dimensions", "overall_verdict", "summary", "required_fixes"],
    "properties": {
        "dimensions": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["dimension", "grade", "passes", "findings"],
                "properties": {
                    "dimension": {"type": "string", "enum": DIMENSIONS},
                    "grade": {"type": "string", "description": "Letter grade, e.g. A, B+, C"},
                    "passes": {"type": "boolean"},
                    "findings": {"type": "string"},
                },
            },
        },
        "overall_verdict": {"type": "string", "enum": VERDICTS},
        "summary": {"type": "string"},
        "required_fixes": {"type": "array", "items": {"type": "string"}},
    },
}

SEARCH_TOOL = {
    "name": "search_source",
    "description": (
        "Search the research source for passages relevant to a question or claim. Returns the "
        "best-matching passages with their exact page numbers. Use it for every claim you attribute "
        "to the source, and cite the page number it returns. Call it as many times as you need."
    ),
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["query"],
        "properties": {
            "query": {"type": "string", "description": "What to look for in the source."},
            "top_k": {"type": "integer", "description": "Number of passages to return (1-10, default 6)."},
        },
    },
    # The request is streamed, so tool input streams as it is generated and is not
    # validated by the API; ClaudeReviewer._run_tool validates it before searching.
    "eager_input_streaming": True,
}

REVIEWER_SYSTEM = """You write adversarial research reviews of policy briefs. Your job is to test a brief against one research source, not to defend it.

Follow the review template you are given exactly, section by section. Define the source's scope first, and judge the brief only against what the source actually sets out to establish.

Every statement you attribute to the source must come from a passage returned by the search_source tool, and must carry the page number that passage came from, as (p. N). Do not cite a page you have not retrieved. If the source is silent on something, say so rather than inferring what it would say. Do not invent case outcomes, statistics, or quotations.

Return only the finished review in Markdown, starting with the template's frontmatter. Set grading_status to "pending"; the review is graded and verified by others after you finish."""

GRADER_INSTRUCTIONS = """You are an independent grader auditing an AI-written adversarial research review for fidelity. You are from a different model provider than the review's author, so that the two do not share blind spots.

Follow the grading template you are given. Grade only fidelity: whether the review accurately and completely represents the source and the brief, follows the template, and cites pages that actually contain what it attributes to them. Do not grade whether the brief's policy is wise.

Check page citations against the full source text you are given, which is marked with page numbers. Sample parts of the source the review did not cite, and report anything it missed.

For each of the six dimensions, give a letter grade, set passes to true only if that dimension needs no fixes, and explain your findings. The overall verdict is "Pass" only if every dimension passes; "Pass with revisions" if the fixes are limited; "Fail" if the review needs to be redone. List every required fix specifically enough that the review's author can act on it."""


# --------------------------------------------------------------------------
# Retrieval tool
# --------------------------------------------------------------------------

class SourceSearch:
    """Answers search_source tool calls from the local vector store, restricted to one source."""

    def __init__(self, citation_key: str, radius: int = 1):
        import chromadb
        from research_lib import get_model

        self.key = citation_key
        self.radius = radius
        self.index = load_index(INDEX_YAML)
        self.model = get_model(DEFAULT_EMBEDDING_MODEL)
        client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
        self.collection = client.get_collection(collection_name_for(DEFAULT_EMBEDDING_MODEL))

    def search(self, query: str, top_k: int = 6) -> str:
        vector = self.model.encode([QUERY_INSTRUCTION + query], normalize_embeddings=True)[0].tolist()
        result = self.collection.query(query_embeddings=[vector], n_results=top_k, where={"citation_key": self.key})
        hits = list(zip(result["ids"][0], result["metadatas"][0], result["distances"][0]))
        if not hits:
            return "No passages found."
        records = load_merged_windows(merge_hit_windows(hits, radius=self.radius))
        return format_context(records, self.index)


# --------------------------------------------------------------------------
# Reviewer (Anthropic) and grader (OpenAI)
# --------------------------------------------------------------------------

class ReviewError(RuntimeError):
    pass


class ClaudeReviewer:
    def __init__(self, model: str = DEFAULT_REVIEWER_MODEL, effort: str = "high"):
        import anthropic

        self.client = anthropic.Anthropic()
        self.model = model
        self.effort = effort

    def _request(self, messages: list) -> object:
        # Streamed so a long review does not hit request timeouts. Server-side fallback
        # ("default") re-runs a safety-classifier decline on Anthropic's recommended model.
        with self.client.beta.messages.stream(
            model=self.model,
            max_tokens=64000,
            system=REVIEWER_SYSTEM,
            tools=[SEARCH_TOOL],
            messages=messages,
            thinking={"type": "adaptive"},
            output_config={"effort": self.effort},
            cache_control={"type": "ephemeral"},
            betas=["server-side-fallback-2026-07-01"],
            extra_body={"fallbacks": "default"},
        ) as stream:
            return stream.get_final_message()

    def write_review(self, prompt: str, search: SourceSearch) -> tuple[str, dict]:
        messages = [{"role": "user", "content": prompt}]
        usage = {"input_tokens": 0, "output_tokens": 0, "tool_calls": 0}
        for _ in range(MAX_TOOL_STEPS):
            message = self._request(messages)
            usage["input_tokens"] += message.usage.input_tokens
            usage["output_tokens"] += message.usage.output_tokens

            if message.stop_reason == "refusal":
                raise ReviewError(f"Reviewer declined the request: {message.stop_details}")
            if message.stop_reason == "max_tokens":
                raise ReviewError("Reviewer hit max_tokens before finishing the review")

            # Append the full content unchanged, including thinking blocks.
            messages.append({"role": "assistant", "content": message.content})
            if message.stop_reason == "pause_turn":
                continue
            if message.stop_reason == "tool_use":
                results = []
                for block in message.content:
                    if block.type != "tool_use":
                        continue
                    usage["tool_calls"] += 1
                    results.append(self._run_tool(block, search))
                messages.append({"role": "user", "content": results})
                continue

            review = "".join(block.text for block in message.content if block.type == "text").strip()
            if not review:
                raise ReviewError("Reviewer finished without returning a review")
            return review, usage
        raise ReviewError(f"Reviewer did not finish within {MAX_TOOL_STEPS} tool steps")

    @staticmethod
    def _run_tool(block, search: SourceSearch) -> dict:
        args = block.input if isinstance(block.input, dict) else {}
        query, top_k = args.get("query"), args.get("top_k", 6)
        if block.name != "search_source" or not isinstance(query, str) or not query.strip() \
                or not isinstance(top_k, int):
            return {"type": "tool_result", "tool_use_id": block.id, "is_error": True,
                    "content": "Invalid input: search_source needs a non-empty 'query' string "
                               "and an optional integer 'top_k'."}
        return {"type": "tool_result", "tool_use_id": block.id,
                "content": search.search(query, max(1, min(top_k, 10)))}


class OpenAIGrader:
    def __init__(self, model: str = DEFAULT_GRADER_MODEL):
        from openai import OpenAI

        self.client = OpenAI()
        self.model = model

    def grade(self, prompt: str) -> tuple[dict, dict]:
        response = self.client.responses.create(
            model=self.model,
            instructions=GRADER_INSTRUCTIONS,
            input=prompt,
            text={"format": {"type": "json_schema", "name": "fidelity_grading",
                             "schema": GRADING_SCHEMA, "strict": True}},
        )
        usage = {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens}
        return json.loads(response.output_text), usage


# --------------------------------------------------------------------------
# Offline stand-ins for --dry-run and tests
# --------------------------------------------------------------------------

class FakeSearch:
    def search(self, query: str, top_k: int = 6) -> str:
        return f"SOURCE: dry-run (p. 1, chunk 0)\n\n[passage matching: {query}]"


class FakeReviewer:
    model = "dry-run-reviewer"

    def __init__(self):
        self.prompts: list[str] = []

    def write_review(self, prompt: str, search) -> tuple[str, dict]:
        self.prompts.append(prompt)
        evidence = search.search("source scope")
        return (f"# Research Review (dry run, round {len(self.prompts)})\n\n{evidence}\n",
                {"input_tokens": 0, "output_tokens": 0, "tool_calls": 1})


class FakeGrader:
    """Fails the first `fail_rounds` rounds with one required fix, then passes."""

    model = "dry-run-grader"

    def __init__(self, fail_rounds: int = 1):
        self.fail_rounds = fail_rounds
        self.calls = 0

    def grade(self, prompt: str) -> tuple[dict, dict]:
        self.calls += 1
        failing = self.calls <= self.fail_rounds
        grading = {
            "dimensions": [{"dimension": d, "grade": "B" if failing and d == "Citation accuracy" else "A",
                            "passes": not (failing and d == "Citation accuracy"), "findings": "dry run"}
                           for d in DIMENSIONS],
            "overall_verdict": "Pass with revisions" if failing else "Pass",
            "summary": "dry run",
            "required_fixes": ["Re-check the page cited for the dry-run claim."] if failing else [],
        }
        return grading, {"input_tokens": 0, "output_tokens": 0}


# --------------------------------------------------------------------------
# The loop
# --------------------------------------------------------------------------

def passes(grading: dict) -> bool:
    """The pass bar: overall verdict "Pass" and all six dimensions present and passing."""
    dims = {d["dimension"]: d["passes"] for d in grading.get("dimensions", [])}
    return (grading.get("overall_verdict") == "Pass"
            and set(dims) == set(DIMENSIONS)
            and all(dims.values()))


def render_grading(grading: dict, *, round_no: int, grader_model: str, reviewer_model: str) -> str:
    lines = [
        f"# Fidelity Grading: Round {round_no}",
        "",
        f"**Grading model:** {grader_model} (review authored by {reviewer_model})  ",
        f"**Overall verdict:** {grading['overall_verdict']}  ",
        f"**Meets the pass bar:** {'yes' if passes(grading) else 'no'}",
        "",
        "| Dimension | Grade | Passes |",
        "|---|---|---|",
    ]
    lines += [f"| {d['dimension']} | {d['grade']} | {'yes' if d['passes'] else 'no'} |" for d in grading["dimensions"]]
    lines += ["", "## Summary", "", grading["summary"], "", "## Findings", ""]
    for d in grading["dimensions"]:
        lines += [f"### {d['dimension']}", "", d["findings"], ""]
    lines += ["## Required Fixes", ""]
    lines += [f"{i}. {fix}" for i, fix in enumerate(grading["required_fixes"], 1)] or ["None."]
    return "\n".join(lines) + "\n"


def reviewer_prompt(*, brief: str, template: str, citation: str, previous: tuple[str, str] | None) -> str:
    parts = [
        "Write an adversarial research review of the policy brief below against one research source, "
        "using the review template below.",
        f"## Source\n\n{citation}\n\nSearch it with the search_source tool.",
        f"## Review template\n\n{template}",
        f"## Policy brief\n\n{brief}",
    ]
    if previous:
        review, grading_md = previous
        parts += [
            "## Your previous review\n\n" + review,
            "## Independent grader's report on that review\n\n" + grading_md,
            "Revise the review to resolve every required fix and finding above. Re-check each cited "
            "passage with search_source before keeping it. Return the complete revised review.",
        ]
    return "\n\n".join(parts)


def grader_prompt(*, source_text: str, brief: str, review: str, template: str) -> str:
    return "\n\n".join([
        f"## Grading template\n\n{template}",
        f"## Review to grade\n\n{review}",
        f"## Policy brief\n\n{brief}",
        f"## Full source text (page markers show page numbers)\n\n{source_text}",
    ])


def run_loop(*, reviewer, grader, search, brief: str, source_text: str, citation: str,
             max_rounds: int, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    review_template = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    grading_template = GRADING_TEMPLATE.read_text(encoding="utf-8")
    rounds, previous = [], None

    for round_no in range(1, max_rounds + 1):
        print(f"Round {round_no}: reviewing...", flush=True)
        review, review_usage = reviewer.write_review(
            reviewer_prompt(brief=brief, template=review_template, citation=citation, previous=previous), search)
        (out_dir / f"round-{round_no}-review.md").write_text(review + "\n", encoding="utf-8")

        print(f"Round {round_no}: grading...", flush=True)
        grading, grading_usage = grader.grade(
            grader_prompt(source_text=source_text, brief=brief, review=review, template=grading_template))
        grading_md = render_grading(grading, round_no=round_no, grader_model=grader.model, reviewer_model=reviewer.model)
        (out_dir / f"round-{round_no}-grading.json").write_text(json.dumps(grading, indent=2) + "\n", encoding="utf-8")
        (out_dir / f"round-{round_no}-grading.md").write_text(grading_md, encoding="utf-8")

        passed = passes(grading)
        rounds.append({"round": round_no, "verdict": grading["overall_verdict"], "passed": passed,
                       "required_fixes": len(grading["required_fixes"]),
                       "reviewer_usage": review_usage, "grader_usage": grading_usage})
        print(f"Round {round_no}: {grading['overall_verdict']} "
              f"({len(grading['required_fixes'])} required fixes)", flush=True)
        if passed:
            break
        previous = (review, grading_md)

    summary = {
        "reviewer_model": reviewer.model,
        "grader_model": grader.model,
        "max_rounds": max_rounds,
        "passed": rounds[-1]["passed"],
        "rounds": rounds,
        "next_step": ("Human page-level verification (AUTOMATION_README.md, Phase 3.6) before the review is "
                      "marked complete." if rounds[-1]["passed"] else
                      f"Did not reach a passing grade in {max_rounds} rounds; review the last grading report by hand."),
    }
    (out_dir / "run-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description="Review a brief against a source, grade it, and repeat until it passes.")
    parser.add_argument("--source", required=True, help="citation key of an ingested, embedded source")
    parser.add_argument("--brief", required=True, type=Path, help="path to the policy brief")
    parser.add_argument("--max-rounds", type=int, default=DEFAULT_MAX_ROUNDS)
    parser.add_argument("--reviewer-model", default=DEFAULT_REVIEWER_MODEL)
    parser.add_argument("--grader-model", default=DEFAULT_GRADER_MODEL)
    parser.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--out-dir", type=Path, help="where to write the run (default: reviews/runs/<brief>/<timestamp>)")
    parser.add_argument("--dry-run", action="store_true", help="exercise the loop offline with stand-in models")
    args = parser.parse_args()

    entry = load_index(INDEX_YAML)["sources"].get(args.source)
    if entry is None:
        sys.exit(f"No source {args.source!r} in index.yaml")
    brief_path = args.brief if args.brief.is_absolute() else REPO_ROOT / args.brief
    brief = brief_path.read_text(encoding="utf-8")
    source_text = (SOURCES_DIR / f"{args.source}.md").read_text(encoding="utf-8")

    if args.dry_run:
        reviewer, grader, search = FakeReviewer(), FakeGrader(), FakeSearch()
        out_dir = args.out_dir or Path(tempfile.mkdtemp(prefix="review-loop-dry-run-"))
    else:
        reviewer = ClaudeReviewer(args.reviewer_model, args.effort)
        grader = OpenAIGrader(args.grader_model)
        search = SourceSearch(args.source)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = args.out_dir or RUNS_DIR / brief_path.stem / stamp

    summary = run_loop(reviewer=reviewer, grader=grader, search=search, brief=brief, source_text=source_text,
                       citation=entry["chicago"], max_rounds=args.max_rounds, out_dir=out_dir)
    print(f"\n{'Passed' if summary['passed'] else 'Did not pass'} after {len(summary['rounds'])} round(s).")
    print(f"Run written to: {out_dir}")
    print(f"Next: {summary['next_step']}")
    sys.exit(0 if summary["passed"] else 2)


if __name__ == "__main__":
    main()
