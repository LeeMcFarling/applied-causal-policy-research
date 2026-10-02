"""
Tests for the pipeline's core invariants. Runs without network access or the
embedding model:

    python3 -m unittest discover tests
"""

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
sys.path.insert(0, str(SCRIPTS))

import research_lib  # noqa: E402


def load_script(name: str):
    """Import a hyphenated script (e.g. ingest-research.py) as a module."""
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ingest = load_script("ingest-research")
evaluation = load_script("eval-retrieval")
review_loop = load_script("review-loop")


def run(*args, cwd=REPO):
    return subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True)


class TestAuthorParsing(unittest.TestCase):
    def test_single_inverted_author_is_not_split(self):
        self.assertEqual(ingest.parse_authors("Eichenbaum, Joe"), ["Eichenbaum, Joe"])

    def test_multiple_authors(self):
        self.assertEqual(
            ingest.parse_authors("Agarwal, Sumit, David Lucca, Amit Seru, and Francesco Trebbi"),
            ["Agarwal, Sumit", "David Lucca", "Amit Seru", "Francesco Trebbi"],
        )

    def test_two_authors_and_initials(self):
        self.assertEqual(ingest.parse_authors("Huber, John D., and Nolan McCarty"), ["Huber, John D.", "Nolan McCarty"])

    def test_institutional_and_empty(self):
        self.assertEqual(ingest.parse_authors("RAND Corporation"), ["RAND Corporation"])
        self.assertEqual(ingest.parse_authors(""), [])


class TestExtractionCheck(unittest.TestCase):
    def test_fused_text_is_flagged(self):
        fused = "Violentcrimedevastatesindividuals,families,andcommunities. Beyondthedirectharmtovictims"
        self.assertGreater(research_lib.fused_token_ratio(fused), research_lib.FUSED_TOKEN_WARN_RATIO)

    def test_normal_text_is_not_flagged(self):
        normal = "Violent crime devastates individuals, families, and communities beyond the direct harm to victims."
        self.assertEqual(research_lib.fused_token_ratio(normal), 0.0)

    def test_check_extraction_returns_flagged_pages(self):
        pages = [(1, "A normal page of text."), (2, "Thisisclearlyfusedtextwithnospaces atall")]
        self.assertEqual(ingest.check_extraction(pages), [2])


def count_words(texts):
    """Stand-in tokenizer for tests: one token per whitespace-separated word."""
    return [len(t.split()) for t in texts]


class TestChunking(unittest.TestCase):
    def chunk(self, pages, **kw):
        return ingest.chunk_by_page("key", pages, count_tokens=count_words, **kw)

    def test_chunks_never_cross_page_boundaries(self):
        pages = [(1, "word " * 900), (2, "short page"), (3, "other " * 450)]
        records = self.chunk(pages, max_tokens=256, overlap_tokens=64)
        for r in records:
            self.assertEqual(r["page_start"], r["page_end"])
        self.assertEqual(sorted({r["page_start"] for r in records}), [1, 2, 3])

    def test_chunks_respect_token_budget(self):
        records = self.chunk([(1, "word " * 900)], max_tokens=256, overlap_tokens=64)
        self.assertGreater(len(records), 1)
        self.assertTrue(all(r["token_count"] <= 256 for r in records))

    def test_consecutive_chunks_overlap(self):
        text = " ".join(f"w{i}" for i in range(600))
        records = self.chunk([(1, text)], max_tokens=200, overlap_tokens=50)
        first, second = records[0]["text"].split(), records[1]["text"].split()
        self.assertEqual(first[-50:], second[:50])

    def test_words_are_never_cut(self):
        text = " ".join(f"word{i}" for i in range(500))
        for r in self.chunk([(1, text)], max_tokens=100, overlap_tokens=20):
            self.assertTrue(all(w.startswith("word") for w in r["text"].split()))

    def test_chunk_text_is_an_exact_slice_of_the_page(self):
        text = "Line one of the page.\nLine two,   with  spacing.\nLine three."
        for r in self.chunk([(1, text)], max_tokens=4, overlap_tokens=1):
            self.assertIn(r["text"], text)

    def test_chunk_ids_are_sequential_and_keyed(self):
        records = ingest.chunk_by_page("src-2026", [(1, "one"), (2, "two")], count_tokens=count_words)
        self.assertEqual([r["id"] for r in records], ["src-2026__0000", "src-2026__0001"])

    def test_oversized_chunk_is_rejected(self):
        # A single "word" the stand-in tokenizer counts as over the model limit.
        def huge(texts):
            return [600 for _ in texts]
        with self.assertRaises(ValueError):
            ingest.chunk_by_page("key", [(1, "x")], count_tokens=huge)


class TestEmbeddingStaleness(unittest.TestCase):
    entry = {
        "status": {"embedding": "complete"},
        "ingestion": {"embedding_model": "model-a", "embedding_version": 1},
    }

    def test_current_embedding_is_not_stale(self):
        self.assertFalse(research_lib.needs_embedding(self.entry, False, "model-a", 1))

    def test_model_or_version_change_makes_it_stale(self):
        self.assertTrue(research_lib.needs_embedding(self.entry, False, "model-b", 1))
        self.assertTrue(research_lib.needs_embedding(self.entry, False, "model-a", 2))

    def test_pending_status_is_stale(self):
        pending = {**self.entry, "status": {"embedding": "pending"}}
        self.assertTrue(research_lib.needs_embedding(pending, False, "model-a", 1))


class TestRetrievalMetrics(unittest.TestCase):
    def test_first_relevant_rank(self):
        self.assertEqual(evaluation.first_relevant_rank([30, 15, 13], {15}), 2)
        self.assertIsNone(evaluation.first_relevant_rank([30, 31], {15}))

    def test_distinct_pages_keep_best_rank(self):
        self.assertEqual(evaluation.distinct_pages([15, 15, 13, 15, 30]), [15, 13, 30])

    def test_summary(self):
        rows = [{"rank": 1}, {"rank": 2}, {"rank": None}, {"rank": 5}]
        s = evaluation.summarize(rows, ks=(1, 3))
        self.assertEqual(s["hit@1"], 0.25)
        self.assertEqual(s["hit@3"], 0.5)
        self.assertAlmostEqual(s["MRR"], (1 + 0.5 + 0.2) / 4)


class TestIntegrityChecks(unittest.TestCase):
    def test_public_sample_passes_extract_check(self):
        result = run("scripts/tracker_check.py", "--root", "samples", "--extract")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_empty_corpus_fails_closed(self):
        with tempfile.TemporaryDirectory() as empty:
            self.assertEqual(run("scripts/tracker_check.py", "--root", empty).returncode, 1)
            self.assertEqual(run("scripts/maturity_scan.py", "validate", "--root", empty).returncode, 1)

    def test_phase_above_a_visible_dependency_is_caught(self):
        """A brief may not claim a higher phase than a brief it depends on."""
        with tempfile.TemporaryDirectory() as tmp:
            domain = Path(tmp) / "Policy_Domains" / "Example"
            shutil.copytree(REPO / "samples" / "Policy_Domains" / "Housing_and_Public_Infrastructure", domain)
            zoning = domain / "zoning-function-ladder.md"
            text = zoning.read_text(encoding="utf-8")
            # zoning-function-ladder depends on nothing in the extract; make it depend on the
            # overview (phase 1) while claiming phase 2, which the check must reject.
            text = text.replace("phase: 1\n", "phase: 2\n", 1).replace(
                "dependencies:\n", "dependencies:\n  - housing-public-infrastructure-system-overview\n", 1)
            zoning.write_text(text, encoding="utf-8")
            result = run("scripts/tracker_check.py", "--root", tmp, "--extract")
            self.assertEqual(result.returncode, 1)
            self.assertIn("zoning-function-ladder", result.stdout)


class TestReviewLoop(unittest.TestCase):
    """The review→grade loop, run offline with stand-in models."""

    def run_loop(self, fail_rounds, max_rounds=3):
        reviewer, grader = review_loop.FakeReviewer(), review_loop.FakeGrader(fail_rounds=fail_rounds)
        with tempfile.TemporaryDirectory() as out:
            summary = review_loop.run_loop(
                reviewer=reviewer, grader=grader, search=review_loop.FakeSearch(),
                brief="A brief.", source_text="<!-- Page 1 -->\nSource.", citation="Author. *Title*.",
                max_rounds=max_rounds, out_dir=Path(out))
            files = sorted(p.name for p in Path(out).iterdir())
        return summary, reviewer, files

    def test_stops_as_soon_as_the_review_passes(self):
        summary, _, files = self.run_loop(fail_rounds=1)
        self.assertTrue(summary["passed"])
        self.assertEqual(len(summary["rounds"]), 2)
        self.assertIn("round-2-grading.json", files)
        self.assertNotIn("round-3-review.md", files)

    def test_gives_up_after_max_rounds(self):
        summary, _, _ = self.run_loop(fail_rounds=99, max_rounds=3)
        self.assertFalse(summary["passed"])
        self.assertEqual(len(summary["rounds"]), 3)

    def test_grader_findings_are_sent_back_to_the_reviewer(self):
        _, reviewer, _ = self.run_loop(fail_rounds=1)
        self.assertNotIn("Independent grader's report", reviewer.prompts[0])
        self.assertIn("Independent grader's report", reviewer.prompts[1])
        self.assertIn("Re-check the page cited", reviewer.prompts[1])

    def test_pass_bar_requires_pass_on_all_six_dimensions(self):
        dims = [{"dimension": d, "grade": "A", "passes": True, "findings": ""} for d in review_loop.DIMENSIONS]
        self.assertTrue(review_loop.passes({"overall_verdict": "Pass", "dimensions": dims}))
        self.assertFalse(review_loop.passes({"overall_verdict": "Pass with revisions", "dimensions": dims}))
        self.assertFalse(review_loop.passes({"overall_verdict": "Pass", "dimensions": dims[:5]}))
        one_fails = dims[:5] + [{**dims[5], "passes": False}]
        self.assertFalse(review_loop.passes({"overall_verdict": "Pass", "dimensions": one_fails}))

    def test_invalid_tool_input_returns_an_error_result(self):
        class Block:
            id, name, input = "t1", "search_source", {"query": ""}
        result = review_loop.ClaudeReviewer._run_tool(Block(), review_loop.FakeSearch())
        self.assertTrue(result["is_error"])


if __name__ == "__main__":
    unittest.main()
