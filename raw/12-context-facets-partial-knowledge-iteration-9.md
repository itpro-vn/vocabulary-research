# Iteration 9 — Contextual facets, partial knowledge và linking bất biến

## 1. Câu hỏi của iteration

Direction mới của iteration 9 là **context-facet invariance and partial-knowledge score linking**: kiểm tra xem vị trí item trong form, bối cảnh administration và informed guessing có làm raw vocabulary score không còn bất biến hay không; sau đó chuyển bằng chứng thành quy tắc sản xuất tách biệt giữa điểm nhanh cho người dùng và ước lượng đã calibration cho nghiên cứu.

Đây là hướng khác với các iteration trước về frequency-band sampling, CAT/IRT nói chung, criterion validity, sampling precision, estimand headword/word-family, fairness/DIF, test–retest và response-time QC. Trọng tâm lần này là nuisance/context facets và việc linking score giữa các form.

## 2. Nguồn đã kiểm tra

Các URL dưới đây đều được HTTP-verify trong callback bằng `curl -L` với browser User-Agent và trả `200` (riêng DOI được resolve tới trang nhà xuất bản):

1. Holster, T. & Lake, J. W. (2022), *Modeling vocabulary size using many-faceted Rasch measurement*, PDF trên JALT/T-EVAL: <https://teval.jalt.org/sites/default/files/26_01_01_Holster_Lake_vocab_size.pdf>.
2. Gyllstad, H., Vilkaitė, L. & Schmitt, N. (2015), *Assessing vocabulary size through multiple-choice formats: Issues with guessing and sampling rates*, DOI: <https://doi.org/10.1075/itl.166.2.04gyl>.
3. Zhang, X. (2013), *The I Don’t Know Option in the Vocabulary Size Test*, ERIC record EJ1027592: <https://eric.ed.gov/?id=EJ1027592>.
4. Stewart, J. & McLean, S. (2017), *A Response to Holster and Lake Regarding Guessing and the Rasch Model*, ERIC record EJ1129759: <https://eric.ed.gov/?id=EJ1129759>.
5. Preply, *How does the vocabulary test work?*: <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works>. Đây là bản text được fetch qua proxy vì endpoint Preply trực tiếp đã trả 403 trong các iteration trước; nội dung proxy được dùng như trang methodology đã fetch, không coi proxy là bằng chứng độc lập về production response data.

## 3. Findings đã xác minh

### 3.1 Raw percentage không tự bất biến giữa các form

Holster–Lake chỉ ra rằng các test form lấy mẫu các dải frequency khác nhau sẽ không cho raw-score estimate bất biến. Lý do không chỉ là sampling error: tồn tại các từ idiosyncratic có độ khó thực nghiệm không khớp hoàn toàn với frequency rank của corpus. Do đó một người có thể có estimate khác nhau khi làm form 5K, 14K hoặc 20K, dù năng lực thật không đổi.

Hệ quả trực tiếp: không được so sánh hai form bằng `raw_correct / n` rồi nhân cùng một constant nếu mục tiêu là đo gain hoặc so sánh cá nhân. Cần một trong các cơ chế sau:

- common-item/common-anchor equating;
- Rasch/MFRM linking sau khi kiểm tra invariance và fit;
- hoặc bảng quy đổi form-specific được xây dựng từ một mẫu overlap đủ lớn.

Điều này bổ sung cho kết luận trước đây rằng frequency band là design variable, không phải bảo đảm về item difficulty.

### 3.2 Nhiều-facet Rasch xử lý item, person và bối cảnh mà không giả định độc lập sai

Nghiên cứu phân tích dữ liệu của 1.872 sinh viên đại học Nhật Bản bằng many-faceted Rasch measurement. Các facet gồm person, item, item position và thời điểm administration. Abstract báo cáo model fit đủ để linking các loại item khác nhau và biến bối cảnh lên cùng vocabulary-size scale.

Một điểm kỹ thuật quan trọng: nếu cùng một item được trả lời ở nhiều bối cảnh, không nên nhân bản nó thành các item độc lập rồi phân tích như thể local independence vẫn đúng. MFRM coi đó là cùng một person–item interaction dưới các context facet khác nhau. Với hệ thống sản phẩm, điều này yêu cầu lưu tối thiểu `form_id`, `item_position`, `administration_context` và version của item stem.

### 3.3 Item position có effect lớn lên item difficulty nhưng nhỏ hơn SE ở person estimate

Trong dữ liệu Holster–Lake, chuyển item từ đầu form tới cuối form thường làm difficulty tăng tương đương khoảng 1.000 từ; position facet có SD khoảng 824 từ. Nếu test được sắp xếp theo frequency band, effect này có thể làm item tần suất cao ở đầu bị đánh giá dễ giả tạo và item tần suất thấp ở cuối bị đánh giá khó giả tạo. Vì vậy các nghiên cứu về quan hệ frequency–difficulty phải đưa position vào model hoặc randomized đủ tốt.

Ở cấp person estimate, sau khi đưa position facet vào, vocabulary estimate tăng trung bình khoảng 34 từ, trong khi SE được báo cáo khoảng 395 từ. Kết luận không phải là position “không tồn tại”, mà là nó thường nhỏ hơn measurement error đối với một estimate cá nhân trong dataset đó; ngược lại nó vẫn quan trọng cho item calibration, linking và phân tích cơ chế difficulty.

Quy tắc an toàn: randomize item position (hoặc giữ thiết kế cố định nhưng ghi lại position), lưu position trong response log, chạy sensitivity có/không có facet, và không dùng một threshold phổ quát cho effect này trước khi pilot trên item bank mục tiêu.

### 3.4 Logit không tuyến tính ở hai đầu và CI phải được báo trên thang sản phẩm

Holster–Lake dùng VST10 để minh họa rằng raw percentage và Rasch logit gần tuyến tính trong khoảng 25–80% nhưng phi tuyến rõ hơn ở các đầu. Calibration thực nghiệm của họ xấp xỉ 1 logit = 2.400 words trong khoảng 0–7.500 words, nhưng đây là tham số của dataset/form đó, không phải constant chung cho Preply hay mọi word universe.

Khoảng tin cậy 95% điển hình của VST10 rộng khoảng 2.500 words. Tác giả kết luận form này không đủ chính xác để đo learning gain nhỏ ở từng cá nhân, dù vẫn có thể hữu ích cho ước lượng vocabulary size nói chung. Do đó report phải có cả `estimate`, `SE/CI`, vùng calibration và cờ `not_suitable_for_small_change` thay vì chỉ hiển thị một số nguyên.

### 3.5 MCQ có thể lệch so với criterion measure và cần sampling cao hơn

Abstract của Gyllstad, Vilkaitė & Schmitt nêu hai vấn đề: multiple-choice có thể overestimate vì guessing và các chiến lược construct-irrelevant; trong case study của Vocabulary Size Test, điểm MCQ lệch so với criterion measure và sampling rate cao hơn được cần để đại diện tốt hơn cho population từ vựng.

Điểm triển khai: correction không nên được chọn chỉ vì một công thức đẹp. Cần pilot có criterion measure (ví dụ meaning recall hoặc một measure đã được chọn trước), so sánh raw score, guessing-aware score và latent score trên hold-out participants, rồi mới khóa scoring policy.

### 3.6 `I don’t know` thay đổi cả guessing lẫn biểu hiện partial knowledge

ERIC record của Zhang (2013) mô tả thí nghiệm 150 sinh viên năm nhất ở Trung Quốc, random assignment vào ba bản: VST gốc; VST có lựa chọn I-don’t-know; và VST có lựa chọn đó kèm penalty. Abstract cho biết guessing bị ảnh hưởng bởi frequency level, partial knowledge và các lựa chọn; I-don’t-know làm giảm số lần đoán nhưng đồng thời làm thay đổi việc biểu hiện partial knowledge.

Vì vậy việc thêm I-don’t-know không thể coi là một “sửa UX” trung tính. Nếu Preply-style test không có lựa chọn này, giữ informed guessing là một phần của construct hiện tại; nếu thêm vào form mới, phải coi đó là form khác và equate bằng common items/overlap data. Không được áp dụng penalty hoặc trừ điểm theo xác suất 1/k nếu chưa có criterion validation.

### 3.7 Rasch mean-square không phải bộ ước lượng tỷ lệ guessing

ERIC record của Stewart & McLean (2017) phản biện việc suy ra tỷ lệ random guesses từ average Rasch mean-square: statistic có thể gần 1 theo thiết kế, kể cả với dữ liệu hoàn toàn ngẫu nhiên. So sánh real data với random data có thể cho thấy độ tin cậy khác nhau, nhưng MSQ trung bình không cho biết bao nhiêu điểm của một người là guessing.

Production implication: dùng fit statistics cho item/person model diagnostics; không dùng một MSQ cutoff để tự động trừ điểm. Guessing/partial-knowledge nên được đánh giá qua thiết kế response/criterion riêng, hoặc được đưa vào một model đã được calibration và kiểm tra coverage trên data hold-out.

## 4. Cập nhật thuật toán đề xuất

### 4.1 Hai tầng output, một estimand được khai báo

Giữ hai output nhưng không trộn chúng:

1. **Fast product score**: nếu cần UX giống Preply, trả estimate trên đúng universe đã khai báo (ví dụ dictionary headword), dùng midpoint/log-rank estimator hiện có và làm tròn theo policy của universe. Gắn `method=midpoint_headword`.
2. **Calibrated research score**: sau khi có pilot response-level, dùng common anchors + Rasch/MFRM hoặc estimator stratified đã calibration. Gắn `method=equated_latent_or_stratified`, kèm CI, calibration version, position/context flags và quality flags.

Cả hai không được tự động quy đổi headword sang lemma/word family. Quy đổi đó cần một mapping/calibration study riêng.

### 4.2 Data model tối thiểu bổ sung

```text
Response {
  session_id, person_id, item_id, form_id,
  answer, correct, skipped, latency_ms,
  item_position, administration_context,
  universe_version, item_bank_version,
  anchor_flag
}

Calibration {
  calibration_id, model, anchor_set_version,
  item_parameters, context_facets,
  population, fit_summary, coverage_results
}
```

`item_position` không được suy ra sau khi đã mất thứ tự response. `form_id` và `universe_version` là bắt buộc để tránh so sánh score khác scale.

### 4.3 Pseudocode cập nhật

```text
function score_session(responses, mode):
    assert one_universe_version(responses)
    record_position_and_context(responses)

    if mode == "fast_midpoint":
        estimate = preply_style_midpoint(responses)
        ci = bootstrap_or_validated_product_ci(responses)
        method = "midpoint_headword"
    else:
        assert calibrated_bank_exists()
        theta, se = MFRM_or_Rasch_score(
            responses,
            facets=[item, person, form, item_position, administration_context]
        )
        estimate = map_theta_to_declared_universe(theta)
        ci = map_theta_interval_to_universe(se)
        method = "equated_context_facet"

    diagnostics = {
        "anchor_inconsistency": check_anchors(responses),
        "position_sensitivity": compare_with_position_facet(responses),
        "floor_ceiling": check_band_extremes(responses),
        "guessing_signal": separate_diagnostic_not_automatic_correction,
        "small_change_warning": ci_width_exceeds_change_threshold(ci)
    }
    return estimate, ci, method, diagnostics
```

### 4.4 Stopping và validation rule

- Không dừng chỉ vì đã tìm được midpoint; dừng khi CI width đạt product target hoặc chạm max item.
- Giữ anchor items ở các form; nếu anchor drift hoặc context-facet fit fail, trả score kèm `non_interpretable_for_comparison` thay vì giả vờ cùng scale.
- Dùng position randomization hoặc cân bằng vị trí; kiểm tra sensitivity trước khi loại bỏ facet.
- Với I-don’t-know hoặc pseudoword/guessing signal, báo diagnostic trước; chỉ correction khi policy thắng raw score trên criterion hold-out và có coverage phù hợp.
- Revalidate theo subgroup và form version; item frequency không thay thế item calibration.

## 5. Đối chiếu với Preply

| Thành phần | Preply methodology đã fetch | Quy tắc đề xuất sau iteration 9 |
|---|---|---|
| Universe | Dictionary hơn 45.000 entries, rank theo corpus BNC điều chỉnh; derived forms được gom về dictionary headwords | Giữ universe/headword là estimand riêng; khai báo version, mapping và exclusion rules |
| Sampling | Khoảng 40 item screening rộng, sau đó khoảng 120 item trong vùng hẹp; rank phân bố logarithmic | Có thể giữ midpoint cho fast score nhưng phải lưu form/position và bootstrap/validation CI |
| Score | Midpoint giữa unknown phía trước và known phía sau; làm tròn; vendor nêu margin khoảng ±10% | Không so sánh raw midpoint giữa form/context khác nhau nếu chưa common-anchor equating |
| Guessing | Methodology đã fetch giải thích sample/margin nhưng không công bố trong trang đó một model response-level cho informed guessing hoặc partial knowledge | Không tự động trừ 1/k; dùng criterion study hoặc calibrated latent model; I-don’t-know là thay đổi construct |
| Context | Trang methodology không công bố position facet, form equating hay MFRM calibration | Randomize/record position; MFRM/Rasch linking cho research score; sensitivity flags cho fast score |
| Uncertainty | Vendor-derived margin; chưa có production response data để kiểm chứng coverage độc lập | Báo CI theo calibration/version; không bê hằng số 1 logit = 2.400 words từ VST khác sang Preply |

Không có nguồn xác thực cho item bank production, response-level data, common-anchor design, position randomization, hoặc context-facet calibration của Preply trong các URL đã fetch. Đây là gap, không phải bằng chứng rằng Preply chắc chắn không có các cơ chế đó.

## 6. Gap còn lại

1. Chưa có item bank và response-level production data của Preply để ước lượng position/context effects, common-anchor stability, DIF và CI coverage.
2. Chưa có criterion dataset của người dùng mục tiêu để chọn giữa raw midpoint, guessing-aware score và latent score.
3. Chưa có hệ số quy đổi đã calibration giữa Preply headword estimate và lemma/word-family estimate.
4. Chưa có bằng chứng xác thực cho một cutoff universal của response time, MSQ, pseudoword false alarm hoặc I-don’t-know penalty.
5. Chưa có pilot để kiểm tra whether context facets materially alter individual estimates trong chính item bank Preply; không được chuyển trực tiếp các con số Holster–Lake sang sản phẩm.

Các gap này được giữ nguyên dưới dạng open research items; không có URL hay tham số nào được bịa để lấp chỗ trống.
