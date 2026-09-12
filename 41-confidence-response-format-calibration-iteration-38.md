# Iteration 38 — Confidence và response-format calibration

## Phạm vi và direction

Iteration này tách một vấn đề chưa được operationalize trong các iteration trước: confidence rating sau từng item và lựa chọn response format (Yes/No, forced-choice, Not Sure) có thể giúp phát hiện guessing/partial knowledge hay không. Mục tiêu không phải biến confidence thành “số từ biết” thứ hai, mà kiểm tra nó như một tín hiệu calibration/validity và xác định khi nào response format đòi hỏi hiệu chỉnh riêng.

Kết luận vận hành: với bài Yes/No có pseudowords, phải lưu hit rate và false-alarm rate, dùng hiệu chỉnh được calibration bằng data; confidence chỉ là covariate/diagnostic cho calibration và uncertainty, không được cộng trực tiếp vào breadth estimate.

## Nguồn đã fetch và kiểm tra

| Nguồn | HTTP | Phần đã dùng |
|---|---:|---|
| Zhang, Liu & Ai (2020), *Pseudowords and Guessing in the Yes/No Format Vocabulary Test*, ERIC record EJ1237987 | 200 | Abstract do tác giả cung cấp: mẫu 105 người, false alarms, pseudoword neighborhood, tương quan với translation và MC VST. [ERIC](https://eric.ed.gov/?id=EJ1237987) |
| Lemhöfer & Broersma (2012), *Introducing LexTALE*, PDF | 200 | Toàn văn PDF: ΔM, I_SDT, hit/false-alarm scoring, response-style correction, self-rating comparison. [PDF](https://lextale.com/pdf/Lemhofer_Broersma_2012.pdf) |
| Weber & Brewer (2004), *Confidence-Accuracy Calibration in Absolute and Relative Face Recognition Judgments*, ERIC record EJ688663 | 200 | Abstract do tác giả cung cấp: calibration phụ thuộc difficulty và polarity; đây là bằng chứng phương pháp ngoài vocabulary, không phải hệ số chuyển đổi cho vocabulary. [ERIC](https://eric.ed.gov/?id=EJ688663) |
| Preply, *How it works* | 403 direct | Không dùng làm nguồn verified trong iteration này; endpoint trực tiếp bị chặn. Chưa có item-level format/confidence data của Preply. |

Search snippets chỉ được dùng để tìm lead; claim trong artifact này chỉ dựa trên các URL HTTP 200 ở bảng trên. URL direct Preply HTTP 403 không được coi là bằng chứng.

## Bằng chứng chính

### 1. Pseudowords cung cấp tín hiệu đo guessing trong Yes/No test

Zhang, Liu và Ai nghiên cứu 105 sinh viên đại học làm ba nhiệm vụ: Yes/No vocabulary test, translation task và multiple-choice Vocabulary Size Test. Real words và pseudowords được ghép các thuộc tính lexical. Abstract báo cáo:

- False alarms trên pseudowords tương quan cao với guessing trên real words, `r > .80`.
- Kết quả hỗ trợ validity của các correction formula dùng false-alarm information để điều chỉnh điểm Yes/No.
- Pseudoword neighborhood size liên quan đến false-alarm rate, nên thiết kế pseudowords không thể chỉ dựa vào “trông giống tiếng Anh”; neighborhood phải là metadata và được kiểm soát.
- Corrected Yes/No scores tương quan cao với translation task, `r > .70`; tương quan với MC VST thấp hơn, gợi ý response format tạo ra khác biệt trong guessing.

Hệ quả cho estimator: raw hit rate không phải một ước lượng đủ. Bài test cần ghi `real_hit`, `pseudo_false_alarm`, `pseudoword_features` và score sau correction. Correction phải fit/validate trên mẫu calibration của item bank; không chuyển một penalty cố định giữa các band, L1, pseudoword neighborhoods hoặc format.

### 2. Signal detection tách sensitivity khỏi response bias

LexTALE mô tả hai cách chấm điểm cho lexical Yes/No:

- Meara `ΔM` phạt false alarms trong tỷ lệ known-word.
- `I_SDT` dựa trên signal detection theory và hiệu chỉnh cả guessing lẫn personal response style, ví dụ thiên về trả lời “yes” hoặc “no”. Công thức dùng hit rate `h` và false-alarm rate `f`.

Bài cũng cung cấp các thống kê riêng cho hit rate, false-alarm rate, `% correct`, `ΔM` và `I_SDT`, cho thấy audit trail nên giữ các đại lượng thành phần chứ không chỉ xuất một count. Hai người có cùng số real words trả lời “yes” nhưng một người cũng chấp nhận nhiều pseudowords không nên được diễn giải là có cùng latent lexical sensitivity.

Một baseline production có thể biểu diễn như sau, với `h_b` và `f_b` theo band hoặc theo pool được calibration:

```text
h_b = real_words_yes_b / real_words_present_b
f_b = pseudowords_yes_b / pseudowords_present_b
s_b = calibrated_signal_detection(h_b, f_b)
```

`calibrated_signal_detection` có thể là `I_SDT`/một model latent đã được kiểm định; không tự gọi `s_b` là “tỷ lệ word families biết” nếu chưa có mapping từ lexical unit của bank sang vocabulary universe.

### 3. Confidence/self-rating không được thay thế item-level evidence

Lemhöfer và Broersma báo cáo LexTALE là predictor tốt của English vocabulary knowledge và general English proficiency; trên nhóm Dutch và Korean, LexTALE nhìn chung dự đoán tốt hơn self-ratings. LexTALE cũng tương quan với các word-recognition paradigms trước đó trong khi self-ratings không cho cùng bằng chứng.

Đây không phải bằng chứng rằng mọi confidence rating đều vô dụng. Nó là cảnh báo estimand: self-report/global confidence có thể có giá trị bổ sung nhưng không nên thay thế response-level evidence. Với confidence sau từng item, sản phẩm nên dùng nó để kiểm tra calibration, effort và uncertainty; không cộng confidence vào `K_hat` và không dùng mean confidence làm proxy cho số lexical units.

### 4. Confidence–accuracy calibration phải kiểm tra theo difficulty và polarity

Weber và Brewer nghiên cứu confidence–accuracy (CA) calibration trong recognition judgments. Abstract báo cáo rằng khi kiểm soát difficulty, các loại phán đoán có khác biệt nhỏ về calibration; difficulty ảnh hưởng calibration; positive/old judgments có calibration mạnh, còn negative/new judgments có ít hoặc không có liên hệ confidence–accuracy trong nghiên cứu đó.

Đây là bằng chứng phương pháp ngoài vocabulary và không cho phép chuyển hệ số trực tiếp. Tuy nhiên, nó hỗ trợ một thiết kế an toàn: confidence phải được đánh giá riêng theo response polarity, frequency band, item difficulty và L1/format facet. Nếu confidence chỉ có calibration ở một số vùng, không được dùng một global confidence multiplier.

## Thuật toán cập nhật

### Estimand và dữ liệu cần lưu

Giữ `K_hat` là breadth estimate trên vocabulary universe/lexical-unit definition đã công bố. Confidence không làm thay đổi định nghĩa đó. Mỗi item response nên có:

```text
item_id
lexical_unit
frequency_band
response_format              # yes_no, forced_choice, not_sure_enabled
response
confidence                    # ordinal or 0..1, optional
response_time_ms
real_or_pseudoword            # for Y/N bank
pseudoword_neighborhood
form_id
person_l1_and_exposure
```

Các output nên tách:

```text
raw_breadth_estimate
bias_adjusted_breadth_estimate
confidence_calibration_status
confidence_sensitivity_range
response_format_status
sampling_or_model_interval
validity_flags
```

`confidence_sensitivity_range` để null nếu chưa có calibration sample đủ cho band/format/L1. Không biến confidence thành `extra_words`.

### Baseline scoring cho Yes/No

Với band `b`, real-word responses `R_b`, pseudoword responses `P_b`:

```text
h_b = sum(yes on real words) / |R_b|
f_b = sum(yes on pseudowords) / |P_b|
s_b = calibrated_SDT(h_b, f_b, bank_version, format, L1)
```

Nếu band có vocabulary-universe size `N_b`, breadth estimator cơ bản là:

```text
K_hat = sum_b N_b * clamp(s_b, 0, 1)
```

Công thức trên chỉ là estimator baseline khi `s_b` đã được định nghĩa và calibration. Nếu item inclusion probabilities không đều, thay mean bằng design/model-based weighted estimate và báo riêng uncertainty do sampling, item model và mapping lexical unit.

### Confidence calibration layer

Dùng hold-out calibration data, không dùng cùng dữ liệu người dùng để vừa fit vừa tự xác nhận:

```text
for each calibration response:
    fit item/ability model using response and item metadata
    retain confidence, correctness/criterion, band, format, polarity, L1

for each cell (band, format, polarity, L1 group):
    bin confidence into preregistered bins
    compute observed correctness or criterion success per bin
    compute calibration error and discrimination
    check reliability, sparse-cell count and held-out coverage

at production time:
    calculate K_hat from calibrated response model
    calculate confidence_calibration_status from the user's pattern
    if calibration_status is insufficient:
        set confidence_sensitivity_range = null
        add flag "confidence_not_calibrated"
    else:
        report confidence diagnostic and uncertainty/sensitivity only
```

Có thể dùng các chỉ số như calibration curve, mean absolute calibration error, Brier score hoặc expected calibration error, nhưng ngưỡng production phải được chọn và kiểm tra trên intended population. Không dùng một ngưỡng ECE từ face-recognition study làm ngưỡng vocabulary.

### Quy tắc Not Sure/forced-choice

- Nếu `Not Sure` là một option: lưu nó như response category riêng trong raw data. Không gộp tự động với wrong; cần calibration xác định nó phản ánh abstention, thiếu kiến thức hay risk aversion.
- Nếu forced-choice không có Not Sure: ghi nhận rằng guessing space khác Yes/No. Không dùng correction formula của Y/N cho MC/forced-choice nếu chưa common-person/common-item equating.
- Nếu confidence được hỏi sau forced-choice: confidence có thể là diagnostic cho overconfidence/underconfidence, không làm thay đổi điểm correctness trước khi có validated model.
- Low confidence + correct không tự động là guessing; high confidence + wrong không tự động là careless. Cả hai là pattern cần kiểm tra bằng calibration/response-time/hold-out criterion.

## So sánh với Preply

| Thành phần | Preply cần xác minh | Quy tắc đề xuất |
|---|---|---|
| Response format | Direct methodology endpoint trả 403 trong iteration này; chưa có evidence item-level về Yes/No, MC, Not Sure hay confidence. | Công khai format; nếu Y/N có pseudowords thì lưu hit/false-alarm và calibrate SDT. |
| Guessing | Chưa có source verified trong iteration này cho correction nội bộ của Preply. | Correction phụ thuộc false alarms, pseudoword properties, band/format/L1; không dùng raw hit rate. |
| Confidence | Chưa có Preply confidence data hoặc calibration threshold. | Confidence optional/diagnostic; báo calibration status và sensitivity, không cộng thành words. |
| Lexical count | Các iteration trước đã ghi nhận vendor scale cần phân biệt khỏi word-family/domain coverage. | Giữ `K_hat` theo vocabulary universe; response-format mapping và confidence layer không thay đổi estimand. |
| Uncertainty | Chưa có Preply item-level coverage validation cho confidence/format. | Tách response/model interval khỏi confidence sensitivity; null khi thiếu calibration. |

## Validation plan

1. **Item-bank calibration:** tạo balanced sample real words/pseudowords theo band, frequency, length, orthographic neighborhood và supported L1; kiểm tra pseudoword quality và local dependence.
2. **Format bridge:** cùng người làm Y/N, MC/forced-choice và một criterion task/translation task; dùng common-person/common-item linking, không so raw percentages.
3. **Confidence pilot:** hỏi confidence sau từng response trong một mẫu đủ lớn; preregister bins/cells; kiểm tra calibration theo band, polarity, format và L1.
4. **Held-out coverage:** ước lượng `K_hat` và confidence diagnostics trên hold-out items; kiểm tra interval coverage và sensitivity khi bỏ confidence.
5. **Decision consistency:** kiểm tra các kết luận thực dụng (ví dụ band classification) có đổi khi dùng raw, SDT-corrected hoặc model-based score không.
6. **Transport:** nếu phục vụ nhiều L1, kiểm tra DIF/response bias cho pseudoword và confidence; không công bố L1-adjusted score trước khi có balanced calibration và external validation.
7. **Preply comparison:** chỉ đối chiếu numerical output sau khi biết item bank, format, lexical universe và vendor calibration; hiện chưa đủ dữ liệu để tái tạo score hoặc xác minh margin của Preply.

## Gaps và kết luận iteration

- Chưa tìm được nguồn xác thực cho hệ số vocabulary-specific biến confidence thành `P(known)` hoặc word count.
- Chưa có Preply item-level response format, pseudoword bank, confidence data, correction formula hoặc calibration sample; direct endpoint trả HTTP 403.
- Bằng chứng mạnh nhất trong iteration là false-alarm correction cho Y/N và SDT correction cho response bias. Confidence nên được triển khai như lớp diagnostic/uncertainty có điều kiện, không phải một nguồn “words” bổ sung.
- Bước tiếp theo nên ưu tiên response-format bridge và calibration protocol trên cùng người dùng, trước khi tối ưu một confidence-adjusted estimator.
