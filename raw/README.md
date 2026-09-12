# Vocabulary-size test algorithm — research archive

> Historical research, not the active implementation contract. Use the [harmonized P0 suite](../docs/specs/README.md) and [current source-data status](../docs/data/SERVER_DICTIONARY_STATUS.md). Old progress counters, Advisor approvals and data-scope statements below describe their historical snapshots.

## Newly incorporated research and prior specs

Files 66–75 (actual iterations 63–72) are indexed in the [research incorporation matrix](../docs/specs/RESEARCH_INCORPORATION.md), with links to every file and the decision applied to active specs. The [superseded seven-spec suite and roadmap](specs-before-harmonization/README.md) are preserved byte-for-byte with a hash manifest.

## Historical learning-snapshot integration

The owner-supplied `english_optimized.db` has now been audited locally: **3,885 source rows**, all unique after the documented headword normalization; **3,848 (99.0476%)** have lexical candidates in pinned Open English WordNet 2025. This does **not** confirm target-sense agreement, a reviewed lemma-POS frame, or the approximately 44,000-item full-library scope. **3,798 explanations contain their target headword**, requiring separate assessment authoring rather than automatic reuse as definition-to-word questions.

- [Actual snapshot audit and revised implementation gates](../docs/data/LAZZYBEE_SNAPSHOT_AUDIT.md)
- [Machine-readable aggregate evidence](../docs/data/snapshot-audit.json)
- [Executable offline audit, mapping, profiling and baseline tools](../tools/lazzybee/README.md)

Raw database/content and record-level mappings remain private. Existing corpus-size targets and calibration requirements below are design/history, not evidence that this snapshot already satisfies them.

> 🎯 **For Implementation & Production Architecture:** See [ROADMAP_ARCHITECTURE.md](../ROADMAP_ARCHITECTURE.md) for the executive blueprint, system architecture, decoupled modules, and team roadmap approved by the Strategic Advisor.

Báo cáo được cập nhật theo từng iteration của Deli Deep. Các claim có nguồn được kiểm tra theo từng artifact; riêng trang Preply trong callback này vẫn có endpoint trả HTTP 403 nên các phần chưa xác minh được giữ dưới dạng gap. Phương pháp Preply được đối chiếu qua bản proxy khi fetch được và luôn được ghi rõ là nguồn vendor/provisional khi chưa có calibration độc lập.

| # | Chủ đề | File |
|---:|---|---|
| 1 | Tóm tắt điều hành | [01-executive-summary.md](01-executive-summary.md) |
| 2 | Bằng chứng và đối chiếu nguồn | [02-evidence-and-comparison.md](02-evidence-and-comparison.md) |
| 3 | Thuật toán đề xuất, công thức, pseudocode | [03-proposed-algorithm.md](03-proposed-algorithm.md) |
| 4 | Độ không chắc chắn, assumptions và kế hoạch validation | [04-uncertainty-validation-gaps.md](04-uncertainty-validation-gaps.md) |
| 5 | Iteration 2: IRT/CAT, calibration và repeat-form equating | [05-irt-cat-iteration-2.md](05-irt-cat-iteration-2.md) |
| 6 | Iteration 3: criterion validity, predictive validity và guessing bias | [06-criterion-validity-iteration-3.md](06-criterion-validity-iteration-3.md) |
| 7 | Iteration 4: sampling precision, test length và item independence | [07-sampling-precision-iteration-4.md](07-sampling-precision-iteration-4.md) |
| 8 | Iteration 5: estimand reconciliation và deployment calibration | [08-estimand-calibration-iteration-5.md](08-estimand-calibration-iteration-5.md) |
| 9 | Iteration 6: measurement invariance, fairness và transportability theo nhóm | [09-measurement-invariance-fairness-iteration-6.md](09-measurement-invariance-fairness-iteration-6.md) |
| 10 | Iteration 7: temporal reliability, alternate forms và retest | [10-temporal-reliability-retest-iteration-7.md](10-temporal-reliability-retest-iteration-7.md) |
| 11 | Iteration 8: response-process, latency và online quality control | [11-response-process-online-qc-iteration-8.md](11-response-process-online-qc-iteration-8.md) |
| 12 | Iteration 9: context facets, partial knowledge và score linking | [12-context-facets-partial-knowledge-iteration-9.md](12-context-facets-partial-knowledge-iteration-9.md) |
| 13 | Iteration 10: domain alignment, covariate shift và TLU estimates | [13-domain-alignment-covariate-shift-iteration-10.md](13-domain-alignment-covariate-shift-iteration-10.md) |
| 14 | Iteration 11: design-based weighting, replicate uncertainty và calibration | [14-design-weighting-uncertainty-iteration-11.md](14-design-weighting-uncertainty-iteration-11.md) |
| 15 | Iteration 12: item-bank security, exposure và repeated-attempt contamination | [15-item-bank-security-exposure-iteration-12.md](15-item-bank-security-exposure-iteration-12.md) |
| 16 | Iteration 13: lexical unit, polysemy và semantic-facet calibration | [16-lexical-unit-polysemy-semantic-facets-iteration-13.md](16-lexical-unit-polysemy-semantic-facets-iteration-13.md) |
| 17 | Iteration 14: distractor và option-function calibration | [17-distractor-option-function-iteration-14.md](17-distractor-option-function-iteration-14.md) |
| 18 | Iteration 15: equating, criterion linking và calibration ngoài | [18-equating-criterion-calibration-iteration-15.md](18-equating-criterion-calibration-iteration-15.md) |
| 19 | Iteration 16: incomplete responses, response status và calibration missingness | [19-incomplete-response-status-calibration-iteration-16.md](19-incomplete-response-status-calibration-iteration-16.md) |
| 20 | Iteration 17: corpus-version drift và domain-coverage calibration | [20-corpus-version-domain-coverage-iteration-17.md](20-corpus-version-domain-coverage-iteration-17.md) |
| 21 | Iteration 18: breadth–depth, graded word knowledge và strength calibration | [21-breadth-depth-strength-calibration-iteration-18.md](21-breadth-depth-strength-calibration-iteration-18.md) |
| 22 | Iteration 19: modality và delivery-mode invariance | [22-modality-delivery-invariance-iteration-19.md](22-modality-delivery-invariance-iteration-19.md) |
| 23 | Iteration 20: local dependence và clustered-item sampling | [23-local-dependence-clustered-sampling-iteration-20.md](23-local-dependence-clustered-sampling-iteration-20.md) |
| 24 | Iteration 21: Bayesian posterior, posterior-predictive checks và calibration | [24-bayesian-posterior-predictive-calibration-iteration-21.md](24-bayesian-posterior-predictive-calibration-iteration-21.md) |
| 25 | Iteration 22: latent response-model robustness, mastery và guessing | [25-latent-response-model-robustness-iteration-22.md](25-latent-response-model-robustness-iteration-22.md) |
| 26 | Iteration 23: use-case, task coverage và diễn giải điểm số | [26-use-case-task-coverage-interpretation-iteration-23.md](26-use-case-task-coverage-interpretation-iteration-23.md) |
| 27 | Iteration 24: tail coverage, censoring và thiết kế điểm cực trị | [27-tail-coverage-censoring-extreme-score-design-iteration-24.md](27-tail-coverage-censoring-extreme-score-design-iteration-24.md) |
| 28 | Iteration 25: sequential stopping, confidence sequences và phân bổ ngân sách | [28-sequential-stopping-confidence-sequences-iteration-25.md](28-sequential-stopping-confidence-sequences-iteration-25.md) |
| 29 | Iteration 26: cognitive-diagnostic profiles, lexical attributes và Q-matrix validation | [29-cognitive-diagnostic-qmatrix-profiles-iteration-26.md](29-cognitive-diagnostic-qmatrix-profiles-iteration-26.md) |
| 30 | Iteration 27: Generalizability Theory, D-study và lắp ráp test | [30-generalizability-dstudy-test-assembly-iteration-27.md](30-generalizability-dstudy-test-assembly-iteration-27.md) |
| 31 | Iteration 28: low-stakes effort, satisficing và context thiết bị | [31-low-stakes-online-effort-context-iteration-28.md](31-low-stakes-online-effort-context-iteration-28.md) |
| 32 | Iteration 29: multistage routing, module assembly và routing-error robustness | [32-multistage-routing-module-assembly-iteration-29.md](32-multistage-routing-module-assembly-iteration-29.md) |
| 33 | Iteration 30: partial credit, VKS và ngưỡng mastery | [33-polytomous-partial-credit-vks-iteration-30.md](33-polytomous-partial-credit-vks-iteration-30.md) |
| 34 | Iteration 31: token/type estimands và domain token coverage | [34-token-type-domain-coverage-iteration-31.md](34-token-type-domain-coverage-iteration-31.md) |
| 35 | Iteration 32: frequency metric, contextual diversity và rank uncertainty | [35-frequency-metric-dispersion-rank-uncertainty-iteration-32.md](35-frequency-metric-dispersion-rank-uncertainty-iteration-32.md) |
| 36 | Iteration 33: norming, reference population và score reporting | [36-norming-reference-population-score-reporting-iteration-33.md](36-norming-reference-population-score-reporting-iteration-33.md) |
| 37 | Iteration 34: measurement error, CSEM và reporting interval | [37-measurement-error-csem-reporting-iteration-34.md](37-measurement-error-csem-reporting-iteration-34.md) |
| 38 | Iteration 35: content-validity blueprinting và expert review | [38-content-validity-blueprinting-expert-review-iteration-35.md](38-content-validity-blueprinting-expert-review-iteration-35.md) |
| 39 | Iteration 36: unseen-vocabulary estimators và tail extrapolation | [39-unseen-vocabulary-extrapolation-iteration-36.md](39-unseen-vocabulary-extrapolation-iteration-36.md) |
| 40 | Iteration 37: cognate/loanword effects và cross-language calibration | [40-cognate-loanword-cross-language-calibration-iteration-37.md](40-cognate-loanword-cross-language-calibration-iteration-37.md) |
| 41 | Iteration 38: confidence và response-format calibration | [41-confidence-response-format-calibration-iteration-38.md](41-confidence-response-format-calibration-iteration-38.md) |
| 42 | Iteration 39: reproducibility, simulation và validation của thuật toán | [42-reproducibility-simulation-validation-iteration-39.md](42-reproducibility-simulation-validation-iteration-39.md) |
| 43 | Iteration 40: criterion-referenced mastery và standard setting | [43-criterion-mastery-standard-setting-iteration-40.md](43-criterion-mastery-standard-setting-iteration-40.md) |
| 44 | Iteration 41: dimensionality và construct separation | [44-dimensionality-construct-separation-iteration-41.md](44-dimensionality-construct-separation-iteration-41.md) |
| 45 | Iteration 42: construct-irrelevant language burden và cue control | [45-construct-irrelevant-language-burden-cue-control-iteration-42.md](45-construct-irrelevant-language-burden-cue-control-iteration-42.md) |
| 46 | Iteration 43: sparse-band/subgroup calibration và partial pooling | [46-sparse-band-subgroup-partial-pooling-iteration-43.md](46-sparse-band-subgroup-partial-pooling-iteration-43.md) |
| 47 | Iteration 44: item-bank lifecycle, pretest, retirement và parameter drift | [47-item-bank-lifecycle-parameter-drift-maintenance-iteration-44.md](47-item-bank-lifecycle-parameter-drift-maintenance-iteration-44.md) |
| 48 | Iteration 45: speededness, timed/untimed measures và time-policy | [48-speededness-timed-untimed-time-policy-iteration-45.md](48-speededness-timed-untimed-time-policy-iteration-45.md) |
| 49 | Iteration 46: psycholinguistic item features và residual difficulty calibration | [49-psycholinguistic-item-features-residual-calibration-iteration-46.md](49-psycholinguistic-item-features-residual-calibration-iteration-46.md) |
| 50 | Iteration 47: selection bias, reference population và calibration weighting | [50-reference-population-selection-weighting-iteration-47.md](50-reference-population-selection-weighting-iteration-47.md) |
| 51 | Iteration 48: morphological transparency và word-family estimand | [51-morphological-transparency-family-estimand-iteration-48.md](51-morphological-transparency-family-estimand-iteration-48.md) |
| 52 | Iteration 49: nonparametric IRT/Mokken và QA item bank | [52-nonparametric-irt-mokken-item-bank-qa-iteration-49.md](52-nonparametric-irt-mokken-item-bank-qa-iteration-49.md) |
| 53 | Iteration 50: cross-lingual adaptation và localized-form calibration | [53-cross-lingual-adaptation-localized-calibration-iteration-50.md](53-cross-lingual-adaptation-localized-calibration-iteration-50.md) |
| 54 | Iteration 51: black-box audit VST tham chiếu và giới hạn đối chiếu Preply | [54-black-box-reference-vst-preply-audit-iteration-51.md](54-black-box-reference-vst-preply-audit-iteration-51.md) |
| 55 | Iteration 52: option-position, distractor-order và randomization | [55-option-position-distractor-order-randomization-iteration-52.md](55-option-position-distractor-order-randomization-iteration-52.md) |
| 56 | Iteration 53: planned-missing matrix sampling và booklet design | [56-planned-missing-matrix-sampling-booklet-design-iteration-53.md](56-planned-missing-matrix-sampling-booklet-design-iteration-53.md) |
| 57 | Iteration 54: accessibility, accommodations và invariance | [57-accessibility-accommodation-invariance-iteration-54.md](57-accessibility-accommodation-invariance-iteration-54.md) |
| 58 | Iteration 55: word prevalence và calibration difficulty theo quần thể | [58-word-prevalence-population-conditioned-calibration-iteration-55.md](58-word-prevalence-population-conditioned-calibration-iteration-55.md) |
| 59 | Iteration 56: Bayesian calibration và phân rã uncertainty cho short forms | [59-bayesian-calibration-uncertainty-decomposition-iteration-56.md](59-bayesian-calibration-uncertainty-decomposition-iteration-56.md) |
| 60 | Iteration 57: content-constrained adaptive selection và shadow-test assembly | [60-content-constrained-shadow-test-iteration-57.md](60-content-constrained-shadow-test-iteration-57.md) |
| 61 | Iteration 58: joint response-accuracy/response-time và rapid-guessing robustness | [61-joint-response-time-rapid-guessing-iteration-58.md](61-joint-response-time-rapid-guessing-iteration-58.md) |
| 62 | Iteration 59: lexical-unit ontology, multiword units và phrase-aware diagnostics | [62-lexical-unit-mwu-diagnostics-iteration-59.md](62-lexical-unit-mwu-diagnostics-iteration-59.md) |
| 63 | Iteration 60: automated item generation, LLM distractors và QA psychometric | [63-automated-item-generation-llm-distractor-qa-iteration-60.md](63-automated-item-generation-llm-distractor-qa-iteration-60.md) |
| 64 | Iteration 61: dialect/register và transportability của World Englishes | [64-dialect-register-world-english-transport-iteration-61.md](64-dialect-register-world-english-transport-iteration-61.md) |
| 65 | Iteration 62: longitudinal growth, common-anchor equating và reliable change | [65-longitudinal-growth-reliable-change-iteration-62.md](65-longitudinal-growth-reliable-change-iteration-62.md) |

## Trạng thái

- Iteration hiện tại: 62
- Findings đã append: 388 dòng JSONL hợp lệ
- Direction mới nhất: Longitudinal change and reliable-growth interpretation — common-item/form equating, practice effects, time/position facets và reliable-change decision layer.
- Kết luận mới: Akase dùng VST 4 làm linking form để đặt bốn form lên một Rasch logit scale; Holster & Lake cho thấy Time và Position có thể là measurement facets; RCI chỉ là decision aid phụ thuộc reliability/reference assumptions, không phải hệ số đổi sang số từ.
- Bổ sung iteration 62: artifact `65-longitudinal-growth-reliable-change-iteration-62.md` chứa 5 nguồn HTTP 200, thuật toán longitudinal, pseudocode, công thức `Delta_K`/`SE_Delta`/`MDC95`, decision labels, bảng so sánh Preply và validation plan. Preply endpoint trả HTTP 403 nên chưa xác minh alternate forms, anchors, retest reliability, practice-effect study hoặc reliable-change reporting.
- Bổ sung iteration 59: artifact `62-lexical-unit-mwu-diagnostics-iteration-59.md` chứa 4 nguồn HTTP 200, data model `MWU_profile`, pseudocode, công thức coverage, uncertainty, release gates và bảng đối chiếu Preply. Preply endpoint trả HTTP 403; chưa xác minh MWU implementation.
- Bổ sung iteration 58: artifact `61-joint-response-time-rapid-guessing-iteration-58.md` chứa 4 nguồn HTTP 200, công thức `K_main`/`K_sens`, pseudocode, quy tắc release và bảng đối chiếu Preply. Preply endpoint trả HTTP 403; chưa xác minh RT logging, rapid-guess policy hoặc joint scoring.
- Bổ sung iteration 57: artifact `60-content-constrained-shadow-test-iteration-57.md` chứa 4 nguồn HTTP 200, pseudocode shadow assembly, objective/constraint formulas, K-estimator, bảng so sánh Preply và validation plan. Preply endpoint trả HTTP 403; chưa xác minh current item bank, routing, shadow solver hoặc exposure controls.
- Bổ sung iteration 56: artifact `59-bayesian-calibration-uncertainty-decomposition-iteration-56.md` chứa 5 nguồn HTTP 200, evidence Bayesian vocabulary/SEM/IRT/CAT, pseudocode, công thức posterior count, release gates, bảng so sánh Preply và validation plan. Preply current endpoint trả HTTP 403; chưa xác minh current item bank, routing, calibration hoặc uncertainty implementation.
- Bổ sung iteration 55: artifact `58-word-prevalence-population-conditioned-calibration-iteration-55.md` chứa các nguồn Springer/Frontiers/UGent HTTP 200, evidence về prevalence norms và crowdsourced sampling, schema metadata, công thức, pseudocode, bảng so sánh Preply và validation plan. Prevalence policy, reference population và calibration response-level hiện tại của Preply vẫn chưa xác minh.
- Bổ sung iteration 53: artifact `56-planned-missing-matrix-sampling-booklet-design-iteration-53.md` chứa nguồn HTTP 200, findings về BIBD/PBIBD, simulation item-count/SE, planned missingness, pseudocode form/scoring, bảng so sánh Preply và validation plan. Preply item assignment, missingness, anchors, weights và IRT vẫn chưa xác minh.
- Kết luận mới: Lextutor VST live có 14 band × 10 item = 140 item, fixed-form 4-choice; JavaScript tính `vocab_size = total_correct × 100` (0–14.000), không dùng IRT và không correction guessing. Answer key/client scoring bị expose nên chỉ phù hợp diagnostic practice nếu không có server-side controls. Read (2007) xác nhận MCQ VST và Yes/No là các construct/response process khác nhau, không được chuyển correction coefficient giữa hai format.
- Bổ sung iteration 51: artifact `54-black-box-reference-vst-preply-audit-iteration-51.md` chứa kiểm đếm HTML/JS, công thức scoring, security/retest implications, pseudocode audit gate, bảng so sánh và nguồn HTTP 200. Preply endpoints và proxy đều HTTP 403 trong callback; chưa tìm được nguồn xác thực cho current item pool/scoring/security của Preply.
- Kết luận mới: ITC yêu cầu đánh giá construct overlap, linguistic/psychological review, item equivalence và validity riêng theo population; item không tương đương không được lập common scale. Park (2024) cho thấy Korean bilingual VST có thể quá dễ và BNC frequency order lệch trong EFL context; Aizawa (2024) đo chênh lệch loanword/option rất lớn. Localized form phải calibration riêng và chỉ link với English/Preply khi anchors/invariance/hold-out pass.
- Bổ sung iteration 50: artifact `53-cross-lingual-adaptation-localized-calibration-iteration-50.md` chứa nguồn ITC và các nghiên cứu bilingual VST/PPVT đã fetch HTTP 200, data model, release gates, pseudocode, scoring/uncertainty, bảng so sánh Preply và validation plan. Chưa có response-level/item-bank data của Preply để xác minh workflow localized, DIF, anchors hoặc loanword policy.
- Direction trước: selection bias và transportability của mẫu online — tách measurement precision khỏi population-representativeness uncertainty, kiểm tra common support và chỉ dùng weighting khi có auxiliary variables/reference data phù hợp.
- Kết luận trước: AAPOR và OPRE/Brick cảnh báo self-selection/opt-in bias không được xóa chỉ bằng quota; propensity/raking/post-stratification cần giả định mạnh, outcome-relevant auxiliaries và positivity. Margin of error có điều kiện trên model không bao gồm systematic selection bias/meta-uncertainty.
- Bổ sung iteration 47: artifact `50-reference-population-selection-weighting-iteration-47.md` chứa evidence HTTP 200, pseudocode reporting layer, schema biến population, công thức UWE/n_eff, so sánh Preply, assumptions và validation plan. Preply proxy methodology vẫn không công khai sampling frame, respondent population, weighting hay norming protocol.
- Direction trước: psycholinguistic item features và residual difficulty calibration — tách frequency rank khỏi item difficulty, kiểm tra length/syllable/neighborhood effects, và dùng covariate-balanced pretest/residual IRT thay vì correction coefficient cố định.
- Kết luận trước: VAST/COCA của Hashimoto báo cáo frequency rank chỉ giải thích 22.5% phương sai item difficulty trong 501 item đầu, giảm còn R²=9.4% khi gom band 1.000 từ. Koirala cho thấy length/syllable/consonant clusters không còn hiệu ứng rõ trong sample khi kiểm soát frequency; Yap và cộng sự cho thấy feature của pseudoword ảnh hưởng RT nên pseudoword controls phải được match/calibrate.
- Bổ sung iteration 46: artifact `49-psycholinguistic-item-features-residual-calibration-iteration-46.md` chứa evidence, item manifest, mô hình residual, pseudocode, assumptions, validation plan và bảng đối chiếu Preply. Preply proxy methodology vẫn chỉ công khai frequency-ranked dictionary, sampling midpoint/log spacing và không công khai feature calibration.

- Kết luận mới: frequency rank phụ thuộc corpus design, register, sampling frame và version; contextual diversity có thể bổ sung signal cho raw frequency nhưng bằng chứng hiện tại là task/ngôn ngữ cụ thể, không phải hệ số vocabulary-size phổ quát. Zipf chỉ là log transform; tail counts vẫn có uncertainty. Item bank nên lưu raw count, document count, corpus metadata, Zipf, rank interval, low-count flag và sensitivity qua các manifest.
- Bổ sung iteration 32: artifact `35-frequency-metric-dispersion-rank-uncertainty-iteration-32.md` chứa bằng chứng BNC/SUBTLEX/wordfreq, frequency manifest, pseudocode, công thức uncertainty tách response CI khỏi rank sensitivity, bảng so sánh Preply và validation plan. Preply production dispersion metric, rank uncertainty và update protocol vẫn chưa xác minh.
- Còn thiếu: item bank hiện tại của Preply, response-level production data, selection probabilities/routing log, exposure/overlap metrics, dữ liệu pilot độc lập để ước lượng độ khó/IRT, information curve, context/distractor facets, DIF, guessing thresholds, test–retest/practice effects, common-anchor stability, mapping headword↔lemma/word-family, sense-level annotations, format linking, latency/device calibration, domain weighting của Preply, security thresholds, depth/strength layer, paper/digital mode-equating, cluster/context metadata, Q-matrix, design effect, prior/model sensitivity, endpoint interval coverage, tail routing và low-effort calibration trên quần thể mục tiêu. Chưa có common-anchor data hoặc calibration/hold-out sample để linking vocab breadth/depth/listening với CEFR/IELTS; các ngưỡng transition, tail cutoff, anchor count, drift, cut score, completion gate, missingness gate, Not Sure, mode effect, dependency, PPC calibration, response-propensity và RTE/rapid-guess gate vẫn chưa được calibration.
- Bổ sung iteration 28: không có nguồn xác thực cho một công thức phổ quát biến effort signal thành số từ điều chỉnh. `effort_adjusted_count` phải để null cho tới khi pilot/hold-out chứng minh correction và coverage; tách `CI_sampling_or_response`, `CI_model`, `effort_sensitivity_range` và `context_sensitivity_range`.
- Bổ sung iteration 27: chưa có Preply variance components, routing probabilities, form/occasion overlap hoặc D-study/hold-out data để chọn Phi/G, band quota, item budget, anchor rate hay margin of error. Các kết quả Kumazawa (`Phi=.30/.41/.51`) chỉ thuộc một classroom criterion test; chưa tìm được nguồn xác thực cho dependability hoặc precision riêng của Preply.
- Bổ sung iteration 26: chưa có Preply Q-matrix, item bank, response-level data hoặc calibration sample để xác minh lexical subskills, CDM model, posterior thresholds, classification coverage và mapping profile→word count. Ngưỡng `p_mastery`, entropy và số item diagnostic phải được pilot-calibrate; chưa tìm được nguồn xác thực cho ngưỡng production chung.
- Bổ sung iteration 25: chưa có coverage-calibrated Bernoulli/finite-population confidence sequence cụ thể cho vocabulary bank; chưa có dữ liệu để chọn `δ`, `n_min`, `hard_max`, expected-gain tolerance hoặc chứng minh coverage dưới adaptive inclusion probability. Các tham số PSER từ PROMIS không được chuyển nguyên sang vocabulary.

## Nguồn bổ sung ở iteration 2

- Fokin, Płużyczka & Golovin (2025), *The Polish Vocabulary Size Test* (PDF, HTTP 200): [arXiv PDF](https://arxiv.org/pdf/2507.19869)
- Akase (2022), *Longitudinal measurement of growth in vocabulary size using Rasch-based test equating* (PDF, HTTP 200): [bản PDF](https://d-nb.info/1257528165/34)
