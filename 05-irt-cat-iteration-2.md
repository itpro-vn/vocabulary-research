# 5. Iteration 2 — IRT/CAT, calibration và repeat-form equating

## Phạm vi direction

Iteration này kiểm tra một hướng khác iteration 1: dùng Item Response Theory (IRT), Computerized Adaptive Testing (CAT), chỉ số độ tin cậy/độ không chắc chắn, kiểm soát guessing và Rasch equating. Mục tiêu là xác định điều kiện để bài test ngắn vẫn có thể báo một estimate có calibration, thay vì chỉ mở rộng raw score theo một hệ số.

## Nguồn đã verify

1. Fokin, Płużyczka & Golovin, *The Polish Vocabulary Size Test: A Novel Adaptive Test for Receptive Vocabulary Assessment*, arXiv PDF, HTTP 200 khi fetch trực tiếp: <https://arxiv.org/pdf/2507.19869>.
2. Akase (2022), *Longitudinal measurement of growth in vocabulary size using Rasch-based test equating*, PDF tại Deutsche Nationalbibliothek, HTTP 200 khi fetch trực tiếp: <https://d-nb.info/1257528165/34>.

Các con số dưới đây là mô tả từ hai tài liệu này; không được diễn giải thành kết quả đã được validation cho English hoặc cho item bank của Preply.

## Bằng chứng từ PVST

### CAT chọn item theo ability

PVST mô tả quy trình IRT/CAT: trình bày stimulus, ước lượng ability hiện tại và uncertainty, rồi chọn stimulus tiếp theo có difficulty gần ability đó. Ý tưởng là item quá dễ với người giỏi hoặc quá khó với người mới cung cấp ít thông tin; matching difficulty giúp tăng information/item. Sau bốn pilot, tác giả dùng 30 stimuli và báo thời lượng khoảng 2 phút. Đây là tham số pilot của bài tiếng Ba Lan, không phải stopping rule đã được chứng minh cho mọi ngôn ngữ.

### Ability logit và logit-to-words

PVST ước lượng ability trên thang logit. Để hiển thị cho người dùng, tác giả fit hàm:

```text
y = a / (1 + exp(-b * (x - c)))
```

Trong đó `x` là ability logit, `y` là vocabulary size hiển thị, `a`, `b`, `c` là hệ số calibration. Hệ số được fit giữa stimulus rank theo tần suất và stimulus difficulty ước lượng từ response data. Trực giác là khi difficulty item bằng ability người làm, xác suất biết item khoảng 50%; rank của item đó chia universe thành phần tương đối biết và không biết, nên có thể dùng làm estimate số từ.

Hệ quả thiết kế: `a` là cận trên của universe, còn `b/c` phụ thuộc item bank, corpus/rank và population. Thay đổi từ dictionary headwords sang lemmas hoặc word families làm thay đổi estimand; không được áp một conversion factor cố định giữa Preply và VST.

### Guessing và quality signal

PVST phối hợp:

- **Binary real-word**: nhanh, dễ mở rộng nhưng chịu overconfidence, self-report bias và false alarm.
- **Multiple-choice**: người làm chọn synonym/definition trong bốn lựa chọn; distractors cùng part of speech giúp giảm đoán nhưng tăng cognitive load và thời gian.
- **Pseudoword**: cung cấp tín hiệu kiểm soát chú ý và xu hướng đánh dấu bừa là “biết”.

Thiết kế PVST dùng tỷ lệ 60% binary, 20% multiple-choice và 20% pseudowords; chính bài báo nói chưa có đồng thuận về tỷ lệ tối ưu. Vì vậy hệ thống mới nên xem tỷ lệ này là starting point để pilot, không phải chuẩn bắt buộc.

PVST tính:

```text
attention_index = (x + y) / (ax + ay)
```

`x` = pseudowords được đánh dấu “không biết”; `ax` = tổng pseudowords; `y` = multiple-choice definitions đúng; `ay` = tổng multiple-choice questions. Tác giả không dùng index để penalty điểm vocab cá nhân; kết quả dưới 70% bị xem là không trustworthy và bị loại khỏi hiệu chỉnh item/aggregate. Pattern phù hợp để áp dụng là quality gate/cờ cảnh báo tách biệt với điểm, trừ khi có calibration thực nghiệm chứng minh penalty là hợp lệ.

### Item fit và targeting

Pilot PVST dùng 1.056 observations trên 252 stimuli. Báo cáo Rasch summary có reliability of separation `.96` cho items và `.95` cho persons. Sau phân tích, tác giả loại items có infit/outfit vượt `1.3` cùng z-score `>2.0`, còn 195 words, chưa tính 38 pseudowords. Item pool vẫn lệch về item dễ và có thể kém phân biệt người dùng vocabulary cao. Kết luận triển khai: phải kiểm tra item-fit, Wright map/targeting, coverage của vùng advanced và DIF; không đủ chỉ sắp xếp item theo frequency.

## Bằng chứng từ Akase: equating và frequency không hoàn toàn là difficulty

Akase nghiên cứu đo tăng trưởng qua nhiều lần làm VST. Nếu dùng các form khác nhau mà chưa equate, điểm tăng có thể do learner growth, practice effect hoặc form khó/dễ khác nhau. Nghiên cứu nối bốn form bằng common/linking items trên cùng Rasch logit scale; ba form gốc fit Rasch tốt và chênh lệch difficulty nhỏ.

Bài cũng ghi nhận overlap đáng kể giữa difficulty item của các frequency bands. Vì vậy frequency là proxy hữu ích để xây universe và khởi tạo bank, nhưng không nên dùng như difficulty parameter duy nhất sau khi đã có response data.

## Đề xuất tích hợp vào thuật toán

### Trước calibration

Dùng fixed stratified random estimator đã mô tả ở file 03. Không tự gọi một bài test ngắn là IRT/CAT nếu chưa có item parameters từ pilot.

### Sau calibration

```text
function cat_vocab(session, bank, universe, max_items, target_se):
    require session.universe_version == universe.version
    responses = administer_fixed_anchors(session, bank)
    theta = provisional_ability(responses, prior=population_prior)

    while len(responses) < max_items:
        candidates = eligible_items(
            bank,
            exclude=responses.item_ids,
            exposure_control=true,
            content_balance=true,
            dif_safe=true
        )
        item = argmax_expected_information(candidates, theta)
        responses.append(administer(item))
        theta, se_theta = estimate_ability_and_se(
            responses, model="Rasch_or_2PL"
        )
        if se_theta <= target_se and anchors_consistent(responses):
            break

    vocab_hat = logistic_calibration(theta, universe.version)
    ci_theta = theta +/- 1.96 * se_theta
    ci_vocab = transform_monotone(ci_theta, logistic_calibration)
    return vocab_hat, ci_vocab, diagnostics(responses)
```

Với Rasch, xác suất đúng có dạng:

```text
P(X=1 | theta, delta) = exp(theta - delta) / (1 + exp(theta - delta))
```

`argmax_expected_information` chỉ hợp lệ khi `delta` (và discrimination nếu dùng 2PL) đã được ước lượng, item-fit kiểm tra và item bank đủ coverage. `max_items` vẫn cần để giới hạn thời lượng; dừng chính nên dựa trên `SE_theta` hoặc độ rộng CI sau transform, không chỉ số lượng câu.

### Uncertainty phải truyền qua calibration

Nếu `V=g(theta)` là hàm logistic calibration đơn điệu, xấp xỉ delta-method:

```text
SE_V ≈ abs(g'(theta)) * SE_theta
```

Nhưng `SE_theta` không bao gồm uncertainty do ước lượng `a,b,c`, thay đổi dictionary/corpus, model Rasch/2PL, guessing, DIF hay construct receptive-vs-productive. Sản phẩm nên báo riêng:

1. `CI_response_or_sampling`;
2. `CI_model`;
3. `sensitivity_range` khi đổi universe, lemma/headword/word-family và exclusion rules.

Dùng bootstrap hoặc posterior draws để kiểm tra khoảng đã transform, thay vì chỉ báo `theta ± 1.96 SE` rồi coi đó là CI số từ chính xác.

## Validation gates cho triển khai

1. Fit item parameters trên calibration sample và đánh giá prediction/CI coverage trên hold-out sample.
2. Kiểm tra Wright map/targeting; bổ sung item nếu advanced region thiếu coverage.
3. Kiểm tra infit/outfit, local dependence, unidimensionality và DIF theo L1/proficiency. Ngưỡng PVST `1.3` và `z>2` chỉ là tham chiếu pilot.
4. Mô phỏng nhiều mức theta và pattern response để chọn `target_se`, `max_items`, quota anchors và exposure control; report bias, MAE/RMSE và coverage 80%/95%.
5. Dùng parallel forms với common anchors; test-retest sau 1–2 tuần để tách learning/practice effect.
6. Đối chiếu với large-form test, receptive interview/known-word audit và reading criterion phù hợp; không coi một nguồn criterion duy nhất là gold tuyệt đối.

## Gap còn mở

- Chưa có response-level data và item bank production của Preply để fit/kiểm tra IRT, DIF, information curve hoặc coverage.
- Chưa có pilot cho English target population để chọn tỷ lệ binary/MC/pseudoword và target `SE`.
- Chưa có bằng chứng cho phép chuyển trực tiếp Preply headword estimate sang VST word-family estimate.
- Claims về 30 stimuli/2 phút và ngưỡng attention 70% của PVST là bằng chứng thiết kế/pilot của bài khác, không nên quảng bá như bảo đảm accuracy cho hệ thống mới.
