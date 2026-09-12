# Current server-dictionary evidence and readiness

**Status:** source supplied; technical promotion gate unresolved. This is the current scope statement. The [older learning snapshot audit](LAZZYBEE_SNAPSHOT_AUDIT.md) and [its aggregate JSON](snapshot-audit.json) remain valid only for that distinct snapshot.

## What is established

The owner confirms `dictionary_optimized_readable.json` and its flattened `dictionary.sqlite` are the full server dictionary export. Both are present in the private, Git-ignored local `private-dictionary/` directory; they are not published here.

The parent's full-verifier rerun returned:

- JSON entries, SQLite rows and stable-ID overlap: **42,497** each.
- JSON surface-unique and normalized-unique headwords reported by that verifier: **42,497** each.
- Source-only IDs, destination-only IDs and mapped-field mismatches: **0**.
- Synthetic verification tests: **4/4 core and 2/2 extended** passed.
- **Overall status `verification_failed`, exit 2.** This remains unresolved; no inferred root cause or final audit approval.

The audit worker additionally reports 27 mapped fields, 1,147,419 compared cells, source preservation, SQLite integrity `ok`, 4 created-date records, 42,497 updated-date records, one packages array, otherwise missing packages, and NULL related/user_note columns. These are worker evidence to retain/revalidate, not permission to waive the failing overall gate.

The parent separately confirmed the protected local files' hashes:

- JSON: `7e8dded6820c34e44966797e24c294a18e209a4b20681cffa99137e2fb11e01f`
- SQLite: `ed0e985d12b2e7bf1ea77dbeed0554d83ebcf3ccc58c783d3d04cbb0ac695bef`

No independent production-server snapshot comparison was performed. Owner-confirmed provenance, local conversion evidence and production comparison are distinct claims. Oxford provenance, full-export semantic quality, frequency/CEFR meaning and psychometric readiness are not established.

## Relation to the learning snapshot

The earlier `english_optimized.db` has **3,885** rows. Full-verifier output confirms **3,884** normalized overlaps with the new export; the worker reports one learning-only and 38,613 server-only headwords. This is not a strict subset assertion and not sense/content equivalence. Preserve the exception privately for review, not automatic insertion/deletion.

The earlier **3,848 WordNet lexical candidates** and **3,798 headword-containing explanations** refer only to the learning snapshot. They must not be reported as full-export coverage or cue statistics. No new WordNet mapping of the full export was completed.

## Next gates, not work already performed

1. Diagnose the exact overall-verifier failure; do not hide a failing check behind aggregate equality.
2. Implement the approved [SQLite standardization spec](../specs/SQLITE_DATA_STANDARDIZATION_SPEC.md) later in a new private artifact, with originals unchanged.
3. Review lemma/POS/target-sense units and content, then freeze a supported frame and item map. Raw record count is not N for measurement.
4. Integrate baseline/service contracts, then run the human pilot and validate each allowed claim.

Subagents and the vocabulary research cron are paused. This documentation update does not resume them or perform a migration. [Harmonized P0 suite](../specs/README.md) is the active implementation target, not a statement of deployed readiness.
