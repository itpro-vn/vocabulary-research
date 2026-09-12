# Iteration 14 — distractor và option-function calibration

## Phạm vi và direction

Iteration này chuyển trọng tâm từ lexical unit/sense sang **chức năng của distractor và số option** trong item. Direction được chọn:

> Distractor and option-function calibration: verify how paradigmatic versus syntagmatic versus unrelated distractors, number of options, collocation cues and constructed-response versus MCQ change item difficulty and construct validity; derive an option-functioning QA gate and partial-knowledge policy for vocabulary-size estimation.

Đây là một facet riêng: cùng target word, frequency band và người làm bài vẫn có thể nhận điểm khác nhau nếu distractor làm thay đổi guessing, collocation hoặc cued recall. Do đó không được coi đáp án MCQ là quan sát thuần túy của “biết từ”.

## Nguồn đã verify

1. Hoshino, *Relationship between types of distractor and difficulty of multiple-choice vocabulary tests in sentential context*, Language Testing in Asia 3(16). Trang Springer trả HTTP 200 và nội dung toàn văn đã được fetch.
   - URL: https://link.springer.com/article/10.1186/2229-0443-3-16
2. Currie, *The number of options in multiple choice items in language tests*, Language Testing in Asia. Trang Springer trả HTTP 200 và nội dung toàn văn đã được fetch.
   - URL: https://link.springer.com/article/10.1186/s40468-014-0008-7

Nguồn (2) nghiên cứu bài language structure/reading, không phải vocabulary-size test thuần túy; các hệ quả về option count chỉ được dùng như bằng chứng thiết kế MCQ cần kiểm định lại trên item vocabulary mục tiêu.

## Findings đã xác minh

### 1. Distractor phải được mô tả như một thành phần đo lường

Hoshino tạo ba điều kiện: distractor paradigmatic liên quan nghĩa của đáp án, distractor syntagmatic là collocate với từ trong câu, và distractor control không có quan hệ nghĩa/cú pháp liên quan. Các distractor được giữ cùng word class và cùng frequency level với đáp án. Distractor syntagmatic được chọn từ 100 collocation mạnh nhất trong cửa sổ ±5 từ bằng log-log score; tác giả tránh mutual information vì MI có xu hướng cho điểm cao với từ tần suất thấp. Ba native speakers kiểm tra để xác nhận chỉ đáp án đúng mới phù hợp context.

**Quy tắc triển khai:** item manifest phải lưu `distractor_relation`, `part_of_speech`, `frequency_band`, `collocation_source`, `context_validation_status` và người/qui trình review. Không nên chỉ lưu đáp án đúng và rank tần suất.

### 2. Loại distractor làm thay đổi difficulty

Trong thí nghiệm 372 sinh viên Nhật, loại distractor có hiệu ứng có ý nghĩa lên kết quả: `F(2,372)=31.60`, `p<.001`, `eta²=.08` (cỡ vừa). Theo Tukey HSD, distractor control tạo item dễ hơn paradigmatic, còn paradigmatic dễ hơn syntagmatic; khác biệt PARA/SYN rõ hơn ở nhóm năng lực trung bình và thấp.

Hệ quả: hệ số quy đổi kiểu `raw_correct × constant` không đủ nếu các form không giữ blueprint distractor giống nhau. Nếu bank có nhiều loại distractor, difficulty calibration phải ước lượng theo item và/hoặc facet distractor, thay vì dùng frequency rank làm proxy duy nhất.

### 3. Context có thể đưa collocation vào construct

Khi trong cùng proposition có expression chưa biết, khác biệt giữa ba loại distractor biến mất: `F(2,109)=.05`, `p=.95`, `eta²=.00`. Khi không có expression chưa biết, khác biệt xuất hiện: `F(2,665)=10.89`, `p<.001`, `eta²=.02`. Diễn giải của nghiên cứu là người làm bài khai thác collocation/context để chọn đáp án; nếu thiếu từ trong proposition thì họ không nhận ra quan hệ đó.

**Quy tắc estimand:** item dạng supplying/cloze phải được gắn `context_burden` và `collocation_facet`. Nếu mục tiêu là written receptive vocabulary breadth, ưu tiên matching target–meaning hoặc context tối thiểu đã kiểm soát; không trộn điểm collocation vào vocabulary-size estimate nếu chưa có common-person calibration.

### 4. QA option-functioning có thể đo bằng response data

Currie báo cáo AENO (actual effective number of options) đo độ phân tán lựa chọn, từ 1 đến số option `k`; hướng dẫn được nghiên cứu dẫn lại là giá trị lý tưởng gần `k`, trong khoảng `k−0.5` đến `k`. Nghiên cứu cũng gọi distractor là **performing** nếu lựa chọn tăng theo thứ tự low > middle > high, và **discriminating** nếu có point-biserial âm có ý nghĩa với tổng điểm.

Trong dữ liệu của nghiên cứu, mean AENO của 3/4/5-option lần lượt là 2.44/3.03/3.49 cho structure và 2.51/2.91/3.50 cho reading. Số option cao hơn làm phân tán lựa chọn rộng hơn, nhưng không đảm bảo distractor hoạt động hoặc tăng validity.

**Gate đề xuất trước khi publish item:**

- kiểm tra mỗi distractor có tỷ lệ chọn đủ quan sát được;
- kiểm tra monotonicity low > middle > high với khoảng tin cậy hoặc kiểm định phù hợp;
- kiểm tra point-biserial của distractor và item-total discrimination;
- lưu AENO và tỷ lệ non-functional distractor;
- review item nếu một option gần như không được chọn, hút nhóm năng lực cao, hoặc làm nhiều đáp án hợp lý.

Các ngưỡng số cụ thể chưa được calibration cho sản phẩm này; không tự áp dụng ngưỡng phổ quát từ một mẫu khác.

### 5. Không có correction phổ quát chỉ từ số option

Nghiên cứu 3/4/5-option không tìm thấy khác biệt có ý nghĩa giữa format về concurrent validity, Cronbach alpha, facility trung bình và discrimination tổng thể. Tuy vậy 3-option có xu hướng dễ hơn do guessing/cued recall; nhiều distractor hơn đôi lúc khiến người đã trả lời đúng ở short-answer chọn nhầm option. Nghiên cứu cũng quan sát khác biệt lớn hơn giữa constructed-response và MCQ so với khác biệt giữa 3, 4 và 5 option.

**Quy tắc:** cố định số option trong blueprint hoặc đưa option count vào calibration; randomize vị trí đáp án; không trừ một xác suất đoán chung chỉ dựa trên `k`. Nếu cần link MCQ với recall, phải có common-person/common-item study và báo uncertainty của linking riêng.

### 6. Partial knowledge chỉ là diagnostic khi chưa có calibration

Hoshino nêu khả năng dùng loại distractor để thu được thông tin về partial vocabulary knowledge, tương tự phân biệt lựa chọn liên quan nghĩa/collocation với lựa chọn không liên quan. Nhưng matching và supplying có construct khác nhau; cùng một lựa chọn sai không thể tự động biến thành cấp độ mastery.

**Output nên tách:**

- `V_size_primary`: chỉ dùng response scoring đã calibration cho lexical unit, format và target sense;
- `partial_knowledge_profile`: các pattern chọn distractor, collocation sensitivity và uncertainty flag;
- `format_sensitivity`: chênh lệch MCQ/recall nếu có dữ liệu ghép cặp.

Không dùng profile partial knowledge để cộng/trừ trực tiếp vào `V_size_primary` trước khi có validation.

## Cập nhật thuật toán đề xuất

### Item manifest bổ sung

```text
item_id, bank_version, surface_form,
lexical_unit_target, sense_id, frequency_band,
retrieval_format, stem_version, context_burden,
collocation_facet, distractor_set_version,
distractor_id, distractor_relation, distractor_pos,
distractor_frequency_band, collocation_source,
option_position, answer_key, review_status,
AENO, distractor_selection_rates,
performing_flag, discriminating_flag,
item_difficulty, item_fit, calibration_status
```

### QA pseudocode

```text
qa_item(item, pilot_responses):
    assert exactly_one_key_fits(item.stem, item.options)
    assert same_pos_and_blueprint_band(item.key, item.distractors)
    if item.format == "supplying":
        annotate_context_burden(item)
        annotate_collocation_facet(item)

    rates = option_selection_rates(pilot_responses)
    aeno = actual_effective_number_of_options(rates)
    monotonic = distractor_choice_rate(low) >=
                distractor_choice_rate(middle) >=
                distractor_choice_rate(high)
    pbis = distractor_point_biserials(pilot_responses)

    flag_nonfunctional_options(rates, aeno, monotonic, pbis)
    fit_item_irt_or_rasch(pilot_responses)
    return item_with_flags

score_session(responses, frame):
    score_primary_only_on_calibrated_key_and_target_sense()
    attach_option_functioning_and_context_flags()
    compute_design_or_IRT_estimate_and_SE()
    return primary_estimate, diagnostics
```

### Không thay đổi công thức estimand nếu chưa calibration

Với strata `b`, lexical unit `u`, inclusion probability `pi_i` và response `y_i`, vẫn dùng:

```text
w_i = 1 / pi_i
p_hat[b,u] = sum_i_in_b(w_i * y_i) / sum_i_in_b(w_i)
V_hat[u] = sum_b N[b,u] * p_hat[b,u]
```

Nhưng `y_i` chỉ hợp lệ cho `V_hat` khi item đã qua option/context QA và đúng format calibration. AENO, distractor flags, collocation sensitivity và constructed-response disagreement đi vào diagnostic/uncertainty decomposition, không âm thầm biến thành correction.

## So sánh với Preply

| Thành phần | Preply được mô tả trong methodology đã verify ở iteration trước | Quy tắc bổ sung sau iteration 14 |
|---|---|---|
| Unit | Dictionary/headword, derived forms được gộp theo quy tắc vendor | Giữ headword output riêng; manifest phải có lexical unit và sense |
| Sampling | Hai giai đoạn, khoảng 40 từ rồi khoảng 120 từ trong vùng frequency hẹp | Ngoài rank/strata phải version hóa distractor/context blueprint |
| Item construct | Trang methodology không công bố calibration chi tiết cho distractor | Công khai format, context burden, distractor relation và QA flags |
| Guessing | Vendor nêu margin khoảng ±10%; không có production item response để độc lập kiểm định | Không dùng correction theo số option; cần pilot MCQ–recall nếu muốn link |
| Partial knowledge | Chưa có mô tả calibration sense/distractor độc lập | Xuất diagnostic profile, không cộng/trừ vào size chính |
| QA | Chưa xác minh được item bank và response-level data production | AENO, option rates, monotonicity, point-biserial, item-fit và review log |

Preply vẫn là benchmark headword/user-facing, không phải bằng chứng rằng một distractor set cụ thể đã được calibration. Item bank và response-level production data của Preply chưa được công bố/verify trong iteration này.

## Validation plan

1. Tạo các item có cùng target, stem và frequency band nhưng thay distractor relation (control/PARA/SYN); randomize giữa người làm và fit difficulty/ability model.
2. Kiểm tra item DIF theo proficiency, L1 và format; không coi mọi khác biệt distractor là bias trước khi xem intended construct.
3. Thu response-level data để ước lượng AENO, selection rates, distractor point-biserial, item discrimination và item-fit; kiểm tra trên hold-out items.
4. Ghép một subset MCQ với meaning-recall/constructed-response trên cùng người và item; ước lượng linking, bias, RMSE và coverage thay vì giả định guessing correction.
5. So sánh supplying với matching/context-minimal; báo riêng written receptive vocabulary và collocation/context facet.
6. Chỉ đưa item vào production khi một reviewer xác nhận một đáp án đúng duy nhất, distractor không tạo thêm đáp án hợp lệ, và các flags có disposition rõ ràng.
7. Recheck Preply-compatible output chỉ khi có item/response evidence; nếu không, báo side-by-side và ghi rõ: **chưa tìm được nguồn xác thực cho hệ số quy đổi hoặc correction dùng chung cho Preply**.

## Gaps

- Chưa có item bank, response-level data và routing log của Preply để kiểm tra option functioning, context facets hoặc production thresholds.
- Các số liệu Hoshino đến từ 372 sinh viên Nhật và supplying-format vocabulary test; cần replication trên quần thể mục tiêu.
- Các số liệu option count của Currie đến từ language structure/reading, không phải vocabulary-size test thuần túy.
- Chưa có hệ số xác thực để chuyển MCQ sang meaning-recall, hoặc để biến distractor pattern thành số từ cộng/trừ.
- Chưa xác định ngưỡng AENO, tỷ lệ non-functional distractor hay point-biserial phù hợp cho production; các ngưỡng phải được đặt sau pilot và kiểm tra coverage/validity.
- Chưa tìm được nguồn xác thực cho một guessing correction phổ quát theo số option hoặc một mapping dùng chung từ distractor response sang vocabulary-size estimate.
