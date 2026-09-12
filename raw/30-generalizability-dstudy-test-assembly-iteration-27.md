# Iteration 27 — Generalizability theory, D-study và lắp ráp test

## Phạm vi và nguồn đã kiểm tra

Iteration này tập trung vào một câu hỏi khác với việc chỉ tính CI theo tỉ lệ đúng: **một vocabulary-size score thay đổi bao nhiêu nếu ta thay item, frequency band/section, form hoặc occasion?** Khung được kiểm tra là Generalizability Theory (G-theory), gồm G-study để phân rã variance components và D-study để thử các cấu hình test trước khi triển khai.

Các URL dưới đây đã được fetch bằng `curl -L` với browser User-Agent và trả HTTP 200; ba PDF trực tiếp trả `content-type: application/pdf`:

1. Kumazawa (2009), *Revision of a Criterion-Referenced Vocabulary Test Using Generalizability Theory*, JALT Journal 31.1, pp. 81–100. Nguồn vocabulary-specific: [PDF](https://jalt-publications.org/sites/default/files/pdf-article/art4_2.pdf).
2. Lee (2005), ETS, *Dependability of Scores for a New ESL Speaking Test: Evaluating Prototype Tasks*, RM-04-07. Nguồn phương pháp G/D-study và thiết kế nhiều facet: [PDF](https://www.ets.org/Media/Research/pdf/RM-04-07.pdf). Đây là speaking assessment, nên chỉ dùng để xác nhận nguyên lý thiết kế, không chuyển số liệu sang vocabulary.
3. Jackson (1970), ETS/ERIC, *Developing Criterion-Referenced Tests*, ED041052. Nguồn về định nghĩa content universe và random/stratified sampling, có ví dụ word list/vocabulary: [PDF](https://files.eric.ed.gov/fulltext/ED041052.pdf).

## Bằng chứng chính

### 1. G-study/D-study là phần bổ sung cho estimator, không phải một công thức đổi điểm

Lee mô tả G-study là giai đoạn ước lượng variance của object of measurement và các facet; D-study dùng những variance components đó để mô phỏng số task/rater và thiết kế đo khác nhau. G-theory tách:

- `G` / generalizability coefficient: dùng relative error, thích hợp khi muốn xếp hạng người làm bài tương đối.
- `Phi` / dependability index: dùng absolute error, thích hợp với quyết định criterion- hoặc domain-referenced.

Trong vocabulary-size test, các facet có thể là:

- `p`: người làm bài;
- `b` hoặc `s`: frequency band/section/content stratum;
- `i:b`: item nằm trong band;
- `f`: form hoặc occasion;
- các tương tác `p×i`, `p×b`, `p×f` nếu có dữ liệu đủ.

Điểm quan trọng: một điểm số có thể ổn định để **xếp hạng** nhưng chưa đủ dependable để khẳng định một người biết một số lượng từ tuyệt đối trong một universe cụ thể. Báo cáo nên giữ hai diễn giải này tách nhau.

### 2. Nghiên cứu vocabulary-specific cho thấy form 25 item có dependability tuyệt đối thấp

Kumazawa xây dựng bài multiple-choice vocabulary achievement/diagnostic test với 131 sinh viên. Năm chapter trong 10 chapter được chọn ngẫu nhiên; mỗi chapter lấy 5 target words, tạo 25 item, với item nested trong section. Test chủ yếu đo receptive meaning trong sentence context.

Bảng variance components của nghiên cứu:

| Thành phần | Tỷ lệ variance trong nghiên cứu |
|---|---:|
| Person | 2% |
| Section | 0% (variance âm được làm tròn về 0) |
| Item × section | 46% |
| Person × section | 1% |
| Person × item-within-section | 52% |
| Tổng | 100% |

Với cấu hình 5 section × 5 item (`k=25`), Phi/dependability cho absolute decisions là `.30`. D-study trên cùng cấu hình variance cho thấy:

- 6 section × 5 item (`k=30`): `.34`;
- 6 section × 10 item (`k=60`): `.51`;
- 40 item trong điều kiện giới hạn khoảng 20 phút: `.41`.

Đây là kết quả của một lớp học, một mục tiêu criterion-referenced và một item bank cụ thể, **không phải sai số phổ quát của mọi vocabulary-size test**. Giá trị của nó đối với thiết kế là cảnh báo trực tiếp: một form ngắn có thể bị item effect và person×item interaction chi phối; vì vậy không được gắn một margin of error cố định cho mọi người dùng chỉ từ số câu.

### 3. Content universe và cấu trúc sampling phải được khai báo trước

Jackson/ERIC nêu điều kiện để suy luận từ kết quả item ra một domain: universe item phải được xác định trước và item của form phải được chọn bằng random hoặc stratified-random sampling. Văn bản cho ví dụ các test vocabulary có thể lấy mẫu từ word list có frequency counts. Kumazawa minh họa dạng nested design khi mỗi item thuộc một chapter/section.

Áp dụng cho estimator:

- `Universe` phải khóa `unit` (headword, lemma hay word family), corpus/frequency source, version, exclusion rules và tổng kích thước `N`.
- Mỗi band lưu `N_b`, item-pool version, sampling probability và cluster/section ID.
- Nếu chọn đều trong từng band, đó là stratified design; nếu route thích nghi hoặc chọn unequal probability, phải lưu inclusion probability và dùng trọng số tương ứng.
- Item cùng stem, cùng context, cùng morphological family hoặc cùng cluster không được âm thầm coi là các quan sát độc lập.

## Đề xuất cập nhật thuật toán

### 4. G-study cho item bank trước khi đặt item budget

Trong pilot, thu response-level data của một mẫu người làm bài đủ đa dạng, với anchor/form overlap để ước lượng:

```text
G-study_design = p × (i:b) × f       # nếu form và band có thể cross hợp lý
hoặc
G-study_design = p × (i:b) × f       # với b là fixed content strata, i nested trong b
```

Nếu không thể fully cross vì mỗi người chỉ gặp một subset, dùng planned incomplete/partially nested design và không gọi variance components là fully identified nếu chưa có simulation/replication kiểm chứng.

Ước lượng các component:

```text
sigma_p2
sigma_b2, sigma_i:b2
sigma_p:b2, sigma_p:i:b2
sigma_f2, sigma_p:f2, sigma_i:f2        # khi có alternate forms/occasions
```

Với cấu hình `n_b` item trong mỗi band, variance của mean score theo band phải phản ánh các component còn lại sau khi chia cho số quan sát tương ứng. Công thức tổng quát phụ thuộc design (crossed/nested, fixed/random, balanced/unbalanced); không nên tự dùng một denominator của thiết kế khác. Đối với một thiết kế đơn giản `p × i` chỉ có item random, relative error thường có dạng:

```text
G(n) = sigma_p2 / (sigma_p2 + sigma_p:i2 / n)
```

và absolute error thêm item main effect:

```text
Phi(n) = sigma_p2 / (sigma_p2 + sigma_i2 / n + sigma_p:i2 / n)
```

Đây là công thức minh họa cho design đơn giản; khi item nested trong band, cần đưa `b`, `i:b`, và các tương tác vào design-specific D-study. Không được dùng hai công thức minh họa này để claim Phi của Preply khi chưa có variance components của Preply.

### 5. D-study chọn giữa coverage và lặp item

D-study nên mô phỏng nhiều cấu hình, ví dụ:

```text
for band_quota in candidate_band_quotas:
    for items_per_band in candidate_item_counts:
        for form_count in candidate_form_counts:
            variance = predict_design_variance(G_components,
                                               band_quota,
                                               items_per_band,
                                               form_count)
            interval = transform_to_vocab_count(variance,
                                                 universe_manifest)
            keep if:
                holdout_coverage(interval) >= target_coverage
                and all_required_bands_are_covered
                and burden <= time_budget
select lowest_burden design meeting precision and coverage gates
```

Quy tắc phân bổ không nên là “mỗi band cùng số câu” một cách mặc định:

- Nếu `p×i:b` chiếm phần lớn error, ưu tiên thêm item độc lập/đại diện trong các band có đóng góp variance lớn.
- Nếu `b` hoặc `p×b` đáng kể, ưu tiên tăng số band hoặc tăng coverage giữa band; lặp trong một band không giải quyết được domain-shift.
- Nếu form/occasion effect đáng kể, tăng anchor overlap và alternate-form linking trước khi tăng tổng số item.
- Luôn có hard maximum, endpoint/tail flags và minimum quota cho band; D-study không được tối ưu Phi bằng cách bỏ hẳn vùng vocabulary mà estimand tuyên bố bao phủ.

### 6. Pseudocode production sau calibration

```text
function gstudy_calibrated_vocab(session, universe, bank, calibration_model):
    assert session.universe_version == universe.version
    responses = administer_fixed_anchors(session, bank)
    responses += stratified_or_adaptive_items(
        bank=bank,
        quotas=calibration_model.minimum_band_quotas,
        exposure_control=true,
        avoid_local_dependence=true,
        max_items=calibration_model.hard_max
    )

    components = calibration_model.variance_components
    estimate = weighted_stratified_count(responses, universe)
    g_score = relative_breadth_score(responses, calibration_model)
    phi = predict_absolute_dependability(components, responses.design)
    interval = design_and_model_interval(
        estimate=estimate,
        components=components,
        inclusion_probabilities=responses.inclusion_probabilities,
        clusters=responses.cluster_ids,
        optional_stopping_safe=true
    )

    status = quality_flags(
        endpoint=detect_floor_ceiling(responses),
        bank_coverage=check_bank_coverage(responses, calibration_model),
        anchor=check_anchor_consistency(responses),
        phi=phi,
        interval=interval
    )
    return {
        "vocabulary_estimate": estimate,
        "interval": interval,
        "relative_breadth_score": g_score,
        "absolute_dependability": phi,
        "universe": universe.id_and_version,
        "status": status
    }
```

Nếu chưa có pilot variance components, fallback vẫn là estimator stratified random và variance/CS ở báo cáo chính; không được giả nhãn đó là G/D-calibrated.

## So sánh với Preply

| Thành phần | Preply (đã/đang được xác minh) | Thiết kế đề xuất sau iteration 27 |
|---|---|---|
| Word universe | Các iteration trước ghi nhận mô tả công khai về BNC/rebalanced sampling và headword/derived-form policy; endpoint Preply trực tiếp trả 403 trong các lần fetch gần đây | Versioned manifest: unit, corpus, bands, `N_b`, exclusions, item-pool version |
| Item routing | Chưa có item bank, routing probabilities hoặc response-level data để xác minh | Fixed anchors + stratified/adaptive routing có inclusion probabilities và quota |
| Error model | Chưa tìm được nguồn xác thực cho G/Phi, variance components, D-study hoặc margin of error của Preply | G-study trên calibration sample; D-study thử band/item/form budgets; report relative và absolute metrics riêng |
| Độ dài/precision | Chưa xác minh được precision theo score range | Chọn burden nhỏ nhất đạt holdout coverage, band coverage, endpoint và time gates; hard maximum |
| Diễn giải | Không được suy ra CEFR/functional mastery chỉ từ một count | Báo count + interval + universe; rank/breadth và domain dependability tách biệt |
| Repeated forms | Chưa có common-anchor/form data của Preply | Anchor overlap, alternate-form linking, occasion/form variance và drift audit |

Không có đủ dữ liệu để kết luận Preply đang hoặc không đang dùng G-theory/D-study. So sánh trên đây chỉ phân biệt thông tin có thể xác minh với thiết kế khuyến nghị.

## Validation plan và giới hạn

1. **Pilot design:** mẫu người làm bài trải rộng proficiency, mỗi người nhận anchor và một subset có overlap; khóa universe/band/item metadata trước khi thu dữ liệu.
2. **G-study replication:** bootstrap/replicate theo người và theo form; kiểm tra stability của variance components, item×person và band effects.
3. **D-study simulation:** mô phỏng các quota, số item/band, anchor rate và form count; đo CI coverage/interval width, không chỉ coefficient.
4. **Hold-out:** đánh giá trên người và item/form chưa dùng để ước lượng; kiểm tra score stability và calibration của absolute interval.
5. **Construct gate:** xác nhận outcome là receptive written breadth trên đúng lexical unit; không dùng Phi của một classroom criterion test làm bằng chứng cho vocabulary size toàn tiếng Anh.
6. **Dependency gate:** residual/Q3 hoặc cluster audit để tránh phóng đại effective sample size khi item liên quan.
7. **Transport gate:** kiểm tra subgroup/DIF, modality, domain profile và corpus-version drift trước khi dùng chung calibration.

Hạn chế lớn nhất vẫn còn: chưa có dữ liệu sản xuất của Preply. Vì vậy các `.30`, `.41`, `.51` chỉ là kết quả của Kumazawa trong một context cụ thể; công thức D-study và target coefficient của hệ thống đề xuất phải được ước lượng lại trên item bank và population mục tiêu.
