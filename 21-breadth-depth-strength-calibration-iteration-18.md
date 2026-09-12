# Iteration 18: breadth–depth và calibration graded word knowledge

## 1. Phạm vi và nguồn đã kiểm tra

Hướng này kiểm tra một câu hỏi khác với việc đếm frequency rank: một bài vocabulary-size có nên biến mọi phản hồi thành một con số “số từ biết”, hay nên tách **breadth** (độ rộng/form–meaning receptive knowledge) khỏi **depth/strength** (mức độ biết một từ và cách dùng từ).

Hai bản PDF học thuật đã được tải trực tiếp bằng `curl` với browser user-agent và trả HTTP 200 trước khi trích dẫn:

1. Read & Dang, *Measuring depth of academic vocabulary knowledge* (accepted version; Language Teaching Research, bản online 2022): [PDF](https://eprints.whiterose.ac.uk/id/eprint/193066/3/Read-Dang+(2022)+pre-publication+version.pdf).
2. Feng Teng, *Assessing the Depth and Breadth of Vocabulary Knowledge with Listening Comprehension*, PASAA 48 (2014): [ERIC PDF](https://files.eric.ed.gov/fulltext/EJ1077893.pdf).

Các hệ số dưới đây là kết quả của những mẫu/ngữ cảnh cụ thể; chúng là bằng chứng để thiết kế và đặt validation gate, không phải tham số production có thể sao chép.

## 2. Bằng chứng chính

### 2.1 Breadth và depth là hai output liên quan nhưng không đồng nhất

Read–Dang phân biệt breadth là số lượng từ được biết theo cách đo của size/levels test, còn depth là mức độ hiểu các khía cạnh khác của từ ngoài liên kết form–meaning. Trên 222 sinh viên năm nhất trong chương trình EAP tại Việt Nam, tổng UVLT và Depth Test có tương quan `r = .64`, tương đương khoảng 41% phương sai chung. Phần phương sai còn lại là cảnh báo thực nghiệm rằng một điểm breadth không chứa đủ thông tin để suy ra strength/depth của từng người.

Teng nghiên cứu 88 người học tiếng Trung đã qua CET4. Trong mẫu đó, depth có tương quan `r = .91` với listening comprehension; đưa depth vào hồi quy sau VST làm tăng `R²` thêm 2.6%. Đây là lý do depth có thể là tín hiệu bổ sung cho một use case như listening, nhưng không phải hàm quy đổi phổ quát từ vocabulary size sang listening: mẫu nhỏ, một L1, một bối cảnh và một bộ test.

**Quyết định:** output chính vẫn là `breadth_estimate` với unit và universe rõ ràng. Nếu sản phẩm cần strength, thêm `depth_profile` tách biệt; không cộng điểm depth vào word count.

### 2.2 Các facet depth có difficulty và reliability khác nhau

Depth Test của Read–Dang có ba phần:

| Facet | Nội dung | Số item | Mean normalized /10 | Cronbach alpha |
|---|---|---:|---:|---:|
| A | Synonyms/semantic associates | 60 | 5.70 | .94 |
| B | Collocations | 30 | 4.25 | .75 |
| C | Word parts (inflected/derived forms) | 60 | 5.33 | .90 |
| Tổng | A+B+C | 150 | — | .95 |

Khác biệt facility giữa ba phần có ý nghĩa (`eta² = .44`). Part B vừa ít item hơn vừa khó hơn và có alpha thấp hơn. Nếu cộng raw scores, Part A/C sẽ có trọng lượng item lớn hơn Part B; nếu normalize rồi lấy trung bình, vẫn cần chứng minh ba facet cùng một latent construct và có measurement invariance. Không quy tắc nào trong hai cách trên tự động tạo ra “số từ biết”.

**Quyết định:** lưu điểm từng facet, `n_answered`, SE/CI hoặc conditional error từng facet. Chỉ tạo `depth_total` sau khi pilot xác nhận mô hình đo; nếu chưa, trả vector profile thay vì một tổng điểm có vẻ chính xác.

### 2.3 Not Sure là một facet của response process, không phải guessing correction

Read–Dang thêm `Not Sure` vào collocation và word-parts sau phản hồi của người học. Bài ghi rõ việc dùng lựa chọn này tạo thêm nguồn phương sai là willingness to use it. Trong nhóm 2K+ (47 người), ở Part B có 29 người (62%) chọn Not Sure không quá 5 lần, nhưng một số chọn 13–19 lần; ở Part C có người không chọn lần nào và có người chọn 21–22 lần.

Tác giả cho rằng nhóm này có xu hướng thận trọng và có thể under-report, nhưng đồng thời nhấn mạnh cần nghiên cứu thêm vai trò của Not Sure và khác biệt cá nhân. Vì vậy:

- `not_sure` phải là response status riêng, không gộp vào wrong trong mọi phân tích;
- dùng tỷ lệ Not Sure như diagnostic/sensitivity covariate;
- không trừ một penalty cố định và không coi người ít chọn Not Sure là chắc chắn biết nhiều hơn;
- kiểm tra sensitivity: score với Not Sure = missing, = wrong, và model-based partial information sau calibration.

### 2.4 Mastery cut score phụ thuộc purpose và sampling error

Với UVLT, bài mô tả ngưỡng 29/30 (97%) do Webb et al. khuyến nghị ở các band tần suất cao. Read–Dang cho rằng 29/30 có thể quá nghiêm ngặt vì measurement error và sampling từ frequency list, nên dùng 27/30 (90%) cho mục đích diagnostic. Bài cũng dẫn criterion-referenced guidance: placement/diagnosis và minimum achievement có thể cần các cut point khác nhau.

**Quyết định:** không nhúng `29/30` hay `90%` như ngưỡng chung. Một mastery decision hợp lệ cần:

```text
mastered_b = 1 nếu lower_CI(p_hat_b) >= cut_b
            0 nếu upper_CI(p_hat_b) < cut_b
            indeterminate nếu CI cắt qua cut_b
```

`cut_b` phải có mục đích, quần thể và validation criterion đã đăng ký trước. Nếu bài chỉ nhằm ước lượng tổng vocabulary size, không biến band score ít item thành claim mastery chắc chắn.

### 2.5 Không được so sánh raw score giữa breadth và depth test

Read–Dang báo mean UVLT `71.7/150` và diễn giải xấp xỉ `2,370/5,000 word families` dưới giả định các item đại diện cho 5.000 family. Cùng nghiên cứu có Depth Test mean `78.93/150`, nhưng nói rõ không có ý nghĩa khi so sánh hai mean vì thiết kế và mẫu từ khác nhau.

Đây là rule quan trọng cho thuật toán: phép mở rộng `p_hat × N` chỉ hợp lệ cho đúng universe/stratum mà item đại diện. Hai test cùng có 150 item không làm chúng cùng scale.

## 3. Thiết kế thuật toán cập nhật

### 3.1 Data model bổ sung

```text
BreadthResult {
  estimate, unit, universe_version, band_results[],
  se, ci95, sampling_method, quality_flags
}

DepthResult {
  profile: {
    semantic_associate: {score, n, se_or_conditional_error},
    collocation:       {score, n, se_or_conditional_error},
    word_parts:        {score, n, se_or_conditional_error}
  },
  not_sure_rate_by_facet,
  depth_scale_version,
  status = calibrated | diagnostic_only | insufficient_data
}

DepthItem {
  item_id, target_unit, facet, sense_id, response_format,
  correct_key, not_sure_allowed, domain, form_version,
  pilot_difficulty, pilot_discrimination, DIF_flags
}
```

### 3.2 Scoring breadth

Giữ estimator đã có trong report:

```text
p_hat_b = mean(correct observed responses in band b)
V_hat   = sum_b N_b * p_hat_b
```

Khoảng uncertainty dùng variance/replicate bootstrap phù hợp với sampling design. `V_hat` không bao gồm tự động construct bias, domain shift, depth uncertainty hay criterion-linking uncertainty.

### 3.3 Scoring depth trước calibration

Với mỗi facet `k`, báo tỷ lệ đúng quan sát được:

```text
q_hat_k = correct_k / eligible_observed_k
```

Nếu cần scale mô tả trong dashboard, normalize theo norm sample đã version hóa:

```text
z_k = (q_hat_k - mean_k) / sd_k
profile = {z_semantic_associate, z_collocation, z_word_parts}
```

Đây chỉ là profile diagnostic. Không được đặt `depth_words = c * depth_score` vì chưa có bằng chứng mapping và các facet không cùng difficulty/reliability.

Sau calibration, có thể fit một multidimensional IRT/latent model hoặc một model facet-specific. Khi đó output phải giữ `depth_scale_version`, item parameters, SE/credible interval và population calibration. Một aggregate depth score chỉ được công bố nếu model fit, reliability/conditional precision và invariance đạt gate đã đăng ký.

### 3.4 Pseudocode

```text
function estimate_vocab_with_profile(session, breadth_bank, depth_bank, manifest):
    assert session.universe_version == manifest.universe_version

    breadth_responses = administer_breadth_items(
        session,
        stratified_or_safe_adaptive_sampling(breadth_bank),
        preserve_anchors=true
    )
    breadth = weighted_breadth_estimate(
        breadth_responses,
        inclusion_probabilities=true,
        ci_method="design_or_replicate_bootstrap"
    )

    depth_responses = administer_depth_items(
        session,
        balanced_by_facet=depth_bank,
        record_status=["answered", "wrong", "not_sure", "omitted", "timeout"],
        do_not_convert_to_breadth=true
    )

    for facet in [semantic_associate, collocation, word_parts]:
        observed = responses(depth_responses, facet, status="answered")
        profile[facet] = score_rate_and_error(observed)
        profile[facet].not_sure_rate = rate(depth_responses, facet, "not_sure")

    if depth_calibration_available(manifest, session.population):
        depth = calibrated_facet_model(depth_responses, manifest.depth_scale_version)
        depth.status = "calibrated"
    else:
        depth = standardized_diagnostic_profile(profile)
        depth.status = "diagnostic_only"

    diagnostics = {
        "breadth_quality": breadth_quality_flags(breadth_responses, breadth),
        "depth_quality": depth_quality_flags(depth_responses, profile),
        "not_sure_sensitivity": sensitivity_runs(depth_responses),
        "cross_construct_conversion": "disabled"
    }
    return breadth, depth, diagnostics
```

### 3.5 Stopping rules

- Breadth dừng theo CI width/SE và band quanh ngưỡng quyết định, như đặc tả trước.
- Depth dừng khi mỗi facet có đủ precision đã pre-register hoặc đạt `max_depth_items`.
- Không dừng depth vì một facet dễ đã đạt ceiling trong khi collocation còn chưa được đo.
- Nếu `Not Sure` hoặc missing tập trung ở một facet, trả `indeterminate`/flag thay vì ép thành wrong.
- Nếu chỉ có đủ dữ liệu cho breadth, không cần kéo dài bài để tạo depth giả; trả breadth hợp lệ và ghi `depth_status = unavailable`.

## 4. So sánh với Preply

| Thuộc tính | Preply methodology đã công khai | Thiết kế đề xuất cập nhật |
|---|---|---|
| Estimand | Dictionary main entries/headwords theo pipeline BNC được mô tả | Breadth unit công bố rõ; depth là output riêng |
| Nhiệm vụ | Hai giai đoạn, broad screening khoảng 40 từ rồi narrow khoảng 120 từ; midpoint theo rank | Breadth stratified/IRT sau calibration; có thể dùng routing nhưng giữ estimand |
| Depth/strength | Chưa thấy công bố response-level depth facets trong methodology đã kiểm tra | Semantic associate, collocation, word parts; không đổi thành word count |
| Guessing/Not Sure | Chưa tìm được nguồn xác thực cho production rule | Log `Not Sure`/missing riêng, sensitivity và calibration trước penalty |
| Mastery | Không phải mục tiêu midpoint chính đã công khai | Cut score theo purpose + CI; trạng thái indeterminate nếu CI cắt ngưỡng |
| Uncertainty | Vendor-stated margin khoảng ±10%, phụ thuộc rank-sampling model | Tách sampling/measurement/construct/domain uncertainty; depth có SE riêng |
| Cross-scale | Chưa có hệ số xác thực headword → depth/lemma/word family | Cấm conversion nếu chưa có common-person/common-item/criterion calibration |

Methodology Preply hiện chưa cung cấp item bank, response data hoặc tài liệu xác minh depth/strength calibration. Vì vậy bảng trên chỉ nói “đã công khai/không thấy công bố trong trang đã kiểm tra”, không kết luận hệ thống production không có các kiểm soát ẩn.

## 5. Validation plan

1. **Common-person design:** cùng người làm breadth test và từng depth facet; cân bằng order và form.
2. **Independent criteria:** reading và listening tests cho intended use; constructed meaning-recall/translation chỉ làm criterion nếu được chấm theo rubric và kiểm tra reliability.
3. **Item calibration:** tối thiểu kiểm tra facility, discrimination, local dependence, DIF theo L1/proficiency/age và facet-specific conditional error.
4. **Not Sure experiment:** randomize/compare forced-choice, Not Sure-as-missing và Not Sure-as-wrong; đo criterion association và subgroup response propensity.
5. **Mastery study:** pre-register cut scores cho placement, diagnosis hoặc course achievement; kiểm tra CI coverage và false classification gần cut.
6. **Hold-out:** khóa item parameters trên calibration sample, đánh giá breadth CI coverage, depth reliability và criterion prediction trên sample độc lập.
7. **Transport audit:** không chuyển các hệ số `r=.64`, `r=.91`, `R² change=2.6%`, alpha hay normalized means sang Preply/population khác nếu chưa replicate.

## 6. Gap còn lại

- Chưa có response-level/item-bank data của Preply để xác định họ có depth layer, Not Sure, recall, collocation hay word-part items hay không.
- Chưa có mapping đã calibration giữa Preply headwords và depth/lemma/word-family units.
- Chưa có sample mục tiêu để ước lượng facet parameters, measurement invariance, mastery cut scores hoặc CI coverage.
- Chưa có bằng chứng đủ để map depth profile sang CEFR/IELTS hay điểm listening/reading cá nhân.

Kết luận iteration: **đếm breadth và mô tả strength là hai nhiệm vụ đo khác nhau**. Bản production an toàn trả breadth estimate có uncertainty; depth profile chỉ là diagnostic cho tới khi có calibration và validation độc lập.
