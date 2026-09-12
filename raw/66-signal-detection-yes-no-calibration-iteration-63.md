# Iteration 63 — Signal detection, false alarms và calibration prevalence cho yes/no vocabulary tests

## 1. Phạm vi

Direction của iteration này là tách **kiến thức từ vựng** khỏi **response style** trong checklist yes/no. Trọng tâm là confusion matrix của từ thật/nonword, các công thức signal-detection/guessing, khả năng FA (false alarm) đại diện cho overestimation, và cách xây dựng correction có criterion test thay vì áp dụng một hệ số phổ quát.

Kết luận ở đây áp dụng cho thiết kế đề xuất; không phải mô tả implementation nội bộ của Preply. Trang Preply được đọc qua endpoint proxy đã fetch được; production item bank và response-level data của Preply vẫn chưa có.

## 2. Nguồn đã kiểm tra và verify

| Nguồn | HTTP | Nội dung sử dụng |
|---|---:|---|
| Pellicer-Sánchez & Schmitt, *Scoring Yes–No vocabulary tests: Reaction time vs. nonword approaches* | 200 | Confusion matrix H/FA/miss/correct rejection; H−FA, cfg, Δm, Isdt; so sánh nonword và RT; overestimation dù FA=0. |
| Stubbe, ERIC record EJ982188, *Do pseudoword false alarm rates and overestimation rates...* | 200 | Mẫu n=490; FA và overestimation khác hướng theo nhóm năng lực; giới hạn của pseudoword proxy. |
| Stubbe & Stewart, *Optimizing scoring formulas... with linear models* | 200 | Regression dùng YN score + FA; pilot coefficients; item analysis; giới hạn transportability. |
| Stubbe, *Comparing Regression versus Correction Formula Predictions...* | 200 | Holdout Group A/B; regression mới và so sánh với h−f/cfg/Δm/Isdt; cảnh báo phụ thuộc item/quần thể. |
| Preply, *How the vocab test works* qua `r.jina.ai` | 200 | Dictionary/rank universe, hai phase, midpoint/log sampling, definition of word và vendor margin-of-error. Đây là nguồn vendor được proxy hóa; không coi là independent validation. |

## 3. Bằng chứng chính

### 3.1. Yes/no tạo ra bốn loại response, không chỉ một tỷ lệ đúng

Pellicer-Sánchez và Schmitt mô tả mỗi item thật/nonword bằng bốn trạng thái:

- **Hit (H):** trả lời “yes” cho từ thật;
- **False alarm (FA):** trả lời “yes” cho nonword;
- **Miss:** trả lời “no” cho từ thật;
- **Correct rejection:** trả lời “no” cho nonword.

Vì vậy raw hit rate đo self-reported recognition, không phải xác suất đã xác nhận meaning. FA cung cấp bằng chứng về xu hướng đánh dấu “yes”, nhưng không quan sát trực tiếp được việc người làm test có biết nghĩa của từng từ thật hay không.

Các công thức được bài tổng hợp:

```text
h = H / N_real
f = FA / N_nonword

H_minus_FA = h - f
cfg         = (h - f) / (1 - f)
Delta_m     = ((h - f) / (1 - f)) - (f / h)
```

Bài cũng trình bày `I_sdt`, công thức phức tạp hơn của Huibregtse et al. nhằm xét guessing và response style. Các công thức này không đồng nghĩa với nhau và cho thể hiện khác nhau theo hit/FA distribution. Bài tường thuật rằng các nghiên cứu trước đó chưa đạt đồng thuận về phương pháp điều chỉnh tốt nhất; một correction không được coi là universal calibration.

### 3.2. FA không phải thước đo thuần của overestimation

ERIC record của Stubbe báo cáo nghiên cứu trên 490 sinh viên ở 30 lớp thuộc năm đại học Nhật, với TOEIC khoảng 230–730. FA pseudoword của nhóm đại học năng lực cao là 4.28%, nhỉnh hơn nhóm thấp 3.96%; nhưng overestimation đo bằng cách đối chiếu 96 từ thật với multiple-choice criterion lại thấp hơn ở nhóm cao (3.24% so với 5.67%).

Hệ quả thiết kế:

1. Cùng một FA rate có thể tương ứng với mức overestimation khác nhau theo proficiency/reference population.
2. FA nên được đưa vào calibration model hoặc quality flag có điều kiện theo population, không dùng như “số từ phải trừ” cố định.
3. Nonword panel cần pretest riêng: hình thái, orthographic neighborhood và độ giống từ thật có thể làm thay đổi FA.

### 3.3. FA=0 cũng không chứng minh raw score là unbiased

Trong Study 2 của Pellicer-Sánchez và Schmitt, khoảng 80% những người không chọn nonword vẫn thể hiện overestimation theo Criterion B (recall). Điều này làm yếu quy tắc “FA thấp thì tin raw hits”. Không chọn nonword có thể phản ánh response style cẩn trọng, nhưng cũng có thể xảy ra khi người làm test nhầm một từ thật với từ gần dạng hoặc chỉ nhận diện hình thức mà không recall được nghĩa.

Cũng trong bài này, RT-based scoring không cho ưu thế rõ ràng so với nonword approaches. Do đó response time có thể là diagnostic phụ, nhưng không thay thế criterion validation và không nên tự động biến thành correction cho vocabulary count.

### 3.4. Regression có thể tốt hơn correction cố định, nhưng chỉ sau supervised calibration

Stubbe và Stewart đề xuất dùng multiple regression với hai predictor riêng: số real-word được báo là biết (`YN`) và số nonword được báo là biết (`FA`), còn outcome là passive recall được xác minh bằng L2→L1 translation. Pilot 69 người sau loại hai FA outlier cho:

```text
predicted_true_knowledge = 8.14 + 0.41*YN - 1.94*FA
R² = 45.2%
```

Sau item analysis, giữ 40 real words có phi-correlation cao và 9 pseudowords có point-biserial âm mạnh, mô hình đạt R²=59.1%:

```text
predicted_true_knowledge = 3.26 + 0.51*YN - 2.39*FA
```

Đây là bằng chứng rằng FA có thể tăng predictive power khi được fit đồng thời với YN và item đã được kiểm tra. Tuy nhiên chính tác giả gọi kết quả là preliminary và cảnh báo hệ số có thể chỉ phù hợp với test/quần thể tương tự. Không được dùng các hệ số trên cho người dùng hoặc item bank khác.

### 3.5. Holdout là điều kiện tối thiểu để nói correction có ích

Nghiên cứu tiếp theo của Stubbe dùng 455 người; sau loại 24 người có hơn 8 FA, tạo công thức ở Group A và kiểm tra ở Group B. New RF được báo cáo có tương quan 0.845 với passive recall ở Group B, R²=70.56%, và residual nhỏ hơn các correction formulas trong phân tích đó.

Kết quả này ủng hộ workflow `fit → holdout → compare`, nhưng không tạo ra hệ số toàn cầu: bài dùng người học Nhật, item list có cấu trúc cụ thể và outcome passive recall. Production calibration cần split theo người và theo item/form, báo MAE/RMSE/bias, calibration curve và coverage; nếu chỉ fit rồi đánh giá trên cùng sample thì không đủ.

## 4. Đối chiếu với Preply

Trang methodology Preply đã fetch qua proxy HTTP 200 mô tả:

- dictionary trên 45,000 entries, xếp theo frequency của spoken/written English;
- phase đầu khoảng 40 từ trải từ dễ đến khó;
- phase hai khoảng 120 từ trong khoảng hẹp quanh ước lượng ban đầu;
- midpoint của checkbox theo rank, với sample phân bố logarithmically;
- chỉ tính dictionary main entries, xử lý derived forms/subentries theo dictionary;
- công bố margin ±10%, ví dụ 20,000 → 18,000–22,000, và giải thích dựa trên SD≈0.25×estimate, trung bình 22.5 sample points và 1.96×SE.

Trong phần content đã fetch không xuất hiện `pseudoword`, `false alarm`, `sensitivity`, `specificity` hoặc criterion calibration. Vì vậy:

| Thành phần | Thiết kế đề xuất | Preply đã xác minh |
|---|---|---|
| Estimand | Khai báo receptive breadth và lexical unit; raw count tách khỏi criterion-confirmed score | Dictionary main-entry count; không thấy response-bias layer được công bố |
| Sampling | Frequency/rank sampling nhưng phải có item pretest và uncertainty theo band | Hai phase, khoảng 40 + 120, midpoint và log spacing |
| Response bias | Nonword panel + criterion sample; FA là covariate/QC, không phải correction cố định | Chưa tìm thấy pseudoword/FA disclosure trong trang đã fetch |
| Correction | Chọn raw/H−FA/cfg/regression bằng out-of-sample validation | Công bố midpoint estimate và vendor ±10%; chưa có independent calibration trong nguồn này |
| Uncertainty | Tách response/model/sampling/transport uncertainty; interval cần coverage audit | Vendor margin ±10%; chưa có response-level coverage evidence |

`±10%` của Preply là claim/methodology của vendor trong trang được fetch, không nên nhập thẳng làm confidence interval đã được kiểm chứng độc lập.

## 5. Quy tắc estimator và pseudocode đề xuất

### 5.1. Data model tối thiểu

```text
Item {
  item_id, lexical_unit, band_or_rank, is_real_or_nonword,
  nonword_generation_method, neighborhood_features,
  form_version, calibration_population
}

Response {
  person_id, item_id, response_yes_no, response_status,
  elapsed_ms, form_id, position, timestamp
}

Criterion {
  person_id, item_id, confirmed_knowledge,
  criterion_type, rater_or_key_version
}
```

### 5.2. Scoring workflow

```text
function score_yes_no(responses, item_manifest, calibration_model=None):
    split = separate_real_and_nonword(responses, item_manifest)
    h = mean(yes(resp) for resp in split.real)
    f = mean(yes(resp) for resp in split.nonword)

    raw = h
    candidates = {
        "raw": raw,
        "h_minus_f": clamp(h - f, 0, 1),
        "cfg": clamp((h - f) / (1 - f), 0, 1) if f < 1 else null
    }

    if calibration_model is available:
        # model was fit on independent criterion sample and versioned item bank
        p_confirmed = calibration_model.predict(h=h, f=f,
                           band_profile=band_profile(split.real),
                           population=declared_population)
        candidates["supervised"] = clamp(p_confirmed, 0, 1)

    qc = {
        "fa_rate": f,
        "fa_count": count_yes(split.nonword),
        "extreme_fa": flag_by_pre_registered_threshold(f, population),
        "missingness": response_status_audit(responses),
        "item_exposure_or_recall": security_audit(responses)
    }

    estimate = choose_candidate_by_locked_validation(candidates, calibration_model)
    interval = uncertainty_bootstrap_or_posterior(
        responses, item_clusters=True, model=calibration_model,
        include_response_and_sampling_components=True)
    return estimate, interval, qc
```

Sau khi có vocabulary universe gồm `N_b` units mỗi band/rank stratum, transform breadth proportion sang count chỉ khi đã khai báo estimand:

```text
K_hat = sum_b N_b * p_known_b
```

Trong đó `p_known_b` phải là calibrated probability của đúng lexical unit, population và form manifest. Nếu chỉ có raw yes/no và không có criterion model, phát hành `K_raw` cùng interval/quality flag; không gọi nó là “true vocabulary”.

### 5.3. Release gates

- Có nonword items đã pretest; lưu neighborhood/orthographic features và không để tất cả nonword cùng một kiểu hình thái.
- Criterion sample độc lập với item/form scoring sample; criterion phải được chấm theo rule rõ ràng, ưu tiên passive recall/meaning confirmation khi claim là receptive meaning knowledge.
- So sánh raw, H−FA, cfg và supervised model trên holdout; chọn theo predictive error, calibration và subgroup bias, không chọn theo in-sample R².
- Fit riêng hoặc kiểm tra invariance theo proficiency, L1/loanword exposure, intended population và item band.
- Không dùng `FA=0` để bỏ qua uncertainty hoặc tự động coi mọi hit là đã biết nghĩa.
- Nếu chưa có criterion data, không áp dụng hệ số 0.41/1.94, 0.51/2.39 hoặc bất kỳ hệ số lấy từ nghiên cứu khác.

## 6. Validation plan

1. **Item pilot:** tạo real/nonword pool theo band; loại nonword có FA quá thấp do dễ nhận là giả hoặc quá cao do giống từ thật bất thường; kiểm tra item discrimination.
2. **Criterion linking:** cho cùng người làm YN test và criterion meaning/translation test trong khoảng thời gian ngắn; ghi criterion type và rater agreement.
3. **Model comparison:** fit raw, H−FA, cfg, Isdt và supervised model; dùng nested cross-validation hoặc split theo người, thêm split theo form/item để kiểm tra transport.
4. **Calibration:** kiểm tra reliability diagram, calibration slope/intercept, MAE/RMSE, mean bias và coverage của interval theo band/proficiency/L1.
5. **Sensitivity:** mô phỏng FA rate, nonword prevalence, item-neighborhood mix và underestimation; báo range `K_raw`–`K_calibrated` nếu kết luận phụ thuộc response model.
6. **Preply bridge:** chỉ link sang Preply/main-entry scale sau khi có common items hoặc criterion sample chung; không coi midpoint/log sampling tương đương với FA-corrected estimate.

## 7. Gaps

- Chưa có response-level data, pseudoword panel, criterion sample hoặc scoring code của Preply; chưa tìm được nguồn xác thực cho Preply có sensitivity/specificity, FA correction, criterion calibration hay subgroup calibration.
- Các hệ số regression được xác minh là của các mẫu học viên Nhật và item lists cụ thể; chưa có bằng chứng chúng transport sang người học Việt Nam/toàn cầu hoặc sang vocabulary universe của Preply.
- Chưa có calibration đủ để chọn giữa correction cổ điển, regression, IRT hoặc latent-class model cho test mục tiêu.
- Cần xác định criterion “biết một nghĩa” so với recall nhiều nghĩa trước khi gán `confirmed_knowledge` và chuyển xác suất sang vocabulary count.

## 8. Nguồn

- https://www.lextutor.ca/rt/sanchez_schmitt_YN-RT-2012.pdf
- https://eric.ed.gov/?id=EJ982188
- https://teval.jalt.org/sites/default/files/SRB-16-2-Stubbe-Stewart.pdf
- https://vli-journal.org/issues/02.1/issue02.1.07.pdf
- https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works
