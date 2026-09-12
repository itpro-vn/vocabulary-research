# Iteration 67: Privacy-preserving response data và calibration governance

## 1. Phạm vi và trạng thái bằng chứng

Iteration này tách một vấn đề vận hành khỏi các iteration về item exposure, copying và response-integrity: **dữ liệu cá nhân của người làm bài và dữ liệu dùng để calibration phải được thu thập, giữ, chia sẻ và phát hành thế nào để không làm hỏng validity/uncertainty của vocabulary-size estimate**.

Các URL dưới đây đã được fetch trực tiếp trong callback và đều trả HTTP 200 trước khi trích dẫn:

| Nguồn | Vai trò | HTTP |
|---|---|---:|
| [GDPR Article 5, legislation.gov.uk](https://www.legislation.gov.uk/eur/2016/679/article/5) | purpose limitation, data minimisation, storage limitation, security/confidentiality, accountability | 200 |
| [GDPR Article 25, legislation.gov.uk](https://www.legislation.gov.uk/eur/2016/679/article/25) | privacy by design/default, pseudonymisation và giới hạn accessibility | 200 |
| [NIST Privacy Framework PDF](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.01162020.pdf) | Identify-P, Govern-P, Control-P, Communicate-P, Protect-P | 200 |
| [NIST SP 800-188](https://csrc.nist.gov/pubs/sp/800/188/final) | de-identification, data-sharing model, re-identification risk và governance | 200 |
| [NIST SP 800-226 IPD](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.ipd.pdf) | differential privacy, privacy–utility trade-off, composition/privacy budget | 200 |
| [U.S. Department of Education PTAC PDF](https://studentprivacy.ed.gov/sites/default/files/resource_document/file/Student%20Privacy%20and%20Online%20Educational%20Services%20%28February%202014%29_0.pdf) | guidance về provider, purpose control, contract, transparency trong bối cảnh FERPA | 200 |
| [Zhou, Luo & Ji, FedIRT arXiv HTML](https://arxiv.org/html/2506.21744) | federated/DP IRT calibration, simulation và empirical illustration | 200 |
| [Preply methodology proxy](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) | đối chiếu disclosure của sản phẩm tham chiếu | 200 |

Hai URL Preply trực tiếp `test-your-vocab` và `test-your-vocab/how-it-works` trong callback trả HTTP 403; proxy ở bảng trên trả HTTP 200. Proxy chỉ giúp đọc trang methodology, không chứng minh quyền truy cập vào production backend hay policy nội bộ.

## 2. Bằng chứng chính

### 2.1 Privacy là một layer riêng, không phải một score correction

GDPR Article 5 nêu purpose limitation, data minimisation, storage limitation, integrity/confidentiality và accountability. Article 25 yêu cầu data protection by design/default, trong đó pseudonymisation và giới hạn amount, extent, storage period, accessibility phải được xem xét ngay khi thiết kế xử lý dữ liệu.

Đối với vocabulary test, các loại dữ liệu có rủi ro và mục đích khác nhau:

| Dữ liệu | Mục đích có thể hợp lệ | Quy tắc thiết kế |
|---|---|---|
| `identity`/email/consent | gửi kết quả, quyền dữ liệu, hỗ trợ | nằm trong identity vault riêng; không đi vào item-response table |
| `session_id`, `response_id` | chấm phiên và audit kỹ thuật | pseudonymous; tách khóa nối; retention ngắn hơn calibration |
| item responses | điểm cá nhân, item calibration | chỉ giữ khi purpose/consent/contract cho phép; access theo role |
| RT/device/network telemetry | QC hoặc nghiên cứu đã đăng ký | không thu mặc định; nếu thu phải có purpose và sensitivity analysis |
| item parameters/aggregate gradients | calibration và equating | có thể giữ ở secure enclave/federated site; kiểm soát release và small-cell risk |
| `K_hat`, CI, flags | trả kết quả | score không tự động là anonymous; cần xem linkage và release context |

Vì privacy control không đo thêm lexical knowledge, không cộng/trừ `K_hat` theo việc có DP, pseudonymisation hay consent. Privacy làm thay đổi **pipeline dữ liệu, tập calibration và uncertainty**, không định nghĩa lại estimand.

### 2.2 De-identification không đồng nghĩa anonymous

NIST SP 800-188 yêu cầu đánh giá mục tiêu và rủi ro trước khi de-identify, chọn data-sharing model, tiến hành re-identification studies và dùng measurable performance levels. Tài liệu cảnh báo công cụ chỉ mask identifiers có thể không đủ; quasi-identifiers và linkage phải được xét.

Trong vocabulary test, một bản ghi không có tên vẫn có thể dễ link nếu chứa tổ hợp hiếm như:

```text
item_response_vector + exact timestamp + rare frequency-band pattern
+ device fingerprint + school/site + score + retest history
```

Vì vậy, safety copy hoặc public research export không được tạo bằng cách đơn giản xóa `user_id`. Quy trình tối thiểu là:

1. định nghĩa threat model và intended data-sharing model;
2. phân loại direct identifiers, quasi-identifiers và sensitive response features;
3. tách khóa nối khỏi response data;
4. đánh giá linkage/re-identification trên dữ liệu giả lập và sample kiểm thử;
5. chỉ release aggregate/synthetic/protected-enclave output theo threshold đã đăng ký;
6. ghi phiên bản transformation và residual risk.

### 2.3 Differential privacy tạo một uncertainty component mới

NIST SP 800-226 mô tả trade-off: epsilon nhỏ hơn thường cho privacy mạnh hơn nhưng accuracy thấp hơn. Khi cùng dataset được phân tích nhiều lần, composition cộng dồn privacy loss thành total privacy budget. Vì vậy, một pipeline DP phải ghi tối thiểu:

```text
privacy_unit = student | session | event
epsilon_total, delta_total
clipping_bound C
noise mechanism and scale
number_of_rounds / releases
accounting method
utility metrics and calibration version
```

Không được lấy CI của estimator non-private rồi trình bày như CI của estimator private. Nếu DP noise đi vào item parameters hoặc ability posterior, interval phải propagate cả nguồn đó.

### 2.4 FedIRT là bằng chứng phương pháp, chưa phải vocabulary-specific validation

Zhou, Luo và Ji (arXiv v2, 03/04/2026) mô tả:

- FedIRT giữ raw response ở từng site và truyền summary/gradient để calibration phân tán;
- FedIRT-DP clip gradient từng người, dùng secure aggregation và thêm Gaussian noise ở server;
- mô hình hỗ trợ 2PL và partial-credit;
- guarantee được mô tả ở mức user với `(ε, δ)` và có composition/post-processing implications.

Trong simulation, họ dùng `K = 10` site, `J = 10` item và `N_k ∈ {50, 100, 300}`. FedIRT bám gần các baseline tập trung `ltm`/`mirt`; FedIRT-DP có sai số lớn nhất ở `N_k = 50`, giảm khi `N_k` tăng và nhỏ hơn khi `N_k = 300`. Empirical illustration dùng một subset TIMSS 2019 gồm 50 trường và 15 item dichotomous, khoảng 6–8 người mỗi trường; DP giữ hầu hết thứ hạng item nhưng làm discrimination/difficulty khác.

Study 3 đưa vào 10%–50% response rows toàn 0 hoặc toàn 1. FedIRT-DP có MSE/bias phẳng hơn FedIRT khi có extreme rows, nhưng khi contamination tăng thì thông tin cũng mất. Đây là evidence cho utility/robustness trade-off trong IRT, **không** là bằng chứng rằng DP tự sửa guessing, copying hoặc vocabulary-specific bias.

## 3. Thiết kế đề xuất cho vocabulary-size estimator

### 3.1 Data zones

Đề xuất chia hệ thống thành bốn zone với quyền và retention riêng:

```text
Identity Vault
  subject_key, consent/legal_basis, contact, deletion_request
  -> chỉ identity service đọc

Scoring Zone
  pseudonymous session_id, item_id, response, response_status
  -> chấm cá nhân; không chứa contact/direct identity

Calibration Zone
  item responses hoặc local sufficient statistics
  -> secure enclave hoặc federated site; versioned bank/strata/anchors

Release Zone
  K_hat, uncertainty decomposition, quality/privacy flags, aggregate reports
  -> không trả raw responses; kiểm soát small-cell và linkage
```

Trong deployment nhiều tổ chức, calibration có hai mode:

- **Secure central calibration:** chỉ phù hợp khi legal basis, contract, access control và retention cho phép; raw responses không đi vào public analytics.
- **Federated calibration:** mỗi site tính local contributions; trung tâm nhận aggregate được bảo vệ. Nếu cần formal DP, dùng user-level unit cho toàn bộ response vector của một người, không coi từng answer là một user độc lập.

### 3.2 Privacy-aware calibration model

Với response vector `x_i` của người `i`, item model 2PL có thể viết:

```text
p_ij(θ_i) = logistic(a_j × (θ_i − b_j))
```

Một vòng federated DP có dạng:

```text
g_i = gradient contribution of the whole response vector x_i
ĝ_i = g_i × min(1, C / ||g_i||₂)
G = Σ_i ĝ_i
G_private = G + Normal(0, σ² C² I)
parameter_next = MAP_update(parameter_current, G_private)
```

`C` và `σ` không chọn theo cảm tính. Chúng phải được calibration simulation trên đúng số item, frequency strata, site size, response missingness và model (Rasch/2PL/partial-credit) dự kiến dùng.

Estimator breadth sau khi có parameter draw `s`:

```text
K_hat^(s) = Σ_h M_h × mean_j∈sample(h) p_j^(s)(θ)
```

Trong đó `M_h` là số lexical units của stratum `h`, còn `p_j` là xác suất biết item theo model đã calibration. Nếu DP làm nhiễu item parameters, lấy `p_j^(s)` từ posterior/parameter draws đã bao gồm DP uncertainty; không tính `K_hat` từ một point estimate private rồi gắn CI non-private.

Báo cáo:

```text
K_hat_main       = median_s(K_hat^(s))
CI_response      = interval from response/model posterior without DP noise
CI_privacy       = sensitivity of K_hat to DP parameter/noise draws
CI_total         = calibrated interval from full simulation/replicate procedure
privacy_status   = private | federated_nonprivate | central_secure | unknown
```

`CI_total` chỉ được release khi coverage đã được kiểm tra trên holdout. Nếu chưa có coverage, trả `uncertainty_status = uncalibrated` và báo riêng `privacy_sensitivity_range`, không tạo một margin cố định.

### 3.3 Pseudocode

```text
function calibrate_vocab_bank_privacy_aware(sites, bank, manifest, privacy_config):
    assert bank.universe_version == manifest.universe_version
    assert bank.item_parameters_version == manifest.item_parameters_version
    assert privacy_config.privacy_unit == "student" or "session"

    local_updates = []
    for site in sites:
        local_rows = site.load_local_responses()
        local_rows = enforce_purpose_and_retention(local_rows, manifest)
        local_rows = remove_direct_identity(local_rows)
        local_rows = keep_statuses(local_rows,
            ["answered", "wrong", "not_sure", "omitted", "timeout"])

        if privacy_config.mode == "federated_dp":
            per_user_gradients = gradient_by_user(local_rows, bank)
            clipped = [clip_l2(g, privacy_config.C) for g in per_user_gradients]
            update = secure_sum(clipped)
        else:
            update = sufficient_statistics(local_rows, bank)

        local_updates.append(update)

    aggregate = secure_aggregate(local_updates)
    if privacy_config.mode == "federated_dp":
        aggregate = aggregate + gaussian_noise(
            sigma=privacy_config.sigma,
            sensitivity=privacy_config.C,
            dimension=aggregate.dimension)
        parameters = map_update(aggregate, prior=manifest.parameter_prior)
    else:
        parameters = standard_irt_update(aggregate)

    account_privacy_budget(privacy_config, rounds=1)
    validate_item_fit_dif_lid(parameters, site_summaries=True)
    draws = posterior_or_bootstrap_draws(parameters, manifest)
    K_draws = [weighted_vocab_count(draw, bank, manifest) for draw in draws]
    intervals = propagate_response_model_and_privacy_uncertainty(K_draws)
    return release_result(
        K_hat=median(K_draws), intervals=intervals,
        privacy_metadata=privacy_config,
        raw_response_export=False)
```

### 3.4 Release gates

Không release một điểm calibrated nếu thiếu một trong các điều kiện sau:

1. `universe_version`, frequency manifest, lexical-unit policy và item-bank version khớp;
2. privacy unit, epsilon/delta, clipping/noise và cumulative release count có log;
3. không có direct identity trong calibration payload;
4. site/group cell đủ lớn hoặc được aggregate theo policy đã đăng ký;
5. item fit, local dependence, DIF và site-imbalance checks vẫn chạy được từ local summaries;
6. CI/credible interval đã tính cả privacy-induced uncertainty nếu DP được dùng;
7. deletion/retention path đã test và không làm hỏng anchor/equating audit;
8. nếu privacy mechanism chưa được validation trên vocabulary bank, `privacy_status` phải là `experimental`, không trình bày như production guarantee.

## 4. So sánh với Preply

| Thành phần | Preply methodology đã fetch | Thiết kế đề xuất |
|---|---|---|
| Universe | hơn 45.000 dictionary entries; main entries, derived forms gộp theo dictionary | giữ universe/headword policy versioned và tách identity/privacy metadata |
| Sampling/scoring | broad khoảng 40 item, narrow khoảng 120 item; midpoint/logarithmic spacing | giữ sampling estimator/IRT nhưng calibration zone có access/retention/privacy manifest |
| Raw response governance | trang methodology mô tả thuật toán vocabulary, không nêu pseudonymisation, retention, DP/federated calibration hay telemetry policy | data zones, purpose/retention/access log, secure/federated calibration |
| Uncertainty | vendor nêu margin khoảng ±10% trong methodology | `CI_response`, `CI_model`, `CI_sampling`, `CI_privacy`, `CI_total`; không tái dùng ±10% khi pipeline thay đổi |
| External audit | direct URLs trả 403 trong callback; proxy methodology trả 200 | yêu cầu audit artifact, parameter/version manifest và release log có thể kiểm tra |
| Privacy claim | chưa tìm được nguồn xác thực cho production privacy controls | chỉ claim mức privacy có mechanism, threat model, accountant và validation tương ứng |

Bảng này không kết luận Preply không có privacy controls nội bộ. Kết luận được hỗ trợ là **các controls đó không xuất hiện trong methodology page đã đọc và chưa có source public xác thực trong callback**.

## 5. Validation plan

### 5.1 Utility và measurement

1. Tạo vocabulary item bank có frequency strata, word-family/headword mapping, anchors và response model đã version hóa.
2. Tạo response data tổng hợp có ability distribution, band structure, missingness, guessing và site heterogeneity giống deployment.
3. So sánh central non-private IRT, federated non-private, federated DP ở các `N_site`, `C`, `σ`, epsilon/delta và số round.
4. Đo item-parameter bias/MSE, rank correlation, θ error, `K_hat` bias, CI coverage và interval width.
5. Kiểm tra conditional error ở low/mid/high vocabulary; không chỉ báo một global average.

### 5.2 Privacy và linkage

1. Threat model: malicious analyst, compromised site, server nhìn aggregate, liên kết với auxiliary data và repeated release.
2. Tấn công linkage/re-identification trên response pattern, timestamp, site, score và retest; so sánh raw-pseudonymous, aggregate, synthetic và DP release.
3. Kiểm tra cumulative privacy budget qua nhiều calibration rounds, alternate forms và subgroup reports.
4. Kiểm tra deletion request: xóa identity link mà không để lộ response; nếu phải re-calibrate sau deletion thì đo thay đổi item parameters/K_hat.
5. Không gọi pseudonymous export là anonymous nếu chưa có re-identification study.

### 5.3 Measurement fairness và transport

1. Chạy DIF/site-heterogeneity trên local summaries; kiểm tra curriculum, L1, age và target population.
2. So sánh `K_hat`/CI trước và sau privacy mechanism theo group; privacy noise không được tạo ra subgroup-specific distortion không được báo.
3. Nếu DP/secure aggregation làm mất diagnostic đủ để kiểm tra LID/DIF, giữ một calibration enclave có kiểm soát thay vì giả vờ rằng absence of evidence là evidence of invariance.

## 6. Assumptions và gaps

- FedIRT là arXiv preprint; kết quả `N_k`, MSE/bias và TIMSS illustration không được chuyển nguyên thành threshold cho vocabulary-size production.
- NIST/GDPR/PTAC là guidance/khung pháp lý hoặc governance, không phải bằng chứng rằng một cấu hình cụ thể tuân thủ mọi luật của quốc gia triển khai.
- DP epsilon/delta, clipping bound, noise scale, retention period và small-cell threshold chưa có dữ liệu target để chọn; **chưa tìm được nguồn xác thực cho các ngưỡng production chung**.
- Chưa có response-level/item-bank data của Preply để kiểm tra họ có pseudonymisation, retention, federated/DP calibration, telemetry controls hay privacy audit nào.
- Chưa có pilot để đo privacy-induced bias riêng trên frequency bands, word families/lemmas, guessing correction, DIF và `K_hat` interval coverage.

Kết luận iteration: **bảo vệ dữ liệu và ước lượng vocabulary là hai layer liên quan nhưng không đồng nhất**. Production nên giữ `K_hat` theo estimand vocabulary đã định nghĩa, thêm privacy metadata và uncertainty sensitivity, dùng federated/DP calibration chỉ sau utility–coverage–privacy validation; không biến privacy mechanism thành một hệ số điều chỉnh số từ.
