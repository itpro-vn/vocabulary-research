# Iteration 48 — Morphological transparency và word-family estimand

## Phạm vi và nguồn đã kiểm tra

Iteration này kiểm tra một vấn đề hẹp nhưng ảnh hưởng trực tiếp đến công thức quy đổi vocabulary size: một word family không phải danh sách các headword được gộp cơ học. Direction tập trung vào tính minh bạch hình thái (morphological transparency), productivity của phụ tố, khả năng suy ra thành viên family và việc tách breadth trực tiếp khỏi morphology/depth.

Các URL dưới đây đều đã được fetch bằng `curl -L` với browser user-agent và trả HTTP 200 trước khi trích dẫn:

1. Bauer & Nation (1993), *Word Families*, PDF tại Victoria University/LExtutor: <https://www.lextutor.ca/morpho/fam_affix/bauer_nation_1993.pdf>.
2. Khaing & Poonpon (2020), *Word Knowledge through Morphological Awareness in EFL Learners*, TESOL International Journal, PDF tại ERIC: <https://files.eric.ed.gov/fulltext/EJ1257212.pdf>.

Trang Oxford của bài Bauer & Nation và trang Preply chính trả 403 trong callback này, nên không dùng chúng làm URL mới đã xác minh. Phương pháp Preply trong report được giữ theo artifact trước, nơi proxy methodology đã được fetch; production item bank và response-level data của Preply vẫn là gap.

## Findings đã xác minh

### 1. Word family là estimand phụ thuộc người học và mục đích

Bauer & Nation mô tả word family trong bối cảnh đọc là base word cùng các dạng phái sinh và biến hình mà người học có thể hiểu mà không phải học từng dạng riêng. Ví dụ watch, watches, watched và watching có thể cùng family nếu người học nắm được phụ tố biến hình. Kích thước family tăng theo kiến thức affixation của người học. Quan hệ phải gần về nghĩa; hard và hardly không được xem là cùng family.

Hệ quả: `K_family` không đồng nhất với `K_headword`, `K_lemma` hoặc số form xuất hiện trong dictionary. Nó là số đơn vị mà người học có thể xử lý như một đơn vị hình thái cho một mục đích cụ thể, ở một mức morphological awareness cụ thể. Vì vậy report phải khai báo lexical unit trước khi cho người dùng một con số.

### 2. Tính minh bạch không phải cờ nhị phân duy nhất

Bauer & Nation dùng các tiêu chí frequency, productivity, predictability, regularity của dạng viết và nói, regularity của affix và regularity của function để xếp các affix vào bảy mức. Ở những mức đầu, affix thường dễ nhận diện, có nghĩa dễ dự đoán và có tính sản sinh cao; ở các mức sau, bất quy tắc hình thức, âm thanh và nghĩa tăng. Tác giả cũng nhấn mạnh thứ tự này được xây cho mục đích đọc; mục đích khác có thể cần thứ tự khác.

Không được dùng một multiplier cố định kiểu “một base biết = toàn bộ family biết”. Item-bank manifest nên lưu tối thiểu:

```text
family_id
base_or_lemma
member_id
frequency_band
morphology_level (2..7 hoặc nhãn tương đương)
affix
semantic_relatedness / transparency rating
orthographic_regular
phonological_regular
productivity_class
member_attested_in_corpus
```

### 3. Affix knowledge là thành phần liên quan nhưng không thay thế breadth

Khaing & Poonpon (2020) nghiên cứu 92 sinh viên EFL Thái Lan. Bài dùng một receptive affix-knowledge test gồm 72 MCQ, trong đó pseudowords kết hợp với affixes thật nhằm giảm lợi thế do người học đã biết sẵn từ; bài productive affix-knowledge yêu cầu tạo dạng từ. Hai loại năng lực không bị gộp thành một điểm vocabulary breadth.

Tương quan giữa tổng điểm receptive và productive affix knowledge là `r = .38` ở nhóm treatment và `r = .53` ở nhóm control. Các con số này thuộc sample và thiết kế của nghiên cứu, không phải hệ số chuyển đổi production. Chúng ủng hộ việc giữ morphology/depth thành output chẩn đoán riêng thay vì cộng trực tiếp vào `K_hat`.

Bài cũng báo cáo rằng sau can thiệp dạy affix, điểm receptive affix của nhóm treatment tăng; điều này cho thấy kiến thức morphology có thể thay đổi độc lập theo instruction. Một bài vocabulary-size test vì vậy không nên diễn giải điểm family cao như bằng chứng chắc chắn về productive command hoặc khả năng dùng mọi member.

## Quy tắc thuật toán đề xuất

### Hai estimand bắt buộc

- `K_direct`: số đơn vị lexical được suy ra từ các item trực tiếp, với response model đã calibrate. Đây là output breadth chính và tương thích nhất với bài test receptive dạng Preply-like.
- `K_family_range`: khoảng nhạy cảm cho family expansion, không phải một số tuyệt đối mặc định.

Với family `g` có các member `j`, lưu `p_direct(g)` từ item response model và một hệ số suy ra đã được calibration theo level:

```text
p_infer(g,j) = clamp( a[level_j] * p_direct(g)
                       + b[level_j] * morphology_signal(g,j)
                       + c[level_j] * corpus_attestation(g,j), 0, 1 )
```

Trong giai đoạn chưa có calibration, không đặt `a`, `b`, `c` theo trực giác. Thay vào đó:

```text
K_family_lower = sum_g 1[p_direct(g) >= mastery_cut]
K_family_upper = sum_g sum_j 1[p_direct(g) >= mastery_cut] * eligible(g,j)
```

`eligible(g,j)` chỉ cho phép những member có quan hệ nghĩa/hình thái được manifest đánh dấu là hợp lệ; upper bound phải được ghi là giả định rộng, không phải estimate đã kiểm chứng.

Khi có pilot, ước lượng `p_infer` riêng theo morphology level và transparency strata trên hold-out sample. Chỉ công bố một `K_family` point estimate nếu interval calibration có coverage chấp nhận được và residual bias không tăng mạnh ở các level 5–7. Nếu không, công bố `K_direct` và `[K_family_lower, K_family_upper]`.

### Pseudocode

```text
for each administered item:
    update receptive response model -> p_direct(base_or_target)

for each family g in versioned_family_manifest:
    direct = p_direct(g.base_or_target)
    add direct contribution to K_direct using declared lexical unit

    lower = (direct >= mastery_cut)
    upper = lower
    for member j in g.members:
        if j.eligible_for_family_estimate:
            if calibrated_inference_model_exists:
                upper += 1[p_infer(g,j) >= mastery_cut]
            else:
                upper += 1  # sensitivity upper bound only

report K_direct
report K_family_lower and K_family_upper
if calibrated_inference_model_exists and validation_passed:
    report calibrated K_family with CI and morphology-level diagnostics
else:
    label family range as sensitivity, not a validated point estimate
report morphology/depth diagnostics separately
```

Không nhân điểm raw của một item lên số member trong family. Cách đó sẽ biến một response đúng thành nhiều bằng chứng độc lập giả và làm CI quá hẹp.

## So sánh với cách làm Preply

| Thành phần | Preply-like reference trong các artifact trước | Thiết kế đề xuất iteration 48 |
|---|---|---|
| Đơn vị chính | Methodology công khai trước đây được mô tả là dictionary/headword scale; production mapping chưa có dữ liệu độc lập | Khai báo rõ `headword`, `lemma` hoặc `word family`; tách `K_direct` và family sensitivity |
| Sampling | Midpoint/log-rank sampling của các rank dictionary theo mô tả vendor đã ghi ở artifact trước | Sampling vẫn có thể stratify theo frequency, nhưng manifest phải thêm morphology level/transparency để kiểm tra coverage |
| Family expansion | Chưa tìm được nguồn xác thực cho quy tắc production family expansion của Preply | Không tự động mở rộng family; chỉ mở rộng bằng model đã calibrate hoặc upper-bound sensitivity |
| Uncertainty | Vendor margin trước đây không cho biết uncertainty riêng do family mapping | Tách response/item CI khỏi `K_family_lower–upper` và morphology-model uncertainty |
| Interpretation | Điểm user-facing cần tránh đọc như productive vocabulary hoặc toàn bộ derived forms | `K_direct` = receptive breadth; morphology/depth = chẩn đoán; family count chỉ release sau hold-out validation |

## Assumptions và gaps

1. Word-family criteria của Bauer & Nation được xây chủ yếu cho reading; không chuyển nguyên sang listening, speaking hoặc productive vocabulary.
2. `mastery_cut` phải được đặt bằng item calibration/standard-setting; chưa có dữ liệu Preply để xác định nó.
3. Transparency/productivity ratings cần annotation protocol và inter-rater check; không được coi nhãn từ một dictionary là ground truth tự động.
4. Tương quan `r=.38/.53` của Khaing & Poonpon chỉ là evidence rằng receptive và productive affix knowledge liên quan nhưng không đồng nhất; không dùng làm multiplier.
5. Chưa có response-level Preply, item bank, family manifest, L1 mix hoặc hold-out sample. Chưa tìm được nguồn xác thực cho hệ số chuyển đổi headword → family của Preply.

## Validation plan bổ sung

1. Tạo family manifest versioned từ corpus/dictionary, gắn morphology level 2–7 và transparency/regularity labels.
2. Mời expert panel độc lập đánh nhãn semantic relatedness và eligibility; báo inter-rater agreement theo level.
3. Pretest các member trực tiếp và inferred trên sample đa dạng proficiency/L1; fit model có morphology-level interactions.
4. Hold out theo family để tránh train/test leakage; kiểm tra calibration curve của `p_infer` và coverage của interval.
5. So sánh ba output: `K_direct`, upper/lower family range và một family point estimate nếu đủ điều kiện. Kiểm tra sai lệch theo frequency band, morphology level, L1 và proficiency.
6. Duy trì sensitivity report khi đổi family policy (inflection-only; productive transparent derivation; full Bauer–Nation levels). Nếu thứ hạng người dùng thay đổi mạnh, không công bố family point estimate như một số ổn định.

## Kết luận iteration

Word-family counting chỉ hợp lệ khi mô hình hóa khả năng suy ra member theo morphological transparency, productivity, predictability và mục đích đo. Khuyến nghị production hiện tại là giữ `K_direct` làm vocabulary breadth chính, thêm family lower/upper sensitivity range, và không cộng derived members trực tiếp cho đến khi có calibration/hold-out data. Đây là bổ sung cho thuật toán đề xuất tổng thể; không thay thế các kiểm tra về sampling, IRT, selection, validity và corpus version đã có trong các iteration trước.
