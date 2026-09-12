# Iteration 41 — dimensionality and construct separation

## Phạm vi

Iteration này kiểm tra một câu hỏi trước khi fit IRT hoặc chuyển điểm thành số từ: bài test đang đo **một latent trait** hay nhiều thành phần liên quan nhưng phân biệt được? Trọng tâm là receptive written vocabulary size/breadth, lexical depth, accessibility và modality. Nếu các thành phần bị trộn, một word count duy nhất có thể có diễn giải sai dù độ tin cậy hoặc tương quan tổng thể cao.

## Nguồn và trạng thái kiểm tra

Các URL sau được fetch bằng `curl -L` với browser User-Agent trong callback và trả HTTP 200:

1. Koizumi & In’nami (2020), *Structural Equation Modeling of Vocabulary Size and Depth Using Conventional and Bayesian Methods*, Frontiers in Psychology: <https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00618/full>
2. Agdam et al. (2014), *Assessing the Dimensionality of Word Knowledge in Different Formats*, ERIC PDF: <https://files.eric.ed.gov/fulltext/EJ1075954.pdf>
3. Cook, Dorans, Eignor & Petersen (1985), ETS RR-85-30, *An Assessment of the Relationship Between the Assumption of Unidimensionality and the Quality of IRT True-Score Equating*: <https://www.ets.org/research/policy_research_reports/publications/report/1985/ihpg.html>
4. Zhang (2004), ETS RR-04-44, *Comparison of Unidimensional and Multidimensional Approaches to IRT Parameter Estimation*: <https://www.ets.org/research/policy_research_reports/publications/report/2004/hyzi.html>

Các URL SAGE/ERIC của Ishii & Schmitt được search như lead nhưng không dùng làm bằng chứng: SAGE trả 403, ERIC metadata không trả được, và đường dẫn PDF đoán được trả 404. Preply direct page cũng trả 403 trong callback; không coi nó là nguồn đã xác minh.

## Bằng chứng chính

### 1. Size và depth có thể rất tương quan nhưng vẫn là hai construct

Koizumi & In’nami nghiên cứu 255 người học Nhật tiếng Anh bằng năm bài vocabulary:

- một bài đo vocabulary size, chia thành ba indicator theo frequency;
- bốn bài đo depth, gồm association, polysemy và collocation;
- các bài dùng format multiple-choice.

Họ so sánh mô hình một nhân tố với mô hình hai nhân tố tương quan. Kết quả conventional SEM:

| Mô hình | χ² | df | CFI | RMSEA | SRMR | AIC |
|---|---:|---:|---:|---:|---:|---:|
| Single factor | 16.153 | 14 | .997 | .023 | .024 | 4,113.674 |
| Correlated size/depth | 8.391 | 13 | 1.000 | <.001 | .018 | 4,107.574 |

Mô hình hai nhân tố phù hợp hơn. Tương quan latent giữa size và depth rất cao: `r=.945` trong conventional SEM và `r=.943` trong Bayesian SEM có cross-loadings nhỏ. Kết luận của tác giả là size và depth liên quan chặt nhưng nên được phân biệt về mặt khái niệm và thống kê.

**Hệ quả:** `r≈.94` không phải lý do đủ để gộp breadth và depth thành một `K_hat`. Nếu mục tiêu là vocabulary size, chỉ các item breadth đã định nghĩa mới đóng góp vào word-count estimand. Depth có thể là output phụ hoặc một latent score được link riêng.

### 2. Cấu trúc đã quan sát có phạm vi tổng quát có điều kiện

Nghiên cứu Frontiers dùng người học Nhật trình độ thấp–trung cấp, một công cụ size với ba indicator và các depth test về association/polysemy/collocation. Spoken forms, word parts và grammatical functions không được đo. Bài viết cũng lưu ý cần mẫu L1/L2 khác và nhiều công cụ hơn.

Do đó, không được chuyển thẳng factor structure, loading hoặc correlation nói trên sang:

- người học có L1 khác;
- vocabulary test nghe hoặc nói;
- productive recall thay cho written recognition;
- item bank có lexical unit, frequency corpus hoặc context khác.

Đây là transportability constraint, không phải phủ định kết quả nghiên cứu.

### 3. Response format và proficiency có thể thay đổi dimension/facet

Nguồn ERIC nghiên cứu 82 elementary và 71 advanced EFL learners, nhấn mạnh word knowledge có nhiều chiều gồm breadth, depth và accessibility. Kết quả abstract báo cáo elementary làm tốt hơn ở selective word-association format, còn advanced làm tốt hơn ở productive format.

**Hệ quả:** format không chỉ là giao diện. Selective recognition và productive recall có thể tải lên các năng lực khác nhau tùy proficiency. Không dùng một hệ số hiệu chỉnh cố định để biến MCQ recognition thành productive/depth knowledge nếu chưa có common-person linking theo proficiency và format.

### 4. Unidimensionality là giả định có hậu quả cho IRT equating

ETS RR-85-30 mô tả unidimensionality là giả định rằng statistical dependence giữa item scores được giải thích bởi một ability dimension. Báo cáo nghiên cứu mối liên hệ giữa vi phạm giả định này và chất lượng IRT true-score equating; các form/parcel có mức gần-unidimensional và mức song song khác nhau.

ETS RR-04-44 về unidimensional và multidimensional IRT nêu rằng khi simple-structure assumption bị vi phạm, tương quan giữa subscales bị ước lượng cao hơn. Vì thế, một composite breadth+depth có thể nhìn như một thang đo rất nhất quán hoặc có tương quan cao chỉ vì cross-loading bị ép về zero.

**Hệ quả:** dimensionality audit phải đứng trước equating, CAT information và score aggregation. Fit một Rasch/2PL không chứng minh rằng mọi item cùng đo một construct nếu test blueprint thực tế gồm nhiều modality/knowledge facets.

## Thuật toán đề xuất

### Data contract cho mỗi item

Mỗi item cần có tối thiểu:

```text
item_id
lexical_unit_type       # headword, lemma, flemma hoặc word family
construct               # breadth, depth_association, depth_collocation, access...
modality                # written-recognition, written-recall, auditory...
frequency_band
L1_or_population_scope
form_version
anchor_flag
content_blueprint_id
```

### Dimensionality gate

1. Chốt trước estimand: ví dụ `receptive_written_lemma_breadth`.
2. Chỉ định item blueprint và giữ các item depth/accessibility ở construct khác.
3. Trên pilot response data, fit các model cạnh tranh:
   - unidimensional Rasch/1PL hoặc 2PL cho breadth-only;
   - correlated two-factor cho breadth/depth;
   - bifactor hoặc MIRT chỉ khi có blueprint và sample đủ để nhận dạng.
4. So sánh fit, residual/local dependence, cross-loading, subgroup invariance và dự đoán hold-out. AIC/CFI/RMSEA là bằng chứng hỗ trợ, không phải quyết định duy nhất.
5. Kiểm tra stability bằng bootstrap người và item; nếu kết luận dimension đổi mạnh theo resample/L1/modality thì không release một tổng latent score.
6. Sau khi dimension ổn định, calibrate IRT trong từng construct; chỉ link/aggregate khi có common-person/common-item evidence và intended-use validation.

### Pseudocode

```text
estimate_vocab(test_response, item_bank, manifest, calibration):
    assert manifest.estimand == "receptive_written_breadth"
    breadth = items_where(item_bank, construct == "breadth"
                          and modality == "written-recognition")
    depth = items_where(item_bank, construct != "breadth")

    models = [fit_1PL_or_2PL(breadth),
              fit_correlated_2factor(breadth, depth)]
    if blueprint_supports_multiple_traits(manifest):
        models += [fit_bifactor_or_MIRT(breadth, depth)]

    audit = compare_models(
        models,
        metrics=[fit, residuals, local_dependence,
                 cross_loadings, subgroup_invariance,
                 holdout_log_score])
    audit = bootstrap_dimensionality(audit, persons=True, items=True)

    breadth_theta = score_latent(test_response[breadth],
                                 calibration.breadth_model)
    band_scores = estimate_band_counts(test_response[breadth],
                                       calibration.breadth_model,
                                       sampling_weights=manifest.weights)
    breadth_count = sum(band_scores.K_hat)

    if audit.mixed_construct_unstable or not calibration.link_validated:
        depth_profile = score_separately(test_response[depth], calibration.depth_models)
        return {
          "K_hat": breadth_count,
          "band_scores": band_scores,
          "depth_profile": depth_profile,
          "total_composite": null,
          "dimensionality_status": "separate_constructs_unvalidated_for_aggregation",
          "uncertainty": combine_response_sampling_model_uncertainty(audit)
        }

    composite = calibrated_composite(breadth_theta, depth, calibration.link)
    return {"K_hat": breadth_count, "band_scores": band_scores,
            "depth_profile": score_separately(depth),
            "total_composite": composite,
            "dimensionality_status": "linked_and_validated",
            "uncertainty": combine_response_sampling_model_uncertainty(audit)}
```

### Count and uncertainty rules

For frequency band `b` with `N_b` declared lexical units and weighted calibrated probabilities `p_i`:

```text
p_hat_b = sum_i(w_i * p_i) / sum_i(w_i)
K_hat_b = N_b * p_hat_b
K_hat = sum_b K_hat_b
```

`p_i` là calibrated probability of knowing/recognizing theo breadth model; không mặc định đồng nhất với một response đúng. Báo riêng:

```text
CI_response_or_sampling
CI_model_or_dimensionality
CI_band_rank_or_manifest_sensitivity
depth_profile_interval
aggregation_status
```

Nếu không có bằng chứng linking, không cộng điểm depth vào `K_hat`, không dùng hệ số tương quan latent để “bù” phần breadth, và không gọi composite là vocabulary size.

## So sánh với Preply

| Khía cạnh | Preply reference | Thiết kế đề xuất |
|---|---|---|
| Public dimensionality evidence | Direct methodology endpoint trả HTTP 403 trong callback; chưa xác minh được factor/IRT report | Pilot bắt buộc fit competing dimensions và lưu audit |
| Output estimand | Các iteration trước ghi nhận proxy vendor mô tả dictionary-headword vocabulary estimate; chi tiết này chưa được direct endpoint xác minh trong callback | `K_hat` chỉ từ breadth construct/lexical unit manifest đã chốt |
| Breadth/depth separation | Chưa tìm được nguồn xác thực cho việc Preply có depth/accessibility subscale riêng | Score breadth, depth và modality riêng; composite chỉ sau linking |
| Cross-form/equating | Chưa có public evidence về cross-loading, dimensionality, common anchors hoặc hold-out linking | Common-person/common-item anchors + dimension stability + hold-out |
| Uncertainty | Không thể xác minh dimensionality contribution của margin vendor từ endpoint bị 403 | Tách response, sampling, model/dimensionality và manifest sensitivity |
| Interpretation | Không suy ra mastery hoặc functional skill chỉ từ count | Không suy ra depth, listening, productive ability hay CEFR từ `K_hat` |

## Release gates và validation plan

Không release composite breadth+depth nếu một trong các điều kiện sau xảy ra:

- item construct/modality chưa có trong manifest;
- model fit chỉ tốt in-sample nhưng hold-out kém;
- cross-loading/local dependence chưa được kiểm tra;
- factor structure không ổn định qua bootstrap, L1, proficiency hoặc form;
- chưa có common-person/common-item link;
- interval chỉ bao gồm response error mà bỏ qua model/dimensionality uncertainty.

Pilot tối thiểu cần ghi response-level data, construct/modality metadata và calibration sample đủ đa dạng. Đánh giá:

1. model comparison và posterior/prediction checks;
2. conditional SE và interval coverage riêng cho `K_hat_b`;
3. DIF/invariance theo L1, proficiency, device và modality;
4. alternate-form linking với anchors;
5. hold-out criterion cho breadth (meaning recognition/recall tùy claim) và depth/accessibility riêng;
6. sensitivity khi bỏ depth items, đổi model và đổi blueprint.

## Kết luận iteration

Evidence đã verify ủng hộ một nguyên tắc bảo thủ: vocabulary size/breadth có thể liên hệ rất mạnh với depth nhưng không mặc nhiên là cùng một latent construct. Unidimensionality cần được kiểm tra trước IRT equating và aggregate scoring. Production nên tính `K_hat` từ breadth-only theo lexical unit đã khai báo, báo depth/accessibility như profile riêng, và chỉ tạo composite sau dimensionality, linking và intended-use validation. Không có public Preply artifact để xác định test của Preply thuộc trường hợp nào; gap này vẫn mở.
