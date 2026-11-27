# Scripture importer pilot: test record

Date: 2026-11-27

## Purpose

Check whether the existing Legal-AI portable importer can index a scripture passage and return its text and source information. This is a one-passage smoke test, not a full search-system evaluation.

## Input

- Source: Vijñānabhairava, Muktabodha catalogue M00271, manuscript BHU C4245.
- Source URL: https://muktabodha-digital-library.org/texts/IAST/M00271
- Input: source verse 1, copied from the locally converted Markdown into one UTF-8 JSON Lines record.
- Fields: `document_id`, `title`, `text`, `locator`, `section_number`, `source_url`, `source_version`, and `chunk_id`.
- Markdown SHA-256: `23f7a03c116c6572cf68190464b847dc184ad6806d6c7b1349a13cb11d217fca`.
- JSONL SHA-256: `d3c8eb203c2faf82c5cb41c513c81f81f77a5f447d89bc2d4d7f7346ddee0bcd`.
- A separate facet JSONL record was keyed by the same chunk ID. Search-time facet filtering was not tested.

## Method and output

The existing [Legal-AI importer](https://github.com/aispanda/Legal-AI/blob/adf4fea92b39dc38338a26535902f18eafdd48b2/build_corpus.py) and [architecture documentation](https://github.com/aispanda/Legal-AI/blob/adf4fea92b39dc38338a26535902f18eafdd48b2/docs/architecture.md) guided the test. The local checkout was at revision `adf4fea92b39dc38338a26535902f18eafdd48b2`; its existing Python 3.14 environment used Tantivy 0.27.0.

The importer built a separate temporary index and reported one indexed record. A keyword query for `rudrayāmalasambhavam` returned the passage. An exact lookup using `Vijñānabhairava section 1` also returned it. Both results preserved the copied verse, title, source URL, `source verse 1` locator, chunk ID, and source version hash.

## Limits and next steps

- The fixture and index are temporary local artifacts, not the corpus or a deployed search service.
- The exact lookup uses the legal engine's section syntax; it does not establish native scripture reference parsing.
- One result does not establish Sanskrit normalization, script variants, multilingual search, ranking quality, or performance at corpus scale.
- Source extraction and formatting were checked automatically; no scholarly review is claimed.
- Build and evaluate scripture-specific passage preparation, citations, and search against representative texts as called for in the [search checklist](../scripture-search/checklist.json).

## Ten-passage preparation follow-up

On 2026-11-27, the first ten consecutive source-numbered paragraphs were copied into a temporary JSONL fixture and indexed separately. Exact lookups using Legal-AI section syntax for numbers 3 and 8 returned the corresponding unaltered text, source URL, locator, and source-file hash. The verse 3 result retained its source page marker. The JSONL SHA-256 was `18a90a915eda1f4fb83fa209e5f976e0029a5e05fe7c820076bd1a3f815da3d4`.

A simple scan found 149 numbered markers but only 101 distinct marker values in the full Markdown. These counts may include non-verse numbers or editorial material; do not apply the pilot paragraph parser to the entire text or infer unique verse identifiers without further analysis. This fixture demonstrates preparation of ten passages, not completion of the pilot dataset or evaluation.

## Full text paragraph pilot

On 2026-11-27, the source text from its opening through its final paragraph was split on blank lines into 155 temporary, source-identical paragraph records, indexed with unique sequential IDs and a source hash. Of these, 149 end with a detected double-bar numeric marker. The source itself restarts its displayed numbering at 4 after 103; another paragraph ends with a single bar. Source numbers therefore remain descriptive labels and are not used as unique or canonical verse IDs. Keyword searches recovered a paragraph after the numbering restart and a paragraph near the end, with their original text and source links.

The paragraph fixture is a working pilot, not a verified verse map. Native-to-canonical verse alignment, robust handling of unnumbered and irregular paragraphs, broader retrieval evaluation and persistent pilot artifacts remain open. JSONL SHA-256: `443037a7c7c8e8125d9d8d852de5a8465347bc880ba4b7d537bce59f216d2b8d`.
