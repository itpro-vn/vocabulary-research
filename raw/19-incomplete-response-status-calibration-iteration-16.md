# Iteration 16 — Incomplete responses, response status và calibration missingness

## 1. Phạm vi

Iteration này kiểm tra một vấn đề khác với latency/online-QC ở iteration 8: cùng một ô trống có thể là người làm bỏ qua, hết thời gian chưa tới item, chọn explicit “I don't know”, lỗi kỹ thuật, hoặc một response thực sự sai. Câu hỏi là có được chấm tất cả như wrong/missing hay không, và khi nào phải đưa response propensity vào mô hình.

Direction:

> Incomplete-response and response-status calibration: distinguish answered-wrong, explicit IDK, user omission, timeout/not-reached and technical missingness; verify MNAR effects and derive a production policy for scoring, minimum completion, uncertainty inflation and sensitivity reporting without treating missingness as an ordinary wrong answer.

## 2. Nguồn đã fetch và verify

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| [Xu & von Davier, *Modeling Nonignorable Missing Data with IRT*](https://files.eric.ed.gov/fulltext/ED523925.pdf) | 200 | Phân loại MCAR/MAR/MNAR; mô phỏng và phân tích PISA về cách xử lý omission |
| [Livingston, ETS, *Basic Concepts of Item Response Theory*](https://www.ets.org/Media/Research/pdf/RM-20-06.pdf) | 200 | Calibration, linking item pool, số response/item mang tính hướng dẫn và pattern scoring |
| [Meara & Buxton, *An alternative to multiple choice vocabulary tests*](https://www.lextutor.ca/rand/meara_buxton.pdf) | 200 | Guessing trong MCQ, ảnh hưởng của distractor/context và quan hệ Y/N–MC |
| [Stubbe & Stewart, *Optimizing scoring formulas for yes/no vocabulary tests with linear models*](https://teval.jalt.org/sites/default/files/SRB-16-2-Stubbe-Stewart.pdf) | 200 | False alarms/pseudowords, hiệu quả của correction và yêu cầu local calibration |
| [Preply, *How does the vocabulary test work?*](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) | 200 qua proxy; endpoint trực tiếp 403 | Mô tả reference test: hai giai đoạn, khoảng 40 + 120 từ, midpoint/log-frequency và headword universe |

HTTP 403 của Preply direct được giữ như gap; không coi đó là bằng chứng về live item bank hay live response handling.

## 3. Bằng chứng chính

### 3.1. Missingness là một cơ chế, không phải một đáp án

Xu và von Davier dùng khung Rubin để phân biệt:

- **MCAR**: xác suất missing độc lập với response quan sát được, response bị thiếu, covariates và năng lực tiềm ẩn.
- **MAR**: missingness phụ thuộc dữ liệu đã quan sát/covariates nhưng không phụ thuộc giá trị chưa quan sát hoặc năng lực sau khi đã điều kiện hóa.
- **MNAR**: missingness vẫn phụ thuộc giá trị chưa quan sát và/hoặc năng lực tiềm ẩn sau khi điều kiện hóa.

Nguồn này lưu ý rằng hai cách vận hành phổ biến đều có vấn đề: coi omission là missing giả định missingness có thể bỏ qua; coi omission luôn là wrong giả định omission chắc chắn có nghĩa là người làm không biết đáp án, bất kể năng lực. Với một bài vocabulary tự nguyện trên web, không được mặc định status blank có cùng ý nghĩa với wrong.

### 3.2. Bias tăng theo lượng missingness và mức liên hệ với năng lực

Trong mô phỏng của nguồn, khoảng 30% missing vẫn cho ước lượng IRT tương đối bền, còn khoảng 50% làm tham số item và person bị ảnh hưởng nghiêm trọng. Bias trong các chỉ số CTT đã thấy từ khoảng 30%. Đây là kết quả của thiết kế nghiên cứu large-scale, **không phải** ngưỡng production đã được calibration cho test vocabulary này.

Nguồn cũng mô tả hai hướng bias đối nghịch:

1. Bỏ qua missing và tính trên completed items có thể nâng tỷ lệ đúng vì người làm có xu hướng bỏ item khó, tức là họ tự chọn một bài gần với năng lực của mình.
2. Recode tất cả missing thành wrong có thể phạt người có khả năng làm đúng nhưng đã bỏ qua, đồng thời không xử lý đúng tính stochastic/MNAR của response process.

Do đó, completion rate phải được báo cùng score. Một score 70% trên 100 item answered không có cùng mức bằng chứng với score 70% trên 60 item answered và 40 item timeout/omitted.

### 3.3. Response propensity có thể được mô hình hóa, nhưng không nên tự chế hệ số

Nguồn PISA so sánh các mô hình có thêm latent response-propensity dimension hoặc dùng omission-rate stratum như predictor trong latent regression. Các mô hình này giảm bias khi missingness không ngẫu nhiên; mô hình-based đặc biệt hữu ích khi missing rate cao hoặc có một số người có pattern missing rất tập trung. Nguồn cũng ghi nhận IRT đơn giản bỏ qua missingness có thể hoạt động khá tốt khi missing vừa phải.

Quy tắc an toàn cho sản phẩm:

- Với missing thấp và phân bố không cho thấy concentration theo band/position: estimate chính dùng các response quan sát được; không tự động chuyển blank thành 0.
- Với missing cao, missing liên quan rõ đến difficulty/band/position, hoặc có timeout liên tục ở cuối bài: không phát hành một point estimate “chính xác”; phát hành cờ `incomplete` và khoảng sensitivity.
- Chỉ fit response-propensity model khi có pilot đủ lớn, có logging status/position/time và có kiểm tra hold-out; không copy hệ số từ PISA hay bài khác.

### 3.4. Calibration item pool cần dữ liệu nối các item

Tài liệu ETS giải thích rằng calibration không cần mọi người làm mọi item, nhưng các item trong pool phải được nối trực tiếp hoặc gián tiếp bằng các nhóm người làm chung. Tài liệu nêu mức thường được chuyên gia đồng thuận khoảng 150 response/item cho Rasch một tham số và khoảng 250 response/item cho mô hình hai tham số; mô hình hai/ba tham số thường cần nhiều dữ liệu hơn. Đây là hướng dẫn khái quát, không thay thế power analysis cho item bank mục tiêu.

Hệ quả là response status phải được lưu khi calibration:

- `answered_correct`
- `answered_wrong`
- `explicit_idk`
- `omitted`
- `timeout_not_reached`
- `technical_missing`

Chỉ hai trạng thái answered đúng/sai là quan sát trực tiếp cho binary vocabulary response. Các trạng thái khác có thể được mô hình hóa như response-process signals, nhưng không được âm thầm biến thành answered_wrong trong item calibration.

### 3.5. Guessing phụ thuộc task và trạng thái trả lời

Meara và Buxton chỉ ra rằng trong MCQ bốn lựa chọn, đoán mù có xác suất đúng 25%; nếu người làm loại được một distractor thì xác suất đoán có thể thành 33%, và nếu loại được hai distractors thì thành 50%. Context/definition cũng có thể khiến người biết từ trả lời sai hoặc người chưa biết từ loại được distractor và trả lời đúng.

Bài này báo tương quan Y/N–MC là `r=.703` trong mẫu 100 người; con số này là kết quả của mẫu/ngữ cảnh bài nghiên cứu, không phải hệ số quy đổi chung. Với thuật toán, `explicit_idk`, blank và wrong phải tách nhau; option count không đủ để xác định một guessing correction phổ quát.

### 3.6. Pseudoword correction phải được calibration theo population/form

Stubbe và Stewart tổng hợp rằng hiệu quả của các công thức chỉnh false alarms trong Y/N vẫn chưa rõ. Trong pilot của họ, regression dùng số từ tự báo biết và số pseudoword bị nhận nhầm đạt `R²=45.2%`, so với `R²=35.6%` của mô hình không có false alarms. Tuy nhiên, tác giả cảnh báo công thức tối ưu cho một mẫu và một form khó chuyển nguyên sang mẫu/form khác.

Vì vậy pseudoword hoặc false-alarm rate nên là:

- một quality/validity signal;
- hoặc một covariate chỉ được dùng sau common-person calibration với criterion test;
- không phải một số hạng trừ điểm được lấy từ nghiên cứu khác rồi nhân thẳng thành số từ.

## 4. So sánh với Preply

| Thành phần | Preply được mô tả công khai | Đề xuất sau iteration 16 |
|---|---|---|
| Sampling | Khoảng 40 từ rộng để định vị, sau đó khoảng 120 từ trong vùng frequency hẹp; midpoint/log-rank | Giữ sampling nếu muốn tái tạo nhanh, nhưng log status/position/time của từng item và completion theo band |
| Estimand | Dictionary trên 45.000+ entries, derived forms gộp về headword; không tương đương word-family scale | Giữ headword estimate riêng; không dùng missing policy để che sự khác biệt estimand |
| Blank/omission | Trang methodology fetch được không công khai rõ production status handling/timeout scoring | Phải phân loại `omitted`, `timeout_not_reached`, `technical_missing`, `explicit_idk`, `wrong`; không recode mặc định |
| Guessing | Trang methodology fetch được không cung cấp hệ số guessing độc lập đã calibration | Báo sensitivity theo status; chỉ dùng guessing/false-alarm correction sau common-person criterion calibration |
| Uncertainty | Preply công khai claim khoảng ±10%, dựa trên model vendor; chưa có response-level validation độc lập | Tách measurement SE, missingness sensitivity và construct/transport uncertainty; chỉ gọi CI sau coverage validation |
| Production evidence | Direct endpoint trả 403; live item bank/routing/response logs chưa xác minh | Cần pilot item-level và hold-out để chọn completion gate, model và cutoff |

## 5. Thuật toán đề xuất cho response status

### 5.1. Data model tối thiểu

```text
ItemResponse {
  session_id,
  form_id,
  item_id,
  lexical_unit_version,
  frequency_band,
  position,
  status: answered_correct | answered_wrong | explicit_idk |
          omitted | timeout_not_reached | technical_missing,
  response_time_ms,
  option_id,
  timestamp
}
```

`technical_missing` không được dùng làm bằng chứng về lexical knowledge. `timeout_not_reached` ở cuối bài phải được tách khỏi người dùng chủ động skip. Nếu UI không có nút IDK thì không được suy đoán rằng blank là IDK.

### 5.2. Pseudocode production-safe

```text
function score_session(responses, item_bank, calibration):
    observed = filter(status in {answered_correct, answered_wrong})
    idk      = count(status == explicit_idk)
    omitted  = count(status == omitted)
    timeout  = count(status == timeout_not_reached)
    tech     = count(status == technical_missing)
    administered = len(responses) - tech
    completed = len(observed) + idk + omitted + timeout
    missing_rate = (idk + omitted + timeout) / max(completed, 1)

    # Do not turn non-observed statuses into wrong in the main estimate.
    theta_obs, se_obs = fit_irt_or_weighted_estimator(
        responses=observed,
        item_parameters=calibration,
        missing_statuses={idk, omitted, timeout}
    )
    vocab_obs = calibrated_theta_to_scale(theta_obs)

    # Sensitivity bounds are not a replacement for a calibrated MNAR model.
    theta_all_wrong = fit_irt_with_nonobserved_as_wrong(responses, calibration)
    theta_nonresponse_model = None
    if missing_rate >= calibrated_missing_gate
       or concentrated_by_band_or_position(responses):
        if calibration.has_response_propensity_model:
            theta_nonresponse_model = fit_joint_response_propensity_model(
                responses, calibration
            )

    low = min(scale(theta_obs), scale(theta_all_wrong))
    high = max(scale(theta_obs), scale(theta_all_wrong))

    flags = []
    if missing_rate >= calibrated_missing_gate:
        flags.append('high_missingness')
    if concentrated_by_band_or_position(responses):
        flags.append('nonrandom_missingness_possible')
    if tech > calibrated_technical_gate:
        flags.append('technical_incomplete')
    if timeout > calibrated_timeout_gate:
        flags.append('speeded_or_not_reached')

    if administered < calibrated_min_administered:
        return {status: 'not_interpretable', flags: flags,
                sensitivity_range: [low, high]}

    return {
        status: 'interpretable_with_flags' if flags else 'interpretable',
        estimate: vocab_obs,
        se: transform_se_to_vocab_scale(theta_obs, se_obs),
        sensitivity_range: [low, high],
        missing_rate: missing_rate,
        counts: {observed: len(observed), idk: idk, omitted: omitted,
                 timeout: timeout, technical_missing: tech},
        flags: flags
    }
```

`calibrated_missing_gate`, `calibrated_min_administered`, và các gate khác không được gán số tùy ý từ nguồn ngoài. Chúng phải được chọn bằng mô phỏng/hold-out trên data của chính item bank và population mục tiêu.

### 5.3. Công thức summary và uncertainty

Nếu dùng estimator theo band ở lớp design-based, báo tối thiểu:

```text
completion_rate = observed_or_explicit_status / administered_nontechnical
missing_rate = (explicit_idk + omitted + timeout_not_reached) / completed
```

Với IRT, báo `theta_hat` và `SE(theta_hat)` từ response quan sát được. Khi chuyển sang số từ bằng hàm calibration `g(theta)`, xấp xỉ delta method là:

```text
SE_vocab ≈ |g'(theta_hat)| * SE(theta_hat)
```

Không gọi `[vocab_obs ± 1.96*SE_vocab]` là confidence interval đã được xác thực nếu chưa có coverage study. Trong giai đoạn chưa có MNAR model, thêm khoảng sensitivity:

```text
S = [g(theta_obs), g(theta_all_wrong)]
```

Khoảng `S` là kịch bản xử lý missing, không phải CI sampling. Có thể thêm kịch bản model-based sau khi response-propensity model được calibration và kiểm tra hold-out.

## 6. Validation plan

1. **Instrument trước**: log sáu status, item position, frequency band, form, response time và nguyên nhân technical failure.
2. **Pilot common-person**: cùng người làm vocabulary MCQ/Y/N, explicit-meaning criterion test và một form có timeout simulation; lưu status không gộp.
3. **Missingness audit**: ước lượng rate theo band, position, device, proficiency proxy; kiểm tra concentration và association với ability.
4. **Scoring comparison**: so sánh observed-only, all-wrong, complete-case và response-propensity model; đánh giá bias, RMSE, coverage và subgroup fairness bằng hold-out.
5. **Guessing/IDK calibration**: so sánh MCQ với criterion meaning test; không lấy 25%/33%/50% làm correction tự động.
6. **Item-bank linking**: giữ overlap giữa các form; đạt cỡ mẫu calibration phù hợp mô hình, sau đó kiểm tra item drift và response-status DIF.
7. **Production gate**: chọn completion/missing thresholds từ kết quả validation; nếu chưa đủ evidence thì trả `not_interpretable` hoặc `interpretable_with_flags`, không trả point estimate với false precision.
8. **Preply comparison**: chỉ so sánh headword estimate với Preply sau khi cùng người làm hai bài, cùng khai báo status và có common-person/common-item bridge. Direct production behavior của Preply hiện vẫn là gap.

## 7. Kết luận iteration

- Blank, explicit IDK, timeout và technical failure là các response status khác nhau; không được mặc định coi tất cả là wrong.
- Khi missingness MNAR, recode thành wrong có thể tạo bias và vấn đề fairness; bỏ qua missing cũng có thể nâng score nếu người làm chủ động tránh item khó.
- Main score nên dùng response quan sát được, kèm completion/missingness và sensitivity range. Response-propensity model chỉ được bật sau calibration trên data mục tiêu.
- Guessing/false-alarm correction không có hệ số phổ quát; mọi hệ số phải được fit và kiểm tra bằng common-person criterion data.

## 8. Gaps còn lại

Chưa có response-level production data, item-bank calibration, status/timeout logs hoặc missingness pattern của Preply. Vì vậy chưa thể xác thực `calibrated_missing_gate`, `calibrated_min_administered`, model MNAR, false-alarm threshold, CI coverage, hay tác động định lượng của incomplete attempts lên midpoint estimator Preply. Chưa tìm được nguồn xác thực cho các ngưỡng production riêng của Preply.
