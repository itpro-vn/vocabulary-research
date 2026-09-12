# Iteration 35 — Content-validity blueprinting and expert review

## Phạm vi và kết luận

Iteration này kiểm tra lớp bằng chứng **trước** calibration thống kê: bài test có thật sự đại diện cho vocabulary universe và construct đã tuyên bố hay chưa. Kết luận chính:

1. Một vocabulary-size score không thể được coi là hợp lệ chỉ vì alpha cao, group means tăng, hoặc IRT fit tốt. Trước đó phải khóa construct, lexical unit, frequency universe, intended use và blueprint.
2. Content validity nên được xây thành một chuỗi bằng chứng có thể audit: literature/domain review → manifest và blueprint → expert review độc lập → sửa/re-review → cognitive tryout/pilot → field-test statistics.
3. Nguồn ETS cung cấp một quy trình phát triển assessment quy mô lớn: bắt đầu từ intended use và target population, prototype nhiều vòng, pilot, field test để có item statistics ổn định; mỗi item trải qua nhiều vòng content/fairness review trước khi vào pool.
4. Nghiên cứu Arabic VST cho thấy các quyết định tưởng như “preprocessing” — re-lemmatization, loại proper nouns/functional words/colloquial forms, xử lý homograph và kiểm tra frequency list — trực tiếp thay đổi estimand và content representation.
5. Frequency bands là khung sampling, không phải bảo đảm difficulty. Arabic pilot có các band không giảm đều; tác giả nêu các khả năng confound từ cognate/diglossia và sai lệch frequency list. Vì vậy monotonicity là diagnostic cần kiểm tra, không phải quy tắc để ép dữ liệu.

## Nguồn đã kiểm tra

Các URL dưới đây đã được kiểm tra bằng HTTP với browser User-Agent trong iteration này; các PDF được tải và đọc text layer.

| Nguồn | Trạng thái kiểm tra | Vai trò |
|---|---:|---|
| [Dinnesen et al., Collaborating With an Expert Panel](https://files.eric.ed.gov/fulltext/EJ1239399.pdf) | HTTP 200 | Định nghĩa content validity; quy trình domain review, expert panel, rubric và review lặp |
| [Papageorgiou et al., ETS RM-21-03, TOEFL Essentials Design Framework](https://www.ets.org/Media/Research/pdf/RM-21-03.pdf) | HTTP 200 | Mẫu quy trình construct, prototype, pilot, field test, content/fairness review và pretesting |
| [Ech-Charfi, Designing and piloting a Vocabulary Size Test of Arabic](https://revues.imist.ma/index.php/IJAL/en/article/download/47599/25300) | HTTP 200, `application/pdf` | Bằng chứng vocabulary-specific về lexical universe, band blueprint, distractors, pilot và lỗi frequency-list |
| [Preply methodology proxy](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) | HTTP 200 | Tham chiếu vendor đã có trong các iteration trước; production page trực tiếp vẫn được kiểm tra là HTTP 403 |

Nguồn Dinnesen et al. là nghiên cứu content-validity trong phát triển can thiệp giáo dục, không phải calibration của vocabulary test. Nó được dùng như nguồn phương pháp về expert review; không được dùng để khẳng định một ngưỡng CVI hay sample size phổ quát cho bài test này.

## Bằng chứng đã xác minh

### 1. Content domain phải được định nghĩa trước khi đánh giá item

Dinnesen et al. mô tả content validity là mức các thành phần của assessment/intervention đại diện cho construct dự định đo. Bằng chứng cần trả lời item có khớp định nghĩa construct, phù hợp mục đích và đại diện cho content domain hay không. Quy trình hai giai đoạn của Lynn được họ tóm tắt là:

1. Nhà phát triển xác định toàn bộ content domain thông qua rà soát tài liệu liên quan.
2. Panel chuyên gia đánh giá có hệ thống các thành phần bằng phương pháp định tính và/hoặc định lượng.

Áp dụng vào vocabulary-size test, “content domain” không chỉ là danh sách từ. Nó phải bao gồm:

- đơn vị đo: headword, lemma, flemma hay word family;
- universe và quy tắc đưa vào/loại ra;
- receptive recognition hay productive recall;
- frequency metric, corpus, register và version;
- sense/POS/context mà item đại diện;
- các band và tỷ trọng của chúng;
- intended use và target population.

Một bài test có thể có psychometric reliability cao nhưng vẫn under-represent construct nếu, chẳng hạn, nó tuyên bố “vocabulary dùng trong đời sống” nhưng chỉ sampling written technical headwords.

### 2. Expert review cần có rubric, dữ liệu thô và vòng sửa

Nguồn Dinnesen et al. ghi nhận có nhiều cách lượng hóa content validity: content-validity index, proportion agreement, kappa, universal agreement hoặc trung bình item-level indices. Nguồn này không kết luận một phương pháp là đúng cho mọi assessment; điểm có thể chuyển thành yêu cầu kỹ thuật là:

- chọn trước rubric và cách tổng hợp;
- lưu rating của từng chuyên gia, không chỉ lưu mean hoặc pass/fail;
- lưu nhận xét mở và quyết định sửa/giữ/loại;
- review lại sau khi sửa để xác nhận feedback đã được tích hợp.

Nghiên cứu mô tả chuỗi review ban đầu, buổi thảo luận với panel, sửa lớn, rồi review lần hai. Panel có cả researcher và practitioner; practitioner giúp phát hiện vấn đề về tính khả thi, liên quan và cách người dùng thực tế hiểu công cụ. Với vocabulary test, panel tối thiểu về vai trò nên có nhà đo lường, chuyên gia vocabulary/lexicography, giáo viên hoặc người thiết kế curriculum và đại diện target population; đây là khuyến nghị thiết kế của Deli, không phải sample-size requirement được nguồn xác nhận.

### 3. ETS cho thấy content review phải đứng trước và song song với calibration

ETS mô tả TOEFL Essentials bắt đầu từ intended uses, target ability range, academic/daily-life contexts, thời lượng và delivery constraints. Họ dùng prototype nhiều vòng; sau đó pilot trên 700 English learners, chọn task types và tinh chỉnh specifications; cuối cùng field-test pool trên population tương tự vận hành với khoảng 5.000 người để tạo item statistics ổn định.

Trong content-development pipeline, ETS nêu:

- assessment specialists và outside item writers được đào tạo;
- item writer draft được assessment specialists review;
- ít nhất ba assessment specialists không tham gia authoring review tuần tự và độc lập;
- item chỉ đủ điều kiện khi tất cả reviewers đánh giá acceptable;
- review xem xét độ rõ, accessibility cho L2, không đòi hỏi background knowledge không liên quan, relevance với specification, key duy nhất và distractors plausible;
- fairness review diễn ra trước khi vật liệu được dùng;
- pretest items trong operational forms để nhận diện item hoạt động kém và sửa hoặc loại;
- form assembly tiếp tục được review để giữ similarity về content và statistical specifications, hỗ trợ equating.

Đây là bằng chứng từ một bài thi ngôn ngữ quy mô lớn, không phải bằng chứng rằng vocabulary-size test phải có đúng ba reviewer hoặc đúng 5.000 người. Các con số đó chỉ là mô tả của ETS cho chương trình TOEFL Essentials.

### 4. Arabic VST làm rõ lexical-universe decisions

Ech-Charfi (2024) xây Arabic VST từ Arabic Internet Corpus. Tác giả cho rằng định nghĩa lemma ở danh sách gốc không nhất quán nên đã re-lemmatize theo định nghĩa lemma và đặc điểm morphology Arabic. Sau đó họ loại:

- item viết bằng Latin script;
- colloquial words không có cognate trong Modern Standard Arabic;
- proper nouns;
- functional words.

Danh sách ban đầu có khoảng 100.000 items và 74.191.620 tokens; sau re-lemmatization còn khoảng 22.000 lemmas và 55.935.369 tokens; final list có 19.968 items. Tác giả cũng phải xử lý homograph bằng cách chia tần suất cho các pronunciation/meaning có thể có, và thừa nhận cách này khá ad hoc.

Điểm quan trọng cho thuật toán là mọi lọc và mapping làm thay đổi mẫu số `N_b`, rank và ý nghĩa `V_hat`. Chúng phải được lưu trong versioned manifest. Không được thay đổi dictionary/corpus cleaning sau calibration mà vẫn gọi score cũ và score mới là cùng một scale.

### 5. Arabic VST cung cấp blueprint cụ thể nhưng frequency không đủ làm difficulty

Arabic VST chọn 10 item ngẫu nhiên từ mỗi band 1.000 từ trong 14 band. Context được thiết kế chủ yếu để chỉ ra part of speech mà không cung cấp quá nhiều cue nghĩa. Mỗi item có bốn definitions cùng part of speech và cùng band với target; key được phân bố đều qua bốn vị trí.

Đây là cách bảo vệ content coverage và giảm một số artifact:

- quota cố định bảo đảm mỗi band có đại diện;
- distractors cùng band/POS hạn chế việc đáp án đúng nổi bật chỉ vì dễ hơn;
- cân bằng vị trí key giảm position bias;
- context hạn chế suy luận ngoài construct vocabulary recognition.

Tuy nhiên chính nghiên cứu này báo cáo các band không giảm đều theo frequency: K4 cao hơn K3 hơn 30 điểm, K8 cao hơn K7 hơn 80 điểm, và K14 cao hơn K11–K13. Tác giả thảo luận ảnh hưởng của cognate/diglossia và nghi vấn một số token counts trong frequency list không khớp concordance query. Do đó, frequency rank nên là biến thiết kế/sampling và covariate để kiểm tra, không nên bị coi là difficulty parameter hoàn hảo.

### 6. Reliability/group separation không thay thế item-level evidence

Pilot Arabic VST có 71 người ở ba nhóm học vấn. Cronbach alpha của 14 band là .94; group means tăng theo level và ANOVA phân biệt nhóm. Nhưng tác giả nói rõ validation sâu hơn cần item analysis hoặc Rasch analysis để kiểm tra item ease/difficulty có phản ánh frequency và vocabulary knowledge hay không, và pilot chưa đủ dữ liệu cho mục tiêu đó.

Production rule: alpha, group differences và frequency profile chỉ là evidence sớm. Item chỉ được vào operational bank khi qua cả content gate và statistical gate. Một item có alpha contribution tốt nhưng ambiguous, cue-dependent hoặc sai lexical unit vẫn phải sửa/loại.

## Blueprint và data contract đề xuất

Mỗi version của item bank nên có manifest bất biến với các trường sau:

```text
bank_version
construct_statement
intended_use
population_definition
lexical_unit                    # headword | lemma | word_family | other
universe_definition
corpus_id, corpus_version
frequency_metric
band_definition[]               # band_id, lower/upper rank, N_b, register mix
inclusion_rules
exclusion_rules
sense_policy, pos_policy
sampling_frame_hash
random_seed_policy
```

Mỗi item cần tối thiểu:

```text
item_id, bank_version, universe_id, lexical_unit_id
band_id, rank_or_rank_interval, raw_frequency, dispersion_if_used
pos, sense_id, stem, context
key, distractors, key_position
writer_id, authoring_version
expert_ratings[]
content_decision, fairness_decision, revision_history
pilot_form, exposure_status
item_fit_status, DIF_status, dependence_cluster
```

Không cho phép item có `content_decision=accepted` nếu thiếu mapping tới một band/lexical unit cụ thể. Không cho phép so sánh hai estimate nếu `bank_version`, `lexical_unit` hoặc construct statement khác mà chưa có linking study.

## Rubric và gates đề xuất

Các ngưỡng dưới đây là **giả định triển khai cần pilot/validation**, không phải ngưỡng đã được nguồn xác nhận cho Preply.

### Content rubric

Mỗi reviewer đánh giá độc lập theo thang 1–5 và ghi nhận xét:

1. **Construct relevance** — item có đo written receptive vocabulary breadth đã tuyên bố không?
2. **Domain representativeness** — item có đúng universe/band/lexical unit và không làm lệch coverage không?
3. **Sense/POS clarity** — một target sense và POS có được xác định đủ rõ không?
4. **Cueing/guessability** — context hoặc option có cho phép trả lời bằng cue ngoài knowledge của target không?
5. **Key/distractor function** — key duy nhất, distractors cùng specification và không có đáp án nổi bật hình thức không?
6. **Accessibility/fairness** — không đòi background knowledge, register/culture không liên quan hoặc năng lực đọc không thuộc construct.
7. **Target-population relevance** — wording phù hợp population và mode vận hành.

### Hard-fail gate

Loại hoặc trả về sửa nếu có một trong các lỗi:

- không xác định được lexical unit/band/sense;
- có hơn một key hợp lý;
- item đo background knowledge hoặc translation/cognate thay vì construct đã tuyên bố;
- stem/context chứa target khác hoặc cue trực tiếp đáp án;
- distractor không cùng loại specification và làm item quá dễ theo hình thức;
- fairness reviewer nêu vấn đề chưa giải quyết;
- mapping corpus/dictionary không tái lập được.

### Quantitative review gate

Không đặt một CVI/CVR universal từ nguồn khác vào hệ thống. Giai đoạn đầu nên:

- lưu item-level ratings và agreement;
- báo tỷ lệ item bị revise/reject theo band;
- kiểm tra chênh lệch rating giữa band, POS, sense và reviewer role;
- dùng ngưỡng nội bộ đã đăng ký trước, sau đó kiểm tra sensitivity khi thay ngưỡng;
- chỉ đóng blueprint khi các item bị loại được thay thế trong **cùng stratum**, tránh làm thay đổi inclusion probability âm thầm.

### Statistical gate sau pilot

Content pass không đủ để vận hành. Cần thêm:

- item difficulty/discrimination hoặc Rasch fit phù hợp model đã đăng ký;
- không có local dependence nghiêm trọng;
- distractor functioning và key-position balance;
- band response profile và tail coverage;
- DIF/fairness review conditional on ability;
- response-time/effort flags chỉ dùng làm validity sensitivity nếu chưa có calibration correction;
- alternate-form common-anchor nếu score được so sánh qua form.

## Pseudocode tích hợp vào estimator

```text
function build_operational_bank(universe, corpus, construct, candidate_items):
    manifest = freeze_manifest(universe, corpus, construct)
    blueprint = make_stratified_blueprint(
        lexical_unit=manifest.lexical_unit,
        bands=manifest.band_definition,
        intended_use=manifest.intended_use,
        population=manifest.population_definition
    )

    candidates = sample_reproducibly(candidate_items, blueprint, manifest.random_seed_policy)
    reviewed = []

    for item in candidates:
        ratings = independent_expert_review(item, rubric=CONTENT_RUBRIC)
        store_raw_ratings(item.id, ratings)
        decision = adjudicate_content(ratings, blueprint, manifest)
        if decision == "hard_fail":
            store_decision(item.id, "reject_or_revise")
            continue
        if decision == "revise":
            item2 = revise(item, ratings)
            ratings2 = independent_re_review(item2, rubric=CONTENT_RUBRIC)
            store_raw_ratings(item2.id, ratings2)
            if not passes_content_gate(ratings2):
                store_decision(item2.id, "reject")
                continue
            item = item2
        reviewed.append(item)

    assert coverage_matches_blueprint(reviewed, manifest)
    assert all(has_lexical_mapping(x, manifest) for x in reviewed)
    assert all(has_fairness_signoff(x) for x in reviewed)

    pilot_data = collect_pilot_responses(reviewed)
    stats = fit_registered_item_model(pilot_data)
    operational = []
    for item in reviewed:
        if passes_statistical_gate(item, stats) and preserves_stratum_coverage(item):
            operational.append(item)

    assert coverage_matches_blueprint(operational, manifest)
    return freeze_bank(manifest, operational, stats)

function estimate_size(responses, bank):
    require bank.content_and_statistical_signoff == true
    for each band b:
        x_b = scored_known_responses(responses, b)
        p_b = model_or_design_estimate(x_b, bank.item_parameters[b])
    V_hat = sum(bank.N_b * p_b for b in bank.bands)
    interval = conditional_or_design_interval(responses, bank)
    return {"estimate": V_hat,
            "unit": bank.lexical_unit,
            "universe": bank.universe_definition,
            "interval": interval,
            "content_status": bank.content_status,
            "calibration_version": bank.version}
```

Nếu chưa có response data đủ để fit model, `build_operational_bank` chỉ trả về `pilot_ready`, không được xuất vocabulary estimate có vẻ chính xác. Baseline stratified estimator vẫn có thể dùng trong nghiên cứu pilot, nhưng phải ghi rõ uncertainty của sampling và construct.

## Công thức và diễn giải

Với band `b`, kích thước universe `N_b`, mẫu `n_b`, score nhị phân `x_bj`:

```text
p_hat_b = mean(x_bj)
V_hat = Σ_b N_b p_hat_b
```

Thiết kế content-validity không thay đổi công thức này; nó xác định liệu `N_b`, `x_bj` và band assignment có đúng estimand hay không. Khoảng sampling sơ bộ có thể dùng:

```text
Var_design(V_hat) ≈ Σ_b N_b² (1 - n_b/N_b) s_b² / n_b
CI_95 = V_hat ± 1.96 * sqrt(Var_design(V_hat))
```

Trong model IRT, interval còn phải chứa model uncertainty và có thể thêm sensitivity range do alternate lexical manifest. Không cộng một “content validity margin” tùy ý vào SEM. Nếu content gate chưa pass, status nên là `not_interpretable_for_operational_use`, không phải một CI rộng hơn để che lỗi construct.

## So sánh với cách làm Preply

| Thành phần | Preply theo methodology đã fetch ở các iteration trước | Thiết kế đề xuất sau iteration 35 |
|---|---|---|
| Đơn vị/Universe | Dictionary entries/headwords, derived-form counts gộp theo headword; vendor mô tả universe hơn 45.000 entries | Freeze manifest headword/lemma/word-family; mọi mapping và exclusion versioned |
| Frequency | BNC-derived mixture và rank theo methodology vendor | Lưu corpus/version/metric/raw counts/dispersion/rank interval; audit drift và list quality |
| Sampling | Hai giai đoạn, khoảng 40 từ rồi khoảng 120 từ hẹp hơn, logarithmic midpoint theo mô tả vendor | Stratified blueprint có inclusion probability; có thể routing/adaptive sau calibration nhưng giữ anchor và quota |
| Content review công khai | Chưa tìm được nguồn xác thực mô tả item-bank expert review, rubric, fairness signoff hoặc pretest statistics sản xuất của Preply | 3+ reviewer như một conservative design pattern tham chiếu ETS; rubric, raw ratings, revision history, fairness gate |
| Scoring | Vendor midpoint/headword estimate và margin được mô tả trong methodology; không được xem là word-family score | `V_hat` gắn lexical unit/universe; CSEM/model/design interval; status nếu content/calibration gate fail |
| Validation | Chưa có production item bank/response-level data để kiểm định độc lập | Domain memo → expert review → pilot → item model/DIF/dependence → field/hold-out validation |

Trang Preply trực tiếp vẫn trả HTTP 403 trong iteration này; vì vậy không thể xác minh thêm production item bank hoặc quy trình review ngoài methodology proxy đã lưu. Không có nguồn xác thực cho một hệ số chuyển headword sang lemma/word-family hay một ngưỡng content-validity riêng của Preply.

## Assumptions và giới hạn

- Các quy tắc reviewer, thang 1–5 và hard-fail ở trên là specification đề xuất, chưa phải tham số đã calibration.
- Bằng chứng Arabic VST có ngôn ngữ, corpus và diglossia riêng; chỉ chuyển bài học về manifest, sampling và audit, không chuyển trực tiếp frequency threshold sang English/Preply.
- ETS TOEFL Essentials là bài thi ngôn ngữ đa kỹ năng; quy mô pilot/field test của ETS không phải công thức cỡ mẫu cho vocabulary-size bank.
- Expert agreement chứng minh content evidence, không chứng minh score validity, reliability, criterion validity hay interval coverage.
- Khi frequency band không monotonic, không tự động sửa item để ép điểm giảm; trước hết kiểm tra corpus, cognate, sense, local dependence và population exposure.

## Kế hoạch validation tiếp theo

1. Tạo một frozen English manifest với hai nhánh song song (headword và word-family) nhưng không trộn điểm.
2. Lập blueprint matrix `band × POS × sense × register × intended-use`, ghi target counts và inclusion probabilities.
3. Cho panel reviewer độc lập review candidate items; lưu raw ratings, comments, revisions và tỷ lệ reject theo stratum.
4. Chạy cognitive tryout để phát hiện cue, ambiguity và lexical-unit mismatch trước pilot lớn.
5. Pilot đủ đa dạng target population; ước lượng item difficulty, dependence, distractor functioning, DIF và band monotonicity như diagnostics.
6. Giữ hold-out items và hold-out persons để kiểm tra score stability, calibration và interval coverage; không dùng toàn bộ pilot cho cả item selection lẫn claims.
7. Chỉ sau khi các gate đạt mới so sánh trực tiếp với Preply trên cùng người, có common-person/common-item linking; báo riêng headword và word-family estimates.

## Gap cần giữ nguyên

Chưa có item bank, expert-review records, response-level production data, corpus manifest đầy đủ hoặc validation sample của Preply. Chưa tìm được nguồn xác thực cho ngưỡng reviewer agreement, quy tắc fairness, hiệu chỉnh frequency-band difficulty hay mapping headword↔lemma/word-family riêng của Preply. Những gap này không được thay bằng giả định ±10% hoặc một hệ số chuyển đổi cố định.
