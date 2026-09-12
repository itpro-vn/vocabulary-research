# Iteration 28 — Low-stakes online effort, satisficing và context thiết bị

## 1. Câu hỏi

Một vocabulary-size test trực tuyến thường có stakes thấp: người làm bài không bị điểm số, chứng chỉ hay quyết định chính thức chi phối. Vì vậy, một câu trả lời sai có thể phản ánh không chỉ không biết từ mà còn thiếu nỗ lực, rapid guessing, gián đoạn hoặc bất tiện do thiết bị. Iteration này kiểm tra cách dùng các tín hiệu đó mà không biến chúng thành một phép đo vocabulary giả tạo.

Kết luận chính: **effort và context là lớp validity/uncertainty, không phải thành phần trực tiếp của số từ**. Không được cộng/trừ vocabulary chỉ vì người dùng trả lời nhanh, chậm, dùng điện thoại hoặc tự báo cáo rằng mình đã cố gắng.

## 2. Bằng chứng đã kiểm tra

| Nguồn | Trạng thái URL | Bằng chứng liên quan | Hệ quả cho estimator |
|---|---:|---|---|
| Pools & Monseur, *Student test-taking effort in low-stakes assessments: evidence from the English version of the PISA 2015 science test*, Large-scale Assessments in Education. [Springer](https://link.springer.com/article/10.1186/s40536-021-00104-6) | HTTP 200 | Bài viết lập luận rằng khi bài test không có hậu quả, người làm có thể không nỗ lực đủ; điểm khi đó phản ánh đồng thời năng lực và động lực thấp. Hai người có cùng proficiency có thể nhận ability estimate khác nhau do motivation. | Điểm thấp phải được diễn giải có điều kiện bởi effort-validity; không kết luận người học mất vocabulary nếu có dấu hiệu disengagement. |
| Kong, Wise & Bhola, *Setting the Response Time Threshold Parameter to Differentiate Solution Behavior From Rapid-Guessing Behavior*. [ERIC PDF](https://files.eric.ed.gov/fulltext/ED490202.pdf) | HTTP 200 | Nghiên cứu phân biệt solution behavior với rapid guessing trong low-stakes computer-based test. Response-Time Effort (RTE) là tỷ lệ item có solution behavior, dùng để đo test-taking effort, không phải kiến thức; RTE nằm trong khoảng 0–1. | Gắn cờ rapid-guess ở cấp item và tính RTE-like index ở cấp phiên. Dùng để cảnh báo/widen uncertainty/review, không trừ điểm từ estimate. |
| Knekta & Eklöf, *The effect of self-reported effort on the validity of low-stakes assessments*. [Trames PDF](https://kirj.ee/public/trames_pdf/2019/issue_3/Trames-3-2019-353-376.pdf) | HTTP 200 | RTE có predictive power lớn hơn self-reported effort (SRE), nhưng SRE bổ sung thông tin. Tương quan RTE–SRE chỉ vừa phải trong các nghiên cứu được bài tổng hợp; self-report có thể thiên lệch hoặc được trả lời hời hợt. | Có thể dùng một câu hỏi effort sau test như tín hiệu thứ hai, nhưng không dùng nó làm ground truth. Bất đồng timing–SRE là lý do để gắn cờ, không phải tự động loại người làm. |
| Passell et al., *Cognitive test scores vary with choice of personal digital device*. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8568735/) | HTTP 200 | Nghiên cứu online trên lượng lớn người tham gia cho thấy device latency/input type làm thay đổi response time; bài cũng báo cáo khác biệt nhỏ giữa nhóm thiết bị ở accuracy của vocabulary measure không giới hạn thời gian. Các khác biệt có thể còn bị confound bởi thành phần nhóm. | Nếu dùng latency để QC, phải lưu device class/input/browser context và calibrate ngưỡng theo context hoặc làm ngưỡng robust. Không chuyển khác biệt thiết bị của nghiên cứu này thành correction số từ khi chưa có pilot vocabulary-size riêng. |
| Preply methodology page. [Preply](https://preply.com/en/learn/english/test-your-vocab/how-it-works) | HTTP 403 | Direct fetch trả challenge Cloudflare/JavaScript; không kiểm tra được timing limit, logging, rapid-guessing filter, attention check, device restriction, effort measure hoặc quality filter. | Preply phải mang cờ `controls_unknown`; không giả định điểm Preply đã effort-adjusted hoặc device-calibrated. |

HTTP statuses được re-check bằng `curl -L` với browser User-Agent trong callback: bốn nguồn học thuật trả 200; trang Preply trả 403. Nguồn PMC có thể trả challenge phụ thuộc đường truy cập; claim trong finding được đối chiếu qua bản full-text/indexed record của bài, và status URL chính vẫn được ghi rõ ở trên.

## 3. Quy tắc production đề xuất

### 3.1 Lưu response process nhưng tách khỏi điểm vocabulary

Mỗi response nên lưu:

```text
Response {
  item_id,
  answer,
  correct,
  latency_ms,
  rapid_guess_flag,
  device_class,
  input_type,
  browser_context,
  interrupted,
  skipped
}
Session {
  effort_self_report_optional,
  rse_or_rte_index,
  effort_conflict_flag,
  quality_status,
  uncertainty_multiplier,
  estimate_status
}
```

`correct` vẫn là dữ liệu dùng trong estimator. `latency_ms`, device và self-report chỉ đi vào diagnostics/validity. Không dùng một ngưỡng thời gian phổ quát nếu chưa có phân phối latency theo item, device và nhóm proficiency.

### 3.2 Rapid guessing / RTE-like index

Sau calibration trên pilot, đặt ngưỡng rapid-guess theo item hoặc theo difficulty/context. Không đặt ngưỡng bằng một con số lấy từ nghiên cứu khác. Với `m` item có response hợp lệ:

```text
RTE_hat = number_of_solution_behavior_items / m
rapid_rate = number_of_rapid_guess_items / m
```

RTE là chỉ báo effort. Khi item bị rapid-guess, có ba chính sách an toàn theo mức độ:

1. **Ít rapid guessing:** giữ response trong estimate, nhưng xuất diagnostic.
2. **Rapid guessing tập trung ở một cụm:** dùng cluster-aware bootstrap hoặc tăng CI/interval; kiểm tra liệu cụm đó có phải một band/device/context cụ thể không.
3. **Rapid guessing cao hoặc phiên không đủ thông tin:** trả `low_effort`/`invalid_or_incomplete` thay vì xuất một con số vocabulary có vẻ chính xác.

Không được coi rapid response là `wrong` mặc định và cũng không được coi rapid response là `known`; đây là trạng thái response-process cần quy tắc riêng.

### 3.3 Kết hợp timing, self-report và thiết bị

Một cổng conservatively calibrated có thể dùng:

```text
if missing_device_context:
    do_not_apply_device_specific_latency_rule

signals = {
    rse_index,
    rapid_rate,
    timeout_rate,
    completion_rate,
    effort_self_report,
    device_context_known
}

if rapid_rate >= calibrated_high_rapid_rate:
    quality_status = "low_effort_review"
    report_estimate = false
elif completion_rate < calibrated_min_completion:
    quality_status = "insufficient_response"
    report_estimate = false
elif timing_selfreport_disagree_strongly:
    quality_status = "effort_conflict"
    report_estimate = true
    inflate_or_sensitivity_report = true
else:
    quality_status = "usable_with_diagnostics"
```

Các ngưỡng `calibrated_high_rapid_rate`, `calibrated_min_completion` và quy tắc `timing_selfreport_disagree_strongly` là **tham số cần pilot**, chưa có nguồn nào trong iteration này cung cấp ngưỡng phổ quát cho vocabulary-size test. Chỉ số effort không được đưa vào công thức:

```text
V_hat = sum_b N_b * p_hat_b
```

thay vào đó, nó quyết định `quality_status`, lựa chọn CI/sensitivity, hoặc yêu cầu làm lại bài.

### 3.4 Device/context

- Ghi tối thiểu mobile/desktop/tablet, hệ điều hành/browser nếu có thể thu thập an toàn, input type và viewport class.
- Dùng device-aware latency calibration: ước lượng phân vị latency theo device × item type × proficiency trong pilot.
- Nếu không có device metadata, bỏ qua correction theo thiết bị và không biến thời gian thô thành bằng chứng effort.
- Với accuracy, chỉ thêm device vào model/sensitivity khi hold-out chứng minh hiệu ứng ổn định và không chỉ là confounding của nhóm người dùng.
- Không khóa điện thoại hoặc ép desktop nếu mục tiêu là public online testing, trừ khi sản phẩm đã công bố mode restriction và equating.

## 4. Tác động đến độ không chắc chắn

Báo cáo nên tách:

1. `CI_sampling_or_response`: sai số do item/response trong estimator vocabulary.
2. `CI_model`: sai số item model, calibration và transform.
3. `effort_sensitivity_range`: khoảng estimate khi giữ nguyên response nhưng áp dụng các quy tắc hợp lý khác nhau cho rapid-guess/low-effort.
4. `context_sensitivity_range`: thay đổi khi phân tích theo device/context hoặc loại các context chưa đủ thông tin.

Không gọi `effort_sensitivity_range` là CI thống kê thông thường. Nếu low-effort có khả năng làm downward bias, lựa chọn an toàn là xuất:

```text
estimate = V_hat
sampling_CI = [L, U]
quality_status = "low_effort_review"
effort_adjusted_count = null
interpretation = "conditional_on_observed_engagement"
```

Một correction tăng số từ để “bù” thiếu effort chỉ được phép sau calibration có criterion/hold-out và coverage; hiện chưa có bằng chứng xác thực để chọn correction như vậy.

## 5. So sánh với Preply

| Thành phần | Estimator đề xuất | Preply có thể xác minh hiện tại |
|---|---|---|
| Số vocabulary | Từ frequency-stratified/IRT-calibrated response, giữ đúng unit/universe | Các iteration trước đã ghi nhận Preply có headword-scale midpoint/logarithmic methodology; không có response-level/item-bank để kiểm tra độc lập |
| Effort | RTE/rapid-guess + self-report tùy chọn; chỉ validity/uncertainty | Chưa xác minh được |
| Device | Lưu context; calibrate hoặc không áp dụng latency correction khi thiếu context | Chưa xác minh được |
| Điểm thấp | Conditional interpretation; có thể không xuất estimate nếu low-effort nghiêm trọng | Không thể biết có quality gate hay không |
| Uncertainty | Sampling/model/construct + effort/context sensitivity riêng | Margin công bố trước đây của Preply không được tái sử dụng cho effort-adjusted estimator |

Do Preply endpoint trả 403, các ô “chưa xác minh” không phải bằng chứng rằng Preply không có kiểm soát; chỉ là **chưa tìm được nguồn xác thực cho ý này**.

## 6. Validation plan bổ sung

1. **Pilot response-level:** mẫu đa dạng proficiency/L1/device; ghi latency chính xác, device context, interruption và post-test SRE.
2. **Threshold calibration:** dùng solution-behavior evidence hoặc response-time mixture/criterion độc lập để chọn rapid-guess thresholds theo item/context; không dùng threshold từ nguồn khác nguyên xi.
3. **Incremental validity:** so sánh model vocabulary chỉ có correctness với model có effort/context; kiểm tra whether RTE adds prediction of criterion performance ngoài raw score.
4. **Hold-out coverage:** đánh giá bias, MAE/RMSE và coverage 80/95% riêng cho usable, effort-conflict và low-effort groups.
5. **Device invariance:** common-person/common-item hoặc alternate forms giữa mobile/desktop; tách latency effect khỏi group composition; kiểm tra accuracy lẫn response process.
6. **Decision rule:** mô phỏng chi phí của false reassurance (xuất điểm thấp do disengagement) và false exclusion (loại người chậm do thiết bị); chọn cổng quality theo intended use.
7. **Auditability:** version hóa device taxonomy, threshold, timestamp, item bank và rule set; khi rule đổi, không hồi tố các score cũ mà không ghi version.

## 7. Gaps

- Không có item bank, response-level data hoặc telemetry của Preply để xác minh effort/device controls, ngưỡng, tỷ lệ rapid guessing hay calibration.
- Bằng chứng device của Passell không phải vocabulary-size test chuyên biệt; không được chuyển effect size thành correction cho vocabulary count.
- Chưa có calibration sample để chọn RTE/rapid-rate thresholds, completion gate, uncertainty multiplier hoặc rule loại phiên.
- Chưa tìm được nguồn xác thực cho một công thức phổ quát biến effort signal thành số từ điều chỉnh. Vì vậy production phải giữ `effort_adjusted_count = null` cho đến khi có pilot và hold-out.
