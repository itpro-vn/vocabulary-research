# 3. Thuật toán đề xuất, công thức và pseudocode

## 3.1 Data model

Mỗi vocabulary universe có một manifest bất biến:

```text
Universe {
  id, version, unit = headword | word_family | lemma,
  dictionary_id, corpus_id, language_variety,
  exclusion_rules, total_units
}
Band {
  band_id, rank_low, rank_high, N_b, sampling_weight,
  item_pool_version
}
Item {
  item_id, target, band_id, answer_key, distractors,
  pos, sense_id, stem_version, exposure_count,
  pilot_difficulty, pilot_discrimination, DIF_flags
}
Response {
  session_id, item_id, answer, correct, latency_ms,
  confidence_optional, skipped, form_id
}
```

## 3.2 Fixed-length stratified estimator

1. Chia universe thành `B` frequency bands, mỗi band có `N_b` units.
2. Chọn `n_b` item ngẫu nhiên không hoàn lại từ item pool của band; dùng seed lưu lại để tái lập.
3. Tính `p_hat_b = mean(correct)`.
4. Ước lượng:

```text
V_hat = Σ_b N_b * p_hat_b
```

Nếu item score trong band là Bernoulli và sample design đúng:

```text
Var(V_hat) ≈ Σ_b N_b² * (1 - n_b/N_b) * s_b² / n_b
SE = sqrt(Var(V_hat))
CI95 = [max(0, V_hat - 1.96*SE), min(N, V_hat + 1.96*SE)]
```

Nếu có trọng số/response missing, dùng survey-weighted estimator và bootstrap theo band thay vì giả vờ các item độc lập.

## 3.3 Adaptive routing an toàn

Adaptive routing chỉ quyết định **band nào cần thêm thông tin**, không thay đổi estimand:

- Bắt đầu với anchor rải đều qua toàn universe và các band trung tâm.
- Ước lượng provisional `V_hat` và band uncertainty.
- Chọn item tiếp theo ở band có đóng góp lớn nhất vào `N_b² Var(p_hat_b)` hoặc nơi posterior uncertainty cao.
- Dừng khi (a) CI width dưới ngưỡng sản phẩm, (b) mọi band quanh ngưỡng quyết định đã đủ precision, hoặc (c) đạt max items.
- Luôn giữ anchor set cố định để equate các form và kiểm tra drift.

Không nên triển khai 2PL/3PL IRT từ đầu với item bank chưa calibration. Sau pilot đủ lớn, có thể fit Rasch/2PL; nếu model có guessing parameter, phải đánh giá bằng calibration/hold-out chứ không tự động trừ `1/k`.

## 3.4 Pseudocode

```text
function estimate_vocab(session, universe, bands, item_bank):
    assert session.universe_version == universe.version
    responses = administer_anchor_items(session, item_bank)
    for band in bands:
        n = initial_allocation(band, target_precision, max_items)
        responses += sample_without_replacement(item_bank[band], n)

    while not stopping_rule(responses, bands):
        estimates = stratified_estimate(responses, bands)
        b = argmax(unresolved_variance_contribution(estimates))
        if no_items_left(item_bank[b]) or max_items_reached(responses):
            break
        responses += sample_without_replacement(item_bank[b], 1)

    result = stratified_estimate(responses, bands)
    diagnostics = {
        'floor_bands': bands_with_rate_near_zero(result),
        'ceiling_bands': bands_with_rate_near_one(result),
        'missing_rate': missing_rate(responses),
        'anchor_inconsistency': anchor_check(responses),
        'response_time_flags': latency_flags(responses)
    }
    return result, diagnostics
```

## 3.5 Preply-style midpoint variant

Nếu mục tiêu là sản phẩm rất ngắn, có thể triển khai midpoint rank estimator:

1. Tạo rank list đã làm sạch, có `rank` hoặc `log(rank)`.
2. Giai đoạn screening rải rộng để định vị.
3. Giai đoạn narrow lấy mẫu logarithmic quanh vùng chuyển tiếp.
4. Tính midpoint có số `unknown` trước cân bằng `known` sau; nội suy trên log-rank nếu cần.
5. Báo estimate trên **đúng headword universe**, không chuyển thẳng sang word families.

Nếu cần calibration simulation và test-retest; midpoint không tự cung cấp CI hợp lệ nếu response correlation, non-monotonic knowledge và selection effects chưa được kiểm tra.

## 3.6 CAT/IRT extension sau khi có pilot calibration

Khi đã có response-level pilot đủ rộng, có thể thay routing theo band bằng CAT trên cùng vocabulary universe. Không triển khai IRT như “black box” trước calibration.

```text
function cat_vocab(session, calibrated_bank, universe, max_items, target_se):
    assert session.universe_version == universe.version
    responses = administer_fixed_anchors(session, calibrated_bank)
    theta = provisional_ability(responses, prior=population_prior)

    while len(responses) < max_items:
        candidate_set = eligible_items(calibrated_bank,
            exclude=responses.item_ids,
            exposure_control=true,
            content_balance=true)
        item = argmax_expected_information(candidate_set, theta)
        responses.append(administer(item))
        theta, se_theta = estimate_ability_and_se(responses, model="Rasch_or_2PL")
        if se_theta <= target_se and anchors_consistent(responses):
            break

    vocab_hat = logistic_calibration(theta, universe.version)
    ci_theta = theta +/- 1.96 * se_theta
    ci_vocab = transform_monotone(ci_theta, logistic_calibration)
    return vocab_hat, ci_vocab, diagnostics(responses)
```

`argmax_expected_information` chỉ hợp lệ khi item difficulty/discrimination đã được ước lượng và kiểm định; với Rasch, xác suất đúng là `P(X=1)=exp(theta-delta)/(1+exp(theta-delta))`. Trước pilot, dùng stratified random estimator ở mục 3.2 an toàn hơn CAT tự hiệu chỉnh.

### Nguyên tắc chuyển logit và dừng

- Fit `a,b,c` trên một calibration sample độc lập; giữ `universe.version`, rank source và cận `a` bất biến trong suốt một phiên bản.
- Chọn item gần theta để tăng information, nhưng bắt buộc quota/anchors cho coverage, exposure control và kiểm tra DIF.
- Dừng theo `SE_theta` hoặc độ rộng CI sau khi transform, không dừng chỉ vì đạt số câu cố định. Giữ `max_items` để chặn phiên quá dài.
- Xuất `estimate`, CI đã transform, unit, universe, `se_theta`, attention/quality flags và item-bank version. Không dùng attention index để trừ điểm nếu chưa có calibration cho phép đo đó.
