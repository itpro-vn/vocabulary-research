# P0.1 — Measurement contract

**Version:** 2.0.0
**Status:** harmonized normative target; empirical approval pending. [Suite decisions and precedence](README.md).

## 1. Evidence and construct

The owner has supplied a full server dictionary export with 42,497 records, distinct from the 3,885-record learning snapshot. Local full-verifier output reports equal record/ID counts and zero mapped-field mismatches but overall failure. [Current source evidence](../data/SERVER_DICTIONARY_STATUS.md) and [SQLite standardization](SQLITE_DATA_STANDARDIZATION_SPEC.md) govern that unresolved data gate. No POS/sense review, pilot, calibration or approved measurement frame is inferred from these counts.

The eventual product construct is **receptive recognition of an approved target meaning for a lemma–part-of-speech unit in a finite declared English lexical universe under a standardized item format**. It is not productive vocabulary, all meanings of a word, collocations, speaking, grammar, general English proficiency, CEFR or word-family size.

The default operational research profile is narrower: `baseline-design-v0.1` estimates `finite_frame_correct_response_total` for a fixed set of approved assessment units. Software can establish design properties of this response total without establishing latent recognition. Both concepts must stay distinct in documentation, data and UI.

## 2. Source record, lexical unit, frame and item

| Entity | Identity and review rule |
|---|---|
| Source record | Exact owner `_id` + source snapshot hash; no identity from normalized word or ordinal |
| Lexical unit | Versioned `unit_id`, canonical lemma, approved POS, chosen target sense, source references and review decision |
| Frame membership | Versioned eligible-unit manifest, stratum and explicit exclusion/reason policy |
| Item version | Immutable stem/options/single approved key/rendering/rubric and unit reference |
| Form mapping | Exactly one locked scored item version per eligible unit in the default profile |

`count_unit = lemma_pos`. One unit has one approved target sense under a declared selection policy; selecting a sense does not redefine the counting unit as all senses. Distinct POS may be distinct units. Inflections, orthographic variants, homographs, proper names, specialist terms, abbreviations, MWUs and loans require explicit inclusion rules and reviewer decisions. Multiword diagnostics and word families are separate constructs unless approved through a new frame/claim profile.

Lookup normalization does not perform lemmatization, sense disambiguation or deduplication. Preserve collisions. WordNet matches are candidate links only, including single-candidate cases. Oxford/CEFR provenance is not established by level labels or HTML clues.

## 3. Universe approval and representativeness

N is computed from the frozen eligible-unit manifest, never hardcoded as 3,885, 20,000, 42,497 or approximately 44,000. Frequency strata require an acquired/licensed/versioned source and a documented unit-mapping policy. Legacy `level`, `new_level`, `popularity`, `en_order`, `vn_order` and `e_factor` are not automatic frequency or calibrated difficulty.

The default baseline requires complete assessment support for its declared frame: every unit has an approved locked item, or a separately validated item-selection/observation design explicitly accounts for missing support. Choosing only easily authored items then expanding to the full dictionary is forbidden. If support is partial, shrink and rename the frame transparently or declare the estimator unavailable; do not impute zero or extrapolate an unstudied tail.

A frame manifest records source/build hashes, unit policy, content-review protocol, inclusion/exclusion inventory, stratum counts, frequency provenance, form mapping, population/use scope and governance approval. The selected sense policy must be frozen before item development and response collection; changing it changes the frame version.

## 4. Observation format and potential outcomes

The baseline uses meaning-recognition MCQ items with exactly one content-approved correct option plus explicit `dont_know`. Stem language, answer language, number of options, instructions, delivery and allowed aids are versioned. No exact number of options or time budget is claimed empirically optimal; register them per study/form before use.

For the mathematical reference, y_i is the fixed binary response that would be observed for unit i under the locked item/conditions. Correct is 1; incorrect or explicit `dont_know` is 0. Timeout, technical failure, omitted response and unpresented items are not 0. Repeated presentations, changing options, learning, fatigue, stochastic guessing or varying contexts violate or complicate the fixed-outcome interpretation; test these in the human pilot rather than calling the design interval total measurement error.

A familiarity yes/no checklist is not the same format as meaning recognition. A separately approved research panel may retain real-word yes/no and nonword yes/no counts with denominators; these are not observations of latent known/unknown truth. No universal false-alarm correction, regression coefficient or zero-FA accuracy guarantee is adopted. Uncalibrated familiarity totals cannot be relabelled as recognized vocabulary.

## 5. Estimands and permitted results

### 5.1 Default response-total profile

`profile_id = baseline-design-v0.1`

`estimand = finite_frame_correct_response_total`

`count_unit = lemma_pos`

`claim_status = diagnostic_only`

Estimate T = Σ y_i over the frozen supported frame using [Sampling](SAMPLING_AND_ESTIMATION_SPEC.md). Public vocabulary claim remains false. `theta`, `vocabulary_count`, `cefr` remain null. Authorized research output may expose `estimate` and its precisely scoped interval; ordinary UI must not call it “words you know.”

The existing CLI labels its internal container `frozen_frame_assessment_unit`. An adapter may produce `count_unit=lemma_pos` only after the frame's unit-review gate passes. An arbitrary list of source rows is insufficient.

### 5.2 Later latent-recognition profile

An expected recognized-unit count under a fitted response/knowledge model is a different estimand with a separately named profile, calibrated parameters, target population, likelihood, identification assumptions, prior/misfit sensitivity and holdout evidence. It cannot inherit “design-unbiased” from the response-total baseline. Guessing/slip adjustment is not enabled by default. The archived Bayesian/Rasch/2PL/3PL designs are research alternatives, not the active V0 scoring engine.

## 6. Uncertainty, stopping and form equivalence

The default interval is `design_confidence`, method `hypergeometric_inversion_bonferroni`, conditional on fixed potential outcomes, frozen screening and valid focused sampling. Its level is set by a registered alpha. It does not automatically include response randomness, key/parameter error, dictionary/frame error, model error, linking, domain transport or device effects.

The focused quota vector is locked before focused responses. No precision-based, stable-point, EVI or RL stopping in this profile. Expiry, abandonment or unsupported item exhaustion produce incomplete evidence, not a shorter valid design. A later sequential profile needs its own estimator, selection probabilities and coverage argument.

Alpha/KR/omega coefficients cannot substitute for interval coverage or an individual vocabulary-count error bound. Alternate-form interchangeability requires preregistered practical-equivalence margins, mean/conditional bias, agreement/dispersion diagnostics and appropriate common-person or linking evidence. High correlation alone is insufficient; a tiny statistically nonzero difference does not automatically fail practical equivalence.

## 7. Claim registry and external labels

Each proposed released interpretation has: `claim_id`, text, estimand, inference type, target population, intended use, supporting evidence, assumptions, rebuttals, reviewer, decision and revalidation triggers. Inference types distinguish domain/evaluation/generalization/explanation/extrapolation/utilization. Record claims orthogonally; do not create a status ladder where scale linking automatically becomes CEFR.

Recruitment labels, cross-construct criterion prediction, same-construct linking and external classification are different evidence uses. CEFR mapping is disabled by default. Enabling it requires an independent quality-characterized external measure, build/validation split, population/ability support, subgroup classification error, uncertainty and separately approved mapping/standard-setting evidence. Shared anchors or correlation do not equate different constructs.

Missing evidence blocks the affected claim, not necessarily every unrelated diagnostic. Unsupported population/domain transport must be visible. Change of source universe, unit/sense policy, item key/format, delivery, scoring/routing, population or intended use triggers scoped re-review and prevents unqualified longitudinal comparison.

## 8. Measurement acceptance

- M01: source rows cannot become frame units without unit/content review and a frozen manifest.
- M02: count unit and estimand agree with Sampling, Scoring and API; baseline never emits latent count, theta or CEFR.
- M03: all frame units have supported approved items; unsupported tails cannot be numerically extrapolated by default.
- M04: yes/no or word-family/MWU formats cannot masquerade as this recognition profile.
- M05: only correct/incorrect/dont_know produce baseline binary outcomes; missing observations block a count.
- M06: interval and stopping claims match the actual design and declared uncertainty scope.
- M07: biased-but-correlated forms fail the registered equivalence criterion; coefficient imports do not pass reliability gates.
- M08: a claim without required population/use/evidence/rebuttal review cannot be released.

No criterion is marked achieved merely by writing this file. [Pilot](PILOT_CALIBRATION_PROTOCOL.md) supplies empirical evidence; [Governance](ARTIFACT_LINEAGE_AND_GOVERNANCE.md) authorizes release.
