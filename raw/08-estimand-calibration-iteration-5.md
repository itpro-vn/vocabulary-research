# 8. Iteration 5 — estimand reconciliation và deployment calibration

## 8.1 Direction và phạm vi

Iteration này tập trung vào **cầu nối giữa estimand của sản phẩm tham khảo và estimand nghiên cứu**: cách một con số “vocabulary size” phụ thuộc vào dictionary/corpus, đơn vị đếm, quy tắc gộp derived forms, cách chọn mẫu và calibration. Mục tiêu không phải thay thế các kết luận về sampling/IRT ở các iteration trước, mà làm rõ khi nào có thể so sánh hoặc quy đổi kết quả.

Các URL trong bảng dưới đã được fetch lại bằng HTTP client với browser User-Agent và đều trả HTTP 200 tại thời điểm iteration:

| Nguồn | URL đã verify | Bằng chứng sử dụng |
|---|---|---|
| Preply methodology qua proxy đọc nội dung | <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works> | dictionary/corpus, headword pipeline, midpoint/log-rank, khoảng bất định |
| ERIC record của Kremmel (2016) | <https://eric.ed.gov/?id=EJ1122574> | lemma vs word family; band 500/1.000+ |
| BYU ScholarsArchive, Hashimoto (2016) | <https://scholarsarchive.byu.edu/etd/5958/> | COCA VAST, Rasch reliability, frequency rank–difficulty |
| Wellington/Nation, VST specifications | <https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/vocabulary-tests/the-vocabulary-size-test/Vocabulary-Size-Test-information-and-specifications.pdf> | word-family unit, score expansion, band là sampling frame |

Endpoint Preply gốc trả HTTP 403 trong môi trường nghiên cứu; vì vậy chỉ nội dung proxy HTTP 200 ở trên được dùng làm nguồn đã fetch, không coi endpoint 403 là URL đã xác minh.

## 8.2 Preply: estimand và pipeline được công bố

Preply mô tả một dictionary có hơn 45.000 entries, xếp theo tần suất trong spoken và written English. Quy trình công khai gồm:

1. dùng BNC và dictionary tiếng Anh uy tín;
2. tái cân bằng word counts thành một phần spoken demographic, một phần spoken context-governed và một phần written;
3. cộng tần suất của derived forms vào headword rồi loại các derived forms khỏi danh sách;
4. loại mục không có trong dictionary, gồm place names, people’s names và “gibberish”;
5. xếp các dictionary-matched entries theo tần suất giảm dần.

Trang này cũng nói họ đếm các main entries, không đếm subentries; đây là lựa chọn dictionary-specific. Họ không công bố một bảng ánh xạ đầy đủ từ entry sang lemma hoặc word family. Vì vậy estimate của Preply phải được gắn nhãn **Preply/BNC dictionary-headword scale**, thay vì gọi chung là số word families.

## 8.3 Preply: midpoint, logarithmic sampling và claim về sai số

Thiết kế được công bố là hai bước: khoảng 40 từ phủ rộng để định vị trình độ, tiếp theo khoảng 120 từ trong vùng hẹp quanh transition. Midpoint được minh họa bằng cách cân bằng số từ “không biết” trước midpoint với số từ “biết” sau midpoint; rank của midpoint là point estimate. Các sample points được phân bố gần logarithmic theo rank.

Preply công bố margin of error **±10%**. Lập luận trên trang là standard deviation của sample points xấp xỉ `0,25 × V`, số điểm trung bình `n = 22,5`, nên:

```text
SE_relative = 0,25 / sqrt(22,5) = 0,0527046
margin95_relative = 1,96 × SE_relative = 0,103301 ≈ 10,33%
```

Trang cũng nói test hiện có 120 từ ở phase 2, và làm tròn estimate trên 10.000 đến hàng trăm, còn từ 300–9.999 đến hàng chục. Đây là **mô hình sai số do vendor tự công bố**, dựa trên giả định sample-point distribution gần normal; chưa có response-level data để kiểm tra coverage của khoảng ±10% theo từng mức năng lực, L1 hoặc form. Không nên tái sử dụng ±10% như một định luật cho estimator khác.

## 8.4 Đơn vị đếm không thể đổi bằng một hệ số cố định

Kremmel (2016) ghi trong ERIC abstract rằng hai quy ước truyền thống cần được xem xét lại: word families là counting unit mặc định và frequency bands đều rộng 1.000 mục. Bài lập luận lemma có thể hữu ích hơn cho assessment/pedagogy; band 500 mục có thêm thông tin ở tần suất cao, còn band lớn hơn 1.000 mục có thể phù hợp ở tần suất thấp.

VST specifications của Nation lại định nghĩa một estimand khác: written receptive vocabulary size theo **word families**, với bản 14.000 có 140 items và 10 items mỗi 1.000-family level, tổng điểm nhân 100; hai bản 20.000 có 100 items và nhân 200. Chính tài liệu cảnh báo mỗi level có quá ít item để đo mastery của từng level một cách đáng tin cậy; frequency levels chỉ dùng để tránh bias trong sampling, còn total score mới là mục tiêu.

Hệ quả: nếu cùng một người có `H` trên Preply-headword scale và `F` trên VST-word-family scale, không được giả định `F = aH`, `F = H/k` hoặc dùng một hằng số từ tài liệu khác. Những hệ số đó phải được ước lượng trên sample làm cả hai test và chỉ có giá trị trong universe, population và construct đã calibration.

## 8.5 Frequency rank là frame tốt hơn difficulty model

Hashimoto (2016), trong thesis lưu tại BYU, báo cáo VAST xây trên COCA 450 triệu tokens, với 403 ESL learners. Phân tích Rasch có person reliability 0,96 và separation 4,62. Tuy nhiên frequency rank chỉ giải thích một phần nhỏ biến thiên item difficulty: với 501 items đầu, `r = 0,474`, `r² = 0,225`; khi gom thành các band 1.000 từ, `r = 0,306`, `r² = 0,094`.

Do đó frequency vẫn phù hợp để tạo coverage frame và stratification, nhưng không đủ để gán difficulty hoặc chuyển điểm giữa các test. Bridge nên dùng item-level evidence (và/hoặc latent linking), không dùng rank-only lookup.

## 8.6 Calibration bridge được đề xuất

### Hai output phải tách biệt

Sản phẩm nên trả về:

- `estimate_preply_headword`: chỉ khi tái tạo đúng universe/rank rules tương thích Preply;
- `estimate_research_unit`: estimate trên universe lemma hoặc word-family đã version hóa;
- `unit`, `universe_version`, `corpus_version`, `dictionary_version`, `test_form`, `mode=receptive_recognition`;
- CI/prediction interval cho từng output, cùng quality flags.

Nếu chưa có common-person pilot, chỉ báo hai estimand song song. Không xuất một “converted vocabulary size” duy nhất.

### Pilot để link hai scale

1. Chọn mẫu người đa dạng L1, proficiency, tuổi và mục tiêu sử dụng.
2. Cho mỗi người làm hai form trong counterbalanced order, có common anchors và khoảng nghỉ phù hợp.
3. Lưu response-level data, latency/skips và item metadata; không chỉ lưu tổng điểm.
4. Fit từng scale riêng; kiểm tra item-fit, floor/ceiling, DIF và test-retest.
5. Link latent scales bằng common items/persons hoặc fit regression có kiểm soát population; giữ hold-out sample để đánh giá bias và coverage.
6. Chỉ phát hành bảng quy đổi nếu prediction interval, subgroup error và invariance đạt ngưỡng đã định trước.

Pseudocode:

```text
function report_vocab(responses, preply_universe, research_universe, bridge=None):
    h = estimate_preply_midpoint(responses, preply_universe)
    r = estimate_stratified_or_irt(responses, research_universe)
    out = {"preply_headword": h, "research_unit": r,
           "units": [preply_universe.unit, research_universe.unit]}
    if bridge is not None and bridge.is_valid_for(responses.population,
                                                   preply_universe.version,
                                                   research_universe.version):
        out["linked_estimate"] = bridge.predict(h, r)
        out["linked_interval"] = bridge.prediction_interval(h, r)
    else:
        out["linked_estimate"] = null
        out["linking_status"] = "not_calibrated"
    return out
```

## 8.7 Cập nhật quyết định và gap

- Giữ fixed-length stratified estimator làm baseline research scale; midpoint/log-rank là compatibility mode cho Preply-like headword scale.
- Bắt buộc version hóa vocabulary universe và xuất unit trong API/report.
- Không chuyển thẳng headword ↔ lemma/word-family khi thiếu pilot common-person/common-item.
- Tách vendor-reported uncertainty khỏi CI đã được kiểm định empirically.
- Gap còn lại: item bank và response data sản xuất của Preply; mapping đầy đủ dictionary entry–lemma–word family; calibration sample đa dạng; DIF; independent CI coverage và hold-out link validation. **Chưa tìm được nguồn xác thực cho hệ số quy đổi headword↔lemma/word-family dùng chung.**
