# Scripture catalogue and parser artifacts

## Three primary records

| File | Responsibility | Current state |
| --- | --- | --- |
| [source-plan.json](../source-plan.json) | Source inventories, works, catalogue item IDs, titles, source links and descriptive metadata. | Maintained catalogue; not a live cloud inventory. |
| [parser-registry.json](../scripture-search/parser-registry.json) | Parser profile names, versions, supported formats, limitations and evidence. | Existing experimental and proposed profiles. |
| [book-index.json](../scripture-search/book-index.json) | One row per catalogue ID; recorded Markdown path, hash, historical cloud observation, edition decision and parser assignment when known. | Imported historical snapshot, not a live inventory or proof of selected editions. |

`source-plan.json` owns titles and source descriptions. `book-index.json` references its IDs rather than duplicating those descriptions. `${SPIRITUALITY_WORKSPACE}` is a placeholder for the local workspace root, not a GitHub path. Never assume a recorded local or cloud path is currently accessible; recheck source hashes and cloud generations. An `unknown` edition status is not a primary selection.

## Parsing and search dependencies

| File | Purpose |
| --- | --- |
| [passage_parser.py](../scripture-search/passage_parser.py) and its existing tests | Existing parser implementation; experimental profiles must be validated before relying on their boundaries. |
| [metadata-regions.experimental.jsonl](../scripture-search/data/metadata-regions.experimental.jsonl) | Per-file hashes and candidate publisher-header byte ranges, generated from 1,565 local Markdown files. No source text is embedded. |
| [metadata_regions.py](../scripture-search/tools/metadata_regions.py) and [tests](../scripture-search/tools/test_metadata_regions.py) | Reproduce the metadata span experiment for a supplied corpus. This identifies only explicit delimiters, not every kind of metadata. |
| [experiments](../scripture-search/experiments/) | Experimental GRETIL profile code, book settings parser and candidate reference detector with synthetic tests. These are not production-approved boundaries. |
| [book-index-import-report.json](../scripture-search/migration/book-index-import-report.json) | Records the inputs and counts for the one-time processing snapshot import. |
| [parser design](parser-profile-implementation-plan.md), [quickstart](parser-profiles-quickstart.md) and [evaluation plan](scripture-technology-evaluation-plan.md) | Explain the existing proposed implementation and tests. |

To regenerate metadata spans without altering the Markdown, run `python3 scripture-search/tools/metadata_regions.py --corpus <markdown-directory> --output <new-output.jsonl>`. The output path must not already exist. Before using a recorded span, verify the Markdown SHA-256. `no_recognized_header` means the format was not recognized, not that the file contains no metadata. The 1,316 classified files are an experimental count, not a corpus-wide accuracy measurement.

The source plan refers to external source URLs. The book index points to local Markdown, cloud objects and, where recorded, commit-pinned GitHub Markdown under [corpus](../corpus/). The initial GitHub corpus contains nine selected entries; other rows have no GitHub link until published. Parser registry evidence links point to the design and tests. Full passage data, metadata classifications, exact reference lookup and a reproducible search index require their corresponding inputs and versions. A local index is generated from selected passages; it is not a replacement for the source or the catalogue. The existing Legal-AI importer must be versioned with each future index build.

## Missing or unfinished

* An up-to-date reconciliation of the historical book index with the live local corpus and cloud bucket, including edition selections and holds.
* Link four locally observed DLS Markdown files to catalogue IDs; they are present in the metadata-span experiment but not linked by the imported catalogue snapshot.
* Versioned per-book parser configurations linked to registered, tested parser profiles, and reproducible passage manifests and test evidence.
* Part-specific source attribution for multipart files; the current local search experiment excludes six such entries.
* A full-corpus index manifest, exact-passage navigation and representative retrieval tests. The local three-book experiment is not a deployed MVP.

Large generated batches and binary indexes are kept outside Git; a future published artifact needs a durable location, checksums, tool versions and a reproducible manifest. Existing experimental batches have not been deleted. The 186 MiB reference inventory and 225 MiB alignment file exceed GitHub's ordinary per-file limit and are not included in this repository. Keep original Markdown unchanged; classifications are separate observations.
