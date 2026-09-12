# Iteration 57 — Content-constrained adaptive selection và shadow-test assembly

## Phạm vi

Iteration này nghiên cứu một vấn đề khác với CAT tổng quát: khi vocabulary-size test dùng adaptive selection, làm thế nào tối ưu thông tin mà vẫn giữ đúng vocabulary universe, frequency-band coverage, lexical-unit balance, enemy-item separation và item exposure. Mục tiêu là tránh việc maximum-information selection dồn vào vài item dễ thông tin nhất rồi làm thay đổi estimand hoặc tạo form không đại diện.

Không có bằng chứng rằng Preply hiện dùng shadow tests. Endpoint sản phẩm Preply được kiểm tra lại trong callback và trả HTTP 403; vì vậy phần Preply dưới đây chỉ ghi gap, không suy luận cơ chế nội bộ.

## Nguồn đã fetch và kiểm tra

| Nguồn | HTTP | Bằng chứng dùng trong iteration |
|---|---:|---|
| Bengs, Brefeld & Kröhne, *Optimal Constrained Item Selection in Computerized Adaptive Testing*, Journal of Computerized Adaptive Testing | 200 | Shadow-test assembly, content/enemy constraints, matroid greedy/intersection, mô phỏng SE và giới hạn độ phức tạp |
| Veldkamp, Verschoor & Eggen, *A multiple objective test assembly approach for exposure control problems in CAT* | 200 | Information–exposure–pool-usage objectives, exposure weights và điều kiện theo ability |
| Van der Linden/Chang, *Implementing Content Constraints in Alpha-Stratified Adaptive Testing Using a Shadow Test Approach* (ERIC archive text) | 200 | Kết hợp alpha-stratification với shadow constraints và cảnh báo stratification đơn độc không đảm bảo exposure bound |
| Nations vocabulary-size-test specification | 200 | Cấu trúc frequency-stratified word-family universe dùng làm ví dụ về estimand cần bảo toàn |
| Preply test endpoint | 403 | Không citable cho cơ chế hiện tại; chỉ ghi gap |

## Bằng chứng chính

### 1. Shadow test tối ưu trên full form, không chỉ item kế tiếp

Bengs, Brefeld và Kröhne mô tả shadow testing approach là phương pháp constrained item selection: ở mỗi bước, một full-length test khả thi được assembly tại trait estimate hiện tại; item tiếp theo được lấy từ test đó. Cách này làm cho các constraint của toàn test được xét trước, thay vì chỉ kiểm tra item còn lại ở bước hiện tại.

Điểm quan trọng cho VST là một form adaptive có thể có nhiều constraint đồng thời:

- số item tối thiểu/tối đa trong từng frequency band;
- lexical unit đã khai báo (headword, lemma hoặc word family), không trộn estimand;
- sense/context hoặc task facet;
- không chọn hai item cùng enemy cluster, cùng stem hoặc có quan hệ gây clue;
- item exposure cap và anchor quota;
- độ dài form và số item chưa dùng.

Nếu không nhìn trước, một CAT có thể đạt information tốt ở nửa đầu nhưng không còn đủ item để hoàn tất quota frequency hoặc tránh cluster ở cuối. Khi đó test vẫn có điểm số nhưng không còn là sample hợp lệ của declared universe.

### 2. Constraint đơn giản có thể dùng greedy; constraint phối hợp cần full-test optimization

Bengs et al. phân tích categorical bounds dưới dạng matroid constraints. Với một matroid constraint, greedy chọn item có information lớn nhất trong tập còn feasible và có thể đạt nghiệm tối ưu. Với hai matroid có thể dùng matroid intersection. Từ ba hoặc nhiều constraint tổng quát, bài toán có thể trở nên NP-hard; vì vậy production cần solver/algorithm có trạng thái feasibility rõ ràng, không âm thầm bỏ quota.

Bài báo mô phỏng bank tổng hợp 500 item, 2PL với item parameters coi như biết và test length 30. Trong các constraint áp dụng được, phương pháp tối ưu có SE thấp hơn tương đương test ngắn hơn tới 10% so với maximum priority index và tới 30% so với một constrained CAT heuristic khác. Đây là kết quả phương pháp trên bank tổng hợp, không phải biên độ hiệu quả đã được chứng minh cho VST hoặc Preply.

### 3. Coverage và enemy constraints có ý nghĩa construct, không chỉ là kỹ thuật

Nguồn JCAT cảnh báo hai rủi ro của selection chỉ theo information:

1. thiếu coverage content làm giảm face/content validity;
2. các item có stem hoặc quan hệ tương tự có thể tạo local dependence hoặc mutual clue.

Với vocabulary test, các item cùng word family, cùng stem, cùng context template hoặc cùng sense có thể làm response không độc lập. Một shadow-test manifest nên lưu `enemy_cluster_id`, `family_id`, `sense_id`, `context_template_id` và rule tối đa item mỗi cluster trong một form.

### 4. Exposure là objective riêng, không phải correction score

Veldkamp, Verschoor và Eggen mô hình hóa exposure control như bài toán nhiều mục tiêu: maximize information, minimize item compromise và optimize pool usage. Họ dùng exposure parameters dựa trên exposure rates quan sát làm trọng số trong item selection và cho phép điều kiện hóa theo ability level. Nguồn báo cáo phương pháp nhằm xử lý cả overexposure và underexposure.

Hệ quả cho vocabulary estimator:

- `exposure_penalty` chỉ điều chỉnh xác suất item được chọn;
- không trừ hay cộng số từ dựa trên exposure của item;
- item exposure, answer leakage và repeated-attempt status phải là quality/security metadata;
- nếu exposure làm thay đổi inclusion probability, estimator phải biết inclusion probability hoặc dùng model calibration tương ứng.

Nếu server chỉ chọn item bằng weighted information nhưng không log selection probability, không thể tái lập design-based uncertainty cho score adaptive.

### 5. Alpha-stratification hữu ích nhưng không tự đủ

Nguồn ERIC về alpha-stratified CAT kết hợp shadow tests cho biết shadow approach có thể áp dụng constraint trên item selection và tạo constraint giúp giảm overexposure/underexposure. Alpha-stratification có xu hướng làm exposure đều hơn, nhưng nguồn cũng ghi rõ exposure không tự động nằm dưới một upper bound; kết quả phụ thuộc pool size, item-parameter distribution, số strata và test length.

Do đó frequency bands của VST có thể dùng làm content strata ban đầu, nhưng không nên coi chúng là exposure-control mechanism. Cần thêm exposure monitoring và constraint theo ability hoặc form.

## Thuật toán đề xuất

### Item-bank manifest tối thiểu

Mỗi item cần có:

```text
item_id
lexical_unit_id
lexical_unit_type              # headword | lemma | word_family
frequency_manifest_id
frequency_band
sense_id
context_template_id
enemy_cluster_id
anchor_flag
irt_a, irt_b, optional_irt_c
calibration_version
exposure_cap
exposure_count_by_theta_bin
eligible_population/form flags
```

Universe phải khai báo trước:

- `M_h`: số lexical units trong frequency stratum `h`;
- `n_h_min`, `n_h_max`: quota item trong form;
- lexical-unit rule và inclusion/exclusion policy;
- target test length `N`;
- anchor/exposure/enemy constraints.

### Shadow-test objective

Với ability estimate hiện tại `theta_t`, item information `I_i(theta_t)` và binary selection variable `x_i`, assembly có thể viết:

```text
maximize  Σ_i x_i * I_i(theta_t)
          - λ_exp * ExposurePenalty_i(theta_t)
          - λ_dep * DependencePenalty_i
          - λ_anchor * AnchorPenalty_i
```

subject to:

```text
Σ_i x_i = N
n_h_min <= Σ_{i in band h} x_i <= n_h_max       for every h
Σ_{i in enemy cluster c} x_i <= cluster_cap_c
Σ_{i in lexical-unit group g} x_i <= lexical_cap_g
anchor_min <= Σ_i x_i * anchor_i <= anchor_max
exposure_count_i + x_i <= exposure_cap_i       when a hard cap applies
x_i ∈ {0,1}
```

Trong giai đoạn đầu, `ExposurePenalty`, `DependencePenalty` và `AnchorPenalty` có thể là objective phụ; các quota giữ vocabulary universe nên là hard constraints. Không dùng penalty để thay thế quota bắt buộc nếu penalty không có bằng chứng rằng quota luôn đạt.

Nếu objective có nhiều mục tiêu, phải ghi rõ `lambda`/priority trong versioned test specification. Không tự điều chỉnh lambda theo kết quả của từng người nếu điều đó làm inclusion design không tái lập.

### Pseudocode

```text
input:
  calibrated item bank B
  declared strata M_h and quotas [n_h_min, n_h_max]
  test length N
  exposure/enemy/lexical constraints
  prior or current posterior for theta

used = {}
responses = []
for t in 1..N:
    theta = estimate_theta(responses, fixed_item_parameters=True)

    eligible = {
      i in B:
      i not in used
      i satisfies population/form/mode rules
      i is not an exposed/compromised item beyond policy
    }

    shadow_status, shadow_test = assemble_full_test(
      eligible,
      theta,
      objective = information
                  - exposure_penalty
                  - dependence_penalty,
      hard_constraints = band_quota,
                       lexical_unit_bounds,
                       enemy_cluster_bounds,
                       anchor_bounds,
                       exposure_caps,
      length = N
    )

    if shadow_status != FEASIBLE:
        return status = INSUFFICIENT_FEASIBLE_BANK,
               partial_score = null,
               diagnostic = violated_constraints

    candidates = shadow_test - used
    item = choose_from_shadow_test(candidates, tie_break = seeded_server_random)
    response = administer(item)
    log(item_id, response, theta, shadow_id, solver_version,
        display_order, eligibility_snapshot, selection_probability)
    used.add(item)
    responses.append((item, response))

K_draws = posterior_or_irt_count_draws(responses, fixed_item_parameters=True)
report median(K_draws), quantiles(K_draws),
       constraint_status, exposure_status, calibration_version
```

`estimate_theta` và `posterior_or_irt_count_draws` phải dùng item parameters đã calibration trước. Không cho short form tự do ước lượng đồng thời toàn bộ `theta`, `a`, `b` và exposure parameters khi không có anchors; đó là unidentified hoặc quá bất ổn cho production.

### Quy đổi sang vocabulary count

Nếu posterior probability known của item `j` là `p_j^(s)` trong posterior draw `s`, và sample đại diện stratum `h`, count draw có thể là:

```text
K^(s) = Σ_h M_h * mean_{j in sampled_h}(p_j^(s))
```

Nếu item inclusion probabilities khác nhau, thay mean đơn giản bằng estimator có trọng số theo inclusion probability hoặc model-assisted calibration đã được validation. Không dùng `raw_correct / N * M` khi item difficulties trong adaptive form không đồng nhất.

Báo riêng:

- posterior/response interval với item parameters cố định;
- item-sampling/design interval qua replicate shadow forms hoặc bootstrap phù hợp;
- sensitivity khi thay quota/manifest/corpus/reference population;
- status nếu shadow assembly không khả thi hoặc constraint bị relax.

## So sánh với Preply

| Khía cạnh | Thuật toán đề xuất | Preply hiện xác minh được |
|---|---|---|
| Sampling | Adaptive có full-form shadow constraints; giữ quota theo declared universe | Trang endpoint sản phẩm trả 403 trong callback; không xác minh được current routing |
| Universe | Manifest versioned, lexical unit và stratum size công khai nội bộ | Các iteration trước đã ghi methodology vendor/proxy về dictionary/headword và frequency ranking, nhưng current item bank chưa xác minh trực tiếp trong callback này |
| Scoring | IRT/posterior trên item bank neo; count tính theo stratum/inclusion design | Chưa có nguồn xác thực cho item parameters, solver, exposure hoặc current score implementation |
| Constraint | Frequency, lexical-unit, enemy, anchor và exposure được log/QA | Chưa tìm được nguồn xác thực Preply dùng shadow test hay constraint nào |
| Uncertainty | Tách response/model, item-sampling/design và population sensitivity | Không được gán margin/interval cụ thể cho current Preply nếu không fetch được và không có coverage study |
| Security | Exposure caps, answer-security metadata, server-side seeded randomization | Chưa xác minh current controls |

## Assumptions và giới hạn

1. Item parameters đã calibration từ sample độc lập và được neo qua common items/form versions.
2. Frequency bands là coverage strata, không đồng nghĩa item difficulty hoặc mastery.
3. Shadow solver trả status và violated constraints; không fallback im lặng.
4. Exposure penalty không thay thế inclusion-probability accounting.
5. Các kết quả 10%/30% là mô phỏng trên bank tổng hợp, không chuyển thành expected gain của VST.
6. Nếu item bank không đủ để thỏa quota, sản phẩm phải trả `insufficient_feasible_bank` hoặc dùng một form khác đã được pre-calibrate; không tự nới constraint rồi giữ cùng scale.
7. Cited sources là CAT methodology chung; chưa có nghiên cứu shadow-test riêng cho English vocabulary-size count trong các nguồn của iteration này.

## Validation plan

1. Tạo bank pilot có `frequency_band × lexical_unit × sense × enemy_cluster` manifest và calibrate 1PL/Rasch/2PL trên sample độc lập.
2. So sánh bốn selector trên cùng response simulation: unconstrained MFI, greedy quota, shadow-test ILP và shadow-test + exposure control.
3. Đo: bias của `K_hat`, RMSE, conditional SEM, band coverage, constraint violation, solver latency, item exposure Gini/max và rate of infeasible assembly.
4. Dùng common-person/common-item forms để kiểm tra linking giữa fixed stratified form và adaptive shadow form.
5. Hold-out validation theo L1, proficiency và retest; kiểm tra whether adaptive selection thay đổi DIF hoặc domain transport.
6. Stress-test enemy clusters/local dependence bằng item sets có shared stem/family/context; compare naive CI với cluster/design-aware CI.
7. Run exposure simulation theo theta bins và repeated attempts; đặt cap chỉ sau khi kiểm tra trade-off information–security–pool usage.
8. Chỉ release adaptive count nếu item parameters, shadow constraints, solver version, selection log và interval coverage đều pass; nếu không, report diagnostic status thay vì số từ có vẻ chính xác.

## Gap cần tiếp tục

- Chưa có current Preply item bank, routing log, constraints, solver hoặc exposure telemetry.
- Chưa có response-level vocabulary pilot để định lượng trade-off giữa shadow constraints và precision.
- Chưa có vocabulary-specific evidence để chọn quota, exposure cap, enemy-cluster cap, lambda hoặc solver fallback.
- Chưa có common-person/common-item data để chứng minh shadow-adaptive scale tương đương với Preply headword scale.
