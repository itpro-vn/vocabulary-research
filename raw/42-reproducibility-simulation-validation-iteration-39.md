# Iteration 39 — Tái lập thuật toán, mô phỏng và validation theo chuẩn TBA

## Phạm vi và direction

Iteration này không nghiên cứu thêm một mô hình CAT/IRT mới. Direction là **algorithm reproducibility and simulation-based validation**: xác minh yêu cầu về audit trail, mô phỏng trước triển khai, precision có điều kiện, equating/comparability và periodic validation cho một bài kiểm tra vocabulary-size. Mục tiêu là biến các yêu cầu đó thành một benchmark protocol có thể tái chạy, thay vì chép các ngưỡng CAT từ lĩnh vực khác.

## Nguồn đã kiểm tra

| Nguồn | HTTP | Cách kiểm tra | Vai trò |
|---|---:|---|---|
| ITC/ATP, *Guidelines for Technology-Based Assessment* | 200 | tải PDF và trích xuất 173 trang bằng `pypdf` | Nguồn hướng dẫn chính thống về adaptive design, simulation, scoring, precision, equating và validation |
| Ayanwale & Ndlovu (2024), *The feasibility of computerized adaptive testing of the national benchmark test: A simulation study* | 200 | tải PDF ERIC và trích xuất 18 trang bằng `pypdf` | Ví dụ học thuật có thông số mô phỏng, chỉ số sai số và trade-off exposure/precision |
| Preply methodology page | 403 trực tiếp; proxy 200 trong các lần trước | kiểm tra lại bằng `curl` với browser UA | Nguồn vendor để đối chiếu; không có response-level hay validation artifact công khai được xác minh |

URL ITC: <https://www.intestcom.org/upload/media-library/tba-guidelines-final-2-23-2023-v4-167785144642TgY.pdf>

URL nghiên cứu CAT: <https://files.eric.ed.gov/fulltext/EJ1428037.pdf>

URL phương pháp Preply (proxy được dùng trong các iteration trước): <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works>

## Findings đã xác minh

### 1. Adaptive engine phải có manifest tham số bất biến

ITC/ATP guideline 2.8 yêu cầu các lựa chọn trong test adaptive phải được nghiên cứu và ghi lại để chứng minh validity/defensibility. Danh sách nêu trực tiếp gồm: kích thước item bank; IRT model; phân phối item parameters; item-selection method; exposure constraints; content constraints; scoring method; termination criteria. Guideline cũng yêu cầu khảo sát sớm các thuộc tính như score standard error, average test length, bank utilization, content coverage và exposure rates.

Áp dụng cho vocabulary-size: mỗi score phải giữ `algorithm_manifest_id`, `universe_version`, `item_bank_version`, `selection_rule`, `scoring_rule`, `termination_rule`, `seed`, quotas, exposure policy và các phiên bản calibration. Không được chỉ lưu số từ cuối cùng.

### 2. Mô phỏng phải chạy trước khi bật adaptive production

ITC/ATP guideline 2.9 yêu cầu CAT được thông tin bởi simulation với independent variables thực tế và dependent variables gắn với mục tiêu của chương trình. Guideline nêu phải kiểm tra item/module assignment, mức sử dụng item/module, exposure constraints và termination criteria trước triển khai.

Trong vocabulary test, simulation grid tối thiểu nên thay đổi:

- đường cong mastery theo frequency band, gồm floor/ceiling;
- độ khó, discrimination và guessing/slip;
- local dependence giữa morphology, semantic set hoặc shared context;
- DIF theo L1, cognate/loanword status và mode;
- missingness, rapid guessing và response-style bias;
- fixed stratified, midpoint và adaptive routing;
- các phiên bản corpus/rank và bank thiếu item ở tail.

Metrics phải gồm bias, RMSE/MAE, interval coverage, average/quantile test length, band/content coverage, item exposure/overlap và tỷ lệ không hội tụ. Mean test length một mình không phải validation.

### 3. Precision của adaptive test phải có điều kiện theo mức năng lực

ITC/ATP guideline 7.2 nói reliability/measurement precision phải được chứng minh trên toàn range của scale. Với adaptive test, test-information function và conditional standard-error curves phù hợp hơn một reliability coefficient cho cả form.

Do đó, báo cáo vocabulary nên có `SE_or_CI(vocabulary_level)` hoặc bảng precision theo band/ability, đặc biệt ở floor và ceiling. Không dùng một margin trung bình kiểu “±10%” làm cam kết phổ quát nếu chưa có coverage study trên đúng universe, population và version.

### 4. Nhiều form/bank/device cần equating và tài liệu đầy đủ

ITC/ATP guideline 7.3–7.7 yêu cầu equating khi có nhiều form, và comparability phải xét forms, items, devices, technology và administrative conditions nếu claim score interchangeable. Bằng chứng nên xem distribution shape, reliability và SEM; hồ sơ phải nêu data sources/samples, methods, analyses và limitations. DIF hoặc measurement-invariance analysis có thể cần thiết.

Production rule: form mới hoặc bank mới phải có common anchors/common-person linking và một hold-out comparability analysis trước khi trộn score với lịch sử. Growth/retest chỉ được báo khi scale linking và score-difference error đã được kiểm tra.

### 5. Validation phụ thuộc intended use và phải lặp lại định kỳ

ITC/ATP guideline 7.9–7.15 yêu cầu định nghĩa rõ intended use và construct; validity evidence phải hỗ trợ đúng intended use; một nghiên cứu đơn lẻ thường không đủ; hạ tầng không được cản trở performance; fairness cần được kiểm tra trên population đa dạng; validation phải được thực hiện định kỳ.

Hệ quả cho sản phẩm: receptive written vocabulary breadth theo headword/lemma/word-family là một construct và không tự động tương đương CEFR placement, reading coverage, listening ability, instructional recommendation hoặc growth. Mỗi diễn giải mới cần criterion và hold-out evidence riêng.

### 6. Ví dụ CAT cho thấy không thể chuyển ngưỡng giữa lĩnh vực

Ayanwale & Ndlovu (2024) mô phỏng 10.000 examinees, item pool 500 câu theo 3PL, maximum Fisher information, Randomesque exposure control và termination `SE < 0.35`. Họ đánh giá conditional bias (CBIAS), conditional mean absolute error (CMAE), conditional RMSE (CRMSE), precision và exposure; kết quả fixed-length và variable-length có trade-off khác nhau.

Đây là template tái lập hữu ích, nhưng `SE < 0.35`, 500 items, 3PL và kết luận fixed/variable không được bê nguyên sang vocabulary. Chúng phụ thuộc bank, latent trait, item model, mục tiêu và population của nghiên cứu đó. Vocabulary phải dùng calibration/hold-out riêng để chọn ngưỡng.

## Benchmark protocol đề xuất

### A. Artefact bắt buộc trước simulation

```text
RunManifest {
  run_id, git_commit, random_seed, software_versions,
  universe_id, universe_version, unit, corpus_manifest,
  item_bank_version, calibration_sample_id,
  model, priors_or_bounds, selection_rule,
  content_and_band_quotas, exposure_rule,
  missingness_rule, stopping_rule, max_items
}
```

Không sửa manifest sau khi chạy. Nếu đổi corpus, mapping lexical unit, item parameters, rule hoặc code, tạo `run_id` mới.

### B. Thiết kế simulation

Tạo latent population với các profile biết trước `V_true`: low, middle, high và mixed-band mastery. Với mỗi profile, sinh response theo nhiều cell:

1. stratified Bernoulli baseline;
2. Rasch/2PL/3PL sau calibration;
3. pseudoword/yes-no response bias;
4. L1/DIF và cognate contamination;
5. local dependence;
6. missing/timeout/rapid-guessing;
7. alternate bank/form/device;
8. tail floor/ceiling và rank-version drift.

Mỗi cell chạy đủ replicate với seed được lưu. Cell nào không có empirical calibration phải gắn `synthetic_assumption=true`; không coi kết quả simulation là bằng chứng field validity.

### C. Metrics và công thức

Với replicate `r`:

```text
bias = mean_r(V_hat_r - V_true_r)
MAE  = mean_r(abs(V_hat_r - V_true_r))
RMSE = sqrt(mean_r((V_hat_r - V_true_r)^2))
coverage = mean_r(lower_r <= V_true_r <= upper_r)
length = mean_r(number_of_items_r)
```

Báo cáo thêm bias/coverage theo band và decile của `V_true`, không chỉ trung bình toàn population. Ghi riêng:

```text
response_CI          # error do response/sample/model đã calibration
rank_sensitivity     # thay đổi do corpus/rank manifest
construct_sensitivity # thay đổi do unit/sense/domain definition
format_sensitivity   # Y/N, MCQ, Not Sure, confidence, mode
```

Các sensitivity range không được cộng vào point estimate như thể chúng là số từ đã biết.

### D. So sánh ba estimator

```text
for cell in simulation_grid:
    truth = generate_population(cell)
    for method in [fixed_stratified, preply_midpoint, safe_adaptive]:
        result = run(method, truth, manifest, seed)
        save_metrics(result, truth, cell, manifest)
compare_bias_rmse_coverage_length_exposure()
reject_if_coverage_or_content_gates_fail()
```

- `fixed_stratified`: estimator chính trước calibration, với `V_hat = Σ_b N_b p_hat_b`.
- `preply_midpoint`: benchmark ngắn trên đúng dictionary-headword universe; không đổi trực tiếp sang word-family count.
- `safe_adaptive`: adaptive chỉ bổ sung thông tin cho band có uncertainty lớn, vẫn giữ anchors/quota để bảo toàn estimand.

### E. Release gates

Không bật production adaptive nếu chưa có:

- item-bank/content manifest và seed tái chạy;
- calibration sample độc lập với hold-out validation;
- bias/RMSE/coverage theo range, band và subgroup;
- conditional SE/information evidence;
- exposure, overlap, security và content-coverage audit;
- common-anchor equating cho form/bank/device variation;
- periodic revalidation trigger khi corpus, item bank, UI hoặc scoring đổi.

Các ngưỡng số cụ thể (`target_SE`, minimum coverage, max exposure, max interval width) phải được đặt sau pilot theo intended use. Chưa có nguồn xác thực cho ngưỡng riêng của Preply.

## Bảng đối chiếu với Preply

| Thành phần | Preply đã công bố/được xác minh trước đây | Thiết kế đề xuất sau iteration 39 |
|---|---|---|
| Định vị | screening rộng rồi narrow sampling quanh midpoint; rank logarithmic theo vendor methodology proxy | benchmark midpoint như baseline, thêm fixed-stratified và adaptive có manifest |
| Universe | dictionary headword, BNC-derived spoken/written ranking theo vendor methodology proxy | versioned universe, unit rõ ràng, corpus/rank manifest và sensitivity |
| Calibration | chưa thấy public response-level item parameters | calibration sample, hold-out, common anchors, conditional SE |
| Simulation | chưa thấy public simulation report/routing log | Monte Carlo grid realistic, seed/commit lưu, metrics bias/RMSE/coverage/length/exposure |
| Uncertainty | vendor methodology nêu margin khoảng ±10% trong nguồn trước đây; coverage độc lập chưa xác minh | báo response CI, rank/construct/format sensitivity riêng; không claim universal margin |
| Form/bank linking | chưa xác minh production anchor/equating artifacts | common-person/common-item linking và comparability audit trước merge |
| Validation | direct methodology endpoint 403 trong callback này; proxy là vendor source | intended-use-specific validity argument, subgroup/hold-out evidence, periodic revalidation |

## Gaps còn lại

- Chưa có item bank, response-level production data, routing log hoặc calibration sample của Preply.
- Chưa có nguồn xác thực cho Preply `target_SE`, termination rule, exposure cap, conditional information curve hoặc interval coverage.
- Chưa thể ước lượng các ngưỡng release gate từ nguồn học thuật chung; phải pilot trên universe/target population thực tế.
- Simulation chỉ chứng minh hành vi dưới các giả định đã sinh. Nó không thay thế criterion validity, response-process study, DIF, test–retest hoặc field hold-out.

## Kết luận iteration

Một estimator vocabulary-size đáng tin cần được giao như một **reproducible measurement system**: universe và bank có version; engine có manifest; adaptive rules được mô phỏng trước; precision là conditional; forms được equate; intended use được giới hạn; validation lặp lại. Ayanwale & Ndlovu cung cấp cấu trúc simulation có thể tái dùng, còn ITC/ATP cung cấp các yêu cầu về bằng chứng và tài liệu. Không có bằng chứng mới cho phép khẳng định thuật toán production của Preply ngoài methodology vendor đã được ghi nhận ở các iteration trước.
