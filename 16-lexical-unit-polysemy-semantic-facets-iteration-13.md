# Iteration 13 — lexical unit, polysemy và semantic-facet calibration

## Phạm vi và direction

Iteration này kiểm tra một vấn đề cấu trúc chưa được vận hành hóa trong các vòng trước: một item từ vựng đang đo **form**, **lemma/flemma/word family**, hay một **meaning sense** cụ thể? Direction được chọn là:

> Lexical-unit and semantic-facet calibration: verify how flemma/lemma/word-family choices, polysemy and meaning-recall versus multiple-choice alter what a vocabulary-size item measures; use primary research to derive a dual-estimand item-bank manifest and rules for avoiding false precision from one form or one sense.

Đây là direction khác với các vòng trước ở chỗ chuyển tranh luận về “đơn vị từ” thành schema item-bank và quy tắc báo cáo; không xem một câu trả lời đúng là bằng chứng tự động cho toàn bộ family hoặc mọi sense.

## Nguồn đã kiểm tra

1. Stuart McLean, dự án KAKENHI-16K16890, trang cơ sở dữ liệu nghiên cứu quốc gia Nhật Bản. URL trả HTTP 200 với user-agent trình duyệt. Trang nêu mục tiêu, kết quả cuối và các bài báo liên quan.
   - URL: https://kaken.nii.ac.jp/grant/KAKENHI-PROJECT-16K16890/
2. Saito & Shintani, *Exploring polysemy in the Academic Vocabulary List: A lexicographic approach*, bản PDF tại kho Birkbeck. URL trả HTTP 200; PDF được tải và trích xuất bằng pypdf.
   - URL: https://eprints.bbk.ac.uk/id/eprint/46038/3/45432.pdf
3. Preply, *How does the vocabulary test work?*, bản văn bản qua `r.jina.ai`. Endpoint proxy trả HTTP 200 và nội dung phương pháp; endpoint Preply trực tiếp vẫn không dùng được trong môi trường này. Đây là nguồn mô tả của nhà cung cấp, không phải kiểm định độc lập.
   - URL: https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works

Các URL DOI/nhà xuất bản khác được probe trong iteration nhưng trả 403 và không được dùng làm nguồn trích dẫn mới.

## Findings đã xác minh

### 1. Lexical unit phụ thuộc quần thể và mục đích

Trang KAKEN tóm tắt kết quả nghiên cứu của McLean rằng **flemma hoặc lemma, không phải word family**, là đơn vị đếm từ phù hợp nhất cho cả ngôn ngữ tiếp nhận và sản sinh của sinh viên đại học Nhật. Kết luận này rất hữu ích để bác bỏ việc mặc định word family luôn là đơn vị đúng, nhưng không nên biến thành hằng số phổ quát: nó được xác lập trên một quần thể/ngôn ngữ cụ thể và cần được kiểm tra lại cho người dùng mục tiêu.

Hệ quả: hệ thống phải lưu `lexical_unit` như một thuộc tính versioned (`headword`, `lemma`, `flemma`, hoặc `word_family`), không suy ra đơn vị từ tên bài test. Hai người cùng trả lời đúng một surface form có thể được tính giống nhau ở scale headword nhưng khác nhau ở scale family nếu family member chưa được kiểm tra.

### 2. Số item trong band và format truy hồi là hai facet khác nhau

Cùng trang KAKEN báo cáo rằng 30 item không đại diện chính xác cho một band 1.000 từ, trong khi 65 item là một cân bằng thực dụng giữa độ chính xác và tính khả thi. Trang này cũng báo cáo meaning-recall đại diện construct đọc tốt hơn multiple-choice trong dự án.

Đây không phải tham số đã calibration cho sản phẩm mục tiêu. Nó là bằng chứng thiết kế để đưa vào validation plan: nếu muốn nói về band-specific estimates, cần kiểm tra độ bao phủ với cỡ mẫu gần mức đã nghiên cứu; nếu dùng MCQ vì tốc độ, phải coi format là facet riêng và không dùng hệ số từ recall để “sửa” MCQ khi chưa có common-person calibration.

### 3. Polysemy tập trung đáng kể ở vùng tần suất cao

Nghiên cứu AVL operationalize polysemy bằng việc một lemma có hơn một definition trong cả Collins COBUILD Advanced Learners’ Dictionary và WordNet. Trong 2.673 AVL lemmas hiện diện ở cả hai nguồn, sau khi loại homonyms, 919 (34,38%) được phân loại là polysemous; 607 (66,05% theo phép chia 607/919; phần abstract của bài ghi 66,05%, trong khi phần Highlights hiển thị 65,05% — cần coi đây là một bất nhất báo cáo nguồn) trong số polysemous lemmas nằm ở 1.000 AVL lemmas tần suất cao nhất.

Hệ quả đo lường: một item ở band cao không mặc nhiên dễ theo nghĩa “chỉ có một nghĩa quan trọng”. Nếu stem hoặc lựa chọn chỉ kiểm tra một sense, điểm đúng chỉ chứng minh knowledge của sense/facet đó. Item bank cần `sense_id`, `sense_source`, và `sense_scope`; nếu không có annotation sense đáng tin cậy thì chỉ xuất form-level estimate và ghi rõ giới hạn.

### 4. Quan hệ frequency–number-of-senses là phi tuyến

Bài AVL báo cáo số meaning definitions và tần suất lemma có tương quan dương nhưng phi tuyến: từ tần suất thấp thường monosemous hơn; sau một ngưỡng, số definitions tăng cùng frequency. Vì thế frequency rank không đủ để dự đoán semantic coverage hay item difficulty.

Quy tắc đề xuất: frequency dùng để tạo sampling frame và strata, không dùng như proxy duy nhất cho số sense hoặc độ khó. Các item có polysemy cao nên được phân tầng/flag riêng; sensitivity analysis phải so sánh estimate form-level với estimate sense-aware trên cùng người làm.

### 5. Preply và scale lemma/flemma là hai estimand khác nhau

Methodology của Preply mô tả một dictionary có hơn 45.000 entries, xếp theo frequency từ speech và writing. Họ mô tả quy tắc cộng frequency của derived forms vào headword rồi loại derived form; ví dụ `quick` và `quickly` không được giữ như hai entry độc lập trong dictionary frame.

Do đó số Preply là dictionary/headword scale với quy tắc gộp riêng. Không được dùng số Preply làm số lemma, flemma hoặc word-family mà không có mapping và common-person/common-item calibration. Báo cáo nên giữ ít nhất hai output:

- `V_headword_preply_compatible`: chỉ khi frame, exclusions và gộp derived forms được tái tạo hoặc được calibration.
- `V_lemma_or_flemma_research`: estimand độc lập, dùng lexical-unit manifest và item responses tương ứng.

## Item-bank manifest đề xuất

Mỗi candidate item nên có tối thiểu các trường sau:

```text
item_id, bank_version, surface_form,
lemma_id, flemma_id, word_family_id,
lexical_unit_target, sense_id, sense_source, sense_scope,
frequency_corpus, corpus_version, token_frequency, frequency_rank,
frequency_band, domain_tags, part_of_speech,
retrieval_format, stem_version, distractor_set_version,
loanword/cognate_flag, exclusion_reason,
anchor_flag, exposure_count, calibration_status
```

`lexical_unit_target` là trường bắt buộc và không được suy đoán khi runtime. `sense_id` có thể là `unknown` trong giai đoạn thu thập candidate, nhưng item đó không được dùng để claim sense-aware score cho đến khi annotation được review. `corpus_version` và `bank_version` giúp tái lập frame khi corpus hoặc dictionary thay đổi.

## Thuật toán đề xuất sau iteration 13

### Hai estimator song song

Với estimand `u` (ví dụ headword, lemma hoặc flemma), chia frame thành strata `b` theo frequency/domain đã version hóa. Với item `i` có inclusion probability `pi_i` và response `y_i` (đúng/sai theo format đã định nghĩa), dùng:

```text
w_i = 1 / pi_i
p_hat[b,u] = sum_i_in_b(w_i * y_i) / sum_i_in_b(w_i)
V_hat[u] = sum_b N[b,u] * p_hat[b,u]
```

`N[b,u]` là số đơn vị lexical trong frame của đúng estimand, không phải số surface forms của một frame khác. Nếu dùng adaptive routing, phải lưu `pi_i`; không được coi sample CAT là random sample đều nhau.

### Pseudocode

```text
build_frame(corpus_version, dictionary_version, lexical_unit):
    normalize_forms()
    map_surface_to_lemma_flemma_family()
    aggregate_or_split_only_according_to(lexical_unit)
    annotate_frequency_band_and_sense()
    exclude_and_record_reason_for_each_removed_unit()
    return versioned_frame

administer(person, bank_version, target_format):
    sample_or_route_items_with_logged_probability()
    collect(response, latency, item_id, form, sense_id, exposure_metadata)
    score_only_against_target_lexical_unit_and_target_sense()
    return response_log

estimate(response_log, frame):
    compute_design_weighted_estimate_for_each_unit()
    compute_design_SE_and_quality_flags()
    if common-person/common-item linking exists:
        estimate linking_to_other_unit_scale()
    else:
        keep headword/lemma/flemma outputs separate
    run sensitivity: form-level vs sense-flagged subset,
                    recall vs MCQ if both are available
    return estimates, intervals, flags
```

### Không tự động quy đổi format hoặc lexical unit

Không có hệ số đã xác minh để đổi trực tiếp MCQ sang meaning-recall, hoặc word-family sang lemma/flemma cho Preply. Nếu thiếu nguồn xác thực cho hàm quy đổi, phải ghi: **“chưa tìm được nguồn xác thực cho ý này”**. Hàm linking chỉ được fit bằng common-person/common-item pilot, có hold-out validation và báo uncertainty của linking riêng với sampling SE.

## So sánh với Preply

| Thành phần | Preply được mô tả | Thiết kế đề xuất |
|---|---|---|
| Frame | Dictionary hơn 45.000 entries, rank từ corpus speech/writing | Frame versioned, công bố corpus, dictionary và lexical unit |
| Derived forms | Cộng frequency derived forms vào headword rồi bỏ derived form | Chọn headword/lemma/flemma/family tường minh; mapping lưu trong manifest |
| Semantic facet | Trang phương pháp không công bố sense-level calibration | `sense_id`/scope bắt buộc cho claim sense-aware; form-level nếu thiếu annotation |
| Format | Hai giai đoạn, second phase khoảng 120 words theo mô tả của Preply | Sampling/adaptive tùy mục tiêu, log `pi_i`, format và common anchors |
| Uncertainty | Preply mô tả margin khoảng ±10% dựa trên mô hình vendor | Tách design/measurement/linking/construct uncertainty; CI phải kiểm tra coverage |
| Quy đổi | Không có mapping độc lập sang lemma/flemma/word family | Không quy đổi nếu chưa common-person/common-item calibration |

## Validation plan bổ sung

1. Tạo một pilot gồm người học nhiều L1 và trình độ; mỗi người làm các block liên kết: headword-compatible, lemma/flemma, và nếu có thể word-family; thêm meaning-recall và MCQ trên common items.
2. Với các lemma polysemous, chọn nhiều sense đã annotation; kiểm tra liệu một form-level response có dự báo sense-level response hay không. Không giả định điều này trước khi đo.
3. So sánh 30 và khoảng 65 item trên từng 1.000-unit band trong cùng thiết kế; báo bias, RMSE, coverage của interval và thời lượng, không chỉ correlation.
4. Fit linking model cho các scale chỉ trên training respondents/items; đánh giá trên hold-out người và hold-out item. Report linking SE riêng.
5. Kiểm tra DIF theo L1, loanword/cognate flag và domain; nếu scale thay đổi theo nhóm, xuất subgroup calibration hoặc sensitivity thay vì gộp âm thầm.
6. Tái lập Preply-compatible estimate chỉ khi có dictionary/headword mapping và rules tương ứng. Nếu không có, report side-by-side chứ không gọi một output là bản chuyển đổi của output kia.

## Gaps còn lại

- Chưa có item bank và response-level production data của Preply để kiểm tra sense coverage, format effect, mapping và calibration.
- Chưa có hệ số quy đổi đã xác minh giữa Preply headword scale và lemma/flemma/word-family scale; chưa tìm được nguồn xác thực cho hệ số dùng chung.
- Kết quả flemma/lemma và 65 item/band từ KAKEN có phạm vi quần thể/ngôn ngữ cụ thể; cần replication ở quần thể mục tiêu.
- Nghiên cứu AVL dùng definitions của hai nguồn từ điển để operationalize polysemy; điều này không đồng nhất với mọi taxonomy sense trong production item bank.
- Cần response data để tách semantic knowledge khỏi sampling error, format effect và response-process/guessing signals.
