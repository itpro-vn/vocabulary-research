# Iteration 45 — speededness, timed administration và time-policy

## Phạm vi và trạng thái nguồn

Iteration này tách **speededness** khỏi response-time quality control thông thường. Câu hỏi không phải là “người làm nhanh có tốt hơn không”, mà là giới hạn thời gian có làm thay đổi xác suất trả lời đúng, tỷ lệ bỏ item hoặc chiến lược đoán đến mức score không còn chỉ phản ánh vocabulary breadth hay không.

Các URL sau đã được fetch và kiểm tra:

| Nguồn | HTTP | Dùng cho |
|---|---:|---|
| ETS, Cintron (2021), *Methods for Measuring Speededness* | 200 | Định nghĩa, biểu hiện và rủi ro với IRT truyền thống |
| GMAC, Talento-Miller, Guo & Han (2012), *Examining Test Speededness by Native Language* (PDF) | 200 | Nhiều chỉ báo speededness, nhóm ngôn ngữ, completion/time-pressure |
| Crossref API, Applied Linguistics (2025), DOI `10.1093/applin/amaf037` | 200 | Năm timed/untimed measures, 145 người học, CFA |
| Crossref API, DOI `10.1177/02676583261420616` (2026) | 200 | Timed/untimed lexicosemantic judgment và listening proficiency |
| Preply methodology qua `r.jina.ai` | 200 | Mô tả vendor về sampling/midpoint/margin; không thấy time policy |
| Preply direct methodology URL | 403 | Không dùng trực tiếp để suy luận; proxy được ghi rõ là nguồn vendor/provisional |

## Bằng chứng đã xác minh

### 1. Speededness là rủi ro validity, không phải chỉ là latency

ETS định nghĩa speededness là mức độ time limit làm thay đổi performance. Các biểu hiện được nêu gồm random guessing, để lại một phần đáng kể item chưa trả lời và rushed behavior. Báo cáo cũng nêu speeded responses không chỉ phụ thuộc ability, nên không phù hợp với traditional IRT nếu mô hình không xử lý thành phần speeded.

Hệ quả cho vocabulary-size testing:

- `K_hat` breadth phải dựa trên accuracy/knowledge response trong điều kiện không bị time pressure, trừ khi intended construct chính thức bao gồm lexical access speed.
- Nếu có time limit, item cuối không còn trao đổi cùng một quantity như item đầu: response có thể bị censoring bởi thời gian thay vì sai vì không biết.
- Không được dùng một mô hình IRT accuracy bình thường rồi coi omission/rapid guessing như response sai mà không kiểm tra tốc độ làm bài.

Nguồn: <https://www.ets.org/research/policy_research_reports/publications/report/2021/kcvu.html>.

### 2. Cần nhiều chỉ báo speededness, không dùng một completion cutoff duy nhất

Báo cáo GMAC phân biệt power test và speed test theo cách score được xác định: number right so với number reached. Nhiều bài thi chuẩn hóa nằm giữa hai cực vì có time limit và penalties khi không trả lời hết. Báo cáo dùng dữ liệu máy tính để xem nhiều chỉ báo: số item hoàn thành, thời gian còn lại gần cuối, tỷ lệ hoàn thành tất cả item, tỷ lệ hoàn thành ít nhất 75%, time pressure ở nhóm item cuối và rapid guessing.

Hàm ý triển khai:

1. Tách `not_reached`, `omitted`, `answered_wrong`, `answered_correct`, `timeout` trong event log.
2. Lưu item position và elapsed time; nếu chỉ lưu tổng score thì không thể audit speededness sau này.
3. Đánh giá đồng thời completion, late-window latency, omission và accuracy. Rule “80% thí sinh tới item cuối” chỉ là heuristic lịch sử, không phải ngưỡng vocabulary đã calibration.
4. Nếu test intended là power/knowledge test, time limit nên là hard safety cap sau khi pilot chứng minh phần lớn người dùng hoàn thành trong điều kiện không speeded; không dùng cap để tạo thông tin cho `K_hat`.

Nguồn: <https://www.gmac.com/-/media/files/gmac/research/validity-and-testing/rr-12-01-speededness.pdf>.

### 3. Time pressure có thể khác theo L1, nhưng phải điều kiện hóa trên ability

GMAC so sánh 15 nhóm ngôn ngữ với native-English group trong một CAT tiếng Anh toàn cầu. Ở verbal section, Korean có chênh lệch rất lớn về số item hoàn thành so với English (`d = -4.27`, `n = 4,035`) và chỉ 47% hoàn thành toàn bộ verbal section. Mean time của Japanese và Korean cao hơn English với effect size khoảng 0.70 và 0.71. Tuy nhiên, khi kiểm soát ability, tác giả không tìm thấy khác biệt liên quan giữa các ngôn ngữ so với English.

Không được diễn giải kết quả này thành một “hệ số L1 correction” cố định cho vocabulary. Quy tắc an toàn hơn là:

- kiểm tra interaction `L1 × time_pressure` sau khi điều kiện hóa trên latent ability;
- xem DIF/response-time DIF theo band và format;
- nếu timed score lệch nhưng untimed accuracy không lệch, coi đó là access/time effect và không sửa trực tiếp vào vocabulary count;
- chỉ tạo linked timed scale sau common-person/common-item calibration và hold-out validation.

Nguồn: <https://www.gmac.com/-/media/files/gmac/research/validity-and-testing/rr-12-01-speededness.pdf>.

### 4. Timed và untimed word measures có thể chia sẻ construct nhưng không chứng minh score interchangeable

Metadata/abstract được fetch từ Crossref API cho nghiên cứu Applied Linguistics 2025: 145 learners, 40 English words trong dải 2K–5K, và các measure gồm untimed meaning recognition, untimed form recall, timed Yes–No response-time (có accuracy và RT), masked repetition priming. CFA cho phép một hoặc hai psychometric dimensions; một-factor được ưu tiên vì parsimony nhưng two-factor có predictive validity marginally mạnh hơn đối với self-reported proficiency.

Hệ quả:

- Accuracy và RT có thể cùng liên quan đến lexical knowledge, nhưng RT có thể mang thêm lexical-access/automatization facet.
- `RT` không được quy đổi thành “biết thêm X từ”.
- Production nên giữ `K_hat_breadth` và `access_speed_profile` tách biệt. Nếu muốn một score chung, phải prespecify linking model và kiểm định predictive/criterion validity ngoài mẫu calibration.

Nguồn: <https://api.crossref.org/works/10.1093/applin/amaf037>.

### 5. Một timed lexicosemantic task có thể ít nhạy với time pressure, nhưng bằng chứng task-specific

Crossref API của nghiên cứu 2026 về lexicosemantic judgment task cho biết timed LJT được thiết kế để đo automatized phonological vocabulary knowledge. So với untimed version, timed LJT có liên hệ tương tự với listening proficiency; abstract mô tả effect của time pressure có thể tương đối nhỏ.

Đây là bằng chứng ủng hộ việc đo access-speed trong một task chuyên biệt, không phải bằng chứng rằng mọi timed vocabulary-size test tương đương test receptive breadth. LJT có construct và criterion khác với một estimator đếm lexical units theo frequency rank. Không transport trực tiếp coefficient hoặc equivalence claim sang Preply.

Nguồn: <https://api.crossref.org/works/10.1177/02676583261420616>.

## Đối chiếu với Preply

Preply methodology công khai:

- dictionary hơn 45.000 entries xếp theo frequency;
- phase đầu khoảng 40 từ từ dễ đến khó để định vị;
- phase hai khoảng 120 từ trong vùng hẹp, có midpoint/logarithmic-rank reasoning;
- vendor margin được nêu là khoảng ±10.33% ở confidence 95% theo mô hình sample-point của họ;
- output được làm tròn theo quy mô estimate.

Trong bản methodology đã fetch, không thấy công khai:

- time limit hoặc target completion time;
- response latency được dùng trong score hay không;
- cách phân biệt omitted, not-reached, timeout và answered-wrong;
- rapid-guessing/speededness diagnostic;
- timed-versus-untimed equating.

Vì vậy chỉ có thể nói phương pháp Preply **không công khai speededness layer**, không được khẳng định vendor test là psychometrically untimed. Gap này phải được giữ trong report và không được lấp bằng suy đoán. Nguồn: <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works>.

## Quy tắc thuật toán đề xuất

### Data model tối thiểu

```text
ResponseEvent {
  person_id, form_id, item_id, band_id,
  started_at, submitted_at, elapsed_ms,
  response_status: correct | wrong | omitted | not_reached | timeout,
  score_response, rapid_guess_flag, device_id, qc_flags
}

SpeedAudit {
  form_id, target_population, n,
  completion_rate, completion_rate_75,
  omitted_rate, not_reached_rate,
  late_window_rate, rapid_guess_rate,
  conditional_time_by_ability_and_band,
  subgroup_effects, status
}
```

### Phân tách output

- `K_hat_breadth`: chỉ dùng accuracy/IRT breadth response sau khi loại hoặc mô hình hóa response bị speeded.
- `access_speed_profile`: median/quantile latency chuẩn hóa theo item difficulty và ability; không cộng vào `K_hat`.
- `speededness_status`: `none`, `possible`, `material`, `unknown`.
- `validity_status`: score release status; nếu material speededness thì không phát hành point estimate như breadth chuẩn.
- `time_sensitivity_range`: chênh lệch giữa untimed estimate và các time-cap sensitivity runs khi có data.

### Pseudocode

```text
for each response:
    record elapsed_ms and exact response_status
    if not_reached or timeout:
        do not silently recode as ordinary wrong
    if elapsed_ms < item_rapid_guess_cutoff:
        mark rapid_guess_flag

fit breadth_model on non-speeded calibration responses
fit response-time model conditional on ability, band, item difficulty
compute audit metrics by form, band, ability decile, L1/device when sample permits

speeded = (
    high not_reached/omitted concentration in final positions
    OR material late-window rapid_guess increase
    OR accuracy/completion relation remains after conditioning on ability
    OR subgroup-by-time interaction is material in hold-out data
)

if speeded == false and cap is only a safety cap:
    release K_hat_breadth with ordinary calibrated uncertainty
elif speeded == possible:
    release K_hat_breadth with speed sensitivity flag and range
elif speeded == material:
    do not release breadth point estimate from timed form;
    route to untimed form or report validity_status = speeded

always report access_speed_profile separately
```

Không điền literal ngưỡng “material” từ GMAC/ETS. Các ngưỡng phải được chọn bằng pilot trên target population, simulation và held-out coverage/criterion validation.

### Công thức sensitivity tối thiểu

Nếu có cùng người làm untimed và timed form với common items/persons:

```text
Delta_time = K_hat_timed - K_hat_untimed
SE_Delta = sqrt(SE_timed^2 + SE_untimed^2 - 2 * Cov_timed_untimed)
CI_Delta = Delta_time +/- 1.96 * SE_Delta
```

Nếu không có covariance/linking evidence, không giả định hai estimate độc lập và không báo `SE_Delta` giả. Chỉ báo `time_sensitivity_range` mô tả, hoặc thu thập common-person data.

Với timed response model, có thể mô hình hóa:

```text
logit(P(correct_i = 1)) = theta_person - b_item + DIF_terms
log(elapsed_i) = alpha_item - beta * theta_person + gamma_band + u_person + e_i
```

Hai phương trình chỉ được ghép trong joint model sau khi kiểm tra local dependence và model fit. `elapsed_i` không được dùng như feature trực tiếp để tăng `P(known)` nếu chưa có validation chống circularity.

## Kế hoạch validation

1. **Untimed reference sample:** cùng item blueprint, không time pressure; dùng làm reference breadth scale.
2. **Timed arms:** randomize nhiều time caps và một safety-cap arm; giữ item order/form comparable.
3. **Common-person/common-item linking:** ước lượng `Delta_time`, covariance và conditional effects theo ability/band/L1.
4. **Speed audit:** preregister completion, omission, not-reached, late-window, rapid-guess và response-time DIF metrics; không dùng riêng 80%-finish heuristic.
5. **Equity:** kiểm tra time effect sau conditioning on ability, không áp dụng correction coefficient theo L1 chỉ từ latency thô.
6. **Coverage:** bootstrap/Monte Carlo theo frequency bands và tail, đánh giá CI coverage riêng cho breadth và time sensitivity.
7. **Release gate:** nếu timed arm không đạt non-speeded status hoặc interval quanh `Delta_time` loại zero theo intended precision, chỉ phát hành untimed breadth hoặc gắn validity flag; không gộp access speed vào word count.

## Kết luận iteration

Speededness là một nguồn construct-irrelevant variance có thể làm sai vocabulary breadth, đặc biệt khi time pressure dồn vào item cuối hoặc khác nhau theo L1/ability. Nên thiết kế test breadth như power/untimed test với safety cap, log response status và latency để audit, và giữ lexical access speed thành output riêng. Bằng chứng timed/untimed vocabulary gần đây cho thấy các task có thể chia sẻ latent construct và timed pressure đôi khi nhỏ, nhưng các kết luận đó task-specific, không đủ để equate với Preply. Preply chưa công khai time policy hoặc speededness handling; đây là gap bắt buộc trong validation của estimator.
