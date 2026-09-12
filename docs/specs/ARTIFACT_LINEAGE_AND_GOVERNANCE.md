# P0.5 — Artifact lineage and governance

**Version:** 2.0.0
**Status:** release-blocking normative target. [Suite decisions](README.md); [prior version](../../raw/specs-before-harmonization/ARTIFACT_LINEAGE_AND_GOVERNANCE.md) is superseded, not an approval of current artifacts.

## 1. Data provenance and dependency chain

The owner confirms the full 42,497-record server JSON/SQLite export. The earlier 3,885-record learning snapshot and its WordNet candidate audit retain their own identity. The overall full-verifier failure remains an unresolved promotion gate despite aggregate equality. [Current data evidence](../data/SERVER_DICTIONARY_STATUS.md) records provenance separately from technical reconciliation, production comparison and semantic/psychometric validation. [SQLite standardization](SQLITE_DATA_STANDARDIZATION_SPEC.md) remains deferred.

Required chain:

```text
owner source snapshots → standardized data build → reviewed lexical units
→ eligible supported frame → approved item/form mapping → sampling policy/plan
→ presented item + response events → scored result → allowed claim/release
```

A later latent/calibrated profile additionally depends on consented response dataset, fit/parameter uncertainty, linking/invariance and independent validation artifacts. These dependencies do not exist merely because the dictionary is complete.

## 2. Artifact identity and registry

Every artifact registry entry has immutable `artifact_id`, type, semantic version, content hash/hash algorithm, restricted storage locator, creation actor/time, producer/code/runtime version, dependency IDs/hashes, owner, access classification, retention/legal basis and review/release status. Version labels are not substitutes for hashes. Changed content always receives a new immutable identity.

Artifact types include source export, standardized build, unit policy/crosswalk, eligible frame, frequency metadata, item/rubric, form map, sampling policy, route/selection plan, response event stream, scoring profile, result, validation report and claim decision. Full source records, keys and identifiers stay private; public documentation contains schema and aggregates only.

Use original `_id` plus source hash for lexical provenance; source ordinals are snapshot-local. Normalized headwords are lookup keys, not stable IDs. Raw byte hashes identify archived files; canonical logical hashes require declared serialization, field ordering, Unicode/numeric handling and domain separation. Preserve array order where semantically meaningful. Never use self-referential final DB hashes inside that same DB.

## 3. Item key approval and changes

Each operational item version records unit/sense reference, exact content/options, one correct option, rubric/language/format, authoring provenance, content-review protocol, opaque reviewer decisions, adjudication status and evidence references. Answer-key review must be independent of the author; unresolved disagreement is not resolved by majority vote alone.

Key status: `approved`, `disputed`, `no_valid`, `multi_valid`, `quarantined`. Only approved single-key MCQ items enter the default bank. This is item governance, not new public session enums. Multiple acceptable options require a separately approved response format/profile.

Key errors, multiple valid answers, target-answer cues or rendering that changes meaning trigger content quarantine even when item statistics look acceptable. A key/content correction creates a new item version, never silent calibration inheritance. Record impacted forms, sessions, parameter fits and results, then decide recalibration/re-score/withdrawal scope explicitly. A new version is not proof that new empirical calibration exists.

## 4. Frame, form and route manifests

Frame manifest includes all reviewed units, exclusion reasons, source/review/frequency versions, strata/counts and assessment support. Form map fixes one scored item version per frame unit for the default profile. No hardcoded full-dictionary count or selected-bank expansion without a valid design.

Session lineage includes profile `baseline-design-v0.1`, estimand `finite_frame_correct_response_total`, `count_unit=lemma_pos`, frame/form hashes, registered alpha, screening plan/history, focused quotas/risk sets, role and conditional probabilities, RNG/code version and restricted replay state. Seed/hash without retrievable referenced state is not sufficient.

Distinguish selection probability, unconditional inclusion and response propensity. Preserve state as known at selection time. If review changes history later, create a superseding analysis rather than overwrite the basis for original weights.

## 5. Events, transactions and replay

Response events are append-only while retained and contain event/session/presentation IDs, server receipt time, subject pseudonym, version, selected option or dont_know, server-derived category, role, source operation/idempotency reference and minimally required timing. Do not log bearer credentials, raw PII or full dictionary content. Material presentation changes are separate events.

Exactly-once semantics come from idempotency records, unique constraints and transactional state/outbox updates, not a promise of exactly-once transport. Result generation references the exact consumed event set and software. Store transaction/version boundaries so concurrency and retries can be replayed.

Two operations are distinct:

- **Historical replay:** same artifacts/code/config/events → same canonical result under declared numerical tolerance and environment.
- **Re-estimation:** new model/key/frame/assumptions → new result ID, explicit differences and predecessor link; never pretend it is unchanged history.

Pin Python/numeric libraries/RNG, algorithms, ordering, locale/Unicode and serializer as relevant. Exact bytes across different SQLite page layouts are not assumed. A replay attestation includes artifact availability, dependency hashes, numerical comparison and limitations. Authorized deletion can legitimately make replay unavailable; do not recreate erased personal records from caches.

## 6. Release gates and claim registry

| Gate | Required evidence |
|---|---|
| G0 Source | Stable export, fidelity verification and resolved overall verifier failure; private protection |
| G1 Units/content | Approved unit/sense policy and single-key item review; no blocking content defects |
| G2 Design/integration | Supported frame, probability/replay tests, consistent API/scoring/unit schemas and implementation tests |
| G3 Pilot/diagnostic use | Cognitive, accessibility, delivery/missingness and target-population operational evidence; approved diagnostic-use policy |
| G4 Recognition/other claims | Independent empirical validation of each interpretation and its uncertainty; no inference from G0–G2 alone |
| G5 Advanced profile | Separate model/stopping/format/transport/DP release evidence where applicable |

Default claim is `diagnostic_only`; `public_vocabulary_claim_allowed=false`, latent fields null. G4 cannot flip this baseline schema silently: use a separately named, validated claim/profile and compatibility decision.

Each claim record names construct/estimand, population/use, inference category, supporting evidence, assumptions, rebuttals, status (`supported`, `partial`, `unsupported`, `not_studied`), approver and review triggers. Maintain separate records for response-total diagnostics, recognition breadth, external criterion prediction, linking and CEFR/placement. Shared anchors/correlation cannot prove construct interchangeability.

Approvals require accountable product/psychometric/data/security owners for their scope. No unregistered numeric thresholds, inherited Advisor sign-off or old draft metadata authorize production. Exceptions record residual risk and cannot waive mathematical support, data protection or false claims.

## 7. Integrity, exposure and rollback

Anomaly/person-fit is model misfit, not a cheating verdict. Restricted integrity records include detector version, threshold evidence, operating-characteristic/false-positive assessment where applicable, review and appeal/reversal disposition. Do not expose detector internals publicly or automatically subtract words. Independent verified compromise can justify a policy action without pretending it is calibrated person-fit evidence.

Freeze exposure constraints into the selection design; bank/selection changes invalidate weights unless explicitly modelled. Rollback pins prior approved configuration/artifacts and stops new affected sessions; in-flight sessions must either complete under valid frozen assumptions or close without a fabricated score. Never mutate a released frame or silently replace a key in active sessions.

## 8. Privacy, rights and erasure

Dictionary license/provenance and restricted source content are distinct from participant response consent. Participant withdrawal must not delete unrelated lexical entries. Conversely, frozen data is not exempt from valid erasure.

Store direct identity separately from pseudonymous research events. Define finite retention periods and backup/cache/queue deletion handling before collection; no default indefinite retention. For in-scope erasure, remove/crypto-shred personal records and linked snapshots as required, evaluate retained aggregate parameters separately under legal/risk review, keep a minimal non-identifying deletion attestation and set replay availability to `unavailable_due_to_authorized_deletion` where necessary.

Do not promise universal model unlearning, guaranteed public report recall or anonymity from hashing. Dependencies must reveal affected derived artifacts and justify retention/rebuild decisions. Optional DP mechanisms require actual privacy accounting and accuracy/fairness/coverage evidence; noise or pseudonyms alone do not establish DP.

## 9. Acceptance

- GOV01: every released result resolves its complete dependency closure; unavailable or hash-mismatched material artifacts block release/replay.
- GOV02: corrected key/frame/model yields new versions and explicit impact/re-score decisions; no silent inherited calibration.
- GOV03: selection history can be reconstructed; probability meanings cannot be interchanged.
- GOV04: exact idempotent event/result behavior survives retries/concurrency/crash recovery.
- GOV05: baseline claims remain diagnostic; unsupported population/use claims fail independently of code tests.
- GOV06: protected artifacts stay out of Git/public payloads; least-privilege access and audit enforced.
- GOV07: valid deletion traverses dependencies, removes in-scope data and marks replay limitations without retaining erased payloads.
- GOV08: rollback isolates new and in-flight sessions safely; statistics alone cannot override content quarantine or authorize fairness/validity claims.

[Privacy](DATA_PRIVACY_AND_ACCESSIBILITY_SPEC.md) and [Pilot](PILOT_CALIBRATION_PROTOCOL.md) supply detailed scope-specific evidence. No gate is marked passed by this document rewrite.
