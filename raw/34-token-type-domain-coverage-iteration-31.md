# Iteration 31 — Token/type estimands và calibration coverage theo corpus

## 1. Phạm vi và câu hỏi

Iteration này tách hai đại lượng thường bị gọi chung là “vocabulary size”:

1. **Breadth count**: số đơn vị từ vựng trong một universe đã khai báo (headword, lemma hoặc word family) mà người làm bài nhận diện được.
2. **Usage coverage**: tỷ lệ các **running-word tokens** trong một corpus/domain mà vốn từ đó bao phủ.

Câu hỏi thiết kế là liệu có thể lấy một con số breadth kiểu Preply rồi diễn giải trực tiếp thành phần trăm coverage hay không. Bằng chứng được fetch từ methodology của Preply qua bản Markdown proxy, bài Nation (2006) dạng PDF và bài Durbahn et al. (2024) dạng PDF. Tất cả ba URL được dùng làm nguồn đều trả HTTP 200 khi kiểm tra; endpoint Preply gốc trả HTTP 403 và không được coi là đã fetch trực tiếp.

## 2. Bằng chứng đã xác minh

### 2.1 Preply đo dictionary-entry/headword breadth, không phải token coverage

Preply mô tả một dictionary khoảng 45.000 mục có thứ hạng tần suất. Họ nói rõ chỉ đếm **main entries**, không đếm subentries, và xem một từ là đã biết khi người làm bài biết ít nhất một định nghĩa. Họ cũng phân biệt receptive vocabulary với productive vocabulary. Do đó scale của họ phụ thuộc vào dictionary và quy tắc entry; nó không tự động tương đương với lemma, word family hoặc số token được bao phủ.

Nguồn: [Preply — How the vocab test works](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) (HTTP 200). URL gốc `https://preply.com/en/learn/english/test-your-vocab/how-it-works` trả HTTP 403 trong callback này.

### 2.2 Corpus và derived-form rules của Preply là một phần của estimand

Preply công bố pipeline: dùng British National Corpus; cân bằng lại frequency counts thành một phần spoken demographic, một phần spoken context-governed và một phần written; cộng counts của derived forms vào headword theo từ điển rồi bỏ derived forms; loại các mục không có trong từ điển, gồm tên riêng và gibberish; cuối cùng xếp các dictionary-matched entries theo tần suất giảm dần. Đây là một lựa chọn để tạo **ranked headword universe**, không phải một phép đo coverage trên một domain cụ thể.

Một hệ quả là cùng một rank/headword count có thể bao phủ lượng token rất khác nhau trong hội thoại, văn học, học thuật hoặc phim. Muốn tính usage coverage phải có corpus đích và mapping từng unit sang các occurrence của corpus đó.

Nguồn: [Preply methodology](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) (HTTP 200).

### 2.3 Token, type và word family là các estimand khác nhau

Nation (2006) phân biệt:

- **token**: mỗi lần xuất hiện trong văn bản;
- **type**: mỗi dạng từ khác nhau;
- **word family**: nhóm các dạng/lemmas liên hệ theo quy tắc hình thái.

Trong ví dụ phân tích *Lady Chatterley’s Lover*, 1.000 word families đầu chiếm 80,88% running-word tokens; 2.258 types là nguồn của các token đó nhưng chỉ quy về 898 families xuất hiện trong tác phẩm. Ở band 6.000, chỉ 832 tokens và 263 families xuất hiện. Như vậy frequency concentration làm cho một tập nhỏ families có thể tạo coverage token lớn, trong khi các band thấp tần số thêm nhiều types/families nhưng rất ít token.

Nation cũng cảnh báo word-family size phụ thuộc mức hình thái được chọn. Level 6 có thể gom rất nhiều derivational forms; lemma phù hợp hơn cho productive speaking/writing, còn family lớn có thể hợp lý hơn cho receptive reading/listening. Vì vậy không được dùng một conversion factor cố định giữa headword count, lemma count và family count.

Nguồn: [Nation (2006), How Large a Vocabulary Is Needed for Reading and Listening](https://www.lextutor.ca/cover/papers/nation_2006.pdf) (HTTP 200).

### 2.4 Thứ hạng frequency phụ thuộc corpus và mục tiêu sử dụng

Nation ghi BNC dùng để xây các list có khoảng 90% written và 10% spoken; điều này làm phân bố list chịu ảnh hưởng của văn viết Anh-Anh, formal và adult. Ông đối chiếu hai câu hỏi khác nhau: (a) các từ xuất hiện thường nhất trong chính một spoken corpus bao phủ bao nhiêu; và (b) một list BNC đại diện cho vốn từ của người dùng điển hình bao phủ các corpus khác thế nào. Cách (a) thường cho coverage cao hơn trên chính corpus đó, còn cách (b) hướng tới một universe tổng quát hơn.

Bài viết kiểm tra list trên các corpus độc lập bằng cách xem tokens, types và families có giảm dần từ band cao xuống band thấp hay không. Đây là một kiểm tra ordering hữu ích, nhưng không chứng minh từng item đã ở đúng band.

Nguồn: [Nation (2006)](https://www.lextutor.ca/cover/papers/nation_2006.pdf) (HTTP 200).

### 2.5 Coverage phải gắn với input/domain, không phải diễn giải phổ quát

Durbahn et al. (2024) định nghĩa lexical coverage là phần trăm **running words** đã biết trong một input. Bài tổng hợp ba cách đo: match điểm vocabulary/levels test với lexical profile của text, test trực tiếp các từ xuất hiện trong text, và thao tác thay words bằng nonwords. Bài cũng cho thấy reading, listening và viewing không nhất thiết dùng cùng một coverage threshold; trong viewing, hình ảnh và topic knowledge có thể hỗ trợ suy luận từ chưa biết. Trong nghiên cứu của họ, comprehension giảm khi coverage giảm; 100% cao hơn đáng kể so với 90% và 80%, còn kết luận về threshold phải gắn với task và định nghĩa “adequate comprehension”.

Điều này củng cố quy tắc: một test breadth có thể cung cấp input cho ước lượng coverage, nhưng không được gọi `K words = X% comprehension` nếu chưa có corpus/task-specific calibration.

Nguồn: [Durbahn et al. (2024), Lexical coverage in L1 and L2 viewing comprehension](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DFCA6605076705D5762C98F286D16B27/S0272263124000391a.pdf/lexical-coverage-in-l1-and-l2-viewing-comprehension.pdf) (HTTP 200).

## 3. Đề xuất thuật toán hai output

### 3.1 Manifest và estimand

Mỗi phiên phải lưu:

```text
Universe:
  unit = headword | lemma | word_family
  dictionary_id, corpus_id, corpus_version
  rank_definition, derived_form_rule, proper_name_rule, sense_rule
  total_units = N

DomainProfile:
  domain_id, corpus_version
  token_total = T_d
  unit_token_weight[unit_id] = w_d(unit_id)
```

Output bắt buộc:

- `breadth_estimate`: `K_hat`, số unit của đúng `Universe` được ước lượng là đã biết;
- `breadth_ci`: interval do sampling/response/model cung cấp;
- `domain_coverage[domain_id]`: `C_hat_d`, tỷ lệ token dự kiến được bao phủ;
- `coverage_ci_d`: interval theo sampling/profile bootstrap;
- `coverage_basis`: corpus, tokenization, unit mapping và version;
- `interpretation`: coverage là proxy cho lexical access trong domain, không phải bảo đảm comprehension.

### 3.2 Breadth estimate

Nếu band `b` có `N_b` units và lấy mẫu ngẫu nhiên không hoàn lại `n_b`, với `Y_i` là indicator biết item/unit `i`, baseline breadth là:

```text
p_hat_b = mean(Y_i in sample b)
K_hat = sum_b N_b * p_hat_b
```

Nếu các unit trong band có token weights theo domain, không dùng `p_hat_b` để nhân thẳng với tổng token weight trừ khi giả định exchangeability/weights đồng nhất. Dùng Horvitz–Thompson theo unit:

```text
C_hat_d = (1 / T_d) * sum_b (N_b / n_b) * sum_{i in sample_b} w_d(i) * Y_i
```

Trong đó `T_d = sum_i w_d(i)` trên universe/domain. Công thức này ước lượng token total của các unit được biết, trong khi `K_hat` vẫn ước lượng số unit, không biến thành coverage.

Với simple random sampling không hoàn lại trong từng band, một variance design-based cho coverage là:

```text
Var(C_hat_d) = (1 / T_d^2) * sum_b N_b^2 * (1 - n_b/N_b) * s2_{wy,b} / n_b
```

` s2_{wy,b}` là sample variance của `w_d(i) * Y_i` trong band. Nếu sampling unequal-probability, thay bằng trọng số inclusion probability và replicate/cluster bootstrap. Nếu corpus có nhiều token trong cùng một document hoặc item phụ thuộc, bootstrap theo document/cluster; không dùng CI độc lập một cách máy móc.

### 3.3 Pseudocode

```text
function estimate_breadth_and_coverage(session, universe, bands, domain_profiles):
    assert session.universe_version == universe.version
    responses = administer_calibrated_or_stratified_items(session, bands)
    Y = resolve_known_indicator(responses)  # predeclared receptive rubric

    K_hat = 0
    for b in bands:
        p = mean(Y[i] for i in sample(b))
        K_hat += b.N_units * p

    for domain in domain_profiles:
        covered_token_total = 0
        for b in bands:
            z = [domain.weight(i) * Y[i] for i in sample(b)]
            covered_token_total += (b.N_units / len(z)) * sum(z)
        C_hat[domain.id] = covered_token_total / domain.token_total
        CI_C[domain.id] = design_or_cluster_bootstrap(domain, responses)

    CI_K = breadth_sampling_model_interval(responses, bands)
    return {
      "breadth_estimate": K_hat,
      "breadth_ci": CI_K,
      "domain_coverage": C_hat,
      "coverage_ci": CI_C,
      "unit": universe.unit,
      "universe_version": universe.version
    }
```

### 3.4 Calibration curve và diễn giải

Nếu product cần câu trả lời kiểu “K_hat tương ứng coverage bao nhiêu”, fit riêng một hàm `C_d(K)` từ các learner/known-unit profiles và text hold-out của domain `d`. Dùng monotone spline hoặc binning có bootstrap, kiểm tra coverage của interval và đánh giá theo domain mới. Chỉ được hiển thị `C_d(K_hat)` khi domain/corpus version khớp hoặc có transport validation.

Không đảo ngược một ngưỡng coverage thành một vocabulary size phổ quát. Ví dụ “đạt 95% coverage” phải giữ nhãn corpus/task; cùng K trên một corpus hội thoại và một corpus học thuật không mang cùng coverage.

## 4. So sánh với Preply

| Thành phần | Preply công bố | Thiết kế đề xuất |
|---|---|---|
| Universe | Khoảng 45k dictionary main entries | Manifest versioned; chọn rõ headword/lemma/family |
| Scoring target | Receptive, biết ít nhất một definition | Breadth receptive rubric riêng; depth không cộng vào K |
| Rank | BNC counts, rebalanced spoken/written, derived forms cộng vào headword | Rank là metadata; domain profile độc lập |
| Sampling | Screening khoảng 40 từ rồi narrow sample khoảng 120; midpoint theo rank/log-rank | Stratified hoặc calibrated adaptive sampling, inclusion probability lưu rõ |
| Primary output | Một số vocabulary estimate trên dictionary scale | `K_hat` + CI trên unit scale |
| Token coverage | Không thấy output coverage theo corpus đích trong methodology | `C_hat_d` theo token weights và corpus/domain |
| Uncertainty | Preply công bố margin khoảng ±10% theo mô hình riêng của họ | CI sampling/model/construct tách riêng; coverage CI bootstrap/design-based |
| Conversion | Không có mapping xác minh sang family/lemma hoặc coverage | Chỉ map qua calibration curve có hold-out; nếu thiếu thì báo “chưa tìm được nguồn xác thực cho ý này” |

## 5. Validation plan và giới hạn

1. Xây ít nhất hai corpus hold-out có metadata domain, tokenization và unit mapping; không dùng corpus dùng để xếp rank làm hold-out duy nhất.
2. So sánh `K_hat` và `C_hat_d` trên text mới theo spoken, general written, academic và nếu cần viewing; report bias, MAE và interval coverage.
3. Kiểm tra band ordering bằng token/type/family counts như Nation đề xuất; audit các band có non-monotonicity.
4. Đối chiếu mapping headword↔lemma↔family trên mẫu có annotation; report sensitivity range thay vì nhân một hệ số cố định.
5. Kiểm định trực tiếp domain task bằng comprehension criterion riêng. Coverage chỉ là predictor/proxy; không suy ra comprehension nếu chưa có criterion validation.
6. Khi adaptive sampling được dùng, tính inclusion probability và dùng design/replicate variance; kiểm tra route sensitivity bằng fixed-form và alternate-form hold-out.
7. Chưa có item bank, response-level data hoặc production corpus profile của Preply để ước lượng `C_d(K)`, xác minh exact sample probabilities hoặc đánh giá coverage CI của Preply. Vì vậy phần so sánh Preply chỉ nói về những gì methodology công bố; không khẳng định implementation hiện tại ngoài các chi tiết đó.
