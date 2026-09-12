# LazzyBee learning database: verified snapshot and integration decision

> **Scope clarification:** this audit and its machine-readable evidence apply only to the earlier 3,885-record learning snapshot. The owner has separately supplied the full 42,497-record server export; see [current server-dictionary status](SERVER_DICTIONARY_STATUS.md) for its evidence and unresolved overall-verifier gate. The counts and WordNet/cue results below are not full-export results.

## Status and scope

This is an **actual-data audit** of the owner-supplied `english_optimized.db`, not a synthetic fixture. Read-only analysis was performed locally. The original database and record-level outputs are not published.

- Snapshot SHA-256: `1a9a3c9c70d2ea6b56f8ab6c06e3302284f56a186c2bed5591a187d98f3d4473`.
- File size: **14,919,680 bytes**.
- SQLite `PRAGMA quick_check`: **ok**.
- Verified inventory: **3,885 vocabulary rows**, not 44,000.
- The owner's approximately 44,000-item full-library statement remains unverified by this file. Whether this snapshot is a starter pack, optimized subset, or another export scope is not established.
- **3,885 is a source-record/headword count, not a reviewed lemma-POS or sense count, calibrated item bank, or estimate of any person's vocabulary.**

Machine-readable evidence: [snapshot-audit.json](snapshot-audit.json). Reproduction tools: [../../tools/lazzybee/README.md](../../tools/lazzybee/README.md).

## 1. Actual schema and structural quality

The database contains the application tables `system`, `vocabulary`, `packageinfo`, and `packagestatus`, plus SQLite's internal sequence table. Counts are respectively 4, 3,885, 0, and 0 for the application tables. System values were not read/exported.

The vocabulary schema has these columns:

```text
id, question, answers, related, queue, level, due, rev_count,
user_note, last_ivl, e_factor, l_vn, l_en, priority, meaning,
package, packages, illustration
```

Structural checks:

- Nonempty text headwords: **3,885**.
- Unique headwords after NFC + case folding + whitespace normalization: **3,885**.
- Duplicate normalized headword rows, duplicate IDs, null IDs, blank/nontext headwords: **0** in each check.
- `answers` and `meaning`: **3,885 JSON objects each**, with no missing or invalid JSON in these fields.
- Every `answers` object has nonempty string fields `explain`, `example`, and `pronounce`.
- Every `meaning` object has nonempty `vn` text.
- `l_en` and `l_vn` are nonempty in all rows, including after the text-presence heuristic strips HTML tags.
- `related`, `package`, `packages`, and `illustration` are empty in this snapshot. Their absence does not prove the backend lacks packages or images.

These findings establish structural availability, **not** semantic correctness, pronunciation accuracy, copyright clearance, or psychometric quality. No learning-progress values, notes, or account data were used to infer learner ability.

### Stored source levels

| Stored level | Rows |
|---|---:|
| 1 | 647 |
| 2 | 571 |
| 3 | 609 |
| 4 | 613 |
| 5 | 600 |
| 6 | 589 |
| 7 | 256 |
| **Total** | **3,885** |

The meaning/provenance of these levels is not yet established. They must not be renamed CEFR levels, frequency bands, or calibrated difficulty parameters. They can inform exploratory blocked analyses, with that limitation explicitly stated.

## 2. Real WordNet comparison

Pinned resource: [Open English WordNet 2025, core XML release](https://github.com/globalwordnet/english-wordnet/releases/download/2025-edition/english-wordnet-2025.xml.gz).

- Resource SHA-256: `9ca6d1dcb75f822fdd66617f7d9da48142ace38dd544d6ad5e2feca1674ad3fe`.
- Indexed lemma-to-sense links: **185,129**.
- Indexed lexical entries with sense links: **135,969**; distinct exact lemma spellings in that index: **128,009**.
- These are counts of this pinned resource/index, not interchangeable with a live website's headline counts or a vocabulary-size scale.

### Matching method

Exact spelling first, then NFC/case/whitespace normalization if exact matching fails. The source has no explicit top-level POS column, so this run did **not** filter matches by inferred HTML POS. No stemming, morphological exception resolution, fuzzy matching, WordNet Plus augmentation, or automatic sense disambiguation was applied.

| Result | Source rows |
|---|---:|
| Exact headword candidates | 3,846 |
| Normalized-only headword candidates | 2 |
| No candidate in this run | 37 |
| **Rows with any candidate** | **3,848 / 3,885 (99.0476%)** |

Candidate ambiguity, counting sense links per source row:

| Candidate set | Source rows |
|---|---:|
| One candidate | 548 |
| Multiple candidates | 3,300 |
| No candidate | 37 |
| **Total** | **3,885** |

**99.0476% is lexical candidate coverage, not semantic agreement.** All 3,885 rows retain pending sense review, including the 548 with one candidate. No sense was automatically approved. The 37 unmatched rows are retained, not treated as invalid English; local inspection suggests function-word, morphological, and other normalization cases, but no per-record diagnosis has been approved.

Record-level candidates and an editable review queue were generated privately. Their row count and mapping checksum were verified. They are not in this public repository.

## 3. POS and CEFR clues in existing HTML

A deliberately limited extractor recognizes whitelisted Vietnamese grammatical labels in `l_vn` `span.tl`/`strong` elements:

- **2,186 rows** have one recognized POS hint.
- **1,548 rows** have multiple recognized POS hints.
- **151 rows** have no recognized hint under this extractor.

These are dictionary-wide hints, not reviewed POS assignments for `answers.explain`. They may describe different senses, phrases or dictionary sections. A missing hint does not establish that the source lacks grammatical information.

`l_en` contains `epp-xref` CEFR class markers in **2,768 rows**. Per-label row counts are A1=61, A2=314, B1=839, B2=1,172, C1=674, C2=802. Counts overlap because a row can describe multiple senses/phrases. This is neither a source-level-to-CEFR conversion nor a validated assessment calibration. Markup styles alone do not establish the original source or rights to republish its content.

## 4. Critical authoring constraint: target words inside explanations

An exact-headword, case-insensitive, Unicode-boundary text check after stripping HTML tags found:

- **3,798 explanations (97.7606%)** mention their own target headword.
- **2,836 examples (72.9987%)** mention their own target headword.

This is normal in learning content. It becomes an answer cue if the text is reused unchanged in a definition-to-word assessment. These counts are a targeted heuristic, not a complete leakage audit: inflected forms, images, morphology and semantic cues require additional checks.

**Do not automatically promote these fields into scored questions.** Introduce a separate `ItemVersion` authoring layer. Depending on the chosen format, rewrite definitions, deliberately blank the appropriate span, or use independently reviewed options. A blind global string replacement is not sufficient: it can remove legitimate context or leave other answer cues. A word-to-meaning format intentionally presents the target word and has different cue controls.

## 5. Revised solution using this database

### Preserve the source and separate identity layers

Keep a private immutable source snapshot and stable source-ID crosswalk. Do not modify the production dictionary. Separate:

1. Source headword record.
2. Reviewed lemma-POS plus target sense.
3. Reviewed question version.
4. Frozen frame/bank release.
5. Learner response and scoring release.

The snapshot is now sufficient to start actual content audit, normalization and authoring. It does not establish an already reviewed 3,885-unit lexical frame. Multiple POS/senses may expand or consolidate units, subject to the chosen counting policy.

### Practical implementation sequence

1. **Inventory — completed:** read-only SQLite/JSON/profile checks, pinned WordNet candidate mapping, source/hash lineage and private review queue.
2. **Sense/POS review — pending:** adjudicate ambiguous mappings, inspect the unmatched queue, define target sense, preserve exceptions and establish stable unit identity.
3. **Item authoring — pending:** remove unintended target cues for the selected format, review language burden and distractors, record rights and content-review decisions.
4. **Pilot frame — pending:** freeze a reviewed inventory with one assessable unit policy. If only a subset has usable items, limit the pilot estimand to that frame. Do not multiply a convenience-bank score up to 3,885, 20,000 or 44,000.
5. **Assessment integration — pending:** server-side answer authority, immutable release IDs, frozen stage-2 quotas, idempotency, missingness semantics, accessibility and protected item delivery.
6. **Psychometric validation — pending:** simulation under the selected bank design, human feasibility study, calibration/holdout, test–retest and subgroup checks before public vocabulary-count claims.

The bundled residual-HT reference is appropriate only under its stated sampling/response assumptions. Its output is a finite-frame correct-response total, not a latent count of known words. The conservative interval may be too wide for a short test; UX targets must be evaluated rather than promised.

### Meaning of completion

The data-onboarding and reference-tool stages are complete for **this snapshot**. Production assessment, semantic adjudication, item-bank readiness, human calibration and the scope of the approximately 44,000-item full library remain open.

## 6. Data protection and rights

- No `.db`, full headword inventory, definitions/examples, per-record candidates, review CSV, system values or user-progress values are published here.
- Public artifacts contain source identifiers/checksums, schema names, aggregated counts, authored tools and synthetic tests only.
- Open English WordNet attribution terms and the rights to LazzyBee's existing dictionary content are separate questions. Availability in an app/database is not evidence of redistribution rights.
- Read-only source hash was rechecked after processing. No production endpoint was contacted.

## 7. Reproduction

Use a consistent private SQLite backup. The commands print aggregate JSON; the record-level mapping output must remain private.

```bash
python3 tools/lazzybee/vocabtool.py audit --db /private/english_optimized.db
python3 tools/lazzybee/profile_snapshot.py /private/english_optimized.db
python3 tools/lazzybee/vocabtool.py index --xml /private/english-wordnet-2025.xml.gz --out /private/wordnet.sqlite
python3 tools/lazzybee/vocabtool.py map --db /private/english_optimized.db --index /private/wordnet.sqlite --out /private/candidates.jsonl
python3 -m unittest discover -s tools/lazzybee/tests -v
```

The WordNet parser is intended for a trusted pinned resource. Exact checksum equality, completed-output metadata and row-count checks are required before accepting generated mapping artifacts. Software tests use synthetic fixtures; actual-data statistics are separately recorded in the evidence JSON.
