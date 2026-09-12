# Iteration 19 — Modality và delivery-mode invariance

## 1. Phạm vi và direction

Direction của iteration này:

> **Modality and delivery-mode invariance:** kiểm tra liệu nhận diện bằng chữ, nhận diện bằng âm thanh, paper-versus-digital và response mode có làm thay đổi điểm vocabulary-size hay không; tách written receptive breadth khỏi listening/lexical-access subtests và chỉ so sánh sau khi equate.

Các iteration trước đã xử lý frequency sampling, word families/headwords, IRT, guessing, validity, response process, fairness, context, corpus drift và breadth/depth. Iteration này tập trung vào một nguồn biến thiên khác: cùng lexical content nhưng khác kênh tiếp nhận hoặc cách phân phối bài.

## 2. Nguồn đã kiểm tra

| Nguồn | Trạng thái kiểm tra | Vai trò |
|---|---:|---|
| [Aizawa, Iso & Nadasdy (2017), ERIC PDF](https://files.eric.ed.gov/fulltext/ED578279.pdf) | HTTP 200; tải và trích xuất được PDF | Nghiên cứu parallel visual/aural vocabulary tests |
| [Stewart, McLean & Batty (2021), VLI PDF](https://vli-journal.org/wp/wp-content/uploads/2022/01/06_VLI202115.pdf) | HTTP 200; tải và trích xuất được PDF | Tổng hợp quan hệ giữa các modality của vocabulary knowledge với reading/listening |
| [Preply methodology](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) | HTTP 200 qua endpoint đã dùng trong các iteration trước | Đối chiếu disclosure về word universe, frequency sampling và midpoint; không thấy calibration modality trong phần methodology đã fetch |

Search snippets chỉ được dùng để tìm nguồn. Các claim định lượng trong file này lấy từ PDF đã tải thành công, không lấy trực tiếp từ snippet.

## 3. Bằng chứng chính

### 3.1. Parallel design có thể cô lập mode effect

Aizawa, Iso và Nadasdy xây dựng hai test receptive vocabulary song song. Hai test dùng cùng target words, distractors và format; khác biệt chính là target word được trình bày bằng âm thanh trong Aural Test (AT) hoặc bằng chữ trong Visual Test (VT). Mỗi test có 120 câu: 15 câu ở mỗi band 1.000 từ của JACET8000, với một đáp án và ba distractors cùng từ loại. Target được trình bày trước choices; thời lượng trình bày target khoảng 5 giây và choices khoảng 10 giây.

Thiết kế này quan trọng hơn một so sánh hai bài khác nhau: nội dung lexical và cấu trúc lựa chọn được giữ chung, giúp ước lượng phần chênh lệch do modality. Trong production, nếu muốn xuất written breadth và aural breadth, cần một common-person/common-item pilot tương tự, thay vì dùng hai item bank khác nhau rồi quy đổi bằng raw percentage.

### 3.2. Written và aural score không tự động cùng scale

Nghiên cứu có 140 sinh viên engineering lower-intermediate ở Nhật. Điểm trung bình được báo cáo là 88.56 cho VT và 78.16 cho AT. VT cao hơn AT có ý nghĩa thống kê ở các frequency bands được phân tích; khoảng cách tăng tới khoảng band 6, sau đó pattern ở band 7–8 không còn đơn giản.

Cùng lexical content nhưng mức đúng khác nhau cho thấy `p_correct_visual` và `p_correct_aural` không nên được coi là hai quan sát của cùng một latent score nếu chưa kiểm tra invariance. Không nên lấy điểm written rồi gán nhãn listening vocabulary size, cũng không nên cộng hai mode vào một tổng số từ.

Các nguyên nhân khả dĩ (chỉ là diễn giải measurement, không phải hệ số đã được nguồn xác nhận) gồm khả năng nhận diện orthographic form, phonological form, mapping giữa âm thanh và nghĩa, tốc độ xử lý, và việc distractors được đọc/hiển thị. Vì vậy item-level mode effect phải được ước lượng bằng dữ liệu response, không suy ra từ frequency rank một mình.

### 3.3. Aural test có tín hiệu criterion khác trong một mẫu cụ thể

Aizawa et al. báo cáo AT tương quan với TOEIC ở mức `r = .57`, so với `r = .44` cho VT. Phân tích hồi quy của họ chọn AT band 3 rồi AT band 5 là các yếu tố giải thích TOEIC tốt nhất; VT scores không được chọn làm estimating factors.

Kết quả này hữu ích để thiết kế validation nhưng không phải conversion coefficient. Nó là kết quả của một mẫu Nhật Bản, một thiết kế test và một criterion cụ thể. Tác giả cũng nói cần phát triển thêm các form AT/VT để cải thiện reliability. Do đó thuật toán không được dùng `.57/.44` để chuyển written estimate thành listening estimate. Chỉ có thể pre-register hypothesis rằng aural subtest có thể có incremental validity cho listening, rồi kiểm tra trên hold-out sample.

### 3.4. Modality nên khớp với criterion cần dự đoán

Stewart, McLean và Batty tổng hợp nghiên cứu về các modality của written vocabulary knowledge. Họ báo cáo rằng meaning recall có tương quan mạnh hơn meaning recognition với reading trong bằng chứng được tổng hợp. Với listening, họ dẫn các estimate của meta-analysis: auditory-modality vocabulary tests có tương quan trung bình khoảng `.60`, còn orthographic tests khoảng `.52`; chênh lệch này không có ý nghĩa thống kê trong tổng hợp đó.

Bài cũng nhấn mạnh written và spoken receptive vocabulary có thể khác đáng kể, và cảnh báo không nên dùng written meaning-recognition test kiểu VST để đo listening vocabulary size. Với form recall và meaning recall trong quan hệ với listening, bài báo cáo khoảng `r = .63` (95% CI `.53–.72`) và `r = .58` (95% CI `.54–.62`); khoảng tin cậy chồng lấp, nên chưa đủ căn cứ chọn một format làm chuẩn phổ quát.

Hệ quả là estimand phải được ghi rõ:

- `written_receptive_breadth`: nhận diện form viết và nối với nghĩa theo format của item bank;
- `aural_receptive_breadth`: nhận diện spoken form và nối với nghĩa theo test audio;
- `depth` hoặc `meaning_recall`: output khác, không cộng thành số từ;
- `listening_criterion`: biến validation/criterion, không phải bản thân vocabulary-size score.

## 4. So sánh với Preply

Methodology Preply đã được fetch trong các iteration trước và được re-check HTTP 200 qua endpoint proxy ở iteration này. Phần methodology công khai mô tả dictionary/headword universe, ranking dựa trên BNC-derived spoken/written frequencies, hai giai đoạn sampling và midpoint estimate. Phần đã fetch không cung cấp item-level calibration cho visual-versus-aural mode, paper-versus-digital equating, audio device/latency, font/viewport hoặc accessibility.

Vì vậy so sánh an toàn là:

| Khía cạnh | Preply disclosure đã kiểm tra | Thiết kế đề xuất |
|---|---|---|
| Estimand | Dictionary/headword vocabulary estimate theo methodology công khai | Ghi rõ written receptive breadth; không gắn nhãn listening nếu không có aural subtest |
| Sampling | Hai giai đoạn, frequency-ranked và midpoint/logarithmic sampling theo disclosure | Giữ sampling frame/version; thêm mode-stratified calibration nếu có nhiều delivery modes |
| Mode | Chưa thấy mode-equating coefficient hoặc item-by-mode parameters trong phần đã fetch | Randomized common-item/common-person study; ước lượng DIF/mode effect và linking |
| Output | Một vocabulary-size number | Written breadth + uncertainty; aural/depth là output riêng nếu được đo và calibration |
| Cross-mode comparison | Chưa có bằng chứng công khai đủ để so sánh score | Chỉ so sánh sau common-anchor/equivalent-group linking và kiểm tra CI/fit |

Không được suy luận rằng Preply đo auditory vocabulary chỉ vì bài chạy trên web hoặc dùng câu hỏi tương tác. Chưa tìm được nguồn xác thực cho mode-specific item parameters của Preply.

## 5. Quy tắc thuật toán cập nhật

### 5.1. Default production path

1. Giữ output chính của test hiện tại là `written_receptive_breadth` trên đúng lexical frame mà item bank định nghĩa.
2. Ghi `delivery_mode = web_visual` cùng form/version, viewport class, input device và response status.
3. Không dùng written score để báo `listening_vocabulary_size`.
4. Nếu cần listening signal, tạo aural subtest có cùng target words/choices trong calibration study, nhưng báo nó như `aural_receptive_breadth` cho tới khi có linking.
5. Giữ `depth`, `meaning_recall`, `collocation` và `word_parts` ở scale riêng; không biến thành thêm word counts.

### 5.2. Calibration model khi có data

Với item `i`, người `p` và mode `m`, bắt đầu bằng logistic model hoặc 2PL mode-facet model:

```text
logit(P(Y[p,i,m] = 1)) = theta[p]
                       - b[i]
                       - delta_mode[m]
                       - gamma[i,m]
                       + covariates[p,m]
```

Trong đó:

- `theta[p]` là latent ability của construct được định nghĩa (không mặc định là listening);
- `b[i]` là item difficulty trên reference mode;
- `delta_mode[m]` là global mode shift;
- `gamma[i,m]` là item-by-mode interaction, chỉ giữ khi có sample đủ lớn và fit ổn định;
- `covariates` chỉ được thêm khi pre-registered và không che khuất mode effect.

Nếu mode interaction nhỏ và invariance đạt, dùng common-item linking để đưa mode về reference scale. Nếu interaction lớn hoặc DIF tập trung ở item/sense/frequency band, không ép một conversion coefficient; báo score theo mode riêng và gắn cờ non-equivalent.

### 5.3. Pseudocode

```text
function score_vocab(response, bank, requested_output):
    assert bank.lexical_frame is declared
    mode = response.delivery_mode
    written = score_reference_written_items(response, bank)
    written_ci = uncertainty(written, bank, response.status)

    result = {
        written_receptive_breadth: expand_within_frame(written, written_ci),
        written_CI: written_ci,
        mode: mode,
        flags: quality_flags(response)
    }

    if requested_output == "listening":
        if not bank.has_calibrated_aural_subtest:
            result.listening_status = "not_measured"
            result.listening_note = "chưa tìm được nguồn xác thực cho quy đổi written→listening"
        else:
            aural = score_aural_subtest(response, bank)
            if not bank.mode_linking_validated:
                result.aural_receptive_breadth = aural.score
                result.aural_status = "separate_uncalibrated_or_locally_calibrated_scale"
            else:
                result.aural_receptive_breadth = link_to_reference(aural, bank)
                result.aural_CI = uncertainty(aural, bank, response.status)

    return result
```

`expand_within_frame` chỉ được phép áp dụng trên frequency/dictionary frame đã dùng để xây dựng item bank. Không dùng các correlation trong nghiên cứu modality làm hàm quy đổi word count.

## 6. Validation plan cho mode invariance

### Calibration sample

- Tuyển người ở các dải năng lực và L1 mục tiêu; không chỉ một lớp lower-intermediate.
- Randomize thứ tự mode hoặc dùng counterbalanced equivalent groups để giảm practice/priming.
- Dùng cùng target words/choices cho common-item subset, nhưng tách forms đủ để tránh nhớ đáp án.
- Thu response-level data, response status, device/browser, audio replay/latency và accessibility accommodation.

### Phân tích bắt buộc

1. So sánh item difficulty theo mode, global shift và item-by-mode interaction.
2. Kiểm tra DIF theo mode conditional on ability; không chỉ so sánh raw means.
3. Kiểm tra frequency-band pattern và ceiling/floor riêng cho từng mode.
4. Link score bằng common items/equivalent groups; báo SE/CI của linking.
5. Kiểm tra invariance theo L1, proficiency và device/audio condition.
6. Dùng hold-out listening/reading criterion để kiểm tra incremental validity; không suy ra từ cùng sample calibration.
7. Re-test với alternate forms để tách mode effect, practice effect và learner growth.

### Decision gates

- **Equivalent:** mode effects nhỏ, no material DIF, linking error nhỏ so với conditional SE → có thể báo common scale với CI.
- **Locally linkable:** có mode shift ổn định nhưng không có interaction nghiêm trọng → link có version/mode metadata và cảnh báo.
- **Non-equivalent:** interaction lớn, DIF không ổn định, hoặc audio/device effects đáng kể → giữ output riêng; không quy đổi.
- **Insufficient evidence:** chưa có response-level calibration hoặc sample không đại diện → chỉ báo written score của mode reference và ghi gap.

## 7. Kết luận và giới hạn

Bằng chứng hiện có đủ để thay đổi specification: written vocabulary-size score không được gọi là listening vocabulary size; aural và visual scores không được cộng hoặc quy đổi trực tiếp; mode phải là metadata và là một facet calibration nếu sản phẩm cung cấp nhiều modality.

Bằng chứng chưa đủ để đặt một hệ số paper↔digital hoặc written↔aural cho Preply. Hai nguồn đã verify cung cấp bằng chứng nghiên cứu modality, nhưng không cung cấp item bank/response-level production data của Preply. Vì vậy các tham số mode-specific, threshold mode effect, mode linking error, và coverage của CI vẫn là gap thực nghiệm. Báo cáo giữ nguyên nguyên tắc: không có nguồn xác thực thì ghi rõ gap, không bịa hệ số.
