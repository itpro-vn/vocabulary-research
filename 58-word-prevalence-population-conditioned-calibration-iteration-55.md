# Iteration 55 — Word prevalence và calibration difficulty theo quần thể

## 1. Direction và phạm vi

Iteration này kiểm tra liệu **word prevalence** — tỷ lệ người trong một quần thể cho biết họ biết một từ — có cung cấp thông tin khó khăn bổ sung cho corpus frequency hay không. Mục tiêu là đưa prevalence vào item selection/calibration một cách bảo thủ, không biến một thống kê quần thể thành “số từ biết” trực tiếp của cá nhân.

Direction này khác với các iteration trước về raw frequency/dispersion/rank drift: ở đây biến mới là **empirical percentage-known norm** được đo trên người thật, cùng các giới hạn transport theo quốc gia, tuổi, giáo dục và reference population.

## 2. Nguồn đã kiểm tra

Các URL dưới đây được kiểm tra bằng `curl -L` với browser user-agent trong callback và đều trả HTTP 200. Nội dung bài Springer và Frontiers được fetch qua bản Markdown proxy sau khi URL gốc đã được status-check; proxy chỉ dùng để đọc nội dung, không thay URL nguồn.

| Nguồn | Nội dung dùng | HTTP |
|---|---|---:|
| [Brysbaert et al., Word prevalence norms for 62,000 English lemmas](https://link.springer.com/article/10.3758/s13428-018-1077-9) | định nghĩa prevalence, cỡ dữ liệu, thiết kế random yes/no, quan hệ với frequency, khác biệt US/UK | 200 |
| [Brysbaert et al., How Many Words Do We Know?](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.01116/full) | phân biệt type/token/lemma/word family và sự phụ thuộc của ước lượng vào định nghĩa, input, tuổi | 200 |
| [UGent record, Word knowledge in the crowd](https://biblio.ugent.be/publication/5878579) | metadata/abstract của nghiên cứu crowdsourcing gốc về prevalence và vocabulary size | 200 |

Trang sản phẩm Preply đã từng trả HTTP 403 trong các callback trước; vì vậy không coi endpoint hiện tại là nguồn đã xác thực cho prevalence policy, item bank hay population calibration.

## 3. Bằng chứng đã xác minh

### 3.1 Prevalence là biến difficulty đo từ người thật, không chỉ là frequency proxy

Bài Springer định nghĩa word prevalence là số/tỷ lệ người cho biết họ biết từ đó. Bộ dữ liệu tiếng Anh gồm 61.858 từ, thu từ một nghiên cứu online có hơn 220.000 người. Tác giả nói prevalence hữu ích để đánh giá độ khó, ghép stimulus và chọn stimulus cho vocabulary tests.

Nguồn này cũng ghi rằng prevalence dự đoán thời gian xử lý từ **vượt lên trên** các biến frequency, word length, similarity to other words và age of acquisition. Do đó frequency rank không nên được xem là mô hình difficulty hoàn chỉnh. Tuy nhiên, đây là bằng chứng về dự đoán xử lý từ và lựa chọn item; nó không tự chứng minh rằng thêm prevalence sẽ làm giảm sai số của một vocabulary-size estimator cụ thể.

### 3.2 Frequency và prevalence bổ sung cho nhau

Springer mô tả corpus word frequency và prevalence là các thước đo bổ sung, bao phủ những dạng trải nghiệm ngôn ngữ khác nhau; prevalence không hoàn toàn quy về frequency. Từ đó có một quy tắc thiết kế rõ:

- giữ frequency/corpus bands để bảo đảm declared vocabulary universe và coverage;
- dùng prevalence như biến đồng biến hoặc lớp phân tầng trong từng frequency band;
- không thay toàn bộ frequency bands bằng prevalence bands khi chưa kiểm tra coverage, lexical-unit definition và validity của estimand.

Một từ hiếm trong corpus vẫn có thể được nhiều người biết; ngược lại một từ có frequency tương đối cao có thể ít người nhận biết trong reference population. Chênh lệch này chính là lý do prevalence có thể giúp phát hiện item bất thường, nhưng không cho phép gán nhãn “universal difficulty”.

### 3.3 Prevalence phụ thuộc reference population

Trong dữ liệu English prevalence, US và UK có tương quan `r = .93`, nhưng bài báo ghi nhận một số từ khác biệt do văn hóa và khuyến nghị dùng prevalence theo quốc gia hoặc loại các từ lệch khi chỉ nghiên cứu một quốc gia. Đây là tương quan cao nhưng không phải đồng nhất tuyệt đối.

Hàm ý cho VST:

1. item manifest phải có `reference_population_id` (ít nhất variety/quốc gia và khung tuổi/giáo dục nếu có);
2. không dùng bảng US/UK để tuyên bố score chung cho mọi người học English;
3. nếu target population khác reference population, prevalence chỉ là prior/covariate ban đầu và phải có sensitivity hoặc calibration riêng;
4. chênh lệch prevalence theo nhóm cần được xem cùng DIF và construct validity, không tự động coi mọi chênh lệch là bias.

### 3.4 Thiết kế crowdsourcing cho thấy cách tách false alarm và contamination

Bài Springer mô tả một session gồm sample ngẫu nhiên 67 từ thật và 33 nonword. Người làm bài trả lời có biết chuỗi chữ hay không; feedback minh họa được tính bằng tỷ lệ trả lời “yes” cho từ thật trừ tỷ lệ nonword bị nhận nhầm là từ. Đây là tín hiệu riêng cho false alarm/guessing tendency, không nên cộng trực tiếp vào vocabulary breadth.

Người dùng có thể làm nhiều session và mỗi session có sample khác. Khi phân tích, tác giả giới hạn còn ba session đầu vì một số người đã làm hơn 100 lần và nếu giữ toàn bộ sẽ tạo trọng số quá lớn. Đây là precedent độc lập cho hai guardrail của sản phẩm online:

- kiểm soát repeated-attempt contamination và không để super-repeaters chi phối norm;
- lưu false-alarm rate như quality/response-process signal, không suy ra một correction coefficient cố định cho mọi người.

Đây không phải bằng chứng Preply đang dùng 67/33, random session hay giới hạn ba lần.

### 3.5 Lexical unit vẫn là điều kiện tiên quyết

Bài Frontiers phân biệt word type, token, lemma và word family, đồng thời nhấn mạnh vocabulary-size estimates thay đổi theo định nghĩa của “word”, lượng input và tuổi. Bài báo đưa ví dụ cho native American English 20 tuổi: khoảng 42.000 lemmas, 4.200 non-transparent multiword expressions và 11.100 word families; các con số này không phải một scale để chuyển thẳng sang headwords.

Vì vậy prevalence phải gắn với:

```text
lexical_unit = lemma | headword | word_family
universe_version
language_variety
reference_population_id
```

Không được lấy prevalence norms theo lemma rồi chuyển trực tiếp thành số headword/word-family của bài Preply.

## 4. Thuật toán đề xuất: prevalence-aware nhưng vẫn giữ estimand

### 4.1 Item-bank manifest

Bổ sung các trường sau vào manifest hiện có:

```text
Item {
  item_id,
  target,
  lexical_unit_id,
  universe_version,
  frequency_band,
  corpus_id,
  log_frequency,
  prevalence_reference,
  prevalence_n,
  prevalence_se,
  reference_population_id,
  prevalence_source_version,
  prevalence_quantile,
  pilot_difficulty,
  pilot_discrimination,
  DIF_flags
}
```

`prevalence_reference` là tỷ lệ percentage-known của quần thể chuẩn, không phải câu trả lời của người hiện tại. Nếu tỷ lệ bằng 0 hoặc 1 trong sample nhỏ, lưu cả `prevalence_n` và một estimate đã shrink; không dùng giá trị cực biên như một difficulty chân lý.

### 4.2 Sampling theo ô frequency × prevalence

Với mỗi frequency band `b`, chia item pool thành các quantile prevalence `q` (ví dụ low/middle/high chỉ là nhãn khởi đầu, không phải ngưỡng production đã được xác thực). Chọn `n_bq` item trong từng ô với seed và inclusion probability được lưu.

Mục tiêu là bảo đảm mỗi band có cả item “dễ hơn/dễ được biết” và “khó hơn/ít được biết” so với frequency dự đoán. Nếu một ô quá ít item hoặc prevalence metadata thiếu, quay về frequency-stratified sampling và gắn cờ `prevalence_unavailable`; không bù bằng item không cùng construct.

### 4.3 Scoring giữ nguyên declared universe

Với estimator design-based tối giản, nếu `N_b` là số lexical units trong band và `p_hat_b` là tỷ lệ biết ước lượng sau khi xử lý status/missingness:

```text
K_hat = Σ_b N_b * p_hat_b
```

Prevalence không xuất hiện như một số từ cộng thêm. Nó chỉ được dùng để:

- cân bằng sample;
- làm biến dự báo difficulty trong model-assisted estimator;
- kiểm tra sensitivity khi reference population thay đổi.

Nếu đã có pilot response-level đủ lớn, mô hình IRT có thể dùng prevalence để khởi tạo hoặc giải thích difficulty, nhưng tham số phải được calibration từ response data:

```text
b_i = β0
      + βF * z(log_frequency_i)
      + βP * z(probit(prevalence_reference_i))
      + u_i
P_i(known | θ) = logistic(a_i * (θ - b_i))
K_hat(θ) = Σ_j∈declared_universe P_j(known | θ)
```

Đây là specification/inference cần kiểm định, không phải hệ số đã được nguồn học thuật cấp sẵn cho Preply. Trong production, có thể bắt đầu bằng frequency-only model làm baseline rồi so sánh out-of-sample với frequency+prevalence model. Nếu thêm prevalence không cải thiện hold-out item difficulty, không được giữ biến chỉ vì nó có vẻ hợp lý.

### 4.4 Pseudocode

```text
function build_prevalence_aware_form(bank, target_population, n_total, seed):
    assert bank.universe_version is fixed
    rng = seeded_rng(seed)
    cells = group_by(bank, [frequency_band, prevalence_quantile])
    allocation = allocate_with_minimums(cells, n_total,
                                        preserve_frequency_coverage=true)
    form = []
    for cell in cells:
        eligible = cells[cell].where(
            reference_population_compatible(cell, target_population)
            or allow_population_sensitivity(cell)
        )
        if eligible is empty:
            mark_gap(cell, "prevalence_unavailable")
            eligible = frequency_band_pool(cell.frequency_band)
        form += sample_without_replacement(eligible, allocation[cell], rng)
    return form, audit_inclusion_probabilities(form)

function score_prevalence_aware(responses, bank, universe):
    assert responses.universe_version == universe.version
    observed = responses.where(status == ANSWERED)
    p_band = weighted_band_rates(observed, bank,
                                 weights=stored_inclusion_probabilities)
    K_hat = sum(universe.N_band[b] * p_band[b] for b in p_band)
    model = fit_or_load_calibrated_model(bank, responses)
    model_sensitivity = compare_models(
        frequency_only=model.frequency_only,
        frequency_plus_prevalence=model.frequency_plus_prevalence)
    return {
        "K_hat": K_hat,
        "lexical_unit": universe.unit,
        "response_or_model_CI": uncertainty_from_design_or_model(responses),
        "prevalence_population": bank.reference_population_ids,
        "prevalence_sensitivity": model_sensitivity,
        "false_alarm_rate": separate_nonword_signal(responses),
        "flags": derive_quality_and_population_flags(responses, bank)
    }
```

### 4.5 Độ không chắc chắn và báo cáo

Tách ít nhất ba thành phần:

1. `CI_response_or_sampling`: sai số do câu trả lời và sample item;
2. `CI_model`: sai số tham số IRT/model nếu có calibration;
3. `population_sensitivity_range`: thay đổi khi dùng prevalence reference khác hoặc loại item có country divergence.

Không được trình bày một `±10%` phổ quát chỉ vì prevalence có sample lớn. Sample lớn làm prevalence norm ổn định hơn; nó không xóa item ambiguity, DIF, construct mismatch hoặc selection bias của target test-taker. Chỉ hợp nhất các thành phần thành một interval tổng nếu pilot/hold-out đã chứng minh coverage.

Output đề xuất:

```text
K_hat = ước lượng số lexical units biết
95% interval = chỉ cho response/model uncertainty đã calibration
population sensitivity = [K_hat_min, K_hat_max] dưới reference populations hợp lệ
reference_population = mã quần thể dùng cho item difficulty
warning = "không so sánh trực tiếp với scale khác lexical unit hoặc quần thể nếu chưa equate"
```

## 5. So sánh với cách làm Preply

| Thành phần | Preply theo thông tin đã có trong state trước iteration này | Thiết kế prevalence-aware đề xuất |
|---|---|---|
| Đơn vị đo | methodology vendor được ghi nhận là dictionary/headword scale; current item bank chưa xác minh | khai báo `lemma/headword/word_family` và `universe_version` trong từng form |
| Độ khó item | frequency-ranked list và midpoint/logarithmic narrowing theo methodology đã ghi nhận | frequency giữ vai trò coverage; prevalence thêm covariate/quantile trong từng band |
| Quy đổi | midpoint trên vùng chuyển tiếp; vendor từng nêu margin khoảng ±10% trong methodology đã ghi nhận | design-based hoặc calibrated IRT; prevalence không cộng trực tiếp vào `K_hat` |
| Population | current norm/reference population chưa xác minh | khai báo `reference_population_id`, sensitivity theo country/age/education |
| Repeat attempts | current repeat policy chưa xác minh | rate-limit/flag repeat exposure; norm validation dùng session cap hoặc model chống super-repeater weighting |
| Nonword/false alarm | current format/false-alarm policy chưa xác minh | nếu có nonwords, giữ false-alarm như quality signal riêng; không tự áp `1/k` correction |
| Uncertainty | vendor margin không thay thế CI coverage độc lập | báo response/model interval và population sensitivity riêng |
| Tính so sánh | không được giả định tương thích với lemma/word-family scale | chỉ link sau common-item/person, DIF, calibration và hold-out coverage |

Bảng này không khẳng định Preply hiện có hay không có prevalence metadata. **Chưa tìm được nguồn xác thực cho việc Preply dùng word prevalence, reference population nào, hay có population-specific equating.**

## 6. Validation plan

1. **Manifest audit:** tạo prevalence snapshot có nguồn, ngày, population, sample size, confidence/shrinkage và lexical-unit mapping; kiểm tra item duplicate, polysemy và spelling variant.
2. **Incremental predictive test:** trên pilot response-level, so sánh frequency-only với frequency+prevalence bằng held-out item difficulty, log-loss/RMSE, item-fit và posterior predictive checks.
3. **Common-person population study:** cho các nhóm target làm cùng common items; kiểm tra item shift, DIF và score shift theo country/age/education. Không gộp scale nếu chưa đạt invariance đã định trước.
4. **Sampling simulation:** mô phỏng form chỉ frequency, form frequency×prevalence và form IRT; đo bias, RMSE, interval coverage, band coverage và tail behavior ở nhiều `K_true`.
5. **Repeat-session experiment:** cho phép alternate forms với item overlap được kiểm soát; đo practice/contamination, false-alarm drift và ảnh hưởng của số lần làm lên score. Không chuyển quy tắc “ba session” của nghiên cứu crowdsourcing thành policy Preply nếu chưa pilot.
6. **External criterion:** kiểm tra liên hệ với receptive reading/listening criterion phù hợp; không dùng prevalence score làm criterion thay cho lexical knowledge.
7. **Release gate:** chỉ deploy prevalence-aware model nếu cải thiện hold-out một cách ổn định, không tạo DIF/material population drift và không làm hỏng declared frequency coverage. Nếu fail, giữ prevalence ở dạng diagnostic/audit metadata.

## 7. Assumptions và gaps

- Prevalence norms là đặc tính của quần thể tham chiếu; transport sang EFL learner population, L1 khác hoặc quốc gia khác cần dữ liệu mới.
- Nguồn Springer hỗ trợ giá trị của prevalence cho difficulty và xử lý từ, nhưng không cung cấp hệ số chuyển prevalence thành vocabulary count cá nhân.
- Các ví dụ số trong Frontiers (42.000 lemmas, 11.100 word families) thuộc native American English và không phải norm cho người học hoặc cho Preply.
- Chưa có response-level/item-bank data của Preply để ước lượng lợi ích gia tăng, item prevalence, population calibration, false-alarm policy hoặc repeat-session contamination.
- Chưa tìm được nguồn xác thực cho current Preply prevalence implementation, reference population, prevalence-based sampling, item exposure cap hoặc equating giữa populations.

## 8. Kết luận iteration

Word prevalence là một biến difficulty đáng đưa vào item-bank metadata vì nghiên cứu English quy mô lớn cho thấy nó bổ sung cho corpus frequency và có khác biệt theo quần thể. Cách an toàn là dùng prevalence để cân bằng/chẩn đoán và làm covariate sau calibration, trong khi frequency vẫn bảo đảm coverage của declared universe và `K_hat` vẫn là tổng xác suất biết trên đúng lexical unit. Không được biến prevalence của US/UK hoặc một crowdsourced norm thành correction factor hay vocabulary count phổ quát. Bước bắt buộc tiếp theo là pilot response-level với common-person/common-item để kiểm tra lợi ích dự báo, DIF và coverage trước khi đưa prevalence vào scoring production.
