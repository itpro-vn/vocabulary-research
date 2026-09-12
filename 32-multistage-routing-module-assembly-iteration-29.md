# Iteration 29 — multistage adaptive vocabulary testing and routing robustness

## 1. Phạm vi và mức độ bằng chứng

Iteration này kiểm tra một hướng riêng: thay vì chọn từng item như CAT thuần túy, bài test có thể dựng sẵn các **module** theo mức độ khó và route giữa các module. Mục tiêu là giữ được:

- adaptation theo năng lực;
- coverage có chủ đích của frequency bands và lexical units;
- các pathway/panel có thể so sánh;
- kiểm soát exposure và bảo mật item bank;
- khả năng review đáp án trong một stage, thay vì phụ thuộc hoàn toàn vào quyết định item-by-item.

Bằng chứng chính gồm:

1. Li et al., *Automated Test Assembly for Multistage Testing With Cognitive Diagnosis* (Frontiers, 2021), bản PDF truy cập qua Europe PMC, HTTP 200: khung MST/CD-MST, panel/module/pathway, ATA và các ràng buộc thống kê/phi thống kê.
2. Rutkowski, Liaw, Svetina & Rutkowski, *Multistage Testing in Heterogeneous Populations: Some Design and Implementation Considerations* (Applied Psychological Measurement, 2022), bản PDF truy cập qua Europe PMC, HTTP 200: mô phỏng routing, module length, exposure và bias ở các quần thể năng lực khác nhau.
3. Xu, Wang, Cai & Tu, *The Automated Test Assembly and Routing Rule for Multistage Adaptive Testing with Multidimensional Item Response Theory* (Journal of Educational Measurement, 2021), hồ sơ ERIC HTTP 200: abstract về ATA/routing cho M-MST và so sánh với MCAT.

Các số liệu routing trong Rutkowski là kết quả mô phỏng ILSA/TIMSS, không phải calibration của vocabulary test. Không được chuyển trực tiếp các con số như 36 item hay xác suất misrouting 0,30 vào sản phẩm.

## 2. Findings đã xác minh

### 2.1 MST là adaptation ở cấp module

Li et al. mô tả MST gồm nhiều panel song song; mỗi panel có stages, modules và pathways. Thí sinh bắt đầu bằng một panel được gán ngẫu nhiên, trả lời module ở stage đầu, sau đó được route sang module ở stage tiếp theo phù hợp với năng lực ước lượng. Chuỗi module đã đi qua là pathway.

Điểm thiết kế quan trọng: MST là một thỏa hiệp giữa CAT và linear test. Nó vẫn thích nghi, nhưng item được quản lý trong các module dựng sẵn. Trong nguồn này, MST còn cho phép người làm bài xem lại/sửa đáp án trong stage hiện tại và hỗ trợ việc giữ các panel tương đương.

**Áp dụng:** item vocabulary không nên được chọn chỉ theo frequency rank. Mỗi module phải có manifest gồm frequency coverage, lexical unit, sense/context, format, difficulty và exposure metadata.

### 2.2 Parallelism phải được kiểm tra ở cấp pathway/panel

Li et al. nêu ba mục tiêu assembly:

1. module có information curve đủ rõ để phân biệt các stage;
2. information của các pathway tương ứng giữa các panel tương tự;
3. từng pathway thỏa ràng buộc phi thống kê.

Ràng buộc phi thống kê trong bài gồm content balance và exposure control; ràng buộc thống kê có target test-information function, test length và cấu trúc stages/modules.

Với vocabulary-size test, "content" cần được mở rộng thành frequency-band coverage, lexical-unit quota (headword/lemma/word family), domain profile, sense/polysemy policy và tỉ lệ item format. Một pathway chỉ được coi là tương đương khi cả thông tin đo lường và các coverage constraint quan trọng đều đạt.

### 2.3 Có hai chiến lược assembly, với trade-off khác nhau

Li et al. phân biệt:

- **Top-down:** đặt target information cho toàn pathway, sau đó xây những pathway tương ứng giữa các panel.
- **Bottom-up:** xây các module song song theo target information riêng, sau đó trộn module thành các panel.

ATA có thể dùng linear programming để đáp ứng chặt content constraints và các ràng buộc kiểu enemy-item, nhưng bài báo cảnh báo bài toán 0–1 có thể phức tạp, tốn thời gian hoặc infeasible khi item bank nhỏ mà constraints quá nhiều. Heuristic giảm tải tính toán nhưng cần hậu kiểm rằng các panel thực sự đạt specifications.

**Quy tắc sản xuất:** chạy solver/heuristic offline; không assemble tại request của người dùng. Mỗi panel/pathway được version hóa và có report về độ lệch so với target.

### 2.4 Routing merit thuần túy có thể làm lệch exposure và parameter recovery

Rutkowski et al. mô phỏng MST 1-2-3, bốn linked panels, 36 item/người và nhiều quần thể năng lực. Merit routing tạo exposure lệch: item dễ được đưa nhiều hơn cho nhóm low-performing và item khó nhiều hơn cho nhóm high-performing. Trong mô phỏng, merit routing có bias lớn hơn ở achievement estimates, ảnh hưởng rõ hơn tới nhóm low-performing; standard errors lại nhỏ hơn.

Probabilistic misrouting, tức mỗi người vẫn có xác suất khác 0 đi vào module không tối ưu, làm giảm bias/variability trong parameter recovery so với merit routing, với standard error nằm giữa merit và random routing. Tác giả nhấn mạnh đây là thỏa hiệp precision–bias, không phải một xác suất tối ưu phổ quát.

**Áp dụng:** nếu dùng module routing, cần ghi lại xác suất route và bảo đảm mọi module có xác suất exposure đủ để calibrate. Không route cứng theo một ngưỡng score mà không có sensitivity simulation.

### 2.5 Equal module length và CTT routing là baseline thực dụng, không phải bằng chứng tương đương

Trong mô phỏng của Rutkowski et al., module length bằng nhau giúp kiểm soát position effects. Number-correct/CTT routing có kết quả gần chấp nhận được so với IRT routing trong các điều kiện mô phỏng, nhưng item khó có variability giữa replication cao hơn. Nghiên cứu cũng thấy thiết kế có short core module có slight positive bias ở low-achievement groups; core dài hơn giảm bias trong chính điều kiện đó.

**Áp dụng:** có thể dùng CTT number-correct để route ở bản triển khai đầu nếu chưa có IRT realtime, nhưng phải:

- giữ final scoring trên một thang đã calibration;
- benchmark CTT-route với IRT-route;
- dùng equal-length modules làm baseline để giảm position confound;
- chọn core length bằng simulation/D-study, không sao chép số item của nghiên cứu khác.

### 2.6 ATA/routing hữu ích khi có nhiều constraints, nhưng evidence vocabulary-specific còn thiếu

Abstract ERIC của Xu et al. ghi nhận hai loại ATA và một bộ routing rules cho M-MST; mô phỏng trên item banks giả lập và một multidimensional assessment cho thấy M-MST đạt quality control tốt và ability estimation bằng hoặc tốt hơn MCAT trong cùng điều kiện, đặc biệt khi phải đáp ứng nhiều non-statistical constraints.

Đây là căn cứ cho kiến trúc preassembled modules khi vocabulary test cần đồng thời cân bằng frequency, lexical unit, domain và exposure. Nó không chứng minh M-MST luôn tốt hơn CAT hoặc rằng các module vocabulary đã có đủ thông tin.

## 3. Thuật toán đề xuất: constrained MST cho vocabulary breadth

### 3.1 Data model bắt buộc

Mỗi item có tối thiểu:

```text
item_id, prompt_version, answer_key
lexical_unit_type, lexical_unit_id, word_family_id
frequency_source, corpus_version, band, rank
sense_id, part_of_speech, domain_tags
format, difficulty_b, discrimination_a, guessing_c
panel_id, module_id, pathway_ids
exposure_count, exposure_rate, last_seen_at
anchor_flag, enemy_group, device/mode metadata
```

Mỗi module có:

```text
module_id, stage, target_theta_range, item_ids
length, target_information_curve
band_quota, lexical_unit_quota, domain_quota
anchor_ids, exposure_limits, content_constraints
```

### 3.2 Assembly offline

Một candidate assembly phải thỏa các hard constraints:

- item không xuất hiện hai lần trong cùng pathway;
- không vi phạm enemy/context overlap;
- đạt minimum coverage cho các band được khai báo;
- không gom quá nhiều lexical relatives hoặc shared contexts gây local dependence;
- anchor phân bố đủ giữa panel/pathway;
- exposure dự kiến nằm trong giới hạn;
- mọi pathway có coverage và information target trong tolerance;
- tail modules không được xem là chính xác nếu bank không có item thông tin ở tail đó.

Soft objective có thể tối thiểu hóa:

```text
Loss(panel) =
  wI * distance(TIF_pathway, target_TIF)
+ wC * coverage_deviation
+ wA * anchor_deviation
+ wE * exposure_imbalance
+ wD * dependence_penalty
+ wP * position_effect_proxy
```

`w*`, tolerance và quota không được coi là phổ quát; chọn qua calibration sample và D-study.

### 3.3 Routing

Candidate production blueprint, cần simulation trước khi chốt:

- stage 1: một core module có độ khó trung tâm và coverage rộng;
- stage 2: các module easy/medium/hard;
- stage 3: các module tail-low / central / tail-high hoặc các module được target theo posterior ability;
- nhiều panel song song, random panel assignment;
- route theo IRT provisional theta nếu có; dùng number-correct theo bảng route đã calibration nếu chưa có realtime IRT;
- thêm randomization có giới hạn hoặc probabilistic routing để mọi module có exposure và calibration support;
- luôn ghi `route_rule_version`, `route_probability`, `module_id`, `theta_before_route` và `route_reason`.

Randomization không được làm hỏng coverage cá nhân: xác suất route vào module phù hợp vẫn phải chiếm phần lớn, còn xác suất route thay thế được chọn từ simulation để kiểm soát bias/exposure. Chưa có nguồn xác thực cho một xác suất chung áp dụng cho vocabulary.

### 3.4 Scoring và quy đổi sang số từ

Final score phải được ước lượng trên thang chung, không dùng raw percent giữa các pathway nếu chưa equate.

Với IRT, ước lượng `theta_hat` từ toàn bộ response pathway bằng item parameters đã calibration. Quy đổi sang count bằng calibration function đã fit trên common-person sample:

```text
V_hat(theta) = A / (1 + exp(-B * (theta - C)))
```

`A`, `B`, `C` phụ thuộc word universe, lexical unit, corpus version và calibration sample. Chúng không được lấy từ Preply hoặc nghiên cứu khác nếu không có common-person/common-item linking.

Nếu muốn giữ estimator design-based theo frequency bands, với band `b` có universe size `N_b`, inclusion probability `pi_i` và response/knowledge estimate `p_hat_b`:

```text
V_hat = sum_b N_b * p_hat_b
p_hat_b = sum_i (R_i / pi_i * y_i) / sum_i (R_i / pi_i)
```

MST routing làm `pi_i` phụ thuộc vào stage, response và module path. Phải log hoặc tính được `pi_i`; không được giả định mọi item có cùng inclusion probability. IRT estimate và design-based estimate nên được dùng như sensitivity estimators cho tới khi hold-out cho thấy chúng agree trong tolerance.

### 3.5 Pseudocode

```text
ASSEMBLE_BANK(item_bank, specs, calibration_data):
    fit_or_import_item_parameters(calibration_data)
    candidates = generate_panels_and_pathways(item_bank, specs)
    candidates = reject_hard_constraint_violations(candidates)
    for candidate in candidates:
        candidate.loss = evaluate_TIF_coverage_anchors_exposure_dependence(candidate)
    chosen = optimize_or_heuristic_select(candidates)
    verify_each_pathway(chosen)
    simulate_routes(chosen, proficiency_grid, response_models, route_error_grid)
    reject_if_bias_or_interval_coverage_fails(chosen)
    publish_versioned_panel_manifest(chosen)

RUN_TEST(response_stream, panel):
    path = []
    for stage in panel.stages:
        module = select_module(stage, provisional_theta, route_rule_version)
        response = administer(module)
        log(module, response, inclusion_probability, device_context)
        path.append(response)
        provisional_theta = estimate_theta(path, calibration_parameters)
        if quality_gate_fails(path):
            continue_with_flag_or_stop_by_protocol()
    theta = final_equated_estimate(path)
    count = calibration_function(theta)
    interval = combine_response_SE_model_uncertainty_and_linking_error(theta)
    status = classify_endpoint_bank_coverage_effort_and_route_quality(path)
    return {theta, count, interval, path, status}
```

## 4. Độ không chắc chắn và routing-error sensitivity

Báo cáo ít nhất bốn thành phần riêng:

1. `CI_response_or_sampling`: uncertainty do số item và response trong các band/pathway;
2. `CI_model`: item-parameter/model uncertainty;
3. `CI_linking`: common-anchor/equating uncertainty giữa panel và form;
4. `route_sensitivity_range`: thay đổi estimate khi dùng IRT route, CTT route và routing-error scenarios.

Có thể tổng hợp thận trọng bằng simulation:

```text
for replicate in bootstrap_or_posterior_draws:
    draw item parameters and response model
    draw route realization using logged route probabilities
    estimate theta and V_hat
    store V_hat
report quantiles plus separate sensitivity ranges
```

Không gộp `route_sensitivity_range` vào một CI hẹp nếu routing rule chưa được calibration. Nếu endpoint module không có information đủ, trả `low_information`/`censored` thay vì ép một count chính xác.

## 5. So sánh với Preply đã xác minh

| Thuộc tính | Preply methodology đã đọc ở iteration trước | MST đề xuất trong iteration này |
|---|---|---|
| Word universe | Dictionary hơn 45.000 entries, derived forms aggregate về dictionary headwords theo methodology đã fetch qua proxy; đây là headword estimand | Khai báo rõ headword/lemma/word-family; calibration riêng cho từng estimand |
| Frequency | BNC-derived mixture spoken/written, rank và logarithmic sampling theo methodology đã fetch | Frequency là một constraint trong module/pathway; version hóa corpus và band manifest |
| Adaptation | Methodology công khai mô tả hai phase và midpoint sampling, nhưng không xác minh được module routing | Preassembled panel/module/pathway, route log và common-scale calibration |
| Uncertainty | Vendor-stated khoảng ±10%, chưa có independent response-level coverage trong nguồn truy cập | Tách response/model/linking/route sensitivity; coverage phải kiểm tra bằng hold-out simulation và calibration |
| Guessing/effort | Không xác minh được live controls; endpoint trực tiếp trả 403 trong lần kiểm tra trước | Effort/rapid guessing là validity flag riêng; không trừ trực tiếp số từ |
| Panel/form equivalence | Chưa có item bank hoặc route log công khai để xác minh | ATA kiểm tra TIF, band/lexical coverage, anchors, exposure và dependence trước khi publish |
| Production evidence | Chưa có response-level data, routing probabilities, item exposure hay common-anchor data công khai | Chưa phải production result; đây là algorithm specification cần pilot |

Hai thang Preply-headword và MST-lemma/word-family không được coi là cùng một số. Muốn so sánh cần common-person/common-item calibration và báo conversion uncertainty.

## 6. Validation plan trước khi triển khai

1. **Bank audit:** kiểm tra lexical-unit mapping, sense, frequency snapshot, local dependence và enemy/context groups.
2. **Pilot calibration:** sample đa dạng proficiency/L1/domain; fit Rasch/2PL suite; kiểm tra item fit, DIF, option functioning và response process.
3. **Assembly simulation:** chạy proficiency grid gồm floor, central và advanced tail; so sánh equal-length với unequal-length modules; đo bias, RMSE, CSEM/coverage và exposure.
4. **Routing study:** so sánh IRT merit, CTT number-correct, random và probabilistic routing. Tuning xác suất probabilistic chỉ từ bank-specific simulation; không dùng 0,30 như mặc định.
5. **Panel linking:** đặt common anchors giữa panels/forms; kiểm tra drift, anchor stability và pathway equivalence.
6. **Hold-out validation:** đánh giá count interval coverage, rank reliability, criterion validity và domain/task coverage trên người không dùng để calibration.
7. **Operational monitoring:** theo dõi route frequencies, module exposure, endpoint/censoring, item parameter drift, path-specific residuals và device/effort flags.
8. **Release gate:** chỉ publish count nếu panel version, lexical estimand, calibration version, uncertainty status và route quality đều đã ghi được; nếu không, trả estimate với trạng thái limitation.

## 7. Gaps

- Chưa có item bank, module/pathway definitions, routing log, exposure probabilities hoặc response-level data của Preply.
- Chưa xác minh Preply có sử dụng MST, CAT, CTT routing hay probabilistic routing; methodology endpoint trực tiếp trả 403.
- Chưa có số liệu vocabulary-specific để chọn số stage, module length, core length, route cutoffs, probabilistic routing rate, anchor rate hoặc tolerance của TIF/coverage.
- Chưa có hệ số quy đổi đã calibration giữa Preply headwords và lemma/word-family.
- Bằng chứng Rutkowski và Li et al. là phương pháp/MST hoặc mô phỏng giáo dục nói chung; cần validation riêng trên vocabulary-size response data.

**Kết luận iteration:** MST là hướng triển khai đáng thử khi test phải đồng thời giữ frequency/lexical/domain coverage, form equivalence và exposure control. Baseline an toàn là equal-length preassembled modules, route theo IRT hoặc CTT đã calibration, panel/pathway anchors, và routing sensitivity report. Không được coi routing module là cải thiện đã chứng minh so với Preply cho đến khi có pilot và hold-out coverage.

## Sources checked

- Li, Y. et al. (2021), *Automated Test Assembly for Multistage Testing With Cognitive Diagnosis*, PDF HTTP 200: https://europepmc.org/articles/PMC8136431?pdf=render
- Rutkowski, L. et al. (2022), *Multistage Testing in Heterogeneous Populations: Some Design and Implementation Considerations*, PDF HTTP 200: https://europepmc.org/articles/PMC9382094?pdf=render
- Xu, L. et al. (2021), *The Automated Test Assembly and Routing Rule for Multistage Adaptive Testing with Multidimensional Item Response Theory*, ERIC record HTTP 200: https://eric.ed.gov/?id=EJ1327563
- Preply methodology (direct check in prior iterations: HTTP 403, not treated as verified for current controls): https://preply.com/en/learn/english/test-your-vocab/how-it-works
