# Iteration 33 — Norming, reference population và score reporting

## 1. Phạm vi và direction

Iteration này tập trung vào **norming, reference-population transport và score-reporting calibration**. Câu hỏi không phải chỉ là “tính được bao nhiêu từ”, mà là: con số đó có ý nghĩa với quần thể nào, có thể so sánh giữa form/ngày thi hay không, và khi nào được phép xuất percentile hoặc criterion decision.

Direction này bổ sung cho các iteration trước. Các iteration trước đã xử lý sampling, IRT, validity, domain alignment, equating, uncertainty và CEFR guardrails; iteration này biến các yêu cầu đó thành một lớp reporting có điều kiện, tách rõ:

- **descriptive breadth estimate**: `K_hat` trên lexical universe đã khóa;
- **measurement uncertainty**: khoảng bất định của `K_hat`;
- **norm-referenced interpretation**: percentile đối với reference sample được định nghĩa;
- **criterion-referenced interpretation**: đạt/không đạt một task hoặc ngưỡng đã validation;
- **transport status**: mức độ có thể vận chuyển score sang quần thể/domain khác.

## 2. Nguồn đã fetch và kiểm tra

| Nguồn | HTTP khi kiểm tra | Vai trò |
|---|---:|---|
| ETS, *TOEIC Listening & Reading Test Score User Guide* (PDF) | 200 | Ví dụ chính thức về percentile theo reference population, cập nhật norm table, scale linking, SEM/SEdiff và criterion-specific cut score |
| Dudley, Marsden & Bovolenta (2024), *A Context-Aligned Two Thousand Test* (White Rose Research Online, bản PDF xuất bản) | 200 | Nghiên cứu vocabulary-specific về target population, curriculum overlap, adjusted estimate, validation chain, reliability và Rasch diagnostics |
| Preply methodology endpoint | 403 trong các lần kiểm tra trước; bản text proxy đã fetch 200 | Chỉ dùng làm gap/đối chiếu những gì Preply công bố; không gán cho Preply norming facts chưa xác minh |

Các PDF trên được tải trực tiếp và text layer được trích xuất cục bộ. Search snippets chỉ là lead, không dùng làm bằng chứng độc lập.

## 3. Bằng chứng đã xác minh

### 3.1 Percentile là quan hệ với một reference population, không phải thuộc tính tuyệt đối của điểm

ETS định nghĩa percentile rank trong Score User Guide là tỷ lệ người thuộc TOEIC Public Testing Program population của ba năm trước có điểm thấp hơn điểm scaled của thí sinh. Tài liệu nói bảng percentile được tính trên pool ba năm và cập nhật mỗi tháng 5.

Hệ quả cho vocabulary-size test:

1. Percentile phải đi cùng `reference_population_id`, thời gian lấy mẫu, cỡ mẫu, sampling frame và ngày phát hành.
2. Percentile của người học tiếng Anh trong một nhóm tuyển chọn (ví dụ học sinh, người dùng website, người thi tự nguyện) không được gọi là percentile của “người học tiếng Anh nói chung”.
3. Khi norm table được cập nhật, cùng một `K_hat` có thể có percentile mới; score report phải lưu version cũ để tái lập lịch sử.
4. Nếu chưa có reference sample phù hợp, `percentile` phải là `null`, không thay bằng một phân phối giả định hoặc bảng quy đổi từ bài khác.

Nguồn: <https://www.ets.org/content/dam/ets-india/pdfs/toeic/toeic-listening-reading-score-user-guide.pdf>, phần “Percentile Rank”, tr. 12.

### 3.2 Alternate form cần common scale trước khi so sánh

ETS mô tả TOEIC: số câu đúng của Listening và Reading được chuyển sang một thang điểm chung; thủ tục thống kê nhằm để điểm thu được ở các ngày thi khác nhau có cùng ý nghĩa về mức proficiency được chỉ ra.

Đây là bằng chứng triển khai cho một vocabulary test có nhiều form hoặc adaptive route:

- raw correct count/proportion chỉ so sánh được khi forms có cùng khó và cùng blueprint;
- nếu không, phải dùng common items, IRT linking hoặc equating đã được kiểm định;
- `form_id`, `bank_version`, `anchor_set_version` và `linking_error` phải nằm trong score record;
- score report cần phân biệt thay đổi do người học với thay đổi do form/bank.

Không có cơ sở để dùng scale của Preply cho một test mới chỉ vì cả hai đều báo “số từ”. Cần common-person/common-item data và một lexical-unit mapping đã khóa.

Nguồn: <https://www.ets.org/content/dam/ets-india/pdfs/toeic/toeic-listening-reading-score-user-guide.pdf>, phần “Interpreting Scores”, tr. 13.

### 3.3 SEM và SEdiff là thành phần bắt buộc của diễn giải score, nhưng không được copy số của TOEIC

ETS minh họa hai lớp uncertainty: khoảng hai phần ba lần đo TOEIC nằm trong khoảng ±25 scaled points quanh “true score”; standard error of difference giữa hai lần thi khoảng 35 scaled points. Tài liệu dùng ±1 SEdiff như ví dụ khoảng 68% cho chênh lệch hai lần đo.

Đối với vocabulary-size test, quy tắc an toàn là:

- xuất `K_hat` cùng `CI_response_sampling` hoặc posterior interval đã calibration trên chính vocabulary bank;
- nếu có retest, xuất thêm `SEdiff_K` để phân biệt growth với form/occasion noise;
- dùng cùng một đơn vị với score đang báo, ví dụ headword count hoặc lemma count;
- không chuyển ±25/±35 TOEIC points thành số từ, cũng không gọi margin được quảng cáo của một sản phẩm là SEM nếu chưa có coverage study.

Một điểm quan trọng: SEM của phép đo người không bao gồm tự động uncertainty do lexical universe, corpus rank, headword↔lemma mapping, domain transport hoặc criterion link. Các thành phần đó phải tách riêng trong report.

Nguồn: <https://www.ets.org/content/dam/ets-india/pdfs/toeic/toeic-listening-reading-score-user-guide.pdf>, phần “Interpreting Scores” và “Repeat Test Takers”, tr. 13–14.

### 3.4 Cut score là criterion-specific, không phải pass/fail phổ quát

ETS nêu TOEIC không phải bài có một pass/fail grade cố định. Doanh nghiệp hoặc tổ chức có thể tự đặt minimum score theo năng lực cần cho công việc cụ thể.

Áp dụng cho vocabulary estimator:

- `K_hat` là mô tả breadth, không tự tạo ra quyết định đạt/trượt;
- một criterion decision phải chỉ rõ task/domain, population, loss của false positive/false negative và mẫu dùng để validation;
- ví dụ hợp lệ hơn là `coverage_for_domain_d >= threshold` sau khi đã calibration trên corpus/task, thay vì “biết 5.000 từ = đạt B2”;
- chỉ xuất `criterion_status=pass` khi cut score và classification accuracy đã được xác nhận; nếu không, xuất `criterion_status=not_validated`.

Nguồn: <https://www.ets.org/content/dam/ets-india/pdfs/toeic/toeic-listening-reading-score-user-guide.pdf>, phần “Passing the TOEIC Test”, tr. 16.

### 3.5 Vocabulary estimate thay đổi khi test được transport sang target population khác

Dudley, Marsden và Bovolenta (2024) phát triển CA-TTT cho 16-year-old English-speaking learners học French trong bối cảnh khoảng 400–450 giờ học trên lớp và rất ít tiếp xúc ngoài lớp. Mẫu gồm 222 người từ 89 trường ở England.

Thiết kế test cố ý align với target-language-use domain: 79.42% item trung bình xuất hiện trong curriculum list tương ứng. Accuracy của từ có trong list là 84.61%, còn từ ngoài list là 68.83%. Khi điều chỉnh estimate theo số high-frequency words on-list/off-list, mean estimate giảm từ 1,627 xuống 1,480.

Nghiên cứu này không cung cấp hệ số sửa cho tiếng Anh hoặc Preply. Giá trị phương pháp luận là chứng minh rằng một frequency-based vocabulary count có thể phụ thuộc curriculum exposure và sampling frame. Vì thế production phải lưu:

- population profile và exposure context;
- target-language-use/curriculum list version;
- tỷ lệ overlap giữa item bank và domain;
- score cả unadjusted và domain-adjusted chỉ khi adjustment đã pre-register và hold-out validate.

Không dùng norm của người học classroom-limited để báo cáo như norm của người học có immersion, và ngược lại.

Nguồn: <https://eprints.whiterose.ac.uk/id/eprint/211470/8/dudley-et-al-2024-a-context-aligned-two-thousand-test-toward-estimating-high-frequency-french-vocabulary-knowledge-for.pdf>, abstract, pp. 9–15.

### 3.6 Một validation chain tốt phải tách domain, universe score, observed score và target score

CA-TTT dùng chuỗi suy luận gồm:

1. **Domain description** — item có đại diện cho target-language-use domain không?
2. **Generalization** — score có đại diện cho universe item không; xem internal consistency/model fit.
3. **Scoring** — item có difficulty/fit phù hợp không?
4. **Explanation** — có giải thích được misfit và construct interpretation không?
5. **Extrapolation** — score có liên hệ với proficiency/behavior ngoài test không?

Trong pilot, one-factor CFA cho overall test và hai band có fit tốt; categorical omega là `.92` ở band 1,000, `.94` ở band 2,000 và `.96` cho hai band. Tuy nhiên person-separation reliability là `.80` ở band 1,000 và `.88` ở band 2,000; band 1,000 khá dễ với phần lớn mẫu. Các số này thuộc CA-TTT pilot, không phải precision của Preply.

Production implication: reliability cao chỉ hỗ trợ consistency/generalization. Nó không tự chứng minh norm transport, percentile validity, functional interpretation hoặc criterion cut score.

Nguồn: <https://eprints.whiterose.ac.uk/id/eprint/211470/8/dudley-et-al-2024-a-context-aligned-two-thousand-test-toward-estimating-high-frequency-french-vocabulary-knowledge-for.pdf>, pp. 8–9 và 15–18.

## 4. Lớp reporting được đề xuất

### 4.1 Data model

```text
ScoreReport {
  estimate: K_hat,
  estimate_unit: headword | lemma | word_family,
  universe_id,
  universe_version,
  bank_version,
  form_id,
  measurement_interval: [lo, hi],
  interval_method,
  sem_or_se_K,
  linking_error,
  rank_or_corpus_sensitivity,
  endpoint_status,
  reference_population_id: nullable,
  reference_population_version: nullable,
  norm_sample_n: nullable,
  norm_sampling_frame: nullable,
  norm_dates: nullable,
  percentile: nullable,
  percentile_interval: nullable,
  criterion_id: nullable,
  criterion_status: not_validated | pass | fail | indeterminate,
  domain_profile_id: nullable,
  transport_status,
  validity_flags[]
}
```

### 4.2 Quy tắc percentile

```text
function report_percentile(K_hat, reference_sample, reference_metadata):
    if reference_sample is null:
        return percentile=null, status="no_norm_sample"
    if not compatible(reference_metadata, target_population, universe_version,
                      estimate_unit, form_linking):
        return percentile=null, status="norm_not_transportable"
    N = count(reference_sample)
    less = count(x < K_hat for x in reference_sample)
    equal = count(x == K_hat for x in reference_sample)
    p = (less + 0.5 * equal) / N
    p_interval = bootstrap_people_and_recompute_percentile(reference_sample, K_hat)
    return p, p_interval, status="norm_referenced"
```

Công thức midrank trên chỉ là quy ước reporting; độ rộng `percentile_interval` phải được bootstrap hoặc ước lượng bằng phương pháp đã validation. Không biến `CI_K` thành percentile interval bằng một phép đổi tuyến tính đơn giản.

### 4.3 Quy tắc criterion

```text
function criterion_decision(report, criterion):
    if criterion is null or not criterion.is_validated:
        return "not_validated"
    if report.transport_status != "validated":
        return "indeterminate"
    if interval_crosses(criterion.boundary, report.measurement_interval):
        return "indeterminate"
    if criterion.uses_domain_coverage:
        return classify(report.domain_coverage_interval, criterion)
    return classify(report.estimate_interval, criterion)
```

Criterion nên ưu tiên task/domain coverage nếu mục tiêu là đọc, nghe hoặc xử lý tài liệu cụ thể. `K_hat` breadth vẫn là output riêng, không cộng domain coverage vào số từ.

### 4.4 Quy tắc alternate form

```text
function compare_forms(response, form_id, bank_version):
    raw = score_raw(response)
    if not linking_model_exists(form_id, bank_version):
        return raw, status="form_specific_only"
    linked = apply_linking(raw, linking_model(form_id, bank_version))
    return linked, interval=combine(measurement_error, linking_error),
           status="linked_scale"
```

Form mới không được đưa vào norm percentile cho tới khi có common-anchor/common-person study và kiểm tra drift.

## 5. Đối chiếu với cách làm của Preply

| Thành phần | Preply đã công bố/đã xác minh | Lớp đề xuất sau iteration 33 |
|---|---|---|
| Estimand | Methodology proxy mô tả dictionary main entries, receptive knowledge và derived forms được cộng vào headword | Công khai `estimate_unit`, dictionary mapping và version; không gọi headword count là lemma/family count |
| Frequency universe | BNC và pipeline spoken/written rebalancing được mô tả trong proxy | Lưu corpus/bank version, population/TLU profile và sensitivity khi vận chuyển |
| Short test score | Preply có score/margin được hiển thị theo sản phẩm; item-level calibration và reference norm sample chưa xác minh | Tách `K_hat`, measurement interval, rank/construct sensitivity và endpoint status |
| Percentile/norm | Chưa tìm được nguồn xác thực cho norm population, percentile table, update window hoặc subgroup norms riêng của Preply | Chỉ tính percentile khi có reference sample metadata; nếu thiếu trả `null` |
| Alternate forms | Chưa có item bank/anchor/common-person data công khai để xác minh scale linking | Dùng common-item/IRT equating; lưu linking error và form id |
| Criterion decision | Chưa có evidence công khai cho cut score theo task hoặc pass/fail vocabulary | Tách criterion layer; default `not_validated`, không map thẳng sang CEFR |
| Transport | Chưa có response-level data theo population/domain để kiểm tra norm portability | Báo `transport_status` và curriculum/domain overlap; cần hold-out theo subgroup |
| Preply gaps | Endpoint methodology trực tiếp trả 403 trong các lần kiểm tra trước; bản proxy không giải quyết được norming/SEM/anchor data | Không điền số liệu thiếu bằng assumption; ghi “chưa tìm được nguồn xác thực cho norm sample, percentile update và linking riêng của Preply” |

## 6. Uncertainty và assumptions

### 6.1 Các thành phần phải tách

```text
measurement_interval   = response_sampling_or_model uncertainty
linking_error           = alternate-form/common-scale uncertainty
rank_sensitivity        = corpus/frequency-manifest sensitivity
mapping_uncertainty     = headword/lemma/family and sense mapping
transport_uncertainty   = target-population/domain shift
criterion_uncertainty   = boundary/classification error
```

Không cộng các thành phần bằng một scalar duy nhất nếu chưa có nested bootstrap hoặc simulation đã kiểm tra coverage. Score report nên hiển thị các thành phần riêng, sau đó có thể thêm một `overall_sensitivity_range` với nhãn rõ rằng đó không mặc định là frequentist CI.

### 6.2 Assumptions cần ghi trong report

- Reference sample là người độc lập; không trộn repeated attempts.
- Norm sample làm cùng construct, lexical universe, modality và response rubric, hoặc có linking đã xác minh.
- `K_hat` và reference scores cùng estimate unit.
- Nếu population là classroom-limited, curriculum overlap được đo và không bị coi là nuisance có thể bỏ qua.
- Criterion threshold không được suy ra từ một percentile tùy ý.
- Các số SEM/SEdiff của ETS chỉ là ví dụ triển khai; không chuyển trực tiếp sang vocabulary count.

## 7. Validation plan

1. **Norm-sample design:** tuyển reference cohorts theo population/use case đã định; lưu age, L1, education, exposure, modality, region và recruitment frame; kiểm tra nonresponse/selection bias.
2. **Norm stability:** chia theo thời gian/form; bootstrap theo người; kiểm tra percentile drift giữa các cửa sổ 12/24/36 tháng trước khi chọn update cadence.
3. **Common-scale study:** cho cùng người làm hai forms; thiết kế common anchors phủ các band; so sánh raw, Rasch/2PL linking và observed score differences.
4. **SEM coverage:** dùng repeated forms hoặc simulation có ground truth để kiểm tra coverage của `measurement_interval`; báo riêng low/medium/high score regions.
5. **Transport audit:** hold-out theo curriculum/exposure/domain; so sánh item difficulty, band accuracy và calibration error giữa nhóm; gắn `norm_not_transportable` nếu drift vượt tolerance đã pre-register.
6. **Criterion validation:** xác định task criterion độc lập; estimate ROC/classification accuracy và hậu quả false positive/negative; chỉ phát hành cut score sau cross-validation.
7. **Reporting usability:** kiểm tra người dùng có hiểu `K_hat`, percentile, CI và criterion status là bốn khái niệm khác nhau; không hiển thị percentile nếu metadata norm thiếu.
8. **Preply bridge:** chỉ đối chiếu Preply sau khi có item bank/response-level/common-person data hoặc một linking study được phép; nếu không, bảng chỉ ghi “không xác minh được”.

## 8. Gaps

- Chưa có reference population, norm sample size, sampling frame, percentile update cadence hoặc subgroup norms của Preply.
- Chưa có Preply common-item/common-person data để xác minh alternate-form equating, linking error hoặc form drift.
- Chưa có response-level data để ước lượng SEM/SEdiff của Preply trong đơn vị headword count.
- Chưa có criterion sample để map vocabulary breadth sang reading/listening task, CEFR hoặc pass/fail decision.
- CA-TTT là nghiên cứu tiếng Pháp trong nhóm học sinh 16 tuổi; các số 79.42%, 84.61%, 68.83%, 1,627 và 1,480 không được dùng như prior cho tiếng Anh/Preply.
- Chưa tìm được nguồn xác thực cho một công thức phổ quát biến `K_hat` của Preply thành percentile dân số, lemma/family count hoặc functional level.

## 9. Kết luận iteration

Norm-referenced score chỉ hợp lệ theo reference population được mô tả; vocabulary-size estimate không có percentile phổ quát. Reporting production nên mặc định là `descriptive_only` khi thiếu norm sample, tách measurement interval khỏi linking/rank/transport uncertainty, và chỉ phát hành criterion decision sau validation theo task. Bằng chứng CA-TTT cho thấy curriculum alignment có thể làm estimate thay đổi đáng kể, còn ETS cung cấp pattern triển khai rõ cho rolling norm tables, common scale và SEM/SEdiff — nhưng không có số nào trong tài liệu ETS được phép copy thành margin cho Preply.

### URL nguồn

- ETS TOEIC Score User Guide: <https://www.ets.org/content/dam/ets-india/pdfs/toeic/toeic-listening-reading-score-user-guide.pdf>
- Dudley, Marsden & Bovolenta (2024), CA-TTT open PDF: <https://eprints.whiterose.ac.uk/id/eprint/211470/8/dudley-et-al-2024-a-context-aligned-two-thousand-test-toward-estimating-high-frequency-french-vocabulary-knowledge-for.pdf>
- Preply methodology (đối chiếu/gap): <https://preply.com/en/learn/english/test-your-vocab/how-it-works>
