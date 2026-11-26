# Scripture inventory review

Claude Opus 5.5, high effort. Reviewed public source counts and the proposed inventory contract. Suggested gaps require source verification.

**1) Missing works / list families**

*High*
- Itihāsa critical editions: Mahābhārata (BORI), Vālmīki Rāmāyaṇa (Baroda), Harivaṃśa
- Prasthānatraya: Brahmasūtra with sectarian bhāṣyas (Śaṅkara, Rāmānuja, Madhva, Nimbārka, Vallabha)
- Kalpasūtras (Śrauta/Gṛhya/Dharma) and Vedāṅga, linked to IGNCA recensions
- Darśana root texts: Yoga, Nyāya, Vaiśeṣika, Mīmāṃsā sūtras; Sāṃkhyakārikā
- Dharmaśāstra: Manu, Yājñavalkya, Nārada smṛtis
- Āgama lists: 28 Śaiva Siddhānta Āgamas, Pāñcarātra Saṃhitā lists (*candidate*), Vaikhānasa
- Buddhist canon catalogues: Tibetan Kangyur/Tengyur (Tōhoku numbering), Chinese Taishō (CBETA), Pali Chaṭṭha Saṅgāyana incl. aṭṭhakathā/ṭīkā, Digital Sanskrit Buddhist Canon
- Tamil: Tirumurai (12), Nālāyira Divya Prabandham, Meykaṇṭa 14 Śāstras, Tirukkuṟaḷ

*Medium*
- Upapurāṇa lists, tracked as variants
- Śākta/Kaula tantras (*candidate*)
- Regional bhakti: Jñāneśvarī, Rāmcaritmānas, Vīraśaiva vacanas (*candidate*, scope-dependent)

*Named bibliographies for reconciliation*
- New Catalogus Catalogorum
- Potter, *Encyclopedia of Indian Philosophies* bibliography
- Kane, *History of Dharmaśāstra*
- Lancaster, Korean Buddhist Canon
- PTS editions list

**2) Column changes**

*Add*
- `source_native_id`
- `inventory_snapshot_date` and `inventory_snapshot_hash`
- `base_print_edition`: editor, publisher, year, series, volume
- `etext_derivation`
- `source_file_checksum` and `markdown_checksum`
- `markdown_verified_by` and `markdown_verified_date`
- `rights_statement_verbatim`, `rights_source_pointer` and `rights_checked_date`
- `external_ref_scheme` and `external_ref_id`, as a join table (Taishō, Tōhoku, PTS, NCC)
- `list_membership`: list family, variant and position, as a join table
- `equivalence_status` (unreviewed / asserted) plus `equivalence_evidence`

*Replace*
- `language` → `original_language` + `edition_language`
- `title` → `title_original_script` + `title_iast` + `title_search_normalized`
- Any "complete" boolean → `coverage_status` enum + `evidence_pointer`

*Separate*
- Work, edition and file levels

**3) Evidence before claiming an inventory complete**

*Universal standard:* source-declared count, retrieved count, matched count, enumerated gaps with reasons, and a dated snapshot.

- **GRETIL legacy:** per-row file existence and hashes; deduplication rule across languages; explanation of the 1,125 vs 843 counts.
- **GRETIL OPAC:** full paginated export of 405 records, or documented export limit. Record-level links to legacy rows must come from explicit evidence, not title matching.
- **Muktabodha:** identify the 2 missing-file IDs and their status (withheld, renamed, or error); item-level usage terms.
- **IFP / Gokarna:** full item export; per-collection counts; manuscript vs transcript distinction.
- **IGNCA:** per-recension listing with page pointers.
- **Sanskrit Documents, SARIT, Project Madurai, SuttaCentral:** repository commit or listing snapshot; counts; SuttaCentral root texts separated from translations.
- **Internet Archive:** query string, date and identifiers. Label as "sampled", never complete.
- **Collected works (20 persons):** publisher bibliography per person; item-level reconciliation; missing volumes listed.
- **Reference lists (Muktika, Mahāpurāṇa):** cite the list's source edition; every item mapped or marked as a gap.

## Verification after review

The apparent two missing Muktabodha files were a parsing issue. The catalogue IDs M00002a and M00002b are both in the ZIP. All 569 downloaded metadata IDs now match archive members. This establishes file presence and does not assess conversion or textual fidelity.
