# Iteration 46 — Psycholinguistic item features and residual difficulty calibration

## Phạm vi

Iteration này kiểm tra một giả định dễ bị ẩn trong vocabulary-size test: frequency rank có đủ để đại diện cho item difficulty hay không. Direction mới tách ba lớp:

1. **Frequency rank** là biến thiết kế để lấy mẫu coverage.
2. **Item difficulty** là tham số cần ước lượng từ response data.
3. **Psycholinguistic features** (length, syllables, orthographic neighborhood, morphology, cognate/L1, format/context) là covariate có thể gây chênh lệch difficulty hoặc response process, nhưng không được biến thành một correction coefficient phổ quát nếu chưa có held-out calibration.

## Bằng chứng đã verify

### 1. Frequency rank không phải là predictor đủ mạnh của item difficulty

Hashimoto, *Rethinking Vocabulary Size Tests: Frequency Versus Item Difficulty*, được lưu tại BYU ScholarsArchive (HTTP 200), mô tả VAST dựa trên COCA với 403 ESL learners. Abstract báo cáo Rasch person reliability 0.96 và separation 4.62, nhưng frequency rank chỉ giải thích 22.5% phương sai item difficulty trong 501 item thuộc 5.000 từ đầu (Pearson r=0.474). Khi đối chiếu với các band 1.000 từ, tương quan giảm còn r=0.306, tương đương R²=9.4%.

Đây là kết quả của một item bank/sample cụ thể, không phải hệ số có thể chuyển nguyên sang Preply hay mọi ngôn ngữ. Hàm ý trực tiếp: band/frequency vẫn hữu ích để bảo đảm coverage và estimand, nhưng routing và uncertainty phải dựa trên item parameters đã pretest; không suy ra P(known) chỉ từ rank.

Nguồn: <https://scholarsarchive.byu.edu/etd/5958/> (HTTP 200).

### 2. Length/syllable không nên được cộng correction tự động

Koirala, *The word frequency effect on second language vocabulary learning* (EUROCALL proceedings; PDF ERIC, HTTP 200), báo cáo khảo sát 217 người học ESL nói tiếng Tây Ban Nha/Bồ Đào Nha bằng 140 từ. Thiết kế tách các nhóm frequency, word length, syllable count và consonant-cluster count; các nhóm length/syllable/cluster được giữ trong range frequency 50–500. Frequency liên hệ với perceived difficulty, nhưng khi đã kiểm soát frequency, nghiên cứu không thấy hiệu ứng rõ của các biến cấu trúc còn lại trong sample này.

Kết quả này không phủ định mọi hiệu ứng lexical feature. Nó đặt ra một cổng kiểm định: chỉ đưa một feature vào item model khi feature đó có incremental predictive value ngoài frequency trong pilot và không làm xấu calibration/validity ở hold-out. Không dùng một hệ số length/syllable lấy từ nghiên cứu khác để điều chỉnh số từ của người dùng.

Nguồn: <https://files.eric.ed.gov/fulltext/ED564187.pdf> (HTTP 200).

### 3. Pseudoword có thể bị feature confound ở response process

Yap, Sibley, Balota, Ratcliff & Rueckl phân tích dữ liệu English Lexicon Project trong bài *Responding to Nonwords in the Lexical Decision Task* (PMC full text, HTTP 200). Phân tích item-level dùng gần 37.000 nonword trials từ hơn 800 người. Nonword RT tăng theo số chữ, số orthographic neighbors, số affixes và số syllables; RT giảm theo Levenshtein orthographic distance và baseword frequency. Phân tích participant-level cho thấy vocabulary knowledge liên hệ với độ nhạy đối với một số dimension.

Hàm ý cho pseudoword controls: dùng pseudoword để phát hiện false alarm/response bias là hợp lý, nhưng phải cân bằng hoặc mô hình hóa feature của pseudoword. Không dùng RT pseudoword để cộng/trừ trực tiếp vào K_hat; nếu thu RT, đó là signal response-process/quality hoặc latent access, cần linking riêng.

Nguồn: <https://pmc.ncbi.nlm.nih.gov/articles/PMC4404174/> (HTTP 200).

### 4. Đối chiếu Preply và giới hạn xác minh

Proxy `r.jina.ai` trả HTTP 200 cho trang methodology. Nội dung công khai mô tả dictionary hơn 45.000 entries xếp theo frequency, khoảng 40 từ ở bước thăm dò, sau đó khoảng 120 từ trong vùng hẹp hơn; midpoint được tìm bằng số item biết/không biết ở hai phía và sample spacing là logarithmic. Direct Preply endpoint trả HTTP 403 trong callback.

Trang công khai không cho thấy item-level difficulty model, length/syllable/neighborhood manifest, pseudoword construction, pretest regression hoặc residual calibration. Vì vậy không thể kết luận Preply bỏ qua các feature này trong production; chỉ có thể nói chúng không được disclosed ở nguồn đã fetch. Gap này được ghi riêng trong `state/findings.jsonl`.

Nguồn proxy đã verify: <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works> (HTTP 200). Direct URL: <https://preply.com/en/learn/english/test-your-vocab/how-it-works> (HTTP 403, không dùng như nguồn nội dung).

## Quy tắc thuật toán đề xuất

### Item manifest

Mỗi lexical unit cần có tối thiểu:

```text
item_id, lexical_unit_type, target_sense, corpus_version
frequency_count, frequency_rank, frequency_band, rank_interval
n_letters, n_syllables, n_morphemes, orthographic_neighborhood
cognate_or_loanword_flags_by_L1, format, context_length, distractor_flags
pseudoword_flag, pseudoword_base_features, exposure_count, item_version
```

`frequency_band` xác định coverage/estimand; các feature còn lại là covariate và audit metadata. Nếu feature không đo được ổn định hoặc thiếu cho nhiều item, không dùng nó như correction.

### Pretest and calibration

1. Lấy mẫu item theo frequency band và bảo đảm coverage của lexical unit/sense/domain.
2. Trong mỗi band, kiểm tra balance hoặc dùng design weights cho length, syllables, morphology, neighborhood, L1/cognate và format.
3. Pretest item mới ở dạng unscored; fit Rasch/1PL hoặc model đã được chọn trước. Mô hình candidate:

\[
\operatorname{logit} P(Y_{pi}=1)=\theta_p-b_i,
\]

với sensitivity model có covariates:

\[
b_i = b_{band(i)} + \beta^T x_i + u_i,
\]

trong đó `x_i` là các feature đã prespecify và `u_i` là residual item difficulty. Đây là model calibration, không phải công thức cộng correction trực tiếp vào K_hat.

4. Chỉ giữ `x_j` nếu nó cải thiện dự báo out-of-sample và không tạo DIF/construct-irrelevant variance; so sánh model không covariate, covariate-fixed và residual model.
5. Routing dùng item parameter đã calibrate. Estimate vocabulary breadth vẫn là weighted finite-population/IRT estimate theo lexical-unit estimand; không biến `u_i` thành số từ bổ sung.

### Pseudocode

```text
manifest = load_versioned_manifest()
assert every_item_has_band_and_lexical_unit(manifest)

pilot = collect_unscored_responses(manifest.pretest_items)
base = fit_predeclared_irt(pilot, predictors=[band_or_rank])
full = fit_candidate_irt(
    pilot,
    predictors=[band_or_rank, length, syllables, morphology,
                neighborhood, cognate_L1, format_context]
)

for feature_set in [base, full, prespecified_subsets]:
    score = heldout_logloss_and_calibration(feature_set)
    dif = subgroup_dif_audit(feature_set)
    fit = item_fit_and_residual_checks(feature_set)
choose = simplest_model_with_better_heldout_calibration(
    score, dif, fit, content_validity_gate=True
)

while test_not_stopped:
    item = select_item(
        target_band=coverage_balanced_band(),
        difficulty=choose.item_parameter,
        exposure_cap=True,
        local_dependence_guard=True)
    response = administer(item)
    store(response, response_status, latency, item_version)
    update_theta_or_band_posterior(response)

K_hat = estimate_breadth_from_weighted_band_or_irt_model()
report(K_hat, response_interval, model_sensitivity, feature_sensitivity)
never_adjust_K_hat_by_raw_length_or_pseudoword_RT()
```

## Assumptions và uncertainty

- Frequency rank là thuộc tính của corpus/version, không phải universal lexical difficulty.
- Covariate coefficients are transportable only within a documented population, format and item-bank version; otherwise re-estimate.
- Tách ít nhất: response/sampling interval, IRT/model interval, frequency-manifest sensitivity và subgroup/DIF sensitivity.
- Nếu feature balance thất bại hoặc item difficulty drift theo feature, báo cáo range qua manifests thay vì một correction point estimate.
- Pseudoword false alarms có thể hỗ trợ response-bias diagnostic; chưa có bằng chứng từ các nguồn trên cho một công thức vocabulary-size correction phổ quát.

## Validation plan

1. Hold-out theo người và theo item: so sánh base-frequency model với residual-feature models.
2. Kiểm tra calibration curve, coverage của interval, item-fit và stability của `b_i` theo L1/proficiency.
3. Chạy sensitivity trên các manifest: frequency-only, frequency+balanced features và frequency+residual IRT.
4. Kiểm tra content validity trước khi bỏ item chỉ vì residual difficulty; item khó không đồng nghĩa item không hợp lệ.
5. Với pseudoword, cân bằng length/neighborhood/baseword frequency và báo cáo false-alarm rate riêng.
6. So sánh với Preply chỉ ở mức methodology: Preply midpoint/log-frequency sample là baseline mô tả; chưa được coi là cùng estimand hoặc cùng item calibration nếu không có common-person/common-item data.

## Kết luận iteration

Frequency stratification nên giữ vai trò bảo đảm coverage, nhưng item difficulty cần được pretest/calibrate và kiểm tra residual lexical-feature effects. Feature adjustment là một model-selection/validation problem, không phải bảng hệ số cố định. Đây là lớp bổ sung cho estimator hiện tại; chưa đủ dữ liệu để hiệu chỉnh trực tiếp Preply hoặc công bố một hệ số chuyển đổi chung.
