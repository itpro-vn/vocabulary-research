# P0.6 — Pilot calibration and validation protocol

**Version:** 2.0.0
**Status:** study design contract, not authorization to recruit or a claim of completed validation. [Suite decisions](README.md).

## 1. Source readiness and study purpose

The complete server export is owner-confirmed and reports 42,497 records, distinct from the earlier 3,885-record learning snapshot. The overall verifier failure is unresolved even though matched-record/field counters passed. Resolve [data gates](../data/SERVER_DICTIONARY_STATUS.md) and the deferred [SQLite build](SQLITE_DATA_STANDARDIZATION_SPEC.md) before claiming an approved input release.

The earlier observation that 3,798 explanations in the learning snapshot contain the headword is snapshot-specific. Do not generalize that count to the full dictionary or reuse learning definitions verbatim as answer-revealing stems. Profile/review the full source before item authoring. Neither stored levels nor incidental POS/CEFR HTML labels are calibration or semantic review.

Default profile `baseline-design-v0.1` measures `finite_frame_correct_response_total` with reviewed `lemma_pos` units and a diagnostic-only claim. The study must separately examine whether/how these responses support receptive-recognition interpretation. No fixed 1,200-item bank, ten strata, participant total, item count or ±10% target is inherited as an empirically justified constant.

## 2. Registered protocol before collection

Register construct/frame/form versions, target deployment population/use, inclusion/exclusion and recruitment design, research consent/ethics review, accommodations, study arms, timing/missingness rules, sample-size/power or simulation rationale, primary estimand, independent criterion, analysis/holdout plan, multiplicity strategy, stopping rules, practical acceptance margins and safety/escalation owners.

Actual numeric recruitment counts, age ranges, retention periods, alpha/precision targets, form-equivalence margins, acceptable bias/coverage error and subgroup support must be selected from the use case and simulations before data collection. They are mandatory configuration fields, not default constants supplied by unrelated vocabulary or CAT publications. Unset required study parameters block recruitment.

Separate build and independent validation by person and relevant form/item exposure. Avoid leakage through repeated attempts, shared stems, anchors or item revisions. A random response split within the same person/item is not an independent holdout. Record target versus achieved support; convenience recruitment/weighting does not automatically make the sample representative.

## 3. Phase A — content and cognitive study

Create a reviewed unit-to-sense crosswalk and a supported item frame. Record item author, independent key review, rubric version, language burden, cue review, distractor rationale and adjudication. Exactly one correct option for baseline MCQ. Quarantine disputed/no-valid/multi-valid and meaning-changing rendering defects before collecting calibration data, regardless of p-value/discrimination.

Use cognitive interviews/think-aloud or equivalent reviewed methods to test meaning recognition versus test-taking cues, translation burden, familiarity, guessing, instruction comprehension and dont_know interpretation. Include intended language/device/accessibility groups. Findings trigger new item versions and re-review, not silent edits to recorded data.

LLMs may draft candidates under restricted-data policy, but cannot approve keys/senses or generate synthetic human responses as if they were pilot observations. Synthetic data are labelled simulations and never fill recruitment gaps.

## 4. Phase B — operational and design pilot

Test instructions, consent, accessibility, mobile/desktop rendering, offline/disconnect recovery, idempotency, timing capture, completion/missingness and response fatigue under the actual deployment conditions. Timing is not used as an unvalidated score correction.

Exercise broad screening followed by frozen focused quotas and SRSWOR remainder draws. Planned research items are outside the scored design and separately consented; default scheduling is after core completion. Planned matrix missingness in a calibration study is not the same as missing required core outcomes in the baseline. Use a separately declared booklet/calibration design and analyse it accordingly.

Log item/form/presentation IDs, unit/stratum, assignment probabilities/risk sets, server outcome, choice/dont_know categories, delivery/response times with trust flags, consent/purpose versions, accommodations and quality/integrity decisions. Keep identity separately restricted. Do not collect more demographic information than justified for the registered validity/fairness analysis.

Baseline API and score validity must be checked end to end, not inferred from the offline scoring function alone.

## 5. Phase C — independent validation of the baseline

Use a longer/independent criterion appropriate to the same construct, with known measurement limitations and reviewed items. A reference test or vendor product is not ground truth. Preply disclosure/claimed margin is not validation of this implementation. Characterize criterion error and avoid equating different lexical units or response formats.

Primary analyses include bias, MAE/RMSE, interval coverage/width, completion, conditional error over the supported ability/band range, endpoint/floor/ceiling effects, form and subgroup differences, missingness patterns and sensitivity to key/response-process assumptions. Correlation is supplementary. Compare to census/known totals in simulation and the registered criterion in human data, distinguishing those two evidence types.

Report conditional uncertainty scope. Fixed-potential-outcome design confidence does not automatically cover stochastic guessing, knowledge changes, key error, unit/frame uncertainty or criterion error. Simulations and repeat administrations should quantify whether the simplified profile's interpretation is acceptable or requires a different model/claim.

A lexical subset test cannot validate unrepresented dictionary tails. Any public recognition claim requires explicit frame scope and evidence that the response score supports that interpretation; otherwise remain diagnostic-only.

## 6. Reliability, forms and longitudinal use

Report conditional/overall error and test–retest with order, memory/practice, time and delivery effects considered. Within-form alpha/KR/omega is not an individual word-count error bound and is not a sole release gate.

Form interchangeability requires preregistered practical-equivalence margins, mean/conditional bias, agreement/dispersion assessment and appropriate common-person or common-anchor evidence. High correlation with material systematic bias fails interchangeability; a negligible but statistically significant difference is evaluated against practical margins rather than a blanket p-value rule.

Common anchors are candidates, not immutable truths: inspect content, fit, DIF and exposure; purify/replace under a versioned linking protocol and propagate linking uncertainty. Growth claims require justified form comparability and practice/time controls. No universal reliable-change or minimal-detectable-change coefficient is transferred from another study.

## 7. Optional latent calibration after baseline evidence

If justified, preregister Rasch/1PL, regularized 2PL or other candidate models with identification constraints, item/person support, priors/estimation, convergence/fit diagnostics, dimensionality, local dependence and held-out evaluation. More parameters are not automatically better; 3PL requires identification/support evidence and comparisons. Item uncertainty and information holes must be measured, not repaired by declaring a larger total sample sufficient.

Distractor/option-position/format effects and key changes require explicit analysis. A calibrated adaptive candidate must validate its actual selection/update/stopping path and uncertainty under estimated parameters. Response-only bootstrap with fixed item parameters is not total uncertainty. Calibration draws/bootstrap/equivalent methods apply to the relevant model claim, not retroactively as mandatory machinery in the simple residual baseline.

CAT/RL, EVI, non-myopic selection and advanced stopping remain off until a separate profile beats the accepted baseline under the same declared time/item budget and satisfies support, uncertainty, fairness and security gates. No imported item-count or calibration-N threshold is authoritative.

## 8. Research alternatives and fairness

- Yes/no correction: require a separately declared familiarity/criterion-calibrated format, real/nonword denominators, independent holdout and subgroup/transport analysis. No universal H−FA/regression correction.
- Isotonic profiles: preserve raw design evidence, preregister frequency-order assumptions and evaluate bias/coverage. Ability monotonicity is not the same as frequency ordering.
- Key uncertainty models: sensitivity/research only; do not replace adjudication or introduce baseline fractional credit.
- External criterion predictions, scale linking and CEFR/placement: distinct studies; same anchors/correlation do not establish cross-construct equivalence. CEFR default stays disabled.
- DP/federated methods: independent privacy/utility/coverage/fairness study with explicit accounting; no default mechanism/budget.
- Integrity detectors: calibrate operating characteristics under realistic prevalence/support; misfit is not cheating. Separate research flagging from confirmed review actions.

Fairness analysis covers justified L1, age/education/background, ability, device and accommodation groups with privacy protection. Report insufficient subgroup power/support rather than “no DIF” from nonsignificance. Test effect sizes, multiplicity, content explanations and measurement invariance as appropriate. Do not disclose identifiable small cells or subtract scores by demographic membership.

## 9. Decisions, artifacts and revalidation

Per item: accepted, accepted-non-anchor, needs-more-data, revise-and-repilot, quarantined or retired, with content/statistical evidence, approver and version. A statistical pass never overrides content/key failure. Item edits invalidate inherited calibration unless a documented impact analysis justifies an exception.

Study outputs: registered protocol; consent/data-purpose versions; de-identified restricted dataset manifest; assignment/response logs; content/adjudication records; analysis code/environment; fit/support/coverage/form/fairness reports; holdout report; claim registry and release decision. Archived raw research is not empirical evidence about this bank.

A change to source/frame/unit policy, key/format, delivery, scoring/routing/stopping, population or intended use triggers scoped revalidation and versioned results. [Governance](ARTIFACT_LINEAGE_AND_GOVERNANCE.md) owns promotion and rollback.

## 10. Acceptance

- PILOT01: required protocol parameters, consent/ethics/privacy owners and sample rationale are approved before recruitment.
- PILOT02: reviewed keys/cues and cognitive evidence precede calibration eligibility.
- PILOT03: independent holdout is leakage-controlled; reference limitations and support gaps are explicit.
- PILOT04: design simulations weight complete paths by actual probability, check intervals/endpoints/missingness and do not claim human validity from fixtures.
- PILOT05: empirical error/coverage/form-equivalence and subgroup evidence meet registered practical criteria, not imported constants.
- PILOT06: model/parameter uncertainty and adaptive behavior are evaluated for the profile actually claimed.
- PILOT07: unsupported recognition/CEFR/placement/transport claims remain disabled; baseline schema remains diagnostic-only.
- PILOT08: deletion, confidentiality, accessibility and incident handling pass end-to-end tests before release.

This protocol is ready for implementation planning, not evidence of completed recruitment or a production-approved score.
