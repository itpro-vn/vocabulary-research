# Iteration 62 — Longitudinal change và reliable-growth interpretation

## 1. Phạm vi

Direction của iteration này là phân biệt **tăng điểm quan sát được** với **tăng vocabulary size có thể quy cho người học**. Trọng tâm là common-item/form equating, practice effects, facet của occasion/position và reliable change. Không suy ra cơ chế này là cơ chế đang chạy trong Preply: endpoint Preply được kiểm tra trong callback trả HTTP 403.

## 2. Nguồn đã kiểm tra

| Nguồn | HTTP | Bằng chứng dùng trong iteration |
|---|---:|---|
| Akase, *Longitudinal measurement of growth in vocabulary size using Rasch-based test equating* | 200 | 189 học sinh; VST 1–3 theo dõi 3 năm; VST 4 làm linking form; Rasch common logit scale; raw-score và Rasch method; practice/testing effects. |
| Holster & Lake, *Modeling vocabulary size using many-faceted Rasch measurement* | 200 | 1.872 người học; facets Person, Item, Time, Position; concurrent equating; item position có ảnh hưởng substantive đến difficulty. |
| Guhn, Forer & Zumbo, *Reliable Change Index* | 200 | Định nghĩa RCI, SE của difference, biến thể công thức và các giả định cần công khai. |
| ETS, *Standards for Quality and Fairness* | 200 | Yêu cầu về population/comparability, anchors, equating assumptions, SE, model fit và rule của adaptive test. |
| Akase, *The Role of Vocabulary Learning Strategies in Longitudinal Vocabulary Growth* (TESL-EJ 2026) | 200 | VST 1–4 equated; sáu band 1K–6K, mỗi band 26 item; Rasch-estimated VS tăng theo các wave; mô tả mục tiêu giảm practice effects. |
| Preply test endpoint | 403 | Không dùng làm bằng chứng tích cực; chỉ ghi gap. |

## 3. Findings chính

### 3.1. Không equate thì không thể tách growth khỏi form difficulty

Akase theo dõi cùng một cohort qua ba form VST được thiết kế tương đương nhưng trước đó chưa được formal equating. Một form thứ tư lấy item từ VST 1–3 được dùng làm link. Bốn form được đặt lên một logit scale bằng Rasch; các form fit tốt và chênh lệch độ khó gốc nhỏ. Kết luận áp dụng được cho thiết kế là: cùng số item, cùng frequency bands hoặc cùng nhãn form không đủ để tuyên bố hai điểm comparable.

`observed_change = learner_change + form/occasion_effect + error`

Muốn ước lượng `learner_change`, phải loại hoặc mô hình hóa form/occasion effect bằng common items, linking form, hoặc concurrent calibration trên item bank chung.

### 3.2. Common anchor phải được bảo vệ và kiểm tra invariance

Trong nghiên cứu Akase, VST 4 lấy item từ các form cũ theo từng band để nối thang. Đây là một mẫu thiết kế phù hợp hơn việc re-use nguyên form cho mọi lần đo: người học không thấy toàn bộ đáp án cũ, nhưng scale vẫn có cầu nối.

Production rule đề xuất:

- `anchor_id`, `form_version`, `occasion`, `display_position` và item exposure phải có trong log;
- anchor được bảo mật, có exposure cap và không dùng để phát hành điểm nếu item đã bị lộ rộng;
- fit, difficulty drift và DIF của anchor phải được kiểm tra sau mỗi wave;
- nếu anchor không invariant, không ép form về cùng scale; tạo version/scale mới và báo discontinuity.

### 3.3. Rasch theta phù hợp hơn raw band score cho so sánh dọc

Nguồn Akase mô tả raw score method là tỷ lệ đúng trong một band nhân quy mô band, còn Rasch method dùng toàn bộ item để ước lượng xác suất người học biết từng item. Hai phương pháp gần nhau nhưng không đồng nhất. Vì difficulty không do frequency quyết định hoàn toàn, raw score của một band có thể bị form composition chi phối.

Với estimator đã có IRT calibration, nên lưu:

- `theta_t`, `SE_theta_t` hoặc posterior draws;
- `K_hat_t = sum_b N_b * mean_i P(known_i | theta_t, b)`;
- `K_draws_t` để tính thay đổi trực tiếp trên cùng estimand;
- band profile và `K_hat` tổng, không chỉ một raw percentage.

Không nên gọi `K_hat_t2 - K_hat_t1` là “số từ học thêm” nếu form chưa equate hoặc nếu estimand/word-unit/corpus manifest thay đổi.

### 3.4. Time và item position là facets có thể làm sai growth

Holster & Lake dùng many-faceted Rasch, thêm `Time of administration` và `Position` vào Person/Item. Abstract báo cáo data-model fit đủ để local linking và so sánh score gains, nhưng item placement trong form có ảnh hưởng đáng kể đến difficulty. Vì vậy, dù item bank đã calibrate, một form đặt item khó dồn về cuối hoặc khác điều kiện occasion có thể tạo delta giả.

Production controls:

1. randomize/cân bằng position trong pilot và lưu permutation;
2. đưa position/occasion vào facet model hoặc chứng minh hiệu ứng không material;
3. kiểm tra speededness, low-effort và missingness theo wave;
4. không dùng raw score change để bù bằng một correction factor position/time cố định trước khi có pilot vocabulary-specific.

### 3.5. Reliable Change Index là decision layer, không phải vocabulary conversion

Guhn, Forer & Zumbo mô tả:

`RCI = (X_time2 - X_time1) / SE_difference`

Trong classical test theory, một dạng SE difference dùng variance và reliability của hai occasion:

`SE_diff = sqrt( Var1*(1-r1) + Var2*(1-r2) )`

Một dạng với giả định variance và retest reliability dùng chung là:

`SE_diff = SD * sqrt(2*(1-r_retest))`

Nguồn nhấn mạnh RCI có nhiều biến thể; chọn công thức phải phù hợp reference sample, reliability và dữ liệu đang có. `|RCI| ≈ 1.96` chỉ là quy ước kiểm định hai phía dưới giả định chuẩn, không phải ngưỡng phổ quát “tăng 1.96 từ”.

Trong IRT/Bayesian production, ưu tiên cách tương đương nhưng sát model hơn:

`Delta_theta = theta_2 - theta_1`

`SE_Delta = sqrt(SE_2^2 + SE_1^2 - 2*Cov(theta_1, theta_2))`

hoặc lấy trực tiếp:

`Delta_K^(m) = K_2^(m) - K_1^(m)` cho từng posterior draw `m`.

Báo cáo nên có `Delta_K`, interval của `Delta_K`, và một cờ decision `reliable_growth` chỉ khi các release gates đều đạt.

## 4. Thuật toán longitudinal đề xuất

### 4.1. Data model tối thiểu

```text
Attempt {
  person_id, occasion_id, form_id, form_version,
  item_id, response, response_status,
  display_position, elapsed_ms, exposure_count,
  language_variant, device_mode, timestamp
}

CalibrationManifest {
  item_version, corpus_version, lexical_unit,
  band, anchor_set_version, theta_scale,
  item_parameters, position/occasion facet parameters,
  calibration_population, calibration_date
}
```

### 4.2. Pseudocode

```text
function score_longitudinal(attempt_t1, attempt_t2, manifest):
    assert same declared_construct(manifest_t1, manifest_t2)
    assert same lexical_unit_and_corpus_or_explicit_link()

    qc1 = run_response_qc(attempt_t1)
    qc2 = run_response_qc(attempt_t2)
    if qc1.invalid or qc2.invalid:
        return report(status="not interpretable", reason=qc1/qc2)

    link = check_anchor_invariance_and_form_fit(manifest_t1, manifest_t2)
    if not link.pass:
        return report(status="score change observed, not equated growth",
                      reason=link.failure)

    theta1 = estimate_theta(attempt_t1, item_parameters,
                            position_facet, occasion_facet)
    theta2 = estimate_theta(attempt_t2, item_parameters,
                            position_facet, occasion_facet)

    K1_draws = transform_theta_to_K_draws(theta1, manifest_t1)
    K2_draws = transform_theta_to_K_draws(theta2, manifest_t2)
    delta_draws = paired_or_covariance_aware_difference(K2_draws, K1_draws)

    delta_K = median(delta_draws)
    interval = quantile(delta_draws, [0.025, 0.975])
    rci = delta_K / se(delta_draws)
    mdc95 = 1.96 * se(delta_draws)

    reliable_growth = (
        interval.lower > 0 and
        anchor_invariance_pass and
        form_fit_pass and
        position_occasion_effect_within_calibrated_range and
        practice_exposure_audit_pass and
        no_construct_or_population_shift
    )

    return {
      "K_t1": summarize(K1_draws),
      "K_t2": summarize(K2_draws),
      "delta_K": delta_K,
      "delta_interval": interval,
      "RCI_or_model_z": rci,
      "MDC95": mdc95,
      "reliable_growth": reliable_growth,
      "flags": all_failed_gates
    }
```

### 4.3. Decision labels

| Điều kiện | Nhãn nên phát hành |
|---|---|
| Form/anchor link fail hoặc construct/corpus thay đổi | `not comparable` |
| Link pass nhưng interval của delta chứa 0 | `no reliable change detected` |
| Link pass, interval dương, QC/practice/position pass | `reliable growth detected` |
| Delta dương nhưng exposure, practice hoặc position chưa audit | `observed increase; attribution uncertain` |
| Chỉ có raw score ở hai form khác nhau | `raw change only; do not claim growth` |

`MDC95 = 1.96 * SE_Delta` là ngưỡng measurement-error decision dưới giả định hai phía chuẩn hóa. Nếu mục tiêu là phát hiện growth một phía, preregister ngưỡng và interval tương ứng; không đổi ngưỡng sau khi xem kết quả.

## 5. So sánh với Preply

| Thành phần | Đề xuất research-grade | Preply đã xác minh trong iteration 62 |
|---|---|---|
| Same-scale longitudinal score | Rasch/IRT common scale, common anchors hoặc linking form | Chưa xác minh; endpoint trả 403 |
| Form difficulty | Concurrent calibration, anchor drift và fit checks | Chưa tìm được nguồn xác thực |
| Practice/retest | Alternate secure forms, exposure log, practice audit | Chưa tìm được nguồn xác thực |
| Time/position facets | Log occasion/position; facet model hoặc pilot chứng minh negligible | Chưa tìm được nguồn xác thực |
| Change statistic | `Delta_K`, model interval/posterior draws; RCI chỉ là decision aid | Chưa tìm được nguồn xác thực |
| User wording | Tách “observed increase” và “reliable growth” | Chưa xác minh có báo longitudinal change |

## 6. Validation plan

1. **Anchor pilot:** tạo tối thiểu hai alternate forms theo cùng blueprint; ước lượng item difficulty, anchor invariance, fit và common-person/common-item linking.
2. **No-growth retest sample:** cho một nhóm làm lại trong khoảng thời gian ngắn với exposure được kiểm soát để ước lượng test–retest error và practice effect.
3. **Growth sample:** theo dõi cohort có can thiệp/learning exposure đã ghi nhận; so sánh Rasch-linked delta với raw-score delta.
4. **Facet audit:** randomize position, cân bằng form order, ghi thời gian/thiết bị; fit model có/không có position/occasion để đo distortion.
5. **Coverage:** mô phỏng latent theta và response data theo band; kiểm tra coverage của interval `Delta_K` và false-positive rate của `reliable_growth`.
6. **Sensitivity:** so sánh RCI cổ điển, SE difference từ model và posterior paired draws; nếu kết luận đổi theo phương pháp, chỉ phát hành `growth evidence sensitive to model`.
7. **Security/practice:** theo dõi anchor exposure, overlap, retest delay và item recall; loại các wave có contamination không thể định lượng.
8. **Reporting:** luôn ghi calibration population, form/anchor versions, SE, interval, failed gates và declared lexical unit.

## 7. Gaps

- Chưa có response-level/item-bank data của Preply để ước lượng test–retest reliability, practice effect, anchor stability, form drift, position effect hoặc `SE_Delta`.
- Chưa tìm được nguồn xác thực cho Preply có alternate forms, Rasch/IRT equating hay reliable-change reporting.
- Kết quả Akase và Holster/Lake là bằng chứng từ các VST/learner populations cụ thể; không được chuyển thẳng ngưỡng `MDC`, reliability hoặc form parameters sang Preply.
- Cần calibration riêng cho target population, lexical-unit definition, corpus version và intended use trước khi phát hành “số từ tăng thêm”.

## Nguồn

- https://link.springer.com/article/10.1186/s40468-022-00155-8
- https://teval.jalt.org/sites/default/files/26_01_01_Holster_Lake_vocab_size_0.pdf
- https://gwern.net/doc/psychology/2014-gunn.pdf
- https://www.ets.org/pdfs/about/standards-quality-fairness.pdf
- https://tesl-ej.org/pdf/ej118/a6.pdf
- https://preply.com/en/learn/english/test-your-vocab (HTTP 403 trong callback; gap, không dùng làm evidence)
