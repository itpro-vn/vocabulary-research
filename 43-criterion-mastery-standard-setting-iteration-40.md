# Iteration 40 — criterion-referenced mastery standard setting

## Phạm vi và nguồn đã kiểm tra

Iteration này tách một vấn đề khỏi việc ước lượng tổng số từ: **khi nào một lexical unit được gọi là “known/mastered” cho một mục đích cụ thể?** Nghiên cứu trước đã có các mô hình IRT, partial credit, word-family và band-level scoring; phần này kiểm tra cách đặt ngưỡng có thể kiểm toán thay vì chọn tùy ý `P(known) = 0.50` hoặc `0.67`.

Các URL dưới đây đã được kiểm tra bằng HTTP với browser User-Agent và trả HTTP 200:

1. Katz (ETS, 2019), *Standard Setting Panelist Cognition: A Framework and Implications for Practice*, RM-19-12: <https://www.ets.org/Media/Research/pdf/RM-19-12.pdf>
2. Çetin & Gelbal, *A Comparison of Bookmark and Angoff Standard Setting Methods*: <https://files.eric.ed.gov/fulltext/EJ1027679.pdf>
3. McLean & Stoeckel (2021), *Lexical Mastery Thresholds and Lexical Units: A Reply to Laufer*: <https://files.eric.ed.gov/fulltext/EJ1316857.pdf>

Một PDF Springer được search tìm thấy trả HTTP 200 nhưng nội dung tải về là HTML shell, không phải PDF hợp lệ; không sử dụng nó làm bằng chứng.

## Bằng chứng chính

### 1. Standard setting là một phần của validity argument

Katz định nghĩa standard setting như một hệ thống quy tắc hợp lý để gán số nhằm phân biệt các trạng thái/nấc hiệu năng, và mô tả nó là một phần không thể tách rời của lập luận validity cho việc sử dụng điểm. Quy trình panel điển hình gồm:

- định nghĩa performance-level description (PLD);
- định nghĩa người ở sát ngưỡng, thường gọi là minimally competent, just-qualified hoặc borderline examinee;
- cho panel làm quen với bài, huấn luyện và thực hành phương pháp;
- thu thập phán đoán độc lập vòng đầu;
- thảo luận bằng chứng và có thể xem thêm độ khó/phân bố phân loại;
- thu thập vòng phán đoán tiếp theo;
- tổng hợp hoặc đồng thuận thành cut score được khuyến nghị.

Hệ quả cho vocabulary test: “đã biết từ” không chỉ là một nhãn kỹ thuật suy ra từ item response. Đó là một claim về việc dùng điểm, phụ thuộc lexical unit, population, modality và intended use. Nếu mục đích là hỗ trợ đọc, ngưỡng phải được liên hệ với coverage/hiểu văn bản; nếu mục đích là mô tả receptive breadth, không nên tự động biến nó thành cut score đủ dùng cho nghe, CEFR hoặc placement.

### 2. Angoff và Bookmark tạo ra hai cách nhìn khác nhau về ngưỡng

Nguồn ERIC mô tả Angoff là việc chuyên gia ước lượng xác suất một borderline/minimally competent examinee trả lời đúng **từng item**; tổng các xác suất trung bình tạo nên cut score. Với vocabulary item, panel không nên được hỏi chung chung “từ này khó không?”, mà phải được hỏi theo profile cụ thể: người học vừa đạt chuẩn cho mục đích X có xác suất nhận diện/giải nghĩa đúng item này là bao nhiêu?

Bookmark sắp item từ dễ đến khó theo tham số IRT rồi yêu cầu chuyên gia đặt dấu tại điểm chuyển giữa item mà borderline examinee có thể và không thể trả lời. Trong tài liệu được fetch, response probability (RP) thường được dùng ở 0.50 hoặc 0.67; khoảng 0.50–0.80 cũng xuất hiện trong tài liệu được nghiên cứu. Các RP này là lựa chọn phương pháp của standard-setting study, không phải hằng số tự nhiên của “biết từ”.

Trong 1PL với logistic scale và `P(X=1|theta)=RP`, vị trí Bookmark có thể viết:

```text
theta_bookmark = b + log(RP / (1 - RP))
```

với `b` là item difficulty. Với 2PL/3PL phải giải theo ICC đã fit (bao gồm discrimination và nếu dùng thì lower-asymptote/guessing). Không được dùng công thức 1PL cho item bank đã fit model khác.

### 3. Cut score nhạy với panel, model và RP

Nghiên cứu so sánh được fetch từ ERIC dùng 17 chuyên gia tiếng Anh và bài proficiency 55 item (sau khi loại 5 item). Kết quả được báo cáo như sau:

| Thành phần | Kết quả trong nghiên cứu | Ý nghĩa cho estimator |
|---|---:|---|
| Angoff cut score của từng chuyên gia | 17.55–37.90 | Panel disagreement là một nguồn uncertainty thực, không chỉ là lỗi làm tròn |
| Angoff cut score trung bình | 27.83 | Một con số tổng hợp che khuất phân bố phán đoán |
| Bookmark, 1PL + RP=.50 | 19.242 | Phụ thuộc mô hình và RP |
| Bookmark, 1PL + RP=.67 | 25.247 | Thay RP làm đổi ngưỡng đáng kể |
| Bookmark, 2PL + RP=.50 | 18.897 | Thay model cũng làm đổi ngưỡng |
| Bookmark, 2PL + RP=.67 | 25.102 | Cần sensitivity analysis trước release |
| Tương quan xác suất chuyên gia với item difficulty thực nghiệm | `r = .60` | Phán đoán có signal nhưng không hoàn hảo |

Nguồn cũng ghi nhận Kendall’s W được dùng để kiểm tra mức tương hợp giữa chuyên gia. Vì vậy, production log nên lưu từng judgment, panel round, training version, model version, RP, Kendall’s W hoặc chỉ số agreement tương đương, và phân bố cut score; không chỉ lưu mean.

Đây là bằng chứng phương pháp từ một bài proficiency, không phải calibration vocabulary-size riêng. Không được chuyển trực tiếp các cut score hoặc RP trên thành số từ.

### 4. Với vocabulary, band-level mastery không thể suy ra từ total count

McLean & Stoeckel chỉ ra rằng điểm ở từng word band có ý nghĩa hơn tổng điểm khi diễn giải lexical mastery hoặc ghép người học với tài liệu. Ví dụ, tổng điểm gợi ý người học biết 3.000 trong 5.000 từ đầu không có nghĩa là họ mastery ba band 1.000 từ đầu. Vì vậy, một rule kiểu `estimated_total >= K => mastered first K words` là sai estimand.

Bài viết thảo luận các mức coverage thường được nêu cho các mục đích khác nhau: 95% để hỗ trợ comprehension, 98% cho meaning-focused input và 100% cho fluency development. Tuy nhiên, chính bài viết cũng nói rằng chưa có nghiên cứu nào xác thực các mastery threshold được test creators gợi ý bằng kết quả sử dụng ngôn ngữ ngoài đời. Do đó:

- các mức 95/98/100% chỉ là target/use-case hypotheses trong pipeline này;
- phải đo coverage trên corpus/task mục tiêu, không dùng chúng làm “ngưỡng biết từ” chung;
- phải giữ band-level estimate, confidence interval và coverage criterion tách rời total vocabulary count;
- recognition MCQ có thể overestimate knowledge cần cho reading/listening, nên criterion phải khớp modality.

## Đề xuất cập nhật thuật toán

### Hai lớp điểm

1. **Descriptive breadth layer**: ước lượng `p_known[b]` hoặc `K_hat_b` theo từng frequency/knowledge band, với lexical unit đã khai báo. Đây là lớp chính cho vocabulary-size estimate.
2. **Criterion-referenced mastery layer**: chỉ tạo `mastery_status[b, use_case]` khi có PLD, panel standard setting và criterion validation cho đúng use case. Lớp này không được cộng thêm từ vào `K_hat`.

Nếu band `b` có `N_b` units và item sampling weights `w_i`, có thể báo cáo descriptively:

```text
p_hat_b = sum_i(w_i * P_known_i) / sum_i(w_i)
K_hat_b = N_b * p_hat_b
```

`P_known_i` phải là posterior/IRT probability hoặc calibrated response probability, không mặc định đồng nhất với một câu trả lời đúng. Nếu test là fixed-form Bernoulli và không có model, dùng tỷ lệ có trọng số nhưng phải gắn sampling/measurement interval riêng.

Với một intended use `u`, panel định nghĩa cut trên profile người vừa đạt chuẩn. Angoff tạo:

```text
C_A(u) = sum_i mean_j(p_ji(u))
```

Trong đó `p_ji(u)` là judgment của panelist `j` cho item `i`. Bookmark tạo `theta_cut(u, RP, model)` từ vị trí ordered-item; sau đó link về band-level ability/coverage bằng calibration data. `C_A` hoặc `theta_cut` là threshold của use case, **không phải hệ số quy đổi universal sang word count**.

### Pseudocode

```text
calibrate_mastery_threshold(use_case, item_bank, panelists, response_data, criterion_data):
    freeze lexical_unit, frequency_manifest, modality, population, PLD(use_case)
    fit_and_check IRT(response_data)
    publish item-order and item-fit report

    for panelist in trained_panelists:
        collect Angoff p_ji for every eligible item
    C_A = aggregate_by_item_and_panel(Angoff judgments)
    agreement = compute_panel_agreement(judgments)

    for model in [1PL_or_Rasch, 2PL_if_supported]:
        for RP in [0.50, 0.67, predeclared_alternative_RP]:
            theta_cut[model, RP] = bookmark_from_ICC(item_bank, model, RP)

    panel_uncertainty = bootstrap_or_jackknife_panelists(judgments)
    method_sensitivity = range(theta_cut and linked scores over model, RP)

    if criterion_data exists:
        validate against held_out coverage_or_task criterion:
            classification_error, calibration, subgroup_DIF,
            interval_coverage, decision_consistency
    else:
        mastery_status = "unvalidated"

    return {
        descriptive_band_scores,
        C_A, theta_cut, agreement,
        panel_uncertainty, method_sensitivity,
        mastery_status, validation_record
    }
```

### Quy tắc release bảo thủ

- Không release `mastered = true` chỉ vì `P_known >= .50` hoặc `.67`.
- Không lấy mean panel cut mà bỏ qua range, agreement và model/RP sensitivity.
- Chỉ công bố `mastery_status` khi PLD, panel training, judgments, calibration và held-out criterion đều tồn tại.
- Nếu chưa đủ criterion, trả `mastery_status = unvalidated`, nhưng vẫn trả `K_hat_b`/`p_hat_b` như descriptive estimate kèm interval và caveat.
- Đối với claim “đủ đọc tài liệu band X”, phải kiểm tra lexical coverage và comprehension/task outcome riêng; không suy ra từ tổng vocabulary count.

## Uncertainty và validation plan

Tách ít nhất bốn thành phần:

1. response/model uncertainty của người làm test;
2. item/sampling uncertainty trong band;
3. panel uncertainty của standard setting;
4. criterion/transport uncertainty khi chuyển từ “biết item” sang task coverage hoặc population khác.

Báo cáo nên có `CI_response_or_sampling`, `panel_cut_range`, `method_sensitivity_range` và `criterion_validation_status`. Có thể bootstrap panelists và calibration persons; với adaptive test cần giữ lại routing và re-fit trong mỗi replicate. Tối thiểu cần đánh giá:

- coverage của interval cho `K_hat_b` và band classification;
- sensitivity khi đổi RP, IRT model, panel subset và item order;
- agreement giữa panelists và stability sau training/feedback rounds;
- criterion classification trên hold-out data (meaning-recall, corpus coverage hoặc task comprehension tùy claim);
- DIF theo L1, proficiency, modality và population;
- decision consistency quanh mastery cut;
- alternate-form/common-anchor linking trước khi gộp cut score.

## So sánh với Preply

| Khía cạnh | Preply đã công bố trong methodology proxy | Thiết kế đề xuất |
|---|---|---|
| Output | dictionary-headword vocabulary estimate | tách `K_hat_b` descriptive khỏi `mastery_status` theo use case |
| Sampling | proxy mô tả sampling logarithmic/midpoint và khoảng margin vendor | band/lexical-unit manifest, calibrated weights, item-level uncertainty |
| Mastery threshold | chưa tìm được nguồn xác thực về panel/Angoff/Bookmark hoặc criterion cut của Preply | PLD + trained panel + Angoff và Bookmark sensitivity |
| Ngưỡng RP | chưa xác minh được | predeclare RP/model; không coi .50/.67 là universal |
| Uncertainty | vendor methodology có margin khoảng ±10% nhưng chưa có coverage validation độc lập trong state | tách response, sampling, panel và criterion/transport uncertainty |
| Band interpretation | total estimate không đủ để chứng minh mastery từng band | báo band-level scores và coverage criterion riêng |
| Auditability | chưa có public item-bank/panel artifact | lưu judgments, model, RP, agreement, panel range, criterion evidence |

Direct endpoint `https://preply.com/en/learn/english/test-your-vocab/how-it-works` trả HTTP 403 trong callback; proxy methodology từng trả HTTP 200 nhưng là nguồn vendor, không thay thế independent calibration. Chưa tìm được nguồn xác thực cho Preply standard-setting protocol hoặc mastery threshold.

## Kết luận iteration

Standard setting giúp biến “known/mastered” thành một claim có intended use và evidence chain, nhưng nó không tự giải quyết estimand vocabulary size. Tích hợp an toàn nhất là giữ count/band estimate làm output mô tả, còn mastery là lớp criterion-referenced riêng, có panel/model/RP sensitivity và chỉ được xác nhận sau hold-out validation. Kết quả iteration này được append vào `state/findings.jsonl` với 6 record mới.
