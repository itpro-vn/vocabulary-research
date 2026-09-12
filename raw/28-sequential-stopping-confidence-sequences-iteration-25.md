# Iteration 25 — Sequential stopping, confidence sequences và phân bổ ngân sách

## Phạm vi và câu hỏi

Direction của iteration này là **sequential confidence-sequence stopping and budget allocation**: khi test chọn item và có thể dừng sau mỗi câu, làm sao giữ được độ tin cậy của khoảng ước lượng, tránh dừng vì “kết quả có vẻ ổn”, và phân bổ câu hỏi theo lợi ích thông tin trên mỗi đơn vị burden. Trọng tâm mới so với các iteration trước là tính hợp lệ dưới **optional stopping** và cơ chế dừng theo chi phí/precision; đây không phải việc bê một ngưỡng SE cố định vào mọi item bank.

## Bằng chứng đã kiểm tra

### 1. Confidence sequence cho dừng tùy ý

Howard, Ramdas, McAuliffe và Sekhon (Annals of Statistics, 2021) định nghĩa một confidence sequence (CS) là chuỗi khoảng tin cậy có bảo đảm đồng thời:

\[
P(\forall t \ge 1: \theta_t \in CI_t) \ge 1-\alpha.
\]

Bài báo nhấn mạnh ba thuộc tính liên quan trực tiếp tới vocabulary test online: (a) bảo đảm non-asymptotic/nonparametric trong các điều kiện đã nêu; (b) không cần ấn định trước sample size cuối; và (c) cho phép arbitrary stopping rules. Ví dụ sub-Gaussian được nêu trong bài có dạng bán kính:

\[
r_t = 1.7\sqrt{\frac{\log\log(2t)+0.72\log(10.4/\alpha)}{t}},
\]

cho trường hợp quan sát 1-sub-Gaussian. Công thức này là ví dụ bound của bài báo, không phải một margin phổ quát cho vocabulary count. Nó cho thấy chi phí của việc theo dõi liên tục: bán kính có thêm thành phần log-log so với trực giác fixed-n thông thường. Với response Bernoulli 0/1, bound bounded/sub-Bernoulli hoặc empirical-Bernstein phù hợp hơn có thể được dùng, nhưng phải kiểm tra điều kiện và coverage bằng mô phỏng trước khi đưa vào production.

**Ý nghĩa cho test:** nếu mỗi frequency band có luồng item được lấy ngẫu nhiên và response `known ∈ {0,1}`, có thể duy trì CS theo số item đã quan sát trong band. Các CS phải được tính đồng thời trong thời gian; không được tính CI fixed-n rồi theo dõi và dừng tại lúc độ rộng vừa đạt ngưỡng. Nếu chọn item thích nghi làm thay đổi inclusion probability, raw mean không còn đủ: hoặc giữ một reserve sample độc lập trong mỗi band, hoặc dùng estimator/inference martingale có trọng số xác suất chọn (IPW) đã được chứng minh.

### 2. SE stopping thất bại khi item bank lệch khỏi trait range

Morris và cộng sự nghiên cứu stopping rule cho CAT khi item bank có thông tin không đồng đều. Quy tắc phổ biến dừng khi posterior SE nhỏ hơn cutoff, ví dụ `SE < 0.3`, nhưng có thể hỏi rất nhiều câu ở vùng trait mà bank không có item đủ thông tin; thậm chí CAT có thể dùng hết bank mà không đạt cutoff. Bài báo đề nghị xem **bank information function** cùng phân bố trait của quần thể mục tiêu để xác định vùng attainable precision.

Đây là cảnh báo trực tiếp cho vocabulary-size testing: frequency tail, floor và ceiling là các vùng dễ thiếu item thông tin. Nếu còn cố hỏi cho tới khi một SE/CI cutoff chung đạt được, test sẽ tăng burden mà không nhất thiết tăng accuracy. Khi attainable precision không đủ, output phải có cờ `low_information` hoặc `censored`, không biến kết quả endpoint thành count chính xác.

### 3. Expected precision gain là tín hiệu dừng/phân bổ tốt hơn SE hiện tại

Cùng nghiên cứu mô tả **predicted standard error reduction (PSER)**: dừng khi các item còn lại được dự đoán không cải thiện precision đáng kể. Trong mô phỏng hai PROMIS banks, cấu hình `hypo=.015, hyper=.025` đạt RMSE tương đương hoặc tốt hơn các rule so sánh với ít item hơn; trong vùng trait không được bank nhắm tới, SE trung bình cần 23.23 câu, PROMIS 11.17 câu, còn PSER 6.16 câu. Các con số này chỉ là kết quả trên hai bank và simulation cụ thể.

Tác giả yêu cầu tuning theo item parameters, phân bố trait, mục tiêu precision/burden, exposure controls, enemy/content constraints và mô phỏng/response sequence thực tế. Vì vậy, vocabulary test nên dùng expected reduction của **tổng độ rộng khoảng ước lượng** hoặc expected information trên item ứng viên, nhưng không được chuyển các giá trị `.015/.025` thành tham số chung.

### 4. Precision budget nên phụ thuộc khoảng cách tới decision boundary

Morris và cộng sự cũng nêu nguyên tắc cho computerized classification: dùng precision chặt hơn gần decision point và có thể dùng precision lỏng hơn khi ước lượng cách xa điểm quyết định. Ví dụ `SE < .2` gần ngưỡng và `SE < .4` ở xa chỉ là minh họa phụ thuộc mục đích, không phải chuẩn vocabulary.

Suy ra một vocabulary product có thể có hai chế độ:

- **Ước lượng count:** tiếp tục cho tới khi total interval half-width dưới budget `δ` hoặc đạt hard maximum/attainable-precision rule.
- **Phân loại task/coverage:** tiếp tục nếu interval còn cắt qua một ngưỡng task; dừng sớm nếu toàn khoảng đã ở cùng một phía, đồng thời vẫn trả interval và không gọi đó là count chính xác hơn.

## Thuật toán đề xuất được cập nhật

### Estimand

Giữ estimand đã version hóa từ các iteration trước. Với frequency/domain strata `b = 1..B`, `H_b` là số lexical units trong universe của band (theo word-family/lemma policy đã công bố), và `p_b` là xác suất một unit trong band được người làm test biết theo định nghĩa scoring:

\[
V = \sum_{b=1}^{B} H_b p_b.
\]

Nếu dùng domain profile hoặc unequal-probability sampling, `H_b` và inclusion probability phải nằm trong manifest; không thay bằng dictionary size mơ hồ.

### CS theo band và tổng hợp

Với mỗi band, lưu `n_b`, `s_b`, `\hat p_b=s_b/n_b`, và khoảng đồng thời `CS_b(n_b)=[L_b,U_b]`. Chọn `α_b` sao cho `Σ_b α_b ≤ α`; union bound khi đó cho:

\[
CI_V = \left[\sum_b H_bL_b,\;\sum_b H_bU_b\right]
\]

với điều kiện estimator và CS của từng band đúng với sampling design. Độ rộng nửa khoảng cho sampling uncertainty là:

\[
W_{sampling}=\frac12\sum_b H_b(U_b-L_b).
\]

Cách viết này cố ý không gán một `±10%` chung cho mọi người. `W_sampling` chỉ là thành phần sampling/response-model uncertainty của estimand hiện tại; calibration error, lexical-unit ambiguity, domain transport và model misspecification phải báo riêng.

### Pseudocode

```text
initialize versioned lexical universe and strata b = 1..B
load H_b, alpha_b, minimum n_min[b], hard_max[b]
load calibrated item parameters, exposure/content constraints
initialize n_b = 0, s_b = 0, reserve_pool[b]

while true:
    update all band CS_b from responses observed so far
    estimate V_hat = sum_b H_b * p_hat_b
    interval = [sum_b H_b * L_b, sum_b H_b * U_b]
    sampling_halfwidth = 0.5 * sum_b H_b * (U_b - L_b)

    if every n_b >= n_min[b] and sampling_halfwidth <= delta:
        if task_decision_mode and interval crosses any task threshold:
            continue
        stop(status="precision_reached")

    if task_decision_mode and all relevant thresholds are outside interval:
        stop(status="decision_stable", retain_count_interval=true)

    if all bands meet hard_max or expected_gain_per_item is negligible:
        stop(status="attainable_precision_or_max", endpoint_or_low_info=true)

    choose next band/item by:
        expected reduction in total interval width per burden unit
        subject to n_b < hard_max[b], exposure caps, content balance,
        local-dependence spacing, and reserve-anchor requirements

    administer item and record response status, item id, band, inclusion probability,
    response time and form metadata
    update n_b and s_b only according to the pre-registered missingness/scoring rule
```

### Nếu dùng IRT/CAT thay vì design-based CS

Dùng posterior/SE hoặc test information để route item, nhưng phải thêm:

1. bank information plot theo vùng vocabulary ability và frequency tail;
2. minimum item count, hard maximum và endpoint status;
3. PSER-like expected information/SE reduction để tránh hỏi vô ích;
4. tuning bằng simulation với item exposure, content constraints và response model thật;
5. hold-out coverage/RMSE theo score range, đặc biệt floor/ceiling;
6. sensitivity report khi đổi 1PL/2PL/3PL hoặc guessing/slip assumptions.

SE của IRT không tự động là khoảng có coverage thực nghiệm, và CS của sample mean không tự động giải quyết model misspecification của IRT. Hai lớp này phải được validation riêng.

## So sánh với cách làm Preply

| Thành phần | Cách Preply đã được ghi nhận trong state/report trước | Đề xuất iteration 25 |
|---|---|---|
| Universe/sampling | Preply công khai mô tả dựa trên BNC, rebalance spoken/written và logarithmic/frequency-oriented sampling trong phần methodology đã kiểm tra ở các iteration trước. | Version hóa corpus, lexical-unit policy, `H_b`, routing/inclusion probability; không suy ra endpoint từ dictionary size. |
| Dừng test | Chưa có bằng chứng đã verify về confidence sequence, optional-stopping correction, expected information gain, attainable precision hay decision-proximity stopping của Preply. | CS time-uniform cho design-based stream; hoặc SE + PSER-like rule cho calibrated CAT; có min/max và low-information status. |
| Điểm endpoint | Chưa có item bank, routing log, response-level data hoặc tail-calibration data công khai để xác nhận coverage/uncertainty theo score range. | Không coi maximum quan sát là point estimate chính xác; route tail module/common anchors khi có, nếu không thì trả censored interval. |
| Uncertainty | Chưa tìm được nguồn xác thực cho một margin of error phổ quát riêng của Preply. | Báo `sampling_halfwidth`, calibration/model uncertainty và construct/transport gap riêng; không gộp thành một con số nếu chưa coverage-calibrated. |
| Mục tiêu task | Count người dùng nhìn thấy không nên tự động đổi thành CEFR/functional ability. | Có thể dùng interval để quyết định task threshold, nhưng chỉ báo task classification khi đã criterion-calibrated; count và coverage vẫn là output khác nhau. |

**Trạng thái xác minh Preply:** endpoint `https://preply.com/en/learn/english/test-your-vocab/how-it-works` đã trả HTTP 403 trong các lần fetch trực tiếp được ghi nhận; do đó chưa thể xác nhận item-level sequential behavior, exact stopping rule hoặc production uncertainty của Preply. Những phần nêu về methodology Preply trong bảng là các disclosure đã được lưu từ iteration trước, không phải suy đoán mới của iteration này.

## Assumptions và giới hạn

- CS band-level cần sampling design phù hợp; raw response mean không đủ nếu adaptive selection làm thay đổi inclusion probability.
- Formula minh họa từ Howard et al. là cho sub-Gaussian setting; triển khai Bernoulli/finite-population/without-replacement cần bound và coverage test riêng.
- `δ`, `n_min`, `hard_max`, `α_b`, task thresholds và expected-gain tolerance là policy/calibration parameters, chưa có giá trị phổ quát cho Preply.
- PSER evidence đến từ PROMIS health-outcome CAT, không phải vocabulary test; chỉ dùng làm nguyên tắc thiết kế và phải tune bằng vocabulary pilot.
- Dừng sớm làm giảm burden nhưng không thể tạo thông tin ở band mà item bank không bao phủ; low-information/censored status là kết quả hợp lệ hơn false precision.

## Validation plan bổ sung

1. **Simulation dưới sampling design:** tạo population lexical units có `H_b`, `p_b`, frequency/domain weights; mô phỏng fixed, random-stratified và adaptive routing. Kiểm tra coverage của `CI_V` tại mọi stopping time, bias và expected test length.
2. **Optional-stopping stress test:** cho phép dừng khi interval hẹp, khi estimate vượt task threshold, và khi người dùng liên tục “peek”; so sánh fixed-n Wald/Clopper–Pearson với CS. Fixed-n CI không được dùng làm baseline hợp lệ cho adaptive stop nếu coverage sụt.
3. **Bank-alignment simulation:** cố ý làm thiếu item ở floor/ceiling và tail; đo RMSE, interval coverage, item burden và tỷ lệ `attainable_precision_or_max`.
4. **Expected-gain tuning:** grid-search gain tolerance và budget trên pilot item parameters; chọn Pareto frontier precision–burden theo mục tiêu, không chọn bằng heuristic `.015/.025`.
5. **Operational pilot:** lưu item id, stratum, inclusion probability, response status, latency, form và route; khóa reserve anchors để kiểm tra alternate-form linking và repeated-attempt contamination.
6. **External validation:** common-person sample làm cả test đề xuất và criterion reading/listening/task measures; đánh giá coverage theo low/mid/high score, không chỉ RMSE trung bình.

## Gaps

- Chưa có source xác thực cho một công thức CS Bernoulli/finite-population cụ thể đã được calibration trên vocabulary item bank của Preply.
- Chưa có Preply response-level data để đo expected information gain, stopping behavior, item exposure, band coverage hoặc endpoint interval coverage.
- Chưa có calibration sample để chọn `δ`, `n_min`, `hard_max`, task decision thresholds và tolerance của PSER-like rule.
- Chưa có bằng chứng cho phép chuyển interval/SE của một vocabulary test thành CEFR hoặc count headword↔lemma/word-family phổ quát.
- Với các claim ngoài nguồn đã fetch, nếu không có dữ liệu mới thì ghi đúng: **chưa tìm được nguồn xác thực cho ý này**.

## Nguồn đã fetch/verify trong iteration 25

1. Howard, Ramdas, McAuliffe & Sekhon, *Time-uniform, nonparametric, nonasymptotic confidence sequences*, Annals of Statistics (2021): [Project Euclid](https://projecteuclid.org/journals/annals-of-statistics/volume-49/issue-2/Time-uniform-nonparametric-nonasymptotic-confidence-sequences/10.1214/20-AOS1991.full). HTTP 200; nội dung bài được lấy qua bản Markdown proxy sau khi endpoint HTML trực tiếp bị hạn chế.
2. Morris et al., *Stopping Rules for Computer Adaptive Testing When Item Banks Have Nonuniform Information*: [PMC article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7518406/). HTTP 200; nội dung bài được fetch và đối chiếu qua bản Markdown proxy do challenge của endpoint trực tiếp.
3. Bản landing/publisher dùng để cross-check metadata của bài CAT: [Taylor & Francis DOI page](https://www.tandfonline.com/doi/full/10.1080/15305058.2019.1635604). Endpoint trả 403 nên không dùng nội dung page này làm bằng chứng; bằng chứng CAT trong file này lấy từ PMC đã fetch được.
