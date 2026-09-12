# Iteration 6 — Measurement invariance, fairness và transportability theo nhóm người học

## 1. Câu hỏi của iteration

Iteration này kiểm tra một rủi ro khác với sampling và calibration thuần túy: cùng một mức năng lực từ vựng tiềm ẩn có thể tạo ra xác suất trả lời khác nhau ở các nhóm người học. Trọng tâm là DIF (differential item functioning), ảnh hưởng của L1 loanword/cognate và khác biệt cách tiếp cận bài theo tuổi. Mục tiêu triển khai là biến bằng chứng này thành quy trình sàng lọc item, calibration theo subgroup và cách báo cáo không nhầm lợi thế ngôn ngữ có thật với bias đo lường.

Các nguồn dưới đây đã được fetch và kiểm tra HTTP 200 trong iteration 6. Các kết quả nghiên cứu là bằng chứng cho thiết kế/validation; chúng không phải tham số đã được calibration cho item bank của Preply.

## 2. Bằng chứng đã xác minh

### 2.1. DIF xuất hiện trong bài vocabulary multiple-choice giữa hai nhóm L1

Stoeckel & Bennett (2013) phân tích một bài kiểm tra receptive written English vocabulary 90 item ở 184 sinh viên Hàn Quốc và 146 sinh viên Nhật Bản học tiếng Anh tại nước mình. Bài được xây bằng cách lấy ngẫu nhiên 30 từ từ mỗi trong hai 1.000 từ đầu của General Service List và 30 từ từ Academic Word List. Tác giả dùng Rasch-based person measures để giữ ability chung, sau đó calibrate item riêng theo nhóm; tiêu chí DIF là p ≤ .01 và độ chênh lệch độ khó tuyệt đối ít nhất 0,5 logit. Kết quả: 21/90 item biểu hiện DIF.

Nguồn: [Stoeckel & Bennett, 2013 — Vocabulary Learning and Instruction](https://vli-journal.org/issues/02.1/issue02.1.08.pdf).

### 2.2. Tần suất và phạm vi sử dụng loanword trong L1 có thể đổi hướng DIF

Trong các item được xem xét, tần suất của loanword tương đương trong L1 dự đoán hướng DIF ở hầu hết trường hợp. Tác giả cũng nhận diện các yếu tố khác: loanword có thể có phạm vi nghĩa hẹp hơn hoặc xuất hiện trong ít compound hơn so với từ tiếng Anh; overlap về âm/văn tự với một loanword khác có thể kéo người làm bài về distractor. Ví dụ room và hall có distractor hấp dẫn cả các thí sinh có ability tương đối cao; hai item này được xem là có vấn đề đo lường và nên sửa wording/distractor.

Hệ quả: xếp item chỉ theo tần suất tiếng Anh là chưa đủ. Item metadata cần có cờ cognate/loanword theo L1 mục tiêu, phạm vi nghĩa/compound và lịch sử distractor. Tuy nhiên, lợi thế do người học thực sự đã gặp một loanword có thể là construct-relevant, không tự động là bias cần loại bỏ.

Nguồn: [Stoeckel & Bennett, 2013 — Vocabulary Learning and Instruction](https://vli-journal.org/issues/02.1/issue02.1.08.pdf).

### 2.3. Equivalent forms và CAT cần kiểm tra/calibrate theo nhóm

Stoeckel & Bennett kết luận rằng các item có DIF cần được xử lý đặc biệt khi dùng để tạo equivalent forms hoặc calibration cho CAT. Best practice được họ nêu là calibrate item riêng theo từng nhóm native-language; trong CAT có thể dùng L1 do thí sinh khai báo để chọn calibration set tương ứng. Tác giả không khuyến nghị xóa toàn bộ item DIF: làm vậy có thể làm mất tính đại diện của frequency-band sampling hoặc xóa khác biệt ngôn ngữ tự nhiên có liên quan tới construct.

Quy tắc thiết kế được áp dụng cho thuật toán:

1. Lưu `l1_group` hoặc nhóm ngôn ngữ theo cách khai báo tự nguyện; không dùng nó để thay đổi điểm cơ học trước khi có calibration.
2. Chạy DIF sau pilot đủ lớn cho từng nhóm và kiểm tra cả uniform lẫn non-uniform DIF.
3. Với item có DIF, phân loại nguyên nhân: construct-relevant linguistic exposure, wording/distractor artifact, hoặc nguyên nhân chưa biết.
4. Sửa/loại item rõ ràng gây nhiễu; giữ item phản ánh khác biệt exposure hợp lệ nhưng dùng group-specific calibration hoặc báo cảnh báo transportability.
5. Nếu subgroup quá nhỏ để ước lượng riêng, dùng common calibration bảo thủ và ghi rõ độ không chắc chắn; không tạo hệ số subgroup từ dữ liệu ít.

Nguồn: [Stoeckel & Bennett, 2013 — Vocabulary Learning and Instruction](https://vli-journal.org/issues/02.1/issue02.1.08.pdf).

### 2.4. Measurement invariance theo tuổi là giả định cần kiểm định, không phải mặc định

Fox, Berry & Freeman (2014) dùng item-response analysis trên dữ liệu của ba vocabulary tests phổ biến với nhóm trẻ, trung niên và lớn tuổi. Cả ba bộ dữ liệu cho thấy differential responding đáng kể: người thuộc các nhóm tuổi khác nhau nhưng đạt cùng tổng điểm vẫn có xác suất chọn các response category khác nhau trên cùng item và có cách tiếp cận bài khác nhau. Vì vậy kết luận an toàn hơn là các nhóm tuổi có thể đạt điểm khác nhau, chứ không mặc nhiên suy ra điểm đó là cùng một common ability trên mọi nhóm.

Nguồn bài và abstract đã kiểm tra qua [Europe PMC, PMID 25402336](https://europepmc.org/article/MED/25402336). Bản ghi API có abstract đầy đủ: [Europe PMC REST record](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:25402336%20AND%20SRC:MED&resultType=core&format=json).

### 2.5. Ví dụ đối chứng: invariance có thể đạt sau khi xử lý misfit, nhưng phụ thuộc population

Một nghiên cứu Rasch trên PPVT-III Form A ở 229 người lớn người Mỹ gốc Phi có kỹ năng đọc đơn từ khoảng lớp 3–5 cho thấy toàn bộ item ban đầu chưa fit đầy đủ. Sau khi chỉ phân tích item 73–156 và xử lý misfit, các item còn lại đạt internal consistency, unidimensionality và không có DIF đáng kể theo ability, gender và age (với một sửa đổi nhỏ). Kết quả này là một ví dụ quan trọng cho pipeline: phải sàng lọc item misfit trước khi kết luận invariance. Nó không chứng minh item bank của bài khác cũng invariant.

Nguồn bài và abstract đã kiểm tra qua [Europe PMC, PMID 22639554](https://europepmc.org/article/MED/22639554). Nghiên cứu có population đặc thù, nên chỉ dùng làm bằng chứng quy trình chứ không dùng làm tham số chuyển đổi cho Preply.

## 3. Cập nhật thuật toán đề xuất

### 3.1. Dữ liệu item cần bổ sung

Ngoài frequency rank/band và unit (headword/lemma/word-family), mỗi item nên có:

- `item_id`, `version`, `target`, `definition_or_context`, `correct_option`;
- `frequency_frame`, `frequency_rank`, `band`, `unit_definition`;
- `l1_exposure_flags`: cognate/loanword theo các L1 được pilot, nếu có bằng chứng độc lập;
- `distractor_history`: tỷ lệ chọn từng distractor theo ability/subgroup;
- `irt_parameters_by_group` khi sample đủ lớn, cùng cỡ mẫu và ngày calibration;
- `fit_stats`: infit/outfit hoặc chỉ báo CTT tương ứng, missing/timeout rate;
- `status`: active, revise, quarantine, retired và lý do quyết định.

Không nên lưu nhãn L1 nhạy cảm nếu không cần cho mục đích đo lường; nếu lưu, phải giải thích mục đích, cho phép bỏ qua và tách dữ liệu định danh khỏi response log.

### 3.2. Quy trình scoring có fairness gate

```text
input: response_log, item_bank, declared_L1_optional, target_precision

1. score raw responses; retain response time, missing, and distractor choice
2. estimate baseline ability/size using the pre-registered common scale
3. run quality checks: attention, speededness, item misfit, local dependence
4. if a validated L1-specific calibration exists and subgroup sample is adequate:
       estimate on that calibration, while preserving the same reported construct
   else:
       estimate on common calibration and mark subgroup-calibration-gap
5. calculate item-level DIF diagnostics on pilot/monitoring data:
       compare item difficulty or response functions conditional on ability
6. classify flagged DIF item:
       construct-relevant exposure -> retain with metadata / group calibration
       wording or distractor artifact -> revise or quarantine
       unresolved -> quarantine for new forms or report sensitivity analysis
7. transform ability to the declared unit scale (headword OR lemma OR family)
8. report point estimate, calibrated interval, unit/frame, quality flags,
   subgroup transportability status, and sensitivity with flagged items removed
```

DIF là một QA/fairness layer, không phải phép trừ điểm hậu kỳ. Trừ một số lượng cố định vì L1 hoặc tuổi mà chưa có calibration sẽ biến response bias chưa đo được thành bias mới.

### 3.3. Cách ra quyết định DIF

Ngưỡng p và logit của Stoeckel & Bennett chỉ là tiêu chí của nghiên cứu đó, không nên bê nguyên thành ngưỡng sản xuất. Pipeline cần pre-register:

- phương pháp (Rasch/IRT likelihood, Mantel–Haenszel hoặc logistic DIF phù hợp response model);
- effect-size threshold và multiple-comparison control;
- minimum subgroup sample và số anchor item;
- tiêu chí expert review về cognate, loanword, range of use, distractor và construct relevance;
- quyết định giữ/sửa/loại cùng lý do, không chỉ nhãn “DIF = bad”.

Báo cáo production nên cung cấp ít nhất: số item được test DIF, số item flag theo subgroup, effect-size distribution, nhóm nguyên nhân, sensitivity của điểm khi loại item flag, và trạng thái calibration. Nếu không đủ dữ liệu để kiểm định, ghi rõ `chưa tìm được nguồn xác thực cho ngưỡng DIF sản xuất riêng của Preply` thay vì gán một ngưỡng chung.

## 4. Tác động tới so sánh với Preply

Preply methodology đã được ghi nhận ở các iteration trước là headword/dictionary-based, còn VST là word-family scale; hai thang đo không đồng nhất. Iteration này bổ sung thêm một trục không đồng nhất: Preply-compatible midpoint/rank estimate có thể transport khác nhau theo L1, tuổi và exposure. Vì chưa có item bank và response-level data production của Preply, chưa thể kiểm định DIF hoặc tạo group-specific bridge cho Preply.

Bảng so sánh cập nhật:

| Đặc điểm | Preply theo methodology đã fetch | Thuật toán đề xuất |
|---|---|---|
| Đơn vị báo cáo | Dictionary headword/entry theo frame riêng | Chọn và công bố rõ headword, lemma hoặc word family; không trộn output |
| Sampling | Hai giai đoạn, rank/logarithmic midpoint; khoảng 40 + 120 từ theo mô tả công khai | Stratified baseline hoặc CAT đã calibration; giữ coverage theo frame và dừng theo precision |
| DIF/L1 | Chưa có item bank/response data công khai để kiểm chứng | Pilot theo L1/tuổi; DIF conditional on ability; review exposure và distractor; calibration riêng khi đủ dữ liệu |
| Uncertainty | Preply công bố claim khoảng ±10%, chưa có coverage độc lập trong nguồn đã fetch | CI/PI được calibration bằng response data, sensitivity flagged-item và uncertainty subgroup |
| Claim hợp lệ | Ước lượng theo dictionary/headword frame của Preply | Written receptive breadth trên unit đã khai báo; không suy ra productive fluency |

## 5. Validation plan bổ sung

1. **Pilot phân tầng:** thu response của các nhóm L1 và tuổi mục tiêu, với cùng frame và đủ overlap item; lưu distractor và response time.
2. **Item fit trước DIF:** loại hoặc sửa misfit rõ ràng trước khi diễn giải DIF, tương tự bài PPVT đối chứng.
3. **DIF analysis:** fit common Rasch/IRT model, sau đó so sánh item response functions conditional on ability; kiểm tra uniform/non-uniform DIF và điều chỉnh multiple comparisons.
4. **Expert response-process review:** với item flag, rà cognate/loanword, nghĩa vay mượn, compound, phonology/orthography, context và distractor; có think-aloud subsample nếu khả thi.
5. **Equating:** tạo alternate forms bằng common anchors; nếu nhóm có DIF ổn định và construct-relevant, fit group-specific item parameters rồi nối lên cùng latent scale.
6. **Transportability holdout:** giữ một nhóm L1/tuổi hoặc site không dùng khi calibration; đánh giá bias, RMSE, interval coverage và classification stability.
7. **Fairness report:** báo riêng common-scale estimate, group-calibrated estimate (nếu hợp lệ), số item flag, sensitivity range và gap dữ liệu. Không thay thế các kết quả thất bại bằng một điểm “đã hiệu chỉnh” không có provenance.

## 6. Gaps còn lại

- Chưa có response-level data hoặc item bank sản xuất của Preply để chạy DIF, kiểm tra item exposure/distractor và xác thực claim ±10% theo subgroup.
- Chưa có ngưỡng DIF sản xuất riêng của Preply; không được suy ra từ tiêu chí của một nghiên cứu 90 item.
- Chưa có mapping đã calibration giữa headword của Preply và lemma/word-family theo từng L1/tuổi; `chưa tìm được nguồn xác thực cho hệ số quy đổi headword↔lemma/word-family dùng chung`.
- Bằng chứng Stoeckel & Bennett tập trung Korean/Japanese và có hạn chế về corpus/informant; không được khái quát trực tiếp cho mọi L1.
- Bằng chứng Fox et al. tập trung ba test và nhóm tuổi; chưa chứng minh riêng cho vocabulary-size product online.
