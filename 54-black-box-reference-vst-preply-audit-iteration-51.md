# Iteration 51 — Black-box audit của form VST tham chiếu và giới hạn đối chiếu Preply

## Phạm vi và trạng thái nguồn

Direction này kiểm tra một implementation vocabulary-size test có thể fetch trực tiếp để tách:

1. fact quan sát được trong HTML/JavaScript;
2. công thức scoring thực sự chạy;
3. hàm ý triển khai cho một estimator mới;
4. claim về Preply chưa thể xác minh ở callback hiện tại.

Nguồn đã fetch:

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| [Lextutor Recognition Levels Test](https://www.lextutor.ca/tests/vst/) | 200 | HTML, form fields và JavaScript scoring live; trang ghi provenance P. Nation & D. Beglar 2007 |
| [Read (2007), *Second Language Vocabulary Assessment: Current Practices and New Directions*](https://files.eric.ed.gov/fulltext/EJ1072194.pdf) | 200 | Nguồn học thuật để đối chiếu construct MCQ VST và Yes/No |
| Preply test và trang how-it-works do task cung cấp | 403 trong callback | Không dùng làm nguồn đã xác minh |

Tất cả URL được đưa vào bảng nguồn citable đều trả HTTP 200 trong callback. Preply chỉ được ghi như một gap kiểm chứng, không như nguồn đã xác thực.

## 1. Cấu trúc form quan sát được

HTML live của Lextutor có 14 heading: `First 1000`, `Second 1000`, …, `Fourteenth 1000`. Các radio input có tên theo dạng `Lk01_Q1` đến `Lk14_Q10`.

Kiểm đếm trực tiếp trên HTML:

- 14 level/band;
- 10 câu hỏi mỗi band;
- 140 cặp câu hỏi duy nhất;
- 4 radio option cho mỗi câu;
- 560 radio input tổng.

Form khai báo `mode=practice`, action `score_levels.php?mode=practice...`, và toàn bộ 14 band được render trong một form. JavaScript `js_score()` lặp cố định qua mảng `k01` đến `k14`; không có logic chọn band tiếp theo dựa trên câu trả lời. Vì vậy implementation này là fixed-form, frequency-level recognition test, không phải CAT, MST hoặc adaptive routing.

### Hàm ý cho algorithm đề xuất

Khi đối chiếu một sản phẩm như Preply, không được suy ra “adaptive” chỉ từ việc giao diện có nhiều bước hoặc hiển thị một level làm việc. Cần kiểm tra tối thiểu:

- item nào thực sự được request/render;
- xác suất inclusion theo band;
- có dừng/routing trước khi thấy các band còn lại hay không;
- score có dùng tất cả band hay chỉ một subset;
- answer key và scoring nằm ở client hay server.

Manifest production nên lưu `form_version`, `band_id`, `item_id`, `inclusion_probability`, `routing_path` và `scoring_version`; nếu thiếu các trường này thì không thể tái lập score hoặc tính đúng sampling uncertainty.

## 2. Công thức scoring thực sự của form tham chiếu

Trong `js_score()`:

```text
for each band i in 0..13:
    score_i = number of correct answers among 10 items
    percent_i = score_i / 10 * 100
    big_score += score_i
vocab_size = big_score * 100
```

Do đó:

- mỗi đáp án đúng đóng góp 100 đơn vị;
- điểm lý thuyết nằm trong `[0, 14,000]`;
- band score được hiển thị như `score/10` và phần trăm;
- không có guessing correction trong hàm này;
- điểm cuối không dùng IRT ability hoặc item discrimination.

Code còn tính biến `coverage` với các trọng số:

```text
band 1: 0.75 * percent_1
band 2: 0.10 * percent_2
band 3: 0.05 * percent_3
band 4..14: 0.02 * percent_i
```

Tuy nhiên phần hiển thị coverage đã bị comment out; sau đó `coverage` được reset. Vì vậy coverage weights không thay đổi `vocab_size`. Đây là một chi tiết quan trọng để tránh mô tả sai rằng điểm 0–14.000 là weighted corpus coverage.

### Diễn giải đúng

Điểm này là một phép mở rộng tuyến tính: 10 item được dùng như mẫu đại diện cho mỗi block 1.000 lexical units, rồi số đúng được nhân lên. Nó có thể hữu ích cho diagnostic breadth, nhưng không tự động là ước lượng population-calibrated. Sai số còn phụ thuộc representativeness của item trong từng band, item difficulty, local dependence, response format và định nghĩa lexical unit.

Một estimator mới có thể dùng cùng baseline để so sánh, nhưng nên trả cả:

```text
raw_correct
band_scores
lexical_unit
universe_size
estimate
sampling_or_response_interval
model_sensitivity
```

Không nên chỉ lưu một số nguyên `vocab_size` vì sẽ làm mất estimand và uncertainty.

## 3. Client-side answer exposure và giới hạn bảo mật

HTML chứa 14 mảng `var arr` là answer key. Hàm scoring đọc giá trị radio bằng `eval(...)` rồi so sánh với answer key trong browser. Trang practice cũng có nút `Score for Random Answers`, gọi `randomize()` và chọn ngẫu nhiên một trong bốn option cho từng câu.

Đây là fact quan sát được của Lextutor, không phải bằng chứng về nội bộ Preply. Hệ quả kỹ thuật:

- phù hợp với practice/diagnostic, nơi người dùng không cần một score high-stakes;
- không chống được việc xem source, sửa DOM hoặc replay answer;
- repeated attempts có thể bị contamination nếu item pool cố định;
- score client-side không đủ để chứng minh response integrity.

Nếu mục tiêu là score có thể so sánh qua thời gian hoặc dùng làm calibration data, production nên:

1. cấp item từ pool có version và exposure log;
2. giữ answer key ở server hoặc dùng cơ chế response token có kiểm tra server;
3. giới hạn exposure của anchor và item calibration;
4. đánh dấu practice/retest và loại hoặc mô hình hóa response sau exposure;
5. chỉ dùng response integrity đã pass để fit item/person parameters.

Đây là release requirement về measurement integrity, không phải lý do để trừ trực tiếp điểm vocabulary của người dùng.

## 4. Đối chiếu học thuật về construct

Read (2007) mô tả Nation & Gu Vocabulary Size Test là multiple-choice: target word xuất hiện trong câu ngắn không định nghĩa, sau đó có bốn định nghĩa lựa chọn. Đây là một response process recognition form–meaning trực tiếp.

Cùng bài mô tả Yes/No format: real words được trộn với một tỷ lệ đáng kể non-words để phát hiện người làm bài tự báo quá mức. Trong giả định người làm bài trả lời tương đối trung thực, một phép đơn giản là:

```text
adjusted_yes_no = yes_to_real_words - yes_to_nonwords
```

Hai format không thể chia sẻ một correction coefficient mặc định:

- 4-choice MCQ có chance success và distractor functioning;
- Yes/No có self-report bias, false alarm và response style;
- sentence context và definition quality tạo thêm difficulty facets;
- “biết từ” có thể là recognition threshold, không phải productive mastery.

Vì vậy schema phải công bố `test_format` và `construct`. Nếu cần equate MCQ với Yes/No, phải dùng common-person/common-item hoặc calibration sample và hold-out validation; không được chuyển thẳng quy tắc 100-per-correct sang format khác.

## 5. Pseudocode audit/release gate

```text
fetch source with browser-like UA
assert HTTP 200 for every citable source
parse item names, bands, options, answer-key arrays
assert unique_item_count == declared_item_count
assert every band has declared quota
assert every item has exactly one keyed answer
extract scoring function and compute a reference score from fixture responses
assert score fixture matches executable implementation

if source_is_reference_only:
    label result = implementation_observation
else:
    require item-bank and response-level provenance before calling it calibrated

for Preply comparison:
    if official endpoint != 200:
        record gap = "chưa tìm được nguồn xác thực cho ..."
        do not promote proxy/vendor description to current implementation fact
```

Đây là audit gate trước khi dùng một implementation làm reference algorithm. Nó không biến Lextutor thành bằng chứng rằng Preply có cùng item bank hoặc công thức.

## 6. So sánh với Preply và gap hiện tại

| Khía cạnh | Form Lextutor quan sát được | Preply trong callback này |
|---|---|---|
| Item/band | 14 band × 10 item, 140 item; quan sát trực tiếp | Chưa xác minh được current item pool |
| Adaptivity | Fixed form; JS lặp đủ 14 band | Chưa xác minh được routing/inclusion |
| Score | `100 × total correct`, range 0–14.000 | Chưa xác minh được current scoring code |
| Lexical unit | Trang/implementation tham chiếu gắn với VST Nation–Beglar; cần xem specification để chốt đơn vị | Không đủ dữ liệu current để xác minh headword/family mapping trong callback |
| Security | Answer key và score ở client | Chưa xác minh được item exposure/server scoring |
| Uncertainty | Không thấy interval trong hàm practice quan sát được | Chưa xác minh được current interval/calibration |

Các thử nghiệm fetch Preply trong callback (đường dẫn test, how-it-works, trailing slash và query variants) đều trả HTTP 403; proxy fetch cũng trả 403. Do đó chưa tìm được nguồn xác thực cho item pool, số item, answer key, sampling rule, scoring code, result mapping hoặc security controls hiện tại của Preply. Những mô tả Preply đã có trong các iteration trước phải tiếp tục gắn nhãn vendor/provisional nếu không có lần fetch 200 và artifact nguồn tương ứng.

## Kết luận iteration 51

1. Một implementation VST live có thể được audit ở cấp HTML/JavaScript: 14 band, 140 item, fixed-form, 100 đơn vị cho mỗi đáp án đúng.
2. Coverage calculation và displayed vocabulary score là hai nhánh khác nhau; không được gọi điểm cuối là weighted coverage hay IRT score.
3. Client-side answer exposure là giới hạn bảo mật và retest, nhưng không nên biến thành penalty vocabulary trực tiếp.
4. MCQ VST và Yes/No đo response process khác nhau; format và lexical unit phải là metadata bắt buộc trước khi equating.
5. Preply hiện chưa thể kiểm chứng trực tiếp trong callback này; không thêm claim current về Preply ngoài gap đã ghi.

## Nguồn

- https://www.lextutor.ca/tests/vst/
- https://files.eric.ed.gov/fulltext/EJ1072194.pdf
