# Iteration 17 — Corpus-version drift và domain-coverage calibration

## Phạm vi

Iteration này kiểm tra một rủi ro riêng của vocabulary-size estimator: frequency rank không phải thuộc tính cố định của từ. Rank phụ thuộc vào corpus, tỷ trọng spoken/written, domain/register, dictionary filtering, lexical-unit rule và version của danh sách. Nếu các thành phần này đổi mà không version hóa, hai lần chạy có thể cho cùng một câu trả lời nhưng ra hai vocabulary-size khác nhau.

Direction được chọn khác các iteration trước: tập trung vào provenance/version drift của corpus và domain coverage, không vào missingness, IRT, validity, distractor hay common-item equating.

## Nguồn đã fetch và kiểm tra

| Nguồn | HTTP kiểm tra | Cách lấy dữ liệu | Vai trò |
|---|---:|---|---|
| Preply, “How the vocab test works” qua `r.jina.ai` | 200 | `curl -sL -A "Mozilla/5.0"` | Mô tả pipeline corpus–dictionary–ranking và sampling của sản phẩm tham chiếu |
| Dang (2020), *ELT Journal*, accepted manuscript tại White Rose | 200 | PDF tải trực tiếp, trích xuất bằng `pypdf` | Bằng chứng domain coverage và cấu trúc band test |
| Rayson & Garside, *Comparing Corpora using Frequency Profiling* | 200 | PDF tải trực tiếp, trích xuất bằng `pypdf` | Bằng chứng về representativeness, comparability và drift audit |
| EAP Foundation, BNC/COCA lists | 200 | HTML tải trực tiếp, loại script/style | Mô tả công khai về band/list/version; nguồn thứ cấp nên không thay thế primary dataset |

Endpoint Preply trực tiếp trả 403 trong môi trường này; URL proxy ở trên trả nội dung có `URL Source` là trang Preply và được dùng đúng cho các claim mô tả phương pháp, không dùng để khẳng định dữ liệu production chưa công khai.

## Findings chi tiết

### 1. Preply có pipeline tái cân bằng corpus và gộp derived forms

Preply mô tả các bước sau:

1. Chọn British National Corpus vì có thành phần spoken lớn.
2. Dùng một từ điển Anh có thẩm quyền.
3. Lấy tần suất các từ.
4. Tái cân bằng thành ba phần bằng nhau: spoken demographic (conversation), spoken context-governed (meetings/lectures), written.
5. Cộng tần suất của derived forms vào headword theo guidance của từ điển rồi loại derived forms.
6. Loại các mục không có trong từ điển.
7. Xếp các dictionary-matched entries theo tần suất giảm dần.

Trang này nói từ điển có khoảng 70.000 headwords nhưng chỉ khoảng 45.000 xuất hiện trong BNC 100 triệu từ. Con số 45.000 vì vậy là kích thước của một universe sau lọc corpus–dictionary, không phải số lượng headword của từ điển.

**Hệ quả:** report và runtime manifest phải lưu `corpus_id`, `corpus_version`, số token mỗi domain, trọng số rebalance, `dictionary_id`/edition, derived-form policy, filter counts và final universe size. Không được coi “rank 15.000” là một scale có nghĩa nếu thiếu manifest này.

Nguồn: <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works>

### 2. Sampling Preply gần logarithmic nhưng bộ lọc thủ công làm thay đổi xác suất inclusion

Preply mô tả hai giai đoạn: khoảng 40 từ trải từ dễ đến khó để định vị, sau đó khoảng 120 từ trong vùng hẹp hơn; các mẫu trong vùng này nằm gần đều theo khoảng cách logarithmic của frequency rank. Preply cũng loại các mục có nghĩa dễ suy ra, dễ nhầm về hình thức, quá địa phương/slang/chuyên ngành/archaic, ít dùng độc lập, hoặc cognate/false friend với tiếng Bồ Đào Nha.

Các quy tắc này có thể tăng construct validity cho receptive vocabulary của nhóm mục tiêu, nhưng làm sample không còn tương đương với “lấy đều mọi rank”. Việc lấy “từ đầu tiên hợp lệ” sau mỗi vị trí logarithmic có thể tạo inclusion probability phụ thuộc vào mật độ item hợp lệ quanh rank đó. Chính trang Preply cảnh báo rằng lựa chọn cá nhân khi bỏ qua item có thể làm lệch kết quả ở một số mức.

**Quy tắc triển khai:**

- Item manifest có `candidate_rank`, `final_rank`, `included`, `exclusion_reason`, `cognate_policy`, `domain_tags`, `lexical_unit_version`.
- Nếu dùng design-based estimator, tính hoặc mô phỏng `pi_i` sau bước lọc; không gán `pi_i = 1/n` theo thói quen.
- Nếu chưa ước lượng được `pi_i`, chạy sensitivity với ít nhất bộ lọc chặt và bộ lọc rộng, rồi báo chênh lệch như construct uncertainty.
- Tách “vocab breadth theo general English” khỏi “vocab hữu ích cho người nói tiếng mẹ đẻ/target domain”; không trộn hai claim trong một con số.

Nguồn: <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works>

### 3. BNC/COCA là list có purpose và lexical-unit definition cụ thể

Trang EAP Foundation mô tả BNC/COCA lists theo band 1.000 từ, từ 1k đến 25k. Theo trang này, 1k và 2k được xây từ corpus 10 triệu từ gồm 6 triệu spoken English Anh-Anh/Mỹ (kể cả film/TV) và 4 triệu written English; từ 3k trở đi dùng ranking BNC và COCA sau khi loại 1k/2k. Trang cũng mô tả word family đến Bauer–Nation level 6, phù hợp hơn với receptive reading/listening so với productive writing/speaking.

Trang cho biết version 2.0.0 có tổ chức lại một số family members và thêm frequency information từ BNC 100 triệu từ. Điều này cho thấy version change có thể đổi membership/band, không chỉ đổi metadata.

**Hệ quả:**

- Chốt `estimand_unit` trước khi viết scoring: `headword`, `lemma`, `flemma` hoặc `word_family_level_6`.
- Lưu hash của danh sách và bảng mapping form → lexical unit; không dùng tên “1k”/“2k” đủ làm định danh.
- Khi đổi list version, chạy common-item rank comparison và re-calibration; không so sánh raw scores giữa version cũ/mới như cùng một scale.
- BNC/COCA page là nguồn mô tả thứ cấp, dù URL đã trả HTTP 200. Cần primary dataset/documentation của Nation/BNC/COCA cho production release; **chưa tìm được nguồn xác thực độc lập cho một hệ số chuyển đổi chung giữa BNC/COCA word-family và Preply headword scale**.

Nguồn: <https://www.eapfoundation.com/vocab/general/bnccoca/>

### 4. Một band frequency cố định có coverage khác nhau theo domain

Dang (2020) dùng BNC/COCA2000 để phân tích một academic spoken corpus và một academic written corpus, mỗi corpus trên 13 triệu từ và chia thành bốn nhóm ngành. BNC/COCA2000 chiếm 88,61% token trong academic spoken corpus nhưng 76,39% token trong academic written corpus.

Đây không phải bằng chứng để thay 88,61%/76,39% vào mọi sản phẩm: chúng thuộc hai corpus học thuật cụ thể. Nhưng nó chứng minh rằng cùng một high-frequency list có thể có coverage rất khác khi register/domain đổi.

**Quy tắc báo cáo:**

- General estimate: trọng số theo corpus target đã công bố.
- Domain profile: `coverage_d,b = tokens in domain d covered by band b / total tokens in d`.
- Nếu user chọn domain (academic speech, academic writing, conversation…), báo thêm profile đó, không sửa ngầm general estimate.
- Chênh lệch giữa domain profile và corpus dùng để tạo rank là `transport/coverage uncertainty`, không gộp vào CI sampling của người làm test.

Nguồn: <https://eprints.whiterose.ac.uk/id/eprint/152672/1/Dang+_in+press__ELT.pdf>

### 5. Band-level receptive test không tự động là tổng vocabulary

Trong nghiên cứu Dang, Updated Vocabulary Levels Test có level 1.000 và 2.000 đo receptive knowledge của các band đầu; mỗi level có 10 clusters, mỗi cluster 6 từ và 3 định nghĩa; mastery được đặt ở ít nhất 29/30. Nghiên cứu trên 66 sinh viên EAP tại Việt Nam báo dưới một phần năm master 2.000 từ và hơn 20% chưa master 1.000 từ.

Tác giả nhấn mạnh format chỉ đo matching form–meaning receptive, không đo đầy đủ collocation, biến hình, hay dùng trong ngữ cảnh. Vì thế, một ngưỡng band như 29/30 là criterion cho mastery của section cụ thể, không phải phép biến đổi phổ quát sang word count hoặc productive vocabulary.

**Hệ quả:** sản phẩm nên trả riêng:

```text
band_mastery[b]       # chỉ khi n_b đủ và criterion đã calibration
breadth_estimate      # tổng theo estimand đã định nghĩa
coverage_profile[d,b] # khả năng phủ token theo domain
```

Không dùng `29/30 × 1000` nếu test format, lexical unit, population hoặc band definition khác Updated VLT.

Nguồn: <https://eprints.whiterose.ac.uk/id/eprint/152672/1/Dang+_in+press__ELT.pdf>

### 6. Corpus chuẩn phải được đánh giá representativeness, không chỉ bằng tổng token

Rayson và Garside nêu bốn vấn đề khi so sánh corpora: representativeness, homogeneity, comparability và độ tin cậy của statistical tests theo kích thước corpus. Corpus normative nên có các loại văn bản chính và, nếu có thể, tỷ lệ phù hợp với ngôn ngữ đời thường; các corpus đem so sánh nên được xây dựng bằng cùng stratified sampling và randomised selection nếu có thể.

**Áp dụng cho frequency universe:** corpus manifest phải có bảng theo `domain × register × mode × time × source`, gồm token count, document count, unique lexical units và weight. Một corpus rất lớn nhưng thiếu conversation hoặc quá lệch written vẫn có thể cho rank không phù hợp target use.

Nguồn: <https://ucrel.lancs.ac.uk/people/paul/publications/rg_acl2000.pdf>

### 7. Drift audit nên dùng counts và effect size, không chỉ p-value

Rayson và Garside ghi nhận chi-square có thể không đáng tin khi expected frequency dưới 5 và có thể phóng đại khác biệt khi so sánh corpus nhỏ với corpus lớn; phương pháp của họ dùng log-likelihood ratio trong frequency profiling.

Điều này phù hợp làm QA cho corpus update, không phải công thức trực tiếp để chấm vocabulary test. Drift report nên gồm:

- token-count change theo domain và lexical unit;
- log-likelihood hoặc phương pháp count-aware tương thích với dữ liệu thưa;
- absolute/relative frequency change;
- rank displacement và số item đổi band;
- coverage delta trên các domain target;
- danh sách item đổi lexical unit hoặc bị dictionary filter.

Không nên đánh dấu “frequency drift” chỉ vì một p-value nhỏ trong corpus cực lớn; cũng không nên bỏ qua thay đổi có effect size lớn nhưng test không có power ở vùng hiếm.

Nguồn: <https://ucrel.lancs.ac.uk/people/paul/publications/rg_acl2000.pdf>

## Thuật toán đề xuất bổ sung: versioned corpus + domain profile

### Manifest bắt buộc

```text
CorpusManifest {
  corpus_id, corpus_version, retrieval_date, license,
  domains: [{id, register, mode, source_count, token_count, weight}],
  tokenization_version, lemmatizer_version,
  lexical_unit_policy, dictionary_id, dictionary_version,
  inclusion_filters, excluded_categories,
  frequency_count_method, final_universe_hash
}
```

### Xây rank list

```text
build_universe(manifest):
    for each document in corpus snapshot:
        tokenize with pinned tokenizer
        map forms to lexical units with pinned mapping
        count tokens per domain and lexical unit
    normalize counts inside each domain
    apply pre-registered domain weights w_d
    combined_count[u] = sum_d w_d * normalized_count[d,u]
    add derived-form counts only if lexical_unit_policy says so
    filter by versioned dictionary and exclusion rules
    sort descending by combined_count, deterministic tie-break by unit_id
    assign final_rank and frequency_band
    emit manifest + universe hash + domain coverage table
```

### Domain-weighted breadth estimate

Với band/stratum `b`, universe có `N_b` lexical units, mẫu xác suất không đều `pi_i`, và response đã được calibration thành xác suất biết `q_i`, dùng:

```text
p_hat_b = sum(i in sample_b, q_i / pi_i) / sum(i in sample_b, 1 / pi_i)
V_hat_general = sum_b N_b * p_hat_b
```

Nếu cần target domain `d`, dùng `N_{d,b}` hoặc một profile coverage đã định nghĩa trước:

```text
V_hat_d = sum_b N_{d,b} * p_hat_b
coverage_d,b = token_coverage(d, b, corpus_version)
```

Không suy ra `N_{d,b}` từ token coverage nếu một lexical unit có nhiều sense hoặc nhiều derived forms mà mapping chưa được calibration; đó là gap cần pilot.

### Drift gate trước release

```text
if corpus_version_changed or dictionary_version_changed or lexical_unit_policy_changed:
    compare old/new manifests
    compute rank displacement and band migration
    compute coverage_d,b deltas for every target domain
    run common-person/common-item re-calibration
    if scale-link CI or coverage delta exceeds pre-registered threshold:
        create new score scale; do not silently backfill old scores
    else:
        publish linking table and version note
```

Ngưỡng `coverage delta`, rank displacement và CI-linking phải được calibration trên population mục tiêu; hiện chưa có dữ liệu production để đặt số cụ thể.

## So sánh với Preply

| Thành phần | Preply mô tả | Đề xuất production |
|---|---|---|
| Universe | Khoảng 45.000 dictionary main entries có trong BNC | Versioned universe với hash, dictionary edition và final count |
| Corpus | BNC, rebalance 1/3 demographic spoken + 1/3 context spoken + 1/3 written | Manifest domain/register/token, trọng số pre-registered, snapshot bất biến |
| Lexical unit | Headword; derived forms cộng vào headword; main entries, không subentries | Chọn một estimand rõ ràng; lưu mapping form → unit và không trộn scale |
| Sampling | Khoảng 40 định vị + khoảng 120 vùng hẹp, gần logarithmic rank | Stratified/random sampling hoặc lưu `pi_i` sau exclusion; routing phải log |
| Item exclusion | Nghĩa suy ra, nhầm hình thức, local/slang/technical/archaic, cognate/false friend | Manifest lý do loại, pilot DIF/construct và sensitivity bộ lọc |
| Domain claim | General English speech/writing theo rank list | Thêm domain profile; không coi general rank là coverage academic/conversation |
| Version drift | Trang mô tả pipeline nhưng không công khai production snapshot/routing data | Release gate, rank displacement, band migration, common-item linking |
| Uncertainty | Preply mô tả midpoint/log rank; chi tiết production calibration không công khai trong nguồn đã fetch | Tách sampling CI, model uncertainty và coverage/construct transport uncertainty |

## Gap còn lại

- Chưa có item bank, raw counts, exact dictionary edition hoặc snapshot để tái tạo toàn bộ Preply universe.
- Chưa có domain routing/selection probability và response-level production data của Preply.
- Chưa có common-person/common-item calibration giữa Preply headword scale và BNC/COCA word-family/lemma scale; **chưa tìm được nguồn xác thực cho hệ số quy đổi dùng chung**.
- Chưa có target population và domain mix đủ để đặt ngưỡng drift/coverage hoặc chứng minh CI coverage.
- EAP Foundation là nguồn mô tả thứ cấp; primary list documentation cần được thu thập trước khi khóa production item bank.

## Kết luận iteration

Frequency rank chỉ có thể tái lập khi corpus composition, domain weights, dictionary, lexical-unit mapping, filters và version đều bất biến hoặc được ghi lại. Preply đã công khai nhiều quyết định thiết kế hữu ích — rebalance spoken/written, gộp derived forms, lọc dictionary và logarithmic sampling — nhưng chưa đủ dữ liệu để xác minh production snapshot hay calibration. Bản v1 nên giữ estimator stratified đã đề xuất, bổ sung corpus manifest/domain profile và chặn việc so sánh raw score qua version change nếu chưa có linking.
