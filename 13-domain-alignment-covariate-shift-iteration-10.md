# 13. Domain alignment, covariate shift và ước lượng theo target-language-use (Iteration 10)

## 13.1 Direction và câu hỏi

Iteration này tách một vấn đề khác với sampling/IRT thuần túy: một bài test có thể lấy mẫu đúng theo frequency nhưng vẫn không đại diện cho domain mà người làm bài học hoặc sử dụng ngôn ngữ. Câu hỏi là:

1. frequency-only sampling có tổng quát sang curriculum/target-language-use (TLU) domain không;
2. domain overlap có làm thay đổi score không;
3. có thể post-stratify theo domain như thế nào mà không nhầm domain-specific estimate với general vocabulary size;
4. sản phẩm nên chọn coverage theo proficiency/use case ra sao.

## 13.2 Nguồn đã fetch và kiểm tra

- Dudley et al. (2024), *A Context-Aligned Two Thousand Test: Towards estimating high-frequency French vocabulary knowledge for beginner-to-low intermediate learners*: PDF tại White Rose Repository, HTTP 200, 1,335,038 bytes; text layer đã được trích xuất bằng `pypdf`, 34 trang.
  - URL: https://eprints.whiterose.ac.uk/id/eprint/211470/8/dudley-et-al-2024-a-context-aligned-two-thousand-test-toward-estimating-high-frequency-french-vocabulary-knowledge-for.pdf
- *Key Issues and Considerations in Measuring Vocabulary Growth*: PDF ERIC, HTTP 200, 146,399 bytes; text layer đã được trích xuất bằng `pypdf`, 13 trang.
  - URL: https://files.eric.ed.gov/fulltext/EJ1444050.pdf

Hai URL trên được kiểm tra lại bằng HTTP request có browser User-Agent trong iteration này và đều trả 200. Search snippets chỉ được dùng để tìm lead, không dùng làm bằng chứng cuối.

## 13.3 Bằng chứng về domain overlap

Dudley et al. dùng argument-based validation và định nghĩa TLU domain là từ vựng trong chương trình GCSE French của nhóm người học. Trong pilot có 222 học sinh 16 tuổi, trung bình 79,42% item của CA-TTT xuất hiện trên danh sách chương trình; SD = 2,61 điểm phần trăm và 95% CI = [79,07%; 79,77%]. Đây là bằng chứng thực nghiệm rằng domain alignment có thể được operationalize bằng overlap giữa item frame và vocabulary của TLU, thay vì chỉ nói test “có vẻ phù hợp”.

Bài cũng kiểm tra X-Lex trong cùng bối cảnh: trong 40 item thuộc band 1.000 và 2.000, chỉ 25,81% (SD = 2,91%; 95% CI = [25,42%; 26,20%]) xuất hiện trong danh sách GCSE. Với X-Lex, accuracy trung bình của item có trong curriculum là 53,57% (95% CI = [50,63%; 56,52%]), còn item ngoài curriculum là 46,63% (95% CI = [43,97%; 49,29%]). Vì vậy hai test có thể cùng mô tả là frequency-based nhưng đo các sample khác nhau đối với nhóm người học này.

**Hệ quả:** generalization inference phải bao gồm câu hỏi “item sample đại diện cho population nào?”. Nếu mục tiêu là vocabulary trong khóa học, curriculum-aligned score có thể hợp lệ hơn random sample của general corpus. Nếu mục tiêu là general written receptive vocabulary, không được thay general frame bằng curriculum frame rồi vẫn gọi kết quả là tổng số từ biết nói chung.

## 13.4 Post-stratification theo domain

Dudley et al. đưa ra ví dụ điều chỉnh estimate theo membership trong curriculum list. Với một universe high-frequency gồm 2.000 units:

```text
N_on  = 649       # units thuộc domain/curriculum
N_off = 1,351     # units ngoài domain
p_on  = 0.80      # tỷ lệ biết ước lượng từ item trong domain
p_off = 0.50      # tỷ lệ biết ước lượng từ item ngoài domain

V_domain_adjusted = p_on * N_on + p_off * N_off
                   = 0.80 * 649 + 0.50 * 1,351
                   = 1,194.70 units
```

Trong nghiên cứu, phép tính này được dùng để điều chỉnh CA-TTT estimate theo số lượng high-frequency words on/off curriculum. Báo cáo của bài cho thấy raw/unadjusted và adjusted estimate khác nhau đáng kể: unadjusted mean 1.627, SD 285, 95% CI [1.589; 1.664]; adjusted mean 1.480, SD 309, 95% CI [1.439; 1.521] (n = 220 cho bảng điều chỉnh).

Đây là **post-stratification/domain adjustment**, không phải guessing correction. Nó phải được diễn giải như estimate trên một population frame có hai stratum, với `N_on`, `N_off` và quy tắc phân loại được version hóa. Cần tính uncertainty cho cả hai `p_hat` và cho việc xác định membership; không nên chỉ đưa một con số làm tròn.

Một dạng tổng quát hơn cho `J` strata là:

```text
V_hat_domain = Σ_j N_j * p_hat_j

Var(V_hat_domain) ≈ Σ_j N_j² * (1 - n_j/N_j) * s_j² / n_j
```

Nếu item trong mỗi stratum không lấy mẫu ngẫu nhiên, hoặc có nhiều item phụ thuộc cùng một context, thay công thức trên bằng survey-weighted/cluster bootstrap và báo design effect. Nếu domain chỉ là một nhãn do người dùng tự khai, phải coi đó là nguồn uncertainty thêm chứ không xem membership là ground truth.

## 13.5 Frequency không đủ để dự đoán difficulty trong domain

Tổng quan ERIC được kiểm tra trực tiếp ghi nhận rằng frequency chỉ tương quan ở mức vừa phải với teacher ratings về usefulness và difficulty. Một nghiên cứu được tổng quan còn cho thấy phán đoán của giáo viên về các từ học sinh có khả năng biết liên hệ với điểm vocabulary test mạnh hơn frequency. Điều này không phủ nhận frequency: frequency vẫn là trục hữu ích để bảo đảm coverage và hạn chế selection bias. Nhưng nó cho thấy frequency rank không thể là biến duy nhất khi item frame nhắm đến lớp học, nghề nghiệp, kỳ thi hoặc domain chuyên môn.

Metadata nên có tối thiểu:

- `frequency_source` và snapshot/version;
- `domain_id` hoặc danh sách domain membership;
- exposure/usefulness evidence nếu có;
- unit (`headword`, `lemma`, `word_family`);
- item difficulty đã calibration trên population tương ứng;
- cognate/loanword và L1 flags;
- item exposure và form position.

## 13.6 Coverage phải phụ thuộc intended use và proficiency

Tổng quan ERIC phân biệt rõ trade-off giữa vocabulary-size tests và vocabulary-level tests. Size tests phủ rộng khoảng 1.000–14.000 nên có ích hơn cho người trung/cao cấp hoặc người có nhiều exposure ngoài lớp; levels tests có sampling rate cao hơn ở các band đầu nên phù hợp hơn cho beginner/low-intermediate. Đưa các band thấp-frequency vào bài của beginner có thể tăng random guessing và overestimate; ngược lại, bài chỉ phủ đến 5.000 có thể không phát hiện growth ở các band 7.000–9.000 của người học cao hơn.

Vì vậy `band_allocation` phải là policy theo use case:

- **general estimate, unknown population:** rải anchor qua toàn frame, giữ quota tối thiểu mỗi band, không suy ra band mastery từ vài item;
- **beginner/classroom estimate:** ưu tiên band high-frequency và curriculum/TLU frame, chỉ dùng band xa năng lực như diagnostic với cờ uncertainty;
- **advanced/general reading estimate:** mở rộng frame và giữ sample đủ lớn ở middle/low-frequency bands;
- **growth/placement decision:** chọn band quanh ngưỡng hành động nhưng giữ anchor/coverage để không biến score thành estimate cục bộ không thể so sánh.

## 13.7 Quy tắc sản xuất đề xuất

Xuất **hai estimand riêng**:

1. `general_vocab_hat`: estimate trên dictionary/corpus frequency frame đã version hóa; đây là output có thể so sánh giữa form nếu universe, unit và calibration giống nhau.
2. `domain_vocab_hat`: estimate trên TLU/domain frame; lưu `domain_id`, `N_j`, `n_j`, `p_hat_j`, item membership rule và CI riêng.

Không chuyển `domain_vocab_hat` thành “tổng số từ biết” nếu chưa có validation trên domain sử dụng và không trộn nó với `general_vocab_hat` bằng một hệ số cố định.

Pseudocode:

```text
function estimate_by_domain(responses, universe, strata, mode):
    assert universe.version == responses.universe_version
    for stratum in strata:
        items = valid_responses(responses, stratum)
        p_hat[stratum] = mean(item.correct for item in items)
        se[stratum] = finite_population_or_bootstrap_se(items, stratum)

    estimate = sum(stratum.N * p_hat[stratum] for stratum in strata)
    ci = bootstrap_or_design_based_ci(responses, strata)

    result = {
        "estimate": estimate,
        "ci": ci,
        "unit": universe.unit,
        "frame_version": universe.version,
        "strata": [{"id": s.id, "N": s.N, "n": count(s),
                    "p_hat": p_hat[s], "se": se[s]} for s in strata]
    }
    if mode == "domain":
        result["domain_id"] = universe.domain_id
    return result
```

Routing adaptive vẫn có thể chọn item theo uncertainty contribution `N_j² Var(p_hat_j)`, nhưng không được bỏ hẳn strata ngoài domain nếu output đang được gọi là `general_vocab_hat`. Nếu chỉ muốn estimate domain, phải đổi tên output và report rõ frame.

## 13.8 So sánh với Preply reference

Preply methodology trước đây được lưu trong state mô tả dictionary/headword universe và two-stage logarithmic midpoint sampling. Trong iteration này, endpoint methodology qua `r.jina.ai` trả HTTP 403 khi re-check; direct production item bank và response data cũng chưa có. Vì vậy chỉ có thể đối chiếu ở mức đã lưu từ lần fetch trước, không được khẳng định triển khai hiện tại:

| Khía cạnh | Preply methodology đã lưu | Đề xuất sau iteration 10 |
|---|---|---|
| Frame/unit | Dictionary/headword, BNC-derived ranking theo mô tả vendor | Version hóa general frame; domain frame là output riêng, unit công bố rõ |
| Sampling | Broad screening rồi narrow logarithmic midpoint | Stratified/domain sampling; adaptive chỉ tăng thông tin trong strata vẫn giữ estimand |
| Domain | Chưa xác minh production có curriculum/TLU weighting | Lưu domain overlap, `N_j`, `p_hat_j`, CI; post-stratify khi mục tiêu là domain |
| Score | Midpoint rank estimate, vendor claim khoảng ±10% | General và domain estimate tách biệt; CI phải calibration bằng response/item data |
| Validation | Chưa có response-level production evidence trong task | Kiểm tra domain overlap, item difficulty, hold-out TLU criterion và coverage CI |

**Khoảng trống:** chưa tìm được nguồn xác thực cho domain weighting, curriculum adaptation, target-language-use frame hoặc covariate-shift correction trong Preply production. Không được suy ra “Preply không có” chỉ vì methodology không công bố hoặc endpoint bị chặn.

## 13.9 Validation plan bổ sung

1. Chốt population và intended use trước khi chọn frame: general reading, classroom curriculum, placement hay domain nghề nghiệp.
2. Tạo domain manifest có version; tính overlap của candidate items với TLU corpus/list trước khi thu response.
3. Pilot người làm bài đa dạng proficiency; mỗi người làm cả general và domain form với anchors chung.
4. Ước lượng `p_hat_j`, item difficulty, DIF và conditional SE trong từng stratum; kiểm tra local dependence nếu item dùng chung context.
5. So sánh raw general estimate, post-stratified domain estimate và criterion domain outcome; báo bias, MAE/RMSE và 80/95% CI coverage trên hold-out.
6. Kiểm tra sensitivity khi đổi domain list, frequency corpus, unit và exclusion rules.
7. Chỉ phát hành domain-adjusted score sau khi chứng minh nó cải thiện criterion/use-case validity mà không làm hỏng comparability của general scale.
