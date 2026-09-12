# 1. Tóm tắt điều hành

> **Actual-data update:** The supplied LazzyBee snapshot is now available and audited: 3,885 source records; 99.0476% have WordNet lexical candidates, but semantic review and human calibration remain pending. This supersedes any generic assumption that no owner data is available, not the unresolved Preply-data or validation gaps. See [snapshot audit](../docs/data/LAZZYBEE_SNAPSHOT_AUDIT.md). Raw records are not published.

## Kết luận hiện tại

Một bài test vocabulary-size nên công bố trước **đơn vị đo** và **quần thể từ**. Hai cách đang được đối chiếu không đo cùng estimand:

- VST của Nation/Beglar và các phiên bản mô tả bởi Wellington lấy **word families** theo các dải tần suất 1.000 word families; điểm tổng được mở rộng tuyến tính (140 item × 100 hoặc 100 item × 200).
- Preply mô tả một vũ trụ khoảng 45.000 **dictionary main entries/headwords**, gộp derived-form counts theo headword và dùng một thiết kế hai giai đoạn có midpoint trên thứ hạng tần suất.

Vì vậy không nên gọi hai điểm số là cùng một “số từ biết”. Sản phẩm nên trả về tối thiểu: `estimate`, `unit`, `universe_definition`, `test_mode` (receptive recognition/productive), và khoảng bất định.

## Đề xuất v1

1. Chốt một vocabulary universe có phiên bản: dictionary headwords **hoặc** word families, không trộn hai loại.
2. Xây frequency bands từ corpus nói + viết; lưu `band_id`, `N_b`, version corpus/dictionary và quy tắc loại từ.
3. Lấy mẫu ngẫu nhiên phân tầng theo band. Mỗi item có target, POS, sense, distractors và metadata về nguồn band.
4. Ưu tiên 4-choice receptive recognition nếu mục tiêu là đọc; kiểm tra distractor bias bằng pilot và Rasch/IRT.
5. Ước lượng tỷ lệ biết trong mỗi band rồi cộng theo quy mô band; báo cáo khoảng tin cậy theo phương sai mẫu phân tầng.
6. Nếu cần test ngắn, có thể dùng routing hai giai đoạn như Preply, nhưng phải giữ một tập anchor ngẫu nhiên để kiểm tra calibration và không được trình bày ±10% như sự thật chung nếu chưa có validation độc lập.

## Công thức lõi

Với band `b` có `N_b` đơn vị từ, mẫu `n_b`, câu trả lời nhị phân `x_bj ∈ {0,1}`:

```text
p_hat_b = (1 / n_b) * Σ_j x_bj
V_hat = Σ_b N_b * p_hat_b
Var(V_hat) ≈ Σ_b N_b² * (1 - n_b/N_b) * s_b² / n_b
CI_95 = V_hat ± 1.96 * sqrt(Var(V_hat))
```

` s_b² ` là phương sai mẫu của item scores trong band. Nếu mỗi band có rất ít item, không được diễn giải `p_hat_b` như mastery chính xác; chỉ dùng tổng có trọng số hoặc tăng cỡ mẫu ở vùng quyết định.

## Cảnh báo quan trọng

- VST specification nói rõ mỗi band chỉ có ít item và không đo đáng tin mastery từng band; tổng score mới là mục tiêu.
- VST không sửa guessing; tài liệu giải thích mỗi item đại diện cho 100/200 đơn vị nên correction có thể làm méo estimand, đồng thời thừa nhận score hơi generous.
- Preply tự báo ±10% dựa trên giả định phân phối và sample size cụ thể; cần kiểm định bằng repeated forms, hold-out items và benchmark interview/reading coverage.

## Cập nhật iteration 2: IRT/CAT

Bằng chứng mới từ PVST (2025) cho thấy CAT có thể chọn item gần ability hiện tại, ước lượng ability trên logit, rồi chuyển sang số từ bằng hàm logistic đã calibration; bài pilot dùng 30 stimuli trong khoảng 2 phút. Đây là hướng phù hợp cho test ngắn nhưng chỉ sau khi item difficulty/discrimination được calibration trên response data. Pseudowords và multiple-choice nên cung cấp quality/attention signal riêng; không tự động trừ điểm vocabulary.

Bằng chứng Akase (2022) cho thấy các parallel forms cần common/linking items và Rasch equating để tách growth khỏi practice effect và khác biệt độ khó form. Frequency là điểm khởi tạo tốt cho item universe nhưng không đủ làm difficulty parameter vì có overlap giữa các frequency bands.

Khuyến nghị hiện tại: trước pilot dùng stratified estimator; sau pilot mới bật CAT/IRT với stopping theo `SE_theta`/độ rộng CI, transform uncertainty sang vocabulary scale và báo thêm model/construct sensitivity. Xem chi tiết tại [05-irt-cat-iteration-2.md](05-irt-cat-iteration-2.md).

## Cập nhật iteration 4: sampling precision

Bằng chứng từ McLean et al. (2021) cho thấy các levels tests thường chỉ lấy 5–30 item để đại diện một band 1.000 từ; resampling có thể làm ước lượng thay đổi đáng kể, và ngay cả 100/200 item đôi khi vẫn sai, dù lợi ích tăng thêm giảm rõ sau khoảng 40 item. Đây không phải ngưỡng đủ phổ quát. Baseline vì vậy phải lưu `n_b` theo band, dùng finite-population variance hoặc bootstrap phù hợp, và dừng theo độ rộng CI chứ không theo hệ số nhân điểm.

Một mô phỏng tái lập của Deli trên band 1.000 đơn vị với tỷ lệ biết 75% cho mean absolute error khoảng 158 từ ở n=5, 112 ở n=10, 75 ở n=20 và 53 ở n=40; đây là sanity check, không phải calibration sản phẩm. Bằng chứng NVLT cũng cảnh báo local item dependence trong format matching theo cụm; item độc lập hoặc bootstrap theo cụm là điều kiện để CI không bị lạc quan.

Chi tiết và bảng mô phỏng: [07-sampling-precision-iteration-4.md](07-sampling-precision-iteration-4.md).

## Cập nhật iteration 18: breadth, depth và strength

Bằng chứng Read–Dang trên 222 sinh viên EAP cho thấy breadth và depth liên quan nhưng không đồng nhất (`r=.64`, khoảng 41% phương sai chung). Ba facet depth có difficulty/reliability khác nhau: synonyms, word parts và collocations có alpha lần lượt `.94/.90/.75`; không được cộng raw score hoặc đổi depth thành word count. `Not Sure` có độ phân tán cá nhân lớn nên phải giữ là response-process signal và chạy sensitivity, không áp penalty cố định. Teng cho thấy depth có thể bổ sung tín hiệu cho listening trong một mẫu cụ thể (`r=.91`, `R²` tăng 2.6%), nhưng không phải hàm chuyển phổ quát.

Khuyến nghị cập nhật: `breadth_estimate` vẫn là output đếm chính có unit/universe/CI; `depth_profile` là vector facet (semantic associate, collocation, word parts) với error và trạng thái `diagnostic_only` cho tới khi có calibration. Mastery cut score phải theo intended use và CI; không bê ngưỡng 29/30 hay các hệ số từ nghiên cứu khác vào Preply. Chi tiết, pseudocode và validation plan: [21-breadth-depth-strength-calibration-iteration-18.md](21-breadth-depth-strength-calibration-iteration-18.md).

## Cập nhật iteration 51: audit implementation tham chiếu

Audit HTML/JavaScript live của Lextutor VST cho thấy một form cố định gồm 14 band × 10 item = 140 item, bốn lựa chọn mỗi item. Hàm chấm tính `vocab_size = total_correct × 100`, tối đa 14.000; phần coverage weights được tính riêng nhưng không dùng cho điểm hiển thị. Answer key và scoring nằm trong client JavaScript, nên đây là diagnostic practice reference chứ không phải thiết kế đủ chống gian lận/retest.

Read (2007) xác nhận MCQ VST và Yes/No là hai response process khác nhau; không chuyển correction coefficient giữa chúng nếu chưa equate. Preply hiện trả HTTP 403 ở các endpoint đã thử trong callback, nên chưa có bằng chứng mới xác thực cho item pool/scoring/security hiện tại của Preply. Chi tiết: [54-black-box-reference-vst-preply-audit-iteration-51.md](54-black-box-reference-vst-preply-audit-iteration-51.md).
