# Iteration 21 — Bayesian posterior, posterior-predictive checks và calibration

## 1. Phạm vi và kết luận ngắn

Iteration này kiểm tra một hướng riêng: dùng Bayesian posterior và posterior-predictive calibration như lớp kiểm định/định lượng uncertainty cho vocabulary-size estimator. Đây không phải đề xuất thay ngay estimator phân tầng hoặc midpoint của Preply bằng một Bayesian black box.

Kết luận thực dụng:

1. Bayesian IRT cho phép đưa prior vào ước lượng ability và item parameters; prior giúp ổn định bài toán nhưng phải có sensitivity analysis.
2. Posterior predictive checking (PPC) là lớp kiểm tra model–data fit và có thể đưa parameter uncertainty vào mô phỏng. Với vocabulary test, PPC phải kiểm tra local dependence giữa item gần nhau về lexical family, semantic cluster, shared context hoặc phrasing.
3. Simulation-based calibration (SBC) kiểm tra implementation/inference dưới model giả định; SBC không chứng minh model đúng với người học thật và không tự bảo đảm coverage cho một người cụ thể.
4. Raw posterior-predictive p-value không nên được hiểu như p-value frequentist hoặc ngưỡng pass/fail phổ quát; nghiên cứu được kiểm tra cho biết phân phối của nó không uniform ngay cả khi model đúng. Nếu cần dùng, phải có calibration bằng mô phỏng/bootstrap-like procedure.
5. Báo cáo production nên tách `posterior_interval` của model, `sampling/response uncertainty`, `sensitivity_range` do estimand/corpus, và `external_coverage` đo trên hold-out. Không được gắn posterior interval vào margin ±10% của Preply khi chưa có dữ liệu chung để kiểm chứng.

## 2. Nguồn đã fetch và verify

| Nguồn | HTTP/content check | Bằng chứng dùng |
|---|---|---|
| Grant, *Bayesian item-response theory models for educational assessment data*, PDF | URL `https://www.tqmp.org/RegularArticles/vol15-2/p075/p075.pdf` trả HTTP 200; PDF 21 trang, đã extract text | Prior cho ability/difficulty/discrimination, Bayesian IRT và sensitivity analysis |
| Kuhfeld, *A Posterior Predictive Model Checking Method Assuming Posterior Normality for Item Response Theory* | `https://europepmc.org/articles/PMC6376537?pdf=render` trả HTTP 200; PDF 18 trang, đã extract text | Local independence, PPMC, parameter uncertainty, Monte Carlo discrepancy checks |
| Talts et al., *Validating Bayesian Inference Algorithms with Simulation-Based Calibration* | `https://arxiv.org/pdf/1804.06788` trả HTTP 200; PDF 19 trang, đã extract text | SBC, rank-uniformity, giới hạn của SBC đối với model adequacy và single-observation coverage |
| Paganin & de Valpine, *Computational methods for fast Bayesian model assessment via calibrated posterior p-values* | `https://arxiv.org/pdf/2306.04866` trả HTTP 200; PDF 35 trang, đã extract text | Raw posterior predictive p-values không uniform; calibrated p-values cần double simulation/calibration |

Web extractor cấu hình search-only không extract được URL; nội dung trên được lấy bằng curl với browser UA và extract PDF, không dùng search snippet làm bằng chứng. URL PMC trực tiếp bị reCAPTCHA nên không dùng URL đó; bản PDF Europe PMC ở trên đã được fetch thành công.

## 3. Findings chi tiết

### 3.1 Bayesian IRT: prior là giả định có thể kiểm tra, không phải sự thật bổ sung

Nguồn Grant mô tả Bayesian IRT bằng cách kết hợp prior và likelihood để tạo posterior cho latent ability và item parameters. Các lựa chọn thông dụng trong tổng quan gồm normal cho ability/difficulty và lognormal cho discrimination; nguồn khuyến nghị sensitivity analysis để quyết định prior.

Ứng dụng vào bài vocabulary:

- Dùng prior yếu/vừa cho item difficulty và ability khi item bank đã có pilot, tránh kéo estimate quá mạnh về population mean.
- Nếu có 3PL/guessing parameter, prior phải phản ánh giới hạn hợp lý nhưng không được tự động dùng `1/k` làm correction.
- Chạy ít nhất hai cấu hình prior và ghi chênh lệch `V_hat`, interval, item ranking và stopping decision.
- Nếu posterior thay đổi mạnh theo prior, chưa được gọi đó là precision cao; gắn cờ `prior_sensitive` và dùng dữ liệu calibration thêm.

Một Bayesian interval chỉ mô tả uncertainty có điều kiện trên model, prior và dữ liệu. Nó không tự giải quyết sai estimand (headword so với word family), covariate shift, DIF hoặc local dependence.

### 3.2 PPC phải kiểm tra local independence và dependency có cấu trúc

Kuhfeld định nghĩa local independence trong IRT: với một latent ability cố định, xác suất joint của hai response phải bằng tích các xác suất riêng. Bài nêu các nguồn vi phạm như item dùng chung passage, phrasing quá giống, meaning quá giống hoặc nhiều subdomain.

Đối với vocabulary-size test, các dependency cần được đưa vào discrepancy statistics:

- cặp cùng morphological family hoặc shared stem;
- semantic set hoặc các target gần nghĩa;
- item dùng chung sentence context/distractor template;
- item xuất hiện quá gần nhau trong một session;
- residual correlation của cặp ngoài cùng `cluster_id`, vì metadata cluster có thể thiếu.

Nếu bỏ qua dependence, posterior có thể hẹp hơn thực tế và stopping rule dừng sớm. PPC không chỉ nên so sánh tổng số câu đúng; phải so sánh phân phối residual/pair score/cluster score giữa response quan sát và các bộ response replicate.

### 3.3 Quy trình PPMC có thể triển khai như một QA layer

Kuhfeld mô tả quy trình Monte Carlo: rút nhiều vector tham số từ posterior; với từng vector, sinh một bộ dữ liệu replicate từ predictive distribution; sau đó so sánh discrepancy của replicate và dữ liệu quan sát. Cách này đưa parameter uncertainty vào model-fit assessment thay vì coi item parameters là cố định.

Nghiên cứu mô phỏng local dependence trong 2PL với các cỡ mẫu `N=250, 500, 1.000`, 20 item và 100 replication cho mỗi điều kiện. Các con số đó là thiết kế mô phỏng của nghiên cứu, không phải cỡ mẫu hay threshold production cho bài vocabulary mục tiêu.

Production implication:

- version hóa model, prior, discrepancy list, số posterior draws, số replicate và random seed;
- chạy PPC trên calibration/QA sample, không nhất thiết chạy toàn bộ mỗi session người dùng;
- giữ discrepancy theo band, pair và cluster để biết model hỏng ở đâu;
- nếu PPC phát hiện local dependence, sửa item bank, cluster-bootstrap/cluster model hoặc nới uncertainty; không chỉ tăng số câu.

### 3.4 SBC kiểm tra code/inference, không kiểm tra toàn bộ validity

Talts et al. giới thiệu SBC bằng cách sinh tham số và dữ liệu từ joint prior, chạy inference, sau đó kiểm tra rank statistics của giá trị thật trong posterior samples có gần discrete-uniform hay không. Đây là test tốt cho lỗi implementation, likelihood, sampler hoặc posterior approximation.

Nhưng chính nguồn cũng giới hạn diễn giải: SBC chỉ xác nhận tính calibration của inference đối với model generative đã giả định. Nó không bảo đảm posterior cover ground truth của một observation cụ thể và không chứng minh model đủ phong phú để biểu diễn dữ liệu thật. PPC mới kiểm tra predictive behavior; external validation mới đo transportability/criterion validity.

Vì vậy pipeline phải có ba gate độc lập:

1. **SBC gate:** simulator → inference → rank histogram/diagnostics.
2. **PPC gate:** response replicate → discrepancy theo band/pair/cluster/format.
3. **External coverage gate:** mẫu người thật hold-out, full-form hoặc criterion subset; đo bias, MAE/RMSE và coverage 80/95%.

Không được đánh dấu estimator “đã calibrated” chỉ vì SBC pass.

### 3.5 Raw posterior-predictive p-value không phải p-value frequentist

Paganin và de Valpine ghi rõ posterior predictive p-values (ppp) dễ dùng nhưng phân phối của chúng không uniform dưới giả thuyết model sinh ra dữ liệu. Calibrated ppp cần một bootstrap-like procedure, đồng thời phải tính uncertainty của calibration; nghiên cứu đưa ra phương pháp giảm chi phí bằng các chain ngắn hơn trong các calibration replicates sau khi chain dữ liệu thật đã hội tụ.

Hệ quả:

- không dùng `ppp < 0.05` như một threshold universal cho item-bank acceptance;
- không diễn giải `ppp=0.50` như “model đúng 50%”;
- nếu cần một decision flag, calibrate threshold trên simulator có cùng item count, band design, response mechanism và dependence structure;
- lưu cả discrepancy, số replicate, Monte Carlo SE và calibration version;
- `ppp` là evidence về model criticism, không phải hiệu chỉnh trực tiếp `V_hat`.

## 4. Đề xuất tích hợp vào estimator hiện tại

Estimator chính vẫn là stratified estimator hoặc CAT/IRT sau calibration. Bayesian layer chỉ được bật sau pilot có response-level data và item metadata.

### 4.1 Output contract

```text
EstimateResult {
  vocab_hat,
  unit, universe_version,
  posterior_interval,       # chỉ uncertainty conditional on model/prior
  sampling_or_response_ci,  # stratified/cluster bootstrap hoặc response posterior
  sensitivity_range,        # prior/model/unit/corpus alternatives
  quality_flags: {
    sbc_status,
    ppc_status,
    ppc_discrepancies,
    prior_sensitive,
    local_dependence,
    floor_ceiling,
    missingness,
    external_coverage_status
  },
  calibration_version,
  model_version,
  seed
}
```

### 4.2 Pseudocode

```text
function validate_bayesian_vst(model_spec, calibration_data, simulator):
    assert model_spec.universe_version == calibration_data.universe_version

    sbc = run_sbc(
        simulator=simulator,
        model=model_spec,
        draws=prior_parameter_draws,
        replicated_datasets=sbc_replicates,
        checks=[rank_uniformity, sampler_diagnostics, recovery_bias]
    )
    if sbc.fail:
        return BLOCK("inference implementation not calibrated")

    posterior = fit_model(model_spec, calibration_data)
    ppc = posterior_predictive_checks(
        posterior=posterior,
        discrepancy=[
            band_score, item_residual,
            within_family_pair_score,
            semantic_cluster_score,
            shared_context_pair_score,
            format_and_position_score
        ],
        replicates=ppc_replicates,
        seed=model_spec.seed
    )
    return posterior, ppc

function estimate_vocab_with_bayesian_layer(session, fitted_model, design):
    responses = administer_with_anchors_and_exposure_control(session, design)
    posterior_draws = update_person_posterior(fitted_model, responses)
    V_draws = transform_each_draw_to_vocab_scale(
        posterior_draws,
        calibration=fitted_model.vocab_mapping,
        unit=fitted_model.universe.unit
    )

    posterior_interval = quantile_interval(V_draws, level=0.95)
    design_ci = cluster_or_band_bootstrap(responses, design)
    sensitivity = refit_or_reweight_under_alternatives(
        alternatives=[prior_set, Rasch_or_2PL, unit_mapping, exclusion_rules]
    )

    if posterior_predictive_flagged(fitted_model):
        quality = "diagnostic_only"
    elif not external_coverage_validated(fitted_model.calibration_version):
        quality = "model_conditional; coverage unverified"
    else:
        quality = "validated_for_target_population"

    return EstimateResult(
        vocab_hat=median(V_draws),
        posterior_interval=posterior_interval,
        sampling_or_response_ci=design_ci,
        sensitivity_range=sensitivity,
        quality_flags=quality,
        calibration_version=fitted_model.calibration_version
    )
```

### 4.3 Quy tắc stopping

Không dừng chỉ vì posterior interval hẹp. Dừng khi đồng thời:

1. `SE_theta` hoặc interval trên vocabulary scale đạt target đã đặt trước;
2. anchor consistency, missingness và exposure gates đạt yêu cầu;
3. không có PPC/local-dependence flag nghiêm trọng áp dụng cho form/model;
4. band/domain quotas cần thiết vẫn được phủ;
5. nếu dùng cho quyết định hành động, posterior probability quanh threshold phải đạt ngưỡng đã calibration trên hold-out, không chọn ngưỡng từ một session.

Nếu SBC/PPC chỉ là QA offline, một session có thể vẫn trả score nhưng phải gắn `coverage_unverified` hoặc `diagnostic_only` thay vì giả vờ có uncertainty toàn diện.

## 5. So sánh với Preply

| Thành phần | Preply methodology đã fetch | Thiết kế đề xuất sau iteration 21 |
|---|---|---|
| Estimand | Dictionary/headword universe, BNC-derived rank và derived-form aggregation theo mô tả vendor | Giữ universe/unit/version explicit; có thể thêm word-family/lemma nhưng không đổi scale âm thầm |
| Routing | Hai giai đoạn: screening rộng rồi narrow logarithmic range quanh midpoint | Stratified estimator/CAT có anchor, quota và inclusion log; Bayesian layer chỉ sau pilot |
| Uncertainty | Vendor nêu khoảng ±10% theo model của họ; chưa có response-level production data để kiểm định độc lập | Tách posterior interval, design/cluster CI, sensitivity range và external coverage; không tái dùng ±10% mặc định |
| Model fit | Không thấy production item bank, posterior model hoặc PPC trong methodology đã fetch; chưa tìm được nguồn xác thực cho phần này | SBC → PPC discrepancy → external hold-out coverage, mỗi lớp có trạng thái riêng |
| Local dependence | Chưa xác minh được item clustering/shared context trong production bank | Kiểm tra family/semantic/context pair residuals; cluster bootstrap hoặc model nếu dependence đáng kể |
| Guessing | Preply methodology hiện có ghi vendor midpoint/rounding; production guessing controls chưa xác minh được | Giữ quality signal và sensitivity; không dùng raw ppp/automatic `1/k` correction nếu chưa calibration |
| Kết quả người dùng | Một estimate làm tròn theo khoảng giá trị | Estimate + unit/version + interval components + flags; chỉ gọi “validated” khi hold-out coverage đạt gate |

Đây là so sánh với methodology đã fetch, không phải khẳng định về code/item bank hiện tại của Preply. Direct Preply fetch trong môi trường nghiên cứu vẫn bị 403 và chưa có dữ liệu response-level, nên phần “không công khai/không xác minh” phải giữ nguyên.

## 6. Assumptions và gaps còn lại

### Assumptions cần ghi trong manifest

- Model generative có thể mô phỏng response mechanism đủ gần để SBC/PPC có ý nghĩa.
- Prior được version hóa và sensitivity set đã được định trước, không chọn sau khi thấy kết quả.
- Item cluster, semantic relation, shared context và format metadata đầy đủ để kiểm tra dependence.
- Posterior sampling hội tụ; chain diagnostics và effective sample size đủ cho interval/ppp.
- Vocabulary mapping từ latent ability sang `V` được fit trên calibration sample độc lập và giữ bất biến trong một universe version.
- External coverage được đo trên population/intent-of-use mà sản phẩm định báo cáo.

### Chưa thể kết luận từ nguồn hiện có

- Chưa có số draw/replicate, prior, ppp threshold hoặc model class tối ưu riêng cho vocabulary test mục tiêu.
- Chưa có production item bank/response-level/routing data của Preply để chạy SBC/PPC, kiểm tra local dependence hoặc xác nhận ±10%.
- Chưa có common-person/common-item sample để đo coverage khi chuyển posterior ability sang headword/lemma/word-family count.
- Chưa có bằng chứng cho phép gọi một posterior interval là confidence interval theo nghĩa frequentist trên quần thể người dùng mục tiêu.
- Chưa tìm được nguồn xác thực cho bất kỳ quy tắc Bayesian production hiện tại nào của Preply; không suy diễn từ vendor methodology.

## 7. Validation plan tiếp theo

1. Xây simulator có universe, frequency bands, item clusters, guessing/missingness và response dependence đã biết; chạy SBC với nhiều prior.
2. Chạy PPMC trên calibration response data với discrepancy định trước; so sánh raw ppp và calibrated ppp qua double simulation.
3. Fit model trên train split, đánh giá item/ability prediction và interval coverage trên hold-out; báo bias, MAE/RMSE, coverage 80/95%, interval width.
4. Lặp theo proficiency, L1, domain và form; kiểm tra DIF, floor/ceiling và local dependence.
5. So sánh posterior output với stratified estimator và Preply-style midpoint trên cùng người, cùng universe khi có thể; không gộp các estimand khác đơn vị.
6. Chỉ sau khi các gate đạt mới chọn target SE, max items, calibration version và wording “validated” trong UX.
