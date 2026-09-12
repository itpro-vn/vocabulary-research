# Iteration 53 — Planned-missing matrix sampling và booklet design

## Phạm vi

Iteration này kiểm tra một hướng thiết kế mới: thay vì đưa toàn bộ item bank cho mọi người, hệ thống phân phối các booklet/form xoay vòng, mỗi form chỉ chứa một phần item nhưng có anchor chung. Mục tiêu là giảm burden trong khi vẫn phủ các frequency band và calibrate được item bank. Trọng tâm là phân biệt `NA_BY_DESIGN` (item không được phát theo kế hoạch) với `NOT_REACHED`, `OMITTED` hoặc nonresponse.

Đây là bằng chứng thiết kế assessment nói chung; không phải bằng chứng rằng Preply hiện đang dùng matrix sampling, IRT, weights hoặc anchor linking.

## Nguồn đã fetch và verify

| Nguồn | HTTP | Nội dung dùng trong iteration |
|---|---:|---|
| Gonzalez & Rutkowski, *Principles of Multiple Matrix Booklet Designs and Parameter Recovery in Large-Scale Assessments* | 200 | Matrix sampling, trade-off coverage–burden–individual precision, IRT/common scale, mô phỏng số item/person và parameter recovery. |
| Aybek, Arıkan & Ertaş (2024), *A practical guide to item bank calibration with multiple matrix sampling* | 200 | Complete/incomplete, balanced/unbalanced, BIBD/PBIBD, common/rotating anchors, item-bank calibration bằng IRT. |
| Kaplan & Su (2018), ERIC record EJ1183725, *On Imputation for Planned Missing Data...* | 200 | So sánh two-form, three-form và PBIBD; kết luận design choice có thể ảnh hưởng bias mạnh hơn imputation choice. |
| NCES NAEP Technical Documentation | 200 | Precedent chính thức cho matrix sampling, weighting và IRT/scaling ở assessment quy mô lớn; không phải vocabulary-specific. |
| Preply test endpoint | 403 trong các lần kiểm tra trước và callback này | Không thể xác minh item pool, form assignment, missing-data policy, anchor, weights hoặc IRT của Preply. |

## Findings chính

### 1. Matrix sampling không mặc nhiên phù hợp với điểm số cá nhân

Gonzalez & Rutkowski mô tả multiple-matrix sampling/rotated booklet: item pool được chia thành các block; mỗi người nhận một subset khác nhau nhưng các form được nối với nhau. Cách này tăng content coverage của toàn bộ assessment và giảm thời gian/burden cho từng người.

Trade-off quan trọng: precision cá nhân bị hy sinh để tăng coverage. Thiết kế matrix sampling trong large-scale assessment thường tối ưu cho phân phối hoặc so sánh nhóm, trong khi một vocabulary-size test lại thường trả một `K_hat` cho từng người. Vì vậy:

- Nếu mục tiêu là **individual K_hat**, phải phân bổ đủ item/person và báo `SE_K`/interval; không dùng một form cực ngắn chỉ vì toàn item bank đã được phủ ở cấp quần thể.
- Nếu mục tiêu là **calibrate item bank hoặc ước lượng phân phối population**, matrix sampling có thể giảm burden đáng kể, nhưng output cá nhân phải được coi là model-based và có precision condition.
- Bằng chứng này không hỗ trợ việc coi raw percent-correct của các form khác nhau là cùng điểm nếu chưa equate.

### 2. Booklet phải có cấu trúc liên kết, không phải random subset độc lập

Aybek, Arıkan & Ertaş phân biệt:

- complete vs incomplete: mọi form có toàn bộ item hay chỉ subset;
- balanced vs unbalanced: item/block xuất hiện đều hay không đều;
- BIBD/PBIBD: các block xoay vòng theo cấu trúc để cân bằng hoặc gần cân bằng exposure;
- unbalanced incomplete design có thể dùng common block (anchor) hoặc rotating common parts.

Nguồn này cho ví dụ minh họa pool 90 item, non-rotating common part 10 item, rotating anchors 5+5 item và mỗi người làm 20 item. Ví dụ không phải quy tắc cho VST, nhưng cho thấy nguyên tắc triển khai: một pool lớn có thể được calibrate trên các form ngắn khi các form có đường nối bằng anchor.

Áp dụng vào vocabulary-size test:

1. Mỗi band/lexical unit có blueprint và tối thiểu anchor riêng; không để form 1 chỉ có low-frequency còn form 2 chỉ có high-frequency.
2. Anchor phải xuất hiện trên đủ các form cần nối và được khóa khỏi thay đổi tùy tiện.
3. Rotating items phải có inclusion probability và form assignment được log.
4. Nếu item chỉ được phát ở một form, item đó không nên là cầu nối duy nhất cho scale hoặc band quan trọng.

### 3. `NA_BY_DESIGN` không được chấm như sai

Với planned missingness, item không được phát là missing theo thiết kế, không phải evidence rằng người dùng không biết từ. Vì vậy response schema tối thiểu phải phân biệt:

```text
CORRECT
INCORRECT
NOT_SURE
OMITTED
NOT_REACHED
NA_BY_DESIGN
TECHNICAL_MISSING
```

`NA_BY_DESIGN` không vào mẫu số raw score và không bị quy thành incorrect. Khi calibration, dùng response quan sát được trên các form, item và anchor; dùng IRT/common scale hoặc một estimator thiết kế phù hợp. Với mục tiêu population, tài liệu IERI mô tả latent-regression IRT và plausible values là hướng thường dùng trong matrix-sampled assessment. Đối với điểm cá nhân, báo posterior/SE thay vì điền một câu trả lời giả rồi xuất hiện như dữ liệu quan sát.

### 4. Số item/person có ảnh hưởng phi tuyến đến precision

Mô phỏng trong Gonzalez & Rutkowski (với điều kiện sạch và item được target) báo cáo tương quan giữa ability thật và EAP estimate:

| Item/person | Correlation true–EAP |
|---:|---:|
| 8 | 0.869 |
| 16 | 0.925 |
| 24 | 0.946 |
| 56 | 0.974 |

Ở vùng giữa phân phối, standard error khoảng 0.40–0.50 khi có 8 item và khoảng 0.18 khi có 56 item. Error lớn hơn ở hai đầu vì test information thấp hơn. Tác giả cũng báo rằng trong dữ liệu mô phỏng sạch, 24 và 56 item cho individual reliability có vẻ đủ; 16 item vẫn trên .9 trong điều kiện đó. Đây **không** phải ngưỡng production cho VST: mô phỏng dùng item targeting tốt, response đúng mô hình, không đưa đầy đủ order effect, skew, item mismatch hay nonresponse thực tế.

Hàm ý: item budget phải được chọn bằng simulation dùng item parameters, frequency-band distribution và ability distribution của quần thể mục tiêu; không được suy ra một margin of error phổ quát từ `n_items`.

### 5. Thiết kế matrix có thể ảnh hưởng bias mạnh hơn lựa chọn imputation

Kaplan & Su (2018) so sánh three-form design dùng trong PISA 2012, two-form design và partially balanced incomplete block design, kết hợp các biến thể single+multiple và multiple+multiple imputation với predictive mean matching. Abstract của bản ghi ERIC báo cáo:

- lựa chọn **design** có ảnh hưởng lớn hơn lựa chọn **imputation method** đối với bias trong nghiên cứu;
- three-form design cho bias thấp hơn two-form và PBIBD trong các điều kiện họ so sánh;
- PBIBD cho bias thấp hơn two-form dù có cùng lượng missing.

Không chuyển các thứ hạng này trực tiếp sang vocabulary test: đây là planned missing context questionnaires và plausible values, không phải VST. Bài học dùng được là phải đánh giá form/anchor/band assignment trước, sau đó mới chọn cách imputation hoặc model. Không thể sửa một ma trận poorly linked bằng một lựa chọn MI bất kỳ.

### 6. Weighting và IRT là các lớp riêng

NCES NAEP Technical Documentation mô tả ba lớp vận hành tách biệt: matrix/probability sample để đại diện, statistical weighting để mẫu phản ánh population, và IRT/scaling để tạo phân phối/nhóm. Kiến trúc này hữu ích cho VST:

- `assignment_probability` và `form_weight` không phải vocabulary ability;
- `item response model` chuyển response thành latent estimate;
- `band/frequency expansion` chuyển latent evidence hoặc band-level estimate sang estimand K;
- population weighting chỉ dùng khi mục tiêu là norm/distribution, không tự động cải thiện individual K_hat.

Nguồn NCES không chứng minh Preply dùng bất kỳ lớp nào trong số này.

## Thiết kế đề xuất cho VST

### Hai chế độ phải tách rõ

**Individual mode (khuyến nghị nếu sản phẩm trả số từ cho từng người):**

- phát một form có đủ item/person để đạt target `SE_K`;
- có fixed core/anchors và band-balanced rotating items;
- có optional second-stage items ở band mà posterior còn rộng;
- không dùng planned missingness để giảm xuống mức làm precision cá nhân không đạt.

**Calibration/population mode:**

- dùng nhiều form incomplete/BIBD/PBIBD với anchor overlap;
- mỗi form có thể ngắn hơn, nhưng cần đủ người/form và đủ response/item;
- fit IRT/common-scale, latent regression hoặc plausible values phù hợp mục tiêu;
- report population distribution/norm uncertainty riêng với individual uncertainty.

### Data model tối thiểu

```json
{
  "respondent_id": "opaque-id",
  "form_id": "vst-2026-f03",
  "assignment_seed": "server-side-token",
  "item_id": "band07-item014",
  "band": 7,
  "lexical_unit": "lemma-or-family-versioned",
  "role": "anchor|rotating|pilot",
  "response_status": "CORRECT|INCORRECT|NOT_SURE|OMITTED|NOT_REACHED|NA_BY_DESIGN|TECHNICAL_MISSING",
  "display_order": 2,
  "item_version": "bank-2026.09",
  "response": 1,
  "latency_ms": 4210
}
```

`assignment_seed`, `form_id`, `item_version`, `role` và `response_status` là bắt buộc để phân biệt form difference, exposure, missingness và actual knowledge.

### Form-construction pseudocode

```text
build_forms(item_bank, bands, target_forms, items_per_person):
    validate_content_blueprint(item_bank, bands)
    anchors = choose_anchors(
        per_band=True,
        lexical_unit_balanced=True,
        DIF_clean=True,
        exposure_cap=True,
        minimum_overlap_between_adjacent_forms=True
    )
    blocks = partition_rotating_items(
        remaining_items=item_bank - anchors,
        preserve_band_quotas=True,
        avoid_local_dependence=True,
        balance_item_position=True
    )
    forms = construct_BIBD_or_PBIBD(anchors, blocks, target_forms)
    assert every_form_has_band_coverage(forms)
    assert graph_of_forms_is_connected(forms, edge='shared_anchor')
    simulate_response_data(forms, calibrated_item_params, target_population)
    reject_if(item_or_person_SE_too_large)
    reject_if(anchor_sensitivity_changes_K_materially)
    return forms
```

### Scoring/calibration pseudocode

```text
score(response_log, item_params, population_model=None):
    assert no_status_is_collapsed(response_log)
    observed = rows where status in {CORRECT, INCORRECT, NOT_SURE}
    planned_missing = rows where status == NA_BY_DESIGN
    nonresponse = rows where status in {OMITTED, NOT_REACHED, TECHNICAL_MISSING}

    fit_common_scale_irt(observed, fixed_or_linked_anchors=True)
    theta_hat, SE_theta = estimate_person_theta(observed)

    # Do not treat planned_missing as wrong.
    band_estimates = estimate_band_mastery(theta_hat, item_params, band_manifest)
    K_hat = expand_to_declared_estimand(band_estimates,
                                        lexical_unit='versioned',
                                        family_rule='calibrated-not-mechanical')
    SE_K = delta_or_posterior_transform(theta_hat, band_estimates)
    missing_sensitivity = rerun_under_nonresponse_scenarios(nonresponse)
    anchor_sensitivity = rerun_with_anchor_sets()

    return K_hat, interval(K_hat, SE_K), missing_sensitivity, anchor_sensitivity
```

### Stopping rule cho individual mode

Dừng khi tất cả điều kiện đều đạt:

1. mỗi frequency band cần báo cáo có số item quan sát tối thiểu theo calibration;
2. `SE_K` hoặc half-width của interval nhỏ hơn target đã định trước;
3. posterior/IRT information không còn tăng đủ lớn so với chi phí của item tiếp theo;
4. không có evidence của ceiling/floor, local dependence, DIF hoặc form-link failure;
5. `NA_BY_DESIGN` không bị nhầm với nonresponse;
6. nếu dừng ở giữa form, item selection probability đã được log và đưa vào estimator/sensitivity.

Nếu band cuối không được phủ hoặc interval vượt target: trả `insufficient_precision` thay vì một số từ có vẻ chính xác.

## So sánh với cách làm của Preply

| Thành phần | Thiết kế đề xuất | Preply hiện xác minh được |
|---|---|---|
| Form/item assignment | form matrix có anchor, band quota, seed/log | Chưa xác minh; endpoint trả 403 |
| Planned missing | trạng thái `NA_BY_DESIGN`, không chấm sai | Chưa tìm được nguồn xác thực cho policy |
| Cross-form linking | common/rotating anchors + IRT/common scale | Chưa xác minh anchor hoặc equating |
| Individual precision | chọn item budget bằng simulation và target SE | Chưa có response-level data để calibrate |
| Population weighting | tách assignment/design weights khỏi ability | Chưa xác minh Preply weights/norming |
| Missing/nonresponse | status-aware scoring và sensitivity | Chưa xác minh |
| Report | K_hat + interval + sensitivity + estimand | Current scoring/mapping chưa fetch được |

Không được ghi rằng Preply dùng hoặc không dùng matrix sampling chỉ từ UI/URL. Kết luận đúng hiện tại là: **chưa tìm được nguồn xác thực cho cách Preply assignment, missingness, anchor, weighting hay IRT.**

## Validation plan

1. **Design simulation:** sinh response theo item parameters và band-specific mastery distributions; so sánh full form, fixed short form, BIBD/PBIBD và rotating-anchor forms.
2. **Precision:** đo bias, RMSE, coverage của interval K, conditional SE theo band và theo percentile; tách individual mode khỏi population mode.
3. **Linking:** hold out một phần anchor; kiểm tra drift khi bỏ từng anchor set và khi thay rotating block.
4. **Missingness:** tạo `NA_BY_DESIGN`, MCAR-like omission, MNAR-like omission, not-reached và technical missing riêng; xác minh planned missing không tạo downward bias.
5. **Form fairness:** randomize assignment trong các nhóm L1, age, education và device; chạy DIF/invariance theo form và subgroup.
6. **Operational pilot:** phát nhiều form trên common-person sample đủ lớn; không release K scale nếu common-anchor graph không connected hoặc interval coverage không đạt.
7. **Preply comparison:** chỉ sau khi endpoint/item/response artifact được fetch được mới điền cột Preply; hiện giữ gap, không suy đoán.

## Gaps

- Chưa có item bank, form IDs, sampling probabilities, anchor list, response logs hoặc missingness codes của Preply.
- Chưa có dữ liệu vocabulary-specific để chọn số anchor, số item/person, form count, band quota, SE target hoặc design cutoff.
- Kết quả mô phỏng IERI/Gonzalez & Rutkowski là evidence thiết kế tổng quát và không thay thế calibration trên quần thể mục tiêu.
- Chưa tìm được nguồn xác thực cho một công thức universal biến planned-missing short forms thành cùng K_hat với một full-form Preply.
