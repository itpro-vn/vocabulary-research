# Iteration 56 — Bayesian calibration và phân rã độ không chắc chắn

## 1. Phạm vi và kết luận điều hành

Direction của iteration này là **Bayesian calibration và uncertainty decomposition cho short vocabulary-size forms**. Mục tiêu không phải biến một bài Bayesian về productive vocabulary thành công thức receptive vocabulary, mà là xác định phần nào Bayesian inference có thể đóng góp một cách kiểm chứng được:

1. biểu diễn phân phối hậu nghiệm thay vì một point estimate;
2. partial pooling cho item khó/ít response;
3. kiểm tra posterior predictive, hội tụ và dự báo ngoài mẫu;
4. tách response/model uncertainty khỏi item-sampling và reference-population uncertainty;
5. dùng posterior để quy đổi ability thành số lexical units trong universe đã khai báo.

**Khuyến nghị:** giữ estimator stratified/IRT làm lõi. Bayesian chỉ được dùng sau khi lexical universe, item parameters, response format và calibration population đã được cố định. Mỗi người làm bài nhận `K_median` và interval trên cùng đơn vị (lemma, word family hoặc headword), cùng các thành phần uncertainty riêng. Không dùng prior để “bù” thiếu item bank hoặc thiếu response-level calibration.

## 2. Nguồn đã fetch và verify

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| Meara & Miralpeix, *Bayesian Vocabulary Tests*, VIAL 2021 | 200 | Bayesian trên mẫu productive vocabulary; giới hạn estimand và thiết kế evaluation |
| Koizumi & In'nami, *Structural Equation Modeling of Vocabulary Size and Depth Using Conventional and Bayesian Methods*, Frontiers in Psychology 2020 | 200 | Bayesian SEM trong nghiên cứu vocabulary size/depth, item bands và model-fit gates |
| Bürkner, *Bayesian Item Response Modeling in R with brms*, arXiv:1905.09501 | 200 | posterior, prior, partial pooling, identification, PPC và cross-validation trong IRT |
| Güsten et al., *Bayesian modeling of item heterogeneity ... and prospects for CAT*, Scientific Reports 2022 | 200 | precedent cho Bayesian item heterogeneity, calibration-before-CAT và conditional error |
| ETS, *Standards for Quality and Fairness* 2014 | 200 | yêu cầu chính thống về uncertainty, reliability, adaptive/matrix sampling và reporting |

URL Preply do người dùng cung cấp trả **HTTP 403** trong callback này; không dùng nó làm nguồn đã xác minh cho cơ chế hiện tại.

## 3. Findings từ nghiên cứu

### 3.1 Bayesian vocabulary paper không phải receptive vocabulary-size estimator

Meara và Miralpeix nghiên cứu productive vocabulary. 160 người tham gia (80 L1 English, 80 L2 Spanish/Catalan advanced) tạo sáu tính từ cho mỗi năm tranh. Mỗi nhóm dùng 50 người làm reference corpus và 30 người làm evaluation. Posterior được cập nhật theo loại response; `P(L2 | words) > .6` được gán L1, `< .4` được gán L2, khoảng giữa là chưa xác định.

Điểm có thể tái sử dụng là cách cập nhật xác suất khi bằng chứng ít và không hoàn hảo. Điểm **không** được chuyển đổi là target: đây là classification của provenance/proficiency và task-specific productive repertoire, không phải tổng số receptive lexical units. Vì vậy không được lấy xác suất L2/L1 hoặc 95% của classifier làm “số từ biết”.

### 3.2 Bayesian SEM ủng hộ tách size khỏi depth

Koizumi và In'nami dùng 255 người học L2 ở Nhật và một size test 40 item: 5 item cho mỗi 1,000-lemma level, chia thành 1,000–3,000, 4,000–6,000 và 7,000–8,000. Bayesian SEM cho thấy mô hình hai nhân tố tương quan (size và depth) phù hợp hơn mô hình một nhân tố; tương quan latent giữa hai nhân tố khoảng `r = .943`, nhưng hai construct vẫn được xem là riêng biệt.

Quy tắc cho sản phẩm:

- `vocabulary_size` chỉ là breadth/size nếu item kiểm tra form–primary meaning;
- depth, polysemy, collocation, word parts và productive use phải là output khác hoặc subscore khác;
- không dùng posterior tổng hợp để tuyên bố người làm bài “biết sâu” tất cả lexical units đã nhận diện;
- frequency-band scores có thể là indicators của size, nhưng phải kiểm tra item-level unidimensionality trước khi aggregate.

### 3.3 Bayesian model phải có release gates

Nghiên cứu Bayesian SEM dùng PSR gần 1.0 và dưới 1.1 như tiêu chí chấp nhận được, trace plot ổn định, posterior-predictive p gần 0.5 với khoảng 95% đối xứng quanh 0. Các model có residual-covariance prior không hội tụ: PSR 5.463 và 5.493 ngay cả sau khi tăng lên 100,000 iterations.

Đây không phải universal threshold cho mọi sampler, nhưng là bằng chứng trực tiếp trong vocabulary research rằng output của Bayesian engine không tự động là kết quả dùng được. VST production phải chặn score release nếu:

- chain diagnostics không đạt;
- posterior predictive không tái tạo được response pattern quan trọng;
- prior sensitivity làm thay đổi quyết định hoặc interval vượt ngưỡng sản phẩm;
- model chỉ hội tụ do prior quá mạnh mà không có calibration evidence.

### 3.4 IRT Bayesian: posterior, partial pooling và identification

Bürkner mô tả posterior:

```text
p(theta, xi | y) ∝ p(y | theta, xi) p(theta, xi)
```

Trong đó likelihood nối response với parameters, còn prior biểu diễn bất định trước dữ liệu. Hierarchical prior cho item tạo partial pooling, giúp item estimates ít bị pattern cực đoan và noise chi phối. Tuy nhiên, posterior tồn tại không có nghĩa model đã được xác định tốt; scale, discrimination và person distribution vẫn cần constraint/anchor. Non-convergence cũng không tự động chứng minh non-identification.

Áp dụng cho VST:

- item difficulty/discrimination nên được calibrate từ sample độc lập có connected design;
- short-form response chỉ cập nhật person ability, không đồng thời “học lại” độ khó item chưa được neo;
- prior phải được version hóa, giải thích và sensitivity-tested;
- nếu band hiếm response, partial pooling là lựa chọn bảo thủ hơn estimate độc lập, nhưng không được giả định shrinkage đã loại hết bias.

### 3.5 PPC và cross-validation là kiểm tra trước khi quy đổi count

Bürkner mô tả việc lấy mẫu từ posterior predictive để so sánh `y` thực với `y_hat`, dùng `pp_check`; log-likelihood có thể dùng cho LOO-CV hoặc k-fold. Quy tắc triển khai: kiểm tra phân phối correct/incorrect theo frequency band, extreme-score pattern, false-alarm/guessing signal, item cluster và subgroup trong dữ liệu replicated. So sánh held-out giữa Rasch, 2PL, guessing-aware và prevalence-covariate models; không chọn model chỉ vì point estimate trông hợp lý.

### 3.6 CAT Bayesian cần calibration trước và error theo trait level

Güsten et al. (Scientific Reports; recognition memory, không phải vocabulary) kết hợp Rasch với response-bias parameter bằng Bayesian MCMC. Họ dùng 1,354 người làm calibration sample và 200 người cho CAT; item infit trên 1.3 bị loại. MAP được cập nhật sau từng response và item tiếp theo chọn theo Maximum Fisher Information. Trong mô phỏng, CAT đạt `SE_theta < .6` ở 26 trial thay vì 79 trial fixed-order, và đạt `rho = .9` ở 26 trial thay vì 50 trial.

Đây là precedent thiết kế chứ không phải hiệu năng của VST. Có thể rút ra ba điều: (a) item phải có calibration trước; (b) precision phụ thuộc trait level và item targeting; (c) stopping rule có thể dựa trên conditional error thay vì số item cố định. Không được chuyển nguyên các con số 26/79 sang vocabulary.

### 3.7 ETS: phải báo uncertainty theo đúng nguồn biến thiên

ETS yêu cầu statistics cho score users phải chỉ rõ degree of uncertainty, giải thích thuật ngữ kỹ thuật và giữ dữ liệu/quyết định để tái lập. Với adaptive test, reliability phải tính ảnh hưởng của khác biệt item selection; resampling simulation được chấp nhận. Với matrix sampling, reliability phải tính sampling scheme. Technical report nên có standard error trên chính score units, conditional SEM khi error thay đổi theo score range, và phân tích riêng cho long/short forms hoặc subgroup khi có dữ liệu.

Đây là cơ sở chính thống để không gói toàn bộ vào một `±10%`: khoảng response/model có thể hẹp trong khi uncertainty do lexical universe, item sampling hoặc target population vẫn lớn.

## 4. Estimator đề xuất

### 4.1 Estimand

Khai báo trước:

- `U`: declared lexical universe, phiên bản cụ thể;
- `M = |U|`: số unit trong universe;
- `unit_type`: lemma, word family hoặc headword;
- strata `h = 1..H`, mỗi stratum có `M_h` unit và `sum_h M_h = M`;
- reference population, language variety, corpus/version và test format.

Không được viết “biết X từ” nếu X đang trộn headword với lemma/word family.

### 4.2 Response model

Với item `j` và ability `theta`, baseline Rasch/2PL:

```text
p_j(theta) = logistic(a_j * (theta - b_j))
logistic(x) = 1 / (1 + exp(-x))
```

Nếu format có informed guessing hoặc false alarm, dùng model đã calibration có lower asymptote/response-bias parameter; không áp một correction factor 0.25/0.33 chỉ từ số đáp án. `a_j`, `b_j` phải đến từ calibration, có uncertainty posterior hoặc replicate estimate.

### 4.3 Quy đổi sang vocabulary count

Với posterior draw `s` và stratum `h`:

```text
K_h^(s) = M_h * mean_j_in_sampled_h p_j^(s)(theta^(s))
K^(s)   = sum_h K_h^(s)
```

Nếu có full-universe model-based probabilities `q_u^(s)`:

```text
K^(s) = sum_{u in U} q_u^(s)
```

Báo `median(K)`, `Q02.5(K)`, `Q97.5(K)` và band-level contribution. Không nhân raw total-correct rate với `M` khi item difficulty không đồng nhất hoặc inclusion probability khác nhau.

### 4.4 Phân rã uncertainty

Tạo các replicate posterior sau:

1. **Response/model uncertainty (`U_resp`)**: thay đổi `theta` theo posterior, giữ item calibration/stratum cố định.
2. **Item-calibration uncertainty (`U_item`)**: đồng thời draw `a_j,b_j` từ calibration posterior.
3. **Item-sampling uncertainty (`U_item_sample`)**: resample item trong từng stratum hoặc dùng finite-population replicate; giữ `M_h` cố định.
4. **Reference-population uncertainty (`U_pop`)**: chạy population-specific calibration/weighting hoặc prevalence sensitivity; không gộp vào CI response như thể là sampling noise.
5. **Model sensitivity (`U_model`)**: so sánh model candidates bằng held-out predictive score và báo range/stacked posterior nếu nhiều model còn hợp lý.

Thực tế có thể báo `CI_response_model` trước, sau đó `range_item_sampling`, `range_population_model`. Chỉ tạo một interval tổng hợp khi quy trình bootstrap/nested posterior đã được validation về coverage trên synthetic và hold-out data.

## 5. Pseudocode

```text
INPUT: declared universe U, strata M_h, calibrated item bank B,
       response vector y, target precision epsilon, max_items

assert unit_type, universe_version, reference_population are declared
assert B is linked to calibration scale and passes item-fit/convergence gates

fit candidate models on calibration data
run convergence diagnostics, PPC, and held-out/LOO comparison
reject model if diagnostics fail or prior sensitivity is material

initialize theta from declared prior or calibrated MAP
while n_items < max_items:
    eligible = unexposed_items_with_band_coverage(B)
    item = choose_item_max_information(eligible, theta)
    administer(item)
    record response_status, display_order, latency, item_id
    update posterior(theta | y, item_parameters)

    if conditional_precision(posterior theta) <= theta_target:
        if every required band around decision boundary has n_min:
            break

for each posterior draw s:
    draw theta_s and item parameters_s
    for each stratum h:
        compute p_j_s for sampled items
        K_h_s = M_h * weighted_mean(p_j_s, inclusion_weights_h)
    K_s = sum(K_h_s)

repeat K calculation over item-sampling replicates and population/model scenarios
run posterior predictive checks on band totals, extreme patterns, false alarms,
clusters and subgroup slices
report median K, 95% posterior interval, component uncertainty and sensitivity ranges
if release gate fails: return provisional/insufficient-precision status, not a precise count
```

## 6. So sánh với cách Preply được công bố/quan sát được

| Thành phần | Preply reference/proxy hiện có trong report | Bayesian production đề xuất |
|---|---|---|
| Đơn vị | phương pháp vendor/proxy nói main dictionary entries; current endpoint chưa verify trong callback | khai báo và version hóa lemma/headword/word-family universe |
| Sampling | proxy mô tả rank/log spacing và midpoint; current implementation chưa xác minh | frequency-stratified/linked sampling với inclusion weights và item calibration |
| Scoring | proxy công bố midpoint/rank và margin; không có response-level calibration hiện tại | posterior ability → weighted sum xác suất biết trên từng stratum |
| Guessing | không được suy ra correction universal từ endpoint 403 | model guessing/false alarm chỉ khi có calibration; otherwise sensitivity, không correction tùy ý |
| Uncertainty | vendor/proxy margin không bao quát mọi construct/population/model uncertainty | tách `U_resp`, `U_item`, `U_item_sample`, `U_pop`, `U_model` |
| Adaptive | chưa có nguồn xác thực cho current Preply adaptive mechanics | MAP/posterior update + information-based selection sau independent calibration |
| QA | current Preply item bank/response data chưa verify | convergence, PPC, LOO/hold-out, item fit, coverage simulation và audit log |

Bảng trên chỉ so sánh với những gì đã ghi trong các artifact trước; không khẳng định đó là cơ chế current Preply khi endpoint trả 403.

## 7. Validation plan và release gates

### Calibration

- calibration sample độc lập, target population và mọi frequency band đều có response;
- connected anchors nếu có nhiều form;
- item-fit, local dependence, DIF và exposure checks;
- prior sensitivity: weakly informative, hierarchical và robustness variants.

### Simulation

Sinh synthetic universe với biết trước `K_true`, band sizes, item difficulty, discrimination, informed guessing, false alarm, missingness, local dependence và population shift. Đo:

- bias và RMSE của median/posterior mean;
- empirical coverage của 80%/95% interval;
- coverage riêng cho extreme score và từng band;
- stopping rate và expected item count;
- false release rate khi prior/model sai;
- sai lệch do item sampling và adaptive exposure.

### Hold-out / repeated forms

- chia calibration/hold-out theo người, không chỉ random response;
- common-person/common-item alternate forms;
- test–retest và form-to-form stability;
- so sánh Bayesian count với baseline stratified estimator và Preply-like midpoint trên cùng sample;
- báo correlation không thay thế calibration/coverage: một estimator có thể tương quan cao nhưng interval sai.

### Production release gate

Chỉ phát hành numerical count nếu:

1. diagnostics hội tụ đạt tiêu chí đã pre-register;
2. PPC không có mismatch material ở band totals, extreme patterns hoặc false alarms;
3. posterior/model sensitivity nằm trong ngưỡng đã định nghĩa;
4. synthetic và hold-out coverage đạt mục tiêu;
5. score report ghi rõ lexical unit, universe, reference population và từng nguồn uncertainty;
6. nếu item exposure/repeat contamination hoặc missingness vượt gate, trả provisional/insufficient precision.

## 8. Gaps

- Chưa có response-level/item-bank data của current Preply để fit hoặc kiểm tra Bayesian model.
- Chưa xác minh được current Preply item pool, answer key, adaptive routing, prior, calibration population hay reference population trong callback này.
- Chưa có study vocabulary-specific chứng minh posterior interval coverage cho công thức `K = sum_h M_h * mean(p_j)` trên target population.
- Các số CAT 26/50/79 từ Scientific Reports thuộc recognition memory; chỉ dùng làm precedent, không phải benchmark VST.
- Cần quyết định product threshold cho `epsilon`, interval width, band minimum và composite uncertainty trước pilot; chưa có nguồn xác thực để chọn một ngưỡng universal.

## 9. Tài liệu đã verify

- Meara, P. M., & Miralpeix, I. (2021). *Bayesian Vocabulary Tests*. VIAL, 18, 177–204. [PDF](https://revistas.uvigo.es/index.php/vial/issue/download/208/78)
- Koizumi, R., & In'nami, Y. (2020). *Structural Equation Modeling of Vocabulary Size and Depth Using Conventional and Bayesian Methods*. Frontiers in Psychology, 11:618. [Article](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00618/full)
- Bürkner, P.-C. (2019). *Bayesian Item Response Modeling in R with brms*. [arXiv PDF](https://arxiv.org/pdf/1905.09501)
- Güsten, J., Berron, D., Düzel, E., & Ziegler, G. (2022). *Bayesian modeling of item heterogeneity in dichotomous recognition memory data and prospects for computerized adaptive testing*. Scientific Reports, 12, 1250. [Article](https://www.nature.com/articles/s41598-022-04997-3)
- ETS. (2014). *ETS Standards for Quality and Fairness*. [PDF](https://www.fr.ets.org/pdfs/about/standards-quality-fairness.pdf)
