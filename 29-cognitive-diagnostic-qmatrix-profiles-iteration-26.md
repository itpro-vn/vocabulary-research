# Iteration 26 — Cognitive-diagnostic profiles và Q-matrix cho vocabulary test

## 1. Câu hỏi của iteration

Iteration này tách một câu hỏi thường bị trộn với vocabulary-size estimation:

> Có nên dùng cognitive diagnostic models (CDM/DCM) để suy ra người làm bài mạnh/yếu ở các lexical subskills, và nếu có thì làm thế nào để không biến profile chẩn đoán thành một vocabulary count giả chính xác?

Direction mới tập trung vào Q-matrix và diagnostic classification, không lặp lại việc ước lượng breadth bằng frequency bands, CAT/IRT, tail censoring hay sequential stopping.

## 2. Nguồn đã fetch và kiểm tra

| Nguồn | Kiểm tra | Vai trò |
|---|---:|---|
| Cambridge University Press & Assessment, *Cognitive Diagnostic Models and how they can be useful* | HTTP 200; PDF đã tải và trích xuất 1.69421e5 bytes text | Framework CDM, Q-matrix, model/classification uncertainty, Q-matrix validation và giới hạn triển khai |
| Javidanmehr & Anani Sarab (2017), *Cognitive Diagnostic Assessment: Issues and Considerations* | HTTP 200; PDF đã tải và trích xuất 6.7475e4 bytes text | Case study ngôn ngữ: thuộc tính vocabulary meaning, triangulation, expert review, Q-matrix validation |
| Zhang et al. (2023), *A Cognitive Diagnostic Assessment Study of the Reading Ability in the B1 Preliminary Test* | HTTP 200; PDF đã tải và trích xuất 5.8171e4 bytes text | Case study độc lập về Q-matrix: GDI/PVAF/mesa plot, heatmap dependency, sửa Q-matrix và G-DINA |
| Preply test/how-it-works | Các iteration trước: endpoint trực tiếp trả HTTP 403 | Chỉ dùng để ghi gap; không suy ra Preply có CDM hay lexical profile |

Search snippets chỉ dùng để tìm lead. Các URL trong bảng nguồn chính đều đã được HTTP-verify trước khi dùng claim.

## 3. Findings đã xác minh

### 3.1 CDM trả profile mastery, không phải phép thay thế cho vocabulary breadth

Cambridge review mô tả CDM là mô hình latent multidimensional: mỗi item nối với một hoặc nhiều attribute qua Q-matrix, và mục tiêu là phân loại người làm bài theo vector mastery/non-mastery. Với mỗi người, mô hình có thể trả:

- xác suất thuộc từng latent class;
- xác suất mastery biên của từng attribute;
- một nhãn class theo MLE/MAP/EAP nếu cần;
- các chỉ số item difficulty/discrimination, model fit và classification consistency/accuracy.

Điểm quan trọng về estimand: `vocabulary_size` hỏi “có bao nhiêu lexical units trong universe mà người này biết theo định nghĩa đã chọn”; CDM profile hỏi “những thuộc tính nào có bằng chứng mastery trong task được thiết kế”. Hai output có thể liên quan nhưng không đồng nhất. Một người có thể nhận diện form nhưng chưa truy hồi nghĩa, hoặc biết meaning trong context nhưng yếu ở morphology/collocation. Không có cơ sở để cộng các xác suất subskill thành thêm số word.

**Quy tắc sản phẩm:** breadth estimate vẫn là output chính và giữ đúng `unit`, `universe.version`, corpus/frequency manifest. Profile CDM, nếu triển khai, là output phụ gồm `p_mastery` và confidence/status cho từng attribute.

### 3.2 Q-matrix phải bắt đầu từ construct theory và evidence response-process

Case study của Javidanmehr & Anani Sarab (2017) retrofit một bài đọc tiếng Anh không được thiết kế ban đầu như diagnostic test. Nhóm tác giả xác định attributes bằng ba nguồn:

1. literature về proficiency/reading;
2. panel chuyên gia;
3. think-aloud protocols của 10 người đã làm bài.

Bốn attribute cuối cùng gồm: understanding vocabulary meaning, making inferences, understanding explicit information và connecting/synthesizing. Các chuyên gia mã hóa item độc lập, thảo luận panel, rồi chuẩn bị Q-matrix ban đầu trước khi validate bằng dữ liệu.

Tín hiệu dùng cho thiết kế vocabulary test:

- `meaning recognition` phải được định nghĩa ở mức lexical task cụ thể, không gắn nhãn chung chung “biết từ”;
- nếu test muốn tách `form`, `meaning`, `morphology`, `collocation`, mỗi attribute phải có operational definition và item evidence;
- item được đánh dấu nhiều attribute chỉ khi task thực sự yêu cầu đồng thời các attribute đó;
- think-aloud là bằng chứng để kiểm tra người làm bài thực sự dùng process dự kiến, không chỉ là cách nhà biên soạn tưởng tượng họ giải item.

Nếu chỉ retrofitting Q-matrix lên một bài test recognition ngắn mà không có semantic/morphological/collocational evidence, profile sẽ dễ bị diễn giải quá mức.

### 3.3 Q-matrix validation cần cả data-driven gate và expert adjudication

Các nguồn đều nhấn mạnh Q-matrix misspecification là điểm dễ làm CDM sai. Quy trình được verify trong case study B1 Preliminary gồm:

1. tạo Q-matrix ban đầu từ theory và content experts;
2. dùng G-DINA discrimination index (GDI) để khảo sát q-vector ứng viên của từng item;
3. xem mesa plot/PVAF, chọn q-vector ở vùng plateau/edge thay vì áp một cutoff đơn lẻ;
4. đưa các đề xuất thay đổi về expert panel để kiểm tra chúng có hợp lý về nội dung hay không;
5. kiểm tra item dependency bằng heatmap của transformed correlations/log-odds;
6. chỉ dùng final Q-matrix sau khi sửa các misspecification hợp lý và lưu version.

GDI ở đây là variance của xác suất trả lời đúng giữa các attribute patterns theo q-vector. Nhiều q-vector có thể đạt mức GDI gần như nhau; vì vậy mesa plot giúp tránh coi một cutoff tùy ý là chân lý. Trong case study, heatmap phát hiện dependency giữa item 24 và 25; sau thay đổi Q-matrix, dependency đó biến mất.

**Production gate:** chưa qua expert + GDI/PVAF + local-dependence audit thì không xuất profile mastery. Item vẫn có thể đóng góp vào breadth estimator nếu đạt các gate item-quality riêng, nhưng Q-matrix chưa hợp lệ phải được gắn `diagnostic_status = unavailable`.

### 3.4 Profile phải giữ posterior uncertainty, không chỉ xuất hard label

Theo Cambridge review, với `K` binary attributes có tối đa `2^K` latent classes nếu không có hierarchy. Với response vector `x_i`, posterior class probability có dạng:

```text
P(alpha_c | x_i) ∝ P(x_i | alpha_c) P(alpha_c)
```

Từ đó xác suất mastery biên của attribute `k` là:

```text
p_mastery[k] = Σ_c P(alpha_c | x_i) * I(alpha_c[k] = 1)
```

Hard label kiểu `mastered`/`not_mastered` chỉ là một quyết định sau cùng, thường dùng ngưỡng 0.5 trong mô tả phương pháp; nó không nên che mất posterior. Cambridge review cũng ghi rõ classification accuracy/consistency chỉ nên diễn giải sau khi CDM fit dữ liệu phù hợp. Accuracy tổng thể có thể gây hiểu nhầm: nếu 90% quần thể đã có attribute, một mô hình gần như không có thông tin vẫn có thể đạt accuracy cao do dự đoán majority class.

**Quy tắc báo cáo:**

```text
profile[k] = {
  p_mastery,
  status: mastered | not_mastered | uncertain,
  posterior_entropy_or_top_class_gap,
  item_count,
  qmatrix_version,
  model_version
}
```

Chỉ gắn `mastered` khi posterior threshold và classification-coverage gate đã được calibration trên population mục tiêu. Nếu posterior gần nhau, trả `uncertain`; không ép thành nhãn nhị phân. Đánh giá thêm sensitivity khi đổi model (DINA/G-DINA/ACDM/RRUM phù hợp item) và Q-matrix.

### 3.5 CDM hữu ích cho diagnostic feedback nhưng chưa phải mặc định production

Cambridge review phân biệt “true diagnostic assessment” được thiết kế ngay từ đầu cho feedback với “retrofitting” một test không diagnostic. Review ghi nhận CDM còn ít được dùng rộng rãi trong operational assessment, và các ví dụ retrofit nhiều hơn true-CDA. Bằng chứng này không phủ nhận giá trị của CDM; nó đặt ra điều kiện triển khai: muốn profile có ý nghĩa hành động, item design, Q-matrix và reporting phải được xây cho mục tiêu chẩn đoán, thay vì suy diễn từ một tổng điểm ngắn.

Với bài test mục tiêu là ước lượng số lượng từ, lựa chọn bảo thủ là:

- không thay fixed/stratified breadth estimator bằng CDM;
- thêm một diagnostic module nhỏ, có item đủ thuần cho từng attribute;
- chỉ bật profile sau khi Q-matrix và classification stability đạt gate;
- nếu không đủ dữ liệu, giữ profile ở dạng nghiên cứu/diagnostic-only và nêu rõ gap.

## 4. Thuật toán đề xuất sau iteration 26

### 4.1 Hai tầng output

**Tầng A — vocabulary breadth:** dùng estimator đã mô tả trong các phần trước:

```text
V_hat = Σ_b N_b * p_hat_b
```

Trong đó `b` là frequency/domain stratum và `p_hat_b` là tỷ lệ biết đã điều chỉnh theo thiết kế. Output giữ `CI_sampling`, `sensitivity_range`, `endpoint_status` và `universe.version`.

**Tầng B — diagnostic profile:** chạy trên một subset item có Q-matrix đã version hóa. Tầng này không sửa `V_hat` và không chuyển `p_mastery` thành word count.

### 4.2 Pseudocode

```text
function run_vocabulary_test(session, universe, bands, breadth_bank, diag_bank):
    assert session.universe_version == universe.version

    breadth_responses = administer_breadth_items(session, breadth_bank)
    breadth = stratified_or_calibrated_estimate(
        breadth_responses,
        bands,
        optional_stopping_safe=true
    )

    if not diagnostic_bank_ready(
        qmatrix_version=diag_bank.qmatrix_version,
        expert_adjudication=true,
        gdi_pvaf_gate=true,
        local_dependence_gate=true,
        classification_coverage_gate=true
    ):
        profile = {"status": "unavailable", "reason": "diagnostic_bank_not_validated"}
        return breadth, profile

    diag_responses = administer_balanced_diagnostic_items(
        session,
        diag_bank,
        min_items_per_attribute=calibrated_minimum,
        max_items=diagnostic_maximum,
        exposure_control=true
    )

    posterior = fit_or_score_cdm(
        diag_responses,
        qmatrix=diag_bank.qmatrix,
        model=diag_bank.model_version,
        priors=population_priors
    )
    p_mastery = marginal_attribute_probabilities(posterior)
    profile = []
    for attribute in diag_bank.attributes:
        entropy = posterior_entropy_for_attribute(posterior, attribute)
        status = classify_with_uncertainty(
            p_mastery[attribute], entropy,
            thresholds=coverage_calibrated_thresholds
        )
        profile.append({
            "attribute": attribute,
            "p_mastery": p_mastery[attribute],
            "status": status,
            "entropy": entropy,
            "items": count_items_for(attribute),
            "qmatrix_version": diag_bank.qmatrix_version,
            "model_version": diag_bank.model_version
        })

    return breadth, {
        "status": "diagnostic",
        "attributes": profile,
        "does_not_change_breadth_count": true
    }
```

### 4.3 Offline Q-matrix build/validation pseudocode

```text
function validate_qmatrix(items, construct_spec, pilot_responses):
    q0 = expert_qmatrix(
        literature=construct_spec.literature,
        independent_experts=construct_spec.experts,
        think_aloud=construct_spec.think_aloud
    )

    candidates = gdi_pvaf_candidates(items, pilot_responses, q0)
    q1 = choose_qvectors_at_mesa_edges(candidates)
    q_final = expert_adjudicate(q0, q1, item_content=True)

    dependency = local_dependence_audit(pilot_responses, q_final)
    if dependency.severe:
        q_final = revise_or_remove_dependent_items(q_final, dependency)

    fit_suite = compare_cdm_models(
        pilot_responses,
        q_final,
        models=["DINA", "G-DINA", "ACDM", "RRUM"]
    )
    coverage = evaluate_classification_accuracy_consistency(
        fit_suite,
        repeated_forms=True,
        holdout_responses=True
    )

    return version_and_publish_only_if(
        q_final,
        fit=fit_suite.acceptable,
        coverage=coverage.calibrated,
        dependency=dependency.acceptable
    )
```

## 5. Uncertainty và validation bổ sung

Tách ba lớp sau, không gộp thành một con số:

1. **Breadth sampling/response uncertainty:** CI hoặc confidence sequence của `V_hat` theo frequency strata.
2. **Diagnostic classification uncertainty:** posterior class probabilities, marginal `p_mastery`, entropy/top-class gap và sensitivity giữa model/Q-matrix.
3. **Construct uncertainty:** liệu item có thật sự đo meaning/morphology/collocation như annotation không; đây không được che bằng posterior hẹp.

Validation tối thiểu cho diagnostic module:

- hai hoặc nhiều chuyên gia mã hóa Q-matrix độc lập; lưu bất đồng và adjudication;
- think-aloud/response-process sample để kiểm tra attribute claims;
- GDI/PVAF mesa plot theo item, không chỉ một cutoff tổng;
- item dependency audit và cluster-aware uncertainty;
- model comparison theo item nếu quan hệ attributes không đồng nhất;
- hold-out prediction, classification consistency trên alternate form và test–retest;
- calibration của `mastered/uncertain` theo attribute, không dùng accuracy tổng khi prevalence lệch;
- kiểm tra sensitivity khi thay Q-matrix/model/priors;
- kiểm tra DIF theo L1, proficiency và domain trước khi báo profile cho nhóm khác.

Các ngưỡng `p_mastery`, entropy, số item tối thiểu và hard maximum chưa có thể chọn từ nguồn ngoài một cách phổ quát. Cần pilot riêng; nếu chưa có, ghi: **chưa tìm được nguồn xác thực cho ngưỡng production của profile vocabulary này**.

## 6. Đối chiếu với Preply

| Thành phần | Thiết kế đề xuất | Preply đã xác minh được |
|---|---|---|
| Estimand chính | Breadth trên universe/version công khai, unit rõ ràng | Trang methodology từng cung cấp mô tả BNC/rebalancing/log sampling qua nguồn đã lưu, nhưng endpoint trực tiếp hiện trả 403 trong các callback |
| Diagnostic profile | Q-matrix, CDM, posterior `p_mastery`, status uncertain | Chưa có item bank/response data/Q-matrix để xác minh Preply có lớp này |
| Scoring | Profile không thay đổi `V_hat`; không cộng subskills thành words | Chưa tìm được nguồn xác thực cho lexical-subskill scoring của Preply |
| Quality gates | Expert + think-aloud + GDI/PVAF + dependency + hold-out calibration | Chưa tìm được nguồn xác thực cho các gate này của Preply |
| Uncertainty | Breadth CI/CS riêng; profile posterior và construct sensitivity riêng | Không được gán margin hoặc model từ nghiên cứu này cho Preply |
| Tail/profile | Endpoint flag và diagnostic `uncertain` khi thiếu thông tin | Chưa có routing/tail/profile data của Preply |

Kết luận đối chiếu không phải “Preply sai”, mà là **phần CDM của Preply chưa thể kiểm chứng công khai trong dữ liệu đã fetch**. Không được dùng framework CDM để điền các gap đó bằng suy đoán.

## 7. Gaps còn lại

- Chưa có Preply item bank, Q-matrix, response-level data, item exposure hoặc calibration sample.
- Chưa biết Preply có đo receptive recognition đơn thuần hay có meaning/context/morphology/collocation facets.
- Chưa có population pilot để calibrate posterior threshold, entropy cut, item quotas và classification coverage.
- Chưa có common-person/common-item linking giữa diagnostic profile và independent criterion (meaning recall, collocation task, reading/listening criterion).
- Chưa có bằng chứng cho conversion từ bất kỳ profile attribute nào sang word count; không được tạo conversion factor.
