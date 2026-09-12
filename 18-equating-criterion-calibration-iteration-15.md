# 18. Iteration 15: equating, criterion linking và calibration ngoài

## Phạm vi

Iteration này tách ba việc thường bị gọi lẫn là “calibration”:

1. **Equating giữa các form của cùng một test**: đưa điểm form A và B về cùng thang đo khi chúng đo cùng construct.
2. **Criterion linking/prediction**: liên hệ vocabulary-size score với reading, IELTS/TOEFL hoặc CEFR; đây không phải equating nếu hai bài đo không cùng construct và không có thiết kế đo chung.
3. **Validation của diễn giải điểm**: kiểm tra content, internal structure, criterion-related validity, response process và hệ quả của việc dùng điểm.

Nguồn được fetch và kiểm tra HTTP trước khi dùng: ETS *Equating Test Scores (without IRT), 2nd ed.* (HTTP 200), bài nghiên cứu Vocabulary Levels Test–reading comprehension (HTTP 200), và ETS *TOEFL iBT Technical Manual* (HTTP 200). Trang Council of Europe trong iteration này trả HTTP 403 nên không được dùng làm nguồn trích dẫn mới.

## 18.1 Equating không phải prediction

ETS mô tả equating là phép biến đổi điểm **đối xứng ở cấp quần thể** để điểm trên các form khác nhau có thể so sánh. Equating không nhằm dự đoán điểm form B của đúng cá nhân đã làm form A. Vì vậy:

- Một hàm hồi quy từ vocabulary-size estimate sang IELTS/TOEFL/CEFR là **criterion linking hoặc prediction**, không nên gọi là equating.
- Sai số của linking (sai số dự đoán, sai số calibration và transport error) phải tách khỏi sampling/response SE của vocabulary test.
- Chỉ gọi là alternate-form equating khi hai form đo cùng vocabulary construct, cùng unit/universe và có thiết kế common-item hoặc equivalent-groups phù hợp.

Nguồn: [Livingston, ETS — Equating Test Scores (without IRT), 2nd ed.](https://www.ets.org/Media/Research/pdf/LIVINGSTON2ed.pdf), phần phân biệt equating và prediction, khoảng trang 10–11 của tài liệu PDF.

## 18.2 Common-anchor design cho alternate forms

Anchor tốt nhất đo cùng knowledge/skills và gần cùng format với test. Với internal anchor, một tập câu hỏi của form chuẩn được lặp lại ở form mới. Giả định cốt lõi là cùng một điểm anchor có cùng ý nghĩa đối với người làm form chuẩn và form mới; nếu item bị lộ, bị sửa hoặc chịu hiệu ứng vị trí, độ khó có thể đổi.

Quy tắc sản xuất cho vocabulary test:

- Anchor phải thuộc cùng vocabulary universe/version, unit (headword, lemma hoặc word-family), frequency-band manifest và format.
- Không sửa stem, target, distractor hay answer key của anchor giữa các form. Nếu cần sửa, bỏ item đó khỏi equating set và thay bằng item mới đã calibration.
- Giữ vị trí tương đối gần nhau giữa các form; tránh chuyển anchor từ đầu sang cuối hoặc ngược lại.
- Trước linking, vẽ difficulty plot theo percent-correct của hai nhóm/form; item lệch khỏi mẫu chung phải được review và có thể loại khỏi anchor.
- Anchor phải đủ rộng để kiểm tra drift; một test rất ngắn với chỉ vài anchor không nên tuyên bố alternate-form equivalence mạnh.
- Anchor có thể gây security exposure; dùng exposure cap, không công bố anchor, và theo dõi repeat-attempt contamination.

Nguồn: [Livingston, ETS](https://www.ets.org/Media/Research/pdf/LIVINGSTON2ed.pdf), phần “The external-anchor design” và “The key assumption of the internal-anchor design”, khoảng trang 29–33.

## 18.3 Tiêu chí chọn anchor có thể kiểm thử

ETS nêu các hướng dẫn thực hành sau cho common items:

| Tiêu chí | Quy tắc áp dụng cho vocab-size test |
|---|---|
| Số lượng | ETS thường thích ít nhất 20 common items cho test dài; đây là tham chiếu thiết kế, không phải ngưỡng phổ quát. Chọn số lượng bằng mô phỏng precision và drift detection. |
| Đại diện | Tỷ lệ content/format/frequency band của anchor nên gần toàn test; không gom anchor ở band dễ hoặc khó. |
| Tính bất biến | Không dùng item bị thay đổi nội dung, item đã public hoặc item có evidence bị học thuộc. |
| Item-set/context | Nếu item phụ thuộc cùng context, tránh phá vỡ set; với vocabulary MCQ, kiểm tra stem cue và distractor context. |
| Vị trí | Giữ vị trí tương đối; vị trí quá khác có thể tạo fatigue/time-pressure effect. |
| Dải độ khó | Bao phủ cả low và high ability; nếu thiếu đuôi khó, linking có thể sai ở nhóm advanced. |
| Thời gian | Hạn chế item ở cuối bài khi có time pressure. |
| Thông tin | Tương quan với tổng điểm có ích nhưng đứng sau tính đại diện của construct/content. |

Đây là QA checklist, không phải tuyên bố rằng 20 item đủ cho test vocab. Cần chọn anchor sau pilot bằng coverage, standard error, DIF và drift simulation.

Nguồn: [Livingston, ETS](https://www.ets.org/Media/Research/pdf/LIVINGSTON2ed.pdf), “Selecting Common Items for an Internal Anchor”, khoảng trang 36–37.

## 18.4 Criterion evidence: vocabulary breadth liên hệ reading nhưng không phải toàn năng lực

Bài nghiên cứu trên 129 sinh viên pre-university tại International Islamic University Malaysia dùng Vocabulary Levels Test và phần reading của một English Proficiency Test. Kết quả được báo cáo là Pearson `r = 0.641`, `p < 0.01`, giữa hai điểm. Trong mẫu này, 100% đạt yêu cầu đọc đầu vào Band 5.5, nhưng chỉ 54.3% đạt mastery ở band 5,000 từ.

Diễn giải an toàn:

- Kết quả ủng hộ criterion-related association giữa receptive vocabulary breadth và reading trong **một mẫu, một bài VLT và một bài EPT**.
- Nó không cung cấp conversion function chung từ số lượng từ sang IELTS/TOEFL/CEFR.
- Tương quan không đồng nghĩa với interchangeable scores; reading còn phụ thuộc grammar, background knowledge, text/domain và chiến lược đọc.
- Calibration study của sản phẩm phải lấy mẫu đúng population/use case, đo criterion độc lập, giữ hold-out sample và báo confidence/prediction interval.

Nguồn: [The Relationship between Vocabulary Size and Reading Comprehension](https://files.eric.ed.gov/fulltext/EJ1095578.pdf), abstract và phần Participants/Procedure (HTTP 200).

## 18.5 CEFR/proficiency linking cần chuỗi bằng chứng

Technical Manual TOEFL là ví dụ chính thống về cách một chương trình proficiency test xây dựng mapping sang CEFR. Manual ghi nhận:

- Reading/listening dùng field-test questions đã có mapping ở các ETS language tests khác.
- Item nằm giữa hai CEFR level được chuyên gia kiểm tra về skills/descriptors.
- Speaking/writing dùng đối chiếu task/rubric với CEFR descriptors, standard setting bằng performance profiles, rồi kiểm tra thống kê giữa các section trên cùng người thi.
- Thang điểm và mapping được thiết kế để nhất quán giữa các test forms.

Bài học cho vocabulary-size product: không lấy một bảng “X từ = B2” từ nguồn ngoài rồi gắn nhãn CEFR. Nếu muốn hiển thị CEFR, cần một nghiên cứu linking riêng, gồm construct alignment, expert review/standard setting phù hợp và kiểm tra empirical trên sample độc lập. Nếu chưa có, UI chỉ nên nói “ước lượng vocabulary breadth” và để CEFR ở dạng nghiên cứu thăm dò hoặc bỏ hẳn.

Nguồn: [TOEFL iBT Technical Manual](https://files.eric.ed.gov/fulltext/EJ1487502.pdf), phần III-4, khoảng trang 38–39.

## 18.6 Cỡ mẫu calibration và staged validity program

TOEFL manual mô tả field test trên population tương tự operational population, đủ lớn để có question statistics ổn định (`N ≈ 5,000`), và phủ toàn dải CEFR. Con số này là ví dụ của một chương trình proficiency lớn, **không phải cỡ mẫu có thể bê nguyên** cho vocabulary-size MVP.

Manual cũng trình bày validity như một chương trình gồm content validity, internal structure, criterion-related validity, response processes và consequential validity; các claim cần warrants, evidence và rebuttals, được bổ sung khi test chuyển từ development sang operational use.

Kế hoạch tối thiểu cho sản phẩm:

1. **Calibration sample**: tuyển người theo proficiency/L1/domain mục tiêu; lưu response-level data và metadata tối thiểu.
2. **Item calibration**: ước lượng difficulty/discrimination, distractor functioning, frequency-band monotonicity, DIF và local dependence.
3. **Form linking**: phát common anchors hoặc equivalent-groups; ước lượng link trên calibration sample và đánh giá drift trên mẫu mới.
4. **Criterion study**: thu reading comprehension/coverage và, nếu claim rộng hơn, các skill khác; không coi một criterion đơn lẻ là gold tuyệt đối.
5. **Hold-out evaluation**: khóa model/universe version trước khi đánh giá; báo bias, MAE/RMSE, correlation, calibration curve và prediction interval coverage.
6. **Use validation**: kiểm tra false-positive/false-negative quanh các ngưỡng hành động; không chuyển correlation thành decision cut score nếu chưa có standard-setting.

Nguồn: [TOEFL iBT Technical Manual](https://files.eric.ed.gov/fulltext/EJ1487502.pdf), phần thiết kế field test khoảng trang 7–8 và phần Validity/Fairness khoảng trang 47–48.

## 18.7 Thay đổi đề xuất cho thuật toán và báo cáo

### Contract điểm

Kết quả mặc định:

```text
estimate = vocabulary breadth trên universe/version đã công bố
CI_response_or_sampling = uncertainty do item/response
sensitivity_range = thay đổi do unit, list, domain và exclusion rules
quality_flags = anchors, speed, missingness, DIF/exposure, floor/ceiling
```

Nếu có criterion linking:

```text
criterion_estimate = f(estimate, covariates)
prediction_interval = PI(f, calibration_error, residual_error)
linking_method = regression | equipercentile | IRT/common-anchor
population = calibration_population
```

`criterion_estimate` không được thay thế `estimate`, và UI phải ghi population/criterion mà mapping có hiệu lực.

### Pseudocode bổ sung

```text
function link_or_equate(form_result, mode, calibration):
    assert form_result.universe_version == calibration.universe_version

    if mode == "alternate_form_equating":
        require calibration.common_anchor_design or calibration.equivalent_groups
        require same_construct_unit_and_format(calibration)
        drift = difficulty_plot_and_anchor_fit(calibration)
        anchors = remove_changed_or_exposed_items(calibration.anchors, drift)
        scale_result = fit_link(form_result, anchors, method="Rasch_or_equipercenile")
        return scale_result, interval_with_linking_error(scale_result)

    if mode == "criterion_linking":
        require calibration.external_criterion
        require calibration.target_population_and_holdout
        fit = fit_pre_registered_link_model(calibration.train)
        validate(fit, calibration.holdout,
                 metrics=[bias, MAE, RMSE, correlation, PI_coverage])
        return predict_with_interval(fit, form_result), "not_equating"

    return form_result, "vocabulary_breadth_only"
```

## 18.8 Kết luận iteration và gaps

Kết luận mới: alternate forms cần common-anchor/equivalent-groups evidence và kiểm tra drift; mapping sang CEFR hoặc IELTS là criterion linking cần calibration/hold-out riêng, không suy ra từ raw word count. Nghiên cứu Malaysia cung cấp association reading–VLT nhưng không đủ cho conversion phổ quát. TOEFL cung cấp một blueprint đáng tham khảo về field calibration và staged validity, không cung cấp tham số cho Preply.

Gaps còn lại:

- Không có item bank/response-level data production của Preply.
- Không có common anchors, routing logs hoặc calibration sample của Preply để kiểm tra score linking.
- Chưa có dữ liệu độc lập để ước lượng conversion headword ↔ lemma/word-family hoặc vocab breadth ↔ CEFR/IELTS.
- Chưa có mẫu criterion đa dạng L1/proficiency/domain và hold-out để đánh giá prediction interval coverage.
- Chưa có ngưỡng anchor count, sample size, drift flag hay CEFR cut score đã được calibration cho sản phẩm.
