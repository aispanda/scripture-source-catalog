# Scripture technology evaluation plan

| Item | Value |
|---|---|
| Status | Proposed plan. Nothing here has been measured. |
| Date | 2026-11-27 |
| Reviewed against | `main` at `7bbee46` |
| Related | [Ingestion and retrieval design](scripture-catalog-ingestion-and-rag-design.md) sections 12 and 13; [edition reconciliation design](scripture-edition-reconciliation-design.md) sections 6 and 10 |
| Checklists | [SCR-01](../checklist.json) and [SCR-02](../scripture-search/checklist.json) |

Every technology evaluation states three things: what is tested, the success criterion, and the decision that follows. **Requirements** come from the story scenarios and must pass. **Candidates** are techniques that may help meet a requirement and are adopted only if they pass. No numeric threshold is set here. Targets, margins and latency budgets are frozen in SCR-02 C-02 before any run. Owner criteria for catalogue fields are recorded before their run.

## 1. Protocol for every run

1. Use the fixtures frozen in SCR-02 C-02. Keep the tuning and held out sets separate, and record the held out checksum.
2. Record the configuration revision, the Markdown and passage set versions, and every model ID and version.
3. Tune only on the tuning set. A retuned variant needs a fresh held out set (SCR-02 C-04 guardrail).
4. Write results to a file outside the corpus and link it from the task's `evidence` field.
5. Before any hosted call, check the recorded source terms by hand.

## 2. Retrieval requirements

| ID | Scenario | What is tested | Success criterion | Decision that follows | Task |
|---|---|---|---|---|---|
| R1 | SCR-02 A-01 | Queries naming a work alias, a locator and an edition, including passages whose source marker repeats | Each fixture returns the intended passage in the requested edition with its locator; other editions are labelled separately; a repeated marker returns every match and states the ambiguity | Pass: the exact route is used in C-05. Fail: fix the locator mapping or alias table before C-04 | SCR-02 C-03 |
| R2 | SCR-02 A-02 | Reviewed Devanāgarī, IAST and plain Latin forms of the same passages | Each form retrieves the expected passage, and display text is unchanged | Adopt the simplest candidate from T1 or T2 that passes; record failing forms as gaps | SCR-02 C-03 |
| R3 | SCR-02 A-03 | Held out meaning queries that do not copy the passage wording | Recall@k meets the target frozen in C-02, and the intended passages are cited | The route chosen in R6 serves meaning queries. If none meets the target, A-03 is reported as failed | SCR-02 C-04 |
| R4 | SCR-02 A-04 | A fixture with a reviewed commentary alignment and neighbouring passages | The result separates source text, context, commentary author and edition, and alignment evidence | Commentary links appear only for reviewed alignments | SCR-02 C-05 |
| R5 | SCR-02 A-05 | Absent references and questions outside corpus coverage | Every fixture reports insufficient evidence and gives no citation | The abstention rule is frozen with the build; any fabricated citation blocks release | SCR-02 C-05 |
| R6 | SCR-02 A-06 | Lexical, semantic, translation assisted and hybrid variants on identical held out inputs | The decision record reports quality and latency by query class. Hybrid qualifies only if it beats the best variant that is not hybrid by the agreed margin within the latency budget | Select the simplest variant that meets the criteria, and record its configuration revision and held out checksum | SCR-02 C-04 |

## 3. Retrieval candidates

| ID | Candidate | What is tested | Success criterion | Decision that follows | Task |
|---|---|---|---|---|---|
| T1 | Script normalization across Devanāgarī, IAST and plain Latin, as a derived index field | R2 fixtures, plus R1 fixtures to check for regressions | R2 passes, and no R1 exact hit is lost | Adopt as a derived field, with display unchanged; otherwise drop | SCR-02 C-03 |
| T2 | Diacritic folding and character level matching | Spelling variant queries on the tuning set, then the held out set | Gain on held out wording queries, and no R1 exact hit is lost | Adopt or drop; can combine with T1 | SCR-02 C-03 |
| T3 | Sandhi segmentation and lemma indexing, for example ByT5 Sanskrit, run locally | Wording queries with compounds and inflected forms | Gain over the T1 and T2 baseline by the margin frozen in C-02, with no R1 loss | Adopt as an extra derived field, or defer | SCR-02 C-04 |
| T4 | Multilingual dense embeddings, for example MITRA (trained on Buddhist material, untested on Hindu texts) | Meaning queries in English and Sanskrit | Contributes to meeting R3 | Enters the R6 comparison; otherwise dropped | SCR-02 C-04 |
| T5 | Translation assisted search over aligned translations, where they exist | English queries on works that have translations | Gain for those queries in R6 | Enters R6 only for works with aligned translations | SCR-02 C-04 |
| T6 | Hybrid fusion, for example reciprocal rank fusion | Combined routes in R6 | The R6 hybrid rule | Adopt only under R6 | SCR-02 C-04 |
| T7 | Reranking of the selected route | The same held out inputs, measured separately | Gain by the frozen margin within the latency budget | Add the reranker or leave it out | SCR-02 C-04 |
| T8 | Query class routing into reference, wording and meaning routes (design section 12.3) | Routing outcome against the best single route, by query class | No loss on any query class against the best single route | Use routing, or use one pipeline | SCR-02 C-04 |
| T9 | Knowledge graph of works, editions and commentary | Not tested in the MVP; no current scenario requires it | A defined query class and a measured benefit | Plan a test only when a scenario needs it | none |

## 4. Catalogue and reconciliation evaluations

| ID | Kind | What is tested | Success criterion | Decision that follows | Task |
|---|---|---|---|---|---|
| M1 | Requirement before unattended use | Clear evidence rules (reconciliation design section 6.3) on reviewed pairs | No wrong confirmation; the share left ambiguous is reported | The rule may run unattended; otherwise it proposes only | SCR-01 C-18 |
| M2 | Requirement | Assembly checks (reconciliation design section 7.4) on each assembled edition | Part bytes are identical, order and gaps are correct, and the hash is reproducible | The assembled file becomes eligible for upload and indexing | SCR-01 C-19 |
| M3 | Candidate | Jev facet suggestions against independently reviewed examples, per field | Meets the owner's criterion for that field, recorded before the run | For each field: automatic adoption, suggestions only, or drop | SCR-01 C-17, C-16 |
| M4 | Candidate | Local model, Jev or Bhashini suggestions for ambiguous reconciliation pairs | The owner finds the suggestions useful on reviewed pairs, with every wrong suggestion recorded | Keep as a reviewer aid or drop; never a confirmation | SCR-01 C-18 |

## 5. Checklist links

Each checklist task links here through its existing `docs` field, which already holds space separated links. No new field is added, so the pinned checklist schema is unchanged. Results go in the task's `evidence` field.
