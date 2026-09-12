# Iteration 72 — Argument-based validity và inference chain cho vocabulary-size test

## 1. Phạm vi và kết luận

Iteration này không tìm thêm một công thức biến số câu đúng thành số từ. Trọng tâm là kiểm tra **chuỗi suy luận** đứng sau mọi con số: từ response quan sát được, qua scoring và generalization từ item sample tới vocabulary universe, rồi mới xem có thể extrapolate sang lexical ability ngoài test và dùng cho quyết định nào.

Kết luận chính:

1. **Validity là tính hợp lệ của một cách diễn giải và cách sử dụng score trong một population/use cụ thể**, không phải nhãn cố định của item bank. ETS yêu cầu công khai construct, mục đích, claim, intended interpretation và population; evidence phải được tổ chức thành một validity argument và tăng theo hậu quả của quyết định.
2. Một vocabulary estimator cần tách tối thiểu sáu gate: `domain_definition`, `evaluation/scoring`, `generalization`, `explanation`, `extrapolation` và `utilization`. Mỗi gate phải có claim, warrant, assumption, backing, rebuttal và trạng thái evidence.
3. `K_breadth` có thể là một ước lượng được calibration cho **receptive vocabulary universe đã định nghĩa**, nhưng không tự động là reading/listening/productive ability, CEFR hay placement score. Generalization tới word universe và extrapolation tới performance thực tế là hai inference khác nhau.
4. Nghiên cứu vocabulary thực tế cho thấy một bài có thể có item fit hoặc tương quan có ý nghĩa nhưng vẫn thất bại ở các inference khác: floor effect, item quá khó, reliability thấp, construct representation lệch và không có evidence cho extrapolation/utilization.
5. Preply công khai khá rõ domain/scoring heuristic: dictionary hơn 45.000 entries, hai phase khoảng 40 + 120 từ, midpoint trên sample logarithmic, main dictionary entries và margin vendor ±10,33%. Tuy nhiên đó là **vendor methodology disclosure**, chưa phải một validity argument độc lập. Trang đã fetch không cung cấp evidence cho alternate-form generalizability, response-process explanation, external extrapolation hay decision-use validity.

Khuyến nghị implementation: phát hành score dưới dạng `K_breadth` kèm `claim_status` và `evidence_status`; chỉ ghi `validated_for_breadth` sau khi các gate cần thiết cho intended use pass. Nếu extrapolation hoặc utilization chưa được kiểm chứng, hiển thị rõ `extrapolation_unverified` thay vì đổi tên count thành “English level”.

## 2. Nguồn đã fetch và verify

| Nguồn | HTTP | Vai trò | Giới hạn |
|---|---:|---|---|
| [ETS Standards for Quality and Fairness](https://www.ets.org/pdfs/about/standards-quality-fairness.pdf) | 200 | Chapter 4: intended construct/use/population; coherent validity argument; evidence, alternative explanations, precision, misuse warning và re-evaluation | Chuẩn tổ chức/assessment tổng quát, không phải vocabulary-specific cutoff |
| [ETS — A Validity Framework for the Use and Development of Exported Assessment](https://www.ets.org/pdfs/about/exported-assessments.pdf) | 200 | Sáu component, Toulmin grounds/warrant/assumption/backing/rebuttal; domain, evaluation, generalization, explanation, extrapolation, utilization | Tập trung exported assessments và fairness giữa populations; cần chuyển thành vocabulary manifest |
| [Bennett, Kane & Bridgeman — Theory of Action and Validity Argument](https://www.ets.org/Media/Research/pdf/TCSA_Symposium_Final_Paper_Bennett_Kane_Bridgeman.pdf) | 200 | Phân biệt generalization tới universe acceptable/exchangeable và extrapolation tới target domain; cảnh báo task/form/year effects | Ví dụ K-12 assessment, không xác nhận ngưỡng vocabulary |
| [Rafatbakhsh & Ahmadi (2022), The Argument-Based Validation of a Large-Scale High-Stakes Vocabulary Test](https://files.eric.ed.gov/fulltext/EJ1375427.pdf) | 200 | Case vocabulary trực tiếp: 12.500 response, 3 phiên bản, 5 năm, corpus/wordlists/Rasch/factor; evidence và threats theo inference | Bối cảnh kỳ thi PhD Iran; không chuyển trực tiếp sang online short form |
| [Preply — How the vocab test works](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) | 200 | Vendor disclosure được fetch trong callback: universe, lexical rule, corpus, sampling, midpoint và margin | Proxy fetch; direct Preply endpoints trả 403. Không có response-level calibration/independent validation trong trang đã fetch |

Direct page của Preply được probe riêng và trả HTTP 403; không dùng response đó làm evidence. Proxy ở bảng trên trả HTTP 200 và có nội dung methodology. Mọi claim về Preply trong file này đều được gắn nhãn vendor disclosure hoặc “không được trang công khai xác minh”, không coi là control ẩn đã tồn tại.

## 3. Evidence mới

### 3.1 Validity phải gắn với claim, use và population

ETS SQF Chapter 4 nêu rằng validity là khái niệm thống nhất, nhưng không dựa trên một nghiên cứu hay một loại evidence duy nhất. Loại và mức evidence phụ thuộc mục đích test và hậu quả của quyết định. Standard 4.1 yêu cầu mô tả construct, purpose, claims, intended score interpretation và intended population. Standard 4.2 yêu cầu validation plan trước operational use; Standard 4.3 yêu cầu xem alternative explanations, mô tả quy trình để người có chuyên môn có thể đánh giá/tái lập và nêu precision; Standard 4.4 yêu cầu cảnh báo misuse; Standard 4.6 yêu cầu reevaluate khi technology, content, purpose hoặc population thay đổi.

Áp dụng vào vocabulary-size test:

- Claim “người làm biết khoảng `K` lexical units trong universe `U`” khác claim “người làm đọc được văn bản X” hoặc “đạt CEFR B2”.
- Cùng một response data có thể đủ cho diagnostic breadth nhưng chưa đủ cho placement hay high-stakes decision.
- CI hẹp chỉ mô tả một lớp uncertainty của estimator; nó không tự chứng minh construct representation, external prediction hay beneficial use.

### 3.2 Sáu component tạo thành một chuỗi có thể bị rebuttal

ETS framework tổ chức argument thành:

1. **Domain definition** — construct và domain nào được đo, item có đại diện và tránh construct-irrelevant variance hay không.
2. **Evaluation** — response được chấm bằng rule nào, score có intended characteristics và có tương đương giữa population không.
3. **Generalization** — score từ một testing instance có đại diện cho universe item/task, form, site và occasion hay không.
4. **Explanation** — score có phản ánh KSA/lexical construct theo cognitive process dự kiến hay do format, language burden, strategy hoặc context khác.
5. **Extrapolation** — score/universe score có dự báo performance trong target domain ngoài testing situation hay không.
6. **Utilization** — score có đủ thông tin, liên quan và chính xác cho decision/use dự kiến; benefit/harm và misuse phải được đánh giá.

Toulmin structure của framework tách:

```text
grounds      = observed responses, item metadata, calibration and validation data
warrant      = rule nối grounds với claim
assumptions  = exchangeability, construct relevance, population support, score meaning
backing      = corpus review, expert review, pilot, psychometrics, external criteria
rebuttals    = floor/ceiling, DIF, speededness, ambiguity, domain shift, missingness, misuse
claim        = score interpretation hoặc action được phép phát hành
```

Điểm quan trọng cho estimator: rebuttal không phải “ghi chú phụ”. Nếu một rebuttal đủ mạnh, claim tương ứng phải hạ từ `validated` xuống `provisional` hoặc bị chặn.

### 3.3 Generalization không đồng nghĩa extrapolation

Bennett, Kane và Bridgeman định nghĩa generalization là mở rộng từ tập performance quan sát được tới universe các performance được xem là acceptable hoặc exchangeable theo testing procedure. Universe score là expected value trên universe này; G-study là một cách thu thập evidence.

Extrapolation lại mở rộng từ universe score của procedure tới universe performance lớn hơn mà người dùng quan tâm. Với test chỉ gồm objective items hoặc task hẹp, bước này thường questionable và cần empirical support. Khác biệt giữa form, task, population hoặc year nếu không được kiểm soát có thể tạo chênh lệch score không phải khác biệt thật của construct.

Với vocabulary estimator:

```text
response sample -> K_breadth trong U       = generalization question
K_breadth -> reading/listening/productive  = extrapolation question
K_breadth -> placement/CEFR/decision       = utilization question
```

Do đó công thức dưới đây có thể ước lượng breadth nhưng không được tự gắn nhãn functional proficiency:

```text
p_hat_h = sum_i_in_band_h(w_i * z_i) / sum_i_in_band_h(w_i)
K_hat   = sum_h(M_h * p_hat_h)
```

`M_h` là số lexical units của band `h` trong frozen universe; `z_i` là response/latent known score sau scoring rule; `w_i` là design/route/nonresponse weight đã kiểm tra support. Interval phải dùng joint replicate hoặc bootstrap/path simulation đã validate, không gọi nó là evidence cho extrapolation.

### 3.4 Case study vocabulary cho thấy cần gate theo inference

Rafatbakhsh và Ahmadi (2022) nghiên cứu vocabulary subsection của kỳ thi đầu vào PhD: ba test versions trong năm năm, 12.500 test-takers. Họ dùng corpus linguistics, COCA, AWL/AVL, Rasch và factor analysis; phân tích bốn inference gồm domain definition, evaluation, generalization và explanation. Kết quả tổng hợp nêu threats ở vocabulary choice, item difficulty, item discrimination, construct representation và reliability; tác giả kết luận các claim không được evidence hỗ trợ đầy đủ và test không hoàn toàn hợp lệ để đánh giá lexical knowledge cho academic purposes.

Các failure cụ thể:

- Humanities: 33,3%–44,5% trong 1.000 người mỗi năm bỏ trống toàn bộ 30 câu English; trong nhóm đã trả lời English, 23,9%–34% không trả lời vocabulary. Tổng cộng 53,2%–60,7% không trả lời vocabulary subsection.
- Mean vocabulary chỉ 1,5–1,6/12; ability trung bình thấp hơn cả item dễ nhất, tạo floor effect.
- Tương quan vocabulary với grammar là 0,445, 0,493 và 0,333 cho humanities, engineering và English language; với reading là 0,493, 0,538 và 0,395. Tương quan có ý nghĩa nhưng yếu không đủ để chứng minh một extrapolation mạnh.
- Vì không còn access tới test-takers, nghiên cứu không đánh giá extrapolation và utilization/impact. Đây là giới hạn evidence, không phải bằng chứng rằng hai inference đã pass.

Hệ quả: item-model fit hoặc một correlation không thể thay thế domain coverage, ability support, generalizability và external-use evidence.

## 4. Thuật toán đề xuất: validity-aware vocabulary estimator

### 4.1 Manifest và evidence object

Mỗi version phải freeze cả measurement scale và argument:

```text
manifest:
  manifest_version
  target_population
  intended_use
  construct_in_scope: receptive lexical units in U
  construct_out_of_scope: productive ability, listening, CEFR, placement unless linked
  lexical_unit_rule
  dictionary_version, corpus_version
  bands[h].definition, bands[h].M_h
  sampling_and_weighting_rule
  response_formats, key_version, missingness_rule
  uncertainty_method, alpha, target_coverage
  max_length, exposure_policy, revalidation_trigger

validity_manifest[]:
  claim_id
  claim_text
  inference: domain|evaluation|generalization|explanation|extrapolation|utilization
  grounds[]
  warrant
  assumptions[]
  backing_urls[]
  rebuttals[]
  evidence_status: pass|partial|fail|not_studied
  population_scope
  intended_use_scope
  last_review
```

`evidence_status=pass` chỉ có nghĩa là evidence đủ cho claim/use đã khai báo; không phải certificate cho mọi use khác.

### 4.2 Gate logic

```text
DOMAIN:
  U, M_h, lexical unit, corpus/rank version, population và intended use đã freeze
  item coverage/relevance qua expert + corpus review

EVALUATION:
  key/acceptable response và scoring rule đã audit
  response process, missingness, floor/ceiling và item fit không tạo rebuttal nghiêm trọng

GENERALIZATION:
  item inclusion/route weights có support
  alternate forms hoặc G-study/replicate evidence ổn định
  conditional interval coverage đạt target trên population đã khai báo

EXPLANATION:
  cognitive/process evidence không cho thấy construct-irrelevant explanation trội
  dimensionality/IRT và convergence evidence phù hợp với construct breadth

EXTRAPOLATION:
  external relevant task/criterion đã pre-specify và hold out
  mapping từ K_breadth tới target performance có calibration/transport evidence

UTILIZATION:
  use/decision, loss, warning và consequence review được ghi rõ
  precision đủ cho decision; misuse ngoài scope được cảnh báo
```

Nếu mục tiêu chỉ là diagnostic breadth, `EXTRAPOLATION` có thể là `not_studied`, nhưng output phải ghi `extrapolation_unverified`; không được gọi là pass ngầm. Nếu mục tiêu placement, gate này là bắt buộc.

### 4.3 Pseudocode

```text
function estimate_vocabulary(session, bank, manifest, validity_manifest):
    assert manifest_is_frozen(manifest)
    claims = resolve_claims_for_use(manifest.intended_use, validity_manifest)

    domain = check_domain_gate(bank, manifest, claims)
    scored = score_responses(session, bank, manifest)
    evaluation = check_evaluation_gate(scored, bank, manifest, claims)

    if not domain.pass or not evaluation.pass:
        return provisional_result(
            reason = domain.rebuttals + evaluation.rebuttals,
            claim_status = downgrade_claims(claims)
        )

    replicates = []
    for draw in joint_calibration_route_response_draws(bank, session, manifest):
        rows = replay_or_resample_items(session, draw, manifest)
        for band in manifest.bands:
            numerator = sum(row.weight * row.known_score
                            for row in rows if row.band == band)
            denominator = sum(row.weight
                              for row in rows if row.band == band)
            p_hat[band] = numerator / denominator if denominator > 0 else null
        K_draw = sum(manifest.bands[h].M_h * p_hat[h]
                     for h in manifest.bands if p_hat[h] is not null)
        replicates.append({"K": K_draw, "p_by_band": p_hat})

    generalization = check_generalization_gate(
        replicates, bank, manifest, claims
    )
    explanation = check_explanation_gate(bank, session, manifest, claims)
    extrapolation = check_extrapolation_gate(
        external_criterion_data_or_null, manifest, claims
    )
    utilization = check_utilization_gate(
        intended_use=manifest.intended_use,
        interval=quantiles(replicates, [0.025, 0.5, 0.975]),
        claims=claims,
        warnings=collect_rebuttals()
    )

    status = classify_claims(
        domain, evaluation, generalization, explanation,
        extrapolation, utilization
    )
    return {
        "K_breadth_median": median([r.K for r in replicates]),
        "K_breadth_interval": quantiles([r.K for r in replicates], [0.025, 0.975]),
        "band_estimates": summarize_bands(replicates),
        "claim_status": status,
        "rebuttals": collect_rebuttals(),
        "manifest_version": manifest.manifest_version
    }
```

### 4.4 Release labels

| Label | Ý nghĩa | Output được phép |
|---|---|---|
| `validated_for_breadth` | Domain, scoring/evaluation, generalization và các gate cần cho breadth đã pass; uncertainty coverage đã kiểm tra | `K_breadth` + interval + universe/lexical-unit definition |
| `breadth_validated_extrapolation_unverified` | Breadth đủ evidence nhưng chưa có external link tới performance | Count diagnostic; cấm đổi tên thành level/CEFR/placement |
| `provisional` | Một essential gate partial, bank support yếu, floor/ceiling, missingness hoặc rebuttal chưa giải quyết | Median/interval nếu tính được, kèm reason và sensitivity; không quảng cáo như precise |
| `not_supported` | Domain hoặc scoring fail, hoặc evidence mâu thuẫn nghiêm trọng | Không phát hành count cho intended use; chỉ trả lỗi/diagnostic nội bộ |

Các threshold như CI width, coverage, sample size, decision stability và hard maximum phải pilot-calibrate theo population/use. Không suy ra một threshold phổ quát từ ETS, nghiên cứu PhD hoặc margin của Preply.

## 5. Đối chiếu với Preply

| Thành phần | Preply disclosure đã verify qua proxy | Kết luận theo argument-based design |
|---|---|---|
| Domain | Dictionary hơn 45.000 entries; main entries; một definition; derived forms cộng về headword; BNC spoken/written rebalanced; loại deducible, slang/dialect/scientific/archaic và cognate/false-friend Portuguese | Có grounds cho một receptive dictionary-defined universe, nhưng phải giữ nguyên target population và exclusion policy; không gọi là universal English vocabulary |
| Sampling/generalization | Khoảng 40 item broad rồi khoảng 120 item narrow; frequency order; sample logarithmic; midpoint trên blank-before và checked-after | Heuristic có thể định vị boundary, nhưng trang không công khai G-study, alternate-form equivalence, inclusion probability, response-dependent route variance hay empirical interval coverage |
| Scoring/evaluation | Checkbox known/unknown và midpoint cancellation được mô tả; rank/logarithmic details được giải thích | Cần audit key, meaning of “know”, guessing/partial knowledge, missingness, floor/ceiling và item fit độc lập |
| Uncertainty | Vendor nêu ±10,33%: SD xấp xỉ 0,25 vocabulary size, average 22,5 samples, SE 0,0527, nhân 1,96; 120 words phase hai; 5% cần thêm khoảng 380 words theo trang | Đây là model-based vendor margin. Chưa có evidence trong page cho calibration error, route/model/key uncertainty, conditional coverage hoặc external prediction; không dùng làm universal margin |
| Extrapolation | Trang mô tả mục tiêu so sánh language acquisition và “receptive vocabulary”, không cung cấp criterion study cho reading/listening/productive use | Report chỉ nên là `K_breadth`; `CEFR`, placement và functional claims là `extrapolation_unverified` nếu không có calibration riêng |
| Utilization | Có mục tiêu tool nhanh, meaningful, vui và so sánh nhóm | Intended use thấp-stakes diagnostic có thể khác placement/high-stakes; user-facing warning phải cấm các use ngoài evidence |

Gap product-specific: **chưa tìm được nguồn xác thực cho ý này** về việc Preply có item calibration posterior, G-study/alternate-form evidence, response-process evidence, external criterion linking, population-specific coverage hay decision-use validation của margin ±10,33%.

## 6. Validation plan

### A. Domain và scoring

- Freeze `U`, dictionary/corpus/version, lexical-unit rule, one-definition policy, exclusions, target population và intended use trước pilot.
- Tạo trace cho từng item: source rank, band, headword/lemma/family, sense, rationale chọn/bỏ, key version và acceptable responses.
- Cognitive interview với target population để kiểm tra “know one definition”, deducibility, context burden và interpretation của checkbox.
- Audit explicit missing/timeout/Not Sure khác `wrong`; kiểm floor/ceiling và support của từng band.

### B. Generalization

- Random/stratified forms với item inclusion probability đã biết; lưu route seed và common anchors.
- G-study hoặc nested replicate study trên person × item × form × occasion; báo conditional error theo band/ability, không chỉ coefficient tổng.
- Kiểm CI coverage bằng simulation finite-universe có `M_h` biết trước và holdout forms/persons. So sánh midpoint/log-rank, design-weighted estimator, fixed IRT và joint replicate estimator.
- Nếu item bank thiếu information ở tail hoặc subgroup, trả `provisional`; không bù bằng prior mạnh hay CI plug-in hẹp.

### C. Explanation và extrapolation

- Factor/IRT/model comparison và response-process evidence để kiểm tra breadth có bị thay bằng reading grammar, language burden, strategy hoặc format familiarity.
- Thu external criterion đã định nghĩa trước: ví dụ receptive recognition, reading/listening task hoặc productive task tương ứng; tách từng modality và domain.
- Dùng holdout và calibration/transport check để đo prediction, conditional error và subgroup invariance. Không biến một correlation thành correction coefficient nếu chưa có evidence thiết kế đúng.

### D. Utilization và revalidation

- Viết decision table: diagnostic count, progress monitoring, curriculum feedback, placement hay high-stakes; mỗi use có precision/harm requirement riêng.
- User study kiểm tra người dùng có diễn giải count thành CEFR hoặc ability không; nếu có nguy cơ, warning phải hiển thị ngay score.
- Re-run validity review khi đổi dictionary/corpus, exclusion, UI/technology, response format, routing, scoring model, population hoặc intended use.
- Lưu report version, evidence status, rebuttals, known gaps và ngày review để không nối các scale khác universe như learner growth.

## 7. Assumptions và gaps

### Assumptions được phép dùng trong estimator

- `U` và `M_h` là finite, versioned và được định nghĩa trước khi nhìn response.
- Item trong mỗi design stratum có exchangeability đủ cho generalization hoặc đã có weight/model bù được khác biệt.
- Response score đo đúng receptive lexical construct đã tuyên bố; “known” không mặc định là full productive mastery.
- Replicate/interval method được coverage-validate trên population/use tương ứng.
- Intended use được công khai và không mở rộng tự động từ diagnostic breadth sang placement/CEFR.

### Gaps hiện tại

- Chưa có response-level/item-bank/common-anchor data của Preply để test các gate evaluation/generalization/explanation.
- Chưa có external criterion data để validate extrapolation từ `K_breadth` tới reading, listening, productive use hoặc CEFR.
- Chưa có independent sample để kiểm vendor margin ±10,33%, nhất là tail, subgroup và route-dependent uncertainty.
- Chưa có calibration cho threshold `CI_width`, conditional coverage, minimum band ESS, decision stability hoặc label transition `provisional` → `validated`.
- **chưa tìm được nguồn xác thực cho ý này** về các control production ẩn của Preply; vì vậy không được điền giả vào `validity_manifest`.

## 8. Artifact/state liên quan

- Findings iteration 72: `state/findings.jsonl`, append từ 453 lên 461 dòng hợp lệ.
- Direction: `state/directions_tried.json`, iteration 72.
- Bằng chứng riêng lẻ được append với event `validity_is_claim_use_specific_argument`, `validity_chain_requires_warrants_and_rebuttals`, `generalization_and_extrapolation_are_separate_inferences`, `vocabulary_validity_study_found_chain_level_failures`, `floor_and_nonresponse_can_break_score_generalization`, `convergence_is_not_extrapolation_evidence`, `preply_current_methodology_disclosure_verified_via_proxy` và `adopt_claim_evidence_warrant_rebuttal_manifest`.
- Chưa có claim rằng thuật toán đã được pilot hoặc production-validated; artifact này là thiết kế evidence/release gate dựa trên các nguồn đã verify.
