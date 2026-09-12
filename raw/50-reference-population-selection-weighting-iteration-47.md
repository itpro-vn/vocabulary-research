# Iteration 47 — Selection bias, reference population và transportability

## Phạm vi

Direction của iteration này là kiểm tra một vấn đề khác với sai số item/IRT: một vocabulary-size score có thể được đo chính xác trên người làm bài nhưng vẫn không đại diện cho quần thể mà báo cáo muốn suy rộng. Trọng tâm là self-selection của test online, reference population, calibration weighting, common support và việc tách measurement uncertainty khỏi population-representativeness uncertainty.

## Nguồn đã verify

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| [AAPOR, *Data Quality Metrics for Online Samples*](https://aapor.org/wp-content/uploads/2023/02/Task-Force-Report-FINAL.pdf) | 200 | Nguồn phương pháp chính về online probability/nonprobability samples, auxiliary variables, weighting, precision và sensitivity. |
| [OPRE/Brick, *Probability and Nonprobability Samples in Surveys: Opportunities and Challenges*](https://acf.hhs.gov/sites/default/files/documents/opre/opre_nonprobability_samples_brief_september2024.pdf) | 200 | Tổng hợp chính sách/phương pháp về opt-in panel, selection bias, positivity, propensity weighting và giới hạn suy rộng. |
| [Preply, *How does the test work?* qua proxy](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) | 200 | Nguồn vendor mô tả estimand và sampling của sản phẩm; không phải bằng chứng độc lập về norm population. |

Direct Preply endpoint `https://preply.com/en/learn/english/test-your-vocab/how-it-works` trả HTTP 403 trong callback; chỉ nội dung fetch được qua proxy được sử dụng.

## Findings đã kiểm chứng

### 1. Self-selection không cho phép gọi kết quả là norm dân số

AAPOR định nghĩa selection mechanism là toàn bộ quá trình coverage, invitation và completion. Với mẫu nonprobability, deviations from random sampling là mặc định; việc hiệu chỉnh dựa trên statistical model đòi hỏi các giả định thường không kiểm chứng được. AAPOR cũng nêu rõ opt-in/recruitment, self-selection và coverage của người không dùng Internet là nguồn systematic error cần đánh giá.

OPRE/Brick nêu cụ thể rằng trong opt-in panel, người tham gia tự chọn vào mẫu; quota age/sex không loại bỏ selection bias của pool. Vì vậy, một test mở cho người dùng tự tìm đến không được dùng như nguồn percentile hoặc “average vocabulary of population” nếu không có sampling frame và calibration evidence.

Đây là vấn đề khác với precision của item sample: có thể có 120 item và khoảng tin cậy nhỏ cho một người, nhưng vẫn không biết người đó có thuộc target population theo cơ chế selection mà norm yêu cầu hay không.

### 2. Weighting chỉ có tác dụng khi auxiliary variables liên quan đúng outcome

AAPOR liệt kê raking, post-stratification, matching/calibration và propensity-score weighting. Các phương pháp này cần auxiliary variables có phân phối đã biết trong population hoặc có reference microdata. Hiệu quả của biến điều chỉnh phụ thuộc đồng thời vào tương quan của biến đó với xác suất được chọn và với outcome.

Suy ra cho vocabulary-size score: cân bằng age, sex hoặc education không tự động sửa bias nếu vocabulary size còn phụ thuộc mạnh vào L1, country, schooling quality, English exposure, migration, occupation, test discovery channel, device/access và động lực làm bài. Một biến chỉ dự báo selection nhưng không dự báo vocabulary có thể làm tăng variance mà không giảm bias. Ngược lại, biến dự báo vocabulary nhưng không liên quan selection chủ yếu giúp giảm variance.

### 3. Cần kiểm tra positivity/common support và giữ nhiều estimate

AAPOR yêu cầu giả định common support/positivity khi suy luận bằng model: mọi nhóm population có tổ hợp auxiliary variables phải có xác suất được đưa vào sample khác 0. OPRE/Brick nhấn mạnh nhóm có xác suất tham gia bằng 0 không thể được phục hồi bằng propensity weighting.

Production nên tạo bảng overlap giữa test sample và reference population cho các cell quan trọng (L1 × age × education × country hoặc các nhóm được định trước), báo tỷ lệ ngoài support và chặn population-weighted norm nếu support quá yếu. Khi support yếu, giữ `K_raw` và `K_weighted` song song, không chọn weighted estimate như “truth”.

### 4. Margin of error không bao gồm selection bias/meta-uncertainty

AAPOR phân biệt random uncertainty với systematic bias. Với online nonprobability sample, confidence interval có thể quá hẹp vì không bao gồm meta-uncertainty về việc adjustment model có đúng không, cũng không bao gồm bias do biến selection bị bỏ sót. Công thức xấp xỉ unequal-weighting effect là `UWE = 1 + CV(w)^2`, với `n_eff ≈ n/UWE`; nhưng công thức này không xử lý đầy đủ clustering, tương quan weight–outcome hoặc các bước propensity/calibration phức tạp.

AAPOR cho rằng bootstrap/jackknife chỉ có giá trị khi tái tạo được toàn bộ design và rerun toàn bộ weighting ở từng replicate. Với nonprobability sample, recruitment process thường không quan sát được, nên resampling ngây thơ từ các respondent có thể đánh giá thấp sampling variability.

Do đó báo cáo phải có ít nhất hai lớp:

- `measurement_interval`: uncertainty có điều kiện trên item bank, response model, form và calibration;
- `representativeness_risk`: đánh giá selection/coverage/common-support và sensitivity giữa các weighting/reference specifications.

Không được dùng margin ±10.33% của Preply như population margin of error. Con số đó là vendor calculation cho sampling estimate của vocabulary items và không chứng minh độ đại diện của người làm bài.

## Quy tắc thuật toán đề xuất

### Dữ liệu cần lưu

```text
respondent_id
K_raw, K_weighted, item_model_version
L1, country, age_group, education_group
English_exposure_proxy, proficiency_proxy, recruitment_source
completion_status, effort_flags, test_date
reference_population_version
weight_method, weight_value, weight_trim_flag
support_status, sensitivity_spec_id
```

`recruitment_source` và các proxy exposure/proficiency phải được thu thập hoặc suy ra theo một quy trình được công khai. Nếu không có reference distribution đáng tin cậy, `weight_value` để null và chỉ công bố descriptive sample estimate.

### Pseudocode

```text
function report_vocabulary_score(responses, target_population, reference_data):
    K_raw = score_breadth(responses, fixed_item_or_IRT_model)

    if reference_data is missing:
        return report(
            K_raw=K_raw,
            measurement_interval=conditional_interval(responses),
            population_status="descriptive_only",
            representativeness="not_established",
            note="chưa tìm được nguồn xác thực cho population norm/selection correction"
        )

    X = predeclared_auxiliaries(responses)
    support = assess_common_support(X, reference_data)
    if support.fails:
        return report(
            K_raw=K_raw,
            measurement_interval=conditional_interval(responses),
            population_status="blocked",
            representativeness="insufficient_common_support",
            sensitivity=run_unweighted_and_trimmed_sensitivity(responses),
            note="không suy rộng population khi nhóm target không có support"
        )

    estimates = []
    for spec in [raking, poststratification, propensity, doubly_robust]:
        w = fit_weights(responses, reference_data, X, spec)
        if diagnostics(w).fail:
            continue
        estimates.append(weighted_K(responses, w))

    if estimates is empty:
        return report(K_raw=K_raw, population_status="descriptive_only",
                      representativeness="adjustment_failed")

    K_weighted = select_predeclared_primary_estimate(estimates)
    weight_sensitivity = interval(min(estimates), max(estimates))
    measurement_interval = conditional_interval(responses, weights=K_weighted.weights)
    population_status = "calibrated_with_model_assumptions"

    return report(K_raw=K_raw, K_weighted=K_weighted,
                  measurement_interval=measurement_interval,
                  representativeness_interval=weight_sensitivity,
                  population_status=population_status,
                  support=support,
                  weighting_diagnostics=diagnostics(w))
```

Đây là tầng reporting/norming, không thay đổi estimand receptive breadth của item test. `K_weighted` không được diễn giải là số từ “đúng hơn” cho từng cá nhân; nó là estimate được transport sang target population dưới các giả định đã công bố.

## So sánh với Preply

| Thành phần | Preply public method | Thiết kế đề xuất |
|---|---|---|
| Item universe | Hơn 45.000 dictionary entries, xếp theo frequency | Giữ corpus/dictionary manifest có version và thêm respondent-population manifest |
| Item sampling | Khoảng 40 item rộng rồi khoảng 120 item hẹp hơn, logarithmic rank, midpoint | Giữ frequency-stratified/IRT estimator đã đề xuất; tách rõ item uncertainty khỏi person-selection uncertainty |
| Per-person margin | Preply nêu ±10.33% cho sampling estimate với khoảng 120 item | Báo conditional measurement interval; không gắn nó với population representativeness |
| Population sampling frame | Không công khai | Bắt buộc công khai target population, recruitment source, inclusion/exclusion và coverage |
| Weighting/reference sample | Không công khai | Chỉ weight khi có reference data, auxiliary variables outcome-relevant và common support |
| Nonresponse/selection | Không công khai | Lưu completion funnel, source, missingness/effort và sensitivity specs |
| Norm/percentile claim | Chưa có bằng chứng public về norming protocol | Chỉ cho percentile sau external benchmark/hold-out validation; nếu thiếu thì `descriptive_only` |

## Assumptions và giới hạn

1. Calibration chỉ có thể giảm selection bias nếu auxiliary variables đủ liên quan đến selection và vocabulary outcome; điều kiện này không thể chứng minh chỉ bằng việc sample khớp demographic margins.
2. Reference sample phải có target population distribution đáng tin và đo cùng các auxiliary variables; nếu chỉ có marginal totals, không dùng phương pháp cần respondent-level propensity model.
3. Weighted measurement interval phải tính lại theo weights/model; UWE chỉ là kiểm tra thô, không phải bảo đảm coverage.
4. Sensitivity range giữa weighting specifications là chỉ báo rủi ro, không phải confidence interval có coverage đã được chứng minh.
5. Không được loại respondent chỉ vì họ thuộc nhóm ít gặp hoặc có score cao/thấp; loại trừ phải theo validity rule độc lập và được pre-register.

## Validation plan

- Thu thập pilot có recruitment đa nguồn và một reference probability sample hoặc benchmark microdata với cùng auxiliary variables.
- So sánh `K_raw`, raking, post-stratification, propensity và doubly robust trên hold-out sample; báo bias, RMSE, coverage và weight dispersion.
- Kiểm tra cell overlap/positivity trước khi fit; stress-test bằng cách bỏ từng auxiliary variable quan trọng.
- Dùng replicate/bootstrap chỉ khi có thể rerun toàn bộ score + weighting pipeline; nếu không, gắn nhãn interval là model-conditional.
- Pre-register target population, primary weighting method, trimming rule, missingness treatment và release thresholds.
- Chỉ mở percentile/norm table sau khi external benchmark cho thấy calibration ổn định theo L1/country/education và các sensitivity range không vượt ngưỡng đã định trước.

## Gap còn lại

Chưa có response-level data, recruitment funnel, L1/country composition, sampling frame, reference sample, weights, common-support diagnostics hoặc norming protocol của Preply. Chưa tìm được nguồn xác thực cho respondent population và quy trình weighting nội bộ của Preply. Vì vậy chưa thể ước lượng một correction coefficient hoặc population margin cụ thể cho score Preply.
