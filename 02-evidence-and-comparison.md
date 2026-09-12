# 2. Bằng chứng và đối chiếu nguồn

## Nguồn đã kiểm tra

1. **Paul Nation — Vocabulary Size Test information and specifications** (PDF, HTTP 200):
   <https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/vocabulary-tests/the-vocabulary-size-test/Vocabulary-Size-Test-information-and-specifications.pdf>
2. **Coxhead et al. — Measuring the vocabulary size of native speakers of English in New Zealand secondary schools** (PDF, HTTP 200):
   <https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/paul-nations-publications/publications/documents/coxhead-secondary-school-vocab-size.pdf>
3. **Zhang & Zhang (2014) — Validation of an English-Chinese VST** (PDF, HTTP 200):
   <https://ccsenet.org/journal/index.php/ijel/article/download/40678/23318>
4. **Preply — Test Your Vocabulary: The Nitty-Gritty Details**: nội dung được fetch qua URL proxy HTTP 200:
   <https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works>
   Endpoint Preply trực tiếp trả 403 trong môi trường này; production item bank chưa được kiểm tra.

## Findings chính

### 2.1 Nation/Beglar VST

- Bản 14K: 140 câu, 10 câu từ mỗi dải 1.000 word families; tổng điểm ×100.
- Các dải dựa trên word-family lists theo BNC và Bauer/Nation levels. Mục tiêu là phủ các dải mà người làm có thể vượt qua, kể cả phía trên vocabulary size dự kiến.
- Ít item mỗi dải giúp ước lượng tổng size nhưng không đủ để nói chắc mastery từng dải.
- Stem là target + câu đơn giản không định nghĩa; câu nêu POS, thu hẹp sense/homograph và hơi gợi cách dùng. Distractors cùng POS, thường gần cùng band.
- Không có lựa chọn “I don’t know”; tài liệu muốn giữ informed guessing. Không correction guessing; score cần được hiểu là hơi generous.
- Đây là receptive written vocabulary, phù hợp hơn với kiến thức cần cho reading chứ không phải productive fluency.

### 2.2 Phiên bản 20K và validity

Coxhead et al. mô tả bản 20K với 100 item, năm item từ mỗi 1.000-word-family list, raw score ×200. Bài viết dẫn báo cáo Rasch reliability khoảng .96 cho đánh giá 140-item ở Nhật và ghi nhận VST phân biệt các nhóm proficiency. Đây là evidence ủng hộ reliability/construct alignment, không phải giấy phép mặc định cho mọi population, ngôn ngữ mẹ đẻ hay item bank mới.

Bài viết cũng nhấn mạnh word family phù hợp khi mục tiêu là reading: biết base/member và quy tắc word-building có thể hỗ trợ suy ra related forms. Đây là lựa chọn lý thuyết; nếu sản phẩm dùng headword thì phải định nghĩa lại và re-calibrate.

### 2.3 Validation theo frequency band

Bài validation English-Chinese trong nguồn số 3 báo cáo nhóm proficiency khác biệt rõ ở high-frequency items nhưng không có khác biệt post-hoc giữa nhóm ở dải 7K–14K (`P=.25`). Diễn giải hợp lý là low-frequency items nằm dưới sàn của đa số người tham gia. Do đó thuật toán nên có floor/ceiling detection và tránh tuyên bố band score chính xác khi response rate gần 0 hoặc 1.

### 2.4 Preply

Preply mô tả:

- Giai đoạn 1 khoảng 40 từ trải từ dễ đến khó để định vị.
- Giai đoạn 2 khoảng 120 từ trong vùng hẹp hơn, xếp theo frequency, với midpoint nơi số từ không biết ở phía trước cân bằng số từ biết ở phía sau.
- Universe khoảng 45.000 dictionary entries; frequency từ BNC spoken/written, derived counts gộp về headword; loại nhiều từ deducible, quá địa phương/chuyên ngành/slang, không đứng riêng và một số cognate/false-friend tùy population.
- Rank sample gần logarithmic. Preply báo ±10% dựa trên SD xấp xỉ 0.25 lần estimate, average sample count 22.5 và 1.96 standard-error multiplier.

Đây là mô tả của nhà cung cấp. Chưa có dữ liệu item-level/held-out để xác nhận calibration, coverage, thiết kế cognate theo từng L1 hoặc CI trên quần thể mục tiêu.

## Bảng so sánh

| Tiêu chí | Preply (mô tả đã fetch) | Nation/Beglar VST | Khuyến nghị hệ thống mới |
|---|---|---|---|
| Đơn vị | Dictionary main entry/headword | Word family | Chọn một và version hóa; không quy đổi ngầm |
| Universe | Khoảng 45K entries | 14K hoặc 20K word families | Corpus + dictionary/word-family list được công bố |
| Sampling | Hai giai đoạn, narrow log-rank midpoint | Stratified theo 1K frequency levels | Stratified random + optional adaptive routing + anchor |
| Item | Chi tiết production chưa biết; trang mô tả sample cleaning | 4-choice, simple context, same-POS distractors | Giữ item spec, pilot distractor bias và DIF |
| Guessing | Trang mô tả midpoint/checkbox; chưa thấy correction rõ trong phần đã fetch | Không correction; thừa nhận generous bias | Không correction mặc định; model lower-asymptote chỉ khi pilot chứng minh cần |
| Output | Estimate + vendor claim ±10% | Raw ×100/×200, total word families | Estimate + CI + unit + construct + diagnostics |
| Validity risk | Dictionary/L1/population/item bank production chưa độc lập kiểm định | Band ít item; low-frequency floor/ceiling | Hold-out, parallel forms, Rasch/IRT, external criterion |

### 2.5 IRT/CAT, guessing control và equating (iteration 2)

Nguồn bổ sung đã kiểm tra thực tế: Fokin, Płużyczka & Golovin, *The Polish Vocabulary Size Test: A Novel Adaptive Test for Receptive Vocabulary Assessment* ([PDF](https://arxiv.org/pdf/2507.19869), HTTP 200) và Akase, *Longitudinal measurement of growth in vocabulary size using Rasch-based test equating* ([PDF](https://d-nb.info/1257528165/34), HTTP 200).

- PVST chọn item kế tiếp theo độ khó gần với ability hiện tại, dừng ở 30 stimuli sau pilot khoảng 2 phút. Đây là nguyên lý CAT để tăng thông tin/item, nhưng số 30 là kết quả pilot của tiếng Ba Lan, không phải tham số mặc định cho English.
- PVST ước lượng ability trên thang logit, rồi fit hàm logistic `y=a/[1+exp(-b*(x-c))]` giữa item difficulty và rank tần suất để hiển thị số từ. Điểm `y` phụ thuộc mạnh vào cận trên `a`, vocabulary universe và đơn vị đếm; vì vậy cần coi đây là calibration có version, không phải quy đổi phổ quát từ logit sang “words”.
- Ba tín hiệu binary, multiple-choice và pseudoword có vai trò khác nhau. Binary nhanh nhưng dễ false alarm/self-report; multiple-choice giảm đoán nhưng tốn tải nhận thức; pseudoword cung cấp tín hiệu attention. PVST dùng attention index làm quality gate (dưới 70% loại khỏi hiệu chỉnh/aggregate), không tự động trừ điểm vocab cá nhân.
- Pilot PVST báo reliability of separation `.96` ở item và `.95` ở person; loại item có infit/outfit `>1.3` đồng thời z-score `>2.0`. Tuy nhiên item bank lệch về phía dễ, có thể kém phân biệt người có vocab cao. Đây là lý do phải kiểm tra targeting và item-fit bên cạnh frequency.
- Akase nối các form bằng common/linking items trên một thang Rasch logit chung để phân biệt growth với practice effect và khác biệt độ khó form. Nghiên cứu cũng ghi nhận overlap đáng kể giữa difficulty của các frequency bands; frequency là proxy hữu ích nhưng không đủ làm difficulty parameter.
