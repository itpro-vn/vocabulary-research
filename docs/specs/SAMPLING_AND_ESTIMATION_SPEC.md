# P0.2 — Sampling and estimation

**Version:** 2.0.0
**Status:** normative implementation target; not a validated human assessment. [Shared contracts](README.md).

## 1. Data, scope and prerequisites

The owner-confirmed full server export contains 42,497 records in the pinned JSON/SQLite, not 42,497 automatically approved units. The older 3,885 learning snapshot is distinct. Full-verifier aggregate equality does not override its overall failure. Resolve [source gates](../data/SERVER_DICTIONARY_STATUS.md) and follow the deferred [SQLite specification](SQLITE_DATA_STANDARDIZATION_SPEC.md).

The default profile is `baseline-design-v0.1`, estimand `finite_frame_correct_response_total`, count unit `lemma_pos`, claim `diagnostic_only`. [Measurement](MEASUREMENT_SPEC.md) defines unit review and supported-frame requirements. This design is not latent recognition, whole-dictionary extrapolation from a convenient item bank, or a nested survey sample.

Freeze U and nonempty strata U_h, counts N_h and one scored item version per unit. Strata may reflect documented frequency evidence; no fixed ten-band, 20,000-unit or 1,200-item requirement survives from the archived proposal. A new frame/bank with incomplete coverage needs a separate observation design; the existing offline reference does not implement bank-construction sampling.

## 2. Disjoint two-stage design

1. Select a broad screening set S1 within the frozen frame under a versioned policy before its responses. Lock its identities/order, item versions and randomization evidence.
2. Record all screening outcomes. Let R_h = U_h minus S1_h and M_h = size(R_h).
3. A registered routing function of permitted screening history H1 chooses the focused quota vector n_h. Lock the vector and selection plan **before any focused responses**.
4. In each R_h, select n_h units by simple random sampling without replacement (SRSWOR). Selection uses a reproducible approved RNG implementation and restricted seed/state. Do not retry seeds or quotas based on focused results.
5. S2 and S1 are disjoint. No repeated scored unit. Every nonempty remainder has positive coverage. This reference requires n_h ≥ min(2, M_h); n_h ≤ M_h, and n_h=0 iff M_h=0. A singleton remainder is a census.
6. Complete the locked design. No adaptive early stopping, on-the-fly item replacement, quota changes after focused responses or precision-based stopping.

Screening item count, focused total, strata, research slots and session time policy are registered study/form parameters, not borrowed universal constants. Routing can redistribute a feasible fixed study budget while satisfying every remainder's support. If constraints cannot be satisfied before selection, reject the plan; if support is lost during administration, return insufficient evidence or invalidate the design as appropriate.

## 3. Research items and exposure

Calibration-only items have scored contribution zero and are marked `research` at selection. They require appropriate research consent and cannot be silently mixed into the core design. Default scheduling is after core scoring/selection to avoid altering the standard response process; interleaving requires a validated, versioned protocol and clear role logs.

Exposure constraints must be resolved before the frozen draw or explicitly represented in the sampling design/risk set. Rejection sampling, shadow-test constraints or replacing exhausted items changes inclusion probabilities unless proven otherwise. Do not preserve SRS weights after a non-SRS selection procedure. A compromised key/item encountered mid-session cannot simply be removed while retaining its original expansion weight.

## 4. Probabilities and audit records

For the locked remainder design, q2_i = n_h/M_h conditional on H1 and the frozen risk set. This is not automatically whole-session inclusion probability and not response propensity. Persist distinct fields for:

- frame/form/item versions and stratum;
- S1 history reference, outcomes/statuses, route policy and decision;
- remainder/risk-set reference and counts;
- focused quota vector, draw algorithm/version, restricted seed or replay state;
- per-unit conditional selection probability, role and selection order;
- response/missingness status separately from selection.

A hash without retained reconstructable artifacts is not sufficient for replay. History and draw references are immutable and access-restricted. Mutation of H1 or the risk set after selection invalidates replay; do not recompute weights against a different history under the same result version.

## 5. Estimator

Let A_h be the number correct in observed screening items in stratum h, k_h the number correct among n_h focused items, and M_h the remaining population size.

```text
T_hat_h = A_h                         if M_h = 0
T_hat_h = A_h + M_h × k_h / n_h       otherwise
T_hat   = sum over strata of T_hat_h
```

Screening contribution weight is 1. Focused contribution weight is M_h/n_h. Research-only contribution weight is 0. Incorrect and explicit dont_know are fixed response outcomes of 0, not evidence of latent nonknowledge. Missing/timeout/technical outcomes are not observations of 0.

Conditional on a valid H1 and fixed potential outcomes, expected focused expansion equals the remainder total; therefore the residual total is design-unbiased for the declared response total. This does not prove unbiased latent knowledge or validate human-response invariance.

**Prohibited substitution:** `1/(pi1 × q2)` is not the default weight for S2 sampled from the complement of S1. A genuine nested S2 subset of S1 has a different observation design and may use a separately validated product expansion. Never pool S1 and S2 as a fixed-size SRS or use a raw mean weighted by observed band exposure.

## 6. Interval and variance

Default interval: finite-population hypergeometric inversion with Bonferroni allocation, as in the reference implementation. For each nonempty remainder with observed k successes in n draws from M units:

1. Candidate integer success totals K range from k to M−n+k.
2. Retain K when both `P_K(X ≥ k)` and `P_K(X ≤ k)` are at least alpha/(2H), with H equal to the frozen number of strata.
3. Add A_h to the lowest/highest retained totals; sum endpoints across strata.
4. A census remainder produces an exact count; an empty remainder contributes the observed screening total only. Empty accepted set or numerical failure is a scoring failure, never zero-width certainty.

This gives a conservative design-confidence interval conditional on fixed potential outcomes, frozen screening and valid focused sampling. Uniform conditional coverage can imply unconditional coverage under the stated design; full-path resampling is not mandatory for every valid conditional interval. Full-path simulations remain useful for validating actual routing and implementation.

Do not replace the interval with Wald/normal approximations for all-right/all-wrong or sparse strata. The closed-form conditional variance component, when n≥2 and M>n, is `M² × (1−n/M) × s²/n`; it is a diagnostic, not the default interval. Stochastic responses, calibration parameters, key errors, uncertain unit definitions and model/linking/transport uncertainty are outside this interval unless explicitly modelled in a different profile.

## 7. Missingness and integrity

Any missing scored observation returns `insufficient_evidence` with null estimate/interval, even if remaining observed items look precise. No default imputation, propensity correction, rescaling to answered items or early-stop estimate. A validated future missingness estimator must be separately registered and tested under plausible nonignorable missingness.

Statistical anomaly is not a cheating finding. Keep raw evidence and versioned review decisions. Excluding flagged outcomes while keeping original weights is invalid. Confirmed design compromise invalidates the result; unreviewed flags do not manufacture correction factors. Detailed thresholds/evidence are not public API data.

## 8. Deferred alternatives

Keep unsmoothed design-weighted profiles in restricted diagnostics where estimable. Isotonic/PAVA may be studied with explicit population/order assumptions, raw-versus-constrained sensitivity and design-aware bias/coverage evaluation. Mokken ability monotonicity is not frequency-order monotonicity. Neither smoothing nor frequency priors repair zero inclusion probability or unsupported bands.

Calibration weighting, model assistance, nested sampling, online CAT, EVI/RL and sequential confidence methods are separate candidate profiles. No archived algorithm or research publication changes the active estimator automatically.

## 9. Simulation and acceptance

- SAMP01: exact probability-weighted enumeration over small populations yields expectation equal to census response total; include asymmetric response-dependent quotas and probability mass exactly 1.
- SAMP02: genuine nested and disjoint designs have separate fixtures; the wrong nested-product substitution must fail the disjoint fixture.
- SAMP03: test interval coverage over all small binary populations, including endpoints, sparse/census strata and every route; do not average unequal-probability paths equally.
- SAMP04: reject duplicate/out-of-frame selections, overlap, absent strata, unsupported quotas and unknown probability semantics.
- SAMP05: missing scored response withholds the count; optional research omission cannot contaminate the core sample.
- SAMP06: recompute selected IDs/quotas/conditional probabilities from frozen replay evidence; post-draw mutation is detected.
- SAMP07: exposure, item invalidation and non-SRS selection cannot reuse SRS weights.
- SAMP08: fixed baseline rejects advanced stopping/configuration; diagnostics cannot silently replace its estimate.

The corrected research fixture proves expectations for its tested finite populations, not general human validity or all interval coverage. Existing offline tests are a reference starting point. [Scoring](SCORING_SPEC_V0.md), [Pilot](PILOT_CALIBRATION_PROTOCOL.md) and [Governance](ARTIFACT_LINEAGE_AND_GOVERNANCE.md) complete the release gates.
