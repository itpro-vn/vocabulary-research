# P0 specification suite — harmonized revision 2.0.0

**Status:** normative implementation target; not implemented, calibrated or production-approved. This revision supersedes conflicting requirements in the [archived prior suite](../../raw/specs-before-harmonization/README.md). Historical detail is evidence/design material, not a second active contract.

## Shared decisions

- **Data:** owner-confirmed full server JSON/SQLite export, 42,497 records in the pinned snapshot; earlier learning snapshot 3,885 records. Full verifier rerun reports zero mapped-field mismatches but overall failure. [Current data evidence](../data/SERVER_DICTIONARY_STATUS.md).
- **Data migration:** deferred. [SQLite standardization](SQLITE_DATA_STANDARDIZATION_SPEC.md) governs a future new artifact, not modification of the originals.
- **Default scoring profile:** `baseline-design-v0.1`; estimand `finite_frame_correct_response_total`. This is the implemented offline reference's vocabulary, not a latent-known-word estimate.
- **Frame unit:** each reviewed `lemma_pos` unit has one approved target sense and one locked assessment item/version for the form. The reference CLI's `frozen_frame_assessment_unit` is an internal container label, not evidence that raw dictionary rows have been reviewed.
- **Default result claim:** `diagnostic_only`; `public_vocabulary_claim_allowed=false`; `theta`, `vocabulary_count` and `cefr` are null. A later latent-recognition model needs a separately versioned profile and empirical release approval, not a different label on the same response total.
- **Design:** disjoint screening plus stratified SRS without replacement from the remainder; focused quotas frozen before focused responses. No adaptive early stopping, pooled mean, default guessing correction or nested-product substitution.
- **Research-only:** yes/no correction, isotonic primary scoring, fractional/uncertain-key scoring, CAT/RL, external proficiency prediction and DP statistical releases unless their own gates pass.
- **Safety:** subagents and vocabulary research cron remain paused; document updates do not authorize them to resume. Raw lexical content remains private and Git-ignored.

## Ownership and precedence

| Contract | Owner document | Other documents must reference, not redefine |
|---|---|---|
| Construct, units, allowed claims | [P0.1 Measurement](MEASUREMENT_SPEC.md) | Frame and interpretation boundaries |
| Selection, probabilities, interval assumptions | [P0.2 Sampling](SAMPLING_AND_ESTIMATION_SPEC.md) | Routing and design validity |
| Response reduction and result values | [P0.3 Scoring](SCORING_SPEC_V0.md) | No-score rules and numeric semantics |
| Transport, concurrency, session states | [P0.4 API](API_AND_STATE_MACHINE_SPEC.md) | Protocol + [JSON schemas](assessment_contract.schema.json) |
| Artifact versions and release authorization | [P0.5 Governance](ARTIFACT_LINEAGE_AND_GOVERNANCE.md) | Replay, review and promotion |
| Human studies and empirical evidence | [P0.6 Pilot](PILOT_CALIBRATION_PROTOCOL.md) | Registered studies, not imported thresholds |
| Privacy, security, accessibility | [P0.7 Privacy](DATA_PRIVACY_AND_ACCESSIBILITY_SPEC.md) | Data minimization, deletion, access and UI |

The seven P0 specifications remain revision 2.0.0; the delivery roadmap and data companion have independent version numbers. The new suite resolves document-level profile conflicts; it does not claim the API/service has been implemented or the offline CLI already enforces all new release gates. The proposed API retains `/v1` as a design namespace because no deployed implementation was established; an existing consumer discovered later requires explicit compatibility review before adoption.

## Review traceability and delivery gates

[Research incorporation matrix](RESEARCH_INCORPORATION.md) records decisions for all ten new files, including items rejected or already covered. Research file numbers 66–75 correspond to actual iterations 63–72. The old fixed 20,000-frame, 1,200-item, ten-band and fixed sample-size targets are historical planning candidates, not acquired resources or new mandatory constants.

Mandatory delivery sequence is defined in the [six-phase roadmap](../../ROADMAP_ARCHITECTURE.md#4-six-delivery-phases): Phase 1 trusted data → Phase 2 reviewed frame/items → Phase 3 pilot MVP → Phase 4 human validation → Phase 5 LazzyBee production/operations → Phase 6 optional optimization/expansion. The P0 documents are cross-cutting contracts for all phases, not a completed implementation phase. The roadmap gives each phase its owner role, dependencies, deliverables, exit gate, rework path and remaining specification gaps.

No file count, passing schema test, mathematical expectation fixture or owner data ownership replaces joint release evidence. [Archived specifications](../../raw/specs-before-harmonization/README.md) remain available without preserving their former normative authority.
