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
