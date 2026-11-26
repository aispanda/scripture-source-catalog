# SCR-02 · Find and verify scripture passages

**Owner** · Pending confirmation · [Checklist](checklist.json) · [Guide](https://github.com/aispanda/Reusable-Delivery/blob/45a5e6653f202e37f181dce8c14e6bc0d34278b7/migrate/DELIVERY.md)

**Outcome** · As a scripture researcher, I want to find the intended passage and relevant commentary by citation, wording or meaning so that I can verify the source and understand its context.

**Scope** · A local search MVP for a classical Hindu pilot, starting with the Vijñāna Bhairava and its available editions and commentary. Preserve a path to Vedas, Upanishads, Tantras, Agamas, other Hindu and Buddhist sources, and works of spiritual masters. Broader corpus coverage and generated answers are later increments. The [SCR-01 source catalogue](../story.md) tracks acquisition, provenance and rights.

**Operations** · Ingest source Markdown into reproducible passage records. Accept a reference, quotation or question. Return ranked passages with original wording, edition and locator, surrounding context, and attributed commentary where a reviewed alignment exists. Report when the available corpus does not supply a confident match.

**Acceptance** · Pending human decision. The scenarios are proposed and all are NOT RUN.

## Requirements and verification

[Acceptance scenarios](scenarios.json) · [Consolidated MVP plan](mvp-plan.md)

## Execution record

NEW linked scope under the mixed-work rule in `migrate/DELIVERY.md` at `45a5e6653f202e37f181dce8c14e6bc0d34278b7`. SCR-01 links to this story and retains its catalogue criteria. The implementation repository, human owner, agent roster and assignments are pending. GPT-6.2 Sol is the requested model for Codex build and independent task verification. Formal acceptance uses a fresh Gemini Neon session in the standalone Google Antigravity App. Its results, human acceptance and ClickUp synchronization are pending. A separate Codex verifier checks each build task C-01 through C-05 against its task acceptance criteria and records evidence in that task before it can pass. Revisit LangGraph applicability after manual validation and before automating repeatable steps.

**Next** · Reconcile the initial corpus inventory in SCR-01, beginning with publisher and canonical title lists. Then map verified Markdown editions into the existing Legal-AI import format and verify scripture-specific citations.
