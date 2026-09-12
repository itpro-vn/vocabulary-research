# 6. Iteration 3 — Criterion validity, predictive validity và guessing bias

## 6.1 Direction và phạm vi

Iteration 3 chọn một hướng khác với hai iteration trước: không tối ưu frequency-stratified estimator hay CAT/IRT, mà kiểm tra **điểm vocabulary-size thực sự đo gì và dự báo được gì**. Mục tiêu là ngăn sản phẩm biến một điểm written receptive vocabulary thành tuyên bố rộng hơn về reading, listening, productive vocabulary hoặc general proficiency mà chưa có bằng chứng.

Nguồn được fetch và kiểm tra HTTP 200 trong iteration:

1. John Read, **Second Language Vocabulary Assessment** (2007), archived PDF mirror for the ERIC item: <https://archive.org/download/ERIC_EJ1072194/ERIC_EJ1072194.pdf>
2. Claudia Harsch & Johannes Hartig, **Comparing C-tests and Yes/No vocabulary size tests as predictors of receptive language skills** (Language Testing, 2016), PDF trên pedocs: <https://www.pedocs.de/volltexte/2018/14980/pdf/0265532215594642_A.pdf>

## 6.2 Vocabulary-size estimate là một estimand hẹp

Read mô tả vocabulary-size measures là các phép đo thường cần một mẫu tương đối lớn đại diện cho một dải frequency đã định nghĩa, cùng một response task đơn giản để người làm test cho biết họ biết từ hay không. Điều này củng cố thiết kế fixed-form: số lượng item cần đủ để mẫu đại diện, nhưng response task nên nhẹ để dành ngân sách cho coverage.

Điểm số nên được gắn nhãn tối thiểu:

```text
construct = written receptive vocabulary breadth
unit      = headword | lemma | word_family
universe  = dictionary/corpus list + version
```

Không được mặc định rằng một người nhận ra dạng viết thì chắc chắn dùng được từ khi nói/viết, biết mọi sense, hoặc có cùng mức độ nhận biết ở modality thính giác. Những diễn giải đó là construct khác và cần criterion evidence riêng.

## 6.3 Frequency list và sampling ảnh hưởng trực tiếp đến điểm

Read ghi nhận các nghiên cứu cũ đã tạo ra ước lượng khác nhau do hai lỗi: không thống nhất “một word” là gì và sampling khiến từ tần suất cao bị đại diện quá mức. Các nghiên cứu sau có ước lượng thực tế hơn khi định nghĩa lexical unit rõ và sampling cẩn thận.

Nguồn cũng nêu không có một frequency list duy nhất là “definitive” cho mọi mục đích. Các list dựa trên corpus cung cấp frequency, range và có thể tách written/spoken; nhưng việc chọn list phải phù hợp với target population và domain. Vì vậy thuật toán không được xuất “số từ tiếng Anh mà bạn biết” như một đại lượng không có điều kiện. Nó phải xuất, ví dụ:

```text
Bạn biết khoảng V word families trong universe U,
được xây từ corpus C, phiên bản T, và đo written receptive recognition.
```

### Hệ quả triển khai

- Manifest của universe là bất biến và có version/hash.
- Ghi rõ `unit`, frequency source, language variety, written/spoken domain và exclusion rules.
- Nếu đổi list hoặc đổi word-family policy, tạo scale version mới; không so sánh thẳng điểm giữa hai universe.
- Báo thêm sensitivity range khi chạy cùng responses qua headword/lemma/word-family universe nếu sản phẩm cần minh họa sự phụ thuộc vào định nghĩa.

## 6.4 Yes/No format: tách breadth khỏi khuynh hướng đoán

Harsch & Hartig (2016) nghiên cứu một mẫu 559 học sinh Đức 14–16 tuổi. Phần X-Lex gồm 100 real-word items, lấy ngẫu nhiên 20 item từ mỗi một trong năm frequency bands đầu (mỗi band 1.000 từ), cộng với 20 pseudowords. Pseudowords có hình thái giống từ thật nhưng không tồn tại, được đưa vào để kiểm soát/correct guessing.

Kết quả quan trọng cho scoring:

- Hit rate (HR) tương quan dương với false-alarm rate (FAR), nghĩa là người đánh dấu nhiều từ thật là “biết” cũng có xu hướng đánh dấu pseudowords là từ đã biết.
- Correlations quan sát được trong bảng của bài: HR với FAR = `.327`; HR với C-test = `.482`; HR với listening = `.491`; HR với reading = `.386`. FAR tương quan với C-test = `-.155`, với reading = `-.158`, còn với listening là `-.097` và không có ý nghĩa thống kê trong mẫu đó.
- Trong các cách chấm thử nghiệm, giữ HR và FAR thành **hai chỉ báo riêng** cho kết quả đáng tin cậy nhất trong mẫu nghiên cứu. HR có thể xem là tín hiệu breadth; FAR là tín hiệu guessing tendency.
- Vì một FAR cao có thể làm HR cao giả tạo, điểm vocab cuối cùng không nên chỉ là tổng “known real words” nếu test có pseudowords.

### Đề xuất scoring bảo thủ

Trong giai đoạn chưa có calibration sản phẩm, không hard-code một penalty phổ quát. Lưu và report:

```text
HR = real_words_marked_known / real_word_items
FAR = pseudowords_marked_known / pseudoword_items
quality_flag = based_on(FAR, response_time, inconsistency, missingness)
```

Sau pilot có criterion data, có thể fit mô hình hiệu chỉnh được giữ lại trên hold-out. Nếu chưa có bằng chứng, FAR chỉ nên tạo cảnh báo hoặc làm biến giải thích trong calibration, không tự động trừ `1/k`, không giả định mọi người đoán như nhau và không thay đổi estimand một cách ẩn.

## 6.5 Predictive validity không đồng nghĩa với vocabulary equivalence

Harsch & Hartig so sánh X-Lex với C-test để dự báo reading/listening. X-Lex có quan hệ đáng kể với cả hai receptive skills, nhưng C-test dự báo mạnh hơn trong bối cảnh và mẫu đó:

| Mô hình | Listening R² | Reading R² |
|---|---:|---:|
| X-Lex HR + FAR, observed scores | .32 | .24 |
| C-test, observed scores | .58 | .53 |
| C-test + X-Lex, observed scores | .60 | .54 |
| X-Lex latent vocabulary + guessing | .43 | .45 |
| C-test latent | .75 | .84 |
| C-test + X-Lex latent | .76 | .85 |

Tác giả kết luận C-test vượt X-Lex trong dự báo receptive skills và phần variance riêng mà X-Lex thêm vào sau C-test là rất nhỏ. Đây không phải bằng chứng X-Lex “không hợp lệ”; nó cho thấy hai format đo construct khác nhau: X-Lex là discrete/decontextualized vocabulary breadth, còn C-test là contextualized processing với nhiều kỹ năng và chiến lược.

### Hệ quả cho product copy và API

Tách ba lớp output:

1. `vocabulary_size_estimate`: ước lượng breadth theo universe đã công bố;
2. `measurement_quality`: FAR, missingness, latency, anchor consistency, CI và flags;
3. `criterion_predictions` (nếu có): chỉ xuất sau khi có mô hình riêng đã validate cho target domain như reading placement hoặc listening screening.

Không dùng R² của nghiên cứu Đức làm hệ số dự báo cho Preply. Mẫu nghiên cứu chỉ là học sinh 14–16 tuổi trong một hệ thống trung học Đức; chính tác giả nêu cần nghiên cứu thêm trên bối cảnh, nhóm test-taker và instrument khác.

## 6.6 Validation gates bổ sung cho thuật toán

1. **Construct gate:** mọi màn hình và report ghi written/receptive + unit + universe version.
2. **Guessing gate:** pseudoword items được chấm riêng; kiểm tra HR–FAR correlation; không penalty trước calibration.
3. **Criterion gate:** nếu tuyên bố placement/reading/listening, thu criterion scores tương ứng và fit mô hình trên một mẫu, đánh giá trên hold-out.
4. **Transport gate:** kiểm tra invariance/DIF theo L1, tuổi, proficiency, modality và domain; không chuyển các hệ số từ mẫu Đức sang toàn bộ người dùng.
5. **Coverage gate:** report MAE/RMSE, bias và CI coverage 80%/95%; kiểm tra theo decile và theo FAR band.
6. **Copy gate:** nếu chưa có evidence, dùng “ước lượng written receptive vocabulary breadth”, không dùng “trình độ tiếng Anh” hoặc “đọc hiểu dự kiến” như đồng nghĩa.

## 6.7 Gaps còn lại

- Chưa có response-level data của Preply hoặc item bank production để kiểm định HR/FAR, item bias và calibration.
- Chưa có evidence xác thực cho việc chuyển đổi trực tiếp giữa Preply headword score và word-family/lemma score; không dùng conversion factor cố định.
- Chưa có pilot đa dạng L1, tuổi, trình độ và mục đích học để ước lượng transportability.
- Chưa có criterion dataset của sản phẩm để tách vocabulary-size estimate khỏi reading/listening prediction.
- Chưa tìm được nguồn xác thực cho các hệ số guessing hoặc ngưỡng FAR dùng riêng cho Preply; các hệ số trong bảng trên chỉ là kết quả của nghiên cứu Harsch & Hartig ở mẫu và thiết kế đã nêu.
