# SAMPLING_AND_ESTIMATION_SPEC.md

> **Project:** `vocabulary-research` — `itpro-vn/vocabulary-research`  
> **Specification ID:** P0.2  
> **Status:** Proposed normative specification  
> **Scope:** Sampling design, routing, population estimation, uncertainty estimation, and simulation validation  
> **Priority:** P0 — correctness-critical

---

## 1. Mục tiêu và quy ước

Tài liệu này quy định thiết kế lấy mẫu và bộ ước lượng cho bài đánh giá vốn từ gồm:

1. **Stage 1 — Screening:** 25–30 items trên toàn bộ 10 tầng.
2. **Stage 2 — Focused Routing:** 40–60 items, ưu tiên các tầng quanh ranh giới năng lực nhưng vẫn duy trì mẫu xác suất tại mọi tầng.
3. **Research/Calibration:** 5–10 items phục vụ nghiên cứu và hiệu chỉnh ngân hàng câu hỏi.

Mục tiêu quan trọng nhất là:

> Tập trung câu hỏi để tăng hiệu quả đo lường, nhưng không biến kết quả thành phép ngoại suy thiếu căn cứ từ một số tầng được hỏi nhiều sang toàn bộ quần thể từ vựng.

### 1.1. Ngôn ngữ quy phạm

- **MUST / MUST NOT:** yêu cầu bắt buộc.
- **SHOULD / SHOULD NOT:** mặc định phải tuân thủ; ngoại lệ cần lý do và kiểm định.
- **MAY:** tùy chọn có kiểm soát.

### 1.2. Phạm vi đặc tả

Đây là thiết kế đề xuất độc lập với cấu trúc mã nguồn hiện tại. Tên module, API và schema bên dưới là hợp đồng đề xuất; không khẳng định repository đã triển khai chúng.

P0.2 MUST phân biệt rõ:

- đại lượng được đo;
- cơ chế chọn mẫu;
- mô hình dùng để routing;
- bộ ước lượng dùng để báo cáo;
- khoảng bất định;
- dữ liệu phục vụ calibration.

Một mô hình có thể giúp chọn câu hỏi tốt hơn mà không nhất thiết trở thành bộ ước lượng chính thức.

---

## 2. Đại lượng đích và đơn vị quần thể

### 2.1. Sampling frame

Gọi:

```text
U = tập hữu hạn các đơn vị từ vựng đủ điều kiện
N = |U|

U = U₁ ∪ U₂ ∪ ... ∪ U₁₀
Uₕ ∩ Uₖ = ∅ nếu h ≠ k

Nₕ = |Uₕ|
Wₕ = Nₕ / N
```

Mười tầng SHOULD được xây dựng từ tần suất, độ khó hoặc một quy tắc kết hợp đã được phiên bản hóa.

Không được mặc định `N₁ = ... = N₁₀`.

Mỗi phiên đánh giá MUST khóa:

- `frame_version`;
- `stratification_version`;
- `item_bank_version`;
- `scoring_version`;
- `routing_version`;
- `estimator_version`.

Thay đổi ngân hàng giữa phiên MUST NOT làm thay đổi âm thầm mẫu số hoặc trọng số.

### 2.2. Đơn vị lấy mẫu không đồng nhất với mọi biến thể câu hỏi

Đơn vị quần thể SHOULD là một đơn vị từ vựng có định nghĩa ổn định, ví dụ:

- lemma;
- word family;
- lemma–sense.

Dự án MUST chọn đúng một định nghĩa cho mỗi thước đo.

Nếu một từ có năm biến thể câu hỏi và từ khác có một biến thể, việc lấy mẫu trực tiếp trên mọi biến thể sẽ làm từ đầu có xác suất cao hơn. Vì vậy:

1. Chọn đơn vị từ vựng theo thiết kế này.
2. Chọn biến thể bằng một cơ chế riêng được ghi log.
3. Không coi các biến thể là năm đơn vị vốn từ độc lập.

### 2.3. Đại lượng đích chính

Trong chứng minh design-based, coi mỗi đơn vị có điểm tiềm năng cố định trong điều kiện kiểm tra đã chuẩn hóa:

```text
yᵢ ∈ [0, 1]

Tₕ = Σᵢ∈Uₕ yᵢ
T = Σₕ Tₕ
P = T / N
```

Ví dụ, `yᵢ ∈ {0,1}` là kết quả chấm đúng/sai theo rubric.

Tên báo cáo phù hợp:

> Số đơn vị từ vựng tương đương trả lời đúng trong sampling frame, theo giao thức đánh giá đã công bố.

Không được tự động diễn giải `T` là “số từ thực sự biết” nếu bài kiểm tra còn chịu ảnh hưởng của:

- đoán đáp án;
- nhớ hình thức nhưng không hiểu nghĩa;
- cue từ distractor;
- khác biệt giữa receptive và productive knowledge;
- độ ngẫu nhiên của câu trả lời;
- học tập hoặc mệt mỏi trong phiên.

### 2.4. Đại lượng latent là kết quả riêng

Nếu cần ước lượng “số từ thực sự biết”, định nghĩa:

```text
pᵢ = P(mastered unit i | latent proficiency, item parameters)
T_latent = Σᵢ∈U pᵢ
```

Đây là đại lượng **model-based**, phụ thuộc vào mô hình đo lường và calibration.

Hệ thống MUST NOT gắn nhãn kết quả latent là design-unbiased.

---

## 3. Quyết định kiến trúc bắt buộc

| Vấn đề | Quyết định P0.2 |
|---|---|
| Estimator chính | Ước lượng design-based bằng phần screening đã quan sát cộng HT trên phần còn lại |
| Screening | Stratified SRSWOR trên đủ 10 tầng |
| Focused routing | Phân bổ thích nghi theo screening; chọn SRSWOR trong mỗi tầng |
| Exploration floor | Ít nhất 2 items Stage 2 mỗi tầng còn ít nhất 2 đơn vị |
| Cập nhật quota Stage 2 | Khóa trước khi quan sát bất kỳ đáp án Stage 2 nào |
| Research | Mẫu xác suất riêng từ phần còn lại; không nhập vào estimator chính mặc định |
| Tầng không có quan sát | Không tự động gán 0 hoặc 1 |
| IRT/Bayesian | Dùng cho routing và kết quả bổ sung, có nhãn model-based |
| Khoảng bất định | Design-based cho estimator chính; posterior interval cho mô hình |
| Dừng sớm theo điểm | Không được hỗ trợ bởi estimator mặc định |
| Frame exclusion | Công khai; không ngoại suy đến các đơn vị có xác suất 0 |

Thiết kế này chủ động tránh bài toán khó hơn: lấy mẫu thích nghi từng câu rồi coi nghịch đảo xác suất của lần rút là trọng số inclusion của cả phiên.

---

## 4. Thiết kế lấy mẫu hai giai đoạn

Trong tài liệu này, “hai giai đoạn” nghĩa là hai pha đo lường nối tiếp trên cùng một frame, không phải thiết kế lấy cụm rồi lấy phần tử trong cụm.

### 4.1. Ngân sách

| Thành phần | Min | Default | Max |
|---|---:|---:|---:|
| Screening | 25 | 30 | 30 |
| Focused Routing | 40 | 50 | 60 |
| Research/Calibration | 5 | 8 | 10 |
| Tổng | 70 | 88 | 100 |

Ngân sách MUST được xác định trước khi lấy mẫu của pha tương ứng.

Ở phiên bản mặc định:

- screening: 3 items/tầng;
- focused: tổng 50 items;
- research: 8 items.

### 4.2. Stage 1 — Screening

Với tầng `h`:

```text
sₕ = số items screening
S₁ₕ = mẫu screening trong Uₕ

S₁ₕ ~ SRSWOR(Uₕ, sₕ)
```

SRSWOR là lấy mẫu ngẫu nhiên đơn không hoàn lại.

Phân bổ screening:

- baseline: 2 items/tầng;
- phân bổ 5–10 slots còn lại theo một quy tắc cố định, phiên bản hóa;
- mặc định với 30 items: `sₕ = 3` tại mọi tầng.

Quy tắc phân bổ bổ sung MAY ưu tiên tầng có dân số lớn hoặc luân phiên cân bằng theo phiên. MUST NOT dựa trên đáp án chưa tồn tại hoặc bị thay đổi trong lúc screening diễn ra.

Xác suất screening:

```text
π₁ᵢ = sₕ / Nₕ, với i ∈ Uₕ
```

Mọi tầng không rỗng MUST có ít nhất một đơn vị screening; cấu hình chuẩn yêu cầu ít nhất hai nếu kích thước cho phép.

Thứ tự trình bày SHOULD được xáo trộn có seed để tránh mọi câu dễ xuất hiện trước mọi câu khó.

### 4.3. Tín hiệu routing

Sau screening, tính đường cong xác suất trả lời đúng:

```text
p̃ₕ = xác suất dự đoán cho tầng h
```

Có thể dùng:

- beta-binomial shrinkage độc lập theo tầng;
- IRT đã calibration;
- monotone smoothing nếu được kiểm chứng;
- mô hình phân cấp có thành phần chuyên môn.

P0.2 mặc định dùng tín hiệu đơn giản:

```text
p̃ₕ = (aₕ + cₕ) / (aₕ + bₕ + sₕ)

cₕ = Σᵢ∈S₁ₕ yᵢ
```

`aₕ, bₕ` là hyperparameters phiên bản hóa. Khi dùng điểm liên tục, đây chỉ là công thức shrinkage phục vụ routing, không phải khẳng định posterior beta-binomial chính xác.

Ưu tiên quanh vùng bất định:

```text
ṽₕ = max(p̃ₕ × (1 − p̃ₕ), v_floor)
qₕ = Mₕ × sqrt(ṽₕ)

Mₕ = Nₕ − sₕ
```

Đây là xấp xỉ phân bổ Neyman để giảm phương sai của tổng.

Để tăng tập trung quanh ranh giới:

```text
bₕ = exp(−abs(p̃ₕ − τ) / t)
qₕ = Mₕ × sqrt(ṽₕ) × (1 + κ × bₕ)
```

Trong đó:

- `τ`: mức xác suất đích, mặc định `0.5`;
- `t > 0`: độ rộng vùng tập trung;
- `κ ≥ 0`: cường độ tập trung.

Các tham số MUST được chọn qua mô phỏng, không tối ưu chỉ trên nhóm người dùng điển hình.

Không được giả định mọi người có một ranh giới duy nhất. Người chuyên sâu hoặc học vẹt từ hiếm có thể tạo đường cong không đơn điệu.

### 4.4. Stage 2 — Focused Routing có exploration floor

Với mỗi tầng:

```text
Rₕ = Uₕ \ S₁ₕ
Mₕ = |Rₕ|

lₕ = min(2, Mₕ)
```

Phân bổ:

1. Cấp `lₕ` slots bắt buộc cho mỗi tầng.
2. Phân bổ ngân sách còn lại theo `qₕ`.
3. Giới hạn `nₕ ≤ Mₕ`.
4. Khóa vector `n = (n₁, ..., n₁₀)`.
5. Lấy mẫu độc lập giữa các tầng:

```text
S₂ₕ ~ SRSWOR(Rₕ, nₕ)
```

Với 50 items Stage 2 và frame đủ lớn:

- ít nhất 20 items bảo đảm exploration;
- khoảng 30 items có thể tập trung vào vùng hữu ích nhất.

Mọi item chưa được screening có xác suất có điều kiện:

```text
π₂ᵢ|S₁,Y₁ = nₕ / Mₕ
```

Do `nₕ > 0` khi `Mₕ > 0`, xác suất này dương.

### 4.5. Điều không được phép trong Stage 2 mặc định

MUST NOT:

- chọn “những từ khó nhất” trong tầng một cách deterministic;
- thay đổi `nₕ` dựa vào đáp án Stage 2;
- dừng tầng sau hai câu sai;
- thay câu mà người dùng có vẻ không biết bằng câu khác;
- ưu tiên item theo popularity mà vẫn dùng trọng số SRS;
- dùng CAT từng câu nhưng vẫn áp dụng estimator tại Mục 7.

Nếu cần chọn không đều trong tầng, phải thay bằng thiết kế PPS hoặc thiết kế xác suất khác với inclusion probabilities và variance estimator tương ứng.

---

## 5. Research/Calibration slots

### 5.1. Thiết kế mặc định

Sau Stage 2, gọi:

```text
C = U \ (S₁ ∪ S₂)
L = |C|
m_R = min(configured_research_budget, L)
```

Lấy:

```text
S_R ~ SRSWOR(C, m_R)
π_Rᵢ|history = m_R / L
```

Thiết kế này đảm bảo mọi item còn lại có cơ hội xuất hiện trong research, ngay cả khi chỉ có 5 slots và không thể cấp một slot cho đủ 10 tầng.

Không cần mọi tầng xuất hiện trong **mỗi** research block; cần mọi item đủ điều kiện có xác suất dương.

### 5.2. Item mới ngoài scoring frame

Nếu research chứa item chưa thuộc `U`:

- MUST dùng một research frame riêng `U_R`;
- MUST ghi xác suất chọn trong `U_R`;
- MUST NOT cộng trực tiếp đáp án đó vào ước lượng tổng trên `U`;
- MUST có cơ chế anchor/linking với ngân hàng hiện hành.

Có thể chia research budget thành:

- audit items trong scoring frame;
- calibration items trong research frame.

Mỗi block phải có thiết kế riêng, không dùng một propensity chung cho hai frame.

### 5.3. Sử dụng đáp án research

Mặc định, đáp án research:

- không cập nhật quota Stage 2;
- không được dùng để “vá” estimator chính;
- được dùng cho calibration, DIF, drift, phát hiện item lỗi và audit độc lập.

Một residual estimator phụ hợp lệ là:

```text
A = S₁ ∪ S₂

T̂_research =
    Σᵢ∈A yᵢ
    + (L / m_R) × Σᵢ∈S_R yᵢ
```

Với `m_R > 0`, estimator này không chệch có điều kiện trên lịch sử trước research, theo giả định điểm tiềm năng cố định.

Tuy nhiên, 5–10 items thường tạo phương sai lớn. Đây không phải estimator báo cáo mặc định.

Không được lấy trung bình hai estimator tương quan bằng trọng số được tối ưu từ chính đáp án nếu chưa phân tích bias và covariance.

### 5.4. Positivity không đồng nghĩa calibration tốt

Xác suất dương chỉ bảo đảm khả năng quan sát, không bảo đảm:

- đủ lượt trả lời cho từng item;
- đủ người ở các mức năng lực;
- nhận diện được guessing parameter;
- ổn định mô hình đa chiều.

Calibration MUST theo dõi số quan sát hiệu dụng theo item × vùng năng lực và độ liên thông với anchor items.

---

## 6. Positive inclusion probability và propensity logging

### 6.1. Bảo đảm ở ba cấp

**Cấp quần thể**

Mọi đơn vị thuộc frame đích MUST đủ điều kiện được chọn.

**Cấp screening**

```text
π₁ᵢ > 0
```

**Cấp phần còn lại sau screening**

```text
π₂ᵢ|S₁,Y₁ > 0
```

Research bổ sung một kênh xác suất dương trên phần frame chưa được hỏi.

### 6.2. Xác suất có điều kiện không phải xác suất inclusion toàn phiên

Với routing thích nghi, xác suất một item xuất hiện ở Stage 2 phụ thuộc vào kết quả screening.

Vì vậy, MUST NOT dùng máy móc:

```text
π_session = 1 − (1 − π₁) × (1 − π₂_observed)
```

`π₂_observed` được tính trên một lịch sử cụ thể; nó không phải xác suất vô điều kiện của một nhánh chọn độc lập.

Estimator chính tránh việc phải tính `π_session` bằng cách điều kiện hóa trên screening và ước lượng phần còn lại.

### 6.3. Loại trừ item

Các quy tắc về ngôn ngữ, accessibility, độ tuổi, license hoặc chất lượng có thể khiến item không đủ điều kiện.

Khi đó phải:

1. tạo frame đích tương ứng;
2. tính lại `Nₕ`;
3. lưu exclusion policy;
4. không báo cáo tổng của frame gốc nếu không có mô hình ngoại suy riêng.

Exposure cap hoặc blacklist tạo xác suất bằng 0 đối với một item trong phiên cũng là thay đổi frame hoặc thay đổi thiết kế, không phải chi tiết triển khai vô hại.

---

## 7. Bộ ước lượng design-based chính

### 7.1. Vì sao không dùng trung bình mẫu gộp?

Estimator sai:

```text
T̂_naive = N × mean(y trên tất cả items đã hỏi)
```

Nếu nhiều câu được hỏi quanh ranh giới có tỷ lệ đúng gần 0.5, estimator này có thể kéo người rất yếu hoặc rất mạnh về giữa.

Số câu hỏi trong mỗi tầng là quyết định thiết kế, không phản ánh kích thước tầng trong quần thể.

### 7.2. Estimator residual Horvitz–Thompson

Với mỗi tầng:

```text
Aₕ = Σᵢ∈S₁ₕ yᵢ
ȳ₂ₕ = (1 / nₕ) × Σᵢ∈S₂ₕ yᵢ

T̂ₕ = Aₕ + Mₕ × ȳ₂ₕ
T̂ = Σₕ T̂ₕ
P̂ = T̂ / N
```

Dạng trọng số:

```text
T̂ =
    Σᵢ∈S₁ yᵢ
    + Σₕ Σᵢ∈S₂ₕ yᵢ / π₂ᵢ|S₁,Y₁
```

Trọng số đóng góp:

```text
screening item: 1
Stage 2 item tại tầng h: Mₕ / nₕ
research item: 0 trong estimator chính
```

Screening có trọng số 1 vì đây là phần quần thể đã được biết trực tiếp. Stage 2 đại diện cho phần quần thể chưa quan sát sau screening.

Đây không phải phép pooling theo tỷ lệ mẫu.

### 7.3. Tính không chệch

Với điểm tiềm năng cố định và điều kiện trên screening:

```text
E[T̂ₕ | S₁, Y₁]
  = Aₕ + Mₕ × mean(y trên Rₕ)
  = Tₕ
```

Suy ra:

```text
E[T̂ | S₁, Y₁] = T
E[T̂] = T
```

Routing có thể dùng một mô hình sai đáng kể mà không gây bias thiết kế cho estimator này, miễn là:

- quota được khóa trước Stage 2;
- Stage 2 thực sự là SRSWOR trong từng phần còn lại;
- mọi phần còn lại có mẫu;
- dữ liệu đáp án và frame đúng;
- không có missingness không được xử lý.

Mô hình routing sai vẫn có thể làm phương sai tăng.

### 7.4. Post-stratification: dùng đúng phạm vi

Công thức quen thuộc:

```text
T̂_PS = Σₕ Nₕ × ȳₕ
```

hợp lệ trong những thiết kế mà `ȳₕ` là estimator phù hợp cho mean của tầng.

Nhưng MUST NOT lấy `ȳₕ` là trung bình gộp screening và focused một cách mặc định. Kích thước focused sample phụ thuộc vào screening outcomes; mẫu gộp không còn tự động là SRS với kích thước cố định.

P0.2 sử dụng:

```text
T̂ₕ = observed screening total + estimated remainder total
```

để tránh giả định sai đó.

### 7.5. Tầng không được hỏi

Trong thiết kế chuẩn, không có tầng không được screening, và không có phần còn lại không được Stage 2 lấy mẫu.

Nếu một hệ thống khác bỏ qua hoàn toàn tầng `h`:

- không có estimator design-unbiased tổng quát cho `Tₕ` từ dữ liệu của các tầng khác;
- post-stratification không khôi phục thông tin đã không được lấy;
- IPW không sửa được xác suất inclusion bằng 0;
- gán 100% cho tầng dễ hoặc 0% cho tầng khó là giả định mô hình.

Muốn báo cáo tầng đó phải chọn một trong hai:

1. bổ sung mẫu xác suất;
2. dùng model-based prediction và công bố rõ sự phụ thuộc mô hình.

---

## 8. Ước lượng phương sai và khoảng tin cậy

### 8.1. Phương sai design-based có điều kiện

Với `2 ≤ nₕ < Mₕ`:

```text
s²₂ₕ = Σᵢ∈S₂ₕ (yᵢ − ȳ₂ₕ)² / (nₕ − 1)

V̂ₕ = Mₕ² × (1 − nₕ / Mₕ) × s²₂ₕ / nₕ
V̂(T̂) = Σₕ V̂ₕ

SE(T̂) = sqrt(V̂(T̂))
SE(P̂) = SE(T̂) / N
```

Nếu `nₕ = Mₕ`, phần còn lại là census và `V̂ₕ = 0`.

Nếu `Mₕ = 1`, phải chọn item duy nhất đó.

MUST NOT dùng phương sai SRS của mẫu gộp toàn phiên.

### 8.2. Wald interval chỉ là chỉ báo xấp xỉ

```text
CI_Wald = T̂ ± 1.96 × SE(T̂)
```

Wald interval có thể under-cover mạnh khi:

- ít mẫu mỗi tầng;
- nhiều tầng toàn đúng hoặc toàn sai;
- năng lực ở hai cực;
- routing khiến quota mất cân đối.

Đặc biệt, `s²₂ₕ = 0` trong mẫu không chứng minh cả tầng đồng nhất.

Wald interval MUST NOT là khoảng chính thức trước khi vượt simulation gates.

### 8.3. Khoảng bảo thủ cho điểm nhị phân

Với `yᵢ ∈ {0,1}`, dùng đảo kiểm định phân phối hypergeometric.

Sau screening:

```text
Kₕ = tổng số đáp án đúng tiềm năng trong Rₕ
kₕ = số đáp án đúng quan sát trong S₂ₕ

kₕ ~ Hypergeometric(Mₕ, Kₕ, nₕ)
```

Xây dựng tập tin cậy cho `Kₕ` bằng cách giữ các giá trị nguyên `K` thỏa:

```text
P_K(X ≥ kₕ) ≥ αₕ / 2
P_K(X ≤ kₕ) ≥ αₕ / 2
```

Miền tìm kiếm:

```text
kₕ ≤ K ≤ Mₕ − nₕ + kₕ
```

Chọn:

```text
Σₕ αₕ ≤ α
```

Mặc định `α = 0.05`, `αₕ = 0.005` cho mỗi tầng.

Nếu `Lₕ, Uₕ` là cận của tập chấp nhận:

```text
CI_total =
[
  Σₕ (Aₕ + Lₕ),
  Σₕ (Aₕ + Uₕ)
]
```

Theo union bound, coverage ít nhất `1 − α`, có điều kiện trên screening, dưới mô hình finite-population cố định.

Khoảng có thể rộng. Đây là chi phí thật của yêu cầu ít giả định; MUST NOT thu hẹp tùy tiện vì lý do UX.

### 8.4. Điểm liên tục trong [0,1]

Hypergeometric interval không áp dụng trực tiếp.

Một fallback bảo thủ dùng Hoeffding bound cho mean khi lấy mẫu không hoàn lại:

```text
εₕ = sqrt(log(2 / αₕ) / (2 × nₕ))

mean_lowerₕ = max(0, ȳ₂ₕ − εₕ)
mean_upperₕ = min(1, ȳ₂ₕ + εₕ)

T_lowerₕ = Aₕ + Mₕ × mean_lowerₕ
T_upperₕ = Aₕ + Mₕ × mean_upperₕ
```

Census phải trả khoảng suy biến tại tổng đã biết.

Có thể thay bằng bound finite-population chặt hơn, nhưng MUST có test coverage riêng.

### 8.5. Bất định thiết kế và bất định đo lường

Khoảng trên phản ánh việc chỉ quan sát một phần frame, dưới giả định điểm tiềm năng cố định.

Nó không tự động bao gồm:

- sai số item parameters;
- biến thiên giữa các lần người dùng trả lời;
- sai lệch construct;
- guessing correction;
- drift;
- thay đổi trạng thái trong phiên.

Nếu target là tổng xác suất trả lời đúng hoặc latent mastery, phải bổ sung mô hình bất định tương ứng và gắn nhãn khác.

---

## 9. Model-based và model-assisted estimation

### 9.1. Model-based extrapolation

Ví dụ mô hình IRT:

```text
P(Yᵢ = 1 | θ)
  = cᵢ + (1 − cᵢ) × logistic(aᵢ × (θ − bᵢ))
```

Ước lượng:

```text
T̂_model = Σᵢ∈U E[pᵢ | observed data]
```

Phân phối bất định SHOULD tích hợp:

- posterior của năng lực;
- uncertainty của item parameters;
- thành phần đa chiều nếu có;
- model discrepancy khi có bằng chứng.

Ưu điểm: ổn định hơn với ít câu hỏi.

Rủi ro: sai lệch ở người chuyên sâu, người học từ hiếm, DIF hoặc đường cong không đơn điệu.

### 9.2. Model-assisted residual correction

Một extension hợp lệ là khóa dự đoán `mᵢ ∈ [0,1]` sau screening, trước Stage 2:

```text
T̂_MA =
    Σᵢ∈S₁ yᵢ
    + Σᵢ∈R mᵢ
    + Σₕ (Mₕ / nₕ) × Σᵢ∈S₂ₕ (yᵢ − mᵢ)
```

Estimator này không chệch có điều kiện trên screening khi dự đoán đã được khóa và sampling đúng.

Không được fit `mᵢ` trên chính Stage 2 rồi mặc nhiên giữ nguyên chứng minh trên.

Extension này MAY triển khai sau estimator chính; cần variance estimator và simulation riêng.

### 9.3. Output không được nhập nhằng

API SHOULD cung cấp các trường riêng:

```text
design_based_total
design_based_interval
model_based_total
model_based_interval
estimand
interval_method
assumption_flags
```

Không chọn kết quả nào “trông hợp lý hơn” để hiển thị sau khi thấy chênh lệch.

---

## 10. Pseudocode chuẩn

### 10.1. Phân bổ ngân sách có floor và capacity

```text
function allocate_with_floor(total, floor, capacity, priority):
    require length(floor) == length(capacity) == 10
    require all(0 <= floor[h] <= capacity[h])
    require total >= sum(floor)

    target = min(total, sum(capacity))
    n = copy(floor)
    extra = zeros(10)

    while sum(n) < target:
        eligible = [h where n[h] < capacity[h]]

        require eligible is not empty

        # Quy tắc apportionment deterministic, phiên bản hóa.
        # Tie-break bằng thứ tự tầng cố định.
        h_star = argmax_over(
            eligible,
            priority[h] / (extra[h] + 1)
        )

        n[h_star] += 1
        extra[h_star] += 1

    return n
```

`priority` MUST dương với mọi tầng còn capacity, hoặc có fallback được xác định trước.

### 10.2. Screening và routing

```text
function plan_screening(frame, config, rng):
    validate_frame(frame)
    require frame.has_exactly_10_strata()

    N = frame.stratum_sizes()

    floor = [min(2, N[h]) for h in 1..10]
    priority = config.fixed_screening_priorities

    s = allocate_with_floor(
        config.screening_budget,
        floor,
        N,
        priority
    )

    S1 = empty_sample()

    for h in 1..10:
        selected = SRSWOR(frame.units[h], s[h], rng)

        for item in selected:
            log_selection(
                item=item,
                phase="screening",
                probability=s[h] / N[h],
                probability_type="phase_inclusion",
                risk_set_size=N[h]
            )

        S1.add(h, selected)

    return shuffle_for_presentation(S1, rng)
```

```text
function plan_focused(frame, S1, Y1, config, rng):
    require all_screening_responses_resolved(S1, Y1)

    for h in 1..10:
        R[h] = frame.units[h] minus S1[h]
        M[h] = size(R[h])
        c[h] = sum(Y1[i] for i in S1[h])

        p[h] = (
            config.a[h] + c[h]
        ) / (
            config.a[h] + config.b[h] + size(S1[h])
        )

        variance_proxy = max(
            p[h] * (1 - p[h]),
            config.variance_floor
        )

        boundary_bonus = exp(
            -abs(p[h] - config.target_probability)
            / config.routing_temperature
        )

        priority[h] = M[h] * sqrt(variance_proxy) * (
            1 + config.boundary_strength * boundary_bonus
        )

        floor[h] = min(2, M[h])

    n = allocate_with_floor(
        config.focused_budget,
        floor,
        M,
        priority
    )

    persist_immutable_routing_plan(
        quotas=n,
        screening_history_hash=hash(S1, Y1),
        configuration=config
    )

    S2 = empty_sample()

    for h in 1..10:
        if M[h] == 0:
            continue

        require n[h] > 0
        selected = SRSWOR(R[h], n[h], rng)

        for item in selected:
            log_selection(
                item=item,
                phase="focused",
                probability=n[h] / M[h],
                probability_type="conditional_phase_inclusion",
                risk_set_size=M[h],
                locked_quota=n[h]
            )

        S2.add(h, selected)

    return shuffle_for_presentation(S2, rng)
```

### 10.3. Research

```text
function plan_research(frame, S1, S2, config, rng):
    C = frame.units minus union(S1, S2)
    m = min(config.research_budget, size(C))

    if m == 0:
        return empty_sample()

    SR = SRSWOR(C, m, rng)

    for item in SR:
        log_selection(
            item=item,
            phase="research",
            probability=m / size(C),
            probability_type="conditional_phase_inclusion",
            risk_set_size=size(C)
        )

    return SR
```

### 10.4. Estimation

```text
function estimate_design_total(frame, S1, Y1, S2, Y2, plan):
    validate_locked_plan(plan)
    validate_no_duplicates(S1, S2)
    validate_membership_and_counts(frame, S1, S2, plan)
    require all_required_responses_resolved()

    total = 0
    variance = 0
    stratum_results = []

    for h in 1..10:
        N_h = size(frame.units[h])
        s_h = size(S1[h])
        M_h = N_h - s_h
        n_h = size(S2[h])
        A_h = sum(Y1[i] for i in S1[h])

        if M_h == 0:
            T_h = A_h
            V_h = 0
        else:
            require n_h == plan.quotas[h]
            require n_h > 0

            mean_h = mean(Y2[i] for i in S2[h])
            T_h = A_h + M_h * mean_h

            if n_h == M_h:
                V_h = 0
            else:
                require n_h >= 2

                s2_h = sample_variance(
                    Y2[i] for i in S2[h],
                    denominator=n_h - 1
                )

                V_h = (
                    M_h * M_h
                    * (1 - n_h / M_h)
                    * s2_h / n_h
                )

        total += T_h
        variance += V_h

        stratum_results.append({
            "stratum": h,
            "population_size": N_h,
            "estimated_total": T_h,
            "estimated_variance": V_h
        })

    interval = conservative_interval(
        frame, S1, Y1, S2, Y2, alpha=0.05
    )

    return {
        "estimand": "finite_frame_standardized_response_total",
        "total": total,
        "proportion": total / size(frame.units),
        "standard_error": sqrt(variance),
        "interval": interval,
        "strata": stratum_results,
        "estimator_version": CURRENT_ESTIMATOR_VERSION
    }
```

### 10.5. Exact binary interval

```text
function binary_remainder_interval(M, n, k, alpha_h):
    if M == 0:
        return [0, 0]

    if n == M:
        return [k, k]

    require 0 < n < M

    accepted = []

    for K in integers(k, M - n + k):
        upper_tail = hypergeom_probability_X_ge_k(M, K, n, k)
        lower_tail = hypergeom_probability_X_le_k(M, K, n, k)

        if upper_tail >= alpha_h / 2
           and lower_tail >= alpha_h / 2:
            accepted.append(K)

    require accepted is not empty
    return [min(accepted), max(accepted)]
```

Production implementation SHOULD dùng tính đơn điệu và tìm kiếm nhị phân thay vì duyệt mọi `K`, nhưng phải cho kết quả tương đương trong test.

---

## 11. Missingness, dropout và integrity

### 11.1. “Không biết” khác “không có dữ liệu”

- Người dùng chủ động chọn “không biết”: có thể chấm `0` theo rubric.
- Lỗi mạng, bỏ phiên, không render được item: missing.
- Timeout: chỉ là `0` nếu giao thức đã định nghĩa và validity study hỗ trợ.

MUST NOT chuyển mọi missing thành sai.

### 11.2. Dropout

Estimator chính yêu cầu hoàn tất mẫu đã khóa.

Nếu chưa hoàn tất:

```text
status = "incomplete"
official_design_estimate = null
```

Có thể hiển thị provisional model-based result, nhưng không gắn cùng nhãn với kết quả hoàn tất.

Inverse response weighting chỉ MAY dùng khi xác suất phản hồi được mô hình hóa, có positivity và kiểm định riêng. Chọn mẫu xác suất không tự động khắc phục nonresponse bias.

### 11.3. Dừng sớm

Dừng theo đáp án hiện tại làm thay đổi thiết kế.

P0.2 mặc định MUST NOT phát hành khoảng tin cậy thông thường cho phiên dừng sớm thích nghi.

Muốn hỗ trợ phải có đặc tả riêng cho:

- sequential estimator;
- stopping rule;
- inclusion probabilities;
- confidence sequence hoặc phương pháp suy luận tương ứng.

### 11.4. Learning và order effects

Các giả định finite-population bị suy yếu nếu một câu hỏi làm người dùng học đáp án cho câu sau.

SHOULD:

- không phản hồi đáp án đúng trước khi kết thúc;
- tránh các biến thể cùng đơn vị trong một phiên;
- randomize presentation order trong phạm vi giao thức;
- mô phỏng fatigue và dependence;
- kiểm định carryover giữa các items liên quan.

---

## 12. Logging và hợp đồng dữ liệu

### 12.1. Session metadata

```json
{
  "session_id": "uuid",
  "frame_version": "frame-v1",
  "stratification_version": "strata-v1",
  "item_bank_version": "bank-v1",
  "scoring_version": "score-v1",
  "routing_version": "routing-p0.2-v1",
  "estimator_version": "residual-ht-v1",
  "screening_budget": 30,
  "focused_budget": 50,
  "research_budget": 8,
  "rng_algorithm": "versioned-approved-prng",
  "rng_seed_reference": "restricted-reference",
  "status": "completed"
}
```

### 12.2. Selection event

```json
{
  "session_id": "uuid",
  "unit_id": "unit-123",
  "item_variant_id": "variant-2",
  "stratum_id": 6,
  "phase": "focused",
  "risk_set_size": 997,
  "locked_quota": 8,
  "conditional_phase_inclusion_probability": 0.0080240722,
  "estimation_weight": 124.625,
  "routing_plan_hash": "sha256:...",
  "selected_at": "ISO-8601",
  "presentation_index": 42
}
```

### 12.3. Audit invariants

MUST kiểm tra tự động:

```text
Σₕ Nₕ = N
S₁ ∩ S₂ = ∅
S_R ∩ (S₁ ∪ S₂) = ∅
0 < π ≤ 1 cho mọi item được chọn
nₕ ≤ Mₕ
nₕ ≥ min(2, Mₕ)
Σᵢ∈S₂ₕ estimation_weightᵢ = Mₕ
T̂ ∈ [0, N] khi y ∈ [0,1]
```

Propensity MUST được lưu tại thời điểm chọn, không suy ngược từ kết quả cuối phiên.

---

## 13. Calibration và trọng số

### 13.1. Hai mục tiêu khác nhau

**Item calibration có điều kiện trên năng lực**

Ước lượng item response function từ likelihood phù hợp. Khi routing chỉ phụ thuộc lịch sử quan sát, cơ chế assignment có thể được bỏ qua trong likelihood dưới các giả định ignorability thích hợp.

Điều này không miễn trừ việc kiểm tra:

- latent trait estimation;
- sample selection;
- model misspecification;
- DIF;
- overlap theo năng lực.

**Ước lượng thống kê đại diện cho population**

Ví dụ tỷ lệ trả lời đúng của một item trong nhóm người học mục tiêu. Cần xem xét cả:

- xác suất tuyển người dùng;
- xác suất item được giao cho người đó;
- xác suất hoàn tất/phản hồi.

Trọng số chọn item không sửa được bias do người dùng tự nguyện tham gia.

### 13.2. Không áp dụng IPW mù quáng

MUST NOT đưa nghịch đảo propensity vào mọi IRT likelihood mà không định nghĩa estimand.

Calibration pipeline MUST chỉ rõ:

- target population;
- unit of analysis;
- assignment mechanism;
- response model;
- weighting strategy;
- uncertainty estimator;
- exposure diagnostics.

---

## 14. Simulation Protocol

### 14.1. Mục tiêu

Mô phỏng phải trả lời:

1. Estimator có bias không?
2. Routing có giảm RMSE ở cùng budget không?
3. Khoảng tin cậy có coverage danh nghĩa không?
4. Hiệu năng có suy giảm ở hồ sơ phi điển hình không?
5. Positivity có được thực thi đúng không?
6. Kết luận có còn đúng khi mô hình routing hoặc response model sai không?

### 14.2. Hai lớp mô phỏng bắt buộc

#### Lớp A — Design correctness

1. Sinh một frame hữu hạn.
2. Sinh và khóa vector `yᵢ` cho một hồ sơ.
3. Lặp lại toàn bộ screening → routing → estimation nhiều lần.
4. So sánh với tổng chính xác `T = Σ yᵢ`.

Lớp này kiểm định trực tiếp định lý không chệch và coverage finite-population.

#### Lớp B — Measurement realism

Mỗi lần kiểm tra sinh câu trả lời theo response model, có thể bao gồm:

- guessing;
- slips;
- fatigue;
- item dependence;
- latent domains;
- item parameter uncertainty;
- dropout.

Truth phải được định nghĩa riêng:

```text
T_probability = Σᵢ P(correct on item i under protocol)
```

hoặc:

```text
T_mastery = Σᵢ masteryᵢ
```

Không đánh giá một estimator của response total bằng latent mastery rồi gọi mọi sai khác là sampling bias.

### 14.3. Frame mô phỏng

Tối thiểu:

- 10 tầng bằng nhau;
- 10 tầng kích thước rất khác nhau;
- tầng nhỏ gần census;
- item difficulty chồng lấn giữa tầng;
- domain phân bố không đều;
- frame có 10.000 và 50.000 đơn vị.

Các kích thước này là cấu hình test, không phải khẳng định frame thật của dự án.

### 14.4. Hồ sơ người dùng bắt buộc

Các vector dưới đây là xác suất trung bình minh họa từ tầng 1 đến tầng 10.

| Hồ sơ | Vector minh họa |
|---|---|
| EFL yếu | `[.85, .65, .40, .20, .10, .06, .04, .03, .02, .02]` |
| Trung bình | `[.98, .95, .88, .75, .55, .35, .20, .10, .06, .04]` |
| Mạnh, phổ rộng | `[.99, .99, .98, .95, .90, .82, .70, .55, .35, .20]` |
| Chuyên sâu | Nền trung bình; tăng mạnh với một domain, kể cả ở tầng hiếm |
| Vẹt từ hiếm | `[.85, .70, .55, .35, .25, .20, .25, .40, .55, .65]` |
| Rất yếu | Gần 0 hoặc gần guessing floor trên hầu hết tầng |
| Gần ceiling | Gần 1 trên hầu hết tầng |

Hồ sơ chuyên sâu MUST được sinh ở cấp item/domain, không chỉ bằng một vector mean theo tầng.

Hồ sơ vẹt từ hiếm SHOULD có hai biến thể:

- thực sự trả lời đúng trong construct được đo;
- chỉ nhận diện hình thức, thất bại ở item nghĩa hoặc productive task.

Biến thể thứ hai kiểm tra validity của phép đo, không chỉ thiết kế mẫu.

### 14.5. Cơ chế sinh đáp án

Tối thiểu bốn họ:

1. finite-population nhị phân cố định;
2. 2PL/3PL IRT đúng với mô hình fit;
3. multidimensional IRT hoặc domain-specific mastery;
4. non-IRT: phi đơn điệu, guessing heterogeneity, local dependence.

Sensitivity scenarios:

- item difficulty calibration lệch;
- 5–20% items có DIF;
- fatigue làm xác suất giảm theo vị trí;
- routing prior lệch về người dùng trung bình;
- research frame thiếu overlap;
- dropout phụ thuộc năng lực hoặc độ khó;
- tầng có toàn đúng/toàn sai trong mẫu nhỏ.

### 14.6. Các estimator đối chứng

MUST so sánh:

1. naive pooled mean;
2. pooled post-stratification không hiệu chỉnh adaptive design;
3. screening-only stratified estimator;
4. estimator residual HT đề xuất;
5. IRT/model-based estimator;
6. model-assisted estimator nếu đã triển khai.

Các thiết kế so sánh SHOULD gồm:

- phân bổ đều với cùng tổng số scoring items;
- phân bổ theo `Nₕ`;
- routing có floor;
- routing không floor;
- oracle Neyman allocation dùng true within-stratum variance.

Đối chứng cố ý sai phải được gắn nhãn để phát hiện một simulation harness không đủ nhạy.

### 14.7. Metrics

Với `R` lần lặp:

```text
Bias = mean(T̂ᵣ − T)
NormalizedBias = Bias / N

RMSE = sqrt(mean((T̂ᵣ − T)²))
NormalizedRMSE = RMSE / N

Coverage95 = mean(Lᵣ ≤ T ≤ Uᵣ)
MeanIntervalWidth = mean(Uᵣ − Lᵣ)

EmpiricalVariance = variance(T̂ᵣ)
VarianceRatio = mean(V̂ᵣ) / EmpiricalVariance

MCSE_Bias = sd(T̂ᵣ − T) / sqrt(R)
MCSE_Coverage = sqrt(Coverage95 × (1 − Coverage95) / R)
```

Ngoài tổng thể, báo cáo:

- bias và RMSE từng tầng;
- kết quả từng hồ sơ;
- worst-case scenario;
- distribution của quota;
- item exposure;
- trọng số lớn nhất;
- tỷ lệ incomplete;
- calibration precision theo item và vùng năng lực.

### 14.8. Số lần lặp

- Smoke test: tối thiểu 500 phiên/scenario.
- CI regression test: tối thiểu 2.000 phiên/scenario.
- Release qualification: tối thiểu 10.000 phiên/scenario quan trọng.

Tại coverage khoảng 95%, 10.000 lần lặp cho MCSE khoảng 0,22 điểm phần trăm.

Mỗi scenario SHOULD chạy trên nhiều frame seeds, không chỉ nhiều sampling seeds của một frame.

### 14.9. Acceptance gates

#### Gate A — Design correctness

Trong Lớp A:

- không có vi phạm positivity;
- không có duplicate ngoài thiết kế;
- estimator khớp exact enumeration trên frame nhỏ;
- bias phù hợp với Monte Carlo error;
- census trả đúng tổng và phương sai bằng 0;
- khoảng exact/bounded không có bằng chứng under-coverage.

Điều kiện thực dụng cho từng scenario:

```text
abs(Bias) ≤ 3 × MCSE_Bias + numerical_tolerance
```

Khi chạy nhiều scenario, phải điều chỉnh kiểm định hoặc dùng tiêu chí tổng hợp đã khóa trước, tránh false alarm do multiple testing.

#### Gate B — Uncertainty

- Khoảng được công bố là 95% không được under-cover có ý nghĩa thống kê.
- Khoảng hypergeometric bảo thủ có thể over-cover.
- Phương pháp xấp xỉ phải được đánh giá riêng ở floor/ceiling.
- Khoảng rộng không bị coi là lỗi implementation nếu đúng thiết kế; phải được xử lý bằng tăng budget hoặc thay đổi phương pháp có công bố.

#### Gate C — Routing efficiency

Ở cùng scoring budget:

- aggregate RMSE SHOULD không cao hơn phân bổ đều;
- không hồ sơ quan trọng nào có RMSE cao hơn đối chứng quá 10% nếu không có phê duyệt;
- SHOULD có cải thiện rõ ở hồ sơ trung bình hoặc vùng ranh giới.

Đây là performance gate đề xuất, phải khóa trước release study.

Nếu routing phức tạp không vượt baseline, dùng baseline đơn giản.

### 14.10. Pseudocode mô phỏng

```text
function run_design_simulation(scenario, repetitions):
    frame = generate_frame(scenario.frame_seed, scenario.frame_config)
    y = generate_fixed_population_scores(frame, scenario.profile)
    truth = sum(y)

    rows = []

    for r in 1..repetitions:
        rng = seeded_rng(scenario.seed, r)

        S1 = plan_screening(frame, scenario.config, rng)
        Y1 = lookup(y, S1)

        S2 = plan_focused(frame, S1, Y1, scenario.config, rng)
        Y2 = lookup(y, S2)

        result = estimate_design_total(
            frame, S1, Y1, S2, Y2, persisted_plan()
        )

        assert_sampling_invariants()

        rows.append({
            "estimate": result.total,
            "truth": truth,
            "variance": result.standard_error ** 2,
            "lower": result.interval.lower,
            "upper": result.interval.upper,
            "quotas": persisted_plan().quotas
        })

    return compute_metrics_and_mcse(rows)
```

---

## 15. Test strategy

### 15.1. Unit tests

MUST có:

- quota tổng đúng và không vượt capacity;
- floor được giữ;
- tầng đã census;
- tầng còn một item;
- toàn đúng/toàn sai;
- frame không đều;
- missing response bị chặn;
- quota mutation sau khóa bị chặn;
- propensity khớp risk set;
- exact interval khớp implementation tham chiếu.

### 15.2. Exact enumeration

Trên frame nhỏ với 2–3 tầng:

1. liệt kê mọi screening sample;
2. tính quota theo đáp án;
3. liệt kê mọi focused sample hợp lệ;
4. tính xác suất của mỗi đường đi;
5. xác minh:

```text
Σ_path P(path) × T̂(path) = T
```

Test này SHOULD chứa routing phi tuyến mạnh để chứng minh estimator không chỉ đúng khi quota gần cố định.

### 15.3. Property-based tests

Các thuộc tính:

```text
0 ≤ T̂ ≤ N
T̂ = T khi quan sát census
đổi nhãn item trong cùng tầng không đổi phân phối estimator
thay đổi thứ tự hiển thị không đổi kết quả với y cố định
research responses không đổi estimator chính
```

### 15.4. Replay và reproducibility

Cùng frame, seed, config và đáp án screening MUST tạo cùng focused sample.

Audit replay MUST phát hiện:

- frame drift;
- RNG version mismatch;
- quota thay đổi;
- thiếu selection event;
- item bị thay thế thủ công.

---

## 16. Giám sát production

Theo dõi tối thiểu:

- quota và response rate theo tầng;
- conditional inclusion probabilities;
- trọng số lớn nhất;
- độ rộng khoảng tin cậy theo nhóm người dùng;
- chênh lệch design-based và model-based;
- exposure theo item;
- distribution của research items;
- calibration uncertainty;
- DIF/drift;
- dropout theo vị trí và độ khó;
- phiên vi phạm invariant.

Chênh lệch lớn giữa model-based và design-based là tín hiệu kiểm tra mô hình hoặc dữ liệu, không phải lý do tự động chọn estimator có kết quả đẹp hơn.

Không được đánh giá fairness chỉ bằng điểm trung bình giữa các nhóm; phải xem bias, coverage và measurement invariance theo nhóm.

---

## 17. Giới hạn đã biết

1. 70–100 câu không bảo đảm ước lượng rất chính xác trên frame lớn và người dùng có kiến thức không đồng đều.
2. Design-unbiased không đồng nghĩa construct-valid.
3. Screening chỉ có 2–3 items/tầng tạo tín hiệu routing khá nhiễu.
4. Exploration floor hy sinh một phần hiệu quả CAT thuần để bảo vệ suy luận quần thể.
5. Research 5–10 items/phiên cần tích lũy nhiều phiên để calibration đáng tin.
6. Exact conservative intervals có thể rộng.
7. Người dùng tự chọn tham gia không tạo mẫu đại diện cho toàn bộ người học.
8. Đáp án chịu order effects hoặc stochastic measurement cần mô hình bất định bổ sung.
9. Positivity lý thuyết không thay thế yêu cầu đủ exposure thực tế.

---

## 18. Definition of Done — P0.2

P0.2 chỉ được đánh dấu hoàn thành khi:

- [ ] Đơn vị từ vựng và estimand đã được phê duyệt.
- [ ] Frame 10 tầng có version và kích thước chính xác.
- [ ] Screening dùng stratified SRSWOR.
- [ ] Focused routing có floor và khóa quota trước Stage 2.
- [ ] Mọi đơn vị đủ điều kiện có xác suất chọn dương.
- [ ] Selection probabilities và risk sets được ghi log.
- [ ] Residual HT estimator được triển khai đúng.
- [ ] Research không bị gộp tùy tiện vào estimator chính.
- [ ] Khoảng bất định phù hợp loại điểm.
- [ ] Missingness và dropout có trạng thái rõ ràng.
- [ ] Exact enumeration tests vượt qua.
- [ ] Simulation bao gồm EFL yếu, trung bình, chuyên sâu và vẹt từ hiếm.
- [ ] Bias, RMSE và coverage được báo cáo cùng MCSE.
- [ ] Các release gates được khóa trước đánh giá cuối.
- [ ] Model-based output có nhãn và giả định riêng.
- [ ] Audit replay tái tạo được quá trình chọn mẫu.

---

## 19. Kết luận quy phạm

Thiết kế P0.2 lựa chọn nguyên tắc:

> **Dùng mô hình để quyết định nên hỏi nhiều ở đâu; dùng mẫu xác suất và bộ ước lượng đúng thiết kế để suy luận về toàn bộ frame.**

Công thức trung tâm là:

```text
Estimated vocabulary total
  = observed screening total
  + probability-weighted estimate of the unscreened remainder
```

Không có kỹ thuật weighting nào tự tạo được thông tin ở một phần quần thể có xác suất chọn bằng 0.

Vì vậy, focused routing MUST đi cùng exploration floor, propensity logging, estimator phù hợp và kiểm định coverage trên cả hồ sơ điển hình lẫn phi điển hình.