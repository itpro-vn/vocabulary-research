# Iteration 23 — Use-case, task coverage và diễn giải điểm số

## 1. Câu hỏi nghiên cứu

Một vocabulary-size estimate chỉ trả lời “người làm bài nhận biết bao nhiêu đơn vị từ theo một universe/estimand cụ thể”. Nó không tự động trả lời người đó đọc được loại văn bản nào, nghe được loại nội dung nào, hoặc tương đương CEFR nào. Iteration này kiểm tra cách nối breadth estimate với lexical coverage và intended use, đồng thời đặt guardrail cho diễn giải CEFR.

## 2. Nguồn đã fetch và verify

| Nguồn | HTTP | Nội dung đã dùng |
|---|---:|---|
| Nation (2006), *How Large a Vocabulary Is Needed for Reading and Listening?* | 200 | 14 danh sách 1.000 word-family từ BNC; điều kiện 98% coverage; ước lượng 8.000–9.000 word-family cho viết và 6.000–7.000 cho nói. [PDF](https://www.lextutor.ca/cover/papers/nation_2006.pdf) |
| Laufer & Ravenhorst-Kalovski (2010), *Lexical threshold revisited* | 200 | Vocabulary size, lexical coverage và reading comprehension là các phép đo liên quan nhưng không đồng nhất; mốc 4.000–5.000/95% và 8.000/98% trong mẫu nghiên cứu. [ERIC PDF](https://files.eric.ed.gov/fulltext/EJ887873.pdf) |
| Council of Europe, *Common European Framework of Reference: illustrative scales* | 200 | Vocabulary Range và Vocabulary Control được mô tả bằng descriptors chức năng, không phải bảng word-count→CEFR. [Official PDF](https://rm.coe.int/168045b15e) |

Các URL trên đều trả HTTP 200 khi kiểm tra với browser User-Agent trong iteration này. Search snippets không được dùng làm bằng chứng độc lập.

## 3. Findings chi tiết

### 3.1 Coverage threshold phụ thuộc intended use

Nation (2006) báo cáo rằng nếu chọn điều kiện 98% text coverage để comprehension không cần trợ giúp, cần khoảng 8.000–9.000 word-family cho written text và 6.000–7.000 cho spoken text. Các con số này được xây từ các frequency lists của BNC và một điều kiện coverage cụ thể. Chúng không phải hệ số phổ quát để nhân một điểm test bất kỳ; thay đổi corpus, domain, spoken/written mix, lexical unit, proper-noun policy hoặc threshold sẽ thay đổi kết quả.

**Hệ quả:** item bank phải lưu `corpus_version`, `domain_profile`, `frequency_band`, `lexical_unit` và `coverage_threshold`. Không được lấy một vocabulary count không rõ universe rồi gắn nhãn “đủ cho đọc/nghe”.

### 3.2 Coverage không đồng nhất với comprehension

Laufer & Ravenhorst-Kalovski đo ba biến riêng: vocabulary size bằng Levels Test, lexical coverage bằng Vocabulary Profile và reading comprehension bằng một bài chuẩn hóa. Abstract của bài báo nêu rằng tăng nhỏ vocabulary knowledge có thể cải thiện reading comprehension dù hầu như không tăng text coverage. Bài báo đề xuất, trong mẫu của họ, một mốc tối thiểu 4.000–5.000 word families tạo 95% coverage và mốc tối ưu 8.000 word families tạo 98% coverage, gồm proper nouns.

**Hệ quả:** thuật toán không được dùng `coverage_hat` như proxy hoàn hảo cho comprehension. Báo cáo nên có hai lớp:

1. `breadth_estimate`: ước lượng số đơn vị từ theo estimand đã công bố;
2. `coverage_projection`: dự báo tỷ lệ token được bao phủ trong một corpus/domain profile cụ thể, kèm uncertainty và cảnh báo rằng đây không phải điểm comprehension.

Nếu cần claim về comprehension, phải có criterion calibration bằng task đọc/nghe thật trên population mục tiêu.

### 3.3 CEFR là mô tả năng lực chức năng, không phải vocabulary-count scale

Trong bảng `VOCABULARY RANGE` của tài liệu Council of Europe, A1 được mô tả là basic vocabulary cho tình huống cụ thể; A2 là đủ cho giao dịch thường nhật; B1 là đủ cho các chủ đề đời sống với circumlocution; B2 bao phủ chủ đề chung và lĩnh vực; C1–C2 mô tả lexical repertoire rộng, idiomatic expressions, colloquialisms và sắc thái nghĩa. Tài liệu tách `VOCABULARY CONTROL` khỏi `VOCABULARY RANGE`.

Không tìm thấy trong PDF một bảng chuyển đổi trực tiếp từ số word-family/headword sang CEFR. Vì vậy vocabulary-size test có thể cung cấp bằng chứng hỗ trợ cho một validation study, nhưng không được tự suy ra `CEFR_level` từ `estimate` nếu chưa có common-person criterion calibration. Những mapping số từ→CEFR lấy từ nguồn khác phải được ghi là external mapping, không phải kết quả nội tại của test.

## 4. Thuật toán cập nhật

### 4.1 Data contract

Mỗi report phải lưu:

```text
breadth_estimate
breadth_unit                 # headword | lemma | word_family
vocabulary_universe_version
breadth_interval             # CI/credible interval đã calibration
coverage_profiles[]          # domain, mode, corpus_version, threshold
coverage_projection
coverage_interval
coverage_status              # below | near | above | not_calibrated
intended_use
cefr_mapping_status          # not_available | externally_linked | validated
```

### 4.2 Coverage projection

Với profile `d`, corpus token `t` có lexical unit `u_t`, và tập đơn vị được ước lượng là `K`, tính:

```text
coverage_hat(d) = sum_t 1[u_t in K] / T_d
```

Nếu `K` là latent estimate thay vì tập đã quan sát đầy đủ, tính coverage qua posterior/bootstrap draws:

```text
coverage_draw_r(d) = sum_t 1[u_t in K_draw_r] / T_d
coverage_hat(d)     = median_r coverage_draw_r(d)
interval(d)         = quantile(coverage_draw_r(d), [0.025, 0.975])
```

Không được dùng một interval của vocabulary count để giả vờ là interval của comprehension. Cần propagate uncertainty từ band sampling/IRT, lexical mapping, corpus sample và domain shift; nếu chưa calibration thì đặt `coverage_status=not_calibrated`.

### 4.3 Task-specific stopping/decision rule

```text
estimate breadth with the calibrated item model
for each supported domain/mode profile d:
    generate vocabulary-universe draws
    compute coverage_projection(d) for each draw
    report median and calibrated interval
    if intended threshold q has validated criterion link:
        status = above only if lower_interval(d) >= q
        status = below only if upper_interval(d) < q
        otherwise status = near/indeterminate
    else:
        status = not_calibrated
return breadth + coverage profiles + uncertainty + caveats
```

`above`/`below` chỉ được dùng khi threshold và interval coverage đã được kiểm định trên population mục tiêu. Không nên gắn một status CEFR vào kết quả này.

## 5. Đối chiếu với Preply

- Preply-like output có thể hữu ích như một single breadth estimate, nhưng estimate chỉ có ý nghĩa sau khi công khai unit, universe, corpus/domain weights và item calibration.
- Trong các iteration trước, endpoint test và `how-it-works` của Preply trả HTTP 403 khi fetch trực tiếp; chưa có public item bank, response-level data, routing probabilities hoặc common-person criterion sample để kiểm định coverage projection hay CEFR linking. Vì vậy **chưa tìm được nguồn xác thực cho** một công thức riêng của Preply để đổi điểm sang task coverage, comprehension hoặc CEFR.
- Nếu Preply chỉ trả một count, proposed algorithm nên giữ count đó như output breadth (sau khi xác định estimand), rồi bổ sung coverage profiles riêng. Không nên so sánh trực tiếp count của Preply với mốc Nation/Laufer nếu một bên là dictionary headwords còn bên kia là word families.

## 6. Validation plan

1. Tạo corpus manifest cho từng profile: source, date, genre, tokenization, proper-noun policy, lexical-unit mapping và frequency version.
2. Dùng common-person sample làm bài breadth test và task đọc/nghe thực tế; ước lượng association nhưng không mặc định association là conversion.
3. Kiểm tra coverage calibration: nếu báo 95%/98%, đánh giá interval coverage và classification (`below/above`) trên held-out texts.
4. Kiểm tra domain shift bằng written/spoken và general/academic/professional profiles riêng; không gộp một threshold.
5. Nếu muốn CEFR output, phải xây common-person linking study với CEFR-relevant performance evidence và báo linking error; nếu chưa làm, giữ `cefr_mapping_status=not_available`.
6. Re-run khi corpus, dictionary, word-family rules hoặc item bank đổi version; không so sánh longitudinal score nếu chưa equate.

## 7. Open gaps

- Chưa có item bank/response-level data của Preply để xác định lexical unit, item inclusion và calibration.
- Chưa có common-person/hold-out data để ước lượng coverage-to-comprehension mapping hoặc CEFR linking cho population mục tiêu.
- Chưa có bằng chứng xác thực rằng một threshold cố định áp dụng đồng thời cho mọi domain, mode, learner group hay task.
