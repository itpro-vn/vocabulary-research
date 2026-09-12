# Iteration 34 — Measurement error, CSEM và cách báo cáo bất định

## Phạm vi

Iteration này tập trung vào lớp reporting sau khi bài test đã ước lượng vocabulary size: cách tách point estimate khỏi sai số đo, cách dùng SEM/CSEM, cách báo cáo chênh lệch giữa hai lần đo, và cách tránh trình bày một margin cố định như bảo đảm phổ quát. Đây là lớp diễn giải bổ sung cho thuật toán IRT/stratified đã có trong các file trước; nó không thay thế calibration item bank.

## Bằng chứng đã kiểm tra

### 1. SEM trung bình không đại diện cho mọi mức điểm

Tài liệu kỹ thuật chính thức của ETS về GRE định nghĩa SEM là độ biến thiên kỳ vọng do measurement error và mô tả khoảng xấp xỉ 95% bằng khoảng hai SEM quanh true score. Tài liệu cũng tách SEM của điểm cá nhân khỏi SEM của score differences.

Quan trọng hơn cho vocabulary test, ETS ghi rõ precision thay đổi theo vị trí trên thang điểm. CSEM (conditional SEM) biểu diễn sai số tại một reported score cụ thể, thay vì dùng một SEM trung bình cho toàn thang. ETS cho biết CSEM của GRE Verbal/Quantitative được ước lượng bằng IRT trên các bài multi-stage và có thể dùng để lập confidence band. Đây là bằng chứng từ một bài thi khác, không phải calibration trực tiếp cho vocabulary; giá trị sử dụng ở đây là nguyên tắc thiết kế reporting.

Nguồn: [ETS, Reliability and Standard Error of Measurement](https://www.ets.org/pdfs/gre/gre-reliability-standard-error-measurement.pdf) (HTTP 200 đã kiểm tra).

### 2. CSEM quan trọng khi có cut score hoặc vùng quyết định

Huebner và Skar trình bày SEM tổng quát bằng công thức khoảng quanh observed score: `observed ± z × SEM`, với ví dụ z tương ứng 68%, 95% và 99%. Họ phân biệt SEM tổng quát, tạo khoảng bằng nhau ở mọi score level, với CSEM vì sai số không phải thuộc tính bất biến theo score. Họ nêu confidence interval hữu ích khi quyết định quanh cut score.

Đối với vocabulary size, không nên biến một ngưỡng như “đủ cho use-case X” thành quyết định nhị phân nếu interval còn bao phủ cả hai phía. Nếu mục tiêu chỉ là tự nhận biết trình độ, nên hiển thị range và độ tin cậy; nếu dùng placement, phải xác định rule hành động và đánh giá decision consistency riêng.

Nguồn: [Huebner & Skar (2021), Conditional Standard Error of Measurement](https://files.eric.ed.gov/fulltext/EJ1311133.pdf) (HTTP 200 đã kiểm tra).

### 3. Có các phương pháp tính CSEM khác nhau, nhưng software không thay thế validation

Manual của gói R `csemTools` mô tả các lựa chọn gồm smoothing, bootstrap CSEM, standardized CSEM, CSEM cho scale scores, so sánh với global SEM và biểu diễn đường cong precision theo observed-score range. Đây là tài liệu phần mềm/triển khai, không phải bằng chứng rằng một phương pháp cụ thể đã đúng cho vocabulary-size estimator.

Quy tắc an toàn: có thể dùng bootstrap hoặc smoothing để tạo candidate CSEM curve, nhưng phải kiểm tra empirical coverage trên calibration/hold-out sample. Nếu không có dữ liệu response đủ lớn, chỉ báo “model-based uncertainty” và không gọi nó là confidence coverage đã được chứng minh.

Nguồn: [CRAN csemTools reference manual](https://cran.rstudio.com/web/packages/csemTools/csemTools.pdf) (HTTP 200 đã kiểm tra).

### 4. Margin của Preply là một mô hình vendor, không phải CSEM đã xác thực độc lập

Trang phương pháp Preply mô tả phase hai khoảng 120 từ và mô hình margin: standard deviation của sample points được giả định xấp xỉ `0.25 × vocabulary estimate`; với trung bình 22.5 sample points, `s / sqrt(n) = 0.0527`, rồi nhân 1.96 cho khoảng khoảng `±10.33%`. Trang cũng nói sẽ tinh chỉnh error calculation khi có thêm dữ liệu về standard deviation, sample size và phân phối sample points.

Vì phương sai được mô tả theo tỷ lệ với estimate và sample count trung bình, đây là một model-based margin có thể thay đổi theo score, item selection và response process. Trang không cung cấp item-level calibration, CSEM theo ability, coverage study độc lập, hay production response data trong phần đã fetch. Do đó report nên ghi “vendor-stated approximate margin” thay vì coi `±10%` là universal guarantee.

Nguồn: [Preply methodology](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) (HTTP 200 qua proxy đã kiểm tra; direct Preply trước đó có endpoint 403 trong môi trường này).

## Quy tắc reporting đề xuất

### 1. Tách bốn lớp thông tin

Mỗi kết quả nên có các trường:

```text
estimate_count                 # point estimate trên unit đã công bố
estimate_unit                  # headword, lemma, flemma hoặc word family
scale_version                 # dictionary/corpus/item-bank/calibration version
precision_method               # CSEM, bootstrap, design-based, posterior hoặc vendor model
se_csem_count                  # conditional SE trên thang count, nếu đã calibration
interval_level                 # ví dụ 0.95
interval_low, interval_high    # band quanh latent/true construct theo định nghĩa đã nêu
model_sensitivity_low/high     # thay đổi do model/response-model, nếu có
frame_sensitivity_low/high     # thay đổi do corpus/domain/unit frame
quality_flags                  # effort, guessing, missingness, tail, DIF, form/linking
```

Không gộp tất cả nguồn bất định vào một con số duy nhất nếu chưa có calibration chứng minh rằng phép gộp đó có coverage đúng. Ít nhất phải tách:

- `measurement_interval`: sai số do response/item measurement;
- `model_interval` hoặc sensitivity: thay đổi giữa Rasch/2PL/alternative calibration;
- `frame_interval`: thay đổi khi đổi corpus, domain, lexical unit hoặc exclusion manifest;
- `quality flags`: tín hiệu có thể làm estimate kém đáng tin nhưng chưa có cơ sở để trừ trực tiếp số từ.

### 2. CSEM trên thang ability rồi chuyển sang số từ

Nếu IRT ước lượng ability `theta` và mapping đã calibration là `V = g(theta)`, dùng CSEM trên theta rồi chuyển bằng delta method:

```text
SE_V(theta) ≈ abs(g'(theta)) * SE_theta(theta)
CI_V ≈ [g(theta) - z * SE_V(theta),
        g(theta) + z * SE_V(theta)]
```

Nếu `g` logistic, ví dụ `g(theta) = A / (1 + exp(-B(theta-C)))`, đạo hàm là:

```text
g'(theta) = A * B * exp(-B(theta-C)) / (1 + exp(-B(theta-C)))^2
```

Ở vùng floor/ceiling, đạo hàm nhỏ nhưng extrapolation và model misspecification có thể lớn; không được hiểu “SE nhỏ” là estimate chắc chắn nếu test không có item thông tin ở tail. Vì vậy tail flag và frame/model sensitivity phải được báo riêng. Nếu mapping không trơn hoặc count được làm tròn, dùng bootstrap qua toàn bộ pipeline thay vì chỉ delta method.

### 3. Interval và rounding

- Tính interval trên scale chưa làm tròn; chỉ làm tròn ở bước hiển thị cuối.
- Độ chính xác hiển thị không được vượt quá độ rộng interval và độ phân giải đã được calibration. Ví dụ, nếu uncertainty hàng trăm word families, không hiển thị đơn vị hàng chục như thể có precision ở mức đó.
- Không dùng `round(estimate)` để làm interval hẹp hơn; làm tròn cả point estimate và hai biên theo cùng policy rồi lưu raw values trong audit record.
- Ghi rõ interval là confidence/measurement band theo calibration design, hay chỉ là model-based range. Không gọi mọi range là “95% true score interval” nếu chưa có coverage test.

### 4. So sánh hai lần làm bài

Với hai estimate trên cùng scale đã equate, không lấy hai interval cá nhân rồi suy luận máy móc. Lưu `SE_diff` hoặc variance của chênh lệch:

```text
SE_diff = sqrt(SE_1^2 + SE_2^2 - 2 * Cov(error_1, error_2))
change_z = (V_2 - V_1) / SE_diff
```

Nếu hai form có common anchors và response errors gần độc lập, covariance có thể được ước lượng hoặc giả định bằng 0 nhưng assumption phải lưu. Nếu chưa có common-anchor equating, trạng thái nên là `not_comparable` thay vì báo growth. ETS minh họa rằng CSEM của score difference cần rule riêng; tài liệu GRE dùng giá trị CSEM lớn hơn của hai mức điểm và nhân 2 cho quy tắc xấp xỉ 95%, nhưng ngưỡng này không được chuyển nguyên sang vocabulary nếu chưa pilot-calibrate.

## Pseudocode lớp reporting

```text
function report_vocab_result(response_vector, item_bank, calibration, purpose):
    validate_scale_version(item_bank, calibration)
    quality = evaluate_quality_flags(response_vector, item_bank)

    theta, se_theta = estimate_ability(response_vector, calibration.model)
    count_raw = mapping(theta, calibration.theta_to_count)

    if calibration.has_conditional_se_curve:
        se_count = csem_on_count(theta, calibration.csem_curve)
        interval = count_raw + [-z95 * se_count, z95 * se_count]
        precision_method = "calibrated_csem"
    else:
        interval = bootstrap_full_pipeline(response_vector, calibration)
        se_count = interval_half_width(interval) / z95
        precision_method = "bootstrap_model_based"

    sensitivity = run_sensitivity(response_vector,
                                  models=calibration.approved_models,
                                  frames=calibration.approved_frames,
                                  units=calibration.approved_units)

    if quality.missingness_gate_failed or quality.exposure_breach:
        status = "invalid_or_review"
    elif not calibration.coverage_validated:
        status = "provisional_model_based"
    else:
        status = "reportable"

    displayed = round_with_precision_policy(count_raw, interval,
                                            calibration.display_policy)
    return {"estimate": displayed,
            "raw_estimate": count_raw,
            "interval": interval,
            "se": se_count,
            "precision_method": precision_method,
            "sensitivity": sensitivity,
            "quality_flags": quality,
            "status": status,
            "purpose": purpose}
```

## Đối chiếu với Preply

| Thành phần | Preply được công bố | Thiết kế đề xuất |
|---|---|---|
| Sampling/estimate | Hai phase; phase hai khoảng 120 từ; midpoint trên rank logarithmic | Giữ sampling theo frequency/domain nhưng lưu inclusion probability, item metadata và calibration version |
| Margin | Vendor mô tả khoảng `±10.33%` từ SD giả định `0.25 × estimate`, n trung bình 22.5 | Không dùng một margin chung; dùng CSEM theo ability/score nếu có, nếu chưa thì ghi provisional model-based interval |
| Score unit | Dictionary entries/headword theo methodology đã fetch | Công bố rõ headword/lemma/flemma/word-family; không đổi unit trong interval layer |
| Retest/growth | Chưa xác minh item bank, common anchors hoặc CSEM score-difference | Chỉ so sánh trên common scale; lưu covariance/SEdiff; nếu không equate thì `not_comparable` |
| Rounding | Preply nói round >10,000 đến trăm và 300–9,999 đến chục | Rounding phụ thuộc width interval và calibration precision; raw values vẫn được lưu |
| Validation | Trang nêu sẽ refine theo participation, nhưng không cung cấp coverage study trong nguồn đã fetch | Hold-out coverage, conditional coverage theo score band, decision consistency quanh cut score, sensitivity theo model/frame |

## Validation plan bắt buộc

1. **Calibration sample:** đủ người trên toàn range, có nhiều alternate forms và common anchors; fit item parameters và theta-to-count mapping.
2. **CSEM estimation:** tạo CSEM theo score/ability bin bằng IRT information hoặc bootstrap full pipeline; kiểm tra smoothing chỉ là phương tiện ổn định hóa, không phải bằng chứng coverage.
3. **Coverage:** trên hold-out sample, kiểm tra tỷ lệ true/reference score nằm trong interval theo từng band; báo riêng global và conditional coverage, đặc biệt floor/ceiling.
4. **Rounding audit:** mô phỏng các estimate sát ranh giới làm tròn; xác minh rounding không làm thay đổi quyết định hoặc tạo interval hẹp giả.
5. **Decision consistency:** nếu có cut score cho placement, đo false classification/indeterminate rate quanh cut; không dùng point estimate đơn độc.
6. **Retest:** với common-anchor forms, ước lượng covariance và SEdiff; kiểm tra reliable-change rule chống practice/form effect.
7. **Sensitivity:** lặp với frequency manifest, lexical unit, response model, missingness/quality gate và domain frame đã được phê duyệt; xuất range thay vì chọn model thuận tiện nhất.
8. **Preply comparison:** chỉ đối chiếu point estimates và interval widths sau khi xác định cùng unit hoặc fit linking study common-person/common-item. Không coi chênh lệch với ±10.33% là validation failure/success nếu chưa biết estimand và sample frame tương đương.

## Gaps còn lại

- Chưa có item-level production data của Preply để ước lượng CSEM, conditional coverage, score-difference error hoặc calibration theo tail.
- Chưa có common-anchor/alternate-form data để xác định covariance và reliable-change threshold cho vocabulary scale.
- Chưa có empirical evidence cho việc chuyển nguyên các quy tắc CSEM của GRE sang vocabulary-size testing; các nguồn ETS/Huebner là nguyên tắc phương pháp, không phải hệ số production.
- Chưa tìm được nguồn xác thực cho một margin universal hoặc hệ số điều chỉnh `±10%` riêng cho Preply ngoài mô tả vendor đã fetch.

## Nguồn đã verify trong iteration 34

- ETS: <https://www.ets.org/pdfs/gre/gre-reliability-standard-error-measurement.pdf> — HTTP 200.
- Huebner & Skar: <https://files.eric.ed.gov/fulltext/EJ1311133.pdf> — HTTP 200.
- CRAN csemTools manual: <https://cran.rstudio.com/web/packages/csemTools/csemTools.pdf> — HTTP 200.
- Preply methodology via verified proxy: <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works> — HTTP 200; direct production endpoint vẫn có gap 403 trong môi trường này.
