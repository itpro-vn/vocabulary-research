# 7. Iteration 4 — sampling precision, test length và item independence

## 7.1 Direction và phạm vi

Iteration 4 chọn direction **sampling-error and precision design**: định lượng ảnh hưởng của số item trong mỗi frequency band đến tính đại diện và độ bất định; kiểm tra yêu cầu item independence; chuyển bằng chứng thành chính sách phân bổ mẫu và stopping rule. Direction này không lặp lại các vòng trước về định nghĩa word-family/headword, IRT/CAT calibration, hay criterion/predictive validity.

## 7.2 Bằng chứng đã kiểm tra

### McLean et al. (2021): cỡ mẫu trong một frequency band

Nguồn PDF học thuật được fetch trực tiếp và trả HTTP 200:

- [McLean et al., “The internal consistency and accuracy of automatically scored written receptive meaning-recall data: a preliminary study”](https://files.eric.ed.gov/fulltext/EJ1458804.pdf)
- DOI được bài nêu: [10.7820/vli.v10.2.mclean](https://doi.org/10.7820/vli.v10.2.mclean)

Các điểm trích xuất được từ phần “1.5 Sample Size” và chú thích hình:

1. Các levels tests trong thực tế thường dùng **5–30 item** để đại diện cho một band 1.000 từ (hoặc band 560 từ). Định nghĩa reliability trong ngữ cảnh này gắn với việc chọn lại mẫu mà không làm ước lượng của cùng một learner thay đổi đáng kể.
2. Bài mô tả các mẫu bootstrap cỡ 5, 10, 20, 50 và 100 từ một band 1.000 từ, với learner có true score 750/1.000; Hình 11 tổng hợp thêm cỡ mẫu lớn hơn.
3. Theo phần diễn giải của bài, ngay cả mẫu **100 hoặc 200 item** đôi khi vẫn cho ước lượng không chính xác; tuy nhiên lợi ích giảm sai số khi thêm item giảm đáng kể sau khoảng **40 item**.
4. Kết luận áp dụng cho thiết kế: số item trong band là một thành phần của representativeness, accuracy, reliability và construct validity. Vì vậy điểm band có ít item không nên được đọc như mastery chính xác, và CI phải bao gồm sampling uncertainty.

Đây là bằng chứng về độ nhạy với cỡ mẫu, không phải bằng chứng rằng “40 item luôn đủ”. Ngưỡng 40 phải được kiểm định lại trên item bank, phân bố ability và mục tiêu độ rộng CI của sản phẩm.

### McLean & Kramer (2015): item independence và format

Nguồn PDF học thuật được fetch trực tiếp và trả HTTP 200:

- [McLean & Kramer, “The Creation of a New Vocabulary Levels Test”](https://teval.jalt.org/sites/default/files/19-02-1_McLean_Kramer.pdf)

Bài nêu rằng format VLT cũ dạng item-cluster/matching có thể tạo **local item dependence**: sau mỗi câu, số lựa chọn còn lại giảm, khiến câu sau phụ thuộc vào câu trước. Đây là vấn đề đối với giả định item independence của cả classical test analysis và IRT. NVLT chuyển sang multiple-choice item độc lập vì format này dễ phân tích item, dễ chấm và dễ triển khai trực tuyến.

Hệ quả: baseline estimator có thể dùng item độc lập; nếu sản phẩm dùng cụm phụ thuộc, variance/CI không được tính như các Bernoulli độc lập. Khi đó phải bootstrap theo cụm hoặc ước lượng design effect; nếu không, CI sẽ quá hẹp.

## 7.3 Đo kiểm mô phỏng tái lập

Để sanity-check hướng dẫn trên, đã chạy `/tmp/vocab_sampling_sim.py` bằng `uv run --with numpy python3`. Thiết kế: một population band có `N=1.000`, đúng 750 đơn vị “known” và 250 “unknown”; với mỗi `n`, lấy mẫu không hoàn lại 100.000 lần và ước lượng `N * p_hat`. Đây là mô phỏng thiết kế do Deli thực hiện, **không phải dữ liệu người làm test**.

| n item trong band | Mean absolute error | RMSE | 95th percentile của absolute error |
|---:|---:|---:|---:|
| 5 | 158.22 | 193.46 | 350 |
| 10 | 112.20 | 136.35 | 250 |
| 20 | 75.08 | 95.99 | 200 |
| 30 | 62.75 | 77.81 | 150 |
| 40 | 53.22 | 67.28 | 125 |
| 50 | 48.10 | 59.94 | 110 |
| 100 | 32.65 | 41.07 | 80 |
| 200 | 21.77 | 27.35 | 55 |

Kết quả tái hiện trực giác của nguồn: 5–10 item có thể tạo sai lệch hàng trăm đơn vị khi mở rộng từ band 1.000; tăng lên khoảng 40 item cải thiện rõ, nhưng không tạo ra một guarantee phổ quát. Mô phỏng không thay thế calibration bằng response data thực tế.

## 7.4 Cập nhật thuật toán

Giữ estimator phân tầng hiện tại làm baseline:

```text
for each band b:
    draw n_b unique, independently authored items
    p_hat_b = mean(correct responses in b)
V_hat = sum(N_b * p_hat_b)
```

Bổ sung các ràng buộc:

- `n_b` phải được lưu trong result và được chọn theo target precision, không ẩn sau một hệ số nhân điểm.
- Band có đóng góp `N_b² * Var(p_hat_b)` lớn hoặc nằm quanh một decision threshold được ưu tiên thêm item.
- Dùng finite-population variance khi sampling không hoàn lại; nếu item responses tương quan, dùng cluster/bootstrap theo đơn vị phụ thuộc hoặc điều chỉnh design effect.
- Khi `n_b` nhỏ, dùng Wilson hoặc beta-binomial interval thay vì Wald interval; khi p gần 0/1 gắn cờ floor/ceiling.
- Stopping rule: dừng khi CI sau transform đạt ngưỡng sản phẩm, các band quanh ngưỡng quyết định đủ precision, hoặc đạt max items. Nếu chưa có calibration, không bật CAT để thay thế kiểm soát sampling error.

Pseudocode cập nhật:

```text
function precision_aware_estimate(session, universe, bands, bank):
    responses = sample_anchors_and_initial_items(bands, bank)
    while true:
        estimates = estimate_by_band(responses, design="without_replacement")
        ci = band_bootstrap_or_finite_population_ci(estimates, responses)
        if stopping_rule(ci, decision_bands, max_items):
            break
        b = argmax(unresolved_variance_contribution(ci))
        if no_eligible_item(bank[b]):
            break
        responses.append(sample_unique_item(bank[b]))
    return aggregate_bands(estimates), ci, diagnostics(responses)
```

## 7.5 Product/report implications

1. Báo `estimate`, `unit`, `universe_version`, `n_b`, `p_hat_b`, `CI_sampling`, `sensitivity_range` và quality flags.
2. Không suy ra rằng ước lượng headword của Preply có thể đổi trực tiếp sang word-family count.
3. Không dùng ±10% của Preply như CI mặc định cho estimator phân tầng mới. Cách midpoint/log-rank của Preply vẫn có thể là UX ngắn, nhưng phải được đánh giá bằng repeated forms, hold-out items và coverage calibration.
4. Với item cluster, phải dùng phương pháp variance phù hợp; format multiple-choice độc lập là lựa chọn an toàn hơn cho baseline.

## 7.6 Gaps còn lại

- Chưa có response-level data hoặc item bank production của Preply, nên chưa đo được sampling distribution, design effect, hoặc coverage của margin Preply trên quần thể thực.
- Chưa có pilot đủ rộng để chọn `n_b` tối ưu theo L1/proficiency, DIF, item exposure và latency.
- Chưa có gold/criterion audit cho từng band; mô phỏng chỉ mô tả sampling error, chưa bao gồm guessing, item misfit, cognate effects hay construct mismatch.
- Chưa tìm được nguồn xác thực cho một quy tắc cỡ mẫu riêng của Preply; vì vậy không hard-code quy tắc đó vào thuật toán đề xuất.
