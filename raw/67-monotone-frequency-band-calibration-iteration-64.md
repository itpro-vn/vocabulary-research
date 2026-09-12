# Iteration 64 — Monotone frequency-band calibration và shape-constrained scoring

## 1. Phạm vi và câu hỏi

Direction của iteration này là kiểm tra một giả định thường được dùng nhưng dễ bị biến thành luật cứng: người học thường biết nhiều lexical units ở band tần suất cao hơn band tần suất thấp, nên profile `p_known` có thể được kỳ vọng giảm theo rank tần suất. Mục tiêu là phân biệt:

1. bằng chứng thực nghiệm rằng frequency vẫn là tín hiệu có thứ tự;
2. giả định monotonicity của mô hình đo lường;
3. phép regularize dữ liệu nhiễu bằng isotonic/PAVA;
4. trường hợp reversal là tín hiệu thật của domain, subgroup, item defect hoặc construct khác và không được xoá.

Kết luận áp dụng cho thuật toán đề xuất, không phải mô tả implementation nội bộ của Preply.

## 2. Nguồn đã fetch và verify

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| Tanabe, *Measuring second language vocabulary knowledge using a temporal method* | 200 | Kết quả accuracy theo frequency band; thiết kế band, part-of-speech, stem burden và option randomization. |
| Firoozi, *Mokken Scale Analysis of the Reading Comprehension Section of IELTS* | 200 | Giả định MHM: unidimensionality, monotonicity, local independence; ví dụ violation và scalability/fit. |
| Dai et al., *The bias of isotonic regression* | 200 | Cảnh báo lý thuyết rằng shape-constrained estimator có bias riêng; không dùng như CI của vocabulary test. |
| Preply, *How does the vocab test work?* qua `r.jina.ai` | 200 | Mô tả vendor về dictionary >45,000 entries, hai phase, midpoint và logarithmic rank sampling. |
| Preply endpoint trực tiếp | 403 | Không dùng trực tiếp để xác minh implementation; không có response-level/item-bank evidence. |

URL đã verify:

- https://files.eric.ed.gov/fulltext/EJ1098666.pdf
- https://files.eric.ed.gov/fulltext/EJ1318850.pdf
- https://arxiv.org/abs/1908.04462
- https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works
- https://preply.com/en/learn/english/test-your-vocab/how-it-works (403, chỉ ghi nhận giới hạn truy cập)

## 3. Bằng chứng

### 3.1 Frequency có trật tự trung bình, nhưng không phải luật phổ quát

Tanabe nghiên cứu 24 sinh viên đại học Nhật bằng breadth test dạng definition–four options. Ở các band 2K, 3K, 4K và 5K, nhóm người tham gia biết nhiều từ hơn ở band tần suất cao; accuracy giảm khi tần suất giảm. Bài cũng nhắc kết quả Aizawa rằng trong JACET8000, điểm trung bình giảm theo frequency nhưng xu hướng dừng giữa 4K và 5K, với core-vocabulary boundary khoảng 5K trong sample đó.

Đây là cơ sở hợp lý cho một prior có hướng `p_2K >= p_3K >= ...`, nhưng sample nhỏ, một L1 và một danh sách frequency cụ thể. Không được biến nó thành quy tắc rằng mọi population, domain hoặc lexical-unit ontology phải đơn điệu. Reversal có thể đến từ domain exposure, cognate/loanword, sense, item defect hoặc sampling noise.

### 3.2 Item construction làm frequency band có ý nghĩa hơn rank đơn độc

Tanabe đặt bốn options trong cùng frequency level, dùng definition không vượt quá level mục tiêu, phân bổ mỗi subtest 10 câu theo tỷ lệ 2 adjective/3 verb/5 noun, và randomize option order. Những kiểm soát này quan trọng vì nếu stem dễ hơn/khó hơn target, part-of-speech bị lệch hoặc correct option thường ở vị trí cố định, profile theo band có thể phản ánh burden/position chứ không chỉ lexical knowledge.

Với item manifest, tối thiểu phải có `band_version`, `frequency_metric`, `lexical_unit`, `part_of_speech`, `stem_burden`, `sense_id`, `option_order_seed` và `calibration_population`. Một band reversal không nên được smoothing trước khi kiểm tra các trường này.

### 3.3 Monotonicity trong Mokken là giả định của thang đo, không phải post-processing

Firoozi mô tả Mokken monotone homogeneity model (MHM) với:

- unidimensionality: một latent trait chung giải thích response;
- monotonicity: xác suất trả lời đúng không giảm khi latent trait tăng;
- local independence: response của các item không phụ thuộc lẫn nhau sau khi điều kiện trên trait.

Nếu MHM fit, raw total score có thể dùng để xếp người làm test trên thang thứ bậc. Double monotonicity model còn yêu cầu invariant item ordering, tức các item-response functions không cắt nhau.

Áp dụng vào vocabulary test cần phân biệt hai thứ tự:

1. **thứ tự theo năng lực người làm test:** xác suất đúng tăng theo latent vocabulary ability;
2. **thứ tự theo frequency band:** band dễ hơn thường có xác suất biết cao hơn, nhưng đây là content/difficulty hypothesis cần kiểm định riêng.

Không thể suy ra thứ tự thứ hai chỉ vì mô hình IRT yêu cầu monotone ICC theo ability.

### 3.4 Violation nhỏ không đồng nghĩa được phép xoá

Trong dữ liệu 40-item IELTS reading của Firoozi (352 sinh viên EFL Ba Tư), item 10, 12 và 28 vi phạm monotonicity. Các violation không có ý nghĩa thống kê; item 28 có `crit=0.57`, cao hơn ngưỡng 0.40 mà bài dùng để nhận diện violation đáng chú ý. Tác giả vẫn giữ item sau khi xem z-value không có ý nghĩa và kết luận MHM phù hợp cho bài đó.

Hệ quả cho vocabulary scoring là cần lưu cả `n_violation`, `z_significance`, `crit`, item/band và population. Quyết định giữ, loại, hoặc pool phải là release decision có kiểm tra sensitivity, không phải một bước vô hình trong code. Nếu reversal lớn hoặc lặp lại theo một subgroup/domain, smoothing có thể che mất non-invariance.

### 3.5 Isotonic regression không miễn nhiễm với bias

Dai và cộng sự nghiên cứu bias của isotonic regression. Abstract nêu rằng dưới mean strictly monotone và noise có đuôi subexponential, bias có tốc độ `O(n^(-β/3))` tới log factors, với `1 <= β <= 2` theo Holder smoothness.

Đây là kết quả lý thuyết thống kê tổng quát, không phải bằng chứng coverage cho vocabulary-size tests. Nó chỉ supports một cảnh báo: `p_iso` là estimator có bias và variance riêng. Vì vậy interval phải được đánh giá bằng respondent/item bootstrap hoặc simulation có data-generating process phù hợp; không được lấy tốc độ lý thuyết này để tuyên bố margin ±10% hay CI cho người dùng.

## 4. Thuật toán đề xuất

### 4.1 Dữ liệu và thứ tự

Với band `b=1..B` được sắp từ frequency cao/easy đến frequency thấp/hard:

```text
N_b       = số lexical units trong vocabulary universe của band b
n_b       = số item được quan sát trong band b
x_b       = số response được chấm là biết/đúng trong band b
p_raw_b   = x_b / n_b                  (hoặc weighted estimate nếu inclusion unequal)
```

Estimand breadth vẫn phải khai báo trước: headword, lemma, flemma hay word family. Nếu universe là finite population và item được lấy xác suất không đều, dùng `p_raw_b` có trọng số inclusion; không dùng isotonic để sửa weighting error.

### 4.2 Weighted PAVA cho profile ứng viên

Ta ước lượng profile đơn điệu không tăng theo frequency rank bằng weighted isotonic regression:

```text
p_iso = argmin_q Σ_b w_b (p_raw_b - q_b)^2
        subject to 1 >= q_1 >= q_2 >= ... >= q_B >= 0
```

`w_b` có thể bắt đầu bằng `n_b` cho sample độc lập, nhưng production phải thay bằng effective information/design weight khi có local dependence, unequal inclusion hoặc IRT information. Dùng PAVA để pool các block vi phạm liền kề; không pool band không liền kề chỉ vì cùng kết quả.

### 4.3 Pseudocode

```text
function estimate_band_profile(responses, manifest, universe, calibration):
    audit_lexical_unit_and_band_versions(manifest)
    audit_stem_pos_sense_and_option_order(manifest)
    audit_missingness_and_cluster_dependence(responses)

    for b in bands_easy_to_hard:
        r_b = responses_for_band(responses, b)
        p_raw[b] = weighted_known_rate(r_b, calibration.inclusion_weights)
        se_raw[b] = band_se(r_b, clusters=respondent_and_item)

    shape_diagnostics = test_monotone_icc_and_band_reversals(
        responses, manifest, population=calibration.population)

    p_iso = weighted_pava_decreasing(p_raw,
                                     weights=effective_band_information(responses))
    K_raw = sum(universe.N[b] * p_raw[b] for b in bands)
    K_iso = sum(universe.N[b] * p_iso[b] for b in bands)

    if not shape_diagnostics.MHM_or_equivalent_ok:
        primary = K_raw
        flag = 'shape_constraint_not_released'
    elif shape_diagnostics.large_or_subgroup_reversal:
        primary = K_raw
        flag = 'domain_or_DIF_review_required'
    else:
        primary = K_iso
        flag = 'monotone_profile_released_with_sensitivity'

    interval = cluster_bootstrap_both_profiles(
        responses, manifest, recompute_weights_and_PAVA=True)
    return primary, K_raw, K_iso, interval, shape_diagnostics, flag
```

### 4.4 Reporting

Luôn lưu:

```text
K_raw, K_iso, delta_shape = K_iso - K_raw
number_of_pooled_blocks, pooled_band_ranges
band_profile_raw, band_profile_iso
CI_raw, CI_iso, bootstrap_method, cluster_definition
shape_test_version, item_bank_version, frequency_manifest_version
population/domain/L1, missingness and quality flags
```

Nếu chưa có calibration criterion hoặc đủ sample per band, chỉ phát hành `K_raw` và profile/uncertainty; `K_iso` là sensitivity analysis. Nếu có calibration và MHM/content/DIF gates đạt, `K_iso` có thể là điểm chính nhưng vẫn phải hiển thị chênh lệch do shape constraint.

## 5. Minh họa tính toán kiểm chứng

Một PAVA chạy cục bộ trên profile minh họa (không phải dữ liệu người dùng) với:

```text
p_raw = [0.92, 0.78, 0.81, 0.55, 0.61, 0.38]
n     = [50,   80,   60,   100,  40,   70]
N_b   = 1000 cho mỗi band
```

Kết quả thực thi:

```text
p_iso     = [0.92, 0.792857, 0.792857, 0.567143, 0.567143, 0.38]
blocks    = [0], [1..2], [3..4], [5]
K_raw     = 4050.0
K_iso     = 4020.0
```

Hai reversal được pool theo trọng số `n_b`; shape constraint giảm điểm minh họa 30 lexical units. Đây không phải confidence interval và không phải hiệu chỉnh đã được validate. Nó chỉ kiểm tra rằng thuật toán tôn trọng thứ tự, giữ nguyên các band không vi phạm, và cho thấy tại sao phải báo `K_raw`/`K_iso` cùng nhau.

## 6. So sánh với Preply

| Thành phần | Thuật toán đề xuất | Preply đã xác minh qua methodology |
|---|---|---|
| Vocabulary universe | Khai báo lexical unit, version và `N_b`; band profile là output riêng | Dictionary hơn 45,000 entries, sắp theo frequency speech/writing; vendor mô tả main entry/derived form |
| Sampling | Có band quota/inclusion weights, item pretest, cluster-aware uncertainty | Hai phase: khoảng 40 item rộng và khoảng 120 item trong vùng hẹp quanh estimate |
| Score | `K_raw = ΣN_b p_raw_b`; `K_iso` chỉ khi shape gates pass; báo sensitivity | Midpoint của checkbox theo frequency rank; sample trong thực tế được phân bố logarithmically |
| Shape check | MHM/local independence, reversal significance, subgroup/domain review, PAVA chỉ là constrained candidate | Trang đã fetch không công bố band-level monotonicity test, isotonic/PAVA hay item-response calibration |
| Uncertainty | Bootstrap/posterior phải recompute profile và PAVA; tách response, sampling, model, transport | Vendor công bố margin khoảng ±10% và giải thích bằng SD/SE của sample points; chưa có independent coverage evidence |
| Response/item calibration | Cần pretest, content controls, item parameters và holdout | Chưa có response-level data, item bank hay calibration sample công khai trong nguồn đã fetch |

Không có nguồn xác thực cho việc Preply có shape-constrained scoring, band pooling, MHM diagnostics hoặc monotonicity-based correction. Không gán các cơ chế này cho Preply.

## 7. Release gates và validation plan

1. **Manifest gate:** cùng frequency metric/corpus version; khai báo lexical unit, sense, part-of-speech, stem burden và population.
2. **Psychometric gate:** kiểm tra unidimensionality, local dependence, monotone ICC và item/band reversals; đánh dấu crit/z và subgroup results.
3. **Model comparison:** so sánh raw, weighted raw, isotonic/PAVA và IRT/hierarchical model trên held-out persons và held-out forms; không chọn theo in-sample fit.
4. **Coverage:** bootstrap theo respondent và item/cluster; đo empirical coverage của `CI_raw` và `CI_iso` trên simulated/holdout populations.
5. **Transport:** lặp lại theo L1, proficiency, age/education, domain và cognate exposure; nếu profile reversal có cấu trúc, phát hành domain profile hoặc raw sensitivity thay vì pool.
6. **Tail:** không extrapolate `p_b` ra ngoài bands đã quan sát chỉ nhờ monotonicity; endpoint/censored estimate phải có flag riêng.
7. **Preply bridge:** chỉ link `K_iso` hoặc `K_raw` sang Preply main-entry scale khi có common-anchor/criterion sample; midpoint/log-rank không chứng minh hai estimand tương đương.

## 8. Gaps

- Chưa có response-level/item-bank data của Preply để kiểm tra band profile, shape constraint, exposure, missingness hoặc coverage.
- Bằng chứng Tanabe/Firoozi không phải calibration cho vocabulary-size product mục tiêu; sample và construct khác nhau ở các phần quan trọng.
- Chưa có dữ liệu để chọn `n_b`, ngưỡng reversal, ngưỡng significance/crit, effective information weight hoặc quyết định raw-vs-isotonic cho population triển khai.
- Chưa tìm được nguồn xác thực cho một công thức universal biến reversal hoặc isotonic profile thành margin-of-error cụ thể.
- Cần pilot có criterion meaning confirmation/recall, item metadata và holdout theo form để kiểm tra `K_iso` có giảm bias hay chỉ làm mất khác biệt domain/subgroup.

## 9. Kết luận iteration

Frequency-band monotonicity là một prior có bằng chứng thực nghiệm ở một số L2 samples, nhưng phải được kiểm tra như giả định đo lường và content hypothesis. Production nên tính song song `K_raw` và weighted monotone `K_iso`, dùng PAVA chỉ sau các gate về lexical-unit/content, MHM/local independence và subgroup/domain diagnostics. Mọi release cần giữ sensitivity `K_iso-K_raw` và interval được bootstrap lại sau pooling; không coi isotonic smoothing là validation, không chuyển lý thuyết bias chung thành margin của Preply.
