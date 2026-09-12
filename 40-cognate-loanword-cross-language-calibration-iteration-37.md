# Iteration 37 — Cognate/loanword effects and cross-language calibration

## Phạm vi và direction

Iteration này kiểm tra một nguồn sai lệch đặc thù của vocabulary-size test: người học có L1 gần với tiếng Anh, hoặc đã tiếp xúc với loanword tiếng Anh trong L1, có thể trả lời item dễ hơn dù frequency, độ dài và format tương đương. Direction được tách khỏi fairness/DIF tổng quát bằng cách tập trung vào cơ chế cognate/loanword, matched anchors và item-bank adaptation theo L1.

Kết luận vận hành: cognate/loanword status phải là metadata và facet calibration trong item bank; không được dùng một hệ số trừ điểm chung cho mọi L1.

## Nguồn đã fetch và kiểm tra

1. Jordan, E. (2012), *Cognates in Vocabulary Size Testing — a Distorting Influence?*, Language Testing in Asia, DOI 10.1186/2229-0443-2-3-5. Bản HTML qua URL proxy HTTP 200, nội dung hiển thị abstract và thông tin bài báo: [bản đã fetch](https://r.jina.ai/https://languagetestingasia.springeropen.com/articles/10.1186/2229-0443-2-3-5).
2. Laufer, B. & McLean, S. (2016), *Loanwords and Vocabulary Size Test Scores: A Case of Different Estimates for Different L1 Learners*, Language Assessment Quarterly. Bản ghi ERIC qua URL proxy HTTP 200, có abstract do tác giả cung cấp: [ERIC record đã fetch](https://r.jina.ai/https://eric.ed.gov/?id=EJ1112140).
3. Szabo, C. Z. (2016), *Exploring the Mental Lexicon of the Multilingual: Vocabulary Size, Cognate Recognition and Lexical Access in the L1, L2 and L3*, Eurasian Journal of Applied Linguistics, 2(2), 1–25. Trang journal HTTP 200: [journal page](https://dergipark.org.tr/en/pub/ejal/article/461007). PDF toàn văn HTTP 200: [article PDF](https://dergipark.org.tr/en/download/article-file/537381).
4. Preply, *How it works*. Bản phương pháp qua proxy HTTP 200 được dùng trong các iteration trước: [methodology](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works). Direct production item bank/response data của Preply vẫn chưa truy cập được.

## Bằng chứng chính

### 1. Cognate làm thay đổi facility bên trong các frequency band

Jordan báo cáo pilot với 60 sinh viên đại học Nhật học tiếng Anh. Bài dùng các item dịch Nhật–Anh trong ba dải 1.000 từ và so sánh cognate với noncognate. Cognate được trả lời đúng nhiều hơn có ý nghĩa thống kê ở dải 2.000 và 3.000 từ; ở dải 1.000 từ, khác biệt không có ý nghĩa thống kê. Bài kết luận tỷ lệ cognate trong test phải đại diện cho tỷ lệ của frequency band đã lấy mẫu, và đề xuất stratified item sampling.

Hệ quả: một band không phải là stratum đồng nhất nếu L1 composition của sample thay đổi hoặc tỷ lệ cognate bị lệch. Hai form có cùng frequency quota nhưng khác tỷ lệ cognate có thể có score khác nhau mà không phản ánh chênh lệch breadth. Frequency vẫn là biến thiết kế cần thiết, nhưng phải đi kèm cognate/L1 facet.

### 2. Loanword có thể làm phồng score, và mức phồng phụ thuộc L1

Bản ghi ERIC của Laufer–McLean mô tả ba test được xây trên BNC/COCA, đo 8.000 lemmas hoặc word families bằng 80 item lấy mẫu ngẫu nhiên. Trong form gốc có 6 loanword đối với nhóm Hebrew và 13 loanword đối với nhóm Japanese; các loanword được thay bằng non-loanword cùng frequency để tạo so sánh within-subject. Ba modality là word-form recall, word-form recognition và word-meaning recall.

Kết quả được abstract báo cáo: form có loanword cho score cao hơn có ý nghĩa ở cả hai nhóm L1, trên tất cả modality và phần lớn proficiency group; người ít khả năng hưởng lợi nhiều hơn. Loanword cũng ảnh hưởng khác nhau đến estimate của hai L1. Vì vậy không có cơ sở để áp dụng `estimate_corrected = estimate - universal_constant` hoặc cùng một tỷ lệ giảm cho mọi người dùng.

### 3. Item-bank manifest phải ghi cognate theo từng L1

Szabo nghiên cứu 54 người bản ngữ Hungary sống ở Romania, dùng Romanian như L2 và English như L3. English form được rút còn 70 item, phân bố đều trên 14 frequency levels. Tác giả thay ba item problematic/false-cognate, kiểm tra cognateness theo Hungarian và Romanian, đồng thời ghi syllable length và part of speech.

Tác giả tạo các form đa ngôn ngữ có số cognate cân bằng theo thiết kế. Tổng ba test có 56% item là cognate; bài nhấn mạnh tỷ lệ này không đại diện tỷ lệ cognate trong ngôn ngữ thực, mà phản ánh phân bố của original VST và các ràng buộc chọn item. Đây là cảnh báo quan trọng: cân bằng experimental không đồng nghĩa với đại diện population; manifest phải lưu cả `cognate_sampling_policy` và nguồn tỷ lệ mục tiêu.

Các trường tối thiểu nên có:

```text
item_id
frequency_frame_version
frequency_band
lexical_unit             # headword/lemma/word-family
part_of_speech
sense_id
syllable_or_orthographic_length
cognate_status[L1]       # cognate / noncognate / false-cognate / uncertain
loanword_status[L1]
source_language[L1]
translation_equivalence[L1]
anchor_group
```

### 4. Cross-language score link cần common-person/common-item, không chỉ raw percentage

Trong Szabo, điểm English và Romanian tương quan `r=.592` (p<.001, N=54); chỉ điểm cognate tương quan `r=.629`. Nghiên cứu cũng có một nhóm 22 người nhận hoạt động nâng cao nhận biết cognate và nhóm kiểm soát 32 người. Chênh lệch English score giữa hai nhóm không có ý nghĩa (`t(38.04)=-0.76`, p>.05). Bài ghi nhận test được làm theo thứ tự cố định, không counterbalance language/item, nên order effect là hạn chế.

Điều này không tạo ra hệ số chuyển English↔Romanian phổ quát. Nó chỉ hỗ trợ việc thu thập L1 background, cognate exposure và matched forms trong calibration. Việc không thấy intervention effect trong mẫu này cũng không chứng minh cognate effect luôn không đổi; sample, proficiency và modality vẫn là điều kiện của kết quả.

## Quy tắc cập nhật thuật toán đề xuất

### Estimand

Giữ `breadth_estimate` là số lexical units theo vocabulary universe đã công bố. Không trừ cognate trực tiếp khỏi số từ biết: nếu người học thực sự biết nghĩa nhờ transfer, đó vẫn là receptive knowledge theo nhiệm vụ; vấn đề là score không còn so sánh công bằng khi muốn diễn giải như cùng mức exposure/learning effort giữa các L1.

Xuất thêm:

```text
l1_profile
cognate_exposure_profile
raw_breadth_estimate
l1_calibrated_breadth_estimate  # null trước khi có calibration
cognate_sensitivity_range
cross_language_comparability_status
```

### Baseline estimator có stratification mở rộng

Với band `b` và L1 stratum `g`, ký hiệu `N_bg` là số lexical units trong frame, `n_bg` số item được lấy, `x_bgj` response đúng:

```text
p_hat_bg = sum(x_bgj) / n_bg
V_hat_l1 = sum_b sum_g N_bg * p_hat_bg
```

Nếu mục tiêu là estimate cho một target population có phân bố L1 `q_g`, không dùng sample mix tùy tiện. Cần calibration weight hoặc post-stratification:

```text
w_bg = target_share_g / observed_share_g
V_hat_target = sum_b sum_g w_bg * N_bg * p_hat_bg
```

`q_g` và `N_bg` phải được định nghĩa trước; nếu không biết population mix thì báo `raw_sample_estimate` và không đặt nhãn population-universal.

### Pseudocode calibration gate

```text
for each item:
    assign frequency_band and lexical_unit
    annotate cognate_status, loanword_status for each supported L1
    assign matched anchor_group with comparable frequency/POS/sense burden

for each calibration participant:
    collect L1, L2/L3 history, residence, exposure and proficiency
    administer balanced cognate/noncognate anchors
    record response, latency and form/order

fit model:
    response ~ person_ability
             + item_difficulty
             + frequency_band
             + cognate_status[L1]
             + loanword_status[L1]
             + modality
             + person_L1
             + cognate_status[L1]:person_L1
             + anchor/form/order facets

check:
    item fit, DIF conditional on ability,
    common-person/common-item linking,
    held-out calibration error by L1 and proficiency,
    score reliability and interval coverage

if L1 interaction is not stable or held-out coverage fails:
    publish raw estimate + cognate_sensitivity_range
    set l1_calibrated_breadth_estimate = null
else:
    publish linked L1 estimate with uncertainty and calibration version
```

Một model có interaction không nên được coi là production correction chỉ vì p-value nhỏ; cần kiểm tra độ ổn định, effect size, item coverage, subgroup sample size và out-of-sample calibration.

## So sánh với Preply

| Thành phần | Preply đã công bố | Quy tắc đề xuất sau iteration 37 |
|---|---|---|
| Vocabulary universe | Dictionary có hơn 45.000 entries; derived-form counts được gộp về dictionary headwords | Giữ unit/headword hoặc đổi sang lemma/word-family nhưng phải công bố riêng; không trộn scale |
| Frequency | BNC-derived, spoken/written mixture; sample rank logarithmic theo methodology vendor | Version hóa corpus/frame và thêm cognate/loanword facet theo L1 |
| Sampling | Khoảng 40 item thăm dò và khoảng 120 item trong vùng frequency hẹp; exact production bank chưa xác minh | Stratify tối thiểu theo band × L1-relevant item facet; giữ common anchors và matched pairs |
| Cognate handling | Methodology đã fetch nói có loại cognate/false-friend cho Portuguese learner test và loại một số item problematic; tỷ lệ/logic cho mọi L1 và live bank chưa xác minh độc lập | Metadata `cognate_status[L1]`, `loanword_status[L1]`, false-cognate và uncertainty; không correction universal |
| Score | Vendor nêu midpoint và khoảng ±10% theo model nội bộ | Tách raw midpoint, design/measurement CI và cognate sensitivity; chỉ phát hành L1-calibrated score sau hold-out |
| Cross-form/group comparison | Không có response-level production data hoặc public common-anchor calibration để kiểm tra | Common-person/common-item linking; báo comparability status và không map sang L1 khác khi thiếu calibration |

## Validation plan

1. **Item annotation audit:** hai annotator độc lập gắn cognate/loanword/false-cognate cho từng L1; adjudication và lưu uncertainty/ambiguous flag.
2. **Balanced calibration sample:** mỗi L1 mục tiêu có đủ nhóm proficiency; trong từng frequency band ghép cognate và noncognate theo frequency, POS, length, sense và distractor burden.
3. **Common-person/common-item design:** cùng người làm các matched forms; anchor không được dùng như item exposure tự do trong production.
4. **Model comparison:** so sánh raw stratified estimator, Rasch/1PL có L1 item facet, và model có cognate×L1 interaction. Kiểm tra item fit, DIF, targeting và local dependence.
5. **Held-out validation:** khóa item/form; đánh giá bias, MAE, interval coverage và subgroup calibration theo L1/proficiency. Không dùng cùng data để vừa ước lượng correction vừa xác nhận correction.
6. **Sensitivity output:** nếu calibration chưa ổn định, giữ score raw và xuất range khi loại/giữ cognate hoặc loanword; không âm thầm sửa điểm.
7. **Drift audit:** khi corpus/dictionary hoặc cognate lexicon đổi version, re-run linking và so sánh anchor difficulty; version cũ và mới không được so trực tiếp nếu chưa equate.

## Gaps

- Chưa có item bank và response-level production data của Preply để biết tỷ lệ cognate/loanword theo từng L1, routing probability, item exposure và effect thực tế trên midpoint.
- Chưa có hệ số universal để hiệu chỉnh cognate/loanword; không được bịa hoặc chuyển 4–16% từ search snippet/secondary source thành production constant.
- Bằng chứng Jordan là Japanese–English translation pilot; Laufer–McLean là Hebrew/Japanese với các modality và frame cụ thể; Szabo là Hungarian–Romanian–English sample. Không được suy rộng trực tiếp sang mọi L1, mọi format hoặc mọi vocabulary universe.
- Chưa xác minh được tỷ lệ cognate mục tiêu của các nhóm người dùng sản phẩm. Nếu không có target population mix, chỉ nên báo sample-conditioned estimate và sensitivity.

## Trạng thái

Iteration này thêm 5 JSONL records vào state, gồm 4 finding và 1 gap. Artifact này là phần bổ sung theo iteration; báo cáo cuối vẫn cần tích hợp/kiểm chứng với item bank, pilot response data và hold-out calibration của sản phẩm.
