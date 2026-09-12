# Iteration 20 — Local dependence và clustered-item sampling

## 1. Phạm vi và direction

> **Local dependence and clustered-item sampling:** kiểm tra liệu item liên quan về stimulus, cluster, ngữ cảnh, thứ tự hoặc quan hệ lexical có vi phạm giả định độc lập hay không; chuyển bằng chứng thành quy tắc item-bank, chẩn đoán Q3, effective sample size và độ không chắc chắn.

Direction này bổ sung cho các iteration trước về sampling precision và IRT/CAT. Trọng tâm ở đây không phải số item trên danh nghĩa, mà là số thông tin độc lập thực tế khi nhiều item chia sẻ stimulus hoặc có quan hệ đáp ứng.

## 2. Nguồn đã kiểm tra

| Nguồn | Kiểm tra | Vai trò |
|---|---:|---|
| [Ha (2022), *Test Format and Local Dependence of Items Revisited: A Case of Two Vocabulary Levels Tests*, Frontiers in Psychology](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.805450/full) | HTTP 200; tải HTML khoảng 707 KB, chuyển được sang text và kiểm tra phần abstract, phương pháp, bảng residual và thảo luận | Nghiên cứu trực tiếp về LID trong LVLT/UVLT, matching cluster và 4-option MCQ |
| [DOI của bài Ha](https://doi.org/10.3389/fpsyg.2021.805450) | HTTP 200 | Xác nhận định danh bài/đường dẫn canonical |
| Preply test và methodology | Endpoint trực tiếp trả HTTP 403 trong callback; không dùng làm nguồn claim mới | Kiểm tra gap về item bank/response-level dependence; không trích dẫn URL này như đã xác minh |

Search snippets chỉ dùng để tìm lead. Các claim định lượng dưới đây lấy từ trang Frontiers đã tải thành công; không lấy trực tiếp từ snippet.

## 3. Bằng chứng chính

### 3.1. LID làm suy yếu diễn giải Rasch/IRT

Ha mô tả local item dependence (LID) là giả định quan trọng của Rasch và các mô hình IRT. Nếu câu trả lời ở item này làm thay đổi xác suất trả lời item kia ngoài latent trait chung, phân tích dựa trên performance có thể không đáng tin hoặc gây hiểu lầm. Các item dùng chung stimulus có thể tạo thành một “polytomous super-item”; khi đó cluster trở thành một nguồn chiều/đơn vị đo riêng và có thể làm phồng reliability, khiến bài trông có chất lượng cao hơn thực tế.

Hệ quả cho vocabulary-size test: nếu ba item nằm trong cùng một matching cluster hoặc cùng context/stem, tổng số item không còn là số quan sát độc lập. Việc lấy `p_hat = số đúng / số item` rồi đưa trực tiếp vào khoảng tin cậy nhị thức sẽ có xu hướng quá tự tin nếu covariance dương bị bỏ qua.

### 3.2. Matching 3-item-per-cluster có LID quan sát được

Nghiên cứu dùng cùng một cohort 311 sinh viên EFL Việt Nam để phân tích Listening Vocabulary Levels Test (LVLT) và Updated Vocabulary Levels Test (UVLT). UVLT dùng matching format 3 item mỗi cluster. Bảng standardized-residual correlations ghi các cặp cùng cluster có tương quan `1.00`, gồm `1000-5/1000-6` và `1000-26/1000-27`. Phần thảo luận báo một số cặp vượt `0.70`, là mức cảnh báo về vi phạm local independence.

Một số cluster còn được mô tả có chuỗi tương quan cao, ví dụ nhóm `1000-1-2-3` và `1000-4-5-6`. Vì vậy ba item trong cluster không nên được xem là ba phép thử Bernoulli độc lập để mở rộng tỷ lệ đúng thành số word families/headwords.

### 3.3. Không chỉ kiểm tra các item cùng cluster

Bài cũng nhắc lại các residual correlations `0.69`, `0.67` và `0.61` mà Webb et al. báo cáo ở các item **khác cluster** của UVLT. Lập luận “không cùng cluster nên độc lập” do đó không đủ an toàn: dependency có thể phát sinh từ nội dung, ngữ cảnh, vị trí gần nhau, lexical relation hoặc chiến lược làm bài.

Ha nêu quy tắc cảnh báo thực dụng rằng tương quan khoảng `0.70` tương ứng gần `0.49` phương sai chung (`0.70 × 0.70`), và một chuỗi item gần nhau có tương quan đáng kể cũng cần được xem xét. Trong production, QA phải kiểm tra toàn ma trận residual và metadata quan hệ, không chỉ lọc `cluster_id`.

### 3.4. 4-option MCQ ít LID hơn trong một mẫu, nhưng không được miễn kiểm tra

Trong cùng nghiên cứu, LVLT 4-option multiple-choice không cho thấy vi phạm LID đáng kể theo các phân tích residual: không cặp nào được báo cáo chia sẻ quá 30% phương sai chung. Một số tương quan giữa item gần nhau được diễn giải nhiều khả năng là “strands” hơn là chiều ẩn riêng.

Đây là bằng chứng theo format, phiên bản test và mẫu cụ thể; nó không chứng minh mọi MCQ đều độc lập, cũng không chứng minh Preply có cùng đặc tính. MCQ có thể giảm dependency do không dùng chung một tập definition/cluster, nhưng item vẫn có thể liên quan qua stem, context, morphological family, semantic relation hoặc ordering.

## 4. Quy tắc thuật toán cập nhật

### 4.1. Manifest bắt buộc

Mỗi item trong bank nên có tối thiểu:

```text
item_id
lexical_unit_id
frequency_band
stimulus_id / context_id
cluster_id (nullable)
shared_stem_id (nullable)
lexical_relation_tags: morphology, synonym, antonym, semantic_set, cognate...
form_version
position_bucket
mode
```

`cluster_id` không chỉ phục vụ rendering. Nó là biến thiết kế để xác định đơn vị resampling và tính uncertainty. `lexical_relation_tags` giúp phát hiện dependency không hiển thị trong layout.

### 4.2. Calibration gate

Trên pilot có response-level data:

1. Fit Rasch/2PL hoặc model đã pre-register trên construct đã định nghĩa.
2. Tính score-residual và standardized-residual correlations, ưu tiên Q3/biến thể phù hợp model.
3. Audit các cặp cùng `stimulus_id`, `cluster_id`, `context_id`, gần nhau về vị trí hoặc có lexical relation.
4. Kiểm tra item-fit, test information và reliability trước/sau khi gộp cluster.
5. Không loại item chỉ vì một correlation trong sample nhỏ; xem xét replicate sample, content review và sensitivity analysis.

Nếu dependency ổn định và có ý nghĩa, ba lựa chọn an toàn hơn là:

- thay matching cluster bằng independent MCQ/meaning-recall items;
- giữ cluster nhưng tính điểm/uncertainty ở cấp cluster (super-item hoặc cluster-level score);
- dùng model có local-dependence/random-effect facet và báo thêm linking/model uncertainty.

### 4.3. Effective sample size và design effect

Với xấp xỉ đơn giản, nếu có `G` cluster, cluster `g` có `m_g` item và intracluster correlation gần `rho`, có thể dùng design effect:

```text
DEFF_g ≈ 1 + (m_g - 1) * rho
n_eff,g ≈ m_g / DEFF_g
```

Nếu cluster có kích thước gần bằng nhau:

```text
n_eff ≈ n / [1 + (m - 1) * rho]
```

Ví dụ trên chỉ là công thức triển khai suy ra từ mô hình cluster, **không phải hệ số đã calibration cho Preply**. Với kích thước cluster không đều, nên dùng variance estimator theo cluster hoặc cluster bootstrap thay vì thay toàn bộ bằng một `rho` chung. Nếu có nhiều tầng phụ thuộc (shared context và lexical family), cần model hoặc replicate resampling phản ánh cả hai tầng; không cộng các design effect một cách máy móc.

CI của tỷ lệ đúng nên dùng variance cấp cluster/replicate. Chỉ sau khi đã xác định sampling frame và expansion target, mới chuyển `p_hat` sang headword/lemma/word-family estimate. LID là uncertainty của đo lường/sampling, không phải lý do để thay đổi lexical estimand.

## 5. Pseudocode

```text
function calibrate_local_dependence(response_matrix, bank, model):
    fit = fit_irt_or_rasch(response_matrix, model)
    residuals = model_residuals(fit)
    pairs = residual_correlation_matrix(residuals)

    flagged = []
    for pair in pairs:
        relation = metadata_relation(pair.item_a, pair.item_b, bank)
        if pair.q3 >= preregistered_q3_review_threshold:
            flagged.append({pair, relation})

    clusters = connected_components(
        flagged, keys=[stimulus_id, cluster_id, context_id, lexical_relation_tags]
    )
    fit_sensitivity = compare_models(
        independent_items=fit,
        cluster_super_items=fit_super_item(response_matrix, clusters),
        cluster_random_effect=fit_local_dependence_model(response_matrix, clusters)
    )
    return {fit, pairs, flagged, clusters, fit_sensitivity}

function score_with_cluster_uncertainty(responses, bank, calibration):
    assert bank.lexical_frame_is_versioned
    observed = score_items(responses, bank)
    if calibration.dependence_is_material:
        groups = groups_by_cluster_or_dependency_component(bank)
        p_hat = weighted_cluster_mean(observed, groups)
        variance = cluster_robust_variance(observed, groups)
        effective_n = equivalent_n_from_variance(variance, p_hat)
        flags = ["local_dependence_adjusted"]
    else:
        p_hat = design_weighted_item_mean(observed, bank)
        variance = independent_or_design_based_variance(observed, bank)
        effective_n = equivalent_n_from_variance(variance, p_hat)
        flags = []

    ci = interval_from_replicate_or_robust_variance(p_hat, variance)
    estimate = expand_within_declared_lexical_frame(p_hat, ci, bank)
    return {estimate, ci, effective_n, flags}
```

## 6. So sánh với Preply

| Khía cạnh | Preply disclosure đã có trong state trước | Quy tắc đề xuất sau iteration 20 |
|---|---|---|
| Lexical sampling | Methodology công khai mô tả headword/frequency sampling và midpoint/logarithmic estimate | Giữ nguyên frame/version, nhưng phải thêm manifest về stimulus/cluster/context và dependency |
| Đơn vị quan sát | Chưa có item-level response data để xác minh item independence | Không mặc định `n_items` là `n_independent`; dùng cluster/robust variance nếu pilot cho thấy LID |
| Định dạng | Endpoint trực tiếp không fetch được trong callback; disclosure trước đó không cho thấy LID parameters | Kiểm tra Q3/residual trên response-level data; không suy ra từ UX |
| Uncertainty | Không thể xác minh hệ số design effect hoặc effective sample size của Preply | Báo CI/SE đã điều chỉnh theo cluster hoặc ghi rõ independent-item CI chỉ là xấp xỉ |
| Score expansion | Midpoint/expansion chỉ hợp lệ trong lexical frame tương ứng | Chỉ expand sau khi xử lý dependency và vẫn giữ headword/lemma/word-family estimand riêng |
| Cross-version comparison | Chưa có common-item/response-level evidence về dependency drift | Version hóa item bank; re-calibrate khi cluster/stimulus/order/content thay đổi |

Không có căn cứ để gán tương quan `1.00`, `0.70` hoặc công thức `n_eff` của nghiên cứu UVLT cho bài Preply. Preply item bank và response-level production data vẫn là gap.

## 7. Validation plan

- Tạo pilot response matrix đủ rộng theo frequency band và ability; ghi toàn bộ item metadata, thứ tự, timing và response status.
- Fit model reference rồi lặp lại sau khi gộp các cluster/dependency components; so sánh item difficulty, person ability, test information, reliability và CI coverage.
- Kiểm tra residual correlations toàn ma trận, không chỉ trong cluster; lặp lại trên hold-out sample và alternate form.
- Dùng cluster bootstrap/jackknife hoặc cluster-robust variance; mô phỏng coverage của CI dưới nhiều `rho`, cluster size và missingness patterns.
- Pre-register ngưỡng “review”, “material dependence” và quyết định super-item/model/loại item; không chọn ngưỡng sau khi xem kết quả.
- Kiểm tra scoring sensitivity: independent-item, cluster-level, robust variance và local-dependence model. Nếu estimate thay đổi vượt tolerance đã định trước, báo `dependence-sensitive` thay vì một số từ duy nhất.
- Kiểm tra drift khi cập nhật corpus, dictionary, context, item order hoặc renderer; dependency là thuộc tính của item × format × sample, không phải nhãn bất biến của headword.

## 8. Kết luận và gap

Bằng chứng đủ để bổ sung một production gate: vocabulary-size test phải kiểm tra local dependence và không được dùng số item danh nghĩa làm effective sample size khi item chia sẻ stimulus/cluster/context. Matching 3-item clusters là rủi ro rõ ràng trong bằng chứng UVLT; 4-option MCQ có kết quả tốt hơn trong mẫu LVLT cụ thể nhưng vẫn cần calibration.

Gap còn lại là item bank, response-level data, cluster/context metadata và variance/CI coverage của Preply. Callback này chưa tìm được nguồn xác thực cho hệ số điều chỉnh riêng của Preply; vì vậy báo cáo chỉ đưa công thức và pseudocode ở mức thiết kế, không giả vờ có coefficient production.
