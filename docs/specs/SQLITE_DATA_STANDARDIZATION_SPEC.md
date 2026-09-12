# SQLite Data Standardization Specification

**Document ID:** DATA-SQLITE-01  
**Version:** 1.0.0  
**Status:** implementation-ready design; migration deferred by owner; NOT a completed migration or data-release approval.  
**Scope:** private, offline LazzyBee dictionary import, fidelity, normalization, lookup and handoff to later measurement work.  
**Executable schema contract:** [sqlite_standardization_v1.sql](sqlite_standardization_v1.sql).

## 1. Decision and non-goals

Preserve both received files unchanged. Build a separately versioned, private SQLite artifact with two layers: source-record fidelity and normalized lookup. Never standardize in place, replace the server database, silently deduplicate records, or infer measurement units from row counts.

The JSON is the original export representation; the received SQLite is its flattened conversion and a reconciliation input. Neither is edited by this design. If the two disagree, block promotion and request a source decision; do not silently select whichever value looks plausible.

The owner has paused subagents and requested specification now, implementation later. This document does not authorize a migration run, resumed cron, new subagents, production access, public dictionary upload or changes to application production code.

Out of scope: WordNet sense matching, Oxford provenance attribution, lemma/POS adjudication, item authoring, calibration, CAT, public API deployment and participant learning-progress migration. These require separate artifacts and approval. No optional enrichment may block basic data-fidelity delivery.

## 2. Evidence and the unresolved verification gate

### 2.1 Received artifacts

Private repository directory: `private-dictionary/`.

| Artifact | Role | Recorded SHA-256 |
|---|---|---|
| `dictionary_optimized_readable.json` | Original server-export representation | `7e8dded6820c34e44966797e24c294a18e209a4b20681cffa99137e2fb11e01f` |
| `dictionary.sqlite` | Received flattened conversion | `ed0e985d12b2e7bf1ea77dbeed0554d83ebcf3ccc58c783d3d04cbb0ac695bef` |

The owner confirms that these represent the full server dictionary. This is owner-confirmed provenance, not an independent production-server comparison. The expected **42,497** rows apply to this pinned export only, not every future dictionary release.

The audit worker reports full reconciliation. The parent's re-run of `audit_verify.py --verify` returned these aggregate results:

- JSON and SQLite: 42,497 records each; 42,497 matched stable IDs.
- Source-only and destination-only IDs: zero; mapped-field mismatches: zero.
- Surface and normalized headword counts reported by the verifier: 42,497 each.
- Synthetic tests: four core and two extended tests passed.
- **Overall verifier result: `verification_failed`, exit 2.** Aggregate success does not override this failure.

The worker additionally reported 27 mapped fields, 1,147,419 compared cells, valid SQLite integrity checks and protected byte-identical copies. Treat these as existing evidence to revalidate, not as authorization to bypass the failing overall gate.

**Open issue AUDIT-001:** determine the exact failed verifier condition. Do not assume the cause is volatile metadata. Diagnose it before standardization promotion. If it is a verifier defect, reproduce it with a regression test and fix narrowly. If it is a material data difference, block and resolve the source discrepancy. Do not delete checks, broadly ignore report subtrees or regenerate a report merely to make the comparison pass.

### 2.2 Distinct learning snapshot

The earlier `english_optimized.db` contains 3,885 records. The audit reports 3,884 normalized headwords shared with the server export, one learning-only headword, and 38,613 server-only headwords. Do not call the learning snapshot a strict subset. Keep the learning-only item in a private review queue; do not insert it into the server snapshot or drop it from the learning source automatically.

These are lexical overlaps under the audit's recorded normalization, not evidence of equivalent senses, definitions or learning state. This specification's normalization must be recomputed and versioned independently if its policy differs.

## 3. Artifact layout and security boundary

Proposed private layout, to be populated only during the later approved implementation:

```text
private-dictionary/
  dictionary_optimized_readable.json          # received source; unchanged
  dictionary.sqlite                          # received conversion; unchanged
  audit-summary.json                         # existing evidence, not overwritten silently
  audit_verify.py / audit_core.py             # existing verification tools
  standardized/
    builds/<build-id>/
      dictionary.standardized.v1.sqlite
      manifest.json
      validation.json
      overlap-summary.json
      private-review.jsonl
    staging/<unique-run-id>/                  # unpublished partial output
    current.json                             # atomic pointer to an approved build
```

- All data directories MUST be mode `700`; files MUST be mode `600` on this host.
- Verify exact output paths are Git-ignored and untracked **before** copying/building. Do not use force-add. The public `raw/` directory contains research documents, never raw dictionary data.
- Reject source/target path aliases, symlinks or resolved path escapes that could overwrite originals. Never follow an untrusted output path outside the allowed private root.
- No credentials, raw entries, headword inventories, definitions, audio URLs, stable-ID inventories or record-level mappings in public reports or stdout. Public documentation may contain schema, aggregate counts and synthetic examples only.
- Rich text and audio/link strings are untrusted data, not instructions. Retain fidelity in storage; sanitize HTML with an approved allowlist at rendering time. Do not evaluate markup, fetch URLs during import, or construct SQL from dictionary values.
- Dictionary-content licensing/provenance is distinct from consent and deletion rules for personal response data. Do not import user progress into this lexical artifact merely because legacy fields exist.

## 4. Baseline schema actually inspected

The received SQLite has table `dictionary` and these 27 columns:

```text
_id TEXT PRIMARY KEY
id INTEGER
question TEXT
answers_pronounce TEXT
answers_explain TEXT
answers_example TEXT
meaning_vn TEXT
related TEXT
queue INTEGER
level INTEGER
due INTEGER
rev_count INTEGER
user_note TEXT
last_ivl INTEGER
e_factor INTEGER
l_vn TEXT
l_en TEXT
l_en_lingoe_1 TEXT
l_vn_lingoe_1 TEXT
db_version INTEGER
updated_at TEXT
created_at TEXT
popularity INTEGER
new_level INTEGER
packages TEXT
en_order INTEGER
vn_order INTEGER
```

Inspected indexes: `idx_question(question)`, `idx_id(id)`, `idx_level(level)`.

SQLite declarations do not prove stored value types. The importer MUST check `typeof()` distributions and each bound value. `STRICT` tables alone are insufficient: SQLite can losslessly coerce a numeric string into an integer. Application validation must reject undeclared coercions before binding.

## 5. Target data model

The linked SQL is normative DDL for a **new** staging database. It is not an ALTER script for the received file. Use SQLite 3.37 or later with working JSON functions; verify the actual runtime supports STRICT tables, foreign keys and required JSON functions before writing.

### 5.1 Tables and cardinality

- `source_manifest`: exactly one pinned import manifest per output database; source hashes, expected source count, mapping/normalization/Unicode/builder versions and declared provenance.
- `source_record`: exactly one row per original JSON object, preserving `_id`, zero-based source ordinal, original object JSON and its UTF-8 SHA-256. Links to the manifest.
- `dictionary_entry`: exactly one row per source record; the 27 mapped fields plus normalized lookup key and optional parsed UTC timestamps/statuses. The stable `_id` is retained unchanged.
- `data_issue`: zero or more versioned issues per entry, or a global issue with NULL entry reference. Severity is `blocking`, `review` or `info`. No blocking issues are permitted in a promoted build.
- `v_dictionary_lookup`: read-only projection, with explicit `_raw` content names and legacy-level names. It is not a reviewed lexical-unit or item-bank view.

Foreign keys and unique keys enforce identity relationships. Cross-table completeness, expected counts, raw-value correspondence, timestamp derivation and digests are validated by the builder/verifier; DDL alone does not prove them.

### 5.2 Stable identity and collisions

- Identity is the source `_id`, compared exactly, including case and whitespace. Require a nonempty JSON string for v1. Do not normalize it, regenerate it from a word, or use numeric `id` as its replacement.
- Duplicate/missing/invalid stable IDs block the entire build. No last-write-wins behavior.
- `question` is preserved exactly; `question_key` is derived and is **not unique**. Multiple source entries that normalize to one key remain separate candidates. Record a collision issue and return all matching IDs.
- Source order is preserved by `source_ordinal`; query order is explicit, never inferred from physical SQLite row order.

### 5.3 Fidelity layer

`source_record.record_json` MUST preserve the original record object, including missing-versus-present-null fields, nested value types, list order and numeric precision. Prefer an exact UTF-8 object slice from the pinned source, excluding separators outside that object. If a serializer is used, prove semantic numeric/type preservation; parsing arbitrary numbers through binary float is not accepted as a generic lossless solution.

Detect duplicate keys at every JSON object level before accepting records. Do not rely on `json.loads` default last-key-wins behavior or on `json_valid()` to detect duplicate keys. Use a maintained parser with a tested duplicate-key policy; do not build an unnecessarily broad custom parsing framework.

The archived source file remains the byte-level authority. The row payload enables typed reconstruction without relying on flattened SQL NULL to distinguish missing fields. `record_sha256` is computed over the exact stored `record_json` UTF-8 bytes and checked by the verifier.

## 6. Complete field mapping

For direct fields, JSON root key maps to the same received SQLite and target column. Every non-null value must match the pinned conversion exactly under the declared type policy.

| JSON path | Received/target column | Type/policy |
|---|---|---|
| `_id` | `_id` | Exact nonempty string; primary identity |
| `id` | `id` | INTEGER or NULL; not identity |
| `question` | `question` | Nonempty TEXT; preserve exact original |
| `answers.pronounce` | `answers_pronounce` | TEXT or NULL; no IPA correction |
| `answers.explain` | `answers_explain` | TEXT or NULL; preserve HTML/text |
| `answers.example` | `answers_example` | TEXT or NULL; preserve HTML/text |
| `meaning.vn` | `meaning_vn` | TEXT or NULL |
| `related` | `related` | TEXT or NULL; this export reported all NULL |
| `queue` | `queue` | INTEGER or NULL; legacy operational field |
| `level` | `level` | INTEGER or NULL; unknown/calibration-independent scale |
| `due` | `due` | INTEGER or NULL; unit not inferred |
| `rev_count` | `rev_count` | INTEGER or NULL; legacy operational field |
| `user_note` | `user_note` | TEXT or NULL; this export reported all NULL |
| `last_ivl` | `last_ivl` | INTEGER or NULL; unit not inferred |
| `e_factor` | `e_factor` | INTEGER or NULL under current schema; no IRT interpretation |
| `l_vn` | `l_vn` | TEXT or NULL; preserve exact link/content string |
| `l_en` | `l_en` | TEXT or NULL; preserve exact link/content string |
| `l_en_lingoe_1` | `l_en_lingoe_1` | TEXT or NULL |
| `l_vn_lingoe_1` | `l_vn_lingoe_1` | TEXT or NULL |
| `db_version` | `db_version` | INTEGER or NULL; distinct from target schema version |
| `updated_at.$date` | `updated_at` | Extract TEXT unchanged; optional UTC derivation is separate |
| `created_at.$date` | `created_at` | Extract TEXT unchanged or NULL; retain source presence |
| `popularity` | `popularity` | INTEGER or NULL; not calibrated frequency/difficulty |
| `new_level` | `new_level` | INTEGER or NULL; retain separately from `level` |
| `packages` | `packages` | NULL, or JSON array string preserving semantic values/order |
| `en_order` | `en_order` | INTEGER or NULL; not corpus-frequency rank by assumption |
| `vn_order` | `vn_order` | INTEGER or NULL |

No undisclosed source roots, nested keys or destination columns may be dropped. The importer compares the actual field inventory with this mapping. Unexpected fields/types create a blocking schema-change issue and require an approved mapping revision. Do not force new source structures into TEXT simply to finish a run.

- JSON integer must fit SQLite signed 64-bit INTEGER. Booleans are not integers for this contract. Reject undeclared numeric-string, real-to-integer, overflow and boolean coercions.
- For nullable fields, missing or explicit JSON null maps to SQL NULL, with the distinction retained in `record_json` and field-state counts.
- Empty string remains empty string, not NULL. Zero remains zero. Empty list remains `[]`, not NULL.
- For `answers` and `meaning`, this export is reported to have exactly the documented keys. Verify all objects, not a sample. A scalar, missing expected container or unexpected nested key blocks this pinned-profile build.
- For `packages`, compare parsed JSON structures rather than formatting. This export is reported to have one array and 42,496 missing fields. Verify missing/null/list categories independently; do not relabel missing as explicit null in the fidelity layer.
- For `created_at`, verify four dated records and 42,493 missing records for this pinned export. For `updated_at`, verify 42,497 extracted dates. These are snapshot assertions, not permanent global schema constraints.

## 7. Lookup normalization and dates

### 7.1 `headword-key-v1`

Define `question_key = NFKC(casefold(NFKC(question))).strip()` using the recorded Unicode database version. `strip()` removes only leading/trailing Unicode whitespace according to that runtime. Do not collapse internal whitespace, strip accents/punctuation, stem, singularize, remove apostrophes/hyphens, translate or choose a sense.

Apply the same versioned function to queries. Keep original `question` unchanged for display and provenance. An empty resulting key is blocking. A collision is a review issue, not deduplication permission. Preserve all colliding IDs, including case or compatibility-character variants.

Normalization is a lookup policy, not a lemma/POS resolver. Audit overlap with the learning snapshot using both exact and versioned normalized matching; report the policy and keep unmatched inventories private.

### 7.2 Date parsing

`updated_at` and `created_at` retain the extracted source text exactly. Never replace them with a parsed value.

Optional derived columns `*_utc` accept only unambiguous timezone-aware RFC 3339 timestamps under `date-profile-v1`. Emit UTC with `Z`, retaining fractional precision without rounding. Offset conversion must be exact; do not silently reduce nanoseconds to microseconds. Naive dates, locale-specific strings, leap-second cases or unsupported formats remain raw with status `unparsed` and a review issue. Missing and explicit null have distinct statuses. Do not assume the host timezone, seconds versus milliseconds, or parse a malformed value as zero.

A parsing failure in an optional derived timestamp does not destroy source fidelity or block basic lookup, but it blocks any feature requiring that parsed timestamp. If a future export uses numeric or object date values, revise the mapping explicitly; v1 TEXT extraction must not coerce them.

## 8. Import, verification and promotion lifecycle

States belong to a private build manifest, not the assessment API:

```text
received → inspected → staged → validated → promoted
                    ↘ blocked / failed
```

Each state transition records its evidence and command/version. A blocked/failed build cannot update `current.json`.

1. **Preflight:** resolve approved source/output paths; check available disk/memory; validate runtimes, permissions, ignored/untracked status, complete source files and hashes. Observe source metadata before/after reads. Never hash while assuming a changing file is stable.
2. **SQLite source consistency:** inspect WAL/journal sidecars. A live/uncheckpointed source is not a safe bare-copy artifact. Request a stable export or an explicitly approved read-only backup workflow; never checkpoint or modify the owner source without permission.
3. **Resolve AUDIT-001:** run the existing full verification and expose failed check names. Record exact cause and approved correction. This may use the same source files; it must not relax fidelity checks.
4. **Full parse:** UTF-8, root array, all records, duplicate-key rejection, full field/type inventory, stable-ID validation. Use bounded processing; record parser/resource limits and fail clearly rather than silently truncate long content.
5. **Reconcile received JSON/SQLite:** compare IDs and all 27 mapped fields; prove source/SQL field inventory coverage. Record cell counts and mismatch counts by field. Never print raw differences publicly.
6. **Build new staging SQLite:** apply linked DDL, enable foreign keys, set `user_version=1`, insert manifest and fidelity rows, then exact typed entries, derived keys/dates and issues. The importer must validate values before parameterized inserts.
7. **Transactions:** use a single logical build with transactional batches if necessary. Partial staging output is never a valid release. Default v1 restart behavior is a clean new staging run, not unverified resume.
8. **Validate target:** integrity/foreign-key checks, counts, identity and source-row bijection, all-field typed reconciliation, raw payload fingerprints, normalization/date expectations and query/index behavior. Run negative synthetic tests as well as checks on the complete dataset.
9. **Finalize:** close connections and settle the new output into a standalone SQLite file without required WAL sidecars. Hash the closed file. Write external `manifest.json` and `validation.json` atomically with file/directory modes verified. The SQLite file MUST NOT contain its own final byte hash, which would be self-referential.
10. **Promote:** only after blocking issues are zero and mandatory tests pass, atomically replace `current.json` with the validated build reference and output hash. Keep previous approved build intact for rollback. No automatic server upload or application DB replacement.

### Idempotency and rollback

Logical build identity depends on source hashes plus mapping, schema, normalization, Unicode and builder versions. Reuse an existing build only after verifying its manifest and content; never overwrite a conflicting build ID. An interrupted staging run may be retained for private diagnosis or removed by an explicitly scoped cleanup.

Byte hashes identify concrete artifacts; do not promise byte-identical SQLite files across different runtimes/page layouts. Deterministic logical content/order can be tested separately. Rollback changes only the private current pointer to a previously validated artifact; it never edits source records or merges incompatible versions.

## 9. Read contract and downstream measurement boundary

Open published artifacts with `mode=ro` and query-only behavior; never use a consumer's read operation to create a missing SQLite file. Verify the build hash at ingestion/startup as appropriate, not by rescanning the whole file for every lookup.

Supported v1 read operations:

- `get_by_source_id(source_id)` → exactly one entry or not found.
- `lookup_exact_original(question)` → ordered candidate list; no silent first-row selection.
- `lookup_normalized(question)` → compute the manifest's key policy and return all matching candidates ordered by source ID with a bounded page size and keyset pagination.
- `iter_entries(after_source_id, limit)` → stable binary source-ID order with pagination; no unspecified ordering.
- Aggregate audit queries → only allowed field/count summaries, not automatic export of restricted content.

Use parameterized predicates. Example query shape:

```sql
SELECT * FROM v_dictionary_lookup
WHERE question_key = ? AND source_id > ? COLLATE BINARY
ORDER BY source_id COLLATE BINARY LIMIT ?;
```

Use a separate first-page query without the cursor condition; do not rely on a sentinel that might omit valid IDs. A source-ID lookup is a different query and must not use the headword index.

The existing offline tools target the earlier learning schema; this artifact does not claim drop-in compatibility. A future explicit `dictionary_standardized_v1` read adapter must map the new view and be tested. Do not create a misleading `vocabulary` view that implies learning-state or measurement semantics.

Downstream sequence remains:

```text
source record → reviewed lemma/POS + target sense → eligible frame → reviewed item
```

The dictionary build supplies source IDs and provenance only. `level`, `new_level`, `popularity`, `en_order`, `vn_order` and `e_factor` remain legacy fields until their meaning is independently documented. None is automatically CEFR, calibrated item difficulty, frequency or mastery. WordNet lexical candidates cannot approve senses. The one learning-only headword requires owner/content review, not automatic source repair.

## 10. Validation manifest and diagnostics contract

The external manifest MUST contain:

- `schema_version`, logical `build_id`, mapping/normalization/date/builder/Unicode/runtime versions.
- Source file roles, SHA-256 and byte sizes; owner-confirmed provenance and whether production comparison was performed.
- Expected and actual record counts, stable-ID counts, duplicate/invalid IDs and nested duplicate-key counts.
- All mapped fields, missing/null/empty/type distributions, compared cell counts, mismatch counts and unmapped inventories.
- Exact/normalized headword counts and collision counts under the declared policy.
- Date status and packages-category counts; optional parse/review issues.
- Target table counts, foreign-key/integrity results, row/payload correspondence and source-preservation hashes.
- Source-to-learning overlap summary, with record-level exceptions only in the private review file.
- Git protection and permission checks; target hash after close; previous build/current pointer references.
- Named test results and separate `blocking`, `review`, `optional_not_run` categories. Overall status cannot be inferred from selected successful counters.

Diagnostic CLI output MUST list failed check names and safe categories. Full row differences remain private. Human timestamps are recorded as observations; semantic comparison may exclude an explicitly enumerated observational timestamp field, but never arbitrary metadata or entire checks. Provenance, counts, types, hashes, permissions and mapping decisions remain material.

Errors: `SOURCE_CHANGED`, `SOURCE_SQLITE_NOT_STANDALONE`, `DUPLICATE_JSON_KEY`, `INVALID_STABLE_ID`, `SCHEMA_DRIFT`, `TYPE_COERCION`, `FIELD_MISMATCH`, `TARGET_INTEGRITY_FAILED`, `GIT_PROTECTION_FAILED`, `AUDIT_GATE_FAILED`, `RESOURCE_LIMIT`, `NORMALIZATION_EMPTY`. Each blocks promotion. `NORMALIZATION_COLLISION`, `DATE_UNPARSED` and `LEARNING_ONLY_ENTRY` are review issues unless a consuming feature requires their resolution.

## 11. Executable acceptance criteria

| ID | Test | Required result |
|---|---|---|
| S01 | Missing source, alias or output escape | Fail before creating/modifying owner files |
| S02 | Source changes or nonempty live WAL/journal | Block unsafe copy/import; no source checkpoint |
| S03 | Full pinned snapshot | 42,497 source objects and received SQL rows; next snapshots use their own manifest |
| S04 | Duplicate root/nested key or invalid/duplicate `_id` | Reject; no overwrite or dropped records |
| S05 | Stable-ID reconciliation | Equal ID sets and complete source/target row bijection |
| S06 | Mapping inventory | All 27 fields covered; unknown roots/keys/columns block |
| S07 | Full field equality | Zero undeclared mismatches across all records/fields |
| S08 | Missing/null/empty/zero/list distinctions | Flattening policy followed; fidelity payload retains distinctions |
| S09 | Type traps | Reject bool-as-int, overflow, numeric strings and undeclared float coercion before binding |
| S10 | Date cases | Raw text unchanged; timezone/precision correct; unsupported values explicitly unparsed |
| S11 | Unicode collision and empty key | Preserve all colliding records; block empty key; no unique-key data loss |
| S12 | Payload/source conservation | Raw payloads reconstruct all typed source fields; digests and ordinals verify |
| S13 | Integrity/foreign keys | `integrity_check=ok`, empty `foreign_key_check`; no orphan/missing entry rows |
| S14 | Read adapter | Correct all-candidate behavior, stable pagination, query-only connections, indexed exact lookup |
| S15 | Injection/markup | Parameterized SQL; data never executed or fetched during import; rendering contract flags raw HTML |
| S16 | Private output | Directories 700, files 600, exact paths ignored/untracked, no raw stdout/public diff |
| S17 | Interruption/idempotency/rollback | No partial promotion; originals unchanged; previous build remains usable |
| S18 | Verifier mismatch regression | Named failure remains visible; AUDIT-001 reproduced/resolved without weakening material checks |
| S19 | Learning overlap | Same declared normalization; one reported exception reviewed, never silently inserted/deleted |
| S20 | Scope guard | No lexical row count reported as approved measurement universe, no auto-CAT/CEFR/sense approval |

S01–S18 and S20 are mandatory promotion gates for this profile. S19 requires a complete overlap report and preserved review queue, not forced lexical agreement. Optional WordNet, semantic review and independent production comparison are separate gates for their own claims; their omission must not be disguised as a fidelity test failure.

Performance acceptance for this local release: record runtime, peak memory, file size and exact lookup query plans on the actual host. Require bounded pagination and the intended indexes; establish product latency/throughput targets only with a declared workload and environment. Do not invent a millisecond SLA from an unexecuted migration.

## 12. Later implementation work packages and handoff

No worker is authorized by this document alone. When the owner resumes implementation, use a single live-data writer and bounded tasks with early artifacts:

1. **WP1 — verifier gate:** expose/reproduce AUDIT-001; deliver regression test, narrow fix and full pass/fail evidence. No enrichment or new parser framework.
2. **WP2 — builder:** implement the versioned new-artifact builder and schema application; deliver negative synthetic tests and source-protection tests before owner-data execution.
3. **WP3 — full build:** reconcile pinned JSON/SQLite, generate staging output and complete validation. Deliver manifest, target hash, row/field counts, issues and rollback evidence.
4. **WP4 — reader adapter:** implement only explicit read operations; test normalization, collision lists, pagination and read-only behavior.
5. **WP5 — integration:** update aggregate data documentation and the seven P0 references after audit acceptance. Keep lexical unit/sense review and item-bank work separate.

Each task brief MUST state allowed paths, forbidden mutations, model configuration, budget, early deliverable and executable acceptance IDs. Parent reviews real artifacts and reruns key checks. A prompt budget is not an enforced runtime limit; report overruns and incomplete deliverables honestly. Do not resume the paused research cron as part of any package.

## 13. Cross-spec traceability

| Existing spec | Required boundary/integration |
|---|---|
| [Measurement](MEASUREMENT_SPEC.md) | Data records are not approved lemma/POS-sense units; retain construct boundaries |
| [Sampling](SAMPLING_AND_ESTIMATION_SPEC.md) | Freeze an eligible reviewed frame separately; normalized lookup count is not N |
| [Scoring](SCORING_SPEC_V0.md) | No score/model/calibration inference from legacy dictionary fields |
| [API/state machine](API_AND_STATE_MACHINE_SPEC.md) | Data-build states remain private; no new assessment enums from this import |
| [Governance](ARTIFACT_LINEAGE_AND_GOVERNANCE.md) | Source/target hashes, versions, derivation, impact and rollback lineage |
| [Pilot](PILOT_CALIBRATION_PROTOCOL.md) | Reviewed items and empirical calibration remain prerequisites |
| [Privacy/accessibility](DATA_PRIVACY_AND_ACCESSIBILITY_SPEC.md) | Restricted content handling; lexical rights separate from participant consent; safe rendering |

This data companion is integrated with the [harmonized P0 suite 2.0.0](README.md). The suite resolves the prior document-level profile/unit/status conflicts and incorporates the approved research clarifications; service implementation, actual data migration and empirical validation remain separate uncompleted gates. Its source-preservation and deferred-migration rules are unchanged.

## 14. Completion definition

**Spec delivery:** this document, linked DDL, source-field coverage check, in-memory synthetic DDL checks and repository links. These may be verified now without migrating owner data.

**Implementation delivery later:** functioning builder and reader, resolved AUDIT-001, immutable originals, complete pinned-data reconciliation, validated private standardized artifact, safe promotion/rollback, reproducible tests and explicit remaining semantic/psychometric limitations.

Do not say “SQLite standardized” until the latter acceptance criteria pass. For this turn, owner SQLite files are intentionally unchanged and implementation is deferred.
