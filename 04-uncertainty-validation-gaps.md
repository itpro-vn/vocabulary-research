# 4. Độ không chắc chắn, assumptions và kế hoạch validation

## 4.1 Assumptions phải công bố

1. **Universe**: dictionary/headword hay word-family; list và version cụ thể.
2. **Construct**: receptive written recognition, không đồng nghĩa productive use, speaking fluency hay full sense knowledge.
3. **Sampling**: mỗi item đại diện cho các đơn vị trong band của nó; item pool không bị selection bias.
4. **Local independence**: response của các item gần độc lập sau khi conditioning theo band/ability; nếu không, analytic SE sẽ quá lạc quan.
5. **Monotonicity**: xác suất biết nhìn chung giảm theo frequency rank; cognate, chuyên môn và sở thích có thể tạo ngoại lệ.
6. **Administration**: test-taker nghiêm túc, không tra cứu; latency/skip có quy tắc rõ.
7. **Missingness**: người bỏ câu không khác hệ thống với người trả lời, hoặc missing được xử lý riêng.

## 4.2 Uncertainty

Báo cáo ít nhất hai thành phần:

- **Sampling uncertainty**: công thức stratified variance hoặc bootstrap theo band.
- **Model/construct uncertainty**: chênh lệch giữa word family/headword, receptive vs productive, dictionary/corpus versions, và sensitivity khi đổi exclusion rules.

Nên trả về `estimate`, `CI_sampling`, `sensitivity_range`, và nhãn chất lượng. Nếu band có tỷ lệ đúng gần 0/1 hoặc quá ít item, dùng Wilson/beta-binomial interval và gắn `floor`/`ceiling` thay vì CI Wald đơn giản.

Preply mô tả margin ±10.33% từ `SD ≈ 0.25V`, `n ≈ 22.5`, `SE=.0527`, `1.96×SE`; đây là một model assumption của trang, không nên tái sử dụng cho estimator phân tầng mới nếu chưa chứng minh cùng sampling distribution.

## 4.3 Validation plan

### A. Content và item quality

- Hai chuyên gia độc lập review POS, sense, stem simplicity, distractor plausibility.
- Nonsense-word pilot để phát hiện đáp án lộ từ distractor.
- Kiểm tra tần suất stem/distractors không làm target thành bài đọc khó.
- Tái tạo frequency bands từ corpus snapshot; hash manifest.

### B. Pilot psychometrics

- Pilot đa dạng proficiency và L1; lưu response-level data.
- Tính item difficulty, discrimination, distractor selection, latency.
- Fit Rasch/2PL sau khi có đủ dữ liệu; kiểm tra unidimensionality, person/item separation và DIF theo L1/proficiency.
- Giữ anchor items cho parallel forms; loại hoặc sửa item có cueing/DIF nghiêm trọng.

### C. Accuracy và calibration

- Tạo gold/criterion subset bằng interview receptive test hoặc extensive known-word audit trên mẫu nhỏ; không coi một bài test khác là gold tuyệt đối.
- So sánh estimate với full/large-form test và hold-out items.
- Report bias, MAE/RMSE, coverage của CI 80/95%, calibration curve theo decile.
- Test-retest sau 1–2 tuần với parallel form; kiểm tra rank-order stability.

### D. Decision validity

- Liên hệ với reading coverage/reading comprehension trên text phù hợp, nhưng báo rõ đây là criterion phụ thuộc domain.
- Kiểm tra các ngưỡng hành động (ví dụ chuyển tài liệu học) bằng false-positive/false-negative cost.

## 4.4 Gaps hiện tại

- Chưa có item bank production hoặc response data của Preply; direct Preply fetch bị 403 và chỉ có methodology page qua proxy.
- Chưa xác minh độc lập sample size/dataset dùng để suy ra ±10% của Preply.
- Chưa có pilot để ước lượng n_b tối ưu, DIF, guessing/cueing và non-monotonicity.
- Chưa có nguồn xác thực cho việc map giữa Preply headword estimates và VST word-family estimates; không được dùng một conversion factor cố định.

## 4.5 Bổ sung từ iteration 2: uncertainty trong CAT và repeat forms

IRT/CAT tạo ra uncertainty trên thang ability (ví dụ `SE_theta` từ information), sau đó phải truyền qua hàm calibration sang vocabulary scale. Với hàm logistic đơn điệu `g(theta)`, một xấp xỉ delta-method là `SE_V ≈ |g'(theta)| SE_theta`; trong sản phẩm nên kiểm tra thêm bằng bootstrap/posterior draws vì uncertainty calibration (`a,b,c`) và sai số construct không nằm trong `SE_theta` thuần túy. Khoảng kết quả nên tách:

1. `CI_sampling_or_response`: biến thiên do responses/items được chọn;
2. `CI_model`: lựa chọn Rasch/2PL, guessing model, calibration và item-fit;
3. `sensitivity_range`: thay đổi universe, lemma/headword/word-family và exclusion rules.

Bằng chứng Akase cho thấy alternate forms phải có common/linking items và equating trên logit chung; nếu không, chênh lệch điểm theo thời gian có thể là practice effect hoặc form difficulty. Bằng chứng PVST cho thấy pseudowords/multiple-choice có thể tạo quality signal; nên dùng chúng để gắn cờ hoặc loại response khỏi hiệu chỉnh item, không tự động biến thành penalty cá nhân.

### Validation gates mới cho CAT

- Calibration/hold-out: fit item parameters trên một mẫu, đánh giá item exposure, prediction và CI coverage trên mẫu khác.
- Targeting: Wright map hoặc biểu đồ item difficulty so với ability; kiểm tra vùng advanced không bị thiếu item.
- Model fit: infit/outfit, unidimensionality, local dependence và DIF theo L1/proficiency; ngưỡng `1.3`/`z>2` của PVST chỉ là tham chiếu pilot, không phải luật chung.
- Stopping simulation: mô phỏng nhiều theta và pattern response để chọn `target_se`, max items và quota anchors; report bias/MAE/RMSE và coverage 80/95%.
- Repeat forms: giữ anchor exposure thấp nhưng đủ lớn để equate; test-retest với parallel form sau 1–2 tuần và tách learning/practice effect.

## 4.6 Bổ sung từ iteration 4: sampling precision và dependence

McLean et al. (2021) cho thấy số item đại diện cho mỗi band là nguồn sai số thực chất: levels tests thường dùng 5–30 item/band, và resampling cùng một learner có thể cho các ước lượng khác nhau. Phân tích được dẫn lại trong bài cho thấy mẫu 100/200 item đôi khi vẫn không chính xác; lợi ích biên của việc thêm item giảm đáng kể sau khoảng 40 item. Do đó `n_b=40` chỉ là điểm khởi đầu để mô phỏng/validation, không phải guarantee.

Baseline phải tính hai loại uncertainty:

1. **Sampling uncertainty theo band**: dùng finite-population variance khi lấy mẫu không hoàn lại hoặc bootstrap item trong band.
2. **Dependence/model uncertainty**: nếu item là một cụm matching phụ thuộc lẫn nhau, bootstrap theo cụm hoặc dùng design effect; không áp dụng công thức độc lập một cách máy móc.

Các gate bổ sung:

- Mô phỏng repeated sampling trên từng band với các `n_b` ứng viên (5, 10, 20, 30, 40, 50, 100...) và các mức mastery; chọn allocation theo mục tiêu MAE/CI coverage, không theo con số 40 cố định.
- Trong pilot, kiểm tra local item dependence, item exposure và response correlation; so sánh CI analytic với bootstrap/cluster-bootstrap.
- Báo riêng `n_b`, `p_hat_b`, `SE_b`, CI phương pháp nào, và cờ floor/ceiling. Không gọi một band có 5 item là mastery chính xác.
- Kiểm định stopping bằng hold-out/repeated forms: coverage CI 80/95%, bias, MAE/RMSE và độ ổn định rank-order.

Mô phỏng sanity-check của iteration 4 (N=1.000, true p=.75, 100.000 lần lấy mẫu không hoàn lại) cho MAE 158.22 ở n=5, 112.20 ở n=10, 75.08 ở n=20, 62.75 ở n=30 và 53.22 ở n=40. Đây là số đo do Deli chạy, không phải dữ liệu người dùng hay bằng chứng calibration cho Preply.
