# Iteration 43 — sparse-band and subgroup calibration with partial pooling

## Phạm vi và trạng thái nguồn

Iteration này nghiên cứu một vấn đề khác với việc chỉ phát hiện DIF: khi vocabulary test phải ước lượng theo frequency band và/hoặc báo cáo theo L1, proficiency, device hay nhóm nhỏ, dữ liệu mỗi ô `band × group` có thể quá thưa. Câu hỏi là có nên shrink/partial-pool các ô này hay không, và làm sao để regularization không che khuất khác biệt item thật.

Hai nguồn học thuật đã fetch trực tiếp và kiểm tra:

1. Pohl và cộng sự, *Partial Measurement Invariance: Extending and Evaluating the Cluster Approach for Identifying Anchor Items*, bản XML toàn văn trên Europe PMC: <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8640350/fullTextXML> — HTTP 200, XML có toàn văn.
2. Baghaei, Strietholt và cộng sự, *A large-scale empirical investigation of measurement invariance decisions under multiple-group item response theory and multiple-group confirmatory factor analysis*, Frontiers in Education: <https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2026.1823761/full> — HTTP 200; bản XML của bài cũng HTTP 200.

URL Preply `https://preply.com/en/learn/english/test-your-vocab` trả HTTP 403 trong callback. Không dùng nó để suy ra item bank, group calibration, shrinkage hay DIF của Preply.

## Bằng chứng đã xác minh

### 1. So sánh latent score cần common scale; partial invariance cần anchor

Pohl và cộng sự nêu rằng muốn so sánh score trên latent construct giữa nhóm hoặc thời điểm thì thước đo phải nằm trên common scale. Trong SEM, vấn đề được gọi là measurement invariance; trong IRT, non-invariance được thể hiện qua differential item functioning (DIF). Khi full invariance không giữ được, partial measurement invariance tìm một tập anchor items được giả định invariant để thực hiện linking.

Hệ quả cho vocabulary-size estimator: một score `K_hat` theo L1 hoặc subgroup không thể được coi là comparable chỉ vì cùng công thức raw percentage. Cần có common scale, anchor evidence và trạng thái comparability được báo cáo riêng.

### 2. Anchor không nhất thiết là một tập duy nhất

Bài báo mô tả cluster approach dựa trên **difference in relative item difficulties (DRID)** và ma trận `ΔR`. Cặp item có quan hệ độ khó tương đối gần như không đổi giữa nhóm có thể tạo thành cluster ứng viên làm anchor. Điểm quan trọng là cách này cho phép nhiều tập anchor hợp lý thay vì mặc định một item duy nhất hoặc giả định mean item difficulty giống nhau giữa nhóm.

Thuật toán nên giữ:

- `anchor_set_id` và item list;
- giả định dùng để chọn anchor;
- stability của anchor qua bootstrap/resample;
- score sau linking theo từng anchor set;
- khoảng hoặc sensitivity do lựa chọn anchor.

Không nên gọi một item là anchor chỉ vì kiểm định DIF của nó không có p-value nhỏ; việc chọn anchor chịu ảnh hưởng của scale indeterminacy, cấu trúc DIF và giả định nhận dạng.

### 3. Chất lượng anchor phụ thuộc vào cấu trúc DIF, cỡ nhóm và missingness

Mô phỏng trong Pohl và cộng sự dùng test 24 item Rasch, hai nhóm, kích thước nhóm 500/1.000/2.000, kích thước DIF từ 0 đến 0,8, các mức mất cân bằng DIF, số item DIF-free bằng 1/3, 1/2 hoặc 2/3 item, và missing response 0%, 20%, 50%. Kết quả cho thấy hit rate và bias chịu ảnh hưởng đáng kể bởi DIF size, mức balancedness và số item thực sự DIF-free. Cluster approach trong đa số điều kiện được báo cáo có bias thấp hơn các cách so sánh, nhưng bias vẫn xuất hiện khi DIF lớn và ngưỡng cluster rộng hơn DIF thật.

Các con số này thuộc thiết kế mô phỏng của bài, không phải thông số vocabulary production. Hệ quả là không được copy một cutoff DIF, anchor rate hoặc minimum subgroup N thành hằng số cho Preply. Cần mô phỏng lại bằng item bank, band distribution, L1 mix, missingness và routing của sản phẩm.

### 4. MGIRT/DIF là chẩn đoán item-level, không phải toàn bộ bằng chứng invariance

Nghiên cứu ICILS 2023 của Baghaei và cộng sự so sánh multiple-group CFA (MGCFA) với multiple-group IRT (MGIRT) trên dữ liệu 31 quốc gia và một thực thể benchmark. Trong MGIRT, RMSD đo khoảng cách giữa item response function của nhóm và IRF chung; RMSD cao gợi ý item non-invariance và có thể cần group-specific item parameters. Bài dùng các mô hình PCM/GPCM và báo cáo RMSD cùng infit/outfit.

Tác giả nhấn mạnh RMSD/DIF là bằng chứng item-level, không tương đương trực tiếp với configural, metric hoặc scalar invariance trong CFA. Vì vậy, một vocabulary test cần tách hai lớp:

- **global construct comparability:** cấu trúc breadth-only có ổn định qua nhóm/form hay không;
- **item-level functioning:** item nào lệch theo nhóm sau khi điều kiện hóa trên trait.

Không được diễn giải `RMSD pass` như bằng chứng rằng mọi chiều của lexical knowledge bất biến.

### 5. Framework và cutoff có thể dẫn tới kết luận khác nhau

Trong ICILS, MGCFA khắt khe hơn: nhiều scale không đạt các mức invariance theo global fit, trong khi RMSD của MGIRT cho thấy hầu hết scale có thể so sánh. Bài kết luận hai framework đánh giá các giả thuyết khác nhau và nên được dùng bổ sung. Tác giả cũng nhấn mạnh cutoff và số nhóm có thể làm thay đổi kết luận.

Hệ quả cho vocabulary-size score theo L1: nếu global fit, DIF-item, anchor linking và predictive/hold-out validation bất đồng, không nên chọn phương pháp “dễ pass” để che khuất vấn đề. Output an toàn là `raw_estimate`, `linked_estimate` nếu đủ bằng chứng, `group_sensitivity_range`, và `comparability_status`.

## Thuật toán đề xuất

### Dữ liệu tối thiểu

```text
Response {
  person_id, group_id, item_id, band_id, response, missing_status,
  form_id, timestamp, qc_flags
}

ItemCalibration {
  item_id, band_id, lexical_unit, difficulty, discrimination,
  group_DIF_diagnostics, anchor_eligibility, content_review_status
}

LinkingRun {
  run_id, anchor_set_id, model, group_ids, item_version,
  pooled_or_unpooled, diagnostics, score_transform
}
```

### Hai estimate cần giữ song song

1. `K_hat_unpooled[b,g]`: estimate theo từng band và group, không shrink. Dùng để phát hiện group/band pattern và làm sensitivity baseline.
2. `K_hat_partial[b,g]`: estimate từ hierarchical model hoặc calibrated shrinkage. Dùng khi ô dữ liệu thưa và chỉ phát hành sau khi kiểm tra coverage, DIF retention và out-of-sample calibration.

Với `N_b` lexical units trong band `b`, `p_bg` là xác suất biết đã calibration, và `w_i` là inclusion/design weight:

```text
p_hat_unpooled[b,g] = sum_i(w_i * p_i) / sum_i(w_i)
K_hat_unpooled[b,g] = N_b * p_hat_unpooled[b,g]
K_hat_unpooled[g]   = sum_b K_hat_unpooled[b,g]
```

Một mô hình partial-pooling nhị phân có thể viết ở mức khái niệm:

```text
logit(P(Y_i = 1)) = theta_person[i]
                    - difficulty_item[i]
                    + group_effect[group_i, band_i]
                    + DIF_item_group[item_i, group_i]

group_effect[g,b] ~ Normal(mu_band[b], tau_band[b])
```

Trong triển khai production, `theta_person`, difficulty, discrimination và variance components phải được fit/calibrate từ response data; không đặt `tau` theo cảm tính. Nếu chưa có dữ liệu đủ để ước lượng hierarchical model, chỉ báo cáo unpooled estimate với interval rộng hơn, không gọi raw score là partial-pooled.

### Pseudocode release gate

```text
fit_sparse_group_vocab(responses, item_bank, calibration):
    assert construct == receptive_written_breadth
    check_band_coverage_and_missingness(responses)

    for candidate_anchor_set in generate_anchor_clusters(calibration, responses):
        fit_multi_group_irt(candidate_anchor_set)
        compute_DRID_and_DIF()
        compute_linked_scores(candidate_anchor_set)
        bootstrap_persons_and_items()

    anchor_range = range_over_valid_anchor_sets()
    fit_unpooled_band_group_model()
    fit_partial_pooling_band_group_model()

    compare:
        - item fit and residual/local dependence
        - DIF/RMSD and group-specific response curves
        - out-of-sample log loss / calibration
        - interval coverage in simulation or hold-out
        - K_hat_unpooled vs K_hat_partial_pool
        - sensitivity to anchor_set and missingness

    if group_sample_small or anchor_range_wide or coverage_not_validated:
        return raw_band_estimates,
               partial_pooling_sensitivity,
               comparability_status="unresolved"

    if partial_pooling_erases_detected_DIF:
        return unpooled_or_group_specific_estimate,
               comparability_status="group_specific_only"

    if holdout_coverage_passes and anchor_range_narrow:
        return K_hat_partial,
               K_hat_unpooled,
               uncertainty_components,
               comparability_status="linked_with_partial_pooling"
```

### Quy tắc không được làm

- Không dùng shrinkage để biến band thiếu dữ liệu thành band “đã đo chính xác”.
- Không cộng group-specific estimates nếu lexical universe hoặc lexical unit khác nhau.
- Không dùng một anchor set cố định cho mọi L1 nếu DIF/DRID cho thấy anchor instability.
- Không suy ra correction coefficient từ mô phỏng Pohl hoặc RMSD cutoff của ICILS.
- Không cộng depth, listening hoặc productive facet vào `K_hat` breadth-only.

## So sánh với Preply

| Thành phần | Thiết kế đề xuất | Preply đã verify trong iteration |
|---|---|---|
| Frequency-band estimate | Giữ unpooled và partial-pooled song song; band uncertainty được phát hành | Không có response-level/routing data công khai được kiểm tra |
| Cross-group score | Common scale, nhiều anchor-set candidate, DRID/DIF, hold-out coverage | Chưa có group-specific calibration hoặc anchor artifact được xác minh |
| Sparse groups | Hierarchical model chỉ sau calibration; nếu không đủ dữ liệu thì báo range/null | Chưa tìm được nguồn xác thực cho subgroup shrinkage |
| DIF interpretation | Tách global invariance khỏi item-level DIF; MGIRT/MGCFA evidence bổ sung nhau | Chưa xác minh được DIF, IRT model hoặc group parameters của Preply |
| Report | `K_hat_unpooled`, `K_hat_partial`, anchor sensitivity, comparability status | Không thể kết luận Preply có linked subgroup scale nào |
| Item universe | Phải khóa cùng dictionary/headword/lemma/word-family và band manifest | Preply methodology production artifact không fetch được trong callback; direct page HTTP 403 |

So sánh này không khẳng định Preply có lỗi. Nó chỉ ghi nhận rằng chưa có artifact công khai đủ để đánh giá sparse-band calibration, anchor stability hoặc subgroup comparability của Preply.

## Uncertainty và validation plan

Báo cáo tối thiểu cần tách:

```text
CI_response_or_sampling
CI_model_or_person_estimation
range_anchor_set
range_partial_pooling
range_missingness_sensitivity
range_manifest_or_frequency_version
```

Validation theo thứ tự:

1. Tạo pilot đa L1/proficiency với cùng item bank, lưu band, form, missingness và response status.
2. Fit unpooled Rasch/2PL, MGIRT/DIF và hierarchical model; kiểm tra convergence, item fit, local dependence và person-score precision.
3. Tạo nhiều candidate anchor sets bằng DRID/cluster và content review. Bootstrap người/item để đo tần suất item được chọn làm anchor.
4. Mô phỏng theo response data thực tế: giảm subgroup N, tăng missingness, tăng DIF unbalancedness và thay đổi phân bố band. Đo bias, RMSE, coverage và false-release rate của unpooled/partial-pooling.
5. Dùng hold-out common-person/common-item sample để kiểm tra score linking giữa forms/groups. Nếu interval của anchor sets chồng lấn kém hoặc linked difference phụ thuộc anchor, `comparability_status` phải là unresolved.
6. Chỉ sau khi đạt coverage mục tiêu mới chọn variance prior/shrinkage strength, minimum subgroup N, anchor count và release threshold. Các ngưỡng này chưa được xác minh cho Preply.

## Gaps

- Không có Preply item-level response data, band-by-group counts, item parameters, DIF/RMSD, routing probabilities hoặc anchor records công khai được xác minh.
- Chưa có bằng chứng để chọn một công thức shrinkage, prior variance, subgroup minimum N hoặc anchor cutoff dùng chung cho vocabulary tests.
- Chưa có calibration xác nhận partial pooling bảo toàn khác biệt thực của vocabulary breadth thay vì làm phẳng DIF.
- `https://ul.qucosa.de/api/qucosa:93667/attachment/ATT-0/` được search thấy như PDF lead nhưng trả HTTP 404 khi fetch; không dùng nó làm nguồn. Trang ITT chính thức xác nhận tiêu đề publication nhưng không cung cấp toàn văn kết quả trong nội dung đã fetch.
- Vì vậy, production nên giữ `K_hat_partial` là sensitivity/experimental output cho đến khi có pilot và hold-out validation; `K_hat_unpooled` hoặc band-level descriptive estimate vẫn là output minh bạch hơn khi comparability chưa được chứng minh.
