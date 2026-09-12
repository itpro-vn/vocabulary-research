# Iteration 22 — Latent response-model robustness và diễn giải mastery

## 1. Phạm vi

Iteration này mở một hướng riêng với các iteration trước: không chỉ hỏi “nên dùng Rasch hay IRT?”, mà kiểm tra độ nhạy của vocabulary-size estimate khi mô hình response thay đổi. Trọng tâm là:

- 1PL/Rasch, 2PL và 3PL cho response đúng/sai;
- mô hình slip/guess có latent mastery;
- rapid guessing và response time như một response-process signal;
- model selection, absolute/relative fit, boundary problem và multiplicity;
- quy tắc bảo thủ để chuyển xác suất “known” thành số lượng từ, thay vì coi câu đúng là bằng chứng chắc chắn người dùng biết từ.

Các nguồn được fetch hoặc kiểm tra trực tiếp trong iteration:

| Nguồn | HTTP check | Vai trò |
|---|---:|---|
| DeMars (2018), *Comparing the Two- and Three-Parameter Logistic Models via Likelihood Ratio Tests: A Commonly Misunderstood Problem* | URL PMC trả HTTP 200; nội dung toàn văn lấy được qua `r.jina.ai` do PMC HTML kích hoạt reCAPTCHA | Cấu trúc 1PL/2PL/3PL, absolute/relative fit, LR boundary, mô phỏng Type-I error và multiplicity |
| Stewart, McLean & Kramer (2017), *A Response to Holster and Lake Regarding Guessing and the Rasch Model* | Trang metadata/abstract CoLab trả HTTP 200 | Bằng chứng trực tiếp về VST, guessing và giới hạn của mean-square Rasch fit |
| Wang et al. (2020), *Cognitive Diagnostic Models for Random Guessing Behaviors* | URL PMC trả HTTP 200; toàn văn lấy qua `r.jina.ai` | DINA/G-DINA, latent mastery, slip/guess, response time và rapid guessing |
| Guo, Zheng & Kern (2020), *IRTBEMM* | URL PMC trả HTTP 200; toàn văn lấy qua `r.jina.ai` | Tính khả thi của Bayesian/MLE estimators, EAP, SE và fit indices |
| Preply test và `how-it-works` | Cả hai URL trả HTTP 403 với browser User-Agent | Chỉ ghi nhận gap; không dùng làm nguồn đã xác minh trong iteration này |

`r.jina.ai` chỉ được dùng như lớp lấy nội dung cho các URL PMC đã kiểm tra HTTP 200; URL nguồn được trích dẫn trong findings vẫn là URL bài gốc PMC. Search snippets không được dùng làm bằng chứng.

## 2. Bằng chứng đã xác minh

### 2.1 1PL/Rasch, 2PL và 3PL là các giả định khác nhau về response

Nghiên cứu IRT nhị phân mô tả một hierarchy lồng nhau:

- 1PL/Rasch: các item dùng một discrimination chung;
- 2PL: mỗi item có discrimination `a_j` riêng;
- 3PL: thêm lower asymptote `c_j`, thường được diễn giải là xác suất đúng do guessing ở mức năng lực thấp.

Theo nguồn, ability estimate phụ thuộc cả vector response của người làm bài và tham số item của model. Do đó, cùng một số câu đúng có thể tạo ra estimate khác nhau khi chuyển giữa Rasch, 2PL và 3PL. Đây là lý do không được dùng công thức `raw_accuracy × N` như một vocabulary count có ý nghĩa psychometric nếu chưa cố định estimand và model.

Với `L(x) = 1/(1+exp(-x))`, các xác suất response có thể viết:

```text
Rasch / 1PL: P(R_ij=1 | theta_i) = L(theta_i - b_j)
2PL:         P(R_ij=1 | theta_i) = L(a_j * (theta_i - b_j))
3PL:         P(R_ij=1 | theta_i) = c_j + (1-c_j) * L(a_j * (theta_i-b_j))
```

Đây là các mô hình response, chưa phải tự động là mô hình “biết từ”. `theta` là latent test ability trên scale của item bank; mapping `theta → vocabulary count` phải được calibration riêng trên universe từ vựng đã định nghĩa.

### 2.2 Model fit cần hai lớp: absolute fit và relative fit

Nguồn phân biệt:

- **Absolute fit:** response dự đoán có khớp dữ liệu quan sát hay không.
- **Relative fit:** model nào trong tập ứng viên giải thích dữ liệu tốt hơn với độ phức tạp phù hợp.

AIC/BIC là relative-fit measures; model thắng AIC/BIC vẫn có thể fit kém tuyệt đối. Vì vậy pipeline phải kiểm tra residual/item fit và predictive performance cùng với AIC/BIC hoặc hold-out log loss. Khi model lồng nhau, LR test có thể hỗ trợ lựa chọn, nhưng không thay thế absolute-fit checks.

Quy tắc đề xuất:

1. Fit các model ứng viên trên calibration sample, không fit lại model class theo từng người dùng.
2. Chạy absolute-fit diagnostics đã định trước: item residual, band residual, local-dependence residual, response-pattern checks và calibration plot.
3. Dùng AIC/BIC hoặc hold-out predictive loss để so sánh tương đối.
4. Chọn model đơn giản nhất vượt cả absolute-fit gate và predictive gate; nếu các model cạnh tranh gần nhau, giữ model chính ổn định và báo `model_sensitivity` thay vì tuyên bố model phức tạp hơn là “đúng”.

### 2.3 3PL có boundary problem; không dùng chi-square chuẩn một cách máy móc

Trong LR test giữa 2PL và 3PL, null hypothesis đặt `c_j=0`, tức tham số guessing ở biên không gian tham số. Điều này vi phạm điều kiện regularity cho phân phối chi-square thông thường của LR statistic.

Nguồn mô phỏng cho thấy:

- so sánh Rasch với 2PL không gặp boundary issue kiểu này;
- so sánh 2PL với 3PL cho toàn test không thể dùng reference distribution chuẩn một cách mặc định;
- với kiểm tra item-level có một guessing parameter ở biên, mixture 50:50 của chi-square 0 và 1 phù hợp hơn trong điều kiện nghiên cứu;
- trong mô phỏng 30 item, 30 kiểm tra item-level ở mức comparisonwise `.05` tạo familywise error ước tính `0.776` nếu không kiểm soát multiplicity; Bonferroni trong điều kiện đó đưa familywise error ước tính xuống `0.049`.

Các số này là kết quả mô phỏng của nguồn, không phải threshold cho vocabulary test. Production nên dùng parametric bootstrap hoặc reference distribution đã mô phỏng theo item-bank/population cụ thể; nếu kiểm tra nhiều item, phải ghi rõ multiplicity control.

### 2.4 Rasch mean-square không chứng minh MCQ không guessing

Bài phản hồi trực tiếp về Vocabulary Size Test lập luận rằng mean-square fit trung bình của Rasch không thể xác định tỷ lệ random guesses trong raw score trung bình: mean-square có thể gần 1 ngay cả với dữ liệu hoàn toàn ngẫu nhiên. Bài cũng lập luận rằng các lựa chọn multiple-choice có thể làm phồng vocabulary-size estimates.

Hệ quả cho một form kiểu Preply:

- không dùng một mean-square tổng hợp để kết luận “guessing không đáng kể”;
- không dùng hệ số correction `1/k` cố định chỉ vì item có `k` lựa chọn;
- kiểm tra distractor/option functioning, response time, pseudoword hoặc confidence nếu có;
- chạy sensitivity giữa Rasch/2PL và model có lower asymptote trên calibration data;
- đưa chênh lệch giữa các model vào `sensitivity_range`, không che nó dưới một số làm tròn.

Bằng chứng này hỗ trợ cảnh báo về cơ chế, nhưng không cung cấp hệ số guessing riêng cho Preply.

### 2.5 Latent mastery với slip/guess cần một định nghĩa thuộc tính rõ ràng

Trong DINA, item yêu cầu một tập thuộc tính được khai báo trong Q-matrix. Người làm bài thuộc một trong hai lớp theo item:

- mastery: có đủ các thuộc tính yêu cầu, xác suất đúng `1-s_j`;
- non-mastery: thiếu ít nhất một thuộc tính, xác suất đúng `g_j`.

Với vocabulary, “biết từ” có thể không phải một thuộc tính đơn: form–meaning recognition, sense cụ thể, word-family relation, collocation hoặc recall có thể khác nhau. Nếu không có lexical-facet annotation/Q-matrix, dùng DINA để gọi một câu đúng là “mastery” sẽ là overclaim.

Có thể dùng mô hình slip/guess như sensitivity layer với một lexical attribute đơn giản, nhưng output phải ghi rõ:

```text
breadth_count = estimate trên lexical universe đã định nghĩa
mastery_profile = xác suất/diagnostic theo facet nếu facet đã được calibration
```

Không cộng trực tiếp depth hoặc confidence vào breadth count.

### 2.6 Rapid guessing có thể làm sai item và person parameters

Nguồn CDM kết hợp response time với item response bằng latent indicator phân biệt solution attempt và rapid guessing. Trong mô phỏng có rapid guessing, model có lớp RG thu hồi tham số tốt hơn; khi bỏ qua RG, slipping bị overestimate và item intensity, guessing, time discrimination bị underestimate. Trong điều kiện không có RG, hai model cho kết quả gần như nhau; một mô phỏng báo classification accuracy trung bình `96.6%` cho cả hai cách.

Đây là bằng chứng ngoài vocabulary, nên chỉ suy ra một nguyên tắc an toàn:

- response time là diagnostic/response-process signal trước khi là điểm số;
- không tự động recode câu trả lời quá nhanh thành sai;
- nếu item response và RT được model chung, phải calibration trên thiết bị, population và UX thực tế;
- nếu chưa có calibration RT, gắn `rapid_guessing_flag` và tăng uncertainty hoặc yêu cầu completion/retest, thay vì thay đổi count âm thầm.

### 2.7 Pipeline tính toán có thể cung cấp uncertainty nhưng không tạo ra validity

IRTBEMM mô tả Bayesian EMM/BE3M và maximum-likelihood estimation cho 3PL, 4PL, 1PL-G và 1PL-AG; package cung cấp item standard errors, EAP ability estimates và log-likelihood, G-square, AIC, BIC, RMSEA. Package cho phép thay prior, initial values, convergence criterion và quadrature settings.

Điều này chứng minh tính khả thi của estimator và output diagnostics, không chứng minh model nào phù hợp với vocabulary-size test. Implementation phải lưu model version, parameter constraints, convergence, effective sample size/SE và sensitivity configuration; không gọi posterior/SE là external validity.

## 3. Mô hình đề xuất cho production

### 3.1 Giữ estimator breadth làm output chính

Output chính vẫn là breadth estimate trên một universe/version cụ thể, ví dụ:

```text
V_hat = số lexical units được định nghĩa là target universe
unit = headword | lemma | word_family
universe_version = corpus + dictionary + filtering manifest
```

Model response chỉ giúp ước lượng xác suất kiến thức hoặc latent position; nó không được phép thay đổi `unit` âm thầm.

### 3.2 Response model candidate

Fit offline một tập ứng viên:

```text
M1 = Rasch/1PL
M2 = 2PL
M3 = 3PL với c_j bị ràng buộc trong khoảng hợp lý
M4 = latent slip/guess model nếu có lexical-facet/Q-matrix
```

M4 chỉ bật khi item bank có annotation thuộc tính đủ để lập Q-matrix. Nếu không, M4 là sensitivity research model, không phải production mastery label.

### 3.3 Chuyển từ model response sang `P(known)`

Một cách mô hình hóa bảo thủ (cần calibration, không phải hệ số có sẵn) là tách latent knowledge `K_ij` khỏi response `R_ij`:

```text
P(R=1 | K=1) = 1-s_j
P(R=1 | K=0) = g_j
P(K=1 | theta_i, band_j) = q_ij
```

Với prior `q_ij` và một response quan sát:

```text
P(K=1 | R=1) = q_ij*(1-s_j) /
               [q_ij*(1-s_j) + (1-q_ij)*g_j]

P(K=1 | R=0) = q_ij*s_j /
               [q_ij*s_j + (1-q_ij)*(1-g_j)]
```

`q_ij`, `s_j`, `g_j` phải được ước lượng/calibrate từ common-person response data hoặc thiết kế validation tương ứng. Nếu không có dữ liệu đủ để tách các thành phần này, không xuất `P(known)` item-level; dùng posterior ability/model sensitivity thay thế.

### 3.4 Quy đổi stratified sang số từ

Với các band `h`, frame size `N_h`, sampled items `S_h` và inclusion probability `pi_j`, có thể tính trên từng posterior draw `d`:

```text
p_h^(d) = weighted_mean_j_in_S_h( P(K_j=1 | data, d), weight=1/pi_j )
V^(d)   = sum_h N_h * p_h^(d)
```

Nếu sampling là equal-probability trong band, `1/pi_j` rút gọn thành trung bình trong band. Nếu item bị cluster/local dependence, variance phải dùng cluster bootstrap/jackknife hoặc effective sample size; không báo interval từ binomial independence mặc định.

Cuối cùng:

```text
vocab_hat = median_d(V^(d))
posterior_interval = quantile(V^(d), [0.025, 0.975])
```

`posterior_interval` chỉ là uncertainty conditional on model/prior/calibration. Báo thêm:

```text
sensitivity_range = range của V_hat khi đổi M1/M2/M3, prior,
                    lexical unit và exclusion rules
external_coverage = coverage đo trên người thật hold-out
```

### 3.5 Model-robust production rule

```text
function fit_model_suite(calibration_data, item_manifest):
    candidates = [Rasch, 2PL]
    if guessing_is_identifiable(calibration_data, item_manifest):
        candidates.append(3PL)
    if q_matrix_is_valid(item_manifest):
        candidates.append(latent_slip_guess)

    results = []
    for model in candidates:
        fit = fit_offline(model, calibration_data)
        abs_fit = absolute_fit_checks(
            fit,
            checks=[item_residual, band_residual, local_dependence,
                    response_pattern, calibration_plot]
        )
        rel_fit = [AIC(fit), BIC(fit), holdout_log_loss(fit)]
        results.append({model, fit, abs_fit, rel_fit})

    eligible = [r for r in results if r.abs_fit.pass and r.fit.converged]
    if eligible is empty:
        return BLOCK("no response model passed calibration")

    primary = simplest_stable_model_with_good_holdout(eligible)
    sensitivity = refit_person_scores(results, same_validation_forms=True)
    return {primary, sensitivity, fit_diagnostics=results}

function estimate_vocab(session, fitted_suite, design):
    response = administer(
        session,
        design,
        anchors=True,
        exposure_control=True,
        log_response_status=True,
        log_response_time=True
    )

    if response.completion_gate_failed:
        return diagnostic_only("insufficient observed responses")

    draws = posterior_or_EAP_person_draws(
        fitted_suite.primary,
        response,
        include_parameter_uncertainty=True
    )
    V_draws = []
    for d in draws:
        p_by_band = estimate_known_rate_by_band(
            d,
            weights=inclusion_weights(design),
            cluster_correction=design.cluster_rule
        )
        V_draws.append(sum(design.N_h[h] * p_by_band[h] for h in design.bands))

    result = summarize(V_draws)
    result.sensitivity_range = run_same_person_alternatives(
        response,
        fitted_suite.candidates,
        alternatives=[lexical_unit, prior_set, guessing_rule]
    )
    result.flags = [
        response_time_flag(response),
        local_dependence_flag(fitted_suite.primary),
        coverage_status(fitted_suite.primary.calibration_version)
    ]

    if not external_coverage_validated(fitted_suite.primary):
        result.quality = "model-conditional; external coverage unverified"
    elif sensitivity_too_large(result.sensitivity_range):
        result.quality = "diagnostic; model-sensitive"
    else:
        result.quality = "validated_for_target_population"
    return result
```

## 4. Stopping và uncertainty

Không dừng chỉ vì raw accuracy hoặc posterior interval có vẻ hẹp. Một session chỉ được coi là đủ cho production breadth output khi:

1. response count và band quotas đạt minimum đã calibration;
2. model fit/convergence gate pass;
3. exposure, missingness và rapid-guessing flags không vượt ngưỡng đã validation;
4. interval trên vocabulary scale đạt precision target đã định trước;
5. sensitivity range giữa model/unit/prior nằm trong tolerance đã xác định;
6. external hold-out coverage của interval đã được đo trên target population.

Nếu chỉ có calibration item parameters nhưng chưa có external coverage, ghi:

```text
quality = model-conditional; external coverage unverified
```

Nếu model suite cho các output chênh lệch lớn, ghi:

```text
quality = diagnostic; model-sensitive
```

Không dùng `c=1/k`, một mean-square, hay một khoảng vendor như margin universal.

## 5. So sánh với Preply

| Thành phần | Preply đã xác minh trong iteration | Thiết kế đề xuất |
|---|---|---|
| Truy cập/kiểm tra | URL bài test và `how-it-works` trả HTTP 403 trong callback này; không thể xác nhận trực tiếp model/item bank | Lưu URL/version và artifact calibration; mọi claim phải có nguồn hoặc cờ gap |
| Response model | Chưa xác minh được model 1PL/2PL/3PL, slip/guess hay latent mastery của production Preply | Fit suite offline; chọn model parsimonious sau absolute fit + hold-out predictive check |
| Guessing | Nghiên cứu VST cảnh báo MCQ có thể inflate estimate và Rasch mean-square không đo được tỷ lệ random guessing | Không correction `1/k`; dùng calibration/sensitivity và response-process flag |
| Mastery interpretation | Chưa có bằng chứng công khai để chuyển mỗi câu đúng thành “biết từ” theo latent mastery | Chỉ dùng `P(known)` khi có slip/guess calibration và lexical-facet/Q-matrix; nếu không, giữ breadth estimate model-conditional |
| Uncertainty | Không có dữ liệu response-level Preply trong iteration để kiểm định margin vendor hoặc model sensitivity | Tách posterior/model interval, design/cluster uncertainty, sensitivity range và external coverage |
| Rapid guessing | Chưa xác minh response-time model hoặc threshold Preply | Log RT nếu có consent/UX support; dùng làm quality flag trước, không recode âm thầm |
| Số từ cuối | Không được suy diễn thêm khi endpoint trực tiếp bị 403 | `V_hat = sum_h N_h p_h`; `unit` và universe version bắt buộc; báo quality flag |

So sánh này không khẳng định Preply đang dùng hay không dùng một model cụ thể. Nó chỉ phân biệt phần đã fetch/verify với phần chưa có item-bank hoặc response-level evidence.

## 6. Validation plan

### 6.1 Simulator

Tạo simulator có:

- frequency bands và frame sizes thực tế;
- `a_j`, `b_j`, `c_j`, `s_j`, `g_j` đã biết;
- latent knowledge và response model riêng;
- cluster/local dependence;
- missingness và rapid guessing theo response time;
- alternate lexical-unit mappings.

Đánh giá recovery bias của `theta`, `p_h`, `V_hat`, interval width và coverage. Chạy nhiều model-generating conditions để không chỉ chứng minh model tự fit chính nó.

### 6.2 Calibration thật

Trên sample người thật đủ đa dạng theo proficiency, L1, domain và mode:

- fit Rasch/2PL/3PL; kiểm tra convergence, item-fit, residual và hold-out log loss;
- nếu muốn latent mastery, thu thêm independent evidence hoặc facet items để định nghĩa Q-matrix;
- ước lượng guessing/slipping theo item/band và kiểm tra stability qua resampling;
- đánh giá rapid-guessing model bằng RT nhưng giữ một analysis không dùng RT để đo robustness;
- ghi model class, prior, constraints và calibration version.

### 6.3 External coverage và sensitivity

Chia train/hold-out theo người, không chỉ randomize response rows. Trên hold-out báo:

- bias, MAE/RMSE của vocabulary estimate;
- 80% và 95% interval coverage;
- interval width;
- sensitivity khi đổi Rasch/2PL/3PL, prior, lexical unit và exclusion rules;
- coverage theo band, proficiency, L1, domain và delivery mode;
- tỷ lệ score bị gắn `diagnostic_only` hoặc `model-sensitive`.

### 6.4 Gates trước khi dùng UX claim

Chỉ dùng wording mạnh như “validated estimate” sau khi external coverage đạt target population. SBC/PPC hoặc fit index chỉ kiểm tra implementation/model–response fit; chúng không thay thế criterion/common-person validation. Nếu Preply không cung cấp item bank, common-person data hoặc response-level data, ghi gap thay vì gán các ngưỡng trên cho Preply.

## 7. Kết luận iteration

Model response là một nguồn uncertainty có cấu trúc, không phải lớp trang trí cho raw score. 1PL/2PL/3PL có thể cho person estimates khác nhau; 3PL model selection có boundary/multiplicity caveat; Rasch mean-square không loại bỏ MCQ guessing; và latent mastery chỉ hợp lệ khi lexical attributes được định nghĩa. Khuyến nghị bảo thủ là giữ stratified breadth estimator làm output chính, fit model suite offline, dùng model đơn giản ổn định làm primary, lưu sensitivity range, chỉ xuất `P(known)` khi có calibration slip/guess và Q-matrix, còn response time chỉ là quality signal cho tới khi được validation.

## 8. Sources

1. DeMars, C. (2018). *Comparing the Two- and Three-Parameter Logistic Models via Likelihood Ratio Tests: A Commonly Misunderstood Problem*. Applied Psychological Measurement. https://pmc.ncbi.nlm.nih.gov/articles/PMC5978598/
2. Stewart, J., McLean, S., & Kramer, B. (2017). *A Response to Holster and Lake Regarding Guessing and the Rasch Model*. Language Assessment Quarterly. https://colab.ws/articles/10.1080/15434303.2016.1262377
3. Wang, C. et al. (2020). *Cognitive Diagnostic Models for Random Guessing Behaviors*. Frontiers in Psychology. https://pmc.ncbi.nlm.nih.gov/articles/PMC7545958/
4. Guo, S., Zheng, C., & Kern, J. L. (2020). *IRTBEMM: An R Package for Estimating IRT Models With Guessing or Slipping Parameters*. Applied Psychological Measurement. https://pmc.ncbi.nlm.nih.gov/articles/PMC7495790/
5. Reference product checked but not citable for methodology in this iteration: https://preply.com/en/learn/english/test-your-vocab (HTTP 403); https://preply.com/en/learn/english/test-your-vocab/how-it-works (HTTP 403).
