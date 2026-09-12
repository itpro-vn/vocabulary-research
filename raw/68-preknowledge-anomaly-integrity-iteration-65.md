# Iteration 65 — Preknowledge, anomalous responses và integrity layer

## 1. Phạm vi và câu hỏi

Direction mới của iteration này là **phát hiện preknowledge/response anomaly trong bài vocabulary online**, tách khỏi item exposure nói chung: person-fit, secure-item checks, response-pattern similarity, false-positive control và cách xử lý score bị nghi ngờ. Mục tiêu không phải biến anomaly statistic thành một “correction factor” cho số từ, mà là quyết định estimate có đủ hợp lệ để phát hành hay không.

Các nguồn đã fetch và kiểm tra HTTP:

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| [UK Department for Education review](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/690007/Statistical_techniques_for_studying_anomaly_in_test_results-_a_review_of_literature.pdf) | 200 | Tổng quan person-fit, copying/similarity, power và false-positive |
| [University of Minnesota repository — Person-Fit Indices](https://conservancy.umn.edu/server/api/core/bitstreams/e95a1a56-270e-44f2-8b8d-fc0d63b8f77f/content) | 200 | Nghiên cứu về kết hợp scalar, timing và graphical indicators |
| [ETS TOEFL iBT Test Security](https://www.ets.org/toefl/institutions/ibt/about/test-security.html) | 200 | Ví dụ vận hành prevention–detection–communication và score validity |
| [Preply methodology proxy](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) | 200 | Đối chiếu công bố methodology vendor; không phải independent calibration |
| [Preply direct test page](https://preply.com/en/learn/english/test-your-vocab) | 403 | Không dùng làm bằng chứng nội dung trong iteration này |

## 2. Findings đã xác minh

### 2.1 Anomaly không đồng nghĩa với cheating

UK review định nghĩa anomaly là response pattern hoặc score lệch khỏi kỳ vọng của mô hình, người có năng lực tương tự hoặc mẫu tham chiếu. Các nguyên nhân có thể gồm test không phù hợp, careless responding, lucky guessing, random/creative responding và cheating. Vì vậy person-fit chỉ là bằng chứng **misfit với mô hình**, không phải kết luận pháp lý/đạo đức rằng người làm gian lận và cũng không cho biết phải trừ bao nhiêu từ.

Nghiên cứu person-fit tại repository Minnesota cũng mô tả aberrant pattern là pattern lệch IRT kỳ vọng; nguyên nhân còn có low motivation, guessing và thiếu cố gắng. Đây là lý do integrity status phải tách khỏi latent vocabulary ability.

### 2.2 Không nên dùng một cờ duy nhất

Nghiên cứu Minnesota nhấn mạnh chi phí của quyết định invalid score: gán nhãn sai có thể gây mất cơ hội, tổn thất tài chính hoặc tổn hại tâm lý; vì vậy nên thu thập nhiều nguồn bằng chứng. Trong CBT, timing có thể là một input, nhưng nên kết hợp với chỉ số scalar và đồ thị/response curve, thay vì dùng một ngưỡng của `lz` hoặc một response time cutoff.

UK review cũng cho rằng các chỉ số khác nhau có power khác nhau theo loại hành vi. Một production VST nên có ít nhất:

- `person_fit_scalar`: ví dụ standardized likelihood hoặc chỉ số tương đương sau calibration;
- `secure_item_residual`: fit trên secure/low-exposure subset;
- `response_process`: timing/rapid-guess signal đã được hiệu chuẩn riêng;
- `similarity_signal`: chỉ khi có nhiều response vectors cùng form và nhóm tham chiếu đủ lớn;
- `content/exposure metadata`: item version, exposure count, anchor/secure status.

Các signal này tạo thành bằng chứng cho `valid`, `review` hoặc `invalid`; chúng không sửa trực tiếp `K_hat`.

### 2.3 Ngưỡng person-fit phụ thuộc test design

UK review tổng hợp rằng power và false-positive rate phụ thuộc ability distribution, difficulty/discrimination distribution, test length, loại và tỷ lệ misfit. Các mô phỏng được review có detection rate thay đổi khoảng 35–98% ở false-alarm rate 5% tùy điều kiện; một nghiên cứu khác có detection trung bình khoảng 37% cho test 30 item và 51% cho 60 item. Đây là số của các mô phỏng/test cụ thể, không phải margin dùng cho vocabulary test.

Hệ quả: threshold phải được tạo bằng Monte Carlo trên item parameters, band mix, response model, test length và tỷ lệ contamination dự kiến của chính VST. Cần report operating characteristic (sensitivity, specificity/false-positive rate, PPV theo prevalence) trước khi bật automatic invalidation.

### 2.4 Exposed items làm residual detection yếu đi

UK review mô tả một failure mode quan trọng: nếu item difficulty được ước lượng từ production responses đã bị nhiều người có preknowledge làm đúng, item exposed trông dễ hơn thật; residual giữa observed và expected response giảm, làm residual-based person-fit kém nhạy. Review ghi nhận phương pháp so sánh mô hình một-factor với mô hình có factor thứ hai cho nhóm item bị compromise có thể robust hơn trong một số điều kiện mô phỏng.

VST vì vậy cần một tập `secure_items`/anchors có exposure thấp, được bảo vệ và dùng để:

1. neo item parameters độc lập với suspected exposed items;
2. tính `secure-only` person-fit;
3. so sánh score/all-items với score/secure-items;
4. phát hiện item drift/compromise ở cấp item bank.

Không được coi difficulty fit từ toàn bộ production response là ground truth khi đang điều tra exposure.

### 2.5 Copying/similarity phải condition theo ability và cỡ mẫu

UK review mô tả copying indices bằng overlap giữa response vectors, thường chú ý identical incorrect answers hoặc cả đúng+sai, rồi so với overlap kỳ vọng của người có raw score/ability tương tự. Overlap phụ thuộc mạnh vào số câu sai của copier/source; hai người ability cao có ít câu sai nên matching incorrect answers tự nhiên thấp, còn nhóm ability thấp có thể matching nhiều hơn.

Với nhóm tham chiếu nhỏ, review nêu ví dụ dưới khoảng 100 người, subgroup empirical của K-index có thể nhỏ và độ chính xác suy giảm; khi đó cần approximation khác hoặc không đưa ra quyết định tự động. Một session cá nhân không đủ để kết luận copying bằng similarity index.

### 2.6 Integrity cần là lớp vận hành riêng

Trang ETS chính thức mô tả ba lớp `prevention`, `detection`, `communication`, đồng thời nêu monitoring, investigation và score validity. Đây là pattern vận hành phù hợp cho VST:

- prevention: randomization/server-side delivery, exposure caps, secure anchors, form rotation;
- detection: person-fit, secure-item checks, item exposure/response similarity và process diagnostics;
- communication: trạng thái score, lý do review/invalid, audit trail và quy trình khiếu nại.

Đây chỉ là nguyên tắc từ ETS, không phải bằng chứng Preply có các cơ chế này.

## 3. Thuật toán đề xuất

### 3.1 Data model tối thiểu

```text
item:
  item_id, bank_version, band_id, lexical_unit_id
  a, b, c_or_guessing, content_flags
  secure_flag, exposure_count, exposure_window

response:
  person_id, item_id, form_id, answer, correct
  rt_ms, timestamp, display_order, response_status

integrity_result:
  person_fit_all, person_fit_secure, timing_signal
  similarity_signal, exposure_risk, secure_score_gap
  integrity_status ∈ {valid, review, invalid, insufficient_evidence}
  evidence_version, threshold_calibration_id
```

### 3.2 Pseudocode

```text
calibrate(item_bank, reference_sample):
    fit intended IRT/response model on clean calibration data
    designate secure anchors with low exposure and stable parameters
    simulate honest, careless, guessing, preknowledge and copying patterns
    estimate null distribution and operating curves for each signal
    choose review/invalid thresholds for target false-positive rate
    return versioned calibration and thresholds

score(response_vector, item_bank, calibration):
    K_all, CI_all = vocabulary_estimate(response_vector, item_bank)
    secure = responses where item.secure_flag and exposure_count <= cap
    K_secure, CI_secure = vocabulary_estimate(secure, secure_item_parameters)

    pf_all = person_fit(response_vector, calibrated_item_parameters)
    pf_secure = person_fit(secure, secure_item_parameters)
    timing = calibrated_response_process_signal(response_vector)
    similarity = similarity_signal_if_reference_group_exists(response_vector)
    gap = standardized_difference(K_all, K_secure, covariance_if_available)

    evidence = combine_only_after_validation(
        pf_all, pf_secure, timing, similarity, gap, exposure_metadata
    )
    if evidence.has_data_quality_failure:
        status = insufficient_evidence
    elif evidence.meets_invalid_rule and evidence.confirmed_by_independent_signal:
        status = invalid
    elif evidence.meets_review_rule:
        status = review
    else:
        status = valid

    return K_all, CI_all, status, evidence
```

### 3.3 Quy tắc quyết định bảo thủ

- `valid`: không có signal vượt threshold đã được calibration; secure subset đủ item; không có missingness/technical failure.
- `review`: một signal mạnh hoặc nhiều signal yếu cùng hướng, nhưng chưa đạt PPV/false-positive gate; phát hành provisional/no-public score tùy use case.
- `invalid`: chỉ khi có bằng chứng độc lập hoặc policy-confirmed compromise, ví dụ secure-item misfit + exposure evidence, hoặc copying evidence đã được kiểm soát theo ability và cỡ mẫu.
- `insufficient_evidence`: secure subset quá ngắn, nhóm tham chiếu quá nhỏ, hoặc calibration không transport được; không đổi thành “zero vocabulary”.

Không dùng `K_corrected = K_all - f(anomaly)` vì literature không cung cấp một hàm chuyển anomaly thành số từ và anomaly có thể do carelessness, guessing, construct mismatch hoặc technical behavior.

## 4. Độ không chắc chắn và validation

Tách ít nhất bốn thành phần:

1. `U_response`: uncertainty của response/IRT score;
2. `U_item_sampling`: uncertainty do band/item sample;
3. `U_integrity`: sensitivity range khi loại suspected items hoặc thay calibration model;
4. `U_transport`: thay đổi theo population, modality, form và exposure regime.

Có thể báo sensitivity envelope:

```text
K_base = estimate(all eligible items)
K_secure = estimate(secure-only items)
K_cleaned = estimate(exclude items with confirmed compromise)
Integrity sensitivity = [min(K_base, K_secure, K_cleaned),
                        max(K_base, K_secure, K_cleaned)]
```

`K_secure` không được coi là unbiased tự động vì secure subset có thể lệch frequency band; phải tái trọng số theo band hoặc fit model có anchors. CI của `K_base` chỉ phát hành khi integrity status hợp lệ; với `review`, báo interval conditional và sensitivity, không báo một điểm chính xác giả tạo.

Validation plan:

1. Tạo calibration sample với item exposure thấp và criterion vocabulary/meaning check độc lập.
2. Tạo simulation grid: test length 30/60/120; band difficulty/discrimination; 0–30% preknowledge; careless/rapid guessing; copying; multiple L1/domain groups.
3. Ước lượng false-positive rate trên honest responders; sensitivity và PPV theo prevalence contamination.
4. Hold out forms/persons; kiểm tra threshold có giữ được false-positive khi đổi form và population.
5. Thử planted compromise trên một phần item, giữ secure anchors, so sánh `pf_all` với `pf_secure`.
6. Audit ảnh hưởng tới `K_hat`, band profile và coverage; không chỉ tối ưu AUC của detector.
7. Pilot human review cho các ca `review`; đo agreement và appeal outcomes trước automatic invalidation.
8. Theo dõi drift theo bank version và exposure window; không reuse threshold khi item parameters/form thay đổi đáng kể.

## 5. Đối chiếu Preply

| Thành phần | Preply methodology đã fetch | Thiết kế đề xuất |
|---|---|---|
| Universe | Khoảng 45.000 dictionary entries/main entries theo mô tả vendor | Versioned universe, item/lexical-unit manifest |
| Sampling | Phase đầu khoảng 40 từ trải dễ–khó; phase hai khoảng 120 từ quanh estimate | Stratified/adaptive nhưng giữ secure anchors và exposure metadata |
| Scoring | Midpoint của checkbox theo rank logarithmic; vendor mô tả ±10% | IRT/stratified estimator + integrity status và uncertainty decomposition |
| Preknowledge/security | Nội dung methodology proxy không công bố person-fit, secure subset, exposure cap hay similarity policy; direct page trả 403 | Prevention–detection–communication layer, thresholds mô phỏng trên item bank |
| Pseudoword/criterion check | Trong trang đã fetch không thấy pseudoword hoặc criterion calibration; chưa tìm được nguồn xác thực cho response-bias/integrity calibration của Preply | Có thể thêm secure/criterion panel, nhưng chỉ dùng sau validation, không correction tùy ý |
| Quyết định score | ±10% là claim vendor gắn với sample/SD assumption cụ thể | Không gộp integrity uncertainty vào một ±10%; báo status, sensitivity và CI đã calibration |

So sánh này không chứng minh Preply không có cơ chế nội bộ; nó chỉ ghi nhận những gì trang methodology đã fetch công khai và những gì chưa xác minh được.

## 6. Gaps còn lại

- Chưa có response-level data, current item bank, exposure log, form assignment hoặc secure-anchor list của Preply.
- Chưa tìm được nguồn xác thực cho threshold vocabulary-specific của `lz`, timing, similarity hay score invalidation của Preply.
- Các detection rates trong UK review là kết quả mô phỏng/nghiên cứu test khác; chưa được chuyển thành ngưỡng cho short vocabulary test.
- Chưa có sample thực để ước lượng PPV, vì PPV phụ thuộc prevalence của preknowledge/cheating.
- Chưa xác định được một secure subset có đại diện đủ cho mọi frequency band; nếu secure items lệch band, `K_secure` cần reweighting hoặc mô hình hierarchical.

## 7. Kết luận iteration

Integrity detection nên là **release gate**, không phải phép trừ vào số từ. Person-fit cần calibration theo test design; multiple indicators và secure-item analysis tốt hơn một cờ đơn; copying similarity cần ability conditioning và sample đủ lớn; mọi threshold phải qua simulation/hold-out với false-positive control. Preply công khai sampling/midpoint/margin nhưng chưa xác minh được lớp integrity tương ứng.
