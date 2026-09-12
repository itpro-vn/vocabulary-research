# Iteration 70 — Answer-key uncertainty, ambiguity và noisy-label scoring

## Phạm vi

Iteration này tách **lỗi của item/key** khỏi năng lực từ vựng của người làm. Mục tiêu không phải đưa ra một correction coefficient cố định, mà thiết kế một cổng trước calibration và một lớp uncertainty cho `K_hat`.

## Bằng chứng đã verify

| Nguồn | Bằng chứng liên quan | Giới hạn chuyển giao |
|---|---|---|
| [Srisomsak et al., BMC Medical Education](https://pmc.ncbi.nlm.nih.gov/articles/PMC12805726/) | 236 kỳ thi/14.238 MCQ có 81 item (0,6%) cần sửa; nguyên nhân multiple-answers 46,9%, wrong-answer 40,7%, all-choices 7,4%, item-removal 4,9%. Trong 77 item có đủ p/rpb, 11 (14,3%) không bị bắt bởi ngưỡng p<0,25 hoặc rpb<0. Review thêm khi key không phải lựa chọn được chọn nhiều nhất hoặc nhiều option có p gần nhau. | Bối cảnh y khoa, không phải vocabulary; dùng như bằng chứng về quy trình phát hiện lỗi key, không chuyển tỷ lệ 0,6% thành tỷ lệ lỗi của Preply. |
| [Pais et al., BMC Research Notes](https://pmc.ncbi.nlm.nih.gov/articles/PMC4982015/) | 800 MCQ được 4 rater độc lập, mù với performance data. Fleiss κ=0,89 cho content area nhưng κ=0,30 cho taxonomy của item-writing flaw; 55,8% item có ít nhất một flaw. Stem/choice flaws làm giảm difficulty và discrimination. | Taxonomy flaw không đồng nhất với “đáp án đúng”; κ thấp là bằng chứng uncertainty trong review, không phải ngưỡng production. |
| [Rush, Rankin & White, BMC Medical Education](https://pmc.ncbi.nlm.nih.gov/articles/PMC5041405/) | Trong 1.925 item, 20 câu có >1 đáp án đúng và 5 câu không có đáp án đúng bị loại trước phân tích. 37,3% item có hơn một flaw; implausible distractor đi kèm 95,0% đúng và discrimination 0,09, so với 80,1% và 0,20 khi không có flaw. | Mẫu veterinary/medical; dùng để biện minh quarantine và không học item parameters từ key chưa adjudicate. |
| [Li et al., ACL Anthology N19-1295](https://aclanthology.org/N19-1295/) | Mô hình xác suất/EM suy ra latent true label và reliability theo từng instance của annotator, hỗ trợ binary và multi-class. Được đánh giá trên synthetic và NLP text classification/entailment. | Không phải vocabulary validation; chỉ là pattern phương pháp để biểu diễn bất đồng reviewer bằng posterior key. |

Tất cả bốn URL trên trả HTTP 200 khi fetch với browser UA trong callback. Preply methodology proxy cũng trả HTTP 200; endpoint trực tiếp `how-it-works` trả HTTP 403.

## Quyết định thuật toán

### 1. Manifest và trạng thái item

Mỗi item vocabulary phải version hóa:

```text
item_id, bank_version, target_unit, frequency_band, stem, options
initial_key, acceptable_set, reviewer_ids, reviewer_labels
review_protocol, adjudication_status, key_posterior, quarantine_reason
```

`acceptable_set` cho phép nhiều đáp án được chấp nhận chỉ khi expert protocol xác nhận chúng cùng biểu đạt meaning target. `no-valid`, `multi-valid-unresolved`, `key-disputed` và lỗi stem/context đi vào `quarantine`; không dùng để ước lượng item difficulty hay `K_hat` chính thức.

### 2. Gate trước calibration

1. Hai hoặc nhiều reviewer nội dung độc lập review item **mù** với response statistics.
2. Lưu nhãn, lý do, phiên bản rubric và κ/α agreement; không chỉ lưu kết luận cuối.
3. Nếu có disagreement: adjudicator có chuyên môn quyết định `acceptable_set`, hoặc đặt item `quarantine`; không majority-vote mù quáng khi reviewer cùng chịu một ambiguity.
4. Chỉ sau khi key ổn định mới mở response data để kiểm tra p, rpb, distractor và IRT fit. Nếu key được sửa, tạo score version mới và re-score; không trộn pre-key và post-key statistics.
5. Item đã biết lỗi nhưng muốn giữ để theo dõi chỉ được đưa vào `sensitivity-only`, không vào operational bank.

### 3. Key posterior và score

Với option `c` của item `i`, lưu:

```text
g_i,c = P(key_i accepts c | reviewer labels, rubric, content evidence)
```

Nếu learner chọn `r_i`, response correctness kỳ vọng là `z_i = g_i,r_i`. Với band `h`, weights `w_i` đã bao gồm inclusion/route/nonresponse calibration của estimator hiện hành:

```text
p_hat_h = sum(i in h) w_i * z_i / sum(i in h) w_i
K_hat   = sum(h) M_h * p_hat_h
```

`K_hat` ở đây vẫn là breadth estimand đã khai báo (headword, lemma hoặc word family); key posterior không tự thay đổi lexical unit.

Key uncertainty có thể tính bằng Monte Carlo: mỗi draw lấy một acceptable key từ `g_i`, chạy lại toàn bộ weighted estimator, rồi lấy quantile của `K_hat`. Khi các key độc lập gần đúng, một thành phần xấp xỉ trong band là:

```text
V_key,h ≈ sum(i in h) (w_i / W_h)^2 * z_i * (1 - z_i)
```

Trong triển khai thật, ưu tiên replicate theo toàn bộ item-key posterior và cộng/ghép với sampling, route, model và form uncertainty; không cộng cơ học các thành phần nếu chúng có covariance. Báo riêng `K_raw` (key ban đầu), `K_adjudicated`, `K_key_sensitivity`, `CI_sampling_model` và `CI_total`.

### Pseudocode

```text
for item in item_bank:
    reviews = blinded_review(item, rubric_version)
    item.key_posterior, item.status = adjudicate(reviews, content_evidence)
    if item.status in {no_valid, unresolved_multi_valid, disputed}:
        item.status = quarantine

calibration_items = [i for i in item_bank if i.status == approved]
fit_item_parameters(calibration_items, response_data)

for respondent:
    collect response r_i and design metadata w_i for approved items
    for each band h:
        z_i = P(key_i accepts r_i | approved key evidence)
        p_h = weighted_mean(z_i, w_i)
    K_adjudicated = sum_h(M_h * p_h)

for b in 1..B:
    draw approved keys from each item posterior
    recompute K_b using the same route/design weights
CI_key = quantile(K_b, [alpha/2, 1-alpha/2])
CI_total = combine_or_jointly_bootstrap(CI_key, sampling, model, form)
release only if key gate, item-fit, coverage and interval gates pass
```

## So sánh với Preply

| Thành phần | Preply đã công khai qua methodology proxy | Thiết kế đề xuất |
|---|---|---|
| Universe/đơn vị | Dictionary hơn 45.000 entries, derived forms aggregate vào dictionary headwords | Giữ lexical-unit manifest và không gọi headword là word-family |
| Sampling/score | Khoảng 40 item broad phase + khoảng 120 item narrow, logarithmic ranks, midpoint và vendor margin khoảng ±10,33% | Giữ route/inclusion metadata; thêm key gate, posterior và key-sensitivity interval |
| Key review | Trang đã fetch không nêu item key version, acceptable alternatives, reviewer adjudication hoặc quarantine | Bắt buộc reviewer mù, adjudication status, immutable score version và quarantine |
| Error claim | Margin vendor là sampling-model claim trong nguồn đã fetch | Không coi margin đó bao gồm key ambiguity; chỉ release total interval sau validation |
| Sản phẩm | Có thể hiển thị nhanh một midpoint estimate | Hiển thị estimate kèm `reliability_status`, `key_status`, `K_raw/K_adjudicated` và cờ sensitivity |

## Validation plan và gaps

- Tạo item pilot gồm key chắc chắn, cố ý ambiguous, multi-valid và no-valid; đánh giá blinded-review agreement, adjudication stability và false-quarantine rate.
- Split reviewer/content evidence thành calibration và hold-out; kiểm tra posterior key calibration (reliability diagram/Brier hoặc log score) trên tập có gold resolution độc lập.
- So sánh ba estimator trên cùng response data: hard initial key, hard adjudicated key và posterior-key Monte Carlo; đo bias/RMSE/coverage theo frequency band, proficiency và L1.
- Chạy simulation với tỷ lệ key error, correlated reviewer error và item clustering; xác nhận `CI_total` bao phủ khi key uncertainty tương quan với difficulty/routing.
- Re-score response-level data sau key correction và kiểm tra invariance, form equating, item exposure và domain coverage; không dùng tỷ lệ lỗi của nguồn y khoa làm prior mặc định cho Preply.
- Gap product-specific: chưa có item bank, reviewer logs, response-level data hoặc calibration sample của Preply. Chưa tìm được nguồn xác thực cho tỷ lệ miskey/ambiguity, cơ chế xử lý multiple-valid, key versioning, quarantine hay việc margin ±10,33% có bao gồm key uncertainty hay không.
