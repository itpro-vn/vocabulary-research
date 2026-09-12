# Iteration 24 — Tail coverage, censoring và thiết kế điểm cực trị

## 1. Câu hỏi nghiên cứu

Một bài vocabulary-size test có thể ước lượng sai hoặc tạo cảm giác chính xác giả khi người làm bài ở gần sàn hoặc trần của item bank. Iteration này kiểm tra bằng chứng về:

- việc xác định tail bằng frequency bands thay vì lấy mẫu dictionary;
- routing/adaptive probing khi độ chính xác bắt đầu giảm;
- thiết kế item cho người học nâng cao và cách mở rộng vùng đo khi có ceiling effect;
- cách diễn giải điểm ở đầu mút, bao gồm censoring, khoảng ước lượng và giới hạn của việc quy đổi sang proficiency/CEFR.

Đây là hướng bổ sung cho các iteration trước về frequency sampling, IRT/CAT, validity và use-case coverage. Trọng tâm ở đây là **endpoint behavior**: điểm rất thấp hoặc rất cao không nên được xử lý như một điểm ở giữa thang đo có cùng lượng thông tin.

## 2. Nguồn đã fetch và verify

| Nguồn | HTTP | Bằng chứng được sử dụng |
|---|---:|---|
| Alexiou (2021), *Vocabulary size and vocabulary development in young learners* | 200 | Dictionary sampling có thể over-sample từ thường gặp; frequency-based sampling; báo cáo ceiling ở phiên bản 5.000 từ và thêm phiên bản 10.000 từ để mở rộng vùng phân biệt. [PDF](https://rpltl.eap.gr/images/2021/11-01-066-Alexiou.pdf) |
| Izura et al., *Lextale-Esp* — bản toàn văn lưu tại Internet Archive | 200 | Mô tả EVST: đi từ band dễ đến khó, dừng khi accuracy dưới criterion, lấy rough range từ hai band cuối rồi probe chi tiết tại band bắt đầu giảm; nonwords dùng để chỉnh response bias. [Text](https://archive.org/stream/ERIC_EJ1021970/ERIC_EJ1021970_djvu.txt) |
| Lemhöfer & Broersma (2012), *Introducing LexTALE* | 200 | Thiết kế item tail cho advanced learners: 60 item từ pool 240 item, pilot difficulty categories, item-whole discrimination, word frequency 1–26 occurrences/million; cảnh báo các score-to-proficiency range chỉ là rough estimates của nhóm Dutch. [PDF](https://www.lextale.com/pdf/Lemhofer_Broersma_2012.pdf) |

Các URL trên đều được kiểm tra trực tiếp bằng `curl -L` với browser User-Agent và trả HTTP 200. Nội dung nghiên cứu được lấy từ text layer của PDF hoặc bản text được fetch trực tiếp; search snippets chỉ dùng để tìm đường dẫn.

## 3. Findings chi tiết

### 3.1. Không lấy mẫu theo trang dictionary để suy ra tail

Alexiou tổng hợp vấn đề của các ước lượng cũ dựa trên dictionary. Từ thường gặp trong tiếng Anh thường đa nghĩa và có nhiều entry, nên việc lấy ví dụ như một từ trên mỗi số trang sẽ làm chúng xuất hiện quá nhiều trong mẫu. Khi các từ thường gặp bị over-sample, tỷ lệ biết từ bị đẩy lên và vocabulary-size estimate bị phóng đại.

Cách thay thế được mô tả là lấy mẫu có nguyên tắc theo frequency. Bài viết dẫn nghiên cứu dùng các band frequency của danh sách Thorndike & Lorge và cho biết kiến thức từ vựng tập trung gần như toàn bộ trong các band thường gặp nhất; việc mở rộng vượt vùng đó không đóng góp đáng kể vào estimate trong bối cảnh được thảo luận. Hệ quả không phải là đặt một cutoff 25.000 cho mọi sản phẩm, mà là:

1. item universe phải có `corpus_version`, frequency definition và lexical-unit policy rõ ràng;
2. inclusion probability phải được biết nếu mỗi band có số item khác nhau;
3. tail phải được kiểm tra bằng calibration data, không được tạo ra chỉ vì dictionary lớn hơn;
4. nếu muốn tuyên bố đo ở mức cao hơn vùng calibration, phải có item và criterion evidence cho vùng đó.

### 3.2. EVST cung cấp mẫu thiết kế hai giai đoạn cho điểm ở tail

Mô tả EVST trong nguồn Izura et al. cho thấy một cơ chế tail-aware cụ thể:

- bắt đầu bằng band dễ nhất;
- tại mỗi band đưa ra 10 real words và 5 invented nonwords;
- tiếp tục sang band kế tiếp khi performance đủ cao;
- khi accuracy rơi dưới criterion đã đặt trước, tính rough score dựa trên accuracy ở hai band gần nhất;
- sau đó đổi sang đánh giá chi tiết hơn trong band nơi accuracy bắt đầu giảm.

Ví dụ được mô tả: nếu accuracy là 100% đến band 5 rồi giảm mạnh, test chỉ nên kết luận thô rằng người làm bài nằm trong khoảng 5.000–6.000 từ trước khi probe sâu hơn, thay vì coi toàn bộ điểm 100% ở band đầu là bằng chứng cho một count chính xác.

Mô tả này cũng cho biết EVST điều chỉnh overestimation bằng số nonword bị chọn là word, theo signal-detection logic. Đây là bằng chứng cho việc tách hai đại lượng:

- **breadth evidence:** real-word recognition theo band;
- **response-style/false-alarm evidence:** xu hướng nhận nhầm nonword.

Không nên trừ một guessing constant tùy ý khỏi mọi test. Nếu dùng nonword, hệ số phải được ước lượng từ calibration sample và kiểm tra theo proficiency/L1; nếu không, nonword chỉ nên là quality flag chứ không tự động biến thành số từ bị trừ.

### 3.3. Tail cho advanced learners cần item calibration, không chỉ frequency rank

Lemhöfer & Broersma mô tả LexTALE, một test nhắm tới medium–high proficiency. LexTALE có 60 item, gồm 40 words và 20 nonwords, lấy từ pool 240 item của một test “10K”. Việc chọn 60 item được thực hiện sau pilot 18 người:

1. words và nonwords được chia thành bốn nhóm difficulty theo tỷ lệ trả lời đúng;
2. tính item-whole correlation như chỉ báo item discrimination;
3. trong mỗi nhóm difficulty, chọn phần tư item có item-whole correlation cao nhất.

40 real words có frequency trong CELEX từ 1 đến 26 occurrences per million, mean 6.4. Những chi tiết này cho thấy item tail phải vừa đủ khó để tạo variance, vừa có discrimination đã được kiểm chứng. Một danh sách “toàn từ hiếm” sẽ không tự động là một tail tốt: có thể tạo floor cho người học thấp, nhiễu do spelling/loanword, hoặc item không phân biệt được người có năng lực cao với người chỉ nhận biết một số từ hiếm.

Nguồn này cũng báo cáo LexTALE được xác nhận với hai nhóm người nói L2 khác nhau, và score distributions được trình bày riêng. Khi tác giả nối LexTALE với các mức proficiency, họ chỉ dùng hồi quy của nhóm Dutch và gọi các khoảng đó là **rough estimates based on limited data**. Vì vậy score-to-proficiency mapping không được coi là thuộc tính phổ quát của item bank.

### 3.4. Ceiling là tín hiệu cần mở rộng thang đo

Alexiou báo cáo phiên bản Pic-Lex 5.000 từ có ceiling effect. Để kéo dài vùng phân biệt ở người học lớn tuổi/có trình độ cao hơn, một phiên bản 10.000 từ được thêm vào. Logic thiết kế là hợp lý cho thuật toán tổng quát:

- nếu nhiều người đạt sát maximum và response pattern cho thấy item không còn phân biệt, test đang bị censor ở phía trên;
- không gán cùng một vocabulary count cho mọi người đạt maximum;
- thêm module khó hơn đã được calibrated, hoặc route sang adaptive tail;
- chỉ nối điểm hai module sau khi có common items/equating và calibration sample.

Đây là bằng chứng từ một assessment cho young learners, nên không thể chuyển nguyên xi các ngưỡng 5K/10K sang test người lớn. Giá trị có thể tái sử dụng là **nguyên tắc xử lý ceiling**, không phải con số cutoff.

## 4. Quy tắc thuật toán cập nhật

### 4.1. Trạng thái phải phân biệt point estimate và censoring

Mỗi phiên test nên lưu thêm:

```text
estimate              # median/point estimate trên universe đã định nghĩa
interval              # CI hoặc calibrated posterior interval
endpoint_status       # none | left_censored | right_censored | both_or_unresolved
transition_band       # band nơi accuracy/information bắt đầu giảm
tail_module_used      # false | true
tail_information      # information/SE tại vùng cuối
false_alarm_rate      # nếu có nonword controls
calibration_population
calibration_version
```

`right_censored` nghĩa là item bank không cung cấp đủ bằng chứng để phân biệt các người đạt gần trần; đây không phải là estimate chính xác bằng maximum. Tương tự, `left_censored` áp dụng khi test quá khó và không đủ item dễ để phân biệt vùng sàn.

### 4.2. Pseudocode cho frequency routing và tail expansion

```text
function estimate_vocab(response_log, item_bank, calibration):
    validate item_bank.corpus_version, lexical_unit, band_manifest
    start_band = calibration.lowest_valid_band
    band_results = []

    for band in bands_from(start_band):
        sample = draw_items(band, exposure_cap, independence_rules)
        answers = administer(sample)
        p_hat = weighted_accuracy(answers, inclusion_probabilities)
        se_band = binomial_or_irt_se(answers, calibration, band)
        band_results.append({band, p_hat, se_band})

        if p_hat < calibration.transition_criterion:
            transition = band
            break

        if information_remaining(band_results) < target_total_se:
            transition = band
            break

    if no transition found:
        # all observed bands are too easy; the upper tail is not identified
        if has_calibrated_tail_module(item_bank):
            append tail_module items with common anchors
            tail_result = administer_and_score_tail()
            equate_with_common_anchors(band_results, tail_result)
            endpoint_status = none if tail_result.informative else right_censored
        else:
            endpoint_status = right_censored
    else:
        # local refinement around the first decline
        refine = draw_more_items(transition, adjacent_bands,
                                 until_local_se <= local_se_target)
        band_results.extend(refine)
        endpoint_status = none

    if no transition found at low end and low-band accuracy is below
       the minimum-valid threshold:
        endpoint_status = left_censored

    estimate = integrate_band_or_irt_posterior(band_results)
    interval = propagate_item_sampling_person_score_and_equating_error()

    if nonwords_available:
        false_alarm_rate = score_nonword_false_alarms()
        return estimate, interval, endpoint_status, false_alarm_rate
    return estimate, interval, endpoint_status
```

Điểm quan trọng là **transition search** và **tail module** không được nhầm với việc làm cho test “khó hơn” bằng cách thêm item ngẫu nhiên. Item ở tail phải có frequency provenance, difficulty/discrimination calibration, exposure control và anchor/equating metadata.

### 4.3. Công thức rough band estimate và interval

Với band `b` có quy mô universe `N_b`, `n_b` item hợp lệ, `x_b` câu đúng và inclusion probability `π_ib`, một estimator design-based cơ bản là:

```text
p_hat_b = sum_i (y_ib / pi_ib) / sum_i (1 / pi_ib)
hat_K_b = N_b * p_hat_b
```

Nếu sampling đơn giản trong band và các item gần độc lập, có thể dùng:

```text
SE(p_hat_b) ≈ sqrt(p_hat_b * (1 - p_hat_b) / n_b)
SE(K_b)   ≈ N_b * SE(p_hat_b)
```

Công thức này chỉ là xấp xỉ. Production estimate phải thêm design effect/local dependence, item-model uncertainty, response-style uncertainty và equating error. Tổng count không nên là `sum(hat_K_b)` nếu các band overlap hoặc model đã gắn chung latent trait; khi dùng IRT/hierarchical model phải propagate posterior/predictive draws thay vì cộng các SE độc lập.

Nếu tất cả item trong band cuối đều đúng, `p_hat_b=1` không chứng minh `p_b=1`. Có thể báo one-sided bound hoặc right-censored status. Nếu đã xác định tail module bằng common anchors, report nên ghi rõ interval sau equating; nếu chưa, chỉ được nói “ít nhất trong vùng được test” hoặc “trên trần quan sát”, không báo một count có độ chính xác như vùng giữa.

### 4.4. Quy tắc dừng

Một phiên có thể dừng khi một trong các điều kiện sau được thỏa mãn:

1. khoảng ước lượng sau khi cộng tất cả nguồn uncertainty đạt `target_total_se` và không có endpoint flag;
2. transition band đã xác định, local refinement đạt `target_local_se`, và tail không bị censor;
3. quota thời gian/item đạt giới hạn nhưng phải trả `endpoint_status` và interval tương ứng;
4. có ceiling/floor: chỉ dừng sau khi route tail module thất bại hoặc module cho thấy không đủ information, khi đó trạng thái phải là censored chứ không phải “complete precise estimate”.

## 5. Đối chiếu với cách làm Preply

Những iteration trước đã ghi nhận methodology công khai của Preply mô tả một bài test ngắn với score estimate và vendor-stated margin; tuy nhiên item bank, frequency universe, routing probabilities, item parameters và response-level calibration của Preply chưa được công khai/kiểm chứng độc lập trong iteration này. Endpoint behavior riêng của Preply vì vậy vẫn là gap.

| Khía cạnh | Thiết kế được kiểm chứng ở nguồn nghiên cứu | Preply: trạng thái kiểm chứng |
|---|---|---|
| Xác định tail | EVST đi từ band dễ, dừng khi accuracy giảm, rồi probe chi tiết tại band chuyển tiếp | Chưa có item/routing log để kiểm tra Preply có làm vậy hay không |
| Advanced coverage | LexTALE dùng pilot difficulty + item-whole discrimination và item hiếm đã calibrated | Chưa xác minh được item selection, band coverage hoặc discrimination |
| Ceiling handling | Pic-Lex thêm phiên bản 10K sau khi thấy ceiling ở 5K | Chưa xác minh được Preply có module trên trần hay gắn maximum thành count |
| False alarms | EVST/LexTALE có nonwords và score/quality adjustment | Chưa xác minh được Preply có pseudoword controls hay guessing model nào |
| Interval ở endpoint | Nghiên cứu khuyến nghị rough range/censored interpretation khi tail thiếu thông tin | Chưa có response data để kiểm tra margin theo score range; không được tự gán ±margin đồng đều |
| Proficiency mapping | LexTALE gọi mapping là rough, dựa trên nhóm Dutch và limited data | Chưa tìm được nguồn xác thực cho mapping Preply → CEFR/proficiency ở endpoint |

Vì vậy implementation không nên mô phỏng một `max_score -> max_vocab` conversion nếu không có bằng chứng. Nếu muốn so sánh với Preply, cần một common-person calibration study, trong đó cùng người làm cả hai test, lưu endpoint status và dùng một criterion độc lập.

## 6. Assumptions và giới hạn

- Frequency band là proxy cho item difficulty; không được coi là difficulty tuyệt đối.
- Các item trong cùng band phải được kiểm tra local dependence; công thức binomial đơn giản có thể đánh giá thấp SE.
- Nonword false-alarm rate chỉ hiệu chỉnh được nếu nonwords có độ khó/orthographic legality được calibration.
- Ngưỡng transition criterion phải được chọn trên pilot và kiểm tra sensitivity; không copy ngưỡng EVST sang sản phẩm khác.
- Tail module phải cùng estimand (headword/lemma/word family) với core module hoặc có bridge/equating đã kiểm định.
- Bằng chứng Pic-Lex áp dụng cho young learners; chỉ nguyên tắc ceiling expansion được chuyển sang thiết kế tổng quát.
- Các khoảng score-to-proficiency trong LexTALE không phải conversion phổ quát; phải báo population, L1, sample size và linking error.

## 7. Validation plan

1. **Pilot endpoint oversampling:** tuyển người ở vùng thấp, giữa và cao; cố ý lấy đủ người có dự kiến gần sàn/trần để ước lượng censoring rate.
2. **Item calibration:** chạy core và tail pool lớn hơn production form; ước lượng item difficulty/discrimination, item-whole correlation, false-alarm behavior và DIF theo L1.
3. **Routing simulation:** replay response logs qua fixed-form, band-routing và IRT/CAT; so sánh bias, RMSE, test length và coverage của interval.
4. **Common-anchor equating:** mọi tail module phải có anchors xuất hiện ở core module trong calibration sample; báo linking error và kiểm tra alternate forms.
5. **Endpoint reliability:** báo riêng accuracy/SE ở mỗi band; kiểm tra nếu tất cả item cuối đúng hoặc sai thì one-sided interval/censoring flag có được tạo đúng.
6. **External criterion:** dùng independent receptive vocabulary criterion và task reading/listening; không dùng CEFR label như ground truth duy nhất.
7. **Population transport:** lặp validation theo L1, age, education và exposure profile; không áp dụng mapping của một nhóm Dutch/Korean cho mọi user.
8. **Regression tests:** khi corpus, lexical-unit manifest, tail pool hoặc calibration version đổi, chạy lại item selection, anchor linking và endpoint classification.

## 8. Gaps còn lại

- Chưa có item bank và response-level data của Preply để kiểm tra ceiling/floor, tail routing, endpoint bias hoặc vendor margin theo score range.
- Chưa có threshold EVST-like được calibration cho mục tiêu của bài test này; nguồn nghiên cứu chỉ chứng minh dạng thiết kế, không cung cấp production cutoff dùng trực tiếp.
- Chưa có common-anchor data để equate một tail module giả định với scale Preply/headword hiện tại.
- Chưa có validation sample đủ rộng để ước lượng endpoint interval coverage, DIF, nonword false-alarm model và transportability.
- Chưa tìm được nguồn xác thực cho một công thức phổ quát đổi điểm tối đa của bất kỳ vocabulary-size test nào thành một vocabulary count không bị censor.

## 9. Kết luận iteration

Bằng chứng mới ủng hộ một quy tắc bảo thủ: tìm band chuyển tiếp trước, probe dày hơn quanh transition, và coi điểm sát sàn/trần là censored cho đến khi có module tail được calibration/equate. Frequency rank giúp định vị vùng đo nhưng không thay thế pilot item calibration. Ceiling effect phải kích hoạt mở rộng thang đo hoặc cảnh báo interval, không được âm thầm chuyển thành một điểm count chính xác. Preply comparison hiện chỉ có thể ghi nhận gap về item/routing/endpoint data, chưa thể khẳng định sản phẩm có hay không có các cơ chế này.
