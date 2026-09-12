# Iteration 44 — Item-bank lifecycle và bảo trì parameter drift

## 1. Câu hỏi nghiên cứu

Direction của iteration này là **item-bank lifecycle and parameter-drift maintenance**: một vocabulary-size test không chỉ cần công thức `K_hat`; nó còn phải duy trì item bank qua các phiên bản, pretest item mới, phát hiện item drift, bảo vệ anchor và loại item lỗi mà không làm thay đổi thang đo âm thầm.

Các URL dưới đây đã được fetch và trả HTTP 200 trong callback:

- ETS, Li (2012), *Examining the Impact of Drifted Polytomous Anchor Items on Test Characteristic Curve (TCC) Linking and IRT True Score Equating*: https://www.ets.org/research/policy_research_reports/publications/report/2012/jewm.html
- UCAT 2021 Technical Report, Pearson VUE: https://www.ucat.ac.uk/media/1508/ucat-2021-technical-report.pdf
- Rizavi, Way, Davey & Herbert (2004), bản lưu trữ ETS, *Tolerable Variation in Item Parameter Estimates for Linear and Adaptive Computer-based Testing*: https://archive.org/stream/ERIC_EJ1110986/ERIC_EJ1110986_djvu.txt
- Preply, *How the vocab test works*, được fetch qua proxy r.jina.ai HTTP 200: https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works

Trang Preply trực tiếp trả HTTP 403 trong lần kiểm tra này; proxy chỉ xác minh được nội dung đã được trích xuất, không phải một cam kết rằng endpoint gốc luôn truy cập được.

## 2. Bằng chứng đã xác minh

### 2.1 Pretest phải tách khỏi scored item

UCAT mô tả quy trình viết item → pretest item mới cùng với item operational → phân tích item mới và item operational ở cuối testing window → chỉ đưa item đạt yêu cầu vào operational item bank. Đây là bằng chứng vận hành trực tiếp cho thiết kế vocabulary test: item mới có thể được nhúng dưới dạng **unscored pretest**, nhưng không nên đóng góp vào `K_hat` cho đến khi có calibration.

Điểm này quan trọng hơn việc chỉ kiểm tra câu hỏi có đúng ngữ pháp hay không. A vocabulary item có thể có nghĩa đúng nhưng vẫn có discrimination thấp, p-value cực đoan, clue quá mạnh, hoặc hoạt động khác nhau theo L1. Những lỗi đó cần bị phát hiện trên response data trước khi item ảnh hưởng đến estimate.

### 2.2 Retirement cần có nhiều cổng, không chỉ difficulty

Trong UCAT, cognitive item được xem xét bằng point-biserial, p-value và IRT b. Report nêu các ngưỡng ví dụ cho chương trình đó:

- operational point-biserial > 0.1;
- pretest point-biserial > 0.05;
- p-value nằm trong khoảng 0.10–0.95;
- IRT b nằm trong khoảng -3 đến 3.

Item không đạt bị retired khỏi bank; nếu sửa, có thể được dùng dưới item ID mới. Các con số trên **không được copy** sang vocabulary test vì chúng phụ thuộc construct, model, cỡ mẫu và mục tiêu sử dụng. Bằng chứng có thể chuyển là cấu trúc cổng: discrimination, difficulty, model parameter, content review và DIF nên được theo dõi riêng.

### 2.3 DIF là một cổng release/retirement riêng

UCAT cũng có bước DIF/bias review sau item analysis. Report chia item cognitive thành A/B/C; Category C được định nghĩa bằng DIF có ý nghĩa thống kê và trị tuyệt đối ít nhất 1.5, rồi item Category C bị loại khỏi bank vì có thể chứa bias. Đây không phải quy tắc universal cho vocabulary items, nhưng cho thấy item có thể bị loại dù các chỉ số difficulty/discrimination vẫn trông ổn.

Với vocabulary-size test, DIF cần được kiểm tra theo L1, proficiency band, age hoặc target population đã định trước. Nếu DIF phản ánh construct-relevant cognate advantage thì không nên tự động xoá; phải gắn nhãn, cân bằng anchor và báo cáo transportability. Nếu không giải thích được bằng nội dung/construct, item không nên nằm trong anchor hoặc scored pool.

### 2.4 Anchor drift làm hỏng equating nếu bỏ qua

ETS Li (2012) nghiên cứu common-item anchor trong IRT true-score equating. Abstract của report nêu ba kết luận trực tiếp:

1. common items phải được đánh giá item-parameter drift;
2. độ dài anchor và số anchor bị drift ảnh hưởng đáng kể đến linking/equating;
3. loại drifted anchor thường cải thiện equating, nhưng loại quá nhiều có thể làm anchor không còn giống một phiên bản thu nhỏ của hai test form.

Do đó, không được áp dụng quy tắc đơn giản “item nào drift thì xoá rồi fit lại”. Cần giữ metadata content/frequency/sense của anchor, kiểm tra anchor coverage sau khi loại, và so sánh score transformation trước/sau loại item.

### 2.5 Recalibration variation không đồng nghĩa learner growth

Bản lưu trữ ETS về repeated calibrations mô tả variation do estimation error, sample characteristics và context effects như item position/section location. Nghiên cứu báo cáo variation nhỏ trong các case linearly administered và kết quả tương tự với adaptive items, nhưng nhấn mạnh rằng context/position effects và cỡ mẫu item nhỏ vẫn có thể ảnh hưởng ability estimates.

Vì vậy, khi `K_hat` thay đổi giữa hai phiên bản, hệ thống phải tách ít nhất:

- thay đổi do người dùng/quần thể;
- thay đổi do item parameter update;
- thay đổi do anchor/equating;
- thay đổi do item content hoặc frequency-manifest;
- thay đổi do exposure/context/position.

Không nên giải thích mọi dịch chuyển score là người học tiến bộ.

### 2.6 Preply công khai phương pháp chọn mẫu, không công khai maintenance

Bản Preply được proxy trích xuất mô tả dictionary hơn 45.000 entries, rank theo frequency, khoảng 40 item ở bước rộng, sau đó khoảng 120 item ở khoảng hẹp theo logarithmic rank; midpoint được dùng để ước lượng vocabulary size. Nội dung công khai này không mô tả:

- pretest item mới;
- calibration model hoặc sample size;
- anchor/common-item design;
- parameter drift monitoring;
- retirement threshold;
- versioned equating;
- exposure/overlap control.

**Chưa tìm được nguồn xác thực cho quy trình bảo trì item-bank nội bộ của Preply.** Vì vậy bảng so sánh chỉ coi maintenance của Preply là unknown, không suy ra rằng Preply không có quy trình đó.

## 3. Quy tắc maintenance đề xuất cho vocabulary-size test

### 3.1 Data model tối thiểu

Mỗi item cần có immutable `item_id` và versioned metadata:

```text
item_id, item_version, lexical_unit, target_sense, frequency_manifest,
frequency_band, content_domain, stem_hash, distractor_manifest,
anchor_flag, pretest_flag, exposure_count, first_live_at, last_review_at,
model_version, a, b, c_or_guessing, se_a, se_b, DIF_flags,
status, retirement_reason, replacement_id
```

`item_id` không được tái sử dụng sau khi sửa nội dung. Sửa stem, target sense, distractor hoặc scoring key phải tạo `item_version` mới; nếu thay đổi đủ lớn thì tạo item ID mới. Điều này ngăn score lịch sử bị chấm lại bằng item definition hiện tại.

### 3.2 Bốn trạng thái item

- `candidate`: chỉ dùng cho content review;
- `pretest`: được đưa vào form nhưng không đóng góp trực tiếp vào score;
- `operational`: đã có calibration và đủ evidence;
- `retired`: không được route hoặc dùng làm anchor.

Có thể giữ `quarantined` như trạng thái tạm thời khi phát hiện drift/DIF nhưng chưa đủ evidence để xoá vĩnh viễn.

### 3.3 Release gate

Một item chỉ chuyển `pretest → operational` nếu tất cả điều kiện sau đạt trong pilot/pretest đã định trước:

1. response count tối thiểu đạt kế hoạch theo band và subgroup;
2. item fit/discrimination/difficulty nằm trong ngưỡng **đã calibration**, không dùng ngưỡng UCAT mặc định;
3. không có clue, lỗi key, lỗi sense hoặc context burden chưa giải quyết;
4. DIF được kiểm tra ở các nhóm có cỡ mẫu đủ;
5. item không làm mất content/frequency coverage của form;
6. score impact trong simulation và hold-out nằm trong giới hạn;
7. metadata và model version được immutable-log.

Khi thiếu cỡ mẫu, item không được “pass vì chưa thấy vấn đề”; trạng thái nên là `pretest_pending` và uncertainty phải được giữ lại.

### 3.4 Drift surveillance

Mỗi testing window hoặc batch đủ lớn, chạy ba lớp:

- **parameter drift:** so sánh `a`, `b`, guessing hoặc category probabilities với baseline, có shrinkage/SE;
- **response-function drift:** so sánh ICC/expected score ở grid năng lực chung;
- **score-impact drift:** chấm lại một tập response đại diện bằng parameter baseline và parameter mới, đo RMSE, median absolute change và tail change của `K_hat`.

Ngưỡng hành động phải được chọn bằng simulation/hold-out. Không đặt một ngưỡng b-difference phổ quát từ tài liệu khác. Có thể dùng mức cảnh báo nội bộ:

```text
green: no material ICC or K_hat impact;
amber: investigate content/context/sample and keep item out of new anchors;
red: quarantine item, exclude from equating, rerun linking and release review.
```

Các nhãn green/amber/red là workflow, không phải cut score đã được validation.

### 3.5 Anchor maintenance

Anchor phải:

- phủ các frequency bands và lexical units theo blueprint;
- không tập trung vào một sense/domain/L1;
- có exposure thấp hơn operational item thường nếu có thể;
- có lịch drift review;
- không bị thay thế đồng thời quá nhiều trong một release.

Khi một anchor bị flag:

1. chạy equating với anchor đầy đủ;
2. chạy lại với anchor bị loại;
3. kiểm tra anchor coverage và transformation;
4. so sánh `K_hat`, CI và score impact trên grid năng lực;
5. chỉ cập nhật scale nếu transformation ổn định hoặc release được đánh dấu là break-in-series.

Nếu không còn đủ anchor, không giả vờ continuity: phát hành form mới như một scale/version mới và ghi rõ không so sánh trực tiếp với phiên bản cũ.

## 4. Pseudocode

```text
function maintain_bank(window, baseline, responses):
    assert manifest_version(window) is immutable

    candidates = new_or_pretest_items(responses)
    for item in candidates:
        fit = calibrate_against_protected_anchors(item, responses)
        quality = evaluate(item, fit, content_review=True,
                           DIF_groups=registered_groups,
                           coverage_blueprint=current_blueprint)
        if quality.sample_insufficient:
            item.status = "pretest_pending"
        elif quality.fail_content or quality.fail_fit or quality.fail_DIF:
            item.status = "retired_or_quarantined"
            item.retirement_reason = quality.reasons
        else:
            item.status = "operational_candidate"

    for anchor in baseline.anchor_items:
        drift = compare_parameter_and_ICC(anchor, baseline, window)
        impact = score_impact_if_removed(anchor, responses, baseline)
        if drift.material or impact.material:
            anchor.status = "quarantined"
            anchor.anchor_eligible = False

    anchor_set = choose_content_balanced_nonquarantined_anchors(baseline, window)
    if not anchor_set.meets_coverage:
        return release_blocked("insufficient stable anchors")

    link_full = equate(window, anchors=baseline.anchor_items)
    link_clean = equate(window, anchors=anchor_set)
    sensitivity = compare(link_full, link_clean, target="K_hat_and_CI")

    if sensitivity.material:
        return release_blocked("parameter/anchor drift changes reported scale")
    if any(item.status == "operational_candidate" and
           not item.holdout_validated for item in candidates):
        return release_blocked("new item lacks holdout evidence")

    publish_version(window, link_clean, metadata=full_audit_log)
```

## 5. So sánh với Preply

| Thành phần | Preply công khai | Thiết kế đề xuất |
|---|---|---|
| Universe | hơn 45.000 dictionary entries, frequency-ranked | versioned lexical universe + frequency manifest |
| Sampling | bước rộng khoảng 40, bước hẹp khoảng 120, logarithmic rank | stratified/adaptive form với pretest và content balance |
| Estimand | vendor midpoint vocabulary count | `K_hat` theo lexical unit đã khai báo, có CI và version |
| New items | chưa thấy công khai | pretest unscored trước khi operational |
| Calibration | chưa thấy công khai | IRT/response model, hold-out và simulation |
| Drift | chưa thấy công khai | parameter, ICC và score-impact surveillance |
| Anchor/equating | chưa thấy công khai | protected common anchors, drift exclusion sensitivity |
| Retirement/DIF | chưa thấy công khai | content, fit, DIF và exposure gates |
| Continuity | chưa xác minh | release manifest + explicit break-in-series nếu anchor không đủ |

Bảng này không nói Preply không thực hiện các bước chưa công khai; chỉ nói rằng các bước đó chưa có nguồn công khai đã xác minh trong iteration này.

## 6. Validation plan

1. Tạo pilot item bank có frequency bands, lexical unit, sense, L1 và domain metadata.
2. Nhúng item pretest ngẫu nhiên có kiểm soát vào form operational; log exposure, position và response status.
3. Calibrate item mới trên protected anchor; chia calibration/hold-out theo người dùng, không chỉ theo response.
4. Mô phỏng drift do sample shift, context shift, exposure và nội dung thay đổi; đo bias của `K_hat`, CI coverage và false retirement.
5. So sánh bốn release: không maintenance, chỉ refit, drift-aware anchors, drift-aware + score-impact gate.
6. Kiểm tra anchor-set sensitivity bằng cách tạo nhiều anchor sets content-balanced; không dùng một anchor set thuận tiện duy nhất.
7. Với mỗi release, báo cáo: item pass/retire/quarantine, lý do, parameter change, DIF status, equating transformation, score-change distribution và break-in-series decision.
8. Chỉ sau khi hold-out cho thấy coverage/continuity đạt mục tiêu mới đặt các ngưỡng sản xuất cụ thể.

## 7. Gaps

- Không có response-level data hoặc item bank của Preply để kiểm tra item drift, exposure, pretest hay anchor.
- Chưa có dữ liệu để chọn cỡ mẫu calibration, drift threshold, anchor rate hoặc score-impact threshold riêng cho vocabulary-size test.
- Các ngưỡng UCAT là ví dụ của một chương trình khác, không được chuyển nguyên sang production.
- Chưa tìm được nguồn xác thực cho quy trình bảo trì item-bank nội bộ của Preply.
