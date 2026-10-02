# Retrieval Evaluation: 17A Source

This evaluates how well the pipeline's retrieval step finds the page that answers a question. The question set ([`17a-retrieval-questions.yaml`](./17a-retrieval-questions.yaml)) has 15 questions, each labeled with the page(s) that actually answer it; the labels were set by locating the answering passage in the source text (quoted in each question's `evidence` field), not by looking at what retrieval returned.

Reproduce the current numbers with:

```bash
python3 scripts/eval-retrieval.py
```

That command evaluates the current vector store. The earlier versions' stores are not kept in the repository; their figures were produced with the same script via `--vector-store`. Results are ranked by distinct page, so a page counts once at its best rank even when several of its chunks score highly.

**Metrics.** *hit@k* is the share of questions whose answering page appears in the top *k* retrieved pages. *MRR* (mean reciprocal rank) averages 1 / (rank of the first answering page), so a correct first result scores 1.0 and a correct third result scores 0.33. With 15 questions, one question moves a hit rate by about 0.07, so differences should be read question by question as well as in aggregate.

## Results Across Versions

| Version | Extraction | Chunking | hit@1 | hit@3 | hit@5 | MRR |
|---|---|---|---:|---:|---:|---:|
| v2 | pdfplumber default (fused words) | whole page (≤4,000 chars) | 0.73 | 0.80 | 0.87 | 0.79 |
| v3 | `x_tolerance=1` | whole page (≤4,000 chars) | 0.67 | 0.87 | 0.93 | 0.78 |
| **v4 (current)** | `x_tolerance=1` | **256 tokens, 64 overlap** | 0.67 | **1.00** | **1.00** | 0.80 |

### v2 → v3: fixing extraction

pdfplumber's default spacing tolerance fused most words on this PDF together (1,185 fused runs of 18+ letters; about 3,000 recoverable words). Setting `x_tolerance=1` recovered about 11,900 words and cut fused runs to 36. Retrieval improved on the pages whose text had been most garbled: the Peavy Road encampment question (rank 2 → 1, the page the independent grader cited when it caught the fabricated claim in Pass 2 of the review), the roadmap question (4 → 2), and the middle-tier decline question (6 → 2). Two questions slipped, and one, street lighting, was not retrieved in the top 10 by either version.

### v3 → v4: chunking by tokens

Evaluating v3 surfaced two problems with whole-page chunks:

1. **Truncation.** `bge-large-en-v1.5` reads at most 512 tokens, and 13 of 42 page chunks (31%) were longer, up to 680 tokens. Text past the limit was silently dropped from the embedding. The 4,000-character cap never triggered, because 4,000 characters is roughly 800–1,000 tokens.
2. **Dilution.** The street-lighting statistic sat well inside the token limit on both of its pages, yet was never retrieved: a whole-page embedding blends a one-sentence fact with everything else on the page.

v4 splits each page into chunks of at most 256 tokens, measured with the embedding model's own tokenizer, with 64 tokens of overlap, breaking only on whitespace and never crossing a page boundary. The 42 pages became 97 chunks (median 254 tokens, maximum 256; none near the 512 limit), and ingestion now refuses to write any chunk over the limit.

The street-lighting question went from not retrieved to rank 1, and every question's answering page now appears in the top three. hit@1 did not improve: three questions moved from rank 2 to rank 3 (roadmap, middle-tier decline) or 1 to 3 (the 1991 crime rate, where a definitions page now outranks the data table).

## Chunk-Size Sensitivity

To check that 256 tokens was not an arbitrary win, the same pipeline was run at two other sizes:

| Chunk size (overlap) | Chunks | hit@1 | hit@3 | hit@5 | MRR |
|---|---:|---:|---:|---:|---:|
| 400 tokens (100) | 66 | 0.53 | 0.87 | 0.87 | 0.73 |
| **256 tokens (64), current default** | 97 | 0.67 | 1.00 | 1.00 | 0.80 |
| 128 tokens (32) | 189 | 0.73 | 1.00 | 1.00 | 0.89 |

The trend is consistent: smaller chunks rank the answering page higher, and 400-token chunks reintroduce the street-lighting miss (rank 9). The default stays at 256 for now. It was chosen before these results were measured, and switching to whichever size scored best on the same 15 questions used to measure it would tune the pipeline to this question set. Smaller chunks also carry less surrounding context into a review, which `query-research.py` offsets by expanding each hit with its neighboring chunks (`--radius`). The 128-token result is a candidate to confirm on a larger question set or a second source.

## Remaining Weaknesses

- **Reference lists compete with the text they cite.** Page 40 (data sources) and other appendix pages appear among the top results for several questions, because bibliography entries share vocabulary with the findings they cite. Excluding or down-weighting reference sections at ingest is a natural next step.
- **Statistics-heavy appendix pages attract "how much" questions.** Pages dense with numbers outrank the narrative page that states the finding in plain language.
- **One source, fifteen questions.** These results describe this document; they are a test harness for future changes, not a general claim about the pipeline.

## Detailed Results

#### v2: default extraction, whole-page chunks

| Metric | Value |
|---|---|
| hit@1 | 0.73 |
| hit@3 | 0.80 |
| hit@5 | 0.87 |
| MRR | 0.79 |

| Question | Relevant pages | Top 3 retrieved | Rank of first relevant |
|---|---|---|---|
| What share of city geography accounts for 20% of violent crime? | [3, 8] | [3, 6, 23] | 1 |
| How much does improved street lighting reduce outdoor nighttime crime? | [4, 11] | [30, 37, 3] | >10 |
| What did the randomized trial find about cleaning and greening vacant lots? | [4, 11] | [11, 14, 21] | 1 |
| How does the paper define violent crime? | [23] | [23, 3, 5] | 1 |
| What happened with the homeless encampment property on Peavy Road in Far East Dallas? | [15] | [13, 15, 26] | 2 |
| Which cities saw their chronic hotspots get worse? | [8] | [8, 10, 3] | 1 |
| What should city leaders do during weeks 5 to 8 of the roadmap? | [20] | [18, 2, 11] | 4 |
| Why is percent change misleading for small crime counts in grid cells? | [32] | [32, 37, 36] | 1 |
| How much did violent crime decline in middle-tier intervention areas compared with similar areas? | [16] | [30, 31, 7] | 6 |
| What do the incidence rate ratio tests show by concentration tier? | [34] | [34, 28, 17] | 1 |
| What kind of firm does the author work for? | [22] | [22, 2, 4] | 1 |
| What was the national violent crime rate at its 1991 peak? | [24] | [24, 5, 3] | 1 |
| How much do the highest-crime areas change from one year to the next? | [3, 9] | [3, 36, 32] | 1 |
| What is the risk of confusing activity with impact? | [21] | [21, 4, 16] | 1 |
| Which organization did Dallas partner with to run the coordinated approach? | [13] | [13, 26, 15] | 1 |


#### v3: fixed extraction, whole-page chunks

| Metric | Value |
|---|---|
| hit@1 | 0.67 |
| hit@3 | 0.87 |
| hit@5 | 0.93 |
| MRR | 0.78 |

| Question | Relevant pages | Top 3 retrieved | Rank of first relevant |
|---|---|---|---|
| What share of city geography accounts for 20% of violent crime? | [3, 8] | [3, 6, 23] | 1 |
| How much does improved street lighting reduce outdoor nighttime crime? | [4, 11] | [31, 3, 35] | >10 |
| What did the randomized trial find about cleaning and greening vacant lots? | [4, 11] | [31, 35, 21] | 5 |
| How does the paper define violent crime? | [23] | [23, 3, 5] | 1 |
| What happened with the homeless encampment property on Peavy Road in Far East Dallas? | [15] | [15, 14, 13] | 1 |
| Which cities saw their chronic hotspots get worse? | [8] | [8, 28, 38] | 1 |
| What should city leaders do during weeks 5 to 8 of the roadmap? | [20] | [18, 20, 2] | 2 |
| Why is percent change misleading for small crime counts in grid cells? | [32] | [32, 33, 35] | 1 |
| How much did violent crime decline in middle-tier intervention areas compared with similar areas? | [16] | [31, 16, 30] | 2 |
| What do the incidence rate ratio tests show by concentration tier? | [34] | [34, 17, 26] | 1 |
| What kind of firm does the author work for? | [22] | [22, 2, 1] | 1 |
| What was the national violent crime rate at its 1991 peak? | [24] | [24, 23, 5] | 1 |
| How much do the highest-crime areas change from one year to the next? | [3, 9] | [32, 9, 31] | 2 |
| What is the risk of confusing activity with impact? | [21] | [21, 4, 20] | 1 |
| Which organization did Dallas partner with to run the coordinated approach? | [13] | [13, 30, 4] | 1 |


#### v4: fixed extraction, 256-token chunks

| Metric | Value |
|---|---|
| hit@1 | 0.67 |
| hit@3 | 1.00 |
| hit@5 | 1.00 |
| MRR | 0.80 |

| Question | Relevant pages | Top 3 retrieved | Rank of first relevant |
|---|---|---|---|
| What share of city geography accounts for 20% of violent crime? | [3, 8] | [3, 23, 6] | 1 |
| How much does improved street lighting reduce outdoor nighttime crime? | [4, 11] | [11, 40, 31] | 1 |
| What did the randomized trial find about cleaning and greening vacant lots? | [4, 11] | [40, 11, 3] | 2 |
| How does the paper define violent crime? | [23] | [23, 3, 5] | 1 |
| What happened with the homeless encampment property on Peavy Road in Far East Dallas? | [15] | [15, 13, 14] | 1 |
| Which cities saw their chronic hotspots get worse? | [8] | [8, 10, 29] | 1 |
| What should city leaders do during weeks 5 to 8 of the roadmap? | [20] | [18, 2, 20] | 3 |
| Why is percent change misleading for small crime counts in grid cells? | [32] | [32, 33, 36] | 1 |
| How much did violent crime decline in middle-tier intervention areas compared with similar areas? | [16] | [31, 34, 16] | 3 |
| What do the incidence rate ratio tests show by concentration tier? | [34] | [34, 33, 35] | 1 |
| What kind of firm does the author work for? | [22] | [22, 18, 2] | 1 |
| What was the national violent crime rate at its 1991 peak? | [24] | [23, 5, 24] | 3 |
| How much do the highest-crime areas change from one year to the next? | [3, 9] | [6, 9, 8] | 2 |
| What is the risk of confusing activity with impact? | [21] | [21, 4, 13] | 1 |
| Which organization did Dallas partner with to run the coordinated approach? | [13] | [13, 30, 15] | 1 |

