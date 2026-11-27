# Scripture parser profiles: pilot quickstart

The registry at `scripture-search/parser-registry.json` records implemented and proposed profiles. `muktabodha-header-paragraph` is experimental: it extracts paragraphs after an identifiable publisher header, not verified verses. Unknown formats, missing header delimiters, multiple fences and mismatched publisher IDs are rejected. The original Markdown stays unchanged.

Run the tests with `cd scripture-search && python3 -m unittest discover -v`.

Example, using an existing local Markdown file and a new output path outside the source folder:

```sh
python3 scripture-search/passage_parser.py /path/to/M00271.md \
  --profile muktabodha-header-paragraph --edition-id muktabodha-m00271 \
  --title 'Vijñānabhairava' \
  --source-url https://muktabodha-digital-library.org/texts/IAST/M00271 \
  --output /tmp/m00271-passages.jsonl
```

Each passage stores the source text, half-open UTF-8 byte offsets, SHA-256, ID, original marker and parser version. The program refuses to overwrite an existing output. Verify `raw[byte_start:byte_end].decode('utf-8') == text` for every passage. The profile preserves unnumbered paragraphs and flags repeated source markers, without inventing canonical numbering. It does not classify root versus commentary, detect every malformed marker, or prove scholarly verse boundaries.

## Pilot evidence and next loop

- M00271: 155 paragraphs matched all 155 byte boundaries in the existing paragraph-review fixture; all source slices round-tripped. This is a single-edition comparison, not an independent corpus-wide benchmark. A public experimental output is `scripture-search/examples/m00271-paragraphs.experimental.json`. The publisher's text header identifies the e-text as Creative Commons BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/ . Source: https://muktabodha-digital-library.org/texts/IAST/M00271 .
- Three bounded Jev 1.14.0 calls using opening/middle excerpts returned `numbered_scripture` for M00271, `root_and_commentary` for M00347, and `tamil_lines` for pmuni0078. These were suggestions consistent with the sample descriptions, not a calibrated accuracy estimate or proof that any particular parser works. The manual probe is `scripture-search/jev-profile-probe.py`; it reads a key from a supplied local environment file, sends excerpts to TypeSafe, and does not select a parser or modify the corpus.
- For a new input, use structure and source information to propose an applicable profile. Test its output against source spans and representative expected boundaries. Log failures or uncertainty; ask Gemini for a bounded proposal using relevant excerpts, then implement and test the new profile before changing its registry status. Jev may suggest categories but cannot confirm accuracy. Formal Lark grammars and meter tools remain options to evaluate when they add measurable value.

Design references: [ingestion and retrieval design](scripture-catalog-ingestion-and-rag-design.md), [technology evaluation plan](scripture-technology-evaluation-plan.md), and the [Sanskrit research notebook](https://notebook.google.com/notebook/5f5b1ec3-96f2-499e-abd7-285eee5ea55a). The latter's recommendations and model suggestions are hypotheses until checked on the target texts.
