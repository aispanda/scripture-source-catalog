# Scripture parser profiles implementation plan

**Goal:** Prepare source-traceable parser profiles and a repeatable improvement loop.

**Design:** Apply source-specific parsing, preserve byte offsets and native markers, and keep uncertain or unsupported formats out of unattended indexing. See `scripture-catalog-ingestion-and-rag-design.md` sections 6.4, 9.5 and 12.1.

1. Registry: retain the existing profile and list proposed profiles with version, applicability, status, evidence, tests and failure behavior. Validate unique IDs and status.
2. Muktabodha pilot: recognize only an unambiguous publisher header bounded by separator lines inside one Markdown fence; preserve the remaining paragraphs and raw byte offsets, retaining unnumbered text and repeated markers. Fail on missing/ambiguous boundaries.
3. Validate synthetic and actual M00271 data: compare source byte slices and the existing 155-paragraph fixture, report deviations and do not claim canonical verse mapping.
4. Route experiments: Jev suggests among eligible profiles or an unknown option; deterministic checks and measured outcomes govern use. Record model, evidence and unresolved cases. Gemini proposes a new profile when existing profiles fail; never silently mark it verified.
5. Repeat on independent representative root, commentary, Vedic and Tamil examples. Promote only after relevant boundary and source-location checks pass. Record gaps and results.
