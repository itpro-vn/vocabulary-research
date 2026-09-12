# Iteration 7 — Temporal reliability, alternate forms và diễn giải thay đổi theo thời gian

## 1. Câu hỏi của iteration

Các iteration trước đã xử lý sampling, IRT/CAT, validity, uncertainty, estimand headword/lemma/word-family và measurement invariance. Iteration này tập trung vào một use case dễ bị overclaim: người dùng làm bài lần hai và sản phẩm nói rằng vốn từ đã “tăng” hoặc “giảm”. Câu hỏi là làm thế nào tách thay đổi thật khỏi khác biệt độ khó giữa form, sai số đo, item exposure và practice effect.

Các URL dưới đây đã được fetch và kiểm tra HTTP 200 trong iteration 7:

- [ERIC EJ1327645 — Akase (2022)](https://eric.ed.gov/?id=EJ1327645), bản ghi chính thức có abstract và thiết kế longitudinal.
- [IDEAS/RePEc — Masrai (2022)](https://ideas.repec.org/a/sae/sagope/v12y2022i1p21582440221074355.html), bản ghi truy cập được có abstract của nghiên cứu lemma-based yes/no vocabulary-size test.
- [Preply methodology qua proxy](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works), nguồn tham chiếu sản phẩm đã dùng ở các iteration trước; endpoint Preply trực tiếp bị HTTP 403 trong môi trường này.

`web_search` chỉ dùng để tìm lead. Chỉ hai bản ghi đã fetch thực tế ở trên được dùng cho claim học thuật; các hệ số không xuất hiện trong trang fetch không được suy đoán.

## 2. Bằng chứng đã xác minh

### 2.1. Alternate forms “được thiết kế tương đương” vẫn cần equating

Akase (2022) nghiên cứu ba form VST do Aizawa và Mochizuki tạo ra. VST 1, 2 và 3 được làm cho 189 học sinh trung học Nhật Bản, tuổi 16–18, trong tháng 4 của năm học thứ nhất, thứ hai và thứ ba. Dù ba form được thiết kế có độ khó tương đương, nghiên cứu ghi nhận việc formal equating trước đó chưa được thực hiện. Để kiểm tra xem score gains là tăng vocabulary size hay chỉ phản ánh chênh lệch độ khó form, tác giả tạo form thứ tư bằng các item lấy từ ba form đầu và làm form này vào tháng 12 của năm thứ ba.

**Hệ quả:** một sản phẩm không được coi hai form là ngang nhau chỉ vì cùng số câu, cùng frequency blueprint hoặc cùng mục tiêu biên soạn. Cần common items/anchors hoặc một item bank đã calibration để nối scale.

Nguồn: [ERIC EJ1327645](https://eric.ed.gov/?id=EJ1327645).

### 2.2. Rasch linking cho phép diễn giải gain trên một logit scale chung

Abstract của Akase báo cáo bốn form được equate bằng Rasch analysis, đặt person và item lên một uniform logit scale. Ba form ban đầu có good fit với Rasch; chênh lệch độ khó giữa các form ban đầu là nhỏ; bốn form đã link có thể dùng để ước lượng gain về vocabulary size trong toàn bộ giai đoạn trung học.

Điểm thiết kế quan trọng không phải là “Rasch luôn đúng”, mà là quy trình: calibrate item/person chung, kiểm tra fit, rồi mới so sánh score theo thời gian. Nếu chỉ lấy `raw_score_form_B - raw_score_form_A`, chênh lệch có thể trộn lẫn learning, form difficulty và stochastic measurement error.

Nguồn: [ERIC EJ1327645](https://eric.ed.gov/?id=EJ1327645).

### 2.3. Frequency band không đủ để làm bảo chứng cho độ khó giữa các form

Follow-up analysis trong cùng abstract cho thấy có considerable overlap về item difficulty giữa các word-frequency bands. Kết luận được nêu là word frequency không phải chỉ báo duy nhất của item difficulty, và tiến bộ của người học có xu hướng uniform/parallel qua các bands.

**Hệ quả cho alternate-form generator:** giữ cùng số item mỗi band là điều kiện coverage, không phải bằng chứng equated difficulty. Form generator phải dùng item parameters (difficulty, fit, DIF, exposure), anchor overlap và hold-out form comparison. Nếu chưa có item calibration, chỉ nên gọi form là “parallel candidate”, không gọi là equivalent form đã chứng minh.

Nguồn: [ERIC EJ1327645](https://eric.ed.gov/?id=EJ1327645).

### 2.4. Reliability của parallel forms là một validation gate riêng

Masrai (2022) báo cáo một lemma-based yes/no vocabulary-size test được làm cho 219 người tham gia. Abstract ghi nhận high reliability indices cho parallel forms và internal consistency; test có một underlying dimension, phân biệt được các mức proficiency và tương quan có ý nghĩa với general English proficiency. Vì abstract không hiển thị trị số hệ số, báo cáo này không gán một con số reliability cụ thể.

**Hệ quả:** trước khi dùng chênh lệch qua thời gian, cần đo parallel-form reliability trên population mục tiêu. Internal consistency không thay thế parallel-form agreement: alpha cao có thể chỉ cho thấy item đồng biến trong một form, không chứng minh form A và form B có cùng scale.

Nguồn: [IDEAS/RePEc — Masrai (2022)](https://ideas.repec.org/a/sae/sagope/v12y2022i1p21582440221074355.html).

## 3. Quy tắc scoring và báo cáo retest đề xuất

### 3.1. Hai loại output phải tách biệt

- `status_change`: thay đổi quan sát được giữa hai lần làm bài trên cùng latent scale.
- `learning_claim`: chỉ được phát hành nếu thay đổi vượt reliable-change threshold đã calibration và không bị quality/practice flags.

Đối với Preply-compatible output, vẫn giữ headword/rank estimate như một output riêng. Không được lấy chênh lệch headword midpoint của hai form chưa equate rồi gọi là số từ đã học.

### 3.2. Công thức reliable change ở mức sản phẩm

Với hai lần đo trên cùng scale:

```text
Delta = theta_2 - theta_1
SE_Delta = sqrt(SE_1^2 + SE_2^2 - 2*r*SE_1*SE_2)
RCI = Delta / SE_Delta
```

Trong đó `theta_i` là score trên common latent scale, `SE_i` là conditional standard error tại lần đo `i`, và `r` là reliability/độ tương quan ổn định của score trên population mục tiêu hoặc phương án bảo thủ đã pre-register. Một rule hai phía thường dùng trong thiết kế có thể là `|RCI| >= 1.96`, nhưng ngưỡng này **chưa được calibration cho Preply** và không được trình bày như tham số đã xác thực.

Nếu không có ước lượng ổn định của `r`, có thể dùng khoảng bất định độc lập bảo thủ:

```text
CI_Delta = Delta ± 1.96 * sqrt(SE_1^2 + SE_2^2)
```

nhưng phải gắn cờ rằng công thức này bỏ qua covariance giữa hai lần đo và có thể rộng hoặc hẹp không đúng tùy thiết kế. Với CAT, `SE_i` đến từ information curve; với stratified estimator, `SE_i` đến từ variance/cluster bootstrap. Khi transform từ `theta` sang vocabulary size `V = g(theta)`, nên lấy posterior/bootstrap draws qua cả calibration và transform thay vì chỉ dùng delta-method.

### 3.3. Pseudocode cho repeat administration

```text
function compare_retests(session_1, session_2, bank, common_scale):
    assert session_1.universe_version == session_2.universe_version
    assert session_1.construct == session_2.construct

    # Use calibrated alternate form; never assume raw-form equality.
    score_1 = estimate_on_scale(session_1, bank, common_scale)
    score_2 = estimate_on_scale(session_2, bank, common_scale)

    anchor_ok = check_common_anchor_consistency(session_1, session_2)
    exposure = detect_repeated_or_leaked_items(session_1, session_2)
    quality = merge_quality_flags(session_1, session_2)

    delta = score_2.theta - score_1.theta
    se_delta = reliable_change_se(score_1.se, score_2.se,
                                  common_scale.retest_reliability)
    rci = delta / se_delta if se_delta > 0 else null

    if not anchor_ok or quality.severe or exposure.practice_risk:
        status = "not_interpretable_without_review"
    elif abs(rci) >= common_scale.preregistered_change_threshold:
        status = "change_exceeds_measurement_error"
    else:
        status = "change_not_separable_from_measurement_error"

    vocab_1 = transform_with_uncertainty(score_1.theta, score_1.se,
                                         common_scale.vocab_transform)
    vocab_2 = transform_with_uncertainty(score_2.theta, score_2.se,
                                         common_scale.vocab_transform)

    return {
        "theta_1": score_1.theta, "theta_2": score_2.theta,
        "delta_theta": delta, "se_delta": se_delta, "rci": rci,
        "vocab_1": vocab_1, "vocab_2": vocab_2,
        "status": status,
        "anchor_ok": anchor_ok, "quality_flags": quality,
        "practice_exposure": exposure
    }
```

### 3.4. Administration policy

1. Dùng alternate form với anchor items giới hạn và exposure control; không lặp toàn bộ item nếu mục tiêu là đo growth.
2. Giữ khoảng cách làm bài hợp lý cho use case. Nếu người dùng làm lại ngay, ghi `short_interval_practice_risk`; chưa có dữ liệu sản phẩm để chọn một khoảng ngày tối ưu.
3. Lưu form version, item exposure, answer latency, skip, quality flags và anchor responses.
4. Chỉ phát hành “tăng/giảm” khi common-scale link đạt QA và change vượt threshold. Nếu không, hiển thị “điểm lần này khác trong phạm vi sai số đo”.
5. Report cả point estimate và interval ở từng lần đo; report `Delta`, `SE_Delta`, reliability version và các flag, không chỉ phần trăm thay đổi.

## 4. So sánh với Preply

| Thành phần | Preply theo methodology đã fetch | Thiết kế đề xuất có retest |
|---|---|---|
| Universe | Hơn 45.000 dictionary entries/headwords, sắp theo frequency rank | Giữ rõ unit/version; có thể có output headword tương thích, nhưng common scale phải bất biến |
| Routing | Khoảng 40 từ screening + khoảng 120 từ ở vùng hẹp, logarithmic rank sampling | Baseline stratified hoặc CAT đã calibration; retest dùng alternate form + anchors |
| Point estimate | Midpoint trên rank interval; estimates được làm tròn theo vùng | Theta/common-scale score rồi transform; báo unit và transform version |
| Repeat comparison | Chưa tìm thấy production evidence về test–retest, practice effect hoặc alternate-form equating của Preply | Rasch/IRT linking hoặc common-item equating; change score kèm SE/RCI |
| Uncertainty | Preply công bố margin khoảng ±10.33% dựa trên assumption riêng của họ | CI/PI và reliable-change threshold phải được pilot calibration; không tái sử dụng ±10.33% cho thay đổi theo thời gian |
| Claim | Vocabulary estimate theo headword/rank frame | Chỉ claim growth khi change vượt sai số, anchors/quality đạt và practice risk không nghiêm trọng |

Preply methodology là nguồn tham chiếu thuật toán midpoint, không phải bằng chứng rằng các lần làm lại độc lập hoặc các form khác nhau đã được equate. Trang này còn nói họ sẽ refine error calculation khi participation tăng; do đó không nên biến margin công bố của Preply thành guaranteed longitudinal change threshold.

## 5. Validation plan cho repeatability

### A. Study design

- Tuyển mẫu đa dạng proficiency, L1 và tuổi trong population mục tiêu.
- Làm hai alternate forms theo counterbalanced order; giữ anchor items đủ để link nhưng kiểm soát exposure.
- Có một subsample làm lại form sau khoảng thời gian đã pre-register và một subsample làm lại form có item overlap khác mức để ước lượng practice effect.
- Giữ một hold-out form không dùng trong calibration.

### B. Psychometric gates

- Fit Rasch/2PL trên calibration sample; kiểm tra item fit, unidimensionality, local dependence và DIF.
- Ước lượng form difficulty drift, anchor stability, conditional SE và test information theo ability.
- Tính parallel-form reliability, rank-order stability và agreement trên common scale; không chỉ dùng internal consistency.
- Kiểm tra item exposure, response time và repeated-item performance để tách familiarity khỏi vocabulary growth.

### C. Accuracy and decision gates

- Báo bias, MAE/RMSE và 80/95% interval coverage trên hold-out.
- Với synthetic known/unknown profiles và repeated sampled forms, kiểm tra false growth/false decline rate.
- Chọn change threshold theo mục tiêu quyết định và chi phí false positive/false negative; pre-register trước khi nhìn kết quả hold-out.
- Kiểm tra sensitivity khi bỏ anchor, bỏ item flagged, đổi form và đổi headword↔lemma/word-family output.

## 6. Gaps

- Chưa có nguồn xác thực cho test–retest reliability, practice effect, item exposure hoặc alternate-form equating của Preply production.
- Chưa có response-level/item-bank data để ước lượng `SE_1`, `SE_2`, `r`, anchor stability và conditional reliable-change threshold.
- Chưa có dữ liệu để chọn khoảng cách retest tối ưu hoặc phân biệt learning thật với memory/familiarity của item.
- Chưa có hệ số chuyển đã calibration từ common latent scale sang headword estimate của Preply hoặc sang lemma/word-family.
- Bản abstract Masrai được fetch qua RePEc có nêu “high reliability indices” nhưng không hiển thị coefficient; chưa được dùng số cụ thể. Nếu cần numeric coefficient, cần full text truy cập được hoặc dữ liệu gốc; hiện **chưa tìm được nguồn xác thực cho trị số coefficient đó trong nguồn đã fetch**.

## 7. Kết luận iteration

Tài liệu Akase cung cấp bằng chứng trực tiếp rằng longitudinal vocabulary-size measurement nên dùng alternate-form Rasch equating thay vì tin vào thiết kế “equal difficulty” trên giấy. Thiết kế đề xuất vì vậy thêm một lớp retest: common-scale score, conditional SE, `SE_Delta`/RCI, anchor and practice flags, và ngôn ngữ báo cáo phân biệt “khác điểm” với “đã tăng vốn từ”. Đây là yêu cầu calibration/validation cho sản phẩm mới, không phải claim rằng Preply hiện đã hỗ trợ các tính năng này.
