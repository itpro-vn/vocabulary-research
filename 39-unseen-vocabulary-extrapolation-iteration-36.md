# Iteration 36 — Unseen-vocabulary estimators và tail extrapolation

## Phạm vi và câu hỏi

Iteration này kiểm tra một hướng dễ bị dùng sai trong vocabulary-size test: coi các từ đã “bắt gặp” như species, rồi dùng capture–recapture hoặc Good–Turing để ngoại suy số từ chưa thấy. Câu hỏi thực dụng là:

1. Capture–recapture thực sự ước lượng được gì trong nghiên cứu vocabulary?
2. Điều kiện nào làm công thức overlap bị lệch trên phân phối Zipf/power-law?
3. Good–Turing/Chao ước lượng coverage hay số lexical units chưa quan sát?
4. Có thể đưa unseen-word extrapolation vào thuật toán receptive vocabulary-size hay chỉ nên dùng làm sensitivity analysis?

Kết luận ngắn: **không dùng CR/Good–Turing làm estimator chính cho receptive vocabulary size từ một bài test item-response**. Estimator chính vẫn là tổng các xác suất biết từ theo một vocabulary universe và frequency-stratified sampling frame đã version hóa. Tail extrapolation chỉ được mở khi có thiết kế exposure độc lập, dữ liệu lặp đủ và validation hold-out; nếu không, trường `unseen_estimate` phải là `null` thay vì cộng một bonus trông có vẻ chính xác.

## Nguồn đã kiểm tra

| Nguồn | HTTP | Vai trò | Giới hạn |
|---|---:|---|---|
| [Meara & Olmos Alcoy, 2010, *Words as species*](https://files.eric.ed.gov/fulltext/EJ887892.pdf) | 200 | Mô tả phép Petersen, analogy words-as-species và các điều kiện capture/recapture | Nghiên cứu productive vocabulary, 24 người học tiếng Tây Ban Nha; không phải receptive online test |
| [Williams, Segalowitz & Leclair, 2014](https://benjamins.com/catalog/ml.9.1.02wil) | 200 | Bằng chứng validity cho CR bằng hai word-association captures | Tác giả nói rõ kết quả là relative PVS, không phải absolute vocabulary size |
| [Nelson, 2015, *Issues with the capture-recapture measure of vocabulary size*](https://www.benjamins.com/catalog/ml.10.1.06nel) | 200 | Phê bình CR khi dữ liệu có power-law/Zipf distribution | Abstract/page summary; full text nhà xuất bản yêu cầu authorization |
| [Chao et al., 2015, *Unveiling the species-rank abundance distribution*](https://www.uvm.edu/~ngotelli/manuscriptpdfs/ChaoEcolMon2015.pdf) | 200 | Good–Turing coverage, singleton/doubleton, Chao1 lower bound và tail model | Lý thuyết ecological species sampling; chỉ chuyển thành analogy, không coi là vocabulary calibration |

Trang phương pháp Preply đã được kiểm tra trong callback này nhưng endpoint trực tiếp trả 403; bản proxy cũng không trả nội dung ổn định. Vì vậy iteration này không đưa thêm claim vendor mới. Các claim Preply đã có trong các chapter trước phải tiếp tục được đọc như vendor/provisional và không được dùng để xác nhận CR/Good–Turing.

## 1. Capture–recapture trong các nghiên cứu vocabulary

### 1.1 Công thức và điều kiện

Meara & Olmos Alcoy trình bày logic Petersen: nếu lần một có `N` types, lần hai có `M` types, và có `X` types xuất hiện ở cả hai lần, estimator đơn giản là:

```text
E_CR = (N * M) / X
```

Ý tưởng chỉ có nghĩa khi hai lần capture tương đương, vocabulary universe không thay đổi, các đơn vị có cơ hội được capture tương tự, và overlap phản ánh việc cùng một population member xuất hiện ở hai lần. Trong bài của họ, “word trap” là hai bài viết cùng một nhiệm vụ; đây là productive output, không phải toàn bộ lexical knowledge ẩn trong đầu người học.

Williams, Segalowitz & Leclair dùng hai word-association captures với 47 bilinguals và báo cáo CR tương quan dương với Lex30 và một chỉ báo tốc độ lexical access. Đây là evidence hội tụ/construct validity cho **relative L2 productive vocabulary size**. Nhưng trang nhà xuất bản ghi rõ CR score không phải chỉ báo trực tiếp của **absolute vocabulary size**. Đây là giới hạn cần giữ nguyên khi chuyển phương pháp sang sản phẩm.

### 1.2 Vì sao receptive item test không phải hai capture tương ứng

Trong receptive vocabulary-size test, item bank chứa các lexical units đã biết trước. Người làm test trả lời đúng/sai trên một mẫu item. Một item không được “capture” chỉ vì nó được hỏi: nó được hỏi nhưng có thể sai; một từ người học biết nhưng không được hỏi vẫn là latent/unobserved. Do đó:

- word xuất hiện ở Form A và Form B là **item overlap**, không phải quan sát độc lập của việc người học “biết” word đó;
- overlap của các câu trả lời đúng bị điều kiện bởi ability, difficulty, context, distractor và việc hai form có chung item;
- nếu forms cố ý lấy từ các frequency band khác nhau, inclusion probability không đồng đều;
- với câu trả lời binary, không quan sát được danh sách đầy đủ các word đã biết để làm `N`, `M`, `X` như trong text production;
- two-form agreement chủ yếu phục vụ reliability/equating, không tự biến thành population-size estimator.

Vì vậy, công thức CR không được áp dụng lên số câu đúng của hai form nếu chưa chứng minh một sampling design tương ứng và đã calibration trên response-level data.

## 2. Power-law/Zipf là phản ví dụ cho overlap thô

Nelson chỉ ra rằng CR cổ điển giả định population phân phối đồng đều. Với power-law/Zipf, xác suất chọn phụ thuộc rank: các thành viên high-frequency được chọn lặp lại dễ hơn nhiều so với các thành viên ở rank 100, 1.000 hoặc thấp hơn. Hai mẫu vì thế có thể overlap lớn ở nhóm common words dù còn rất nhiều tail words chưa được quan sát. `X` lớn làm `N*M/X` nhỏ, tạo underestimation nghiêm trọng.

Hệ quả cho vocabulary test:

1. Nếu item sample đi theo frequency bands, đây không phải uniform random sampling trên toàn lexical universe.
2. Nếu người học có xác suất biết từ tăng theo frequency, observed correctness cũng tạo một probability gradient chứ không phải capture đồng đều.
3. CR bias và response-model bias chồng lên nhau; không thể sửa bằng cách tăng số item mà không mô hình hóa band và item inclusion.
4. Một overlap cao giữa hai form không chứng minh tail vocabulary nhỏ.

Một simulation sanity check cần có trong validation plan: tạo vocabulary universe với rank-frequency power-law, gán xác suất biết theo band/ability, sinh hai form theo đúng inclusion probabilities của production, rồi so sánh `E_CR` với true `K`. Nếu estimator có bias theo slope power-law hoặc tỷ lệ tail, không đưa vào production.

## 3. Good–Turing và Chao: coverage khác richness

Chao et al. định nghĩa `f_k` là số species xuất hiện đúng `k` lần trong sample; `f1` là singleton và `f2` là doubleton. Good–Turing cho sample coverage một dạng đơn giản dựa trên singleton rate:

```text
C_hat_GT ≈ 1 - f1 / n
```

Trong bài, Chao et al. cũng trình bày hiệu chỉnh dùng thêm `f2`. Đại lượng coverage deficit là phần probability mass của assemblage nằm ở các species chưa phát hiện. Nó **không phải** số lượng hoặc tỷ lệ unseen species. Một tail có rất nhiều species cực hiếm vẫn có thể có coverage deficit nhỏ.

Chao et al. mô tả Chao1 như lower bound không tham số cho số species chưa phát hiện, dùng thông tin singleton/doubleton; khi `f2 > 0`, dạng hiển thị trong bài là:

```text
f0_hat = ((n - 1) / n) * (f1^2 / (2*f2))
```

và có nhánh riêng khi `f2 = 0`. Đây là lower bound trong ecological abundance sampling, không phải một conversion factor cho số từ người học biết. Tác giả còn cảnh báo richness rất khó ước lượng khi có nhiều species gần như không thể phát hiện; coverage có thể ước lượng tốt hơn richness.

Để dựng phần tail của RAD, Chao et al. phải thêm một giả định về functional form, ví dụ geometric series. Họ nhấn mạnh các species cực hiếm ngoài khả năng thống kê có thể được coi là có relative abundance bằng zero trong estimator tail. Đây là lý do một tail model nên được xem là mô hình có điều kiện, không phải “sự thật còn thiếu” tự động được cộng vào điểm.

## 4. Quy tắc thuật toán đề xuất

### 4.1 Estimator chính: finite, stratified, calibrated universe

Định nghĩa vocabulary universe `U` trước khi test:

- lexical unit: lemma/flemma/word-family theo manifest đã khóa;
- frequency corpus, rank, band, POS, sense và domain metadata có version;
- `N_h` là số lexical units hợp lệ trong stratum `h`;
- item sampling probability `π_i` và route probability được lưu cho từng item.

Với response model đã calibration, `p_i = P(known_i | response, ability, item parameters)` là xác suất mastery có điều kiện. Estimator breadth chính:

```text
K_hat = Σ_h N_h * p_hat_h
p_hat_h = (1 / n_h) * Σ_{i in sample_h} p_i
```

Nếu dùng design-based weighted estimator với inclusion probability khác nhau:

```text
K_hat_HT = Σ_{i in observed items} (p_i / π_i)
```

Trong production, `p_i` và `π_i` phải nằm trên cùng lexical-unit universe; không được trộn headword count với word-family count.

### 4.2 Uncertainty của estimator chính

Tách các nguồn sai số thay vì gán tất cả cho unseen tail:

```text
V_sampling ≈ Σ_h N_h^2 * (1 - f_h) * s_h^2 / n_h
V_model    = posterior/model variance from item-person calibration
V_link     = variance from external equating or score conversion
V_total    = V_sampling + V_model + V_link + covariance terms when estimated
```

`CI_primary` được tính trên `K_hat` bằng bootstrap/replicate hoặc model-based interval đã kiểm tra coverage. `tail_sensitivity_range` là một output khác, không cộng vào `K_hat` nếu chưa có hold-out calibration.

### 4.3 Khi nào được phép tính unseen/tail sensitivity

Chỉ chạy tail module nếu tất cả điều kiện sau đều đạt:

- có two-or-more genuinely independent exposure processes, hoặc incidence units được định nghĩa trước;
- exposure probability, replacement/without-replacement và dependence được lưu;
- singleton/doubleton hoặc incidence frequency counts có nghĩa trên cùng population và cùng lexical-unit definition;
- tail model được fit trên calibration data, không chỉ trên một respondent;
- simulation và hold-out kiểm tra bias, interval coverage và sensitivity theo Zipf slope/tail prevalence;
- kết quả được gắn nhãn `model_based_tail`, không gọi là observed vocabulary size.

Nếu thiếu một điều kiện, `unseen_estimate = null`, `unseen_status = "not_identified"`, và báo cáo gap: **“chưa tìm được nguồn xác thực cho hệ số chuyển đổi unseen lexical units thành word count của Preply”**.

## 5. Pseudocode production

```text
function estimate_vocabulary(responses, item_bank, manifest, calibration):
    assert manifest.version == item_bank.manifest_version
    assert every item has lexical_unit_id, stratum, N_h, inclusion_probability

    observed = remove_invalid_or_missing_by_status(responses)
    calibrated = score_with_IRT_or_validated_response_model(observed, calibration)

    for each stratum h in manifest:
        rows = calibrated where row.stratum == h
        if effective_sample_size(rows) < min_band_information[h]:
            band_estimate[h] = NA
            band_flag[h] = "insufficient_information"
        else:
            band_estimate[h] = mean(row.p_known for row in rows)
            band_var[h] = calibrated_or_design_variance(rows)

    K_hat = sum(manifest.N_h[h] * band_estimate[h] for h if estimate exists)
    CI_primary = combine_band_and_model_uncertainty(band_var, calibration)

    tail = null
    if validated_independent_exposure_design(item_bank, responses):
        counts = exposure_frequency_counts(responses)
        coverage = good_turing_or_validated_coverage(counts)
        lower_bound = validated_chao_lower_bound_if_applicable(counts)
        tail_models = fit_tail_models_on_calibration(counts)
        if holdout_coverage_and_bias_pass(tail_models):
            tail = summarize_as_sensitivity_only(coverage, lower_bound, tail_models)

    report = {
        "K_hat": K_hat,
        "CI_primary": CI_primary,
        "tail_sensitivity": tail,
        "unseen_estimate": null if tail is null else tail.validated_value,
        "estimand": manifest.lexical_unit_definition,
        "flags": band_flag + response_quality_flags(observed)
    }
    return report
```

Không có nhánh `K_hat = K_hat + f(unseen)` mặc định. Đây là hard guard chống việc biến coverage hoặc một lower bound ecological thành số từ người học biết.

## 6. So sánh với cách làm Preply

| Thành phần | CR/Good–Turing tail module | Estimator đề xuất | Preply trong bằng chứng đã có |
|---|---|---|---|
| Đối tượng đo | Species/types được capture trong sampling process | Lexical-unit mastery trên universe versioned | Các chapter trước mô tả một vendor receptive breadth scale; methodology production chưa có item/response data công khai đã xác minh độc lập |
| Đơn vị | Phụ thuộc species/type và exposure | lemma/flemma/word-family được khóa rõ | Cần giữ riêng headword/derived-form mapping; chưa có production manifest để xác nhận thêm |
| Tín hiệu | Overlap hoặc singleton/doubleton | `p_known` theo band, item model và inclusion weight | Không được suy ra CR/GT nếu vendor không công bố thiết kế tương ứng |
| Tail | Model-based, dễ sai với Zipf và heterogeneity | `null` mặc định; chỉ sensitivity sau validation | Chưa tìm được nguồn xác thực cho unseen-word bonus hay hệ số tail riêng của Preply |
| Uncertainty | Coverage không phải richness; lower bound không phải point truth | `CI_primary` + `tail_sensitivity_range` tách biệt | Không dùng margin vendor trước đây như bằng chứng coverage cho CR/GT |
| Quyết định phát hành | Không phát hành unseen count nếu thiếu assumptions/hold-out | Có hard-fail `not_identified` | Giữ các gap Preply hiện có, không lấp bằng extrapolation |

Endpoint Preply trực tiếp trả 403 trong callback này, nên bảng chỉ ghi trạng thái bằng chứng chứ không thêm claim mới về implementation vendor.

## 7. Validation plan

### Simulation

1. Tạo universe với nhiều kích thước `K_true`, band counts `N_h` và lexical-unit definitions.
2. Tạo rank-frequency theo các slope Zipf khác nhau, có common-word concentration và tail heterogeneity.
3. Tạo person ability và `P(known)` theo item difficulty; thêm guessing/slip, response dependence và missingness.
4. Sinh forms theo inclusion probabilities thật: uniform trong band, unequal band allocation, CAT/MST routing và common anchors.
5. So sánh CR, Good–Turing coverage, Chao1 lower bound và estimator stratified/IRT với `K_true`.
6. Ghi bias, RMSE, empirical interval coverage, tail sensitivity và failure rate ở floor/ceiling.

### Calibration/hold-out

- Calibration sample phải có đủ ability range và các band được công bố.
- Tail module chỉ được fit trên calibration split; đánh giá trên hold-out split chưa dùng để chọn model.
- Kiểm tra nominal 90%/95% coverage của `CI_primary` và coverage riêng của mọi tail interval.
- So sánh direct breadth với independent vocabulary criterion, không coi text type count là ground truth receptive knowledge.
- Nếu dùng hai forms, dùng common-item equating để kiểm tra growth/reliability; không lấy form overlap làm `X` cho CR.
- Stress-test khi frequency corpus/version, word-family grouping, domain và response quality thay đổi.

### Production monitoring

- Theo dõi `f1`, `f2`, effective sample size và band-specific missingness chỉ như diagnostic.
- Theo dõi item exposure và form overlap để bảo mật/alternate-form control; exposure lặp lại không đồng nghĩa lexical mastery.
- Nếu `tail_sensitivity_range` rộng hơn policy threshold hoặc CR/GT khác biệt mạnh giữa manifests, giữ `unseen_estimate=null` và phát hành gap flag.
- Recalibrate khi corpus manifest, lexical-unit grouping, item bank hoặc response model đổi version.

## 8. Assumptions và gaps

### Assumptions có thể chấp nhận nếu được kiểm tra

- Vocabulary universe hữu hạn, versioned và có `N_h` biết được hoặc ước lượng độc lập.
- Item inclusion probabilities và frequency strata được lưu chính xác.
- Response model đã fit trên population tương thích và được kiểm tra item fit, DIF, local dependence và calibration.
- Domain/token coverage được báo tách khỏi breadth count.

### Không được giả định âm thầm

- Tất cả lexical units có cơ hội được hỏi như nhau.
- Một câu đúng là một lexical unit chắc chắn đã mastered.
- Hai form độc lập chỉ vì chúng có prompt khác nhau.
- `1 - f1/n` là tỷ lệ từ người học chưa biết.
- Chao1 lower bound là số từ thật hoặc có thể cộng thẳng vào score.
- Có một hệ số universal chuyển unseen types thành receptive word count.

### Gaps

- Chưa có item bank, response-level production data, route/inclusion probabilities hoặc independent calibration sample của Preply để kiểm tra bất kỳ unseen estimator nào.
- Chưa có bằng chứng xác thực cho một `unseen_word_bonus`, CR overlap rule hoặc Good–Turing conversion riêng của Preply.
- Bằng chứng capture–recapture đã fetch là productive vocabulary và/hoặc ecological analogy; không đủ để cấp phép cho receptive online score.
- Chưa có validation cho việc singleton/doubleton của response exposures có thỏa sampling model cần thiết hay không.

## Quyết định iteration

`K_hat` frequency-stratified/IRT là estimator phát hành. Capture–recapture, Good–Turing và Chao1 chỉ là diagnostic hoặc sensitivity module sau khi được chứng minh bằng thiết kế exposure và hold-out. Không có dữ liệu đó, báo cáo khoảng bất định của estimator chính và ghi `unseen_estimate=null`; không trình bày tail extrapolation như số từ quan sát được.
