# Iteration 61 — Dialect/register và transportability của World Englishes

## Phạm vi và kết luận

Iteration này kiểm tra một failure mode riêng: một bài vocabulary-size test có thể đo exposure với BrE/AmE hoặc một register cụ thể thay vì chỉ đo receptive written vocabulary breadth. Bằng chứng chính thức cho thấy English có biến thể khu vực có hệ thống; các corpus khu vực cũng được thiết kế theo thể loại và không nhất thiết đại diện cho dân số. Vì vậy frequency bands, item difficulty và score linking phải có target variety/register rõ ràng.

**Quy tắc đề xuất:** `K_single_word` vẫn là estimand chính, nhưng mỗi lexical unit phải có metadata về variant, spelling, sense và register. Với item mà mọi variant đều biểu đạt cùng form–meaning construct, canonicalize và chấp nhận các spelling/lexical variants đã được xác định trước. Với item chỉ hợp lệ trong một variety/register, gắn `variant_specific=true`, dùng quota và báo profile riêng. Không cộng điểm correction cho variant; chỉ hiệu chỉnh bằng common-person/common-item data.

## Nguồn đã fetch và verify

| Nguồn | HTTP | Bằng chứng dùng trong iteration |
|---|---:|---|
| [ICE homepage, UZH](https://www.ice-corpora.uzh.ch/en.html) | 200 | ICE có mục tiêu so sánh English worldwide; 26 nhóm xây corpus quốc gia/khu vực; mỗi corpus khoảng 1 triệu từ nói và viết; có common design/annotation. |
| [ICE design, UZH](https://www.ice-corpora.uzh.ch/en/design.html) | 200 | Thiết kế 300 spoken + 200 written texts, nhiều genre; người cung cấp dữ liệu học bằng English trong quốc gia corpus; tỷ lệ nhóm không đại diện toàn dân số. |
| [Cambridge Grammar: British and American English](https://dictionary.cambridge.org/grammar/british-grammar/british-and-american-english) | 200 | Khác biệt BrE/AmE chủ yếu ở vocabulary, pronunciation, spelling; writing ít khác hơn speaking; ví dụ learned/learnt, fit/fitted, got/gotten, at/on the weekend. |
| [ETS Standards for Quality and Fairness 2014](https://www.ets.org/pdfs/about/standards-quality-fairness.pdf) | 200 | Yêu cầu DIF khi đủ dữ liệu, giảm language/cultural validity threats, mô tả adaptation, review/pretest theo intended population, periodic review và linking/equating có population/anchor/SE/model-fit documentation. |
| [Preply methodology](https://preply.com/en/learn/english/test-your-vocab/how-it-works) | 403 | Không thể xác minh chính sách variant, register sampling, item-bank metadata, DIF hoặc equating hiện tại của Preply; đây là gap, không phải bằng chứng Preply không có các cơ chế đó. |

## Tác động lên estimand và item bank

Định nghĩa tối thiểu cho mỗi item:

```text
lexical_unit_id, lemma_or_headword, sense_id
variant_set = {neutral, BrE, AmE, IndianE, ...}
spelling_set = {colour, color, ...}
register = {spoken, academic, news, informal, ...}
frequency_manifest_id, raw_count, document_count
variant_specific, accepted_response_policy
anchor_group, form_id, exposure_count
```

Hai trường hợp phải tách:

1. **Variant-invariant breadth:** `colour`/`color` hoặc `learned`/`learnt` là các surface forms của mục tiêu đã định nghĩa, và test đo khả năng nhận biết meaning. Ghi variant và chấp nhận cả hai khi đáp án là dạng nhập; MCQ không được biến một spelling hợp lệ thành distractor sai nếu stem không tuyên bố chuẩn khu vực.
2. **Variant/register-conditioned knowledge:** một mục từ hoặc sense chỉ phổ biến trong khu vực/register nhất định. Không xóa tự động vì đó là lexical knowledge thật; giữ item trong stratum có nhãn và báo `K_target_variant`/`coverage_target_variant` riêng. Nếu muốn một global score, phải định nghĩa weighting population trước, không dùng frequency của một corpus làm universal weight.

ICE là bằng chứng trực tiếp cho nhu cầu này nhưng không phải norm sample: mỗi component có khoảng một triệu từ theo common design, song design genre có chủ đích và trang chính thức cảnh báo phân bố giới/tuổi không đại diện dân số. Do đó không được coi một regional corpus frequency distribution là phân bố item difficulty hoặc population norm nếu chưa có validation.

## Thuật toán variant-aware

### Bước 1 — Khai báo target

```text
target = {
  construct: "written_receptive_single_word_breadth",
  lexical_unit: "headword | lemma | word_family",
  target_variety: "neutral_global | BrE | AmE | ...",
  target_register: "balanced | spoken | academic | ...",
  population: documented calibration population
}
```

`neutral_global` không có nghĩa “không có biến thể”; nó nghĩa item phải có evidence rằng form/meaning được hiểu trong các subgroup mục tiêu, hoặc item được đưa vào variant profile thay vì main score.

### Bước 2 — Tuyển item và review

```text
for candidate in frequency_strata:
    annotate(candidate, sense, variant_set, register, corpus_manifest)
    if spelling_or_lexical_variant_is_valid(candidate):
        map_to_same_construct_or_mark_variant_specific(candidate)
    review_by_subject_matter + regional reviewers
    pretest on target population and relevant variants
    estimate difficulty, discrimination, DIF, distractor functioning
    retain only if content, fit, exposure and fairness gates pass
```

ETS 7.3–7.7 cung cấp gate thực hành: item phải giảm construct-irrelevant variance; reviewer phải phù hợp; pretest nên đại diện intended population; test và active items phải được operational/periodic review.

### Bước 3 — Scoring và linking

Với form đã calibrated:

```text
p_i(theta, g) = P(correct | ability theta, item i, variant subgroup g)
theta_hat_g = argmax_theta L(response | theta, item_parameters, g)
K_hat_g = h_g(theta_hat_g, lexical_unit, target_population)
```

`h_g` phải được fit trên calibration sample; không dùng hệ số BrE→AmE hay global correction suy đoán. Nếu có các form/variant:

```text
anchors = common lexical units with invariant construct and stable functioning
fit/link forms using common-person or common-item design
check anchor DIF and model fit
retain common scale only if construct and population comparability are documented
report SE_link and sensitivity when anchor set changes
```

Theo ETS 8.1–8.6, comparability phải gắn với population và định nghĩa comparability; linking/equating phải mô tả anchor, calibration, assumptions, standard errors và fit. Nếu forms đo target variety/register khác nhau, kết quả mặc định là profile riêng, không phải interchangeable K.

### Bước 4 — Báo cáo

```text
return {
  K_main: estimate for declared construct and target,
  interval_response_model: calibrated conditional interval,
  variant_profile: estimates/coverage by variant and register,
  sensitivity_common_scale: range across accepted anchor sets,
  flags: [variant_DIF, sparse_variant_band, nonrepresentative_norm,
          form_not_equated, target_mismatch]
}
```

Không diễn giải `K_main` như “tổng tất cả từ tiếng Anh trên thế giới”. Nếu norm sample hoặc item exposure chỉ thuộc một variety/register, báo rõ điều kiện đó.

## So sánh với Preply (chỉ phần đã/không đã xác minh)

| Thành phần | Quy tắc đề xuất | Preply đã xác minh |
|---|---|---|
| Vocabulary universe | Khai báo lexical unit + target variety/register; giữ manifest version | Proxy methodology trước đây mô tả dictionary-headword/BNC-derived ranking; current variant metadata chưa xác minh trong callback này |
| Variant handling | Variant map, accepted forms, variant-specific flags; không correction cố định | Chưa tìm được nguồn xác thực cho BrE/AmE/World English policy |
| Sampling | Frequency strata có register/variant quota và target-population rationale | Proxy methodology trước đây nêu hai-stage logarithmic sampling; current variant/register allocation chưa xác minh |
| Calibration | Pretest theo subgroup, DIF và common-anchor linking trước khi so sánh form | Chưa xác minh production item parameters, subgroup response data hoặc equating |
| Reporting | `K_main` + variant/register profile + conditional uncertainty/flags | Chưa xác minh Preply có profile hoặc uncertainty decomposition như vậy |

## Validation plan

1. Xây candidate set từ các corpus/lexicographic sources đã version hóa; gắn variant, sense, genre và raw/document frequency.
2. Expert review với đại diện target varieties để tách spelling variant, lexical replacement, semantic shift và register-only item.
3. Pilot đủ lớn theo variety × proficiency × register; randomize form nhưng bảo toàn quota và exposure cap.
4. Fit 1PL/2PL (và model sensitivity), kiểm tra item fit, local dependence, distractor functioning và DIF conditional on ability. DIF là trigger review, không tự động exclusion.
5. Tạo common-anchor forms. Kiểm tra anchor stability, construct equivalence, linking error và held-out score agreement; nếu fail, báo score riêng.
6. Kiểm tra coverage/uncertainty theo từng stratum; dùng bootstrap hoặc posterior draws bao gồm item sampling và linking sensitivity. Không chuyển kết quả ICE thành margin-of-error cho cá nhân.
7. Theo dõi drift theo corpus/version, region/register và thay đổi accepted spelling; re-review khi item frequency hoặc usage distribution thay đổi.

## Gaps

- Preply endpoints trả 403; **chưa tìm được nguồn xác thực cho** variant labels, accepted spelling policy, regional/register sample allocation, DIF, anchors, calibration và form-equating của Preply.
- Chưa có response-level pilot của test mục tiêu để ước lượng mức chênh difficulty giữa variant groups; do đó chưa có correction factor, cutoff DIF hay sample-size rule riêng.
- ICE mô tả corpus design và cảnh báo nonrepresentativeness nhưng không cung cấp mapping trực tiếp từ corpus regional frequency sang vocabulary-size score; không được suy ra mapping đó.
