# Iteration 50 — Cross-lingual adaptation và calibration theo ngôn ngữ

## 1. Phạm vi và câu hỏi

Iteration này nghiên cứu cách chuyển một vocabulary-size test sang nhóm ngôn ngữ/L1 khác mà không mặc định rằng bản dịch giữ nguyên construct, item difficulty hoặc thang điểm của bản English. Trọng tâm là:

- equivalence ngôn ngữ và văn hóa;
- thiết kế option bằng L1 để giảm language burden nhưng không tạo cue mới;
- cognate/loanword exposure;
- calibration riêng cho bản localized;
- item-level DIF, option/distractor QA và điều kiện được phép lập common scale.

Đây là lớp bổ sung cho thuật toán breadth hiện tại. Nó không thay thế frequency-stratified estimator, Rasch/CAT, common anchors, hoặc uncertainty layer.

## 2. Nguồn đã fetch và verify

Các URL dưới đây đã được gọi trực tiếp bằng browser user-agent và đều trả HTTP 200 trong iteration:

1. International Test Commission, *ITC Guidelines for Translating and Adapting Tests* (PDF): <https://www.intestcom.org/files/guideline_test_adaptation.pdf>
2. Park (2024), *Validation of the Korean Bilingual Version of the Vocabulary Size Test*, English Teaching 79(2), 139–162 (ERIC full-text PDF): <https://files.eric.ed.gov/fulltext/EJ1434340.pdf>
3. Carcamo (2022), *A Bilingual Version of the Vocabulary Size Test for Spanish Speakers*, International Journal of Language Testing 12(2) (ERIC full-text PDF): <https://files.eric.ed.gov/fulltext/EJ1363638.pdf>
4. Aizawa (2024), *The Impact of Loanwords on the English–Japanese Version of Vocabulary Size Test*, Vocabulary Learning and Instruction 13(1) (ERIC full-text PDF): <https://files.eric.ed.gov/fulltext/EJ1437990.pdf>
5. Kurnaz-Adıbatmaz & Yıldız (2020), *The Effects of Distractors to Differential Item Functioning in Peabody Picture Vocabulary Test* (ERIC full-text PDF): <https://files.eric.ed.gov/fulltext/EJ1288697.pdf>

Các kết quả Korean/Japanese là nghiên cứu theo population cụ thể; không được dùng như tham số chung cho mọi L1.

## 3. Bằng chứng chính

### 3.1. Translation là một quy trình equivalence, không phải thay từ

ITC mô tả mục tiêu của adaptation là thiết lập score equivalence giữa các nhóm ngôn ngữ/văn hóa. Bản hướng dẫn yêu cầu:

- đánh giá phần construct giao nhau giữa các population;
- tính đến khác biệt ngôn ngữ-văn hóa;
- chứng minh directions, rubrics, items và handbook phù hợp;
- kiểm tra format, quy ước làm bài và stimulus có quen thuộc hay không;
- dùng systematic judgmental evidence về cả ngôn ngữ và tâm lý;
- thiết kế data collection để có thể kiểm tra item equivalence;
- cung cấp validity evidence trong từng target population.

ITC cũng nêu rằng item không tương đương giữa các phiên bản không được dùng để lập common scale hoặc so sánh population. Item đó vẫn có thể hữu ích cho content validity riêng của một population. Đây là nguyên tắc release quan trọng: “đã dịch xong” không đồng nghĩa “được phép so sánh điểm”.

**Hệ quả:** manifest phải có `language_variant`, `translation_version`, `translator_review_status`, `item_equivalence_status` và `common_scale_eligibility`. Mỗi assertion rằng hai L1 có cùng K_hat phải dựa trên bằng chứng invariance/equivalence, không dựa vào cùng một English answer key.

### 3.2. Bản bilingual VST phải validate độc lập

Park (2024) validation một Korean bilingual VST 70 item bằng Rasch và nhấn mạnh validity là thuộc tính của score trong mục đích, population và context cụ thể; không thể lấy validity của bản English hoặc một nghiên cứu khác làm giấy phép cho bản đổi ngôn ngữ/rút gọn.

Trong sample nghiên cứu, person ability nằm khoảng 0.37–2.66 logits, còn item difficulty khoảng -4.30–3.74 logits. Có 37/70 item nằm dưới người có ability thấp nhất; test quá dễ và person separation chỉ 1.29. Item separation là 3.27, tức chỉ tạo khoảng ba strata difficulty thống kê dù item được gắn với 14 BNC frequency levels. Đây là failure của targeting/discrimination trong population đó, không phải lỗi có thể sửa bằng cách nhân raw score với 100.

**Quy tắc:** localized form phải có calibration riêng, Wright map/person-item targeting, reliability/separation, fit, dimensionality, local-dependence và external validity. Không tái sử dụng trực tiếp bảng `raw correct × 100` hoặc logistic mapping của bản English/Preply trước khi kiểm tra linking.

### 3.3. Frequency bands của native corpus không nhất thiết là difficulty order của EFL population

Park báo cáo item difficulty Korean VST không giảm đều qua 14 BNC levels. Gom level thành 5 cluster làm pattern rõ hơn nhưng vẫn không hoàn hảo. 11 English loanwords được nhận diện là dễ hơn so với item cùng band; bỏ các item này làm tương quan frequency-level với item difficulty chỉ tăng từ `r = .43` lên `r = .52`.

Tác giả liên hệ sự lệch này với loanwords và curriculum English ở Hàn Quốc, nơi người học có thể được dạy nhiều từ academic/low-frequency hơn so với xác suất gặp từ trong native-speaker BNC. Kết luận không phải “BNC vô dụng”, mà là frequency rank là proxy phụ thuộc population và context.

**Quy tắc:** localized manifest phải lưu `frequency_source`, `corpus_version`, `target_population_exposure` và `band_difficulty_diagnostic`. Nếu band order sai lặp lại trên hold-out, phải dùng cluster band, đổi corpus/blueprint, hoặc báo population-specific scale; không ép mọi item ở band `b` có trọng số 100 như nhau.

### 3.4. Loanword/cognate và bản dịch option có thể làm score inflation

Aizawa (2024) nghiên cứu 134 sinh viên L1 Nhật trên English–Japanese VST. Ba chuyên gia xác định 47/140 target items (33.6%) là loanwords; Fleiss’ kappa chỉ `0.55` với 95% CI `[.46, .65]`, cho thấy việc phân loại loanword không hoàn toàn khách quan.

Tỷ lệ đúng loanword là `83.9%`, so với `49.9%` ở non-loanword; paired test báo `t(125)=26.0`, `p<.001`, `r=.85`. Trong nhóm loanword, item có đáp án đúng viết bằng loanword đạt `94.2%`, so với `79.7%` khi đáp án đúng là Japanese-word; `t(125)=18.3`, `p<.001`, `r=.85`.

Đây là bằng chứng rất mạnh cho việc tách `loanword_status`, `option_script/form` và L1 trong item analysis. Loanword không nhất thiết phải xóa: nếu mục tiêu là receptive knowledge trong thế giới sử dụng thật, chúng có thể là construct-relevant. Nhưng tỷ lệ loanword phải được kiểm soát/cân bằng theo target L1, và không được diễn giải score như cùng một latent scale nếu một L1 hưởng lợi nhiều hơn từ form–meaning overlap.

### 3.5. Quy trình dịch tốt cần nhiều người, pilot nhận thức và kiểm tra thống kê

Carcamo (2022) tổng hợp các bilingual VST trước đó. Với Vietnamese VST, quy trình được mô tả là một giáo viên bản ngữ Việt dịch các option, giáo viên thứ hai đọc và sửa, sau đó cả hai rà soát accuracy/intelligibility; 62 sinh viên được chia thành beginner/intermediate/advanced để kiểm tra khả năng phân biệt. Persian version dùng hội đồng năm chuyên gia bản ngữ đã tốt nghiệp chương trình English và pilot 10 sinh viên để phát hiện ambiguity.

Các ví dụ này không phải tiêu chuẩn đủ cho production, nhưng cho thấy hai lớp bằng chứng cần tách:

1. **linguistic/cognitive review:** closest equivalent thay vì word-by-word, nghĩa và độ dễ hiểu của option, ambiguity, cultural familiarity;
2. **empirical validation:** group discrimination, band/difficulty pattern, dimensionality, DIF, reliability và external criterion.

Một bài PPVT độc lập của Kurnaz-Adıbatmaz & Yıldız (2020) cho thấy việc thay đổi distractor/format có thể làm kết quả DIF phụ thuộc phương pháp: logistic regression phát hiện 15 item, Lord chi-square 9 item, nhưng chỉ 5 item cho kết quả lặp lại giữa các form 3/4 lựa chọn. Kết quả này trên trẻ em và PPVT, không phải benchmark cho VST người lớn; nó chỉ hỗ trợ release rule rằng distractor/option phải được kiểm tra riêng, bằng nhiều phương pháp và trên hold-out.

## 4. Thuật toán localized-form đề xuất

### 4.1. Data model bổ sung

```text
LocalizedVariant {
  variant_id
  base_universe_id
  target_language
  target_population
  translation_version
  translators_and_reviewers
  adaptation_log
  corpus_id
  loanword_annotation_version
  calibration_version
  common_scale_status: pending | linked | separate
}

LocalizedItem {
  item_id
  base_item_id
  target_word_unchanged
  stem_version
  option_text
  option_semantic_equivalence
  option_script_or_loanword_status
  translator_review_status
  cognitive_pilot_status
  calibration_difficulty
  calibration_discrimination
  DIF_flags
  band_order_flag
  common_anchor_status
  release_status: pass | review | fail
}
```

### 4.2. Release gates

Một variant chỉ được link vào English/Preply scale khi tất cả điều kiện sau đạt:

1. **Content gate:** target lexical unit, sense, POS, frequency universe và scoring rule giữ nguyên hoặc thay đổi đã ghi version.
2. **Language gate:** có ít nhất review đa người; option dùng closest semantic equivalent, không dịch máy không kiểm tra; pilot nhận thức không còn ambiguity nghiêm trọng.
3. **Loanword gate:** loanword/cognate status và option form được annotate; tỷ lệ/exposure được báo theo L1; sensitivity có/không có nhóm item này.
4. **Psychometric gate:** item fit, dimensionality, local dependence, monotonicity/band diagnostic và DIF được chạy trong target population.
5. **Anchor gate:** common anchors đạt invariance đủ cho mục đích linking; item không tương đương bị loại khỏi common scale, không âm thầm sửa score.
6. **External gate:** localized score có quan hệ hợp lý với criterion độc lập trong target population; không tuyên bố CEFR/proficiency chỉ vì điểm VST tăng.
7. **Uncertainty gate:** CI/SE bao gồm response/sampling uncertainty và một sensitivity range cho translation/loanword/exclusion decisions.

Nếu gate 4–6 chưa đạt, variant ở trạng thái `separate`: báo điểm trên scale localized đã định nghĩa, không so sánh số học với English/Preply. Nếu chỉ có evidence ngôn ngữ nhưng chưa có response data, trạng thái là `pending`, không phải `linked`.

### 4.3. Pseudocode

```text
function build_localized_variant(base_bank, target_language, target_population):
    draft = translate_options_with_independent_review(base_bank, target_language)
    annotate_semantic_equivalence(draft)
    annotate_loanwords_and_cognates(draft, target_language)
    cognitive_results = pilot_interviews_and_comprehension_check(draft)
    revise_or_flag(draft, cognitive_results)

    calibration, holdout = split_target_population_data()
    fit_group_models(calibration, groups=[target_population, L1, proficiency])
    run_dimensionality_and_local_dependence_checks(calibration)
    run_item_fit_and_monotonicity_by_band(calibration)
    run_DIF_and_option_functioning(calibration)
    repeat_critical_checks(holdout)

    anchors = select_common_anchors(base_bank, draft)
    link_result = test_anchor_invariance(anchors, calibration)

    if content_gate_fail or cognitive_gate_fail:
        return status='fail', reason='content_or_language'
    if repeated_DIF_or_non_equivalence(holdout):
        return status='separate', reason='not_common_scale_eligible'
    if not link_result.pass:
        return status='separate', reason='anchor_linking_failed'
    if not external_validity_and_uncertainty_gate_pass:
        return status='pending', reason='insufficient_validation'

    freeze_version(draft, calibration_version, audit_log=True)
    return status='linked', score_mapping=validated_mapping,
           sensitivity=loanword_and_translation_sensitivity,
           uncertainty=validated_CI
```

### 4.4. Scoring và uncertainty

Khi variant đã linked, dùng mapping đã calibration:

```text
K_hat_variant = g_variant(theta_hat)
CI_variant = [g_variant(theta_low), g_variant(theta_high)]
```

`g_variant` chỉ được coi là cùng `g_english` sau khi common-anchor/linking và invariance pass. Nếu không, dùng `g_variant` riêng trên lexical universe đã định nghĩa.

Báo cáo nên tách:

```text
CI_response_or_sampling
CI_model_or_linking
sensitivity_translation = range(K_hat under approved option variants)
sensitivity_loanword = range(K_hat with annotated loanword policy)
transport_gap = not_identified_until_target_population_validation
```

Không gộp sensitivity do translation vào một “±10%” cố định. Không dùng số liệu Korean/Japanese để tự sinh margin cho Vietnamese hoặc Preply.

## 5. Đối chiếu với Preply

| Thành phần | Preply public methodology đã có trong state/report | Localized-form recommendation |
|---|---|---|
| Universe | Headword-oriented user-facing estimate; không đồng nhất với word-family VST | Khai báo lexical unit và giữ riêng scale headword/family |
| Sampling | Screening và narrow logarithmic/midpoint logic theo tài liệu vendor đã fetch trước đó | Giữ sampling target nhưng thêm variant-specific calibration và anchors |
| Translation | Chưa tìm được nguồn xác thực cho production localized forms, translator workflow, L1 DIF hoặc loanword policy của Preply | Bắt buộc translation log, cognitive pilot, loanword annotation và DIF/option QA |
| Score mapping | Vendor-stated mapping/margin không chứng minh equivalence xuyên ngôn ngữ | Chỉ link mapping khi anchors/invariance/hold-out đạt; nếu không báo scale riêng |
| Frequency | Frequency/rank là proxy của universe, không mặc định là difficulty invariant | Kiểm tra band order theo target population; lưu corpus/context metadata |
| Uncertainty | Không có response-level data để kiểm chứng margin theo từng L1 | Báo CI + model/linking + translation/loanword sensitivity; không bịa margin |

Vì production item bank và response-level data của Preply chưa công khai trong các nguồn đã kiểm tra, **chưa tìm được nguồn xác thực cho việc Preply đã triển khai các gate localized-form nêu trên**. Không được ghi rằng Preply có hoặc không có DIF nếu không có dữ liệu item/response; chỉ có thể nói disclosure hiện có chưa đủ để xác minh.

## 6. Validation plan tiếp theo

1. Khóa một base universe, lexical unit, frequency manifest và English form version.
2. Chọn một target L1 cụ thể; không gộp nhiều L1 trong pilot đầu.
3. Dịch option bằng quy trình hai người/committee, lưu mọi thay đổi và lý do.
4. Chạy cognitive pilot; mã hóa ambiguity, semantic mismatch, reading burden và option cue.
5. Thu response data trên target population đủ đa dạng proficiency; chia calibration/hold-out theo người.
6. Fit base/variant models, kiểm tra anchors, DIF, option functioning, band order, local dependence và person-item targeting.
7. So sánh linked K_hat với full-form/direct criterion; bootstrap hoặc replicate để đánh giá coverage của CI.
8. Công bố variant như `linked`, `separate` hoặc `pending`, kèm population, corpus, translation version, calibration date và sensitivity range.

## 7. Gaps

- Chưa có item bank và response-level production data của Preply để kiểm tra bản localized, common anchors, DIF hay loanword policy.
- Chưa có dữ liệu để chọn ngưỡng DIF, số anchor, cỡ calibration, margin hoặc criterion linking cho một target L1 cụ thể.
- Bằng chứng Japanese loanword có sample L1-specific và expert agreement trung bình; không chuyển trực tiếp sang L1 khác.
- Bằng chứng PPVT distractor là population/test khác; chỉ là cảnh báo QA, không phải tham số VST.
- Chưa tìm được nguồn xác thực cho một quy trình translation/adaptation riêng của Preply.
