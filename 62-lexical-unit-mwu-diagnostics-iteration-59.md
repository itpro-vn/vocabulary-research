# Iteration 59 — Lexical-unit ontology beyond single words: multiword units và phrase-aware diagnostics

## Phạm vi và kết luận

Iteration này kiểm tra một rủi ro estimand: một vocabulary-size test có thể đếm **single-word units** nhưng người dùng lại hiểu “vocabulary” bao gồm collocations, idioms, formulas, phrasal verbs và lexical bundles. Nếu trộn các đơn vị này vào một `K_hat`, con số không còn cùng nghĩa với word-family/headword estimate.

Kết luận bảo thủ:

- `K_single_word` vẫn là output breadth chính, với universe, lexical unit và phiên bản corpus/dictionary được khai báo.
- Multiword-unit (MWU) knowledge phải là một profile/facet riêng: loại MWU, item list/version, recognition hoặc recall score, token coverage và uncertainty.
- Không cộng MWU vào `K_single_word` bằng hệ số cố định. Phrase-aware total chỉ được tạo nếu đó là một estimand mới, có calibration common-person/common-item và validation riêng.
- Coverage của MWU phải tính theo độ dài mỗi phrase và corpus token, không dùng nguyên công thức single-word coverage.

## Nguồn đã fetch và kiểm tra

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| Victoria University of Wellington, *Vocabulary tests* | 200 | Phân biệt Vocabulary Size Test và Levels Test; target population và 20.000 word families |
| Nation, *The Vocabulary Size Test: information and specifications* (bản PDF mirror) | 200 | Construct single words, loại trừ MWU, frequency sampling, số item và hệ số mở rộng |
| Coxhead (2021), *Vocabulary in English in Tertiary Contexts* (ERIC PDF) | 200 | Collocations, formulas, lexical bundles và chức năng MWU |
| Nguyen & Coxhead (2023), *Evaluating multiword unit word lists for academic purposes* (publisher PDF) | 200 | Unit of counting, corpus/list evaluation, coverage formula, overlap và số liệu MWU |
| Preply vocabulary-test endpoint | 403 | Không citable cho cơ chế MWU hiện tại; chỉ ghi gap |

## Bằng chứng đã xác minh

### 1. Vocabulary-size estimand của VST tham chiếu là single words

Trang chính thức của Victoria University of Wellington phân biệt:

- Vocabulary Size Test: đo tổng số từ biết.
- Vocabulary Levels Test: đo kiến thức ở các dải tần suất cụ thể.
- VST bao phủ 20.000 word families và phù hợp native speakers/advanced non-native speakers; bản 14.000 phù hợp hơn với advanced non-native learners hoặc native speakers dưới 12 tuổi.

Specifications của Nation nêu rõ VST đo written receptive vocabulary size. Universe được định nghĩa là **single words**, không gồm multiword units, proper nouns, transparent compounds, marginal words và abbreviations; test cũng không đo khả năng phân biệt homonyms/homographs. Đây là ràng buộc construct, không chỉ là chi tiết triển khai.

Hệ quả: nếu sản phẩm muốn nói “ước lượng số từ biết” theo VST-style, phrase như `on the other hand`, `take into account` hoặc một idiom không được âm thầm biến thành một word-family/headword. Phải giữ nguyên unit đã công bố hoặc trả thêm facet phrase knowledge.

### 2. Frequency sampling không giải quyết MWU ontology

Nation mô tả 14.000-version có 140 multiple-choice items, 10 item từ mỗi 1.000 word-family level; tổng điểm nhân 100. Hai 20.000 parallel versions có 100 item; tổng điểm nhân 200 và hai form đã được kiểm tra equivalence.

Tài liệu cũng cảnh báo số item ở từng frequency level quá ít để đo đáng tin mastery của từng band; total score mới là mục tiêu. Vì vậy, frequency band chỉ giải quyết coverage của **declared vocabulary universe**. Nó không tự quyết định:

- phrase nào là một lexical item;
- các inflected forms của phrase có gộp hay không;
- phrase coverage có nên đổi thành số single words hay không;
- một người biết hai constituent words có được coi là biết collocation hay không.

### 3. MWU là construct sử dụng riêng

Coxhead (2021) mô tả MWU là các chuỗi từ thường xuất hiện cùng nhau không chỉ do ngẫu nhiên. Các dạng gồm:

- academic collocations hai từ, ví dụ `significant difference` và `basic function`;
- formulas;
- lexical bundles dài hơn, ví dụ `on the other hand`, `on the basis of`, `as a result of`.

Bài nêu Academic Formulas List có 607 formulas: 207 xuất hiện trong cả written và spoken texts, 200 written-only và 200 spoken-only. Các MWU còn được phân loại theo chức năng như comparison/contrast và discourse organisation.

Đây là bằng chứng rằng phrase knowledge có modality, register và discourse-function facets. Nó không nên bị nén thành một correction cho receptive single-word count.

### 4. Unit of counting cho MWU không thể mặc định là headword/family

Nguyen và Coxhead (2023) đánh giá hai academic-collocation lists bằng ba lớp: framework về purpose/corpus/selection/validation, so sánh lexical constituents và lexical coverage.

Nghiên cứu báo:

- ACL: 2.469 items.
- AECL: 9.049 items.
- Overlap: 1.298 items, tương đương 52,57% của list ACL nhưng chỉ 14,34% của AECL.

Tác giả cảnh báo unit of counting cho collocations phức tạp hơn single words. Một số pattern phù hợp với lemma khi tense/number không thay đổi collocational target, nhưng các pattern khác nên dùng type vì các verb forms có thể có collocate khác nhau. Ví dụ về nguyên tắc: `make/makes/made/making a decision` có thể được xử lý khác với một adverb–verb pattern mà collocate phụ thuộc vào verb form.

Hệ quả cho item bank: mỗi MWU phải có `mwu_unit_policy` rõ ràng, ví dụ `surface_type`, `lemma_pattern`, hoặc `formula_template`; không thể dùng chung quy tắc word-family đã chọn cho single words.

### 5. MWU coverage cần công thức riêng và báo theo corpus

Nguyen và Coxhead dùng công thức coverage cho MWU:

```text
MWU_coverage =
  Σ_i (frequency(MWU_i) × number_of_words(MWU_i))
  / total_running_words(corpus) × 100
```

Lý do là một occurrence của phrase bao phủ nhiều token. Dùng `frequency(MWU_i) / corpus_tokens` như single-word coverage sẽ không tương thích với định nghĩa token coverage.

Trong COCA Academic, nghiên cứu báo:

| List | Items | Overall coverage |
|---|---:|---:|
| ACL | 2.469 | 0,84% |
| Total AECL | 9.049 | 2,76% |
| Lex AECL | 8.770 | 1,46% |
| Gram AECL | 279 | 1,30% |

500 MWU thường xuyên nhất chiếm 64,29% coverage của ACL và 52,05% của AECL. Tác giả cũng nhấn mạnh coverage của MWU thấp hơn single-word list; trong cùng nghiên cứu, Academic Vocabulary List của Gardner & Davies được nêu với coverage gần 14% trên corpus academic. Các con số này là corpus/list-specific, không phải hệ số đổi phrase thành số từ phổ quát.

### 6. List construction phải có statistical và content QA

Trong mô tả được Nguyen và Coxhead tổng hợp:

- ACL dùng frequency, dispersion, MI và t-score; có manual vetting của hai tác giả và expert review bởi năm chuyên gia.
- Từ 6.808 collocations được trích xuất bằng máy, manual checking loại 63,7% để giữ list có mục tiêu sư phạm.
- ACL có coverage trên academic corpus cao hơn 14 lần so với general corpus trong validation được báo cáo.
- List dài hơn không mặc nhiên tốt hơn: phân phối Zipf làm coverage tăng thêm giảm dần; 500 item đầu có thể mang phần lớn coverage.

Production implication: không đưa mọi n-gram hoặc mọi phrase từ corpus vào test. MWU bank phải lưu purpose, register, corpus, dispersion, association scores, selection decision, semantic/function tag và reviewer/version metadata.

## Thiết kế estimand và data model

### Output chính

```text
K_single_word
unit = headword | lemma | word_family
universe_version
corpus_version
N_h per frequency stratum
CI_response_or_model
CI_item_sampling
```

### Output MWU độc lập

```text
MWU_profile = {
  list_version,
  corpus_version,
  mwu_unit_policy,       # surface_type | lemma_pattern | formula_template
  mwu_types,             # collocation | idiom | formula | lexical_bundle | phrasal_verb
  register,
  modality,              # written | spoken | both
  item_count,
  score_mode,            # recognition | recall | contextual_use
  score_by_type,
  token_coverage,
  coverage_uncertainty,
  response_or_model_SE,
  validity_status
}
```

`MWU_profile` không được cộng vào `K_single_word`. Nếu một phrase chứa constituent words chưa biết, đó là thông tin về phrase construction và usage, không phải bằng chứng tự động rằng constituent word forms đã được master ở mọi sense.

## Thuật toán đề xuất

### Item-bank manifest

Mỗi single-word item và MWU item cần tối thiểu:

```text
item_id, lexical_unit, unit_policy, target_sense, POS,
frequency_band, corpus_version, register, modality,
source_list_version, mwu_type, constituent_count,
association_score, dispersion, reviewer_status,
anchor_flag, exposure_status
```

### Pseudocode

```text
input:
  single_word_bank B_sw with declared strata M_h
  mwu_bank B_mwu with list/corpus/version metadata
  single_word_responses y_sw
  mwu_responses y_mwu

# Main breadth estimand
validate(B_sw.unit_policy, universe_version, corpus_version)
fit_or_lookup_calibrated_RA_model(y_sw, B_sw)
K_single_word = count_from_stratified_posterior_or_design_estimator(
    responses=y_sw,
    universe_sizes=M_h,
    item_parameters=B_sw.parameters
)

# Independent phrase profile
validate(B_mwu.list_version, B_mwu.mwu_unit_policy,
         B_mwu.register, B_mwu.modality)
score_mwu = score_by_item_type(y_mwu, B_mwu)
for each corpus c and MWU item i:
    coverage_c += freq_c[i] * constituent_count[i]
MWU_token_coverage = coverage_c / running_tokens_c * 100

report K_single_word with uncertainty
report MWU_profile with score_SE and token_coverage
never set K_single_word = K_single_word + f(score_mwu)

if a phrase-aware total is requested:
    require a new declared estimand, common-person/common-item linking,
    hold-out criterion validity and pre-registered conversion rule
else:
    phrase_aware_total = null
```

### Uncertainty

Với single-word count, giữ các thành phần riêng:

```text
CI_single_word = response/model + item-sampling + reference-population sensitivity
```

Với MWU coverage, cần ít nhất:

```text
Var(MWU_coverage) =
  response/model uncertainty
  + corpus-frequency uncertainty
  + list/selection sensitivity
  + overlap/dependence sensitivity
```

Không nên coi 0,84%, 1,46% hay 2,76% là interval cho mọi corpus. Nếu cùng phrase xuất hiện dưới nhiều inflectional patterns, sensitivity phải chạy theo từng `mwu_unit_policy` thay vì silently deduplicating.

## So sánh với Preply

| Khía cạnh | Thiết kế đề xuất | Preply xác minh được trong iteration này |
|---|---|---|
| Main unit | Single-word universe được khai báo rõ; MWU là facet riêng | Endpoint trả 403; chưa xác minh Preply có MWU hay chỉ dictionary entries/headwords |
| Phrase inclusion | Không gộp MWU vào `K_single_word` | Chưa tìm được nguồn xác thực cho inclusion/exclusion rule |
| Frequency/corpus | Versioned corpus, band, register và coverage metric | Chưa xác minh corpus/MWU metadata hiện tại |
| MWU scoring | Recognition/recall/contextual-use tách theo type và modality | Chưa xác minh Preply có phrase items hoặc phrase scoring |
| Conversion | Không dùng hệ số cố định từ phrase score sang word count | Không được ghi Preply dùng conversion này |
| Reporting | `K_single_word` + `MWU_profile` + uncertainty | Chưa xác minh Preply công khai output schema này |

## Validation plan và release gates

1. **Construct gate:** expert panel xác nhận single-word và MWU definitions, sense boundaries, phrase templates và intended use.
2. **Corpus gate:** freeze corpus/list versions; kiểm tra frequency, dispersion, register và modality; chạy sensitivity qua corpora.
3. **Unit gate:** adjudicate type/lemma/template policy trên sample; đo inter-rater agreement và lưu bất đồng.
4. **Item gate:** pilot recognition/recall/contextual-use riêng; kiểm tra difficulty, distractor/function, local dependence và DIF.
5. **Linking gate:** nếu muốn phrase-aware output, dùng common-person/common-item design để không nhầm scale.
6. **Coverage gate:** tái tạo token-weighted MWU coverage từ manifest; kiểm tra không double-count overlapping phrases nếu mục tiêu yêu cầu mutually exclusive units.
7. **Validity gate:** hold-out so sánh `K_single_word` với independent reading/usage criteria; MWU profile với contextual-use criterion. Không dùng phrase score làm criterion cho single-word count nếu chưa chứng minh construct overlap.
8. **Release gate:** nếu phrase list, unit policy, corpus hoặc conversion chưa ổn định, release `MWU_profile` ở trạng thái diagnostic-only và giữ phrase-aware total là `null`.

## Gaps

- Preply endpoint trả HTTP 403; chưa tìm được nguồn xác thực cho current MWU item bank, collocation/idiom/formula policy, phrase scoring, corpus, phrase frequency metadata hoặc phrase-to-word conversion.
- Chưa có response-level data để ước lượng độ khó, reliability, DIF, dependence hoặc common-scale linking giữa single-word và MWU facets.
- Các coverage numbers của Nguyen–Coxhead là corpus/list-specific; không được chuyển thành correction coefficient cho Preply.
- Chưa có bằng chứng để nói một người biết constituent single words sẽ biết collocation tương ứng; phải kiểm tra bằng item-level data.

## Nguồn

- https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/vocabulary-tests
- https://pdfs.semanticscholar.org/83a0/ae0a6e780d6f2ee672905b827d806edb5d1b.pdf
- https://files.eric.ed.gov/fulltext/EJ1284507.pdf
- https://www.jbe-platform.com/docserver/fulltext/itl.21041.ngu.pdf?expires=1700873875&id=id&accname=jbid110695&checksum=1035364D26C400B95E608310CFC484C2
- https://preply.com/en/learn/english/test-your-vocab
