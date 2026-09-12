# P0.3 — Scoring V0

**Version:** 2.0.0
**Status:** harmonized normative target. This replaces the prior Bayesian-default proposal; [historical design](../../raw/specs-before-harmonization/SCORING_SPEC_V0.md) is research-only. [Suite contract](README.md).

## 1. Current data and default profile

The owner-confirmed server dictionary export has 42,497 records; the earlier learning snapshot has 3,885. The overall JSON/SQLite verifier failure remains open despite matching aggregate counts and zero field mismatches. See [data status](../data/SERVER_DICTIONARY_STATUS.md). [SQLite standardization](SQLITE_DATA_STANDARDIZATION_SPEC.md), reviewed units, valid items and a frozen supported frame are prerequisites; none supplies calibrated person/item parameters by itself.

Default: `profile_id = baseline-design-v0.1`, `estimand = finite_frame_correct_response_total`, `count_unit = lemma_pos`, `claim_status = diagnostic_only`, `public_vocabulary_claim_allowed = false`. The existing reference [baseline.py](../../tools/lazzybee/baseline.py) computes this response total under its documented assumptions. It does not implement the proposed API, item review, access controls or all release gates.

No default latent theta, recognized vocabulary count, guessing/slip correction, CEFR, fractional-key credit, response-time correction or isotonic score. Advanced models need new profile IDs and empirical governance; they must not be silently substituted under V0.

## 2. Trusted scoring input

Only server-authorized immutable inputs enter the engine: frame/version and unit-review status; form/item/key versions; stratum membership; frozen S1/S2 plan, quotas and risk-set references; validated response events; registered alpha; scoring code/environment version; integrity/retention eligibility.

The client submits option ID or explicit dont_know, never correctness, weights, difficulty, frame size, key, response classification or score. Reject duplicate/out-of-frame IDs, duplicate scored units, invalid keys, missing plan evidence, unsupported quotas and mismatched versions before arithmetic.

The unit adapter may map the CLI container label `frozen_frame_assessment_unit` to `count_unit=lemma_pos` only with a reviewed frame. Do not alter CLI output by relabelling arbitrary dictionary IDs as reviewed units.

## 3. Response semantics

| Server status | Value/use |
|---|---|
| `correct` | y=1, only from approved server-side single key |
| `incorrect` | y=0, valid selected option not equal to key |
| `dont_know` | y=0, explicit user response; distinct analytic category |
| `timeout` | Missing observation; no y |
| `not_answered` | Missing observation; no y |
| `technical_failure` | Missing observation; no y |
| not presented | Not an observed outcome; no response row fabricated |

`dont_know` is not synonymous with timeout, silence or technical failure. Research-role events are not scored core outcomes. Unavailable/revoked keys or compromised designs invalidate scoring rather than becoming `incorrect`. Preserve original events when a later review changes eligibility.

MCQ V0 requires exactly one approved correct option. Review must resolve no-valid/multi-valid/disputed cases before calibration/operational scoring; otherwise quarantine. No majority-vote rescue, partial credit or acceptable-set expansion in this profile. A corrected key creates a new item version and explicit result/calibration impact decision.

## 4. Deterministic scoring pipeline

1. Validate authorization, frozen artifact dependency closure and version coherence.
2. Validate design under [Sampling](SAMPLING_AND_ESTIMATION_SPEC.md), not only JSON shape.
3. Resolve submitted option IDs against the exact presentation/key version; derive server categories.
4. Separate scored and research roles. Determine whether every selected scored unit has a valid binary response.
5. On missing observations, emit `insufficient_evidence`, estimate and interval null, with safe reason codes. Do not enter arithmetic.
6. Otherwise compute the residual estimator and hypergeometric-inversion Bonferroni interval exactly as P0.2 defines.
7. Reject numerical errors, invalid bounds, nonfinite values or values outside [0,N]. Do not silently clip an invalid result to pass.
8. Produce a versioned internal result, signed/hashed according to Governance, plus an authorized safe projection.

Order, serialization, floating tolerances, SciPy/NumPy/RNG versions and alpha are pinned. Store full precision internally; public display precision must not imply greater accuracy. Repeated requests for the same completed result are idempotent. Re-scoring under changed code/key/model produces a new result ID and supersession relation, not an overwrite.

## 5. Result contract and no-score behavior

Shared machine contract: [assessment_contract.schema.json](assessment_contract.schema.json), definition `AssessmentResult`.

| Field | Baseline rule |
|---|---|
| `status` | `scored`, `insufficient_evidence` or `invalidated` |
| `profile_id` | `baseline-design-v0.1` |
| `estimand` | `finite_frame_correct_response_total` |
| `count_unit` | `lemma_pos` after reviewed-frame approval |
| `frame_size` | Count from frozen approved manifest, positive integer |
| `estimate`, `interval` | Both present/non-null only for `scored` |
| `claim_status` | `diagnostic_only` |
| `theta`, `vocabulary_count`, `cefr` | Always null |
| `public_vocabulary_claim_allowed` | Always false |
| `reason_codes` | Safe reasons; nonempty for no-score states |
| lineage IDs/versions | Server-generated immutable references |

`insufficient_evidence` means the valid design lacks required observations/support to compute a released count. `invalidated` means a previously computed/internal result or completed attempt cannot be used because confirmed validity/design conditions failed. Malformed requests are API errors, not psychometric statuses. An unexpected engine/numerical failure is HTTP 503/session `failed`, not a fabricated `invalidated` or zero score.

Safe reasons include `incomplete_design_responses`, `design_support_lost`, `confirmed_integrity_failure`, `item_key_invalidated`, `authorized_data_deletion`. Internal diagnostics may be more detailed under restricted access. Statistical anomaly alone cannot automatically trigger invalidation, correction or unweighted exclusion. Missingness rules still apply after legitimate exclusion.

## 6. Interval and uncertainty scope

For scored baseline results, interval type is `design_confidence`; method is `hypergeometric_inversion_bonferroni`; bounds/level derive from registered alpha and P0.2. Conditions are `fixed_potential_outcomes`, `frozen_screening`, `valid_focused_sampling`. It is not a Bayesian credible interval or a prediction interval for latent knowledge.

All-right/all-wrong responses do not imply zero uncertainty unless supported by census logic. Parameter uncertainty, form/key uncertainty, population transport and stochastic responses require separate studies. A fixed-parameter or design interval cannot be labelled `total_uncertainty` or calibration-error-aware without evidence. No need to bolt calibration draws onto a profile that has no calibrated latent model.

Isotonic diagnostics must keep the unsmoothed estimate and be clearly separate; no corrected result replaces the baseline without a new validated profile. Research sensitivity after excluding anomalous items must use a defensible redefined design/model, not unchanged baseline weights.

## 7. Reporting and access

The complete quantitative `AssessmentResult` is an authorized research/diagnostic contract. Until a user-facing diagnostic release is approved, ordinary public UI receives a completion/no-score message and safe limitations, not a renamed vocabulary count. Public endpoints must enforce purpose/scope; a schema does not grant access.

A later approved recognition interpretation needs a new governed claim/profile and compatible schema change. It cannot set `public_vocabulary_claim_allowed=true` in this baseline schema. External recruitment labels remain labels, not project-generated CEFR. No Preply or foreign-study coefficient/precision target is transferred as measured performance.

## 8. Acceptance and implementation gap

- SCORE01: correct/incorrect/dont_know mapped distinctly; missing/technical statuses withhold numeric outputs.
- SCORE02: scored and no-score shapes pass/fail the shared schema; public latent fields always null.
- SCORE03: duplicate, unknown, overlapping and unpresented unit responses are rejected.
- SCORE04: replay reproduces result within pinned numeric/serialization rules; schema/code upgrades yield explicit new versions.
- SCORE05: census, endpoint, sparse-stratum and numerical-failure fixtures behave correctly; no silent clipping.
- SCORE06: ambiguous/unapproved keys never score; revisions preserve adjudication and affected-result lineage.
- SCORE07: baseline rejects unregistered corrections, stopping methods or latent profiles.
- SCORE08: restrictive result access and no-score UI do not expose keys, frame inventories, seeds or private diagnostics.

Existing 17 offline tests are not evidence that the whole contract is implemented. Implement the adapter/service and test these gates before API deployment or score claims.
