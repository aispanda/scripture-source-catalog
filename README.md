# Scripture source catalogue

[SCR-01](story.md) tracks scripture works, editions, translations, commentaries and their source evidence. [SCR-02](scripture-search/story.md) tracks Markdown ingestion and a local passage-search pilot using the existing Legal-AI importer and Tantivy baseline. [Legal-AI architecture and JSONL contract](https://github.com/aispanda/Legal-AI/blob/main/docs/architecture.md#build-from-another-corpus)

The catalogue comes first. Reconcile each priority publisher or canonical list at the title, edition and volume level and record unresolved gaps. Then ingest source-backed editions into a Markdown-only corpus. The catalogue records provenance, permissions, checksums and review status alongside the text. [Planning register](source-plan.json) · [Coverage review](inventory-review.md)

The register contains 1,743 source items. The Muktabodha local batch produced 560 Markdown drafts from 569 archive members and recorded nine failures. The private Cloud Storage bucket exists and corpus upload remains pending. [SCR-02 execution record](scripture-search/story.md#execution-record)

## Repository map

The [artifact map](docs/scripture-artifact-map.md) explains the source plan, parser registry, book index, metadata-span experiment, dependencies and outstanding work. The book index is a historical snapshot, not a live bucket inventory.
