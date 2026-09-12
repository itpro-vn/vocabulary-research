# Iteration 49 — Nonparametric IRT/Mokken và QA item bank

## Phạm vi

Iteration này kiểm tra một lớp kiểm định model-free trước khi fit Rasch/2PL hoặc mô hình response khác cho vocabulary-size test. Direction mới tập trung vào Mokken nonparametric IRT: đơn chiều, monotonicity, local independence, scalability và invariant item ordering (IIO). Mục tiêu không phải thay IRT bằng Mokken, mà dùng các kiểm định này để phát hiện item bank không phù hợp trước khi ước lượng `K_hat`.

## Nguồn đã fetch và kiểm tra

Các URL dưới đây đã được gọi với browser user-agent và trả HTTP 200 trong iteration:

1. Stochl, Jones & Croudace (2012), *Mokken scale analysis of mental health and well-being questionnaire item responses: a non-parametric IRT method in empirical research for applied health researchers*, toàn văn XML qua Europe PMC: <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3464599/fullTextXML>.
2. Myszkowski (2020), *A Mokken Scale Analysis of the Last Series of the Standard Progressive Matrices*, toàn văn XML qua Europe PMC: <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7712996/fullTextXML>.
3. van der Ark, R package `mokken`, reference manual PDF: <https://cran.r-project.org/web/packages/mokken/mokken.pdf>.
4. Straat, van der Ark & Sijtsma (2014), abstract và metadata tại Tilburg University Research Portal: <https://research.tilburguniversity.edu/en/publications/minimum-sample-size-requirements-for-mokken-scale-analysis>.

Hai nghiên cứu Mokken được dùng như bằng chứng phương pháp đo, không phải bằng chứng rằng vocabulary items cụ thể đã đạt các ngưỡng này. Chưa có item bank hoặc response-level data của Preply để chạy các kiểm định.

## Findings đã xác minh

### 1. MHM là lớp kiểm định yếu hơn IRT tham số nhưng vẫn có giả định rõ

Nguồn Stochl et al. mô tả Mokken thuộc nonparametric item response theory (NIRT), mở rộng Guttman scaling theo hướng xác suất và nới lỏng dạng logistic/probit cứng của IRT tham số. Monotone Homogeneity Model (MHM) yêu cầu:

- **Unidimensionality**: nhóm item đo một latent trait chung.
- **Monotonicity**: xác suất trả lời đúng/đạt response level không giảm khi latent trait tăng.
- **Local independence**: sau khi điều kiện trên latent trait, response của một item không bị ảnh hưởng bởi response của item khác.

Khi các điều kiện này phù hợp, tổng điểm có thể dùng để xếp thứ tự người làm bài, nhất là với response nhị phân. Với vocabulary test, điều này hỗ trợ một bước QA quan trọng: nếu các item được tuyên bố là cùng đo receptive breadth nhưng không tạo được cấu trúc đơn điệu/đơn chiều, không nên giả định rằng raw score có thể quy đổi thẳng thành số từ.

MHM không xác nhận frequency band, lexical unit (headword/lemma/family), hoặc mapping từ latent trait sang số lượng từ. Các phần đó vẫn cần blueprint, item-bank manifest, calibration và criterion validation riêng.

### 2. Scalability coefficient đo mức độ item có thể xếp người làm bài, không phải số từ

Nguồn Stochl et al. cho các định nghĩa:

```text
H_ij = Cov(X_i, X_j) / Cov_max(X_i, X_j)

H_i = sum_{j != i} Cov(X_i, X_j)
      / sum_{j != i} Cov_max(X_i, X_j)

H = sum_{i<j} Cov(X_i, X_j)
    / sum_{i<j} Cov_max(X_i, X_j)
```

`H_ij` là scalability của một cặp item, `H_i` của item và `H` của toàn scale. Nguồn này nêu quy tắc diễn giải thực hành: `H < 0.3` không được xem là scale đơn chiều đủ dùng; `0.3 <= H < 0.4` là yếu; `0.4 <= H < 0.5` là trung bình; `H > 0.5` là mạnh. Đây là rule of thumb của Mokken scale analysis, không phải ngưỡng đã calibration cho vocabulary-size test.

Hệ quả thiết kế:

- Báo `H`, toàn bộ `H_i` và các cặp có `H_ij` thấp; không chỉ báo một alpha hoặc tổng điểm.
- Không chuyển `H = 0.45` thành “độ chính xác 45%” hay một số lượng word families.
- Không xóa item tự động chỉ vì `H_i` thấp trong một sample nhỏ; cần xem content coverage, frequency band, monotonicity và replicate/hold-out.
- Nếu các item trong cùng family/context có covariance cao do local dependence, `H` có thể nhìn tốt nhưng information hiệu dụng bị thổi phồng; phải kiểm tra dependency riêng.

### 3. Monotonicity và local independence là gate trước model fitting

Reference manual của package `mokken` cung cấp các hàm thực hành như `coefH`, `check.monotonicity`, `check.restscore`, `check.iio` và `check.pmatrix`. Manual mô tả kiểm tra monotonicity bằng các rest-score groups; `minsize` được dùng để tránh coi dao động nhỏ do sampling error là violation. Default được ghi trong manual là `N/10` khi `N >= 500`, `N/5` khi `250 <= N < 500`, và `max(N/3, 50)` khi `N < 250`. Đây là cài đặt phần mềm, không phải quy tắc production bắt buộc.

Đối với item vocabulary nhị phân, một QA run nên:

1. Tính rest score loại item đang kiểm tra.
2. Ước lượng `p(correct | rest-score group)` theo nhóm đủ lớn.
3. Gắn cờ nếu đường cong có giảm đáng kể, nhưng dùng ngưỡng violation đã pre-register và sensitivity theo cách chia nhóm.
4. Kiểm tra local dependence giữa các item chung stem, cùng context, cùng morphological family hoặc cùng distractor template.
5. Chạy lại trên sample hold-out và theo frequency band/L1/proficiency; không coi kết quả một calibration sample là bất biến.

Một violation nhỏ trong sample nhỏ không tự động là lỗi nội dung; ngược lại, violation lặp lại trên hold-out là lý do để sửa, thay hoặc loại item.

### 4. IIO/DMM mạnh hơn MHM và không được suy ra từ H cao

Double Monotonicity Model (DMM) thêm giả định item response functions không giao nhau. Khi IIO được hỗ trợ, thứ tự “dễ → khó” của item giữ ổn định trên các mức latent trait. Đây là điều kiện có thể làm cho việc diễn giải thứ tự item và một số quy tắc dừng trở nên dễ hơn.

MHM không bao gồm IIO. Nguồn Stochl et al. tách rõ việc kiểm tra monotonicity, non-intersection và IIO; với response đa mức, việc sắp xếp các item còn phức tạp hơn. Nguồn Myszkowski cũng nhấn mạnh IIO là giả định bổ sung, không tự động có chỉ vì một scale có scalability tốt. Bài đó báo cáo một ví dụ SPM-LS có `H = 0.469` (SE `= 0.021`) và vẫn kiểm tra riêng local dependence/IIO; đây là minh họa phương pháp trên intelligence test, không phải benchmark vocabulary.

Vì vậy, không được triển khai quy tắc “sai một từ thì bỏ qua các từ khó hơn” cho vocabulary test chỉ dựa trên raw frequency hoặc `H`. Chỉ cân nhắc dừng theo failure liên tiếp nếu:

- IIO được kiểm tra với item bank và population mục tiêu;
- violation rate/size có ngưỡng định trước;
- score từ stopping rule được so với full-form score trên hold-out;
- band coverage và tail estimates không bị lệch;
- quy tắc không làm mất thông tin ở người có profile không đơn điệu do domain hoặc L1.

### 5. Cỡ mẫu để chọn scale không phải số item người dùng phải làm

Trang nghiên cứu Tilburg của Straat, van der Ark & Sijtsma mô tả nghiên cứu mô phỏng độ ổn định của hai thuật toán chọn item trong Mokken scale analysis: AISP và genetic algorithm. Với tiêu chí misclassification 5%, abstract báo cáo khoảng **250–500 respondents** khi item quality cao và **1.250–1.750 respondents** khi item quality thấp.

Con số này áp dụng cho nhận diện/chọn scale trong calibration, không phải độ dài operational test và không phải cỡ mẫu để suy ra `K_hat` cho một cá nhân. Kiến trúc phải tách:

```text
calibration_N:
    số người cần để ước lượng/kiểm tra item-bank structure

operational_item_count:
    số item người dùng làm, quyết định bởi information/precision/cost
```

Không được dùng các khoảng trên để khẳng định một bài vocabulary test cần hàng trăm item. Ngược lại, một calibration sample quá nhỏ khiến AISP hoặc các ngưỡng H dễ không ổn định, đặc biệt khi bank có nhiều item chất lượng thấp, nhiều band hoặc nhiều subgroup.

### 6. Mokken là lớp QA, không thay thế Rasch/CAT/equating

Myszkowski ghi nhận các ưu điểm của Mokken cho việc kiểm tra monotonicity, IIO, local independence và khả năng xếp người bằng tổng điểm, nhưng cũng nêu giới hạn: Mokken scaling không cung cấp các khả năng CAT và test equating như Rasch. Với vocabulary-size product cần adaptive routing, alternate forms, common anchors, uncertainty và mapping từ latent ability sang lexical population, vì vậy Mokken nên đứng trước hoặc song song với IRT:

```text
content/lexical-unit blueprint
        ↓
Mokken/NIRT item-bank QA
        ↓
Rasch/2PL/response model calibration
        ↓
adaptive or stratified administration
        ↓
K_direct + uncertainty + family/domain sensitivity
```

Nếu Mokken flag một item, production không nhất thiết phải xóa ngay; item có thể bị giữ ở trạng thái `review`, kiểm tra content và pretest lại. Nhưng item bị violation lặp lại không nên được dùng như anchor hoặc item dừng CAT cho tới khi có resolution.

## Thuật toán QA đề xuất

### Manifest tối thiểu

Mỗi item trong item bank nên có:

```text
item_id
lexical_unit_id
frequency_band
prompt_form
response_type
correct_key
family_id / context_id
anchor_status
calibration_version
exposure_count
mokken_status
mokken_Hi
monotonicity_violation
local_dependence_flag
iio_status
```

`mokken_status` có thể nhận `pass`, `review`, `fail`, `not_run`; không được để thiếu rồi coi như pass.

### Pseudocode

```text
input:
    calibration_responses X[N, J]
    item_manifest M
    preregistered thresholds T

split respondents into calibration and holdout by person
stratify/slice checks by target population, proficiency and L1 when available

for each candidate scale S:
    verify declared lexical unit and content blueprint
    compute H_ij for every pair in S
    compute H_i and H for S

    run dimensionality evidence
    run monotonicity on rest-score groups
    run local-dependence diagnostics for:
        same family, shared context, repeated stem, shared template

    if any H_i or H below T.H_review:
        mark item/scale review; do not silently optimize only for H
    if repeated material monotonicity violation on holdout:
        mark item fail or require content revision
    if local dependence persists:
        cluster items, replace one item, or model dependency

    if stopping or ordered-tail routing is proposed:
        run IIO/non-intersection diagnostics
        simulate and evaluate stopped score vs full score on holdout
        disable stopping unless IIO and score-error gates pass

repeat all checks on holdout and versioned future sample
freeze only items with pass/review resolution and audit trail

fit the selected parametric response model only after QA
estimate person ability and K_hat with previously validated mapping
report QA status and uncertainty separately from vocabulary count
```

## Tích hợp vào estimator `K_hat`

Mokken output không phải một multiplier. Nó là điều kiện để quyết định có nên tin vào score structure của bank:

```text
if bank_QA in {fail, unresolved_review}:
    release K_hat = null or clearly provisional
    report affected bands/items and reason
else:
    fit calibrated response model
    estimate p_known for sampled lexical units
    apply frequency/design weights and previously validated lexical-unit mapping
    report K_direct, response/model interval, and QA flags
```

Nếu dùng stratified direct estimator, một dạng tổng quát vẫn là:

```text
K_direct = sum_b N_b * p_hat_b
```

trong đó `N_b` là số lexical units của band `b` theo vocabulary universe đã khai báo và `p_hat_b` được ước lượng từ response model/weights. Mokken chỉ giúp kiểm tra việc các item trong scale có cấu trúc đo đủ hợp lý; nó không cung cấp `N_b`, không quyết định headword/lemma/family và không thay thế uncertainty calibration.

## So sánh với cách làm Preply

| Thành phần | Preply theo methodology công khai đã có trong các artifact trước | Đề xuất sau iteration 49 |
|---|---|---|
| Item selection | Dictionary/headword universe, sampling theo midpoint/logarithmic rank theo mô tả vendor; production item bank chưa công khai | Giữ frequency-stratified coverage nhưng thêm Mokken QA trên response calibration |
| Scale assumptions | Chưa tìm được nguồn xác thực cho việc Preply kiểm tra MHM, monotonicity, local independence hoặc IIO | Kiểm tra và lưu `H`, `H_i`, monotonicity, dependency, IIO status trước khi fit/đổi bank |
| Stopping | Không có nguồn xác thực cho IIO-based stopping hoặc quy tắc dừng nội bộ | Không dừng theo failure liên tiếp nếu chưa có IIO + hold-out score-error evidence |
| Adaptive/IRT | Preply công khai midpoint/log-rank estimate; chưa có response-level/item-parameter data để xác minh CAT/IRT | Mokken là gate; IRT/Rasch vẫn cần cho ability, CAT, equating và uncertainty |
| Calibration sample | Chưa công khai cỡ mẫu hoặc quy trình item calibration của Preply | Tách `calibration_N` khỏi `operational_item_count`; cỡ mẫu Mokken phải được chứng minh theo bank/item quality |
| User-facing number | Vendor margin trước đây không bao gồm uncertainty do bank structure/construct mapping | Báo `K_direct` chỉ khi QA và calibration gates đạt; thêm provisional/QA flags khi chưa đạt |

Preply-specific claim về Mokken, IIO, cỡ mẫu calibration hoặc production thresholds: **chưa tìm được nguồn xác thực cho ý này**. Endpoint trực tiếp của Preply không được dùng làm nguồn mới trong iteration này.

## Assumptions và gaps

1. Ngưỡng `H = .3/.4/.5` là rule of thumb trong tài liệu Mokken, không phải ngưỡng đã validated cho vocabulary-size test.
2. Các nghiên cứu Mokken đã fetch không dùng item bank của Preply; không được gọi các kết quả của SPM-LS/WEMWBS là benchmark vocabulary.
3. Cần response-level data đủ lớn để phân biệt monotonicity violation thật với sampling error.
4. Local dependence trong vocabulary có thể đến từ family, shared context, stem template hoặc learning during test; cần metadata item và person-level administration log.
5. IIO là giả định mạnh hơn MHM. Nếu không đạt, vẫn có thể dùng MHM/sum score hoặc IRT phù hợp, nhưng phải tắt stopping dựa trên thứ tự item.
6. Chưa có dữ liệu để chọn `H_review`, `H_fail`, `minsize`, violation-size threshold, local-dependence threshold hoặc IIO score-error threshold riêng cho sản phẩm.
7. Chưa tìm được nguồn xác thực cho việc Preply chạy Mokken/NIRT, AISP, IIO, local-dependence diagnostics hoặc bất kỳ calibration sample size nào.

## Validation plan bổ sung

1. Tạo calibration dataset có đại diện các frequency bands, proficiency, L1 và domain sử dụng mục tiêu; tách person-level holdout ngay từ đầu.
2. Pre-register các ngưỡng review/fail và chạy sensitivity trên `H` thresholds, rest-score group sizes và cách xử lý missingness.
3. Chạy `coefH`, monotonicity và local-dependence diagnostics trên toàn bank; lập danh sách item bị flag, không chỉ chọn scale có H cao nhất.
4. Kiểm tra stability của item assignment/flagging bằng bootstrap hoặc repeated split; báo tỷ lệ item đổi trạng thái.
5. Với IIO/stopping, so sánh full-form `K_hat` với stopped-form `K_hat` theo band, tail, L1 và proficiency; release stopping chỉ khi sai số và coverage đạt tiêu chí holdout.
6. Sau QA, fit Rasch/2PL/CAT model, so sánh item/person estimates với bank không qua QA; kiểm tra score linking, CI coverage và alternate-form anchors.
7. Theo dõi drift theo version; item chuyển `pass → review/fail` phải bị loại khỏi anchor và kích hoạt equating/revalidation.

## Kết luận iteration

Mokken/NIRT cung cấp một lớp kiểm định bảo thủ, dễ audit và ít phụ thuộc dạng logistic để phát hiện item vocabulary không đơn chiều, không đơn điệu hoặc phụ thuộc cục bộ. `H`/`H_i` là chỉ báo khả năng xếp người làm bài, không phải số từ và không phải sai số của `K_hat`. IIO/DMM là điều kiện mạnh hơn, phải kiểm tra riêng trước mọi stopping theo thứ tự khó.

Khuyến nghị cập nhật thuật toán tổng thể: thêm Mokken QA sau content/lexical blueprint và trước IRT calibration; tách rõ calibration sample khỏi operational length; không dùng các ngưỡng/cỡ mẫu Mokken như tham số Preply; và chỉ release `K_hat`/stopping rule sau khi có hold-out evidence. Preply chưa công khai dữ liệu hoặc quy trình để đối chiếu các gate này.
