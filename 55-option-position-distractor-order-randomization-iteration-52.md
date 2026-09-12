# Iteration 52 — Option-position, distractor-order và randomization trong VST online

## Phạm vi

Iteration này kiểm tra một nguồn biến thiên mới cho bài vocabulary-size test dạng multiple-choice: vị trí hiển thị của đáp án đúng, thứ tự tương đối của distractor và khả năng tái lập phép randomization. Mục tiêu không phải trừ điểm người làm bài theo vị trí, mà là ngăn một đặc tính giao diện bị lẫn vào item difficulty hoặc vào ước lượng `K_hat`.

Direction này bổ sung cho các iteration về distractor functioning và response format: nó tách riêng **absolute position** của key khỏi **relative order/plausibility** của distractor. Bằng chứng chính không phải nghiên cứu riêng cho Preply; các kết luận chuyển sang VST vocabulary phải ghi rõ mức độ suy luận và được pilot kiểm tra.

## Nguồn đã fetch và verify

Tất cả URL trong bảng dưới đây trả HTTP 200 khi re-check bằng `curl -L` với browser User-Agent trong callback.

| Nguồn | HTTP | Vai trò và giới hạn |
|---|---:|---|
| [Hohensinn & Baghaei, *Does the position of response options in multiple-choice tests matter?* — Internet Archive full text](https://archive.org/stream/ERIC_EJ1125979/ERIC_EJ1125979_djvu.txt) | 200 | Nghiên cứu LLTM trên bài thi tiếng Anh bốn lựa chọn; nguồn toàn văn lưu trữ, không phải dữ liệu vocabulary-size riêng. |
| [Lions et al. (2021), *The Position of the Distractors in Multiple-Choice Test Items* — Frontiers in Education](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2021.731763/full) | 200 | Phân tích lớn về phân bố distractor trong bài thi quốc gia; chủ yếu năm lựa chọn, cần thận trọng khi chuyển sang bốn lựa chọn. |
| [Holzknecht et al. (2021), *The Effect of Response Order on Candidate Viewing Behaviour and Item Difficulty* — paper page](https://www.bergesinstitutespanish.com/papers/107) | 200 | Trang lưu trữ tóm tắt nghiên cứu Aptis MC listening; 30 người eye-tracking và khoảng 6.000 người/item. Không phải receptive written vocabulary. |
| [Qualtrics, Choice Randomization](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/choice-randomization/) | 200 | Tài liệu vận hành mô tả random subset/fixed choice và export viewing order; không phải bằng chứng validity học thuật. |

Trang Preply được cung cấp trong task không được dùng như nguồn fact mới ở iteration này: các callback trước ghi nhận endpoint trả 403. Vì vậy chưa có nguồn xác thực cho current Preply option order, randomization seed, distractor manifest hay position calibration.

## Findings đã xác minh

### 1. Hiệu ứng key-position nhỏ nhưng không được mặc định là bằng không trong bài bốn lựa chọn

Hohensinn và Baghaei phân tích response của 21.642 thí sinh trong kỳ thi tuyển sinh tiếng Anh ở Iran. Bốn booklet chỉ khác vị trí response options và được phân ngẫu nhiên. Mô hình LLTM so sánh difficulty của item stem với difficulty của các position parameter.

Kết quả được báo cáo trong toàn văn:

- position parameters rất nhỏ;
- key ở vị trí về cuối có xu hướng làm item khó hơn một chút;
- hiệu ứng không đáng kể trong định dạng bốn lựa chọn;
- random hóa vị trí key là thực hành hợp lệ cho bài tối đa bốn lựa chọn, miễn là ngăn pattern guessing;
- tác giả không coi kết quả này là giấy phép suy rộng cho số option lớn hơn.

Hàm ý cho VST: không cần áp dụng một correction điểm cố định chỉ vì key nằm ở A/B/C/D. Cần dùng randomization và kiểm tra thực nghiệm. Nếu pilot cho thấy `position_effect` khác 0, có thể thêm covariate position vào calibration model, nhưng không điều chỉnh điểm production trước khi có common-person/common-item và hold-out evidence.

### 2. Balanced answer-key pattern có thể bị khai thác

Toàn văn Hohensinn và Baghaei thảo luận bằng chứng trước đó về middle/edge bias và cảnh báo rằng thí sinh test-wise có thể tận dụng kiến thức rằng answer key được cân bằng đều giữa các vị trí. Do đó, “mỗi vị trí xuất hiện đúng quota” và “random không biết trước” là hai thuộc tính khác nhau.

Production rule nên:

1. sinh permutation bằng PRNG có seed hoặc permutation ID được lưu server-side;
2. tránh một pattern deterministic lặp lại giữa các form;
3. không công bố quy tắc phân bố key theo từng block;
4. vẫn kiểm tra tổng thể để tránh lệch cực đoan do RNG;
5. không dùng pattern của answer key như dữ liệu scoring hay như một penalty cho thí sinh.

Đây là biện pháp giảm test-wiseness và bảo vệ calibration, không phải guessing correction.

### 3. Distractor có thể tạo position signal riêng với key

Lions và cộng sự phân tích dữ liệu 8.800 item năm lựa chọn trong 110 bài thi quốc gia Chile, thu thập qua năm năm, với tổng 318.859.763 lượt trả lời. Distractor mạnh nhất thường xuất hiện ở các vị trí giữa, đặc biệt option C; distractor yếu nhất thường xuất hiện ở option cuối E. Mẫu hình không thay đổi đáng kể theo môn hoặc năm.

Kết luận quan trọng là middle bias trong response không nhất thiết chỉ do vị trí đáp án đúng. Nó có thể phản ánh việc distractor mạnh/yếu được đặt theo thứ tự plausibility. Vì vậy, chỉ thay key position mà giữ hoặc thay đổi relative distractor order không kiểm soát sẽ làm lẫn hai hiệu ứng.

Hàm ý cho item bank:

- lưu `distractor_plausibility_rank` nếu có expert label hoặc pretest estimate;
- lưu `display_position` cho mọi option;
- kiểm tra phân bố key position và distractor rank × position theo band, form và L1;
- khi nghiên cứu position effect, phân biệt ít nhất hai phép thử: cyclic shift giữ relative order và full shuffle;
- full shuffle chỉ được dùng nếu sau hoán vị stem vẫn đúng ngữ pháp, thứ tự logic, đơn vị đo và nghĩa.

### 4. Bằng chứng trong language testing cho thấy modality có thể làm hiệu ứng lớn hơn

Trang lưu trữ nghiên cứu Holzknecht và cộng sự (Language Testing, 2021) mô tả hai study trên Aptis MC listening bốn lựa chọn: Study 1 dùng eye-tracking với 30 thí sinh; Study 2 dùng 200 live items và khoảng 6.000 thí sinh/item. Tóm tắt báo cáo vị trí không gian của key ảnh hưởng lượng processing mà option nhận được và item difficulty; thí sinh tình cờ gặp nhiều key ở vị trí cuối có thể bất lợi.

Đây là evidence cho listening assessment, không thể chuyển trực tiếp thành hệ số cho receptive written vocabulary. Nhưng nó làm rõ một release gate: position invariance phải được kiểm tra trên đúng modality, stem length, thiết bị và response mode của sản phẩm. Không dùng kết quả “hiệu ứng nhỏ” từ một bài EFL khác để hợp thức hóa mọi form online.

### 5. Randomization phải có audit trail

Tài liệu chính thức Qualtrics mô tả bốn cơ chế có ý nghĩa khác nhau: randomize choices, random subset, randomly reverse và fixed-position choices. Nó cũng mô tả việc xuất randomized viewing order.

Đối với VST, cần lưu tối thiểu:

```text
response_id
form_version
item_id
permutation_id hoặc random_seed
option_content_ids theo display order
correct_display_position
```

Nếu chỉ lưu `selected_option = C` mà không lưu display order, response không đủ để phân tích position effect, tái lập item difficulty hoặc phát hiện một generator đã làm lệch key. `display_order` là metadata kiểm toán; không được dùng trực tiếp để tăng/giảm `K_hat`.

## Thuật toán đề xuất có bổ sung position layer

### Item-bank manifest

Mỗi item trong production bank nên có:

```text
item_id
lexical_unit_id
frequency_band
construct = receptive_written_breadth
stem_version
option_content_ids[4]
correct_content_id
option_position_policy
plausibility_rank[4]       # null nếu chưa có nhãn đáng tin
randomization_eligible
anchor_flag
form_version
```

`option_position_policy` phân biệt `fixed`, `balanced_random`, `full_shuffle`, `cyclic_shift` và `fixed_exceptions`. Các exception là item mà thứ tự cần giữ vì grammar, numeric order, “all/none of the above” hoặc semantic progression; exception phải có lý do content-validity và không được giả vờ là random.

### Production pseudocode

```text
function serve_item(item, user, form):
    assert item.construct == "receptive_written_breadth"
    options = item.option_content_ids

    if item.option_position_policy == "full_shuffle":
        perm = cryptographic_or_server_prng_permutation(options, seed=form_seed + item.id)
    elif item.option_position_policy == "cyclic_shift":
        # giữ relative order để tách absolute position khỏi distractor order
        shift = server_prng_integer(0, len(options)-1, form_seed + item.id)
        perm = rotate(options, shift)
    elif item.option_position_policy == "balanced_random":
        perm = assign_key_position_from_randomized_pool(item, form)
    else:
        perm = options

    display = render(perm)
    save_audit(response_id, item.id, form.version,
               permutation_id=hash(perm),
               display_order=ids(perm),
               correct_display_position=index_of(item.correct_content_id, perm))
    return display

function score_response(response, item):
    correct = response.selected_content_id == item.correct_content_id
    # không cộng/trừ theo absolute position
    return int(correct)

function calibration_model(response_data):
    # Chỉ chạy khi có đủ response theo từng position và common persons/items
    fit baseline = IRT_or_Rasch(item_stem, band, person)
    fit position_model = baseline + correct_display_position + distractor_position_features
    compare out_of_sample_fit(position_model, baseline)
    if position_effect_is_replicated_and_material(position_model):
        retain position covariate or redesign item
    else:
        retain randomized display and report position sensitivity as zero/low only
```

### Position sensitivity trong uncertainty

Điểm breadth chính vẫn là số đáp án đúng đã hiệu chỉnh theo item model và lexical-unit universe. Position không được biến thành một correction cố định khi chưa có bằng chứng. Khi đã có pilot, fit hai model:

```text
M0: logit P(Y=1) = theta_person - b_item
M1: logit P(Y=1) = theta_person - b_item + gamma_position[p]
                         + delta_distractor_features
```

Dùng common items/common persons hoặc random assignment đủ mạnh để nhận dạng `gamma`. Đánh giá:

- change in item difficulty và person `K_hat`;
- item-fit và residual theo position;
- hold-out log-loss/Brier hoặc predictive accuracy;
- coverage của CI/credible interval khi position policy thay đổi;
- sensitivity của `K_hat` giữa observed order, cyclic-shift counterfactual và full-shuffle counterfactual.

Nếu chưa chứng minh được `gamma`, báo cáo:

```text
K_hat_primary = calibrated breadth estimate
position_sensitivity = range(K_hat_under_validated_position_models)
```

Không gọi range này là sampling CI. Nó là model/design sensitivity.

## So sánh với Preply và VST tham chiếu

| Khía cạnh | VST/nguồn đã kiểm tra | Preply hiện tại |
|---|---|---|
| Option format | Hohensinn: 4 option; Lions: 5 option; Aptis evidence: 4 option listening | Chưa có nguồn HTTP 200 xác minh current format trong callback này |
| Key position | 4-option study thấy hiệu ứng rất nhỏ, key về cuối hơi khó hơn | Chưa xác minh có randomization hay position calibration |
| Distractor order | Lions thấy distractor mạnh thường ở giữa, yếu ở cuối trong dữ liệu 5-option lớn | Chưa xác minh distractor manifest/plausibility/order |
| Scoring | Khuyến nghị score theo content correctness; không penalty theo position | Chưa xác minh scoring code current; không được gán correction mới |
| Randomization | Random key/option, nhưng phải tránh pattern dễ đoán và lưu viewing order | Chưa xác minh seed, permutation hoặc display-order logging |
| Uncertainty | Position sensitivity là lớp riêng với sampling/IRT uncertainty | Chưa xác minh interval/position contribution |
| Chuyển sang `K_hat` | Chỉ sau calibration đúng modality và hold-out | Chưa có response-level/item-bank data để làm linking |

Preply không được mô tả là có hoặc không có position bias. Claim đúng ở iteration này chỉ là: **chưa tìm được nguồn xác thực cho cơ chế option order và position calibration hiện tại của Preply**.

## Validation plan

1. **Static item QA:** kiểm tra mỗi item có đúng một key, bốn option hợp lệ, không lỗi grammar khi hoán vị; phát hiện “all/none”, ordinal/numeric và fixed exceptions.
2. **Generator QA:** sinh ít nhất nhiều form từ cùng bank; kiểm tra mỗi key position, band và L1 không lệch bất thường; lưu seed/permutation ID.
3. **Counterbalanced pilot:** random assignment người làm bài vào cyclic-shift forms và full-shuffle forms; giữ item stem và content options giống nhau.
4. **Model comparison:** fit baseline Rasch/1PL và model có position + distractor features; dùng common-person/common-item, item-fit và hold-out.
5. **Response-process check:** trên subset, log latency và viewing/selection order nếu khả thi; không biến latency thành knowledge score.
6. **Decision gate:** nếu position effect được lặp lại và làm `K_hat` thay đổi vượt precision target, redesign/randomization hoặc giữ covariate trong model; nếu không, giữ randomization, audit metadata và báo `position_sensitivity` nhỏ.
7. **Preply bridge:** chỉ so sánh với Preply sau khi biết cùng lexical unit, modality, option format và scoring estimand; nếu không, báo hai scale riêng.

## Gaps

- Chưa có item bank, response-level data, display-order log hoặc randomization code của Preply; **chưa tìm được nguồn xác thực cho ý này**.
- Bằng chứng Lions chủ yếu trên five-option national tests; chưa đủ để định lượng vị trí/distractor effect riêng cho four-option vocabulary recognition.
- Chưa có pilot của target VST để chọn ngưỡng “material” cho `position_sensitivity`, số response mỗi position hoặc prior/model specification.
- Chưa có bằng chứng rằng option-order effect trong Aptis listening có cùng độ lớn với receptive written vocabulary; cần xem đây là transportability gap.

## Kết luận iteration 52

1. Với bốn lựa chọn, nghiên cứu EFL lớn cho thấy key-position effect nhỏ nhưng có hướng; randomization là baseline hợp lý, không phải bằng chứng rằng effect luôn bằng zero.
2. Distractor order là confound riêng: distractor mạnh có thể tập trung ở giữa và distractor yếu ở cuối, làm sai diễn giải middle bias nếu chỉ theo dõi key.
3. Production nên randomize server-side, tránh balanced pattern dễ đoán, lưu permutation/display order và không cộng/trừ `K_hat` theo vị trí quan sát được.
4. Position effect phải được đánh giá đúng modality và bằng counterbalanced common-item/person pilot; nếu có effect lặp lại, đưa vào calibration hoặc redesign, còn nếu chưa có evidence thì để ở lớp sensitivity chứ không gọi là CI.
5. Preply current option-order và position controls vẫn là gap vì endpoint không xác minh được; không được đồng nhất với VST tham chiếu hay tự suy ra mechanics hiện tại.
