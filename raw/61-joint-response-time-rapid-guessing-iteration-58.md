# Iteration 58 — Joint response-accuracy/response-time modeling và rapid-guessing robustness

## Phạm vi

Iteration này tách hai câu hỏi thường bị trộn trong online vocabulary testing:

1. Response time (RT) có thể cung cấp latent speed/process information bổ sung cho response accuracy (RA) hay không?
2. Có nên biến RT hoặc rapid-guessing flag thành một correction trực tiếp cho số lượng từ hay không?

Kết luận bảo thủ: joint RA/RT là một lớp calibration và validity diagnostics hữu ích; chưa có bằng chứng để cộng/trừ từ theo RT, RTE hoặc một cutoff rapid-guess phổ quát. Điểm breadth chính vẫn phải được xác định từ RA trên item bank đã calibration, còn speed/effort là output và sensitivity layer riêng cho tới khi có pilot vocabulary-specific.

## Nguồn đã fetch và kiểm tra

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| Fox, Klotzke & Simsek (2023), *R-package LNIRT for joint modeling of response accuracy and times*, PeerJ | 200 | Joint latent speed/accuracy model, log-normal RT + 2PL, MCMC, fit tools, missing-by-design và use cases |
| CRAN LNIRT package page | 200 | Khả năng phần mềm và metadata reproducibility của baseline joint model |
| Wise et al., *Setting the Response Time Threshold Parameter to Differentiate Solution Behavior from Rapid-Guessing Behavior* (ERIC PDF) | 200 | Rapid guessing trong low-stakes test, item-specific thresholds, RTE và treatment như missing |
| Rios, *Assessing the Accuracy of Parameter Estimates in the Presence of Rapid Guessing Misclassifications* (Crossref API record) | 200 | Abstract về simulation EM-IRT/3PL và bias do misclassification |
| Preply vocabulary test endpoint | 403 | Không citable cho cơ chế hiện tại; chỉ ghi gap |

## Bằng chứng đã xác minh

### 1. RA và RT đo hai latent facet khác nhau

Fox et al. mô tả joint model trong đó RA đo latent accuracy/ability, RT đo latent speed. Hai loại quan sát được giả định conditionally independent khi đã biết latent variables; quan hệ speed–ability được mô hình ở cấp người làm bài. Item có đặc tính accuracy (ví dụ difficulty) và speed (time intensity), và mô hình có thể biểu diễn speed–accuracy trade-off.

Hệ quả cho vocabulary-size test: RT có thể phản ánh tốc độ xử lý, effort hoặc response process, nhưng không đồng nhất với receptive lexical knowledge. Một người biết từ nhưng trả lời chậm và một người đoán nhanh không nên bị quy đổi như cùng một thay đổi trong số từ.

### 2. Dạng mô hình và giới hạn chuyển giao

LNIRT dùng log-normal model cho RT sau log-transform, vì RT dương, và two-parameter IRT cho RA. Đây là framework phù hợp để nghiên cứu đồng thời `theta_knowledge` và `eta_speed`, nhưng item parameters, prior và association giữa hai latent variables cần được ước lượng/kiểm tra trên dữ liệu vocabulary. Không được chuyển thẳng các tham số từ achievement test sang VST.

CRAN xác nhận LNIRT hỗ trợ simultaneous responses/response times, variable person-speed functions, item/person covariates, missing-by-design và MCMC. Khả năng phần mềm chỉ cho thấy mô hình có thể tái lập; nó không chứng minh joint score có criterion validity tốt hơn raw vocabulary count.

### 3. Rapid guessing tồn tại trong low-stakes testing và phụ thuộc item

Báo cáo ERIC cho biết rapid guessing có thể xuất hiện xuyên suốt một low-stakes test, không chỉ khi gần hết giờ. Với item `i`, chỉ số solution behavior được định nghĩa bằng `SB_ij = 1` khi `RT_ij >= T_i`; response-time effort của người `j` là tỷ lệ item có solution behavior.

Báo cáo so sánh bốn cách xác định `T_i`: ngưỡng cố định, ngưỡng từ surface features, quan sát phân phối RT và two-state mixture model; khác biệt giữa các cách nhỏ trong nghiên cứu đó. Tuy nhiên, báo cáo cũng nêu item length và item position ảnh hưởng effort, nên VST không nên mặc định một cutoff chung cho mọi stem/context.

Báo cáo ghi nhận psychometric properties có thể cải thiện khi rapid guesses được xử lý như missing trong nghiên cứu cụ thể. Đây là bằng chứng cho sensitivity analysis và quality flag, không phải giấy phép để loại response hoặc điều chỉnh K_hat trước khi có calibration.

### 4. Sai phân loại rapid guess có thể làm lệch ability

Crossref record của Rios (2022) mô tả simulation thay đổi loại và tỷ lệ rapid-guess misclassification ở 10%, 30% và 50%, so sánh effort-moderated IRT với 3PL. Abstract báo cáo EM-IRT cải thiện item-parameter estimation hơn 3PL trong các điều kiện nghiên cứu; underclassification thường gây bias ability lớn nhất. Trong một số điều kiện, nhận diện rapid guess không hoàn hảo vẫn tốt hơn bỏ qua RG, và threshold liberal có thể giảm bias do underclassification.

Không có hệ số nào trong abstract có thể chuyển thành “trừ X từ” cho VST. Kết quả chỉ yêu cầu production phải đo sensitivity với false-positive/false-negative rapid-guess flags và chọn model sau hold-out validation.

## Thiết kế thuật toán đề xuất

### Dữ liệu phải lưu

```text
person_id, form_id, item_id
response, response_status
rt_ms, client/server timestamp quality
item_time_intensity, stem_length, item_position
rapid_guess_flag, threshold_version
theta_model_version, calibration_version
```

`rapid_guess_flag` không được ghi đè `response`; response gốc và trạng thái phải luôn giữ để chạy sensitivity. Các threshold phải versioned theo item/form và calibration sample.

### Lớp scoring chính

1. Fit/lookup IRT cho RA trên item bank đã calibration; ước lượng `theta_knowledge`.
2. Fit RT layer (tối thiểu log-normal item time-intensity; joint LNIRT chỉ trong calibration/validated deployment).
3. Dùng speed/RT để tạo diagnostic: `RTE`, item-level flags, speed–accuracy residuals và possible low-effort status.
4. Tính vocabulary count từ posterior probability known hoặc stratified estimator; không đưa RTE vào công thức count nếu chưa có evidence vocabulary-specific.
5. Báo thêm sensitivity: standard responses, loại/censor rapid-guess flags, và nếu đủ dữ liệu thì joint-model posterior. Nếu các kết quả khác nhau vượt ngưỡng đã pre-register, gắn `score_sensitivity_high` thay vì chọn correction tùy ý.

### Pseudocode

```text
input: calibrated vocabulary item bank B, RA responses y,
       RTs t, item-specific threshold manifest T,
       declared strata M_h, fixed form/adaptive log

for each item i:
    preserve(y_i, t_i, response_status_i)
    rg_i = (t_i < T_i) if threshold_version is valid else UNKNOWN

fit RA model with fixed calibrated item parameters -> theta_knowledge
fit RT model (log-normal or joint LNIRT) in calibration/QA layer
compute speed/effort diagnostics: RTE, theta_speed, item/person fit,
    fraction_rg, response-status and speed-accuracy residuals

K_main = count_from_RA_posterior(theta_knowledge, strata M_h)
K_sens = count_from_RA_posterior(theta_knowledge,
                                  excluding_or_censoring rg-flagged items)

if valid joint model and vocabulary hold-out calibration passed:
    K_joint = posterior count under pre-registered joint RA/RT model
else:
    K_joint = null

report K_main and uncertainty;
report fraction_rg, threshold_version and K_sens - K_main;
if threshold/model/coverage gate fails:
    status = diagnostic_only_or_insufficient_validity
never apply K_main + f(RTE) without a validated vocabulary-specific function
```

### Công thức count và sensitivity

Nếu `p_j^(s)` là posterior probability biết lexical unit của item `j` trong draw `s`, và sample đại diện stratum `h` có kích thước universe `M_h`:

```text
K_main^(s) = Σ_h M_h * mean_{j in sampled_h}(p_j^(s))
```

Với rapid-guess sensitivity, dùng cùng item-bank scale nhưng thay tập response hợp lệ `A_h`:

```text
K_sens^(s) = Σ_h M_h * mean_{j in A_h}(p_j^(s))
Δ_RG = median(K_sens) - median(K_main)
```

`Δ_RG` là sensitivity range, không phải correction mặc định. Nếu item inclusion probabilities không đều do adaptive routing, phải dùng inclusion-probability/model-assisted estimator đã validation; không dùng raw `correct/N * M`.

## So sánh với Preply

| Khía cạnh | Đề xuất | Preply xác minh được trong iteration này |
|---|---|---|
| RT collection | Lưu RT và status; dùng RT như process/quality facet | Endpoint sản phẩm trả 403; chưa xác minh Preply có thu hoặc dùng RT |
| Rapid-guess rule | Item-specific threshold sau pilot; threshold versioned; giữ unknown nếu chưa calibration | Chưa tìm được nguồn xác thực cho threshold hoặc rapid-guess policy |
| Main count | RA/IRT hoặc stratified posterior count; không correction theo speed | Không xác minh được current scoring implementation trong callback này |
| Diagnostics | RTE, fraction RG, speed–accuracy residual, model/item fit và sensitivity | Chưa xác minh Preply có công khai các diagnostics |
| Uncertainty | Tách RA/model, item-sampling và RG-threshold sensitivity | Không gán margin/interval cụ thể cho current Preply nếu không có fetch + coverage data |
| Claim boundary | RT không được biến thành lexical count nếu chưa hold-out validation | Không được ghi Preply dùng joint IRT/RT hay effort correction |

## Assumptions và validation plan

- Item bank và RA item parameters phải được calibration độc lập; short form không tự ước lượng đồng thời toàn bộ theta và item difficulty.
- RT phải có timestamp quality, device/network metadata tối thiểu và policy cho tab-switch/technical latency; nếu không, RT chỉ là weak diagnostic.
- Threshold selection phải được đánh giá bằng item surface features, RT mixture/distribution và held-out labels hoặc criterion proxy; không chọn cutoff để tối ưu K_hat trên cùng sample.
- Pilot vocabulary-specific: so sánh RA-only IRT, 3PL/guessing-aware, effort-moderated và joint LNIRT.
- Đo bias/RMSE của `K_hat`, item-parameter recovery, conditional SEM, interval coverage, RG classification sensitivity, DIF theo L1/proficiency, latency/device effects và retest stability.
- Chia calibration/threshold/hold-out theo người và form; báo `K_main`, `K_sens` và nếu hợp lệ `K_joint` trên hold-out.
- Chỉ release joint/effort-moderated scoring nếu posterior predictive checks, model fit, common-person/common-item linking và coverage pass; nếu không, giữ RT ở lớp diagnostics.

## Gaps

- Preply endpoint HTTP 403 trong callback; chưa tìm được nguồn xác thực cho RT logging, threshold, rapid-guess handling, joint model, item-time intensity hoặc speed-based correction của Preply.
- Chưa có response-level vocabulary pilot để chọn threshold, đánh giá sensitivity hay chứng minh joint RT/RA cải thiện count validity.
- Các nguồn LNIRT và rapid-guessing là methodology chung/achievement testing; không được diễn giải như calibration riêng cho English vocabulary-size tests.
- Chưa có nhãn độc lập cho rapid guess trong VST; mọi flag hiện tại phải coi là uncertain và báo sensitivity, không coi là ground truth.
