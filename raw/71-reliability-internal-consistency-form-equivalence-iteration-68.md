# Iteration 68: Reliability evidence, internal consistency và form equivalence

## 1. Phạm vi và trạng thái bằng chứng

Iteration này tách một câu hỏi cụ thể khỏi các iteration về SEM, test–retest, IRT và alternate forms: **một hệ số nhất quán nội tại cao có đủ để phát hành một ước lượng vocabulary size ổn định hay không?** Trọng tâm là phân biệt:

- nhất quán nội tại trong một form;
- ổn định qua thời điểm hoặc form khác;
- tương đương không lệch giữa các form;
- độ chính xác có điều kiện theo mức vocabulary;
- độ nhất quán của quyết định nếu hệ thống báo band/category.

Các URL dưới đây đã được fetch trong callback và đều trả HTTP 200 trước khi trích dẫn:

| Nguồn | Vai trò | HTTP |
|---|---|---:|
| [ETS Standards for Educational and Psychological Testing](https://www.ets.org/pdfs/about/standards-quality-fairness.pdf) | reliability theo intended use, nguồn sai số, adaptive/matrix sampling, conditional SEM, decision consistency và documentation | 200 |
| [Assessing Reliability of Two Versions of Vocabulary Levels Test](https://files.eric.ed.gov/fulltext/EJ1127013.pdf) | bằng chứng vocabulary-specific về tương quan cao nhưng mean/form bias giữa hai form | 200 |
| [Laufer & Nation, A vocabulary-size test of controlled productive ability](https://www.lextutor.ca/tests/laufer_nation_1999.pdf) | reliability theo frequency band và bốn form của một vocabulary test cụ thể | 200 |
| [Zitzmann & Orona, Frontiers in Psychology (2026)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1796702/full) | giới hạn và lựa chọn alpha/omega/composite reliability cho domain-specific knowledge tests | 200 |
| [Preply methodology page qua extraction proxy](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) | disclosure của sản phẩm tham chiếu về universe, sampling, midpoint và vendor margin | 200 |

Hai URL Preply trực tiếp được kiểm tra trong callback trả HTTP 403; vì vậy chỉ methodology page qua proxy HTTP 200 được dùng làm nguồn đối chiếu. Proxy giúp đọc nội dung public, không chứng minh backend, item bank hoặc calibration nội bộ.

## 2. Findings đã xác minh

### 2.1 Reliability phải gắn với score use và nguồn sai số

ETS Standards 6.1–6.4 định nghĩa reliability theo mức độ score nhất quán và có thể generalize qua các form, occasion và rater có liên quan. Chuẩn không đặt một ngưỡng chung hoặc bắt buộc một phương pháp duy nhất; phương pháp phải khớp với intended use và các nguồn variation mà score được kỳ vọng ổn định qua đó.

Các trường hợp được nêu trực tiếp trong chuẩn gồm:

- adaptive test phải tính ảnh hưởng của item selection; resampling mô phỏng adaptive process có thể dùng;
- test/matrix sampling phải tính scheme chọn item;
- test có nhiều knowledge area/skill phải cho phép ability giữa các area khác nhau;
- score dùng để phân loại phải có form-to-form decision consistency;
- các dạng bằng chứng có thể gồm reliability/generalizability coefficient, information function, overall/conditional SEM và decision consistency;
- thống kê phải được báo theo population, score level, công thức, nguồn variation và điều kiện thu thập.

**Hệ quả cho vocabulary-size test:** α, KR-20 hoặc ω chỉ trả lời một lát cắt của câu hỏi. Nếu item bank lấy mẫu theo frequency band, score còn chịu lỗi do lexical-unit sampling, form assembly, band coverage, model và occasion. Không được gọi một coefficient nội tại là “margin of error của số từ”.

### 2.2 Tương quan form cao không chứng minh alternate-form equivalence

Nghiên cứu Vocabulary Levels Test trong bối cảnh Iran dùng 75 người học EFL trung cấp, hai form được làm cách nhau một tuần và counterbalanced. Kết quả:

- tương quan tổng giữa hai form: `r = .938`;
- mean Form 1: `57.26`, mean Form 2: `59.40`;
- chênh lệch paired: `2.13`, `p = .025`;
- các band 3000, 5000 và Academic cũng có mean khác biệt có ý nghĩa;
- tác giả kết luận hai form không phải parallel forms nghiêm ngặt và không nên dùng để suy luận gain/longitudinal nếu chưa xử lý form difficulty.

Đây là ví dụ quan trọng cho estimator: `r` cao chứng minh người làm bài được xếp hạng gần giống nhau, nhưng không chứng minh hai form cho cùng một mức số từ. Form bias có thể tồn tại dù correlation rất cao.

### 2.3 Reliability của vocabulary test phụ thuộc format, band và population

Laufer và Nation xây dựng controlled-productive vocabulary-levels test với 18 item tại mỗi một trong năm mức: 2000, 3000, 5000, University Word List và 10000. Trong validation sample của nghiên cứu năm 1999:

- KR-21 toàn test: `.86`;
- reliability theo band: `.77`, `.81`, `.84`, `.84`, `.90`;
- test phân biệt các nhóm proficiency;
- bốn form được thiết kế tương đương và đạt mức equivalence được tác giả mô tả là satisfactory.

Các con số này chỉ là evidence cho **controlled productive**, frequency-banded, sentence-completion design và population của nghiên cứu đó. Không được chuyển `.86` thành ngưỡng production cho một receptive, headword-based, online test; item format, population, lexical-unit policy và mục đích score khác nhau sẽ thay đổi reliability.

### 2.4 Alpha/omega cần được diễn giải theo construct model

Bài open-access 2026 của Zitzmann và Orona tranh luận rằng content heterogeneity không tự động làm alpha vô nghĩa, nhưng alpha cũng không phải bằng chứng đủ cho mọi domain-specific knowledge test. Cách chọn coefficient phụ thuộc vào cách score được hiểu:

- nếu score là blend của nhiều facet, composite reliability có thể phù hợp hơn;
- nếu score được hiểu là phản ánh một dominant reflective factor, omega có thể phù hợp hơn;
- nếu factor analysis cho thấy multidimensionality mạnh hoặc item không parallel, phải bổ sung hệ số/mô hình phù hợp và evidence về stability, chẳng hạn test–retest;
- cần phân biệt item sampling từ một domain với một formative construct, vì hai cách hiểu dẫn tới cách diễn giải reliability khác nhau.

Áp dụng thận trọng vào vocabulary size: frequency bands có thể là các facet nội dung có chủ đích, không phải các item duplicate. Vì vậy, không tối ưu item bank để alpha cao bằng cách bỏ các band/lexical facets cần thiết. Ngược lại, alpha thấp cũng không được dùng như giấy phép bỏ qua reliability; phải kiểm tra dimensionality, item fit, band coverage và intended score interpretation.

### 2.5 Preply công bố vendor margin nhưng chưa công bố reliability evidence tương ứng

Trang methodology Preply đã fetch mô tả:

- dictionary hơn 45.000 entries, được xếp theo frequency;
- phase đầu khoảng 40 từ trải rộng từ dễ đến khó để định vị;
- phase hai khoảng 120 từ trong vùng hẹp hơn, lấy theo frequency và phân bố logarithmic;
- midpoint của known/unknown responses để suy ra rank vocabulary;
- margin of error vendor khoảng `±10.33%`, suy ra từ giả định SD gần `0.25 × vocabulary size` và trung bình 22.5 sample points.

Trang không công bố trong nội dung đã fetch:

- α/KR-20/ω hoặc coefficient nội tại;
- test–retest hoặc alternate-form correlation/bias;
- conditional SEM theo mức vocabulary;
- information function hoặc item-level calibration;
- form-to-form decision consistency;
- empirical coverage của khoảng `±10%` trên response-level holdout.

Vì vậy, `±10%` được xác minh là **vendor sampling-model claim**, không phải bằng chứng độc lập rằng mỗi cá nhân sẽ nhận cùng một estimate qua form khác, occasion khác hoặc item bank version khác.

## 3. Đề xuất reliability layer cho thuật toán

### 3.1 Tách các đại lượng không được gộp

Lưu riêng các trường sau trong score record:

```text
K_raw                 = count/estimate trước equating
K_equated             = estimate trên scale đã link với bank/version chuẩn
within_form_alpha     = alpha hoặc KR-20, nếu binary và phù hợp
within_form_omega     = omega hoặc composite reliability, nếu model phù hợp
form_bias             = mean(K_form_B − K_form_A) trên common-person sample
form_LoA              = limits of agreement của chênh lệch hai form
SE_conditional        = conditional error theo θ hoặc K
CI_sampling           = lỗi do lexical-unit/item sampling
CI_model              = lỗi do Rasch/2PL/Bayesian/model choice
CI_form               = lỗi form/anchor/equating
CI_total              = interval đã kiểm tra coverage trên holdout
reliability_status    = validated | preliminary | descriptive_only | not_released
```

`within_form_alpha` và `within_form_omega` không thay thế `SE_conditional`, `CI_form` hoặc `CI_total`.

### 3.2 Công thức thiết kế

Với mô hình IRT đã calibration, information tại ability θ là `I(θ)`. Standard error latent có thể khởi tạo bằng:

```text
SE_θ(θ) = 1 / √I(θ)
```

Nếu breadth count được map từ latent ability và frequency strata:

```text
K_hat(θ) = Σ_h M_h × p_h(θ)
```

Trong đó `M_h` là số lexical units trong stratum h, còn `p_h(θ)` là xác suất biết trung bình sau calibration. Với delta-method approximation:

```text
SE_K_response(θ) ≈ |dK_hat(θ) / dθ| × SE_θ(θ)
```

Tổng uncertainty không nên cộng máy móc nếu các thành phần phụ thuộc nhau. Có thể dùng joint bootstrap/posterior resampling:

```text
K_draw_s = score_model_draw_s(
    response_resample_s,
    item_parameter_draw_s,
    form/anchor_draw_s,
    lexical_universe_draw_s)

CI_total = quantile(K_draw_s, [0.025, 0.975])
```

Nếu có thể chứng minh các component gần độc lập, một diagnostic approximation là:

```text
Var_total ≈ Var_response
           + Var_item_sampling
           + Var_model
           + Var_form_equating
           + Var_reference_population
```

Không đưa `within_form_alpha` trực tiếp vào công thức như một correction cho `K_hat`. Nếu score được dùng để ra quyết định category, đo thêm:

```text
P(correct_category | repeated_form_or_posterior_draws)
```

và báo decision consistency riêng. Với reliable-change claim trên cùng estimand và scale đã equated, có thể dùng:

```text
MDC95 = 1.96 × √2 × SEM
```

nhưng không dùng công thức này để biến hai form chưa equate thành bằng chứng learner growth.

### 3.3 Pseudocode

```text
function reliability_release(session, bank, calibration):
    assert session.universe_version == bank.universe_version
    assert session.lexical_unit_policy == bank.lexical_unit_policy

    responses = clean_status_aware_responses(session)
    K_raw = score_primary_estimator(responses, bank)

    dimensionality = run_dimensionality_and_local_dependence_checks(
        calibration.responses, bank)
    fit = fit_or_load_irt_parameters(calibration, bank)

    within = estimate_within_form_reliability(
        responses=calibration.responses,
        method=[KR20_or_alpha, omega_if_model_supported],
        by_band=True)

    if calibration.has_common_person_alternate_forms:
        form_stats = compare_forms(
            common_person_responses=calibration.common_person_responses,
            estimate_mean_bias=True,
            estimate_limits_of_agreement=True,
            link_with_common_anchors=True)
    else:
        form_stats = {"status": "missing"}

    draws = joint_resample(
        response_rows=calibration.responses,
        item_parameters=fit,
        lexical_universe=bank.manifest,
        form_link=form_stats)
    K_draws = [score_primary_estimator(d.responses, d.bank, d.parameters)
               for d in draws]
    CI_total = quantiles(K_draws, [0.025, 0.975])
    SE_conditional = conditional_se_by_score(K_draws)

    if not dimensionality.pass or not fit.item_fit_pass:
        status = "descriptive_only"
    elif form_stats.status != "equated_and_bias_checked":
        status = "preliminary"
    elif not coverage_validated(CI_total, calibration.holdout):
        status = "preliminary"
    else:
        status = "validated"

    return {
        "K_raw": K_raw,
        "K_equated": equate_if_valid(K_raw, form_stats),
        "within_form": within,
        "form_stats": form_stats,
        "SE_conditional": SE_conditional,
        "CI_total": CI_total,
        "reliability_status": status,
    }
```

### 3.4 Release gates

1. **Construct gate:** lexical-unit universe, frequency manifest, intended receptive/productive construct và reporting purpose đã version hóa.
2. **Within-form gate:** báo α/KR-20/ω phù hợp với item type và model; không tối ưu bằng cách loại các band cần cho content representation.
3. **Dimensionality gate:** kiểm tra band structure, local dependence, item fit và whether one total score is defensible. Nếu score là blend của facets, ghi rõ cách diễn giải.
4. **Form gate:** có common-person/common-anchor data; kiểm tra mean bias và conditional form bias, không chỉ correlation.
5. **Precision gate:** có conditional SE/interval theo word units; coverage được đo trên holdout hoặc simulation đã target-calibrated.
6. **Decision gate:** nếu báo categories/bands, có decision consistency gần vùng cut hoặc ghi `not_validated`.
7. **Population gate:** reliability statistics được tính và báo cho target population; không chuyển nguyên hệ số từ controlled-productive EFL sample sang online receptive population.
8. **Output gate:** thiếu form-equating hoặc coverage thì `reliability_status = preliminary`/`descriptive_only`, không gắn nhãn “validated ±10%”.

## 4. So sánh với cách làm của Preply

| Thành phần | Preply methodology đã fetch | Thiết kế đề xuất |
|---|---|---|
| Universe | hơn 45.000 dictionary entries theo frequency; main-entry policy và derived-form decisions được mô tả | universe/headword–lemma–family policy versioned, có manifest và sensitivity |
| Sampling | phase khoảng 40 từ rộng, sau đó khoảng 120 từ hẹp/logarithmic | có thể giữ two-stage routing, nhưng item selection phải được mô phỏng và audit theo band/form |
| Point estimate | midpoint của known/unknown response trong vùng đã chọn | `K_raw`, sau đó IRT/design/model estimate và `K_equated` nếu link hợp lệ |
| Published uncertainty | vendor nêu khoảng ±10.33% từ sampling normality/SD assumption | `CI_sampling`, `CI_model`, `CI_form`, `CI_reference`; `CI_total` chỉ sau coverage validation |
| Internal consistency | chưa thấy α/KR-20/ω trong methodology page đã fetch | báo coefficient phù hợp như evidence phụ, không làm release gate duy nhất |
| Alternate forms | chưa thấy form equivalence, form bias hoặc test–retest trong page đã fetch | common-person/common-anchor equating, mean bias, conditional form error và limits of agreement |
| User-facing claim | mục tiêu là estimate nhanh và so sánh vocabulary levels | hiển thị count + interval + reliability status; không map coefficient hoặc vendor margin thành universal accuracy |

Bảng này không kết luận Preply không có reliability analyses nội bộ. Kết luận được hỗ trợ là các bằng chứng đó không xuất hiện trong methodology page đã fetch và chưa có response-level/item-bank data public để kiểm tra.

## 5. Validation plan

### 5.1 Calibration sample và alternate forms

1. Chốt target population, receptive/productive construct, lexical-unit policy và frequency manifest.
2. Tạo ít nhất hai form với cùng blueprint nhưng item khác; giữ một bộ common anchors được bảo vệ.
3. Counterbalance thứ tự form và ghi occasion, completion status, item exposure và form version.
4. Kiểm tra mean/variance, conditional bias theo vocabulary range, correlation, limits of agreement và IRT/common-anchor linking.
5. Nếu hai form tương quan cao nhưng có mean/conditional bias, không dùng raw difference làm growth; sửa assembly hoặc equate trên holdout.

### 5.2 Coefficient và model sensitivity

1. Với binary items, so sánh KR-20/alpha và omega/composite reliability chỉ khi assumptions/model được ghi rõ.
2. Kiểm tra dimensionality, band-specific structure, local dependence và item fit trước khi diễn giải coefficient.
3. So sánh total-score, Rasch/1PL, 2PL và model phù hợp đã đăng ký; báo `K_hat` sensitivity thay vì chọn model vì coefficient cao hơn.
4. Không đặt một ngưỡng alpha/omega phổ quát từ nghiên cứu khác. Chọn release threshold theo intended use, conditional precision và hậu quả của sai quyết định.

### 5.3 Coverage và score use

1. Bootstrap/Monte Carlo từ item bank có known vocabulary truth hoặc simulated latent profiles; lặp theo low/mid/high ranges.
2. Đo bias, RMSE, interval coverage, interval width và decision consistency của `K_hat`.
3. So sánh `K_raw` với `K_equated`; kiểm tra coverage sau form drift, band imbalance, missingness và retest practice.
4. Nếu sản phẩm muốn giữ claim kiểu Preply ±10%, phải chứng minh coverage trên target population và đúng pipeline hiện hành; không suy ra từ công thức midpoint hoặc alpha.
5. Chỉ sau khi pass holdout mới phát hành `reliability_status = validated`; nếu không, trả interval/sensitivity và trạng thái rõ ràng.

## 6. Assumptions và gaps

- Nghiên cứu Iran có `N = 75`, một population EFL trung cấp và một VLT format; đó là bằng chứng về form-equivalence problem, không phải hệ số universal.
- Laufer–Nation là controlled productive test năm 1999; reliability theo band không chuyển trực tiếp sang receptive online test.
- Bài Frontiers 2026 là bài measurement/opinion có lập luận về coefficient choice; không thay thế calibration response-level của vocabulary bank cụ thể.
- Preply margin là claim của vendor methodology page; chưa có holdout response data để kiểm tra frequentist coverage hoặc conditional accuracy.
- Chưa có item bank, common anchors, repeated administrations, form metadata hoặc calibration sample của Preply; **chưa tìm được nguồn xác thực cho reliability coefficient, form bias, conditional SEM hoặc decision consistency production của Preply**.
- Chưa có dữ liệu để chọn ngưỡng alpha/omega, anchor rate, sample size, conditional-SE cutoff hoặc category-consistency cutoff cho target deployment; các ngưỡng này phải được simulation/pilot-calibrate.

## 7. Kết luận iteration

**Không được dùng một coefficient nhất quán nội tại để bảo chứng cho một vocabulary count.** Bằng chứng vocabulary-specific cho thấy hai form có thể tương quan `.938` nhưng vẫn lệch mean; một test khác có reliability khác nhau theo frequency band; ETS yêu cầu reliability evidence phải khớp score use và nguồn sai số. Thiết kế production nên dùng alpha/KR-20/omega như một layer mô tả có điều kiện, bổ sung form equating/common anchors, conditional SE và holdout coverage. Khi các lớp này chưa đủ, trả `K_hat` với `reliability_status = preliminary`/`descriptive_only`, không trình bày claim ±10% như accuracy đã validation.
