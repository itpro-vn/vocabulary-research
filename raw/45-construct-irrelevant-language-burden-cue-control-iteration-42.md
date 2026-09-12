# Iteration 42 — construct-irrelevant language burden và cue control

## Phạm vi và trạng thái nguồn

Iteration này tách hai vấn đề thường bị gộp vào “độ khó item”:

1. **Construct-irrelevant language burden:** người làm bài không thể chứng minh biết target vì phải đọc, nghe, viết hoặc xử lý ngữ pháp vượt quá yêu cầu của vocabulary construct.
2. **Cue-induced guessing:** người chưa biết target vẫn chọn đúng nhờ hình thức câu hỏi, độ dài đáp án, distractor vô lý hoặc dấu hiệu biên tập.

Các URL dưới đây được fetch bằng `curl -L` với browser User-Agent và trả HTTP 200:

- Read (2007), *Second Language Vocabulary Assessment*, ERIC PDF: <https://files.eric.ed.gov/fulltext/EJ1072194.pdf>
- Schmitt (1994), *Vocabulary Testing: Questions for Test Development with Six Examples of Tests of Vocabulary Size and Depth*, ERIC PDF: <https://files.eric.ed.gov/fulltext/ED380993.pdf>
- ETS, *Standards for Quality and Fairness*: <https://www.ets.org/content/dam/ets-org/pdfs/about/standards-quality-fairness.pdf>

URL tham khảo của Preply `https://preply.com/en/learn/english/test-your-vocab` trả HTTP 403 trong callback. Vì vậy không dùng trang đó để xác nhận item wording, context burden, distractor design hay cue-control của Preply; **chưa tìm được nguồn xác thực cho các đặc điểm này của Preply**.

## Bằng chứng đã xác minh

### 1. Frequency sampling cần item đơn giản và đủ lớn

Read (2007) mô tả vocabulary-size test là phép ước lượng dựa trên việc lấy mẫu target words từ frequency lists. Vì cần sample tương đối lớn để ước lượng đáng tin, test designers có xu hướng dùng format đơn giản. Bài review đối chiếu Vocabulary Levels Test (matching synonym/short definition) và Vocabulary Size Test (target trong câu ngắn không định nghĩa, bốn lựa chọn định nghĩa); các format này cho bằng chứng trực tiếp hơn về việc một từ có được biết hay không.

**Hệ quả:** không tối ưu UX bằng cách làm stem/context phức tạp hơn nếu điều đó làm giảm số lexical units được lấy mẫu. Độ bao phủ frequency band và precision của `K_hat` phải được ưu tiên; độ dài/độ khó của ngôn ngữ phụ trợ chỉ nên vừa đủ để xác định sense cần đo.

### 2. Context có thể giúp nhận diện sense nhưng đồng thời thêm facet vào construct

Read (2007) mô tả hướng phát triển Yes/No spoken test với hai điều kiện: lexically bare syntactic context và semantically richer sentence context. Context có thể giúp người làm bài nhận dạng target chính xác hơn và liên kết phán đoán “biết từ” với một cách dùng cụ thể. Tuy nhiên, rich context cũng đưa comprehension, register và sense-in-context vào response process.

**Hệ quả:** breadth-only item nên có context tối thiểu, giàu từ tần suất cao, và khai báo sense; contextual-use/depth item phải là construct hoặc facet riêng. Không trộn hai context condition trong cùng một scale nếu chưa có common-item/common-person linking.

### 3. Phải giảm tải đọc/viết/nghe ngoài target word

Schmitt (1994) nêu rõ một task viết câu có thể thất bại vì người học biết nghĩa `gather` nhưng chưa đủ năng lực viết để biểu đạt; task nghe đồng thời đo listening. Những format đó phù hợp khi mục tiêu là kiểm tra việc sử dụng từ trong ngữ cảnh, nhưng kém phù hợp với phép đo rời rạc về việc có biết conceptual meaning hay không.

Khuyến nghị item-writing đã verify là giảm khó khăn của reading, writing, speaking và listening trong item; definitions và sentence/discourse context nên dùng những từ có tần suất cao hơn target.

**Hệ quả production:** `target_difficulty` không được suy ra chỉ từ tỷ lệ đúng. Item manifest phải có đánh giá burden của stem/definition/context và response mode; nếu burden cao, item cần sửa hoặc chỉ được dùng trong subtest use-in-context.

### 4. Cue trong MCQ có thể làm phồng score

Schmitt (1994) yêu cầu item không được “đánh lừa” người biết từ, nhưng cũng không được cho clue để người không biết đoán. Các clue được liệt kê gồm: đáp án đúng dài/ngắn bất thường, đáp án đối lập với đáp án đúng, alternatives lặp lại thông tin của đáp án đúng và distractors lố bịch. Bài viết minh họa một item mà đáp án đúng có vẻ như định nghĩa từ điển và dài hơn rõ rệt, khiến người không biết vẫn có thể chọn.

**Hệ quả:** tỷ lệ đúng cao không đủ để coi là vocabulary knowledge. Cần cả review mù bởi reviewer không biết answer key và kiểm tra empirical option functioning sau pilot.

### 5. Độ dài test là trade-off precision–fatigue, không phải hằng số UX

Schmitt (1994) ghi nhận nhiều item thường cho bức tranh chính xác hơn, nhưng fatigue tạo diminishing returns. Test phục vụ quyết định quan trọng cần dài và bao quát hơn; test motivational có thể ngắn hơn. Vì vậy, item budget phải gắn với intended use và stopping precision, đồng thời theo dõi abandonment/late-response/fatigue.

### 6. Accessibility và audit trail là quality evidence

ETS Standards yêu cầu ghi lại các quyết định lớn về construct, sampling và equating cùng rationale/data; item writers và reviewers phải có năng lực phù hợp; sampling method và tính đại diện phải được mô tả; product review cần bao gồm fairness và accessibility. ETS cũng yêu cầu evidence tương xứng với intended use và hậu quả của việc dùng điểm.

**Hệ quả:** accessibility/cue review không phải bước trang trí sau khi fit IRT. Nó là một release gate trước calibration, với versioned manifest và revision history.

## Item-accessibility và cue-audit gate đề xuất

Các trường dưới đây là **quy tắc engineering được suy ra từ bằng chứng**, không phải ngưỡng đã được nguồn xác minh hay ngưỡng Preply:

```text
ItemManifest {
  item_id, target, lexical_unit, sense_id, frequency_band,
  construct, modality, stem, definition, options, answer_key,
  context_word_frequency_summary,
  reading_burden_review,
  response_mode_burden_review,
  cue_review_flags,
  pilot_option_stats,
  revision_version
}
```

Trước calibration:

1. Chốt `construct = receptive_written_breadth` nếu mục tiêu là word-count breadth.
2. Viết stem/definition bằng từ và cấu trúc đơn giản hơn target; không dùng target hoặc cognate hiển nhiên trong clue.
3. Reviewer độc lập trả lời hai câu riêng: (a) người biết target có thể trả lời mà không cần writing/listening/depth skill không? (b) người không biết target có thể đoán từ độ dài, grammar, semantic overlap hoặc distractor quality không?
4. Gắn cờ item nếu reading burden, modality burden hoặc clue risk cao; sửa/xóa trước pilot, không “để IRT tự hấp thụ”.
5. Pilot với response-level data: item facility, discrimination, option selection, response time và DIF theo L1/proficiency/device. Một item có facility cao nhưng option pattern/cue flag bất thường không được xem là bằng chứng breadth tốt.
6. Tách các item rich-context, recall, listening hoặc productive thành construct/facet riêng; chỉ aggregate sau common-person/common-item linking và hold-out validation.

## Thuật toán tích hợp vào estimator

Estimator vẫn lấy `K_hat` từ breadth-only items và frequency strata; accessibility/cue controls quyết định item có đủ hợp lệ để đóng góp hay không.

```text
estimate_vocab_with_item_qc(session, universe, bands, item_bank, calibration):
    breadth_pool = filter(item_bank,
        construct == "receptive_written_breadth",
        modality == "written-recognition",
        cue_review_flags == clear,
        reading_burden_review == acceptable,
        response_mode_burden_review == acceptable)

    require coverage_check(breadth_pool, bands)
    responses = administer_anchors_and_stratified_sample(breadth_pool)

    for response in responses:
        response.p_known = calibrated_probability(
            response, calibration.breadth_model)

    for band in bands:
        usable = responses where band_id == band and item_qc == pass
        p_hat[band] = weighted_mean(usable.p_known, inclusion_weights)
        K_hat[band] = universe.N[band] * p_hat[band]

    K_hat = sum(K_hat[band])
    qc = {
      "excluded_item_count": count_qc_failures(responses),
      "cue_flag_rate": cue_flag_rate(responses),
      "burden_flag_rate": burden_flag_rate(responses),
      "missing_rate": missing_rate(responses),
      "band_coverage": coverage_summary(responses)
    }

    if qc.cue_flag_rate > calibrated_limit or
       qc.burden_flag_rate > calibrated_limit:
        return K_hat, status="sensitivity_only", qc=qc

    return K_hat, status="descriptive_breadth", qc=qc
```

Với band `b`, nếu `N_b` là số lexical units của universe và `p_i` là calibrated probability of knowing cho item đã qua QC:

```text
p_hat_b = sum_i(w_i * p_i) / sum_i(w_i)
K_hat_b = N_b * p_hat_b
K_hat = sum_b K_hat_b
```

Khoảng bất định phải tách tối thiểu:

```text
CI_response_or_sampling
CI_model
CI_band_manifest_sensitivity
range_burden_cue_sensitivity
```

`range_burden_cue_sensitivity` không phải correction tự động. Tính lại score trong các kịch bản: (a) giữ mọi item pass; (b) loại item burden/cue borderline; (c) thay bằng alternate form đã cân bằng. Nếu interval thay đổi đáng kể, chỉ phát hành score có cờ sensitivity hoặc mở rộng test.

## So sánh với Preply

| Thành phần | Thuật toán đề xuất | Preply trong iteration này |
|---|---|---|
| Construct | Khai báo receptive written breadth; rich context/listening/recall tách facet | Không xác minh được item manifest hoặc construct metadata; trang trực tiếp HTTP 403 |
| Context | Minimal/high-frequency context cho breadth; rich context chỉ khi đã link | Chưa tìm được nguồn xác thực về context burden hoặc sense policy riêng của Preply |
| Guessing/cue | Pseudowords/response diagnostics và peer + empirical cue audit; không tự động coi đúng là biết | Chưa xác minh được distractor/options/anti-cue procedure của Preply |
| Accessibility | Manifest có burden reviews, modality, L1/population scope và revision history | Chưa xác minh được accessibility review hoặc item revision log |
| Precision | Item budget theo band và intended use; báo sensitivity do QC exclusion | Không có response-level data/conditional precision để kiểm tra trong callback |
| Word count | Chỉ breadth items đóng góp `K_hat`; contextual-use score không cộng vào count | Không kết luận được Preply đang đo breadth thuần hay vendor composite |

So sánh này không phải kết luận rằng Preply có cue hoặc burden; đó là **gap quan sát** do endpoint không cho phép kiểm tra artifact.

## Validation plan

1. Tạo hai hoặc nhiều item forms có cùng target/frequency blueprint: một form context tối thiểu và một form rich-context; randomize common-person sample.
2. Thu thập independent reviewer ratings về conceptual-meaning accessibility, reading burden, modality burden và cue risk; lưu reviewer qualifications, training, độc lập và agreement.
3. Pilot đủ đa dạng L1, proficiency, device và tốc độ; fit breadth-only model trước. Kiểm tra item fit, option functioning, local dependence, DIF và response-time flags.
4. So sánh `K_hat` giữa form sau equating. Kiểm tra mean difference, conditional SEM và coverage của interval trên held-out criterion như meaning-recall hoặc task-specific lexical coverage.
5. Làm ablation: bỏ item bị burden/cue flag và đo thay đổi score, band coverage, information và subgroup gaps. Nếu loại item làm score đổi mạnh, item bank có construct-irrelevant contamination.
6. Chỉ chọn các ngưỡng `acceptable`, `calibrated_limit`, minimum item count và stopping rule sau pilot/hold-out; không lấy ngưỡng từ Schmitt/Read/ETS như universal constants.

## Gaps

- Không có item-level Preply data, item wording, distractor statistics, response logs, readability/accessibility review hoặc cue audit công khai được xác minh trong iteration này.
- Chưa có hệ số phổ quát biến reading burden, context richness hay cue risk thành số từ; **chưa tìm được nguồn xác thực cho hệ số correction riêng của Preply**.
- Cần calibration common-person/common-item để quyết định context tối thiểu có thay đổi scale theo L1/proficiency/modality hay không.
