# Iteration 69 — Two-phase design-based estimation for a Preply-style vocabulary test

**Direction.** Verify nested phase-I/phase-II inclusion weights, auxiliary calibration, response-dependent routing and nonresponse, and variance estimation; derive an auditable stage-aware estimator that preserves frequency-band representation while using adaptive information targeting.

**Run status.** 6 JSONL records were appended to the state (5 evidence findings and 1 design decision). The four URLs listed below were independently fetched and returned HTTP 200 for the cited endpoints. The Preply URL is an extraction proxy for the vendor methodology page; the direct Preply methodology endpoint returned HTTP 403 in this callback and is not treated as independently verified.

## 1. Evidence verified this iteration

### 1.1 Nested two-phase sampling has two inclusion probabilities

Estevao and Särndal’s Statistics Canada paper defines the nested design as a phase-two sample `s₂` that is a subsample of a phase-one sample `s₁`, with both contained in the finite population `U`. For an item `j`, the phase-I inclusion probability is `π₁ⱼ = P(j ∈ s₁)`. After the realized `s₁` is available, the conditional phase-II inclusion probability is `π₂ⱼ = P(j ∈ s₂ | s₁)`. The corresponding design weights are `a₁ⱼ = 1/π₁ⱼ`, `a₂ⱼ = 1/π₂ⱼ`, and the combined double-expansion weight is `aⱼ = a₁ⱼ·a₂ⱼ`. The paper states that the double-expansion estimator is design-unbiased for a population total under its sampling assumptions.

**Implementation consequence.** An item record must persist both probabilities (or their reproducible sampling seeds and selection rule), the realized route/history that determines `π₂ⱼ`, and the combined weight. A single post-hoc multiplier based only on frequency rank is not an auditable substitute when the second stage depends on the first-stage responses.

Source: Statistics Canada, Estevao & Särndal, *A new face on two-phase sampling with calibration estimators*, HTTP 200: <https://www150.statcan.gc.ca/n1/pub/12-001-x/2009001/article/10880-eng.pdf>.

### 1.2 Calibration can preserve frequency-band population totals

The same Statistics Canada framework distinguishes auxiliary information available at the population, phase-I and phase-II levels. It performs calibration in two stages: phase-I weights can be calibrated to variables with known population totals, and phase-II/final weights can use variables observed in the larger phase-I sample or the smaller phase-II sample, including a phase-I estimate of an otherwise unknown auxiliary total. The final weights are constrained to reproduce the selected auxiliary totals, and the paper describes phase-I and phase-II calibration as a way to reduce variance when the auxiliary variables explain the study variable.

**Application to vocabulary size.** Let `Uₕ` be the declared item universe for frequency band `h`, and let `Mₕ = |Uₕ|` be its known item count. Put a one-hot band indicator into the calibration vector: `xⱼₕ = 1(j ∈ Uₕ)`. The final weights should satisfy, subject to feasibility and bounded-weight checks,

`Σⱼ∈observed wⱼ·xⱼₕ = Mₕ` for every released band `h`.

This makes adaptive targeting a precision mechanism rather than a silent change to the vocabulary universe. Additional predeclared auxiliary variables may cover lexical-unit type, domain or item-format strata, but they must have documented target totals and not be added opportunistically after seeing the respondent’s score.

Source: Statistics Canada, Estevao & Särndal, HTTP 200: <https://www150.statcan.gc.ca/n1/pub/12-001-x/2009001/article/10880-eng.pdf>.

### 1.3 A model-assisted fallback is not the same as a design-unbiased baseline

Merkouris’s Statistics Canada article describes two-phase sampling as a cost-effective design and develops an optimal linear estimator of totals that is also a calibration estimator. It describes one-step alignment of estimates from the combined first- and second-phase samples, and gives generalized-regression calibration as an approximate alternative for general two-phase designs. The article reports theoretical and simulation comparisons, but it does not make a vocabulary-specific claim.

**Implementation consequence.** Use the explicit design-weighted/calibrated estimator as the primary, inspectable baseline. A regression or machine-learning outcome model may be exposed as a model-assisted sensitivity estimate only when its predictors, fit sample, cross-fitting/holdout process and assumptions are recorded. It must not silently replace the design estimator merely because adaptive item selection made the raw sample look informative.

Source: Statistics Canada, Merkouris, *Optimal linear estimation in two-phase sampling*, HTTP 200: <https://www150.statcan.gc.ca/n1/pub/12-001-x/2022002/article/00011-eng.htm>.

### 1.4 Routing changes the sample and creates a comparability obligation

The ETS guide describes a multi-stage test with a first-stage routing test. The routing score selects among easier, medium or harder second-stage forms; the final score aggregates the routing and later stage. It identifies three scoring challenges: the routing result must select an appropriate stage, results across stages must be combined coherently, and examinees taking different second-stage forms must receive comparable scores. It states that equating different form combinations is the direct solution. For item-adaptive tests, ETS separately identifies information efficiency, content balance and item-exposure protection as competing goals; strict content requirements can reduce precision.

**Application to vocabulary size.** A second-stage route may concentrate items near an estimated vocabulary boundary, but the route must retain positive inclusion probability for every band contributing to the declared estimand. Persist `route_id`, the full first-stage history `H₁`, and `q₂(j | H₁, route_id)`. If routes are preassembled modules, calibrate/equate them with common anchors or a demonstrated linking design before comparing their counts. Do not add the raw number-correct scores from harder and easier modules as if they were already on one scale.

Source: ETS, *Practical Considerations in Computer-Based Testing*, HTTP 200: <https://www.ets.org/Media/Research/pdf/CBT-2011.pdf>.

### 1.5 Variance must retain phase-I and phase-II uncertainty

Estevao and Särndal treat the calibrated estimator through residual components associated with the phase-I expansion and the phase-II double expansion. Their discussion uses first- and second-order inclusion probabilities and compares separate-residual and combined-residual variance estimators; the separate-residual approach keeps residual information from the larger phase-I sample instead of discarding it. The paper also reports a simulation supporting the proposed variance procedure.

**Application to a routed test.** The production interval must include the randomness introduced by the broad screen, the conditional second-stage selection, and any response/nonresponse stage. If the route probabilities are analytically tractable, use the appropriate first- and second-order inclusion probabilities or a validated linearization. If the routing rule is complex or changes with a fitted model, use complete-path replicates that resample the stage-I draw, conditional stage-II draw and response process together. Resampling only the final displayed items understates uncertainty because it conditions away the route.

Source: Statistics Canada, Estevao & Särndal, HTTP 200: <https://www150.statcan.gc.ca/n1/pub/12-001-x/2009001/article/10880-eng.pdf>.

### 1.6 What the checked Preply methodology does and does not disclose

The fetched Preply methodology page says that its vocabulary universe contains more than 45,000 frequency-ordered entries. It describes two stages: approximately 40 words spanning easy to hard words, followed by an approximately 120-word narrower range in which the initial items are expected to be known and the final items unknown. It explains a midpoint/cancellation intuition and says that the second-stage sample is distributed logarithmically in rank. It also says that the current survey tests 120 words in the second phase, including first-phase words that fall in the same interval.

The page does **not** disclose item-level phase-I inclusion probabilities, conditional phase-II probabilities, route-history logs, response propensities, calibration weights, pairwise inclusion probabilities, route equating, or an empirical variance procedure. The direct vendor endpoint returned HTTP 403 in this callback; the methodology content was fetched through `r.jina.ai`, HTTP 200. Therefore the product description supports the disclosed two-stage/midpoint facts, but it does not establish that Preply implements a design-based estimator or that its advertised margin covers route and response uncertainty.

Source: Preply methodology page via extraction proxy, HTTP 200: <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works>.

## 2. Proposed estimand and estimator

### 2.1 Declare the finite vocabulary universe first

Let:

- `U` be the versioned set of eligible lexical units in the test manifest;
- `Uₕ` be frequency/content band `h`, with known size `Mₕ`;
- `yⱼ ∈ {0,1}` be the predeclared receptive-knowledge response for item `j` under the chosen item format and sense rule;
- `K = Σⱼ∈U yⱼ = Σₕ Mₕ·pₕ` be the target vocabulary breadth, where `pₕ` is the finite-population proportion known in band `h`.

The item bank manifest must freeze the corpus/dictionary version, lexical-unit ontology, band boundaries, eligibility exclusions and `Mₕ`. The count is conditional on that declared universe; it is not a universal number of all possible English words.

### 2.2 Stage-aware design weights

For an administration, record:

- `π₁ⱼ`: phase-I probability that item `j` enters the broad screen;
- `q₂ⱼ = P(j ∈ s₂ | s₁, H₁)`: conditional phase-II probability under the realized first-stage history and route;
- `ρⱼ`: response/observation probability, if an additional response or completion stage is present;
- `rⱼ`: observed response status, kept distinct from an incorrect answer;
- `H₁`: the first-stage items, responses, omissions and route decision;
- `π₂ⱼ = π₁ⱼ·q₂ⱼ` for selection into the second stage, plus the exact route seed/rule.

If the response mechanism is treated as conditionally ignorable after documented covariates, the initial observed-item weight is

`aⱼ = 1 / (π₁ⱼ·q₂ⱼ·ρⱼ)`.

The `ρⱼ` term must not be inserted without a response model and positivity diagnostics. If no response model has been validated, publish a missingness/quality flag and a sensitivity range rather than coding a missing item as `yⱼ = 0`.

### 2.3 Band-calibrated estimator

Start from `aⱼ` and obtain calibrated final weights `wⱼ` by minimizing a declared distance from `aⱼ`, subject to band totals and any other predeclared auxiliary constraints. The primary estimate is

`K̂_cal = Σⱼ∈observed wⱼ·yⱼ`.

Equivalently, report band estimates `p̂ₕ = (1/Mₕ)·Σⱼ∈observed,h wⱼ·yⱼ` and `K̂_cal = Σₕ Mₕ·p̂ₕ`. Always retain the uncalibrated design estimate, the calibration diagnostics, maximum weight, effective sample size by band and any infeasible/relaxed constraints. A calibration solution with extreme weights is a warning, not proof of accuracy.

If the selection design is simple and all probabilities are known, the non-calibrated baseline is the double-expansion form

`K̂_HT = Σⱼ∈s₂, observed yⱼ / (π₁ⱼ·q₂ⱼ·ρⱼ)`.

For a ratio-style presentation, normalize weights only after the total-count target and band constraints are explicit; otherwise a normalized mean can hide missing mass in sparse or unobserved bands.

## 3. Pseudocode

```text
function estimate_vocab_size(item_manifest, phase1_log, phase2_log, response_log):
    assert manifest_version_is_frozen(item_manifest)
    U_by_band, M = load_declared_band_universe(item_manifest)

    # Stage-aware inclusion and response records
    rows = join_item_histories(phase1_log, phase2_log, response_log)
    for row in rows:
        require row.pi1 > 0
        require row.q2_given_history > 0
        row.base_weight = 1 / row.pi1 / row.q2_given_history
        if row.status == "observed":
            require row.response_propensity > 0 or response_model_is_not_used()
            row.analysis_weight = apply_response_weight_if_validated(row.base_weight, row)
        else:
            row.analysis_weight = null

    observed = rows where status == "observed"
    if not has_positive_support_in_every_released_band(observed, U_by_band):
        return provisional_or_invalid("band positivity failure", sensitivity=null)

    calibrated = calibrate(
        starting_weights = observed.analysis_weight,
        constraints = band_totals(M) + predeclared_auxiliary_totals,
        distance = preregistered_calibration_distance,
        bounds = preregistered_weight_bounds
    )
    if calibrated.infeasible or calibrated.has_extreme_weights:
        return provisional_or_invalid("calibration failure", diagnostics=calibrated.diagnostics)

    K_cal = sum(row.final_weight * row.known_indicator for row in calibrated.rows)
    p_by_band = weighted_band_proportions(calibrated.rows, M)
    K_raw = design_weighted_total(observed)

    # Route-aware uncertainty: do not resample only the final displayed items.
    replicates = complete_path_replicates(
        phase1_design, conditional_phase2_design, response_model,
        preserve_band_constraints=true
    )
    interval = replicate_interval(replicates, statistic=K_cal)
    diagnostics = {
        "K_raw": K_raw,
        "K_cal": K_cal,
        "p_by_band": p_by_band,
        "effective_n_by_band": effective_sample_size_by_band(calibrated.rows),
        "route_ids": distinct_routes(rows),
        "max_weight": max_weight(calibrated.rows),
        "positivity": positivity_report(rows),
        "interval": interval,
    }
    return release_with_status(diagnostics, status=apply_validity_and_equating_gates(diagnostics))
```

The pseudocode is a proposed implementation design, not a claim that Preply uses these fields or methods.

## 4. Uncertainty and release rules

1. **Sampling/route uncertainty.** Include both stages. A route chosen from first-stage responses is part of the design, not fixed background metadata.
2. **Response uncertainty.** Keep `answered-wrong`, `explicit-IDK`, `omitted`, `timeout` and technical missingness separate. Add a response-propensity adjustment only after an independent validation sample supports it.
3. **Calibration/model uncertainty.** Report the design-weighted baseline, calibrated estimate and model-assisted sensitivity separately. Do not collapse model disagreement into a falsely narrow standard error.
4. **Band uncertainty.** Require positive support and a minimum effective sample size in every released band. If a band is unsupported, censor that component or return a provisional status; do not extrapolate silently from the midpoint.
5. **Route comparability.** Different second-stage modules require common anchors or a demonstrated equating design before scores can be compared or used longitudinally.
6. **Replicate coverage.** Validate the complete-path interval by finite-population simulation and a calibration sample with a known or near-census outcome. A mathematically specified interval is not evidence of empirical coverage until this check passes.
7. **Preply comparison.** Preply’s fetched page gives a vendor sampling error calculation of approximately ±10.33% from an assumed standard deviation of 0.25 times vocabulary size, an average of 22.5 sample points and a normal approximation. That disclosed calculation is not evidence of route-aware, response-aware or form-equated coverage because the page does not disclose those components.

## 5. Validation plan

### Phase A — Design and manifest audit

- Freeze `manifest_version`, `U`, each `Uₕ`, `Mₕ`, frequency ranks, lexical-unit rules and exclusions.
- Unit-test that every released band has a positive selection probability under every route.
- Log the probability calculation and random seed for every item; independently replay a sample of sessions.
- Verify that calibration reproduces all declared band totals within tolerance and that no post-response constraint was introduced.

### Phase B — Finite-population simulation

Generate finite item populations with controlled `pₕ` shapes: monotone, band-reversal, domain-shifted and tail-sparse. Simulate a broad phase-I sample, response-dependent routing, conditional phase-II selection and response/nonresponse correlated with knowledge. Compare:

- naive midpoint/log-rank estimate;
- unweighted phase-II proportion;
- HT/double-expansion estimate;
- band-calibrated estimate;
- model-assisted sensitivity estimate.

Report bias, RMSE, empirical interval coverage, interval width, band coverage, maximum weight and effective sample size. Vary route concentration and nonresponse positivity rather than selecting one convenient scenario.

### Phase C — Pilot with a calibration subset

Use a randomized, larger calibration administration in which a subset receives a much broader item sample. Estimate item difficulty and route/response propensities independently of the production estimator. Hold out persons and forms for validation. Compare complete-path replicate intervals with a linearization implementation.

### Phase D — Module/route equating

If the production design uses preassembled easy/medium/hard second-stage modules, include common anchors and test anchor invariance. Estimate route-specific mean differences and conditional SEM; block longitudinal or cross-route comparisons until equating and holdout checks pass.

### Phase E — Monitoring

Monitor positivity, weight dispersion, band effective sample size, route frequency, response rates, calibration residuals and interval coverage by manifest version. A route or item with inadequate support enters a provisional/maintenance queue; it is not corrected by an arbitrary multiplier.

## 6. Comparison table

| Dimension | Preply methodology disclosed in fetched page | Proposed stage-aware design |
|---|---|---|
| Vocabulary universe | More than 45,000 frequency-ordered entries; vendor dictionary/corpus choices are described | Versioned `U`, explicit lexical-unit rules, band membership and `Mₕ` manifest |
| Stage 1 | About 40 words from easy to hard to locate a general level | Probability sample or auditable routing screen with `π₁ⱼ`, response status and history |
| Stage 2 | About 120 words in a narrower frequency range; logarithmic rank spacing; phase-I overlap may count | Conditional randomized/module selection with recorded `q₂(j | H₁, route)` and positive band support |
| Point estimate | Midpoint/cancellation explanation with logarithmic-spacing caveat | HT/double-expansion baseline plus band-total calibration; report `K_raw` and `K_cal` |
| Adaptive information | Narrowing is described, but the checked page does not disclose route probabilities or selection logs | Information targeting is allowed only inside declared design/content constraints and with route probabilities |
| Band representation | No item-level probability or band-calibration table disclosed | Constrain final weights to `Σ wⱼ·1(hⱼ=h)=Mₕ`; publish feasibility/weight diagnostics |
| Response/missingness | No response-propensity or missingness model disclosed on the checked page | Separate missing statuses; model `ρⱼ` only after validation; never score missing as wrong by default |
| Cross-route comparability | No common-anchor or route-equating evidence disclosed | Common anchors/equating and conditional SEM are release gates |
| Error interval | Vendor calculation based on an assumed SD, sample count and normal approximation; page states roughly ±10.33% | Complete-path design/model/response interval validated by simulation and calibration data |
| Auditability | Product-level methodology narrative; direct endpoint was HTTP 403 in this callback | Persist manifest, probabilities, seeds, route history, calibration weights and replicate recipe |

## 7. Gaps and status

- **Product-specific gap:** The checked Preply methodology does not disclose `π₁`, conditional `q₂`, response propensities, calibration weights, pairwise inclusion probabilities, route-equating evidence or complete-path variance estimation. `chưa tìm được nguồn xác thực cho ý này` as a claim about whether hidden production controls exist; the public page alone cannot establish their presence or absence.
- **Vocabulary-specific calibration gap:** Statistics Canada and ETS provide general two-phase/adaptive design principles, not a validated vocabulary-size coefficient, threshold or Preply conversion. No item-level response pilot is available here to select a route model, calibration distance, minimum positivity threshold or interval method.
- **Operational gap:** A production implementation still needs a frozen item manifest, declared band totals, route probability logger, response-status schema and a finite-population simulation/holdout study before presenting an individual estimate as validated.

## 8. Traceability to state

The six appended records are:

- `nested_two_phase_inclusion_weights`
- `frequency_band_calibration_constraints`
- `optimal_linear_calibration_fallback`
- `response_dependent_routing_is_design_data`
- `separate_residual_variance_for_nested_test`
- `stage_aware_vocab_estimator_and_nonresponse_gap`

All six were validated as JSON objects after append; the findings file grew from 429 to 435 valid lines. The corresponding source statuses recorded during this iteration were: Statistics Canada 2009 PDF — HTTP 200; Statistics Canada 2022 article — HTTP 200; ETS CBT guide — HTTP 200; Preply methodology extraction proxy — HTTP 200. The direct Preply methodology URL returned HTTP 403 and was not cited as a verified page.
