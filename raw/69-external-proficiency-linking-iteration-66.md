# Iteration 66 — External-proficiency linking và nonlinear criterion calibration

## 1. Phạm vi

Direction của iteration này là **liên kết điểm vocabulary-size với một tiêu chí năng lực độc lập**, thay vì biến số từ thành một nhãn CEFR hay một điểm đọc hiểu mặc định. Câu hỏi chính:

1. Một vocabulary estimate nên được đối chiếu với criterion nào và trên quần thể nào?
2. Quan hệ vocabulary → reading/proficiency có thể giả định tuyến tính không?
3. Làm sao tách `vocabulary_count` khỏi xác suất đạt một criterion cụ thể?
4. Validation cần kiểm tra gì trước khi công bố diễn giải ngoài construct receptive vocabulary?

Các URL đã fetch và kiểm tra HTTP trong iteration:

| Nguồn | HTTP | Vai trò |
|---|---:|---|
| [Laufer & Ravenhorst-Kalovski, 2010 — Lexical threshold revisited](https://files.eric.ed.gov/fulltext/EJ887873.pdf) | 200 | 745 người học; VLT word-family, coverage và bài đọc chuẩn hóa; so sánh ngưỡng criterion |
| [Ait Hammou et al., 2025 — Vocabulary Coverage and Size in EFL Critical Reading](https://files.eric.ed.gov/fulltext/EJ1472063.pdf) | 200 | VLT, coverage và critical-reading; kiểm tra quan hệ tuyến tính và skill-specific |
| [Gökcan & Çobanoğlu-Aktan, 2022 — Validation of the Vocabulary Size Test](https://dergipark.org.tr/en/download/article-file/2542175) | 200 | 3PL/IRT, DIF và tương quan với TOEFL/FLPE |
| [ETS Standards for Quality and Fairness, 2014](https://www.tr.ets.org/pdfs/about/standards-quality-fairness.pdf) | 200 | Nguyên tắc validity theo construct–purpose–population, criterion evidence, subgroup và conditional SEM |
| [Preply methodology — proxy fetch](https://r.jina.ai/https://preply.com/en/learn/english/test-your-vocab/how-it-works) | 200 | Mô tả vendor về universe, sampling, midpoint và margin; không phải independent validation |
| [Preply test page](https://preply.com/en/learn/english/test-your-vocab) | 403 | Không dùng làm bằng chứng nội dung trực tiếp |

## 2. Findings đã xác minh

### 2.1 Criterion link phải gắn với mục đích, quần thể và form

Laufer & Ravenhorst-Kalovski dùng 745 sinh viên EAP/college. Criterion là phần tiếng Anh của English Psychometric University Entrance Test do National Institute for Testing and Evaluation quản lý; bài thi có khoảng 60 câu, gồm hiểu từ, cấu trúc câu và thông tin văn bản, làm dưới áp lực thời gian. Các thí sinh làm các phiên bản khác nhau; tác giả ghi nhận chênh lệch độ khó giữa phiên bản được đưa vào điểm.

Vocabulary được đo bằng revised Vocabulary Levels Test: các level 2K, 3K, 5K và phần academic; mỗi “word” là word family. Nghiên cứu dùng các biến này để liên hệ với reading score, không coi vocabulary size tự thân là reading score.

Hệ quả cho hệ thống:

- `criterion_name`, `criterion_version`, `criterion_population` và `criterion_form_equating` phải nằm trong metadata calibration.
- Không dùng một nghiên cứu liên kết word-family với academic reading để biện minh cho headword count của Preply trong mọi population.
- Nếu criterion có phiên bản/form khác nhau, cần common-anchor/equating hoặc một score đã được tổ chức criterion chuẩn hóa.

### 2.2 “Đủ để đọc” là một decision target, không phải hằng số phổ quát

Laufer & Ravenhorst-Kalovski nhấn mạnh “adequate/reasonable comprehension” thay đổi theo bối cảnh. Trong dữ liệu của họ, khoảng 4K–5K word families và khoảng 95% coverage gắn với đọc có hướng dẫn; ngưỡng an toàn hơn cho đọc độc lập được đề xuất khoảng 8K families và 98% coverage. Đây là các diễn giải theo text, sample và quyết định giáo dục cụ thể, không phải hàm chuyển universal.

Bài cũng cho thấy ngưỡng có tính xác suất: có người đạt criterion dưới mức coverage được đề xuất và có người chưa đạt ở mức đó. Vì thế output thích hợp là:

```text
vocabulary_count = K_hat ± uncertainty
P(reading_criterion >= c | K_hat, target_population, text_domain)
```

Không nên trả lời “biết X từ nên đạt CEFR Y” nếu chưa có sample criterion-linking riêng cho target population và intended use.

### 2.3 Không được mặc định quan hệ tuyến tính

Laufer & Ravenhorst-Kalovski báo cáo trong sample của họ một hồi quy tuyến tính có công thức xấp xỉ `Reading score = 69.98 + 0.01 × vocabulary size`, với `R²` khoảng `.64` sau khi loại 10 người ở đầu cao. Tuy nhiên chính bảng nhóm của bài cho thấy increment không đều: coverage tăng ít dần theo band nhưng reading score không giảm tương ứng; khoảng 5K–6K có thể thấy cải thiện reading lớn dù coverage tăng nhỏ. Tác giả cảnh báo công thức tuyến tính chỉ chính xác nếu quan hệ thực sự tuyến tính.

Ait Hammou et al. (2025) cung cấp kiểm tra độc lập: trên 76 người học EFL, VLT tương quan `r=.471` với critical reading; vocabulary size một mình giải thích `R²=.22` (adjusted `.21`). Khi đưa text coverage vào kế hoạch hồi quy, tác giả loại coverage vì không có quan hệ tuyến tính với critical reading. Một số kỹ năng critical-reading có tương quan yếu hoặc không có ý nghĩa với vocabulary size.

Hai kết quả không mâu thuẫn: vocabulary có liên quan đến criterion, nhưng dạng hàm và độ mạnh phụ thuộc criterion, domain, range restriction và population. Do đó calibration phải so sánh ít nhất:

- linear regression với calibration slope/intercept;
- restricted cubic spline hoặc một mô hình monotone có kiểm soát overfit;
- ordinal/logistic model cho các decision threshold (`criterion >= c`);
- mô hình null có covariates ngoài vocabulary (L1, grammar, reading strategy, education) để xem incremental validity.

Mô hình phi tuyến là lựa chọn validation; không được bật production chỉ vì fit in-sample tốt hơn.

### 2.4 External link không thay thế calibration của item bank

Gökcan & Çobanoğlu-Aktan phân tích 140-item VST trên 1.457 response usable. 3PL phù hợp tốt nhất trong các mô hình so sánh; VST tương quan với TOEFL `r=.60` (95% CI `.49–.69`) và với FLPE `r=.53` (95% CI `.45–.60`, `n=368`). Nghiên cứu cũng tìm thấy 10 item có large DIF hoặc quá dễ theo mức khó, gồm các loanword như `yoghurt`, `microphone`, `kindergarten`.

Điều này hỗ trợ hai guardrail:

1. Tương quan với proficiency là bằng chứng convergent/criterion trong sample, không phải công thức đổi điểm cho mọi người.
2. External-linking phải đi cùng DIF/subgroup audit; nếu item bank có item dễ bất thường với một nhóm, correlation có thể phản ánh item bias hoặc population mix chứ không chỉ lexical ability.

Nghiên cứu này cũng dùng voluntary online sample và self-reported TOEFL/FLPE cho một phần dữ liệu; vì vậy không nên xem hệ số của nó là benchmark coverage cho Preply.

### 2.5 Chuẩn validity yêu cầu diễn giải có điều kiện

ETS Standards định nghĩa validation là đánh giá **interpretation** của điểm cho một population và purpose cụ thể. Chuẩn yêu cầu mô tả construct, purpose, claims, intended interpretation và target population; ghi nhận quan hệ với external/criterion variables, tính đại diện của sample, subgroup, correction cho unreliability của criterion và precision.

Về reliability, ETS nêu các bằng chứng có thể gồm information function, overall/conditional SEM và decision consistency; độ tin cậy phụ thuộc score range và use case. Vì vậy, với một vocabulary-size test:

- CI/SEM của `K_hat` không đủ để chứng minh claim về reading/CEFR;
- criterion prediction phải có error/interval riêng trên criterion scale;
- decision probability gần cut score phải được kiểm tra conditional, không chỉ báo correlation toàn mẫu.

## 3. Thuật toán đề xuất

### 3.1 Tách hai lớp output

```text
primary_construct:
  estimate: K_hat
  unit: headword | lemma | word_family
  universe_version: dictionary/corpus manifest
  uncertainty: CI_K or posterior interval
  mode: receptive_written_recognition

external_interpretation (optional, only after linking validation):
  criterion_name: e.g. academic_reading_form_v3
  target_population: versioned population definition
  P(criterion >= c | response_data)
  criterion_prediction_interval
  model_version
  transport_status: validated | provisional | not_validated
```

`K_hat` không lấy ngược từ reading score. Criterion chỉ là một biến validation/interpretation bổ sung.

### 3.2 Calibration data contract

Mỗi người trong linking sample cần có:

```text
person_id, vocabulary_form_id, item_responses, K_hat_or_theta
criterion_score, criterion_form_id, criterion_date
population_covariates, L1_or_language_background, education
missingness_status, accommodation, integrity_status
```

Điều kiện tối thiểu:

- criterion được chấm độc lập với vocabulary test;
- vocabulary và criterion có thời gian đủ gần cho intended interpretation;
- sample bao phủ score range, đặc biệt vùng cut score;
- có train/calibration và held-out validation persons/forms;
- subgroup sample đủ để estimate uncertainty hoặc ghi rõ “insufficient evidence”.

### 3.3 Pseudocode

```text
fit_external_link(vocab_scores, criterion, metadata):
    define construct, purpose, population, criterion cut(s)
    exclude or separately model invalid/incomplete sessions
    split by person (and preferably by form/time) into train and holdout
    verify score-range coverage and subgroup common support

    candidates = {
        linear: criterion ~ K_hat,
        spline: criterion ~ restricted_spline(K_hat),
        ordinal: P(criterion >= c) ~ K_hat + covariates,
        monotone: isotonic_or_monotone_spline(K_hat)
    }
    fit candidates on train only
    if covariates are used:
        compare vocab-only vs vocab-plus-covariates incremental validity
    select by prespecified holdout metric and calibration diagnostics
    estimate conditional SE / prediction interval by K_hat region
    audit residuals, subgroup calibration, DIF-linked item sensitivity,
         transport to held-out form/domain/population
    release only if prespecified error and calibration gates pass

predict(response, vocab_calibration, external_link=None):
    K_hat, CI_K = score_vocabulary(response, vocab_calibration)
    result = {"vocabulary_count": K_hat, "CI_K": CI_K}
    if external_link.status == "validated":
        result["criterion_probability"] = external_link.predict(K_hat)
        result["criterion_interval"] = external_link.prediction_interval(K_hat)
    else:
        result["criterion_probability"] = null
        result["transport_status"] = "not_validated"
    return result
```

### 3.4 Công thức và validation metrics

Với mô hình tuyến tính baseline:

```text
Y_i = α + β K_i + ε_i
```

`Y_i` là reading/proficiency score đã equate, không phải một phần của `K_i`. Với decision criterion `c`, dùng:

```text
logit P(Y_i >= c) = α_c + f(K_i)
```

Trong đó `f` phải được chọn trước hoặc kiểm tra bằng holdout. Nếu dùng spline/monotone model, bootstrap người (không bootstrap item độc lập sai cách) để tạo prediction interval. Báo cáo tối thiểu:

- calibration intercept và slope trên holdout;
- RMSE/MAE trên criterion scale;
- correlation chỉ như mô tả, không phải đủ validity;
- Brier score/AUC cho criterion decision nếu có cut;
- coverage của prediction interval theo vùng `K_hat`;
- calibration plots/decision consistency gần cut;
- kết quả riêng theo L1, education, age, modality và criterion form nếu có cỡ mẫu;
- sensitivity khi loại item DIF/loanword hoặc thay vocabulary model.

`CI_K` và `PI_Y` là hai khoảng khác nhau. Không cộng chúng thành một ±10% chung.

## 4. Đối chiếu với Preply

| Thành phần | Preply methodology đã fetch | Thiết kế đề xuất |
|---|---|---|
| Vocabulary universe | Vendor mô tả dictionary trên 45.000+ main entries, derived forms gộp theo main entry | Versioned universe và công bố unit; không đổi headword count thành word-family count |
| Sampling | Khoảng 40 từ để xác định vùng, sau đó khoảng 120 từ hẹp hơn theo frequency | Có thể giữ short-form routing, nhưng criterion link phải có form/route metadata và holdout |
| Estimator | Midpoint theo checked/unchecked words quanh frequency rank; vendor nêu margin khoảng ±10% theo giả định riêng | `K_hat` là vocabulary construct; external criterion là lớp prediction riêng |
| Criterion claim | Trang methodology đã fetch không công bố calibration độc lập với TOEFL/reading/CEFR; chưa tìm được nguồn xác thực cho production criterion-link coefficients của Preply | Chỉ phát hành probability/criterion claim khi có sample link và holdout coverage |
| Uncertainty | Vendor nêu ±10% cho vocabulary estimate, không phải evidence cho criterion prediction | Báo `CI_K`, `PI_Y`, conditional error và transport status tách biệt |
| Population/subgroup | Trang đã fetch không công bố đủ calibration sample, subgroup DIF hoặc criterion equating cho claim này | Pre-specify population, common support, subgroup calibration và form linking |
| Current implementation | Direct test endpoint trả 403 trong iteration; không xác minh được response-level linking/routing internals | Không suy luận rằng Preply không có cơ chế nội bộ; chỉ ghi nhận phần công khai chưa đủ để xác minh |

## 5. Validation plan

1. **Define claim trước dữ liệu:** chọn một criterion cụ thể, ví dụ academic reading form v3; không gọi đó là “English ability” chung.
2. **Independent calibration sample:** tuyển đủ range vocabulary/proficiency và ghi L1, education, domain, modality, form, integrity/missingness.
3. **Anchor/equate forms:** nếu criterion hoặc vocabulary form có nhiều phiên bản, giữ common anchors và kiểm tra drift trước khi gộp.
4. **Fit candidate functions:** linear, spline/monotone và threshold model; chọn theo holdout chứ không theo R² train.
5. **Check criterion reliability:** dùng score đã equate; nếu criterion reliability thấp, report correction/sensitivity và không overclaim.
6. **Subgroup/DIF audit:** lặp calibration theo subgroup có common support; kiểm tra item DIF/loanword và score residual.
7. **Conditional precision:** tính prediction interval và decision consistency theo các vùng `K_hat`, nhất là quanh cut.
8. **Transport test:** hold out theo person, form, thời điểm và nếu có thể theo domain/population; thay đổi lớn → `provisional` hoặc `not_validated`.
9. **Release policy:** production chỉ trả `criterion_probability` khi calibration slope/intercept, error, subgroup và interval coverage đạt ngưỡng định trước. Nếu không, trả `K_hat` với unit/CI và nói rõ criterion chưa được validate.

## 6. Gaps

- Chưa có response-level/item-bank data của Preply để fit hoặc kiểm tra bất kỳ external-link model nào.
- Chưa có sample độc lập gắn headword-based Preply score với một criterion reading/proficiency đã equate.
- Các hệ số `.64`, `.60`, `.53`, `.47` là của những sample/test/construct khác nhau; không được dùng làm coefficient cho Preply.
- Chưa tìm được nguồn xác thực cho một mapping phổ quát `Preply vocabulary count → CEFR/TOEFL/reading score`.
- Chưa có bằng chứng rằng một mô hình monotone hay spline cụ thể có coverage đúng trên target population; cần pilot và holdout.

## 7. Kết luận iteration

External proficiency là lớp **criterion validation và diễn giải có điều kiện**, không phải thành phần để định nghĩa hay sửa trực tiếp `K_hat`. Bằng chứng đã fetch cho thấy quan hệ vocabulary–reading/proficiency có ý nghĩa nhưng thay đổi theo population, criterion, skill và range; thậm chí coverage có thể không tuyến tính. Thiết kế an toàn là giữ vocabulary count độc lập, fit nhiều candidate link functions trên calibration sample, đánh giá conditional prediction/decision consistency và chỉ phát hành criterion probability sau holdout/subgroup validation. Preply methodology hiện cung cấp mô tả sampling/midpoint và vendor margin, nhưng chưa đủ bằng chứng công khai để xác minh một production link sang CEFR hay proficiency.
