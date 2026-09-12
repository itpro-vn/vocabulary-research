# Iteration 71 — Calibration-error-aware adaptive estimation và decision-stable stopping

## Phạm vi và kết luận ngắn

Iteration này tập trung vào một nguồn sai số thường bị ẩn trong CAT: **tham số item đã calibration không phải là sự thật cố định**. Khi thuật toán dùng `a_hat`, `b_hat` như giá trị chính xác, nó có thể vừa chọn sai item vừa báo `SE` quá hẹp. Hướng mới của iteration là ghép ba lớp:

1. uncertainty của item bank (`phi = {a_i, b_i, covariance/posterior}`);
2. uncertainty của người làm và route/sampling;
3. loss/cost của quyết định hoặc báo cáo thêm một item.

Khuyến nghị: vẫn giữ `K_hat` theo vocabulary universe/band đã khai báo, nhưng mỗi phiên bản item bank phải có **calibration draws** hoặc bootstrap replicate. Adaptive selection và interval phải được đánh giá trên các draw này. Dừng khi đồng thời đạt precision mục tiêu, decision/report đủ ổn định và expected value của item tiếp theo không còn bù được chi phí; các ngưỡng phải được pilot-calibrate, không lấy một ngưỡng CAT hay margin Preply làm hằng số phổ quát.

## 1. Nguồn đã fetch và verify

| Nguồn | HTTP | Bằng chứng dùng trong iteration | Giới hạn chuyển giao |
|---|---:|---|---|
| [Fink & König, *Accounting for item calibration error in computerized adaptive testing*](https://pmc.ncbi.nlm.nih.gov/articles/PMC11947018/) | 200 | Nêu rõ item parameters thường bị coi là fixed; calibration error làm SE thấp giả tạo, gây bias/MSE, đặc biệt ở extreme ability. Mô phỏng 2PL so sánh cWLE, cWLE+BMI và fully Bayesian. | Mô phỏng CAT tổng quát, không phải vocabulary-size test; bài giả định 2PL và cần kiểm tra item misfit/format vocabulary riêng. |
| [Şahin & Weiss, *Effects of Calibration Sample Size and Item Bank Size on Examinee Ability Estimation in CAT*](https://files.eric.ed.gov/fulltext/EJ1101283.pdf) | 200 | Mô phỏng 3PL với calibration sample 150–5.000 và bank 100–500; bank information coverage tại vùng ability quan trọng hơn việc chỉ tăng sample khi bank thiếu information. | Kết quả phụ thuộc simulated bank/model; “150” và “200 item” không phải production threshold. |
| [*Optimal Item Calibration for Computerized Achievement Tests*, Psychometrika](https://link.springer.com/article/10.1007/s11336-019-09673-6) | 200 | Optimal restricted design cho calibration khi không thể chọn examinee ở ability điểm lý tưởng; abstract nói lấy mẫu ngây thơ quanh unrestricted design points là không tối ưu. | Optimal design dựa trên IRT và giả định/model; cần chuyển thành thiết kế khả thi cho vocabulary bands. |
| [Veldkamp & Matteucci, *Bayesian Computerized Adaptive Testing*](https://www.redalyc.org/pdf/3995/399538144004.pdf) | 200 | Review chi phí CAT: rút ngắn test làm giảm information/tăng error; giảm writing/pretest/calibration làm tăng uncertainty item quality. Empirical priors và linked designs là các cách giảm cost cần kiểm soát. | Review và ví dụ CAT, không chứng minh prior nào đúng cho vocabulary bank hay Preply. |
| [ETS, *Practical Considerations in Computer-Based Testing*](https://www.ets.org/Media/Research/pdf/CBT-2011.pdf) | 200 | CAT lặp chọn item/cập nhật score và dừng theo fixed length hoặc precision; design phải tùy content, format, population và giá trị của score user. | Hướng dẫn tổng quát; không đưa loss/cost hay threshold cho vocabulary size. |
| [Li, Gibbons & Ročková, *Deep Computerized Adaptive Testing*](https://arxiv.org/pdf/2502.19275) | 200 | Preprint 2026 chỉ ra one-step information selection có thể myopic; Q-learning mô phỏng reward cho posterior-variance reduction/early termination. | Preprint, 5 latent factors và simulation; không chuyển số item/ngưỡng sang vocabulary. |

Các URL trên được fetch bằng browser UA; status thực tế ghi nhận là HTTP 200. Web extraction backend không dùng được trong callback vì trả lỗi “search-only backend”; nội dung được lấy qua `curl`/PDF extraction. Lead EVTI của Springer chỉ trả challenge page và ResearchGate trả 403 nên không được dùng như bằng chứng.

## 2. Bằng chứng và diễn giải

### 2.1 Calibration error ảnh hưởng cả estimation và item selection

Fink–König mô tả hai điểm hỏng riêng:

- `theta_hat` sau mỗi response dùng item parameters ước lượng, nên uncertainty của item đi vào provisional ability;
- item tiếp theo cũng được chọn bằng những parameters đó, nên sai số selection làm thay đổi toàn bộ đường đi của test.

Trong 2PL, bài viết ghi item information là:

```text
P_i(theta) = logistic(a_i * theta - b_i)
I_i(theta) = a_i^2 * P_i(theta) * (1 - P_i(theta))
```

Vì `a_i` xuất hiện bình phương, maximum-Fisher-information với point estimates có thể ưu tiên item có `a_hat` cao do sai số dương. Đây là “capitalization on calibration error”, không chỉ là một SE nhỏ hơn thực tế. Bài báo ghi rằng bỏ qua calibration error có thể làm bias tới khoảng `0.3 SD` theta trong các nghiên cứu được thảo luận; trong mô phỏng của chính bài, trường hợp cực đoan có bias tới khoảng `40%` độ lệch chuẩn của calibration sample.

**Hệ quả cho vocabulary:** nếu item khó/dễ được dùng để định vị boundary số từ, một item parameter bị lệch có thể làm route đi sang band sai. Vì thế uncertainty phải được truyền qua cả `select -> response -> update -> select`, không chỉ thêm một `SE_item` vào cuối.

### 2.2 Fully Bayesian/parameter draws là pattern phù hợp, nhưng chưa tự động thành count estimator

Bài Fink–König resample item parameters từ posterior calibration draws khi cập nhật Bayesian CAT; trong mô phỏng, fully Bayesian có mức giảm bias cực đoan lớn hơn cWLE và cWLE+BMI. Tác giả nhấn mạnh fully Bayesian phức tạp hơn và mô phỏng còn giới hạn ở 2PL.

Điều có thể chuyển sang hệ thống vocabulary là **cách biểu diễn uncertainty**, không phải các con số hiệu năng:

```text
phi^(m) ~ p(phi | calibration_data)
D^(m)   = learner responses + route/sampling path under phi^(m)
K_hat^(m) = run_count_estimator(D^(m), phi^(m), manifest)
```

`K_hat^(m)` phải còn giữ `M_h`, lexical-unit definition, design weights và band constraints. Không được xem `theta` là số từ; transform từ latent ability sang `p_h`/count phải được calibration độc lập.

### 2.3 Calibration sample không thay thế cho bank coverage

Şahin–Weiss mô phỏng 3PL với nhiều calibration sample và bank size. Kết luận quan trọng không phải “150 đủ”, mà là:

- nếu item bank có ít information tại vùng ability của examinee, tăng calibration sample không làm vùng đó chính xác hơn;
- khi bank có information phù hợp, person ability có thể khá robust với sample size/bank size trong các điều kiện mô phỏng;
- bank khoảng 200 item được tác giả xem là tốt hơn cho nhiều mục đích, nhưng phụ thuộc quality và coverage.

**Quy tắc production:** trước khi tối ưu stopping, vẽ/kiểm tra bank information theo `theta` và theo frequency band. Nếu vùng tương ứng với tail vocabulary không có positive support hoặc information đủ, test phải trả `provisional/coverage failure`; không được “bù” bằng prior mạnh hay tăng một cách cơ học số item ở vùng khác.

### 2.4 Calibration design cần phân bổ theo thông tin, không chỉ theo N tổng

Bài Psychometrika về *Optimal Item Calibration* xây dựng restricted optimal designs cho tình huống examinee có sẵn đến từ một quần thể hữu hạn, thay vì giả vờ có thể lấy đúng các ability point mong muốn. Bài mô tả các interval ability tối ưu và formal condition để kiểm tra optimality; cách lấy mẫu ngây thơ quanh unrestricted points không tối ưu.

Áp dụng cho vocabulary item bank:

- pretest nên có coverage ở ability range dự kiến của người làm và ở các band có count contribution lớn;
- mỗi item mới cần lưu target ability range, band, expected response time/burden và uncertainty của `(a,b)`;
- nếu sample calibration tự chọn từ users online, phải lưu reference population và kiểm tra common support; không gán “calibration uncertainty nhỏ” chỉ vì số response lớn.

### 2.5 Cost và precision là trade-off thiết kế, không phải hậu kiểm

Veldkamp–Matteucci nêu rõ giảm test length làm test kém informative và tăng error; giảm chi phí viết, pretest, calibration làm uncertainty về item quality tăng. Empirical priors/linked designs có thể giảm cost nhưng phải ghi prior và linked calibration assumptions.

ETS cũng nhấn mạnh không có một adaptive method tốt cho mọi chương trình; content, format, population và giá trị của người dùng score quyết định thiết kế. CAT có thể đạt precision tương đương test thường dài hơn khoảng 25% trong một số bối cảnh, nhưng đây không phải hệ số chung.

Do đó mục tiêu không nên là “ít item nhất”, mà là tối thiểu hóa loss có điều kiện trên:

```text
count error + report/decision error + respondent burden + exposure/validity risk
```

### 2.6 Non-myopic selection là hướng nghiên cứu, không phải mặc định production

Deep CAT preprint mô tả Fisher/MI selection là one-step-lookahead, sau đó học policy Q-learning offline. Trong simulation 500 session với bank 150 item, 5 latent factors và ngưỡng posterior variance do tác giả đặt, Q-learning dừng trung bình 21,5 item, so với MI 23,2 và Max Var 25,7. Đây là bằng chứng rằng reward/stopping objective có thể thay đổi test length và early precision; không phải bằng chứng để dùng 21,5 item hoặc ngưỡng `<0.16` cho vocabulary.

Production v1 nên dùng công thức expected-value đơn giản, tái lập được; chỉ bật RL sau khi có simulator, holdout và audit policy drift. Reward phải phạt thiếu band coverage và uncertainty under-reporting, nếu không policy sẽ học “dừng sớm” thay vì học count đúng.

## 3. Thuật toán đề xuất

### 3.1 Data model tối thiểu

```text
manifest:
  manifest_version, corpus_version, dictionary_version
  lexical_unit_rule, bands[h].M_h, exclusions

item:
  item_id, band_id, target_unit, format, sense_id
  theta_or_difficulty_support
  a_hat, b_hat, cov_ab_or_posterior_draw_ref
  fit_status, exposure_status, calibration_n

session:
  respondent_id_pseudonymous, route_seed, form_version
  phase_history, response_status, item_ids
  pi1, q2_given_history, response_propensity_if_validated
  calibration_draw_seed, model_version
```

`calibration_n` chỉ là diagnostics. Không dùng một N tối thiểu cố định thay cho posterior/SE và information coverage.

### 3.2 Count estimator trong mỗi calibration draw

Với vocabulary universe `U`, band `h` có `M_h` units, và response/design rows `i`:

```text
p_hat_h^(m) = sum_i_in_h(w_i * z_i^(m)) / sum_i_in_h(w_i)
K_hat^(m)   = sum_h(M_h * p_hat_h^(m))
```

- `w_i` là design/route/nonresponse-calibrated weight đã được kiểm tra support;
- `z_i^(m)` là known/acceptable response hoặc posterior response score trong draw `m`;
- nếu route phụ thuộc vào `phi^(m)`, phải replay path và recalculate selection probabilities;
- band-total constraints vẫn phải giữ `sum_i_in_h(w_i) = M_h` hoặc một constraint tương đương đã khai báo.

Point report không nên chỉ là plug-in:

```text
K_report = median_m(K_hat^(m))
CI_bank_response = quantile_m(K_hat^(m), [alpha/2, 1-alpha/2])
```

`CI_bank_response` chỉ có ý nghĩa nếu draw đã bao gồm sampling/route/response/model layers cần thiết. Nếu dùng bootstrap path hoặc replicate design, không cộng các SE component khi có covariance chưa biết; dùng joint replicate hoặc nested simulation.

### 3.3 Expected value of another item

Gọi `D` là dữ liệu hiện tại và `d` là report/decision (ví dụ count rounded, interval category hoặc “provisional vs release”). Chọn loss minh bạch:

```text
R(D) = min_d E[L(d, K) | D]

EVI_j = R(D)
        - sum_r P(r | D, j) * R(D union {response r to j})
        - cost_j
```

`L` có thể có các thành phần đã đăng ký trước:

```text
L(d, K) = lambda_count * count_loss(d, K)
        + lambda_decision * wrong_decision(d, K)
        + lambda_burden * time_or_item_cost
        + lambda_invalid * invalid_release_risk
```

Trong v1 không cần tuyên bố các `lambda` là “đúng” theo lý thuyết; chúng là policy parameters phải được owner/score user duyệt và sensitivity-tested. Nếu không có downstream decision, đặt `wrong_decision = 0` và dùng `count_loss + burden`, hoặc dùng stopping theo CI width/conditional SEM.

Candidate score có thể tính bằng Monte Carlo:

```text
for candidate j in eligible_items:
    for calibration draw m:
        simulate response r from posterior predictive(phi_m, D, j)
        update learner posterior and route state
        recompute K_hat_m_after_j and release diagnostics
    EVI_j = current_risk - expected_future_risk - cost_j
select argmax(EVI_j)
```

Candidate vẫn bị loại nếu vi phạm frequency-band coverage, positive inclusion probability, exposure, lexical-unit balance, anchor protection hoặc item-fit gate. Không để EVI chọn toàn item gần theta nếu điều đó làm `M_h`/band support không thể ước lượng.

### 3.4 Stopping rule

Dừng release khi mọi gate sau đây đạt:

1. `CI_total_width <= tau_count` hoặc conditional SEM đạt mục tiêu intended use;
2. với report phân loại/rounded, `P(d_star is unchanged | calibration/response draws) >= 1 - delta_dec`;
3. `max_j(EVI_j) <= 0` trong candidate set hợp lệ, hoặc expected gain thấp hơn tolerance đã đăng ký;
4. band positivity, effective sample size, route/form equating, integrity và key/item gates đều pass;
5. chưa vượt `hard_max` và không có tail/censoring warning.

Nếu còn uncertainty calibration lớn nhưng mọi item còn lại đều có EVI âm, không được ép ra một count “chính xác”; trả `provisional` với interval và reason. Ngược lại, nếu count interval hẹp do plug-in nhưng calibration-draw interval rộng, giữ trạng thái chưa ổn định.

### 3.5 Pseudocode đầy đủ

```text
function administer_vocab_test(manifest, calibrated_bank, respondent):
    assert manifest_is_frozen(manifest)
    assert item_fit_and_key_gates_pass(calibrated_bank)

    phi_draws = load_calibration_draws(calibrated_bank)
    state = initialize_posterior_and_design_state(respondent, manifest)

    while True:
        diagnostics = joint_path_replicates(state, phi_draws, manifest)
        K_draws = [estimate_count(rep, manifest) for rep in diagnostics]
        report = summarize_count(K_draws)

        valid_candidates = filter_by_content_band_support_exposure(
            remaining_items(state), state, manifest
        )
        stop_precision = report.total_ci_width <= tau_count
        stop_decision = decision_stability(report, delta_dec)
        stop_value = max_expected_value(valid_candidates, state, phi_draws) <= 0
        stop_gates = all_validity_and_support_gates(report, state)

        if (stop_precision and stop_decision and stop_value and stop_gates):
            return release(report, status="calibrated")
        if hard_max_reached(state):
            return release_or_provisional(report, status="hard_max_or_uncertain")
        if not valid_candidates:
            return provisional(report, reason="no_valid_candidate_or_band_support")

        j = argmax_expected_value(valid_candidates, state, phi_draws)
        response = administer(j)
        state = update_response_route_design_state(state, j, response)
```

## 4. So sánh với Preply

Các chi tiết product dưới đây lấy từ [artifact iteration 69](72-two-phase-design-based-estimation-iteration-69.md) và [artifact iteration 70](73-answer-key-ambiguity-noisy-labels-iteration-70.md), nơi methodology proxy đã được ghi là HTTP 200; callback hiện tại không reverify được vì direct và proxy probes trả 403/error. Không thêm claim mới về hidden production controls.

| Thành phần | Preply đã được ghi nhận trong state/report trước | Thiết kế calibration-error-aware |
|---|---|---|
| Universe | Hơn 45.000 dictionary entries/headwords theo methodology vendor đã fetch trước | Freeze `U`, `M_h`, lexical unit, corpus/dictionary version; không gọi headword là word-family nếu chưa định nghĩa |
| Sampling | Khoảng 40 broad items, khoảng 120 narrow items, logarithmic rank và midpoint explanation | Route có `pi1`, `q2`, seed/history; replay path trong replicate |
| Point estimate | Midpoint/cancellation; vendor margin khoảng ±10,33% được ghi là calculation theo assumption cụ thể | `K_hat^(m)` qua calibration/route/response draws; report median/interval + diagnostics |
| Item calibration | Public methodology đã fetch không nêu posterior/SE/covariance của item parameters | Lưu `a_hat,b_hat,cov_ab` hoặc posterior/bootstrap draws; không dừng trên SE plug-in đơn thuần |
| Adaptive objective | Narrowing theo rank được mô tả; chưa có bằng chứng public về loss/EVI | EVI/loss chọn item nhưng vẫn bị band/content/exposure constraints |
| Stopping | Chưa tìm được nguồn xác thực cho decision-stability hoặc calibration-aware stopping của Preply | Precision + decision stability + EVI + validity gates; threshold phải pilot |
| Uncertainty | Margin vendor không đủ bằng chứng để nói đã bao gồm calibration/route/model/key uncertainty | Joint path replicates, separate sensitivity and empirical coverage validation |

Gap product-specific: **chưa tìm được nguồn xác thực cho ý này** về việc Preply có calibration posterior, covariance, bank-information audit, expected-value stopping, decision-stability gate hoặc propagation của item-parameter uncertainty vào margin.

## 5. Validation plan

### A. Calibration study và parameter-draw quality

- Dùng pretest linked design, stratify theo frequency band và ability-support proxy; hold out persons/forms.
- Fit candidate 1PL/2PL/3PL hoặc model phù hợp; ghi model selection, item fit, `a/b` covariance và posterior/bootstrapped draws.
- Kiểm tra calibration draws bằng parameter recovery, posterior predictive check và coverage của item parameter intervals; không chỉ kiểm tra correlation.
- Vary calibration sample size, bank size, bank information gaps và item-selection ratio. Không chọn N=150/500/1.000 làm rule trước khi thấy bias/RMSE/coverage mục tiêu.

### B. Finite-population vocabulary simulation

Tạo universe có `M_h` biết trước và tỷ lệ biết theo các shape: monotone, reversal, tail-sparse, domain-shifted. Mỗi scenario thay đổi:

- calibration bias/random error và covariance giữa `a,b`;
- item misfit, discrimination overestimation và bank coverage gaps;
- phase-I/phase-II route, response missingness và exposure;
- `lambda` cost/loss, candidate constraints và hard max.

So sánh:

1. midpoint/log-rank plug-in;
2. design-weighted band estimator;
3. fixed-parameter IRT/CAT;
4. calibration-draw-aware CAT;
5. greedy EVI;
6. constrained greedy information;
7. fixed-length fallback.

Metrics: bias của `K_hat`, RMSE, empirical CI coverage, CI width, conditional coverage theo band/ability, wrong-release rate, decision consistency, item burden, exposure concentration và route comparability.

### C. Decision-policy validation

- Đặt một số downstream use case rõ ràng: rounded count, interval category, hoặc chỉ diagnostic.
- Đánh giá độ nhạy với `lambda_count`, `lambda_burden`, `lambda_invalid`, `tau_count`, `delta_dec` và prior population.
- Kiểm tra policy trên calibration/validation split riêng; không tối ưu loss và báo cáo hiệu quả trên cùng response data.
- Đối chiếu với fixed-length form để biết EVI có thực sự giảm burden mà không làm xấu coverage hay chỉ học dừng sớm.

### D. Operational release gates

- Không release nếu bank information gap nằm trong vùng report; tăng bank coverage hoặc trả provisional.
- Không release nếu calibration-draw interval rộng hơn threshold dù plug-in interval đạt threshold.
- Monitor theo `bank_version`: calibration sample, parameter drift, draw diagnostics, band ESS, route share, total interval coverage và decision-change rate.
- Khi thay bank/model/cost policy, tạo scale version mới và re-equate; không nối trực tiếp longitudinal counts khác version.

## 6. Assumptions và gaps còn lại

### Assumptions cần công khai

- `U`, band boundaries và lexical-unit ontology là finite và versioned.
- `M_h` được biết chính xác từ manifest; nếu universe thay đổi thì đó là scale change, không phải learner growth.
- Calibration draws đại diện đủ cho uncertainty của item parameters; nếu chỉ có point estimate thì chỉ được gọi là provisional.
- Route/selection probabilities và response status được log; nonresponse không mặc định là wrong.
- EVI loss/cost phản ánh intended use; score user chấp nhận việc công khai chính sách stopping.
- Interval method được validate bằng simulation/holdout, không suy ra coverage chỉ từ công thức.

### Gaps

- Chưa có response-level/item-bank/calibration data của Preply để kiểm tra `a,b`, covariance, bank information, route probabilities hoặc calibration-aware margin.
- Chưa có vocabulary-specific evidence để chọn `lambda`, `tau_count`, `delta_dec`, prior hay hard max.
- Chưa có calibration sample để biết item-parameter draws có đủ bao phủ tail vocabulary và các subgroup hay không.
- EVTI lead không được dùng vì endpoint nội dung không fetch được; **chưa tìm được nguồn xác thực cho ý này** đối với công thức/kết quả EVTI cụ thể trong callback.
- Deep CAT là preprint và không phải vocabulary study; cần simulator/holdout riêng trước khi cân nhắc non-myopic/RL policy.

## 7. Traceability

Iteration 71 đã append 11 record mới vào `state/findings.jsonl`: 8 evidence/design records và 2 gap records sau khi thử fetch Preply/EVTI, cùng decision record. Các event chính:

- `calibration_error_understates_cat_uncertainty`
- `max_information_capitalizes_on_parameter_error`
- `bayesian_parameter_draws_are_a_viable_uncertainty_layer`
- `bank_information_coverage_limits_calibration_sample_benefit`
- `calibration_design_should_cover_ability_support`
- `calibration_cost_quality_tradeoff_is_explicit`
- `non_myopic_selection_can_change_stopping_efficiency`
- `adaptive_test_stop_must_match_precision_and_program_values`
- `calibration_error_aware_decision_stopping_design`
- `decision_theory_source_access_gap`
- `preply_current_fetch_gap`

The JSONL was append-only and validated with `json.loads` on every line; line count increased from 442 to 453. Artifact này không thay thế các topic files cũ và không tuyên bố Preply đã dùng thuật toán đề xuất.
