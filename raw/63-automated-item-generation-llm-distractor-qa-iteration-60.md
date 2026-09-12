# Iteration 60 — Automated item generation, LLM distractors và QA psychometric

## Phạm vi và kết luận

Iteration này kiểm tra một lớp khác của thuật toán vocabulary-size test: có thể dùng NLP/LLM để tạo stem, câu contextualized và distractors hay không, và điều kiện nào phải có trước khi item được đưa vào item bank đã calibration.

Kết luận bảo thủ:

- LLM/automatic item generation phù hợp ở **candidate layer**: tạo nhiều câu, lựa chọn và distractor để con người/validator chọn lọc.
- Không được coi item sinh tự động là đã valid chỉ vì câu có vẻ tự nhiên hoặc semantic similarity cao.
- Một nghiên cứu vocabulary-cloze dùng GPT trên 60 item báo cáo chỉ 75% câu được reviewer đánh giá well-formed và 66,85% options phù hợp. Đây là bằng chứng trực tiếp rằng human review/validation là bắt buộc.
- Distractor phải qua hai lớp: (1) linguistic/construct correctness — chỉ có một đáp án đúng, đúng POS/sense/context; (2) psychometric functioning — difficulty, discrimination, option selection, DIF, local dependence và reliability từ pilot response data.
- Nếu item bank được thay bằng item sinh mới, mọi item phải được pretest và calibration/equating lại. Không được dùng chất lượng sinh item để suy ra `K_hat` hoặc chuyển đổi số từ.
- Với Preply, hai endpoint được kiểm tra đều HTTP 403 trong iteration này; **chưa tìm được nguồn xác thực cho việc Preply dùng LLM/AIG, quy trình human review, distractor filtering hoặc psychometric pretesting**.

## Nguồn đã fetch và kiểm tra

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| Wang et al. (2023), ACL Anthology — VocaTT | 200 | Pipeline GPT tạo câu/options cho vocabulary cloze; tỷ lệ expert review và failure modes |
| Taslimipoor et al. (2024), ACL Anthology | 200 | Hai bước generate/filter distractors và clustering theo semantic similarity |
| Alhazmi et al. (2024), ACL Anthology | 200 | Survey task/dataset/method/evaluation của distractor generation |
| Qiu et al. (2020), ACL Anthology | 200 | Distractor cần incorrect + plausible; framework tách correctness/plausibility |
| ETS K–12 Item Development | 200 | Writing guidelines và trained item writers cho item quality |
| ETS (2019), *Distractor Analysis for Multiple-Choice Tests* | 200 | Mô hình response cho distractors và các chỉ số fit/information/reliability |
| Preply vocabulary-test và how-it-works | 403 | Không citable cho cơ chế generation/QA hiện tại; chỉ ghi gap |

## Bằng chứng đã xác minh

### 1. VocaTT cho thấy generation và item acceptance là hai việc khác nhau

Wang et al. mô tả VocaTT gồm ba bước:

1. tiền xử lý danh sách target words;
2. dùng GPT để tạo câu và candidate word options;
3. chọn các options phù hợp.

Trong thử nghiệm 60 câu target academic words, expert reviewers đánh giá:

| Hạng mục | Tỷ lệ được đánh giá đạt |
|---|---:|
| Sentence well-formedness | 75% |
| Suitable word options | 66,85% |

Đây là tỷ lệ của một thử nghiệm nghiên cứu, không phải ngưỡng production phổ quát. Nhưng nó đủ để bác bỏ giả định rằng generation output có thể đưa thẳng vào scored item bank.

Phân tích hậu kiểm của bài nêu các hướng cải thiện: đối chiếu part-of-speech tagging, sentence validation tốt hơn và cải thiện prompt. Trong vocabulary-size test, các lỗi này có thể làm thay đổi target sense, POS, grammatical fit hoặc độ khó của item. Vì vậy manifest phải lưu target, sense, POS, prompt/model/version, generated candidates và quyết định reviewer.

### 2. Distractor generation có thể tách correctness khỏi plausibility/diversity

Taslimipoor et al. (2024) trình bày pipeline hai bước: model sinh cả correct và incorrect options; một bước discriminator tách các ứng viên đúng khỏi distractors; distractors sau đó được gom cụm theo semantic similarity và chọn cluster heads để giữ các lựa chọn khác biệt. Bài báo báo cáo phương pháp vượt các model trước trên hai public datasets.

Qiu et al. (2020) nêu yêu cầu cốt lõi của distractor là vừa **incorrect** vừa **plausible**, và dùng các module riêng để bảo đảm tính sai cũng như điều khiển plausibility. Hệ quả cho vocabulary item:

- semantic similarity không được dùng làm bằng chứng rằng distractor là sai;
- một distractor quá vô lý không đo được vocabulary knowledge;
- một distractor cũng đúng ở sense khác làm item đa đáp án;
- clustering chỉ là diversity pre-screen, không thay thế pilot psychometrics.

### 3. NLP metrics không thay thế psychometric pretest

Survey EMNLP 2024 mô tả distractor generation như một task riêng, với datasets, methods và evaluation metrics cho objective questions. Điều này hữu ích để chọn candidate-generation benchmark, nhưng các metric NLP/semantic similarity vẫn không cho biết:

- item difficulty trên population mục tiêu;
- discrimination của item;
- option characteristic/distractor selection;
- DIF theo L1, trình độ hoặc nhóm dân số;
- local dependence với item khác;
- reliability và score invariance của whole test.

ETS (2019) minh họa việc phân tích distractors bằng ba response models, so sánh generalized residuals, information measures, scale scores và reliability estimates. Do đó item sau khi sinh phải đi qua response-data calibration; không thể release dựa trên LLM judge hoặc similarity score riêng lẻ.

### 4. Human review là control cần thiết, không phải sửa chữa tùy chọn

Trang ETS K–12 Item Development nêu high-quality test items là nền tảng của assessment fair, valid và reliable. ETS mô tả hai control liên quan trực tiếp:

- writing guidelines nghiêm ngặt;
- item writers có kinh nghiệm và được đào tạo về nguyên tắc viết item.

Nguồn này không đặt ra một tỷ lệ reviewer hay acceptance threshold chung cho mọi vocabulary test. Vì vậy hệ thống phải định nghĩa ngưỡng riêng bằng pilot và expert adjudication, rồi version hóa ngưỡng đó.

## Thiết kế item-bank manifest

Mỗi item, bất kể do người hay model tạo, cần lưu tối thiểu:

```text
item_id
lexical_unit                 # headword | lemma | word_family; không tự đổi estimand
unit_policy_version
frequency_band
corpus_version
register
modality
 target_sense
POS
stem_text
correct_option
candidate_options
option_order_seed
source_method                # human | template | LLM | hybrid
model_name_and_version
prompt_template_version
source_examples_or_corpus_ids
reviewer_status              # pending | accepted | rejected | revised
review_flags                 # POS, sense, ambiguity, grammar, clue, offensiveness
psychometric_status          # uncalibrated | pilot | calibrated | retired
anchor_flag
exposure_count
```

Generated text không được làm mất `frequency_band`, `lexical_unit`, `target_sense` hoặc corpus provenance. Nếu không xác định được sense/POS hoặc reviewer không đạt đồng thuận, item bị reject hoặc giữ ở trạng thái unscored.

## Thuật toán đề xuất: guarded generation → review → pilot → calibration

### Candidate generation

```text
input:
  target bank B with declared lexical unit, sense, POS, band, corpus version
  generation methods G = templates + constrained LLM + human candidates

for target t in B:
  candidates = generate(G, constraints={
      target=t,
      required_POS=t.POS,
      required_sense=t.sense,
      stem_readability_limit,
      context_not_giving_answer,
      no_duplicate_or_morphological_leakage
  })

  for candidate c:
      run lexical checks:
          POS_match(c, t)
          sense_match(c, t)
          grammar_ok(c)
          exactly_one_key(c)
          no_definition_or_spelling_clue(c)
          distractor_is_incorrect_in_target_sense(c)
          distractor_is_plausible_for_nonmaster(c)
      run diversity checks:
          no_duplicate_options(c)
          semantic_cluster_and_keep_distinct_options(c)

  send surviving candidates to independent human review
  if reviewer disagreement or any hard check fails:
      revise/reject; do not score
  else:
      store as `reviewed_un calibrated` and reserve for pilot
```

### Pilot and psychometric gate

```text
pilot administer accepted items to target-population sample
estimate item difficulty/discrimination and option-selection behavior
check DIF, local dependence, response-time/effort diagnostics and content balance

for each item:
    if content review fails: reject
    if ambiguous/multiple-key evidence: reject or rewrite
    if distractor is never selected or attracts high performers: flag/revise
    if DIF/local-dependence/fit threshold fails: flag, investigate, or retire
    else: calibrate item parameters and mark scored

assemble forms using only calibrated items
link new form to existing scale with common anchors
calculate K_hat only from calibrated response model/design estimator
```

## Công thức và quy tắc scoring

### Không có correction từ generation quality sang vocabulary count

Không dùng công thức kiểu:

```text
K_adjusted = K_raw × generation_quality
```

Tỷ lệ 75%/66,85% là tỷ lệ acceptance trong một study, không phải sensitivity/specificity của vocabulary knowledge và không phải hệ số hiệu chỉnh điểm.

### Item-level calibrated scoring

Sau pilot, với item `i`, dùng response model đã được chọn trước, ví dụ:

```text
P_i(theta) = logistic(a_i * (theta - b_i))
```

hoặc mô hình phù hợp hơn nếu response options cần modelling riêng. Từ posterior/ability estimate `theta_hat`, quy đổi sang count chỉ qua calibration trên declared vocabulary universe:

```text
K_hat = sum_h M_h * p_hat_h
```

Trong đó `M_h` là số lexical units của frequency stratum `h`, và `p_hat_h` là tỷ lệ/ước lượng mastery trong stratum từ calibrated item model hoặc design estimator. Không lấy `p_hat_h` từ tỷ lệ item được LLM-generated hay tỷ lệ item reviewer chấp nhận.

Nếu item bank thay đổi từ human-authored sang generated item, phải re-estimate `a_i`, `b_i` hoặc chứng minh common-anchor invariance. Nếu chưa có link, score mới chỉ là provisional form score, không được ghi đè scale cũ.

### Uncertainty

Báo riêng:

```text
CI_response_or_model
CI_item_sampling_or_stratum
CI_equating_or_anchor
sensitivity_content_review
sensitivity_generation_method
```

`generation_method_sensitivity` chỉ là khoảng thay đổi khi so sánh các form/item-bank đã được calibration tương ứng. Nó không phải một correction trực tiếp vào `K_hat`.

## So sánh với Preply

| Khía cạnh | Thiết kế đề xuất | Preply xác minh được trong iteration 60 |
|---|---|---|
| Item generation | Có thể dùng LLM/AIG ở candidate layer, kèm provenance và hard checks | Endpoint test và how-it-works trả 403; chưa tìm được nguồn xác thực cho generation method |
| Human review | Bắt buộc trước pilot; reviewer status/version lưu trong manifest | Chưa tìm được nguồn xác thực cho reviewer workflow |
| Distractors | Tách correctness, plausibility, diversity; sau đó pilot option functioning | Chưa tìm được nguồn xác thực cho distractor pipeline/current options |
| Calibration | Chỉ item calibrated mới góp vào `K_hat`; form mới link bằng anchors | Chưa xác minh item parameters, pilot, IRT hoặc common anchors của Preply |
| Scoring | `K_hat = Σ_h M_h p_hat_h`, không dùng generation acceptance làm hệ số | Preply production item bank/response data không fetch được trong callback |
| Uncertainty | Tách response/model, sampling, equating và content-generation sensitivity | Chưa xác minh interval coverage hay uncertainty decomposition hiện tại |

Các thông tin vendor đã được ghi ở các iteration trước chỉ được dùng như disclosed methodology khi URL fetch được; không suy diễn rằng Preply dùng pipeline ở trên.

## Validation plan và release gates

1. **Construct gate:** expert panel xác nhận target sense, POS, lexical unit, frequency band và intended receptive construct.
2. **Generation gate:** kiểm tra POS/sense/grammar, single key, clue leakage, duplicate/morphological leakage và option diversity.
3. **Blind human-review gate:** ít nhất hai reviewer độc lập trên sample; lưu disagreement, revision và lý do reject. Ngưỡng agreement phải được pilot xác định, không tự coi 100% là universal.
4. **Pilot gate:** dùng sample population mục tiêu; ước lượng difficulty, discrimination, option functioning, DIF và local dependence.
5. **Equating gate:** generated form chỉ lên cùng scale khi common anchors và invariance/fit pass; nếu không, phát hành provisional score riêng.
6. **Content-balance gate:** kiểm tra frequency bands, lexical units, POS, register, modality và target senses không bị generator làm lệch.
7. **Hold-out validity gate:** kiểm tra score trên criterion receptive vocabulary/reading đã định trước; không dùng reviewer acceptance làm criterion.
8. **Drift/security gate:** version prompt/model/corpus, monitor item exposure và drift; retire item khi generation model, corpus hoặc response behavior thay đổi.
9. **Release rule:** nếu item chưa human-reviewed hoặc chưa pilot-calibrated, chỉ dùng diagnostic/unscored; không góp vào `K_hat`.

## Gaps

- Preply endpoint và `how-it-works` trả HTTP 403 khi kiểm tra; chưa tìm được nguồn xác thực cho AIG/LLM usage, reviewer acceptance, distractor generation, current item pool, pilot data hoặc calibration.
- Chưa có response-level data để ước lượng liệu item generated có cùng difficulty/discrimination với item human-authored hay không.
- Tỷ lệ 75% và 66,85% đến từ nghiên cứu VocaTT trên 60 item academic words; không được chuyển thành ngưỡng production, correction factor hoặc margin of error cho sản phẩm mục tiêu.
- Chưa có bằng chứng cho một công thức phổ quát biến semantic similarity/LLM judgment thành item validity; cần pilot, blind review và hold-out criterion validation.

## URLs đã kiểm tra

- https://aclanthology.org/2023.nlp4dh-1.7/ — HTTP 200
- https://aclanthology.org/2024.lrec-main.452/ — HTTP 200
- https://aclanthology.org/2024.emnlp-main.799/ — HTTP 200
- https://aclanthology.org/2020.coling-main.189/ — HTTP 200
- https://www.ets.org/k12/capabilities/item-development.html — HTTP 200
- https://www.ets.org/research/policy_research_reports/publications/report/2019/kbgc.html — HTTP 200
- https://preply.com/en/learn/english/test-your-vocab — HTTP 403; không dùng làm bằng chứng nội dung
- https://preply.com/en/learn/english/test-your-vocab/how-it-works — HTTP 403; không dùng làm bằng chứng nội dung
