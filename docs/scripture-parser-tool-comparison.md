# Scripture parsing tools: exploratory comparison

Date: 2026-11-27

## Test and limits

Compare tools on the same locally available Muktabodha M00271 Markdown and its existing 155-paragraph pilot fixture. Assess passage boundaries, original text preservation, source positions and repeated markers. This is a single-document exploratory test, not the frozen evaluation set or a broad quality benchmark. The fixture identifies the source body in advance.

## Results

| Tool | Result | Practical implication |
|---|---|---|
| Lark 1.3.1 | A small grammar identified all 155 paragraphs and their source marker numbers, including both printed 4 markers and an irregular 52. All 155 UTF-8 spans round-trip to the source; 154 of 155 boundaries match the fixture exactly. One span includes an extra leading space. | Promising for configurable parsing, but that boundary mismatch and header classification need correction. This does not establish performance on unseen works, commentaries or Tamil. The fixture supplied the body boundaries. |
| Docling 2.154.0 | The Markdown conversion succeeded. All 155 fixture passages appeared in one Docling code-block item, but were not emitted as 155 passage records. The code item had no per-passage provenance entries. | On this sample, another scripture-specific parser is needed inside the fenced block. This does not evaluate Docling on PDFs, scans, or OCR. |
| Google Document AI layout parser | Not run. No layout processor was found in the checked US/EU locations. Google’s documented layout-parser input formats do not list Markdown. | Evaluate separately on an original PDF/scan with suitable processor access; conversion would change the test and needs its own provenance. [Supported processors and formats](https://docs.cloud.google.com/document-ai/docs/processors-list). |

No quality ranking or adoption decision is justified by these results alone. The Lark test code and Docling outputs were generated in temporary local directories; they are not yet a committed production pipeline. Re-run comparisons on representative texts, including Tamil, commentary and numbered/unnumbered structures, using independent source-grounded references. Document AI testing should use an appropriate source format and record any applicable costs.

See the [technology evaluation plan](scripture-technology-evaluation-plan.md) and [importer pilot](scripture-importer-pilot-test.md).
