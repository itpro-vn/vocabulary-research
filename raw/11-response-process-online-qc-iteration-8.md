# Iteration 8 — Response-process, latency và quality control online

## 1. Câu hỏi của iteration

Các iteration trước đã xử lý sampling, IRT/CAT, validity, uncertainty, estimand headword/lemma/word-family, fairness và retest. Iteration này tập trung vào **quá trình trả lời** trong một bài vocabulary online:

- Có nên dùng response time (RT) để thay đổi điểm vốn từ không?
- Có nên loại hoặc giảm trọng số câu trả lời quá nhanh/quá chậm?
- Pseudoword false alarms nên là correction, quality flag hay cả hai?
- Làm thế nào phát hiện ceiling/low discrimination trong placement hoặc retest?
- Preply đã công khai các response-process controls này chưa?

Các nguồn dưới đây đã được fetch thực tế và kiểm tra HTTP 200 trong iteration 8:

- [Tanabe, *Measuring second language vocabulary knowledge using a temporal method* — ERIC PDF](https://files.eric.ed.gov/fulltext/EJ1098666.pdf)
- [Pellicer-Sánchez & Schmitt, *Scoring Yes–No vocabulary tests: Reaction time vs. nonword approaches* — PDF](https://www.lextutor.ca/rt/sanchez_schmitt_YN-RT-2012.pdf)
- [Lam, *Yes/no tests for foreign language placement at the post-secondary level* — Internet Archive text](https://archive.org/download/ERIC_EJ944127/ERIC_EJ944127_djvu.txt)
- [Preply methodology — fetched through r.jina.ai](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works)

Search snippets chỉ được dùng làm lead; các claim trong file này dựa trên nội dung đã fetch ở các URL trên.

## 2. Bằng chứng đã xác minh

### 2.1. RT liên quan đến lexical access, nhưng không đồng nghĩa với số lượng từ biết

Tanabe nghiên cứu 24 sinh viên đại học Nhật Bản với vocabulary breadth test 40 item. Vocabulary size và mean RT của các câu trả lời đúng có tương quan âm `r = -0.613`, `p < .001`. Nhóm có vocabulary size cao hơn có mean khoảng 4.441 từ và RT 3,77 giây; nhóm thấp hơn khoảng 3.075 từ và RT 5,90 giây.

Trong phân tích hồi quy nhỏ, chỉ giữ người có ít nhất 90% accuracy ở bài đọc, vocabulary score và vocabulary RT cùng giải thích 63,5% phương sai words-per-minute. RT có ý nghĩa (`p = .007`) trong khi score accuracy không đạt ngưỡng (`p = .073`). Tuy nhiên tác giả cũng ghi nhận power hậu nghiệm chỉ .187, thấp hơn .8; đây là bằng chứng gợi ý về lexical accessibility chứ không phải hệ số production để chuyển RT thành “số từ cộng thêm”.

**Hệ quả:** lưu `latency_ms`, RT theo band và RT của câu đúng như một output/diagnostic riêng. Không biến RT nhanh thành điểm vocabulary bổ sung nếu chưa có calibration criterion cho population mục tiêu.

Nguồn: [Tanabe PDF](https://files.eric.ed.gov/fulltext/EJ1098666.pdf), phần Abstract và Results, pp. 118–133.

### 2.2. Quy tắc loại RT cần pilot theo format/device, không dùng một cutoff toàn cục

Trong dữ liệu Tanabe, data screening loại 14 trong 705 câu trả lời đúng, khoảng 2%: 10 câu quá nhanh và 4 câu quá chậm. Kết quả cũng cho thấy RT không tăng một cách ổn định khi frequency giảm trên toàn bộ mẫu; xu hướng gần với kỳ vọng chỉ rõ hơn ở nhóm vocabulary lớn. Tác giả kết luận hiệu ứng frequency của tốc độ phụ thuộc vào vocabulary size.

**Hệ quả:** số 2% không phải tỷ lệ loại mặc định cho mọi sản phẩm. Một bài online cần pilot riêng theo thiết bị, browser, input method, latency mạng, format câu hỏi và nhóm trình độ. Quy tắc an toàn hơn là:

1. lưu raw latency và loại bỏ thời gian render/focus/blur không phải thời gian quyết định;
2. đặt các cờ robust theo người và item, ví dụ quantile/MAD trong pilot đã khóa;
3. dùng cờ để kiểm tra sensitivity/quality trước;
4. chỉ đổi `correct` thành `invalid` hoặc giảm trọng số khi có bằng chứng hold-out rằng quy tắc đó cải thiện criterion validity và CI coverage.

Nguồn: [Tanabe PDF](https://files.eric.ed.gov/fulltext/EJ1098666.pdf), Results và Limitations, pp. 126–136.

### 2.3. RT và pseudoword correction không có “người thắng” phổ quát

Pellicer-Sánchez và Schmitt so sánh phương pháp chấm dựa trên reaction time với các phương pháp correction dựa trên nonword trong Yes/No vocabulary test. Người làm bài sau đó được phỏng vấn để kiểm tra actual knowledge. Abstract báo cáo **không có phương pháp nào có ưu thế rõ ràng**; hiệu quả phụ thuộc vào false-alarm rate và mức độ overestimation của người làm bài.

Bài báo mô tả các loại response `hit`, `false alarm`, `miss`, `correct rejection`, cùng những công thức correction khác nhau dựa trên hit/false-alarm. Bài cũng dẫn lại các so sánh trong đó raw hits hoặc H–FA có thể dự báo tốt và tương đương các công thức phức tạp hơn trong một số bối cảnh. Vì vậy không được coi một công thức pseudo-word hoặc RT là chuẩn chung cho mọi L1, level và test format.

**Hệ quả:** nếu test có pseudowords, báo cáo ít nhất `H`, `FA`, tỷ lệ false alarm và cờ response-style. Có thể hiển thị raw estimate và adjusted sensitivity estimate như hai output, nhưng phải calibration bằng criterion data và hold-out. Không âm thầm trừ `1/k` hoặc trừ false alarms trong một test MCQ nếu item design không phải Yes/No signal-detection task.

Nguồn: [Pellicer-Sánchez & Schmitt PDF](https://www.lextutor.ca/rt/sanchez_schmitt_YN-RT-2012.pdf), Abstract và phần “The Yes–No test”/“Scoring the test”.

### 2.4. Online Yes/No có thể gặp ceiling và liberal response style

Lam báo cáo một online Spanish Yes/No test cho 785 sinh viên, 200 item, giới hạn 10 phút trong điều kiện không giám sát. Điểm trung bình tăng theo level, nhưng post-hoc comparisons không phân biệt được SPAN 211 với SPAN 212 và SPAN 212 với SPAN 300. Ở nhóm SPAN 211 tiếp tục lên SPAN 212, điểm lần hai cũng không tăng có ý nghĩa (`t(43) = 1.34`, `p > .05`). Tác giả kết luận test chỉ phân biệt các level liền kề tới low-intermediate trong chương trình đó.

Pseudoword false-alarm rate trung bình là 29% (SD 21%) trên toàn mẫu; tác giả diễn giải đây là liberal response strategy/low acceptance threshold. Đây là số liệu của bài Spanish cụ thể, không phải ngưỡng phổ quát cho English hay Preply.

**Hệ quả:** thuật toán cần chẩn đoán floor/ceiling và low-discrimination theo band/level. Nếu `p_correct` gần 1 trên các band cao hoặc item information thấp ở vùng quyết định, báo “ngoài vùng phân giải” thay vì phát hành một growth/placement claim chính xác giả. Pseudoword false alarms nên là quality flag và biến sensitivity, không tự động là phép trừ điểm đã xác thực.

Nguồn: [Lam text](https://archive.org/download/ERIC_EJ944127/ERIC_EJ944127_djvu.txt), Abstract, Procedure, Results và Discussion.

### 2.5. Preply công bố midpoint sampling và margin, nhưng gap về response process vẫn mở

Methodology đã fetch của Preply mô tả khoảng 40 từ ở bước screening, sau đó khoảng 120 từ trong vùng hẹp sắp theo frequency; điểm được lấy bằng midpoint giữa số từ chưa biết phía trước và số từ biết phía sau. Trang cũng công bố calculation cho margin khoảng `±10.33%` dựa trên assumption về độ lệch và số sample.

Trong nội dung methodology đã fetch, không thấy mô tả response-time model, quy tắc loại quá nhanh/quá chậm, pseudoword false-alarm control hoặc calibration độc lập cho attention/online response quality. Điều này **không chứng minh Preply không có các control nội bộ**; chỉ có nghĩa là chưa có nguồn công khai đã xác thực cho production behavior đó.

**Gap:** chưa có nguồn xác thực cho tác động của response-process controls trong item bank Preply production. Không được gắn các quy tắc RT/false-alarm bên trên cho Preply như thể đã là tính năng hiện hữu.

Nguồn: [Preply methodology](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works).

## 3. Thay đổi thuật toán đề xuất

### 3.1. Tách điểm vốn từ và response-process diagnostics

Mở rộng schema response:

```text
Response {
  session_id, item_id, answer, correct,
  latency_ms, rendered_at, presented_at, answered_at,
  skipped, focus_loss_count, device_class, form_id,
  pseudoword, quality_flags
}
```

Các output chính:

```text
vocab_estimate       # estimate theo universe/unit đã khai báo
vocab_interval       # uncertainty interval từ estimator/model
rt_summary           # median/log-RT của câu đúng, theo band
quality_flags        # too_fast, too_slow, focus_loss, high_FA, ceiling, floor
sensitivity_estimates# raw, quality-filtered, optional FA-adjusted; không trộn mặc định
```

`rt_summary` và `quality_flags` không được cộng/trừ trực tiếp vào `vocab_estimate` nếu chưa vượt validation gates.

### 3.2. Quality gate đề xuất

```text
function quality_diagnostics(responses, pilot_rules):
    usable = remove_render_and_network_time(responses)
    rt_flags = []
    for r in usable:
        if outside_person_item_pilot_bounds(log(r.latency_ms), pilot_rules):
            rt_flags.append((r.item_id, "latency_outlier"))
        if r.focus_loss_count > pilot_rules.max_focus_loss:
            rt_flags.append((r.item_id, "focus_loss"))

    fa_rate = null
    if any(r.pseudoword for r in usable):
        fa_rate = mean(r.answer == YES for r in usable if r.pseudoword)

    band_stats = summarize_accuracy_by_band(usable)
    ceiling = bands_with_low_information_or_accuracy_near_one(band_stats)
    floor = bands_with_accuracy_near_zero(band_stats)

    severe = (
        proportion_flagged(rt_flags) > pilot_rules.max_flag_rate
        or (fa_rate is not null and fa_rate > pilot_rules.fa_review_threshold)
        or too_many_focus_losses(rt_flags)
    )
    return {"rt_flags": rt_flags, "fa_rate": fa_rate,
            "ceiling_bands": ceiling, "floor_bands": floor,
            "severe": severe}
```

`pilot_rules` phải là phiên bản đã khóa từ calibration/validation, có provenance theo device và form. Nếu chưa có pilot, dùng cờ mô tả và sensitivity, không dùng cờ để thay đổi điểm chính.

### 3.3. Scoring rule an toàn trước calibration

```text
function estimate_vocab_with_qc(session, universe, bands, bank, pilot_rules):
    responses = administer_stratified_or_adaptive_test(session, bank)
    raw = estimate_vocab(responses, universe, bands)
    qc = quality_diagnostics(responses, pilot_rules)

    filtered = remove_only_pre_registered_invalid_events(responses, qc,
                                                         pilot_rules)
    sensitivity = estimate_vocab(filtered, universe, bands)

    if qc.severe or qc.ceiling_bands or qc.floor_bands:
        status = "estimate_with_quality_or_range_warning"
    else:
        status = "estimate_interpretable_subject_to_CI"

    return {
      "raw_estimate": raw.point,
      "raw_interval": raw.interval,
      "sensitivity_estimate": sensitivity.point,
      "sensitivity_interval": sensitivity.interval,
      "rt_summary": summarize_rt(responses),
      "false_alarm_rate": qc.fa_rate,
      "quality_flags": qc,
      "status": status
    }
```

Không chọn giữa `raw_estimate` và `sensitivity_estimate` bằng quy tắc tiện tay sau khi thấy kết quả. Version của item bank, pilot rules và scoring policy phải đi cùng output để tái lập.

### 3.4. Nếu dùng Yes/No pseudowords

Với test Yes/No thuần, có thể tính các biến mô tả:

```text
H  = yes trên real words
FA = yes trên pseudowords
pH = H / số real words
pFA = FA / số pseudowords
H_minus_FA = pH - pFA
cfg = (pH - pFA) / (1 - pFA)  # chỉ nếu policy đã pre-register
```

Các biến này cần được báo cùng raw hits. Không dùng `cfg`, `H_minus_FA` hay công thức khác cho MCQ contextualized nếu chưa chứng minh rằng chúng đo cùng response process. Báo false alarm và khoảng bất định; cắt điểm hoặc reject session chỉ sau hold-out validation.

## 4. So sánh với Preply

| Thành phần | Preply theo methodology đã fetch | Đề xuất sau iteration 8 |
|---|---|---|
| Sampling | Khoảng 40 screening + khoảng 120 narrow, midpoint trên frequency rank | Có thể giữ midpoint/headword output để tương thích; ghi rõ sample và seed/version |
| Unit | Dictionary entries/headwords theo mô tả Preply | Giữ unit rõ ràng; không đổi sang lemma/word family ngầm |
| RT | Chưa thấy response-time model/cutoff trong methodology đã fetch | Lưu latency; chỉ dùng làm diagnostic/sensitivity sau pilot |
| Pseudowords | Chưa thấy pseudoword false-alarm control trong methodology đã fetch | Nếu có Yes/No pseudo-items: báo H, FA, rate và response-style flag; không mặc định trừ điểm |
| Ceiling/floor | Methodology đã fetch không nêu low-discrimination gate | Kiểm tra band accuracy/information; cảnh báo ngoài vùng đo được |
| Uncertainty | Vendor calculation khoảng ±10,33% cho estimate của họ | Giữ như claim của Preply; không tái sử dụng cho RT correction hay reliable change |
| Online quality | Chưa có production evidence công khai về timing/attention calibration | Log focus loss, render/network time, latency outlier; validate trên hold-out |
| Status | Một con số midpoint | Estimate + interval + quality/range status + sensitivity output |

## 5. Validation plan

1. **Pilot response-level:** tối thiểu đủ nhiều L1, proficiency, device và browser; lưu presented/rendered/answered timestamps, focus loss, skip, item, band, unit và form.
2. **Criterion check:** dùng interview/meaning check hoặc một vocabulary criterion độc lập trên subsample; với mục tiêu reading, đo accuracy và speed riêng.
3. **RT rule comparison:** so sánh raw, pre-registered RT flags, robust person/item flags và no-filter trên hold-out; báo bias, MAE/RMSE và interval coverage.
4. **Pseudoword study:** randomize vị trí/selection của pseudo-items; kiểm tra false alarm theo L1/proficiency; so sánh raw hits, H–FA và các correction khác mà không giả định một công thức thắng.
5. **Device/network study:** tách thời gian render/network khỏi decision latency; chạy test-retest ngắn với thiết bị khác để tìm artifact.
6. **Range/ceiling gate:** kiểm tra item information và accuracy theo band; nếu score saturation làm giảm phân giải, phát hành range warning hoặc route sang band khác, không tuyên bố growth nhỏ.
7. **Adversarial/unsupervised QA:** kiểm tra tab switching, paste, focus loss và speed-run; không tự động gọi là gian lận nếu chưa có validation, chỉ gắn quality status.
8. **Pre-registration:** khóa thresholds, scoring policy, treatment của invalid events và primary endpoint trước khi nhìn hold-out results.

## 6. Gaps còn lại

- Chưa có response-level/item-bank production của Preply để xác thực RT, focus, pseudoword, item exposure hoặc ceiling controls.
- Chưa có ngưỡng latency theo device/format và chưa có bằng chứng rằng loại RT outlier cải thiện estimate hơn raw scoring.
- Nghiên cứu Tanabe có mẫu nhỏ (`N=24`) và power thấp cho hồi quy; không dùng các hệ số của nghiên cứu làm production calibration.
- Lam là Spanish placement study trong một chương trình cụ thể; 29% false-alarm rate và ceiling pattern không phải ngưỡng English/Preply phổ quát.
- Chưa tìm được nguồn xác thực cho một correction duy nhất phù hợp đồng thời với Preply midpoint MCQ/headword test và pseudoword Yes/No scoring.

## 7. Kết luận iteration

Bằng chứng hiện có ủng hộ việc **lưu và báo RT/false alarms như tín hiệu response-process**, đồng thời dùng ceiling/floor và low-discrimination làm quality/range gates. Bằng chứng không ủng hộ việc tự động đổi RT thành vocabulary units hoặc áp một công thức pseudoword correction phổ quát. Thuật toán triển khai an toàn nên giữ raw estimate làm output chính, kèm sensitivity estimate và flags; chỉ nâng các flags thành scoring rules sau pilot, calibration và hold-out validation theo population mục tiêu.
