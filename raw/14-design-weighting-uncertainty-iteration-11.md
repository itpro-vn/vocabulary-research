# Iteration 11 — Design-based weighting và calibration độ không chắc chắn

## 1. Phạm vi và kết luận

Iteration này kiểm tra một vấn đề khác với việc chọn frequency bands hay fit IRT: nếu item được lấy với xác suất khác nhau giữa các band/domain, điểm tổng phải được tính như một estimator có thiết kế lấy mẫu, không phải như tỷ lệ đúng của simple random sample. Nguồn vocabulary cho thấy các band 1.000 từ là quy ước hữu ích nhưng không đảm bảo các band có cùng độ khó; nguồn survey/measurement chính thống cung cấp cách giữ lại trọng số, design effect, replicate weights và SEM.

Kết luận triển khai:

1. Xác định rõ population/frame `U` và estimand `T`: số headword, lemma hay word family; general English hay domain/TLU. Không được dùng một CI để che cả sampling error, measurement error và frame/construct bias.
2. Mỗi item cần có `stratum`, `domain`, `inclusion_probability` hoặc xác suất tương đương sau adaptive routing. Nếu thiết kế stratified/adaptive làm các xác suất này khác nhau, dùng trọng số inverse-probability rồi calibrate theo target stratum totals.
3. Độ không chắc chắn sản phẩm nên có ít nhất hai lớp: (a) conditional score uncertainty, từ đáp ứng và item model; (b) design uncertainty, từ việc item sample đại diện frame. Bias do frame, domain shift, cognate/DIF hoặc headword↔word-family mapping phải là sensitivity/gap, không được giả vờ nằm trong CI.
4. Với estimator có routing/weighting, dùng replicate-weight/bootstrap theo đúng design để ước lượng interval và kiểm tra coverage. Chỉ dùng `n` thô là không đủ; báo effective sample size/design effect và quality flag.

## 2. Bằng chứng đã kiểm tra

### 2.1 Frequency band không đồng nghĩa với equal difficulty

Meara (tài liệu vocabulary tests, HTTP 200) gọi việc chia lexicon thành các khối 1.000 từ là “convenient fiction” và cảnh báo frequency lists có thể không đại diện cho độ khó thực tế của người học hoặc loại ngôn ngữ L2 họ tiếp xúc. Tài liệu đề xuất cần một source list phản ánh xác suất người học biết item và có dữ liệu thực nghiệm. Vì vậy frequency rank là biến thiết kế/stratification, không nên được dùng như xác suất biết từ hoặc trọng số độ khó mà chưa calibration.

Nguồn: [Meara 1992 vocabulary tests](https://lognostics.co.uk/vlibrary/meara1992z.pdf).

### 2.2 Sampling rate và replicate forms

Meara mô tả 40 real words + 20 imaginary words trên một list khoảng 1.000 từ, tức khoảng 1/25 list cho mỗi test; nhiều test cùng level làm tăng sampling rate và độ ổn định. Tài liệu cũng cảnh báo bộ test khi đó chưa được validation trên một population L2 lớn. Đây là cơ sở cho việc tăng số item/replicate khi cần precision, nhưng không phải hệ số reliability có thể bê nguyên sang item bank mới.

Cùng nguồn ghi rằng công thức cũ dùng YES trên imaginary words từng có giả định toán học sai và các correction trước đó không hoàn toàn thỏa đáng. Do đó pseudoword/false-alarm nên là covariate/quality signal cho tới khi có pilot chứng minh correction và coverage.

### 2.3 Design-based variance và effective sample size

CDC/NCHS định nghĩa effective sample size trong complex survey là sample size chia cho design effect. Design effect so sánh variance đã tính clustering, stratification và unequal selection probabilities với variance của simple random sample cùng cỡ. CDC khuyến nghị đánh giá cả effective `n`, design effect, CI width, degrees of freedom và relative standard error.

Nguồn: [CDC/NCHS Reliability of Estimates](https://wwwn.cdc.gov/nchs/nhanes/tutorials/reliabilityofestimates.aspx).

### 2.4 Replicate weights/bootstrap không loại bias

Statistics Canada phân biệt random component (variance) với systematic component (bias). Tài liệu variance Census mô tả replicate samples/weights phải trải qua cùng coverage, non-response và calibration adjustments; các replicate estimates sau đó dùng để ước lượng variance. Tài liệu bootstrap mô tả lặp resampling `B` lần để tạo variance và CI.

Áp dụng cho vocabulary: bootstrap cần resample theo strata/routing hoặc dùng replicate weights, không resample ngây thơ toàn bộ item nếu điều đó phá vỡ sampling design. Tuy nhiên interval vẫn chỉ phản ánh những nguồn biến thiên được mô hình hóa; nó không tự bù frame bias, domain mismatch hay sai estimand.

Nguồn: [Statistics Canada — variance estimation](https://www12.statcan.gc.ca/census-recensement/2021/ref/98-306/2021001/chap6-eng.cfm); [Statistics Canada — bootstrap variance estimation](https://www150.statcan.gc.ca/n1/pub/12-001-x/2021002/article/00005/03-eng.htm).

### 2.5 SEM và diễn giải thay đổi

Tài liệu ETS về GRE định nghĩa SEM là biến thiên điểm do measurement error; khoảng khoảng 95% quanh true score được mô tả gần đúng bởi ±2 SEM. Khi so sánh hai lần đo, cần SEM của score differences vì thay đổi nhỏ có thể chỉ là measurement error.

Nguồn: [ETS Reliability and Standard Error of Measurement](https://www.eu.ets.org/pdfs/gre/gre-reliability-standard-error-measurement.pdf).

### 2.6 Đối chiếu Preply

Trang methodology của Preply được fetch qua proxy `r.jina.ai` HTTP 200. Preply mô tả vocabulary size như một mean được sampling theo rank; với khoảng 22,5 sample và 120 từ ở phase hai, họ tính standard error `0,0527`, nhân `1,96` thành khoảng `±10,33%`, và nêu cần thêm khoảng 380 từ để đạt 5% hoặc tổng khoảng 12.000 từ để đạt 1%. Đây là interval có điều kiện theo mô hình rank/sample của Preply. Nó không chứng minh rằng dictionary-headword frame, domain coverage, cognate/DIF, guessing hay mapping sang word-family đã được hiệu chỉnh.

Nguồn: [Preply methodology](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works).

## 3. Estimator đề xuất

### 3.1 Dữ liệu item bắt buộc

Mỗi item version nên có:

```text
item_id, frame_version, estimand_unit, stratum_id, domain_id,
selection_probability pi_i, target_weight q_i, form_id, anchor_flag,
IRT parameters (nếu có), DIF flags, pseudoword_flag, position,
known/unknown response, response quality metadata
```

`pi_i` là xác suất item được đưa tới examinee dưới thiết kế/routing hiện tại. Với CAT, phải tính hoặc log xác suất lựa chọn thực tế; không dùng frequency rank thay cho `pi_i`. `q_i` là target mass của item/stratum trong estimand. Nếu target là tổng số đơn vị trong các stratum, cần lưu `N_h` hoặc target proportion `Q_h` theo frame version.

### 3.2 Stratified design estimator

Với stratum `h`, có `N_h` đơn vị trong frame, `n_h` item được quan sát, đáp ứng kiến thức `y_hi` (0/1), và xác suất đưa item `pi_hi`, estimator của proportion biết trong stratum là:

```text
p_hat_h = sum_i [ y_hi / pi_hi ] / sum_i [ 1 / pi_hi ]
```

Nếu dùng target stratum mass `Q_h`, vocabulary breadth estimate là:

```text
V_hat = sum_h Q_h * p_hat_h * N_h
```

hoặc nếu `Q_h` đã là số đơn vị thay vì proportion:

```text
V_hat = sum_h N_h * p_hat_h
```

Không trộn hai convention. Với IRT/CAT, thay `y_hi` bằng posterior expected mastery `m_hi = P(K_hi=1 | response, theta)` hoặc dùng person ability rồi map sang frame bằng calibration; phải validate mapping đó trên common-person/common-item pilot.

Để tránh một item có trọng số quá lớn khi `pi_i` nhỏ, dùng weight trimming/capping chỉ khi có pre-specified rule, sau đó re-normalize trong stratum và báo sensitivity trước/sau trimming. Trimming thay đổi estimand/variance trade-off, không phải phép sửa miễn phí.

### 3.3 Variance và interval

Bản production nên tính ba quantity riêng:

1. `SE_design`: biến thiên do item sampling/routing, ước lượng bằng stratified bootstrap hoặc replicate weights giữ nguyên `N_h`, `pi_hi`, routing và calibration.
2. `SE_measurement`: biến thiên từ item/person model, ví dụ posterior SD hoặc conditional SEM tại `theta_hat`.
3. `Bias_sensitivity`: chênh lệch khi thay frame version, domain weights, cognate/DIF exclusion, headword↔lemma mapping hoặc guessing policy.

Một interval đơn giản cho score scale đã calibration là:

```text
SE_total = sqrt(SE_design^2 + SE_measurement^2)
CI_95 = estimate +/- 1.96 * SE_total
```

Chỉ dùng phép cộng phương sai này khi hai thành phần được xem là tách biệt và pilot xác nhận; nếu covariance hoặc model uncertainty đáng kể, dùng bootstrap lồng (outer design replicate, inner response/model draw) hoặc posterior predictive interval. Report phải ghi rõ CI nào được phát hành.

Effective sample size dùng để quality flag, không thay thế variance estimator. Với normalized weights `w_i`:

```text
n_eff = (sum_i w_i)^2 / sum_i w_i^2
DEFF_weight = n / n_eff
```

Đây là diagnostic đơn giản; nếu có clustering/local dependence hoặc CAT information curve, design effect phải lấy từ replicate/bootstrap variance thay vì chỉ từ weight dispersion.

## 4. Pseudocode production

```text
function score(response_log, item_bank, frame, target_profile):
    validate_versions(response_log, item_bank, frame)
    rows = join(response_log, item_bank, keys=[item_id, version])
    rows = apply_quality_policy(rows)       # không âm thầm xóa; ghi reason

    for row in rows:
        assert 0 < row.selection_probability <= 1
        row.weight = 1 / row.selection_probability
        row.mastery = calibrated_mastery(row)  # hoặc y=0/1 cho direct score

    for stratum h in target_profile.strata:
        R_h = rows where stratum_id == h
        if count(R_h) < minimum_items(h):
            flag('under_sampled_stratum', h)
        p_h = sum(r.weight * r.mastery for r in R_h) / sum(r.weight for r in R_h)
        p_h = clamp(p_h, 0, 1)

    estimate = sum(target_profile.N[h] * p_h for h)
    design_reps = generate_replicates_preserving_strata_and_routing(rows)
    rep_estimates = [score_point(rep, target_profile) for rep in design_reps]
    se_design = sd(rep_estimates) * replicate_scale
    se_measurement = conditional_sem_or_posterior_sd(rows)
    se_total = combine_uncertainty(se_design, se_measurement)

    n_eff = effective_n(rows.weight)
    flags = quality_flags(n_eff, se_total, coverage_pilot_status,
                          frame_version, domain_profile, DIF_status)
    return estimate, interval(estimate, se_total), n_eff, flags,
           separate_bias_sensitivity(rows, target_profile)
```

`generate_replicates_preserving_strata_and_routing` phải được test bằng simulation: nếu CAT/adaptive routing làm item probabilities phụ thuộc response history, replicate phải tái hiện routing hoặc dùng logged selection probabilities; resample response rows như IID sẽ đánh giá thấp uncertainty.

## 5. Bảng so sánh với Preply

| Thành phần | Preply đã công bố | Đề xuất research-grade |
|---|---|---|
| Frame/đơn vị | Dictionary entries/headword theo methodology; khác word-family/lemma | Version hóa frame; công bố estimand và mapping riêng |
| Chọn item | Hai phase, rank/logarithmic sampling; phase hai khoảng 120 từ | Stratified/adaptive nhưng log `pi_i`, domain, form, anchor và routing |
| Điểm | Midpoint/rank estimate theo sample known/unknown | IPW/stratified estimator hoặc IRT-to-frame calibration |
| Guessing | Không thấy production coefficient xác thực trong dữ liệu hiện có | Pseudoword/false-alarm là diagnostic cho tới khi pilot chứng minh correction |
| Uncertainty | Vendor nêu khoảng ±10,33% theo mô hình 22,5 samples và phase hai | Tách `SE_design`, `SE_measurement`, bias sensitivity; bootstrap/replicate CI |
| Quality | Không có item-bank/response-level production data để kiểm tra độc lập | Effective n, design effect, CI width, under-sampled strata, DIF/domain flags |
| Retest | Không có dữ liệu production xác thực về common anchors | Common-anchor equating + SEM của score difference + reliable-change rule |
| Claim | Fast user-facing estimate | Xuất general estimate và domain/TLU estimate riêng; không gọi CI là bảo đảm chống bias |

## 6. Validation plan và gaps

1. **Frame census simulation:** biết toàn bộ `N_h` và mastery thật của một benchmark frame; mô phỏng Preply-style rank sampling, equal-strata và adaptive/IPW sampling. Kiểm tra bias, RMSE, CI coverage và ảnh hưởng của weight trimming.
2. **Pilot response data:** tối thiểu đủ L1/proficiency/domain groups để ước lượng `pi_i`, item difficulty, DIF, pseudoword false-alarm và conditional SEM; chia train/calibration/hold-out theo người, không chỉ theo item.
3. **Replicate-form test:** tạo forms với common anchors; so sánh raw score, IPW score và IRT-linked score. Kiểm tra retest SEM và reliable-change threshold.
4. **Coverage audit:** nếu target là ±10%, kiểm tra empirical coverage trên repeated samples; không suy ra coverage từ công thức Preply hoặc từ normal approximation một lần.
5. **Domain sensitivity:** tính general estimate với `Q_h` chung và TLU estimates với curriculum/domain weights; báo chênh lệch như construct choice, không chọn giá trị thuận tiện.

Còn thiếu dữ liệu production của Preply: item bank, selection probabilities/routing log, raw responses, frame-to-lemma/word-family map, domain weights, independent criterion sample và coverage validation. Vì vậy chưa thể tuyên bố hệ số quy đổi hay CI production của Preply đã được xác minh độc lập.
