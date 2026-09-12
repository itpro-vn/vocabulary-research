# Vocabulary Research — architecture and implementation roadmap

**Version:** 2.0.0
**Status:** harmonized implementation target; production and empirical claims not approved. Historical Advisor reviews apply only to their [archived revision](raw/specs-before-harmonization/ROADMAP_ARCHITECTURE.md), not automatically to this revision.

## 1. Current evidence

The owner confirms a full server dictionary export: 42,497 records in JSON/SQLite, separate from the earlier 3,885-record learning snapshot. Both remain private local artifacts. The full verifier reports matched records/IDs and zero mapped-field mismatches but **overall verification failure**; the exact failed gate remains unresolved. No source migration, reviewed full measurement frame or human calibration is completed. [Source evidence](docs/data/SERVER_DICTIONARY_STATUS.md).

Research files 01–75 are retained in [raw/](raw/README.md), including the newly reviewed files 66–75/iterations 63–72. The [incorporation matrix](docs/specs/RESEARCH_INCORPORATION.md) distinguishes accepted clarification, already-covered controls and deferred models. The vocabulary research cron and subagents remain paused.

## 2. Architecture decisions

- Use LazzyBee owner data first. Keep original export and flattened SQLite unchanged; create a separately versioned standardized private artifact later.
- Separate source row, reviewed lemma/POS-target-sense unit, supported sampling frame and approved item version. Do not use row count as vocabulary N.
- Default `baseline-design-v0.1` estimates `finite_frame_correct_response_total`, using disjoint screening plus probability-sampled remainder, not latent known-word count.
- Baseline remains diagnostic-only: public vocabulary claim false, theta/vocabulary_count/CEFR null. Empirical recognition claims require separate evidence/profile approval.
- Preserve single-key MCQ, explicit dont_know, no missing-as-wrong, no adaptive early stopping and no automatic guessing/isotonic/RT correction.
- Prefer explicit artifact/response/claim contracts and a verified baseline before calibrated CAT or other advanced models. Papers/vendor claims do not provide local calibration.

## 3. Modules and boundaries

1. **Private data onboarding:** source fidelity, standardized lookup, hashes/versions, exception inventory; no production DB replacement.
2. **Unit/content pipeline:** human sense/POS/key review, cue/distractor/accessibility checks, supported frame and form manifests.
3. **Sampling/session service:** frozen plans/probabilities, secure assignments, idempotent submission and consent-aware research slots.
4. **Scoring/claims:** deterministic response reduction/residual intervals, explicit no-score behavior, restricted diagnostic results and later separately validated models.
5. **Governance/validation:** dependency closure, privacy/erasure, exposure/integrity review, simulation/pilot/holdout and rollback.

Data and item IDs are not public enumeration APIs. Keys, raw source content, seeds and detector internals remain restricted. Public documentation contains schema, tests using synthetic values and approved aggregate evidence.

## 4. Ordered work packages

| Stage | Deliverable | Exit condition |
|---|---|---|
| A — data gate | Exact verifier failure diagnosis and narrowly justified correction | Full named checks pass without dropping material invariants |
| B — standardization | New private artifact per [SQLite spec](docs/specs/SQLITE_DATA_STANDARDIZATION_SPEC.md) | Original hashes unchanged; full mapping, types, NULL/date/JSON, private promotion/rollback verified |
| C — units/content | Reviewed unit/sense and single-key item/form manifests | Supported frame, explicit exclusions, no unapproved key/cue ambiguity |
| D — baseline/service | Read adapter, frozen sampling, scoring and proposed API integration | Joint schema, response, concurrency, replay, security and end-to-end tests |
| E — pilot/claims | Registered cognitive/operational/independent validation studies | Practical error/coverage/form/fairness/use criteria pass for declared claims |
| F — optional advanced profile | Calibrated model/CAT/other format | Better than baseline under same declared budget, with own uncertainty/support/claim gates |

Do not implement a new profile or raise public claim strength merely to use additional research. Source count, bank size, number of strata and respondent N are separate quantities. Historical 20,000-frame/1,200-item/ten-band/sample-count plans are not current mandatory constants.

## 5. Active specification suite

- [Measurement](docs/specs/MEASUREMENT_SPEC.md)
- [Sampling and estimation](docs/specs/SAMPLING_AND_ESTIMATION_SPEC.md)
- [Scoring V0](docs/specs/SCORING_SPEC_V0.md)
- [API and state machine](docs/specs/API_AND_STATE_MACHINE_SPEC.md) + [machine schema](docs/specs/assessment_contract.schema.json)
- [Artifact lineage and governance](docs/specs/ARTIFACT_LINEAGE_AND_GOVERNANCE.md)
- [Pilot and calibration](docs/specs/PILOT_CALIBRATION_PROTOCOL.md)
- [Privacy/accessibility](docs/specs/DATA_PRIVACY_AND_ACCESSIBILITY_SPEC.md)
- Data companion: [SQLite standardization](docs/specs/SQLITE_DATA_STANDARDIZATION_SPEC.md) + [proposed DDL](docs/specs/sqlite_standardization_v1.sql)

[Suite README](docs/specs/README.md) defines ownership/precedence. The seven P0 documents are updated together at revision 2.0.0. Historical detail is retained under raw/specs-before-harmonization, not simultaneously authoritative.

## 6. Status and approval boundary

Completed artifacts: research archive, older snapshot audit/reference tools, data-copy evidence, research decision review, SQLite specification/DDL and harmonized P0 documents. Existing offline tests and new schema checks are engineering evidence only.

Not completed: resolved overall data audit, standardized owner-data build, reviewed full-frame bank, API service, human pilot/calibration, independent production snapshot comparison or public recognition/CEFR validation. Source data and application code remain unchanged in this documentation revision. Implementation and background research stay deferred until separately requested.
