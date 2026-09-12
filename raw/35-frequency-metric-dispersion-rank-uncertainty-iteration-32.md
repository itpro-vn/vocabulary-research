# Iteration 32 — Frequency metric, contextual diversity và bất định của rank

## 1. Phạm vi và direction

Direction của iteration này là **frequency-metric robustness and lexical difficulty**: không chỉ hỏi “từ xuất hiện bao nhiêu lần”, mà kiểm tra cách corpus design, register, contextual diversity, log transformation, cutoff và precision làm thay đổi frequency band và thứ hạng item.

Iteration này không thay thế estimand breadth đã chốt ở các iteration trước. Nó bổ sung một lớp provenance và sensitivity cho frequency axis.

## 2. Nguồn đã fetch và kiểm tra

| Nguồn | HTTP khi kiểm tra | Vai trò |
|---|---:|---|
| Oxford, *About the British National Corpus* | 200 | Corpus size, written/spoken composition, sampling và metadata |
| Soares et al., *SUBTLEX-PT* PDF, University of Valencia | 200 | Raw frequency, contextual diversity, register-specific validation và Zipf |
| `rspeer/wordfreq` README trên `raw.githubusercontent.com` | 200 | Ví dụ triển khai frequency database: snapshot, nhiều nguồn, cutoff và binning |
| Preply methodology qua `r.jina.ai` | 200 | Đối chiếu pipeline công bố; endpoint Preply trực tiếp trả 403 trong lần kiểm tra |

Search snippets chỉ được dùng để tìm lead; các URL trên đều được fetch thực tế. Không dùng số liệu từ snippet làm finding.

## 3. Bằng chứng chính

### 3.1. Frequency rank là thuộc tính của corpus design, không phải thuộc tính tuyệt đối của từ

Trang chính thức của Oxford mô tả BNC1994 là corpus 100 triệu từ gồm khoảng 90% văn viết và 10% văn nói. Phần viết lấy các mẫu tối đa 45.000 từ từ nhiều nguồn; phần nói gồm hội thoại không chuẩn bị và nhiều bối cảnh từ họp, radio đến phone-in, với lựa chọn người nói có cân bằng nhân khẩu học. Corpus cũng có metadata về phân loại và bối cảnh của từng văn bản.

Hệ quả cho vocabulary-size test:

- cùng một headword có thể đổi rank khi thay tỷ trọng spoken/written, thời kỳ, genre hoặc quần thể văn bản;
- một count tổng không đủ để tái lập rank nếu không biết sampling frame, tokenization và weight;
- frequency list phải lưu provenance và metadata, không chỉ lưu `rank`.

Nguồn: <https://www.natcorp.ox.ac.uk/corpus/>.

### 3.2. Contextual diversity là covariate có thể bổ sung cho raw frequency

Soares et al. xây dựng SUBTLEX-PT từ 78.019.765 từ trong 17.496 phim/chương trình TV; database cung cấp cả raw frequency và contextual diversity (CD). CD được định nghĩa là số tài liệu/phim mà một từ xuất hiện. Trong kiểm định gồm 1.920 từ và 1.920 nonword, subtitle database giải thích nhiều phương sai hơn database tần suất từ văn viết; trong kết quả tóm tắt, CD giải thích khoảng 2% phương sai đọc nhiều hơn raw subtitle frequency trong bộ dữ liệu đó.

Đây là bằng chứng psycholinguistic trên tiếng Bồ Đào Nha và task lexical decision/reading, không phải calibration coefficient cho vocabulary-size tiếng Anh. Vì vậy production rule an toàn là:

1. lưu CD hoặc một dispersion measure tương đương khi xây bank;
2. dùng CD để QA và/hoặc làm covariate kiểm tra item difficulty;
3. không thay raw frequency bằng CD một cách mặc định;
4. phải kiểm định lại theo ngôn ngữ, register, population và construct của bài test.

Nguồn: <https://www.uv.es/mperea/SUBTLEX-PT.pdf>, pp. 3 và 7 trong text extraction.

### 3.3. Zipf là biến đổi hiển thị, không loại bỏ sai số ở tail

SUBTLEX-PT mô tả Zipf là logarithm 7-point của frequency. README wordfreq nêu cụ thể:

\[
Z(w) = \log_{10}\left(\frac{\text{occurrences}(w)}{10^9\ \text{tokens}}\right)
\]

Theo README, Zipf 6 tương ứng khoảng 1 lần trên 1.000 từ, còn Zipf 3 khoảng 1 lần trên 1.000.000 từ. Scale log giúp biểu diễn dải frequency rộng hơn và dễ đọc hơn, nhưng không biến một count tail ít quan sát thành một rank chắc chắn. Một vài token thêm/bớt có thể làm thay đổi mạnh rate và thứ tự ở vùng hiếm.

Do đó item manifest cần giữ đồng thời:

- `raw_count`, `corpus_tokens`, `rate_per_million`;
- `zipf` chỉ như biến đổi thuận tiện;
- khoảng bất định hoặc cờ low-count;
- tie/rank interval nếu nhiều item có count gần nhau.

Nguồn: <https://raw.githubusercontent.com/rspeer/wordfreq/master/README.md> và <https://www.uv.es/mperea/SUBTLEX-PT.pdf>.

### 3.4. Frequency bank cần version, cutoff và policy về precision

README wordfreq ghi rõ dữ liệu là snapshot của usage khoảng tới năm 2021, tổng hợp từ nhiều nguồn chứ không phải một corpus đơn. Nó có wordlist `small` và `large` với cutoff khác nhau; frequency được gom vào các bin Zipf làm tròn đến 0,01 để tránh lưu precision giả.

Đây là một ví dụ triển khai, không phải chuẩn psychometric bắt buộc. Giá trị của bằng chứng nằm ở nguyên tắc reproducibility:

- frequency data phải có snapshot date và danh sách nguồn;
- cutoff “không xuất hiện” phải phân biệt với frequency bằng 0;
- decimal precision không được trình bày như measurement accuracy;
- cập nhật corpus phải tạo drift report, không âm thầm thay band membership;
- score cũ cần giữ `bank_version` để so sánh theo thời gian.

Nguồn: <https://raw.githubusercontent.com/rspeer/wordfreq/master/README.md>.

## 4. Quy tắc thuật toán được đề xuất

### 4.1. Frequency manifest

Mỗi lexical unit trong bank nên có tối thiểu:

```text
unit_id, lexical_unit_type, headword_or_lemma,
corpus_id, corpus_version, snapshot_date,
token_count, corpus_token_total, rate_per_million,
zipf, document_count, document_total,
genre_counts, register_weights, rank_interval,
low_count_flag, dictionary_mapping_version
```

`lexical_unit_type` vẫn phải là estimand đã chọn (dictionary headword, lemma hoặc word family). Không trộn các unit type chỉ vì chúng có cùng spelling.

### 4.2. Rank và band assignment có sensitivity

Không gán band từ một rank duy nhất. Với mỗi item, tạo ít nhất các phiên bản:

- `rank_main`: corpus chính với weights đã khóa;
- `rank_spoken`: spoken-only hoặc spoken-heavy;
- `rank_written`: written-only hoặc written-heavy;
- `rank_cd_adjusted`: chỉ nếu pilot chứng minh CD cải thiện item model, không phải để thay score breadth.

Một item được gắn `band_uncertain=true` nếu nó đổi band dưới một perturbation hợp lý hoặc có low count. Item vẫn có thể dùng cho test, nhưng:

- không dùng nó làm anchor duy nhất;
- thêm uncertainty component do band/rank;
- báo sensitivity khi score được tính trên các manifest khác nhau.

### 4.3. Pseudocode

```text
build_manifest(corpus_snapshot, dictionary, weights):
    tokenize_and_tag(corpus_snapshot)
    for unit in dictionary.units:
        counts = aggregate_derived_forms(unit, corpus_snapshot, dictionary)
        token_count = weighted_sum(counts, weights)
        doc_count = count_documents_with_unit(unit)
        rate = token_count / weighted_corpus_tokens * 1_000_000
        zipf = log10(max(token_count, lower_bound) /
                     (weighted_corpus_tokens / 1_000_000_000))
        store_raw_and_metadata(unit, token_count, rate, zipf, doc_count)
    rank_main = rank_by(token_count, tie_policy="interval")
    for perturbation in [spoken_heavy, written_heavy, corpus_subsample_1,
                         corpus_subsample_2]:
        rank_alt[perturbation] = rerank_same_units(perturbation)
    for unit:
        band_uncertain = band(rank_main[unit]) !=
                         all_or_majority_bands(rank_alt[*][unit])
        low_count = token_count[unit] < preregistered_count_floor
    return manifest_with_versions_and_flags

estimate(test_responses, manifest):
    fit_breadth_model_using(rank_main, lexical_unit_type)
    propagate_response_and_sampling_uncertainty()
    propagate_rank_sensitivity_by_refitting_on(rank_alt)
    return K_hat, CI_response_sampling, rank_sensitivity_range,
           endpoint_status, bank_version
```

## 5. Công thức và uncertainty

Điểm breadth chính vẫn được ước lượng trên universe đã định nghĩa, không trên Zipf trực tiếp. Gọi `K_hat(v)` là estimate tại version `v` của manifest. Báo cáo nên có:

\[
CI_{total} = CI_{response/sampling} + sensitivity_{rank/corpus}
\]

Trong triển khai nên giữ hai thành phần tách riêng thay vì cộng độ rộng một cách tùy tiện:

- `CI_response_sampling`: từ response model, stratified sampling hoặc confidence sequence đã calibration;
- `rank_sensitivity_range = [min_v K_hat(v), max_v K_hat(v)]` trên các manifest/weights được định trước;
- `construct_or_mapping_uncertainty`: vẫn tách riêng như các iteration trước.

Nếu cần một scalar để hiển thị, dùng union interval hoặc bootstrap nested đã được pilot kiểm tra coverage; không gọi khoảng rank sensitivity là CI frequentist.

Một rule bảo thủ:

```text
if rank_sensitivity_range_width > preregistered_tolerance:
    status += "frequency-sensitive"
    do not claim precise band-level mastery
if low_count_item_fraction is high:
    status += "tail-low-information"
    expand tail or censor estimate
```

Các tolerance, count floor và cách combine phải được pilot-calibrate; chưa có bằng chứng để điền một giá trị phổ quát cho Preply.

## 6. Đối chiếu với Preply

| Thành phần | Preply công bố | Thiết kế đề xuất |
|---|---|---|
| Corpus | BNC; tái cân bằng 1/3 demographic spoken, 1/3 context-governed spoken, 1/3 written | Giữ corpus/version/weights như manifest và thử sensitivity theo register |
| Unit | Dictionary main entries; derived forms cộng về headword và subentries loại | Giữ lexical-unit type công khai và mapping version; không đổi estimand khi đổi frequency metric |
| Frequency | Xếp dictionary entries theo frequency sau cleaning | Lưu raw counts, document counts, rate, Zipf, rank interval và low-count flag |
| Dispersion/CD | Trang methodology không công bố document-frequency metric hoặc rank uncertainty | Lưu CD/dispersion để QA/covariate; chỉ dùng vào item model sau validation |
| Sampling | Hai bước, khoảng 40 item thăm dò rồi khoảng 120 item vùng hẹp; sample log-rank | Có thể giữ staged design, nhưng item selection phải xem band/rank uncertainty và anchor exposure |
| Uncertainty | Trang công bố margin of error của sản phẩm; chưa xác minh được empirical rank sensitivity | Báo riêng response CI, rank sensitivity, construct/mapping uncertainty; calibration bằng hold-out |
| Version drift | Chưa thấy công bố snapshot/update protocol trong trang methodology được fetch | Bắt buộc `bank_version`, snapshot date, drift audit và backward-compatible score linking |

Nguồn Preply đã fetch qua proxy: <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works>. Endpoint trực tiếp <https://preply.com/en/learn/english/test-your-vocab/how-it-works> trả 403 trong lần kiểm tra; vì vậy production dispersion metric, rank SE và update protocol của Preply vẫn là gap.

## 7. Validation plan bổ sung

1. **Corpus perturbation:** tạo spoken-heavy, written-heavy và genre-balanced manifests; đo tỷ lệ item đổi band và độ rộng `rank_sensitivity_range`.
2. **Subsample stability:** bootstrap theo document, không chỉ theo token, để kiểm tra tail rank và CD stability.
3. **Item model:** fit model có và không có CD/dispersion; so sánh absolute fit, cross-validated prediction và DIF theo register/L1 trước khi cho CD ảnh hưởng score.
4. **Common-person/common-item bridge:** cho cùng người làm các forms dùng các frequency manifest khác nhau; nếu K thay đổi chỉ vì manifest, đó là evidence của construct/version sensitivity chứ không phải learning.
5. **Coverage calibration:** kiểm tra CI response coverage và rank-sensitivity coverage riêng trên hold-out; không chuyển kết quả của SUBTLEX-PT hay wordfreq thành hệ số tiếng Anh/Preply.
6. **Release gate:** chỉ phát hành manifest mới khi raw counts, metadata, rank changes, item exposure và score linking report được lưu cùng version.

## 8. Gaps còn lại

- Chưa có item bank và response-level data sản xuất của Preply để ước lượng rank sensitivity thực tế, item difficulty, CD effect hoặc coverage của interval.
- Chưa tìm được nguồn xác thực cho document-count/dispersion metric, rank uncertainty, count floor và update schedule riêng của Preply.
- SUBTLEX-PT là nghiên cứu tiếng Bồ Đào Nha và task lexical processing; không được dùng như numeric prior cho vocabulary-size tiếng Anh.
- Cần pilot tiếng Anh có corpus/register metadata và hold-out item response trước khi cho CD hoặc rank sensitivity ảnh hưởng điểm số.
