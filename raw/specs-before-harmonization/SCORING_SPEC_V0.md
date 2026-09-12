# SCORING_SPEC_V0.md

> **Readiness clarification from actual data:** [The supplied snapshot](../data/LAZZYBEE_SNAPSHOT_AUDIT.md) establishes content availability, not calibrated item parameters or latent word knowledge. The [offline design baseline](../../tools/lazzybee/README.md) estimates a finite-frame correct-response total and explicitly disallows public vocabulary claims. It is not an interchangeable implementation of the latent model below; cross-spec estimator/unit reconciliation remains required.

> **Dự án:** `vocabulary-research`  
> **Repository:** `itpro-vn/vocabulary-research`  
> **Hạng mục:** P0.3 — Scoring Engine baseline  
> **Phiên bản đặc tả:** `0.1.0`  
> **Trạng thái:** Proposed — cần phê duyệt trước khi phát hành  
> **Phạm vi:** Chấm điểm V0, điều kiện xuất điểm, bất định và hợp đồng dữ liệu  
> **Ngôn ngữ quy phạm:** MUST = bắt buộc; SHOULD = khuyến nghị; MAY = tùy chọn

**Lưu ý tích hợp:** Tài liệu này là đặc tả đề xuất cho dự án được chỉ định, không khẳng định cấu trúc mã nguồn, dữ liệu hiệu chuẩn hoặc API hiện tại của repository đã đáp ứng các yêu cầu dưới đây.

---

## 1. Mục tiêu và giới hạn

Scoring Engine V0 MUST:

1. Ước lượng năng lực nhận biết từ vựng, có điều chỉnh đoán mò và sai sót bất cẩn.
2. Phân biệt phản hồi sai, `Dont_Know`, timeout và bỏ dở.
3. Xuất điểm trên thang latent trait `theta` và, khi đủ điều kiện, thang số từ `V`.
4. Xuất khoảng bất định với tên gọi thống kê chính xác.
5. Từ chối xuất điểm khi bằng chứng không đủ hoặc không phù hợp mô hình.
6. Cho kết quả xác định, có thể tái hiện và kiểm toán.
7. Không diễn giải thiếu dữ liệu thành thiếu năng lực.

V0 MUST NOT:

- Sử dụng tỷ lệ đúng thô như ước lượng trực tiếp số từ đã biết.
- Áp dụng công thức “trừ điểm đoán mò” tuyến tính làm điểm chính thức.
- Ước lượng đồng thời mọi tham số câu hỏi và năng lực cá nhân từ một phiên ngắn.
- Khẳng định đo được toàn bộ vốn từ của một ngôn ngữ nếu miền từ vựng chưa được định nghĩa.
- Gọi Bayesian credible interval là frequentist confidence interval.
- Gọi độ lệch chuẩn posterior là CSEM theo nghĩa Fisher-information.

---

## 2. Đại lượng cần đo

### 2.1. Định nghĩa “biết từ”

V0 đo **khả năng nhận biết nghĩa trong điều kiện bài kiểm tra được quy định**, không mặc nhiên đo:

- Khả năng tự sản sinh từ.
- Khả năng dùng từ trong ngữ cảnh tự nhiên.
- Mọi nghĩa của một từ đa nghĩa.
- Khả năng ghi nhớ dài hạn.

Content manifest MUST chỉ rõ đơn vị đếm:

```text
count_unit = lemma | word_family | surface_form | sense
```

Một phiên bản điểm MUST dùng duy nhất một định nghĩa đơn vị đếm.

### 2.2. Latent trait

```text
theta ∈ ℝ
```

`theta` là năng lực tiềm ẩn trên thang do item bank và quy trình hiệu chuẩn xác lập.

Giá trị `theta = 0` không có nghĩa là “không biết từ nào”.

### 2.3. Điểm số từ

V0 định nghĩa:

```text
V(theta) = tổng xác suất nhận biết trên miền từ vựng tham chiếu
```

`V` là **số đơn vị từ vựng kỳ vọng có thể nhận biết**, không phải phép đếm xác minh trực tiếp từng từ người dùng biết.

Miền tham chiếu MUST có:

- `domain_id` và `domain_version`.
- Đơn vị đếm.
- Tổng kích thước `N`.
- Danh sách đơn vị hoặc các điểm đại diện cùng trọng số.
- Quy trình xây dựng và giới hạn đại diện.

Nếu không có ánh xạ miền hợp lệ, Scoring Engine MUST NOT xuất điểm count.

---

## 3. Mô hình toán học V0

### 3.1. Phân rã nhận biết, đoán mò và bất cẩn

Với câu hỏi `i`:

```text
K_i ∈ {0, 1}

p_i(theta) = P(K_i = 1 | theta)
          = sigmoid(a_i × (theta − b_i))

sigmoid(x) = 1 / (1 + exp(−x))
```

Trong đó:

| Ký hiệu | Ý nghĩa |
|---|---|
| `K_i` | Trạng thái nhận biết tiềm ẩn trong mô hình |
| `p_i(theta)` | Xác suất nhận biết |
| `a_i > 0` | Độ phân biệt |
| `b_i` | Độ khó |
| `g_i` | Xác suất chọn đúng khi không nhận biết, với điều kiện có thử trả lời |
| `s_i` | Xác suất chọn sai khi nhận biết, với điều kiện có thử trả lời |

Khi không có lựa chọn `Dont_Know`:

```text
P(correct | theta)
  = p_i(theta) × (1 − s_i)
    + (1 − p_i(theta)) × g_i

  = g_i + (1 − s_i − g_i) × p_i(theta)
```

Ràng buộc:

```text
0 ≤ g_i < 1
0 ≤ s_i < 1
g_i + s_i < 1
```

**Diễn giải quan trọng:**

- `p` không phải tỷ lệ trả lời đúng.
- `g` không phải xác suất một người “có hành vi đoán”.
- `s` không phải tỷ lệ sai quan sát được của cả phiên.
- `1 / m` chỉ là giả định đoán đều với `m` phương án hữu hiệu, không phải chân lý thực nghiệm.
- Một câu đúng không đủ chứng minh người dùng biết từ đó.

### 3.2. Mô hình `Dont_Know`

V0 sử dụng likelihood phân loại ba kết quả:

```text
Y_i ∈ {correct, incorrect, dont_know}
```

Bổ sung:

```text
dK_i = P(dont_know | K_i = 1)
dU_i = P(dont_know | K_i = 0)
```

Hai tham số này mô tả hành vi chọn “Tôi không biết”, không phải tham số năng lực.

Đặt:

```text
A_i = (1 − dK_i) × (1 − s_i)
B_i = (1 − dU_i) × g_i

C_i = (1 − dK_i) × s_i
D_i = (1 − dU_i) × (1 − g_i)
```

Xác suất phản hồi:

```text
q_correct_i(theta)
  = p_i(theta) × A_i + (1 − p_i(theta)) × B_i

q_incorrect_i(theta)
  = p_i(theta) × C_i + (1 − p_i(theta)) × D_i

q_dont_know_i(theta)
  = p_i(theta) × dK_i + (1 − p_i(theta)) × dU_i
```

Bất biến:

```text
q_correct + q_incorrect + q_dont_know = 1
```

Cấu hình V0 SHOULD thỏa:

```text
0 ≤ dK_i < dU_i < 1
A_i > B_i
```

Như vậy:

- Chọn `Dont_Know` thường là bằng chứng nghiêng về năng lực thấp hơn ở câu đó.
- `Dont_Know` không đồng nhất về likelihood với trả lời sai.
- Không có “điểm phạt” riêng cho việc chọn `Dont_Know`.
- Không tính `Dont_Know` là phương án nhiễu khi xác định `m`.

Mô hình này giả định các tham số hành vi đã được cố định bằng cấu hình hoặc hiệu chuẩn. Khác biệt về mức độ tự tin và chiến lược trả lời giữa người dùng có thể gây sai lệch; V0 MUST công bố hạn chế này.

### 3.3. Quy tắc tham số V0

Trong một lần chấm:

```text
a_i, b_i, g_i, s_i, dK_i, dU_i đều cố định
Chỉ theta được suy luận cho người dùng
```

MUST NOT suy luận `s_i` từ số câu sai của chính phiên rồi dùng lại để chấm phiên đó.

Cấu hình phục vụ phát triển MAY dùng giả định:

```text
a_i = 1
g_i = 1 / m_i
s_i = 0.02
dK_i = 0.02
dU_i = 0.25
```

Các giá trị trên:

- Chỉ là giả định khởi tạo để triển khai và mô phỏng.
- Không phải thông số đã được xác thực cho dự án.
- MUST được gắn `parameter_source = assumed`.
- MUST NOT đủ điều kiện cho điểm count chính thức dành cho nghiên cứu nếu chưa có phê duyệt/kiểm định phù hợp.

`b_i` MUST có nguồn gốc rõ ràng. Nhãn tần suất từ không tự động tương đương tham số độ khó IRT.

---

## 4. Trạng thái phản hồi và dữ liệu thiếu

### 4.1. Trạng thái chuẩn hóa

| Trạng thái | Định nghĩa | Đưa vào likelihood? |
|---|---|---:|
| `correct` | Chọn đáp án đúng, sự kiện hợp lệ | Có |
| `incorrect` | Chọn đáp án sai, sự kiện hợp lệ | Có |
| `dont_know` | Chủ động chọn “Tôi không biết” | Có |
| `timeout` | Hết thời gian, chưa có phản hồi hợp lệ | Không |
| `omitted` | Câu đã hiển thị nhưng không có phản hồi hợp lệ | Không |
| `not_presented` | Câu chưa được hiển thị | Không |
| `invalid` | Sự kiện không hợp lệ hoặc không thể xác minh | Không |

`rapid_guessing` là cờ chất lượng, không phải đáp án.

`incomplete` và `abandoned` là trạng thái phiên, không phải kết quả câu hỏi.

### 4.2. `Dont_Know`

Scoring Engine MUST:

- Bảo toàn lựa chọn này như một phản hồi quan sát riêng.
- Không biến nó thành timeout.
- Không loại nó khỏi mẫu chỉ vì không phải đáp án đúng.
- Không đánh dấu thiếu nghiêm túc chỉ vì tỷ lệ `Dont_Know` cao.

### 4.3. Timeout

V0 không mô hình hóa tốc độ làm bài.

Vì vậy:

```text
timeout đóng góp log-likelihood = 0
```

Timeout:

- Không được tính là sai.
- Không được tính là `Dont_Know`.
- Vẫn tham gia kiểm tra tỷ lệ thiếu dữ liệu.
- Có thể làm phiên không đủ điều kiện xuất điểm.

Việc bỏ qua timeout chỉ hợp lý khi cơ chế thiếu dữ liệu không làm sai lệch nghiêm trọng suy luận sau khi điều kiện hóa trên thiết kế bài kiểm tra. Nếu timeout phụ thuộc mạnh vào độ khó hoặc năng lực, V0 có thể thiên lệch.

Bài kiểm tra có mục tiêu đo cả tốc độ MUST dùng đặc tả khác.

### 4.4. Bỏ dở và chưa hoàn thành

Không gán sai cho các câu chưa được làm.

Phiên `incomplete` hoặc `abandoned` MAY được chấm nếu:

- Đủ số phản hồi hợp lệ.
- Đạt coverage.
- Đạt ngưỡng thông tin.
- Không vi phạm chất lượng.
- Thiết kế cho phép chấm trên phần bài đã hoàn thành.

Kết quả MUST chứa:

```text
completion_status
is_partial = true
```

Nếu không đáp ứng điều kiện:

```text
status = insufficient_evidence
```

Không ngoại suy số câu sai cho phần chưa làm.

---

## 5. Quy trình xử lý bắt buộc

```text
1. Xác thực session, item bank và các phiên bản cấu hình.
2. Khử trùng lặp, kiểm tra thứ tự và tính hợp lệ của sự kiện.
3. Chuẩn hóa trạng thái câu trả lời.
4. Tính cờ chất lượng và dữ liệu thiếu.
5. Loại các phản hồi không được phép đưa vào likelihood.
6. Kiểm tra điều kiện tối thiểu trước suy luận.
7. Tính posterior của theta.
8. Ánh xạ posterior sang V nếu miền tham chiếu hợp lệ.
9. Tính credible interval và CSEM.
10. Kiểm tra điều kiện sau suy luận.
11. Xuất điểm hoặc insufficient_evidence.
12. Lưu bản ghi kiểm toán.
```

Frontend MUST NOT quyết định điểm, ngưỡng chất lượng hoặc đáp án đúng.

---

## 6. Bayesian scoring

### 6.1. Prior

Prior mặc định:

```text
theta ~ Normal(0, 1)
```

Prior MUST được định nghĩa trên cùng thang với item bank.

Thay đổi prior là thay đổi `scoring_config_version`.

V0 MUST NOT âm thầm thay prior theo giới tính, tuổi, dân tộc hoặc thuộc tính nhạy cảm.

### 6.2. Likelihood

Với tập phản hồi được sử dụng `R`:

```text
L(theta) = ∏ q_i,y_i(theta), với i ∈ R

log L(theta) = Σ log q_i,y_i(theta)
```

Giả định:

- Độc lập cục bộ có điều kiện theo `theta`.
- Tham số item cố định.
- Các phản hồi bị loại không được tính lại thông qua số câu đúng/sai.
- Không có phụ thuộc chưa xử lý từ việc lặp cùng một từ hoặc cung cấp gợi ý.

### 6.3. Posterior

```text
posterior(theta | responses)
  ∝ prior(theta) × L(theta)
```

Điểm theta chính thức:

```text
theta_eap = E[theta | responses]
```

V0 chọn EAP để tránh ước lượng vô hạn ở mẫu toàn đúng hoặc toàn sai.

### 6.4. Grid quadrature

Cấu hình khởi tạo:

```text
theta_grid_min = −6
theta_grid_max = 6
theta_grid_step = 0.01
```

MUST dùng log-space:

```text
log_weight_k
  = log_prior(theta_k)
    + log_likelihood(theta_k)
    + log_quadrature_weight_k

weight_k = exp(log_weight_k − logsumexp(log_weight))
```

MUST kiểm tra khối lượng posterior sát biên. Nếu vượt ngưỡng:

1. Mở rộng miền tích phân theo cấu hình.
2. Tính lại.
3. Nếu vẫn không đạt, trả lỗi số học nội bộ; không xuất điểm bị cắt biên.

Ngưỡng đề xuất:

```text
posterior_mass_in_outer_0_2_each_side ≤ 0.0001
```

---

## 7. Ánh xạ theta sang số từ

### 7.1. Miền đầy đủ

Nếu có `N` đơn vị với tham số nhận biết:

```text
p_j_domain(theta)
  = sigmoid(a_j_domain × (theta − b_j_domain))

V(theta) = Σ p_j_domain(theta), j = 1..N
```

### 7.2. Miền phân tầng hoặc xấp xỉ trọng số

```text
V(theta) = Σ w_j × p_j_domain(theta)

w_j > 0
Σ w_j = N
```

Trọng số là số đơn vị được đại diện, không mặc nhiên là trọng số tần suất xuất hiện trong văn bản.

Tham số miền MUST nằm trên cùng thang theta với item bank.

Không được lấy trung bình xác suất của các câu được chọn thích nghi rồi nhân `N`: mẫu thích nghi không nhất thiết đại diện miền từ vựng.

### 7.3. Điểm count chính thức

```text
V_eap = E[V(theta) | responses]
      = Σ weight_k × V(theta_k)
```

MUST dùng công thức trên, không thay bằng:

```text
V(theta_eap)
```

Hai đại lượng thường khác nhau do ánh xạ phi tuyến.

Khoảng giá trị:

```text
0 ≤ V_eap ≤ N
```

API giữ số thực; UI MAY làm tròn để hiển thị.

### 7.4. Không đồng nhất với số từ biết thực tế

V0 suy luận bất định của hàm `V(theta)`.

V0 không mặc định xuất posterior predictive interval cho:

```text
T = Σ K_j
```

Nếu cần phân phối của `T`, phải đặc tả thêm biến thiên trạng thái từng từ và phụ thuộc giữa các từ. Không được gọi khoảng của `V(theta)` là khoảng dự báo cho `T`.

---

## 8. Ba khái niệm bất định

### 8.1. Bayesian credible interval — đầu ra chính thức V0

Khoảng equal-tailed 95%:

```text
theta_lower = Q_0.025(theta | responses)
theta_upper = Q_0.975(theta | responses)

V_lower = Q_0.025(V(theta) | responses)
V_upper = Q_0.975(V(theta) | responses)
```

Diễn giải:

> Với mô hình, prior, tham số item và dữ liệu đã sử dụng, posterior gán xác suất 95% cho đại lượng nằm trong khoảng này.

Khoảng V có thể bất đối xứng quanh `V_eap`.

Định dạng biên độ:

```text
error_minus = V_eap − V_lower
error_plus  = V_upper − V_eap
```

Nếu cần một nửa độ rộng để mô tả:

```text
interval_half_width = (V_upper − V_lower) / 2
```

MUST NOT trình bày `V_eap ± interval_half_width` như tương đương khoảng gốc nếu tâm khoảng không phải `V_eap`.

### 8.2. Frequentist confidence interval — không phải đầu ra V0 mặc định

Một confidence interval 95% có diễn giải theo lấy mẫu lặp:

> Khi lặp lại quy trình lấy mẫu và xây dựng khoảng, khoảng 95% các khoảng sẽ bao phủ tham số thật, dưới các giả định tương ứng.

Không diễn giải nó là xác suất posterior của tham số.

Xấp xỉ Wald, nếu điều kiện phù hợp:

```text
theta_CI ≈ theta_MLE ± 1.96 × SE_MLE
```

Công thức này không tự động hợp lệ cho:

- EAP với prior.
- Mẫu toàn đúng/toàn sai.
- Mẫu ngắn.
- Thiết kế thích nghi chưa được kiểm định coverage.
- Quy trình lọc dữ liệu và dừng bài phức tạp.

V0:

```text
confidence_interval = null
```

Nếu triển khai sau này, MUST ghi rõ phương pháp, thiết kế lấy mẫu, xử lý nuisance parameters và kết quả kiểm định coverage.

### 8.3. CSEM — sai số đo có điều kiện

CSEM dựa trên thông tin đo tại một mức năng lực, không phải xác suất posterior.

Với mô hình phân loại:

```text
p'_i(theta) = a_i × p_i(theta) × (1 − p_i(theta))

q'_correct_i   = p'_i × (A_i − B_i)
q'_incorrect_i = p'_i × (C_i − D_i)
q'_dont_know_i = p'_i × (dK_i − dU_i)

I_i(theta)
  = Σ_c [q'_i,c(theta)² / q_i,c(theta)]

I_test(theta) = Σ_i∈R I_i(theta)
```

Hạng có xác suất bằng 0 đồng nhất và đạo hàm bằng 0 đóng góp 0.

Với mô hình nhị phân không có `Dont_Know`:

```text
q_i = g_i + (1 − s_i − g_i) × p_i

q'_i = (1 − s_i − g_i) × a_i × p_i × (1 − p_i)

I_i(theta) = q'_i² / [q_i × (1 − q_i)]
```

CSEM theta:

```text
CSEM_theta(theta) = 1 / sqrt(I_test(theta))
```

V0 báo cáo tại:

```text
theta_eval = theta_eap
```

Không cộng precision của prior vào `I_test` rồi vẫn gọi kết quả là CSEM Fisher-information.

### 8.4. CSEM trên thang count

Đạo hàm ánh xạ:

```text
V'(theta)
  = Σ w_j × a_j_domain × p_j_domain(theta)
      × (1 − p_j_domain(theta))
```

Delta-method:

```text
CSEM_count(theta)
  ≈ abs(V'(theta)) × CSEM_theta(theta)
```

Đơn vị:

| Đại lượng | Đơn vị |
|---|---|
| `CSEM_theta` | Latent trait |
| `CSEM_count` | Số đơn vị từ vựng |
| `posterior_sd_theta` | Latent trait |
| `posterior_sd_count` | Số đơn vị từ vựng |

CSEM count là xấp xỉ cục bộ. Nó có thể nhỏ gần vùng ánh xạ bão hòa dù năng lực chưa được xác định tốt.

MUST NOT dùng CSEM count nhỏ như bằng chứng duy nhất rằng phiên đủ chất lượng.

### 8.5. Độ lệch chuẩn posterior

```text
posterior_sd_theta
  = sqrt(E[(theta − theta_eap)² | responses])

posterior_sd_count
  = sqrt(E[(V(theta) − V_eap)² | responses])
```

Hai trường này MUST mang tên riêng, không thay tên thành CSEM.

### 8.6. Phạm vi bất định được báo cáo

Khoảng V0 điều kiện hóa trên:

- Tham số câu hỏi cố định.
- Tham số hành vi `dK`, `dU`, `g`, `s` cố định.
- Ánh xạ miền cố định.
- Mô hình một chiều.
- Quy tắc lọc và cơ chế thiếu dữ liệu giả định.

Khoảng chưa bao gồm đầy đủ sai số hiệu chuẩn, sai lệch miền, sai mô hình hoặc khác biệt chiến lược trả lời.

---

## 9. Điều kiện `insufficient_evidence`

### 9.1. Nguyên tắc

Không xuất điểm khi bằng chứng không đủ hỗ trợ diễn giải đã cam kết.

```text
status = insufficient_evidence
score = null
uncertainty = null
```

Điểm posterior tính nội bộ trước khi bị từ chối MUST NOT được đưa sang UI như điểm chính thức.

Không quy đổi trạng thái này thành điểm 0.

### 9.2. Ngưỡng chính sách ban đầu

Các ngưỡng dưới đây là **policy baseline cần được kiểm định**, không phải hằng số đo lường phổ quát.

| Điều kiện | Giá trị đề xuất |
|---|---:|
| Phản hồi được sử dụng tối thiểu | 30 |
| Phản hồi hợp lệ để đánh giá tỷ lệ rapid tối thiểu | 10 |
| Tỷ lệ rapid tối đa | 0.20 |
| Tỷ lệ thiếu trên câu đã hiển thị tối đa | 0.30 |
| Test information tại EAP tối thiểu | 4.0 |
| Độ rộng credible interval count tối đa | `0.40 × N` |
| Item hiệu chuẩn/được phê duyệt trong tập sử dụng | 100% |
| Coverage | Theo test blueprint đã version hóa |

Nếu thiết kế bài ngắn hơn 30 câu, MUST phê duyệt cấu hình riêng dựa trên mô phỏng và dữ liệu pilot; không âm thầm hạ ngưỡng.

### 9.3. Rapid-guessing

```text
rapid_i = valid_timing_i
          AND response_time_ms_i < rapid_threshold_ms_i
```

`rapid_threshold_ms_i` SHOULD được ước lượng từ pilot, có xét:

- Độ dài nội dung.
- Loại câu hỏi.
- Thiết bị và phương thức tương tác.
- Accessibility accommodations.

MUST NOT dùng thời gian mạng đơn thuần làm thời gian suy nghĩ.

V0:

- Loại phản hồi bị gắn cờ rapid khỏi likelihood.
- Tính cờ trước khi xét đúng/sai.
- Không chỉ loại câu rapid trả lời sai.
- Từ chối cả phiên nếu tỷ lệ rapid vượt ngưỡng.

```text
rapid_fraction
  = số phản hồi rapid
    / số phản hồi submitted có timing hợp lệ
```

Nếu timing là điều kiện bắt buộc nhưng dữ liệu timing không đủ đáng tin:

```text
reason_code = timing_unavailable
```

Loại rapid là một giả định xử lý dữ liệu, không phải mô hình mixture đầy đủ. MUST đánh giá thiên lệch của quy tắc này trong mô phỏng.

### 9.4. Không nghiêm túc

Có thể từ chối khi:

- Rapid vượt ngưỡng.
- Có bằng chứng phiên tự động hóa hoặc dữ liệu giả mạo.
- Thất bại tiêu chí chất lượng độc lập đã được xác thực.
- Vi phạm quy tắc kiểm tra đầu vào.

Không được tự động suy ra thiếu nghiêm túc chỉ từ:

- Điểm thấp.
- Tỷ lệ sai cao.
- Tỷ lệ `Dont_Know` cao.
- Toàn đúng.
- Chọn lặp cùng vị trí đáp án.
- Bỏ dở vì lý do không xác định.

Một chỉ báo hành vi đơn lẻ chưa được kiểm định chỉ SHOULD tạo cảnh báo.

### 9.5. Reason codes

```text
too_few_usable_responses
excessive_rapid_guessing
excessive_missingness
timing_unavailable
coverage_not_met
low_test_information
posterior_too_wide
engagement_check_failed
invalid_response_integrity
```

Thiếu domain mapping hoặc cấu hình sai là vấn đề hệ thống, không phải lỗi bằng chứng của người dùng:

```text
status = scoring_unavailable
```

Lỗi payload có thể trả HTTP 4xx; lỗi số học/hạ tầng trả lỗi có thể retry, không giả thành điểm thấp.

---

## 10. Hợp đồng dữ liệu

### 10.1. Input tối thiểu

```json
{
  "session_id": "session-123",
  "completion_status": "completed",
  "item_bank_version": "bank-v1",
  "domain_version": "domain-v1",
  "scoring_config_version": "v0-policy-1",
  "responses": [
    {
      "item_id": "item-001",
      "presentation_id": "presentation-001",
      "selected_option_id": "option-b",
      "response_kind": "answer",
      "response_time_ms": 4200,
      "timing_valid": true
    },
    {
      "item_id": "item-002",
      "presentation_id": "presentation-002",
      "selected_option_id": null,
      "response_kind": "dont_know",
      "response_time_ms": 3100,
      "timing_valid": true
    }
  ]
}
```

Server MUST tự xác định `correct`/`incorrect` từ item bank bất biến.

Cần manifest riêng xác định câu đã hiển thị, timeout và câu chưa hiển thị; không suy ra toàn bộ từ danh sách submitted responses.

### 10.2. Output thành công

Các số dưới đây chỉ minh họa schema:

```json
{
  "status": "scored",
  "scoring_version": "0.1.0",
  "scoring_config_version": "v0-policy-1",
  "item_bank_version": "bank-v1",
  "domain_version": "domain-v1",
  "completion_status": "completed",
  "is_partial": false,
  "score": {
    "theta_eap": 0.42,
    "vocabulary_count_eap": 8420.6,
    "domain_size": 20000,
    "count_unit": "lemma",
    "estimand": "expected_recognizable_units"
  },
  "uncertainty": {
    "credible_interval": {
      "method": "bayesian_equal_tailed",
      "level": 0.95,
      "theta": [-0.12, 0.98],
      "count": [6910.0, 10180.0]
    },
    "posterior_sd_theta": 0.28,
    "posterior_sd_count": 840.0,
    "csem": {
      "method": "conditional_fisher_delta",
      "theta_evaluation": 0.42,
      "theta": 0.31,
      "count": 910.0
    },
    "confidence_interval": null
  },
  "evidence": {
    "presented_count": 50,
    "submitted_count": 48,
    "usable_count": 46,
    "dont_know_count": 7,
    "timeout_count": 2,
    "rapid_excluded_count": 2,
    "rapid_fraction": 0.0417,
    "missing_fraction": 0.04,
    "test_information": 10.41
  },
  "warnings": []
}
```

### 10.3. Output không đủ bằng chứng

```json
{
  "status": "insufficient_evidence",
  "completion_status": "abandoned",
  "is_partial": true,
  "score": null,
  "uncertainty": null,
  "reason_codes": [
    "too_few_usable_responses",
    "coverage_not_met"
  ],
  "evidence": {
    "presented_count": 15,
    "usable_count": 11
  },
  "recommended_action": "retake_or_continue"
}
```

---

## 11. Mã giả Python cho Scoring Engine

Mã dưới đây mô tả thuật toán; các hàm chuẩn hóa, coverage và version lookup MUST được triển khai theo hợp đồng ở trên.

```python
import math
import numpy as np


def sigmoid(x):
    # Stable for scalar or ndarray.
    return np.exp(-np.logaddexp(0.0, -x))


def logsumexp(x):
    m = np.max(x)
    return m + np.log(np.sum(np.exp(x - m)))


def category_probabilities(theta, item):
    p = sigmoid(item.a * (theta - item.b))

    A = (1 - item.dK) * (1 - item.s)
    B = (1 - item.dU) * item.g
    C = (1 - item.dK) * item.s
    D = (1 - item.dU) * (1 - item.g)

    return {
        "correct": p * A + (1 - p) * B,
        "incorrect": p * C + (1 - p) * D,
        "dont_know": p * item.dK + (1 - p) * item.dU,
    }


def item_information(theta, item):
    p = float(sigmoid(item.a * (theta - item.b)))
    dp = item.a * p * (1 - p)

    A = (1 - item.dK) * (1 - item.s)
    B = (1 - item.dU) * item.g
    C = (1 - item.dK) * item.s
    D = (1 - item.dU) * (1 - item.g)

    q = category_probabilities(theta, item)
    dq = {
        "correct": dp * (A - B),
        "incorrect": dp * (C - D),
        "dont_know": dp * (item.dK - item.dU),
    }

    information = 0.0
    for category in q:
        probability = float(q[category])
        derivative = dq[category]

        if probability == 0.0 and derivative == 0.0:
            continue

        if probability <= 0.0:
            raise NumericalError("Invalid category probability")

        information += derivative ** 2 / probability

    return information


def domain_count(theta, domain):
    value = np.zeros_like(theta, dtype=float)
    for unit in domain.units:
        p = sigmoid(unit.a * (theta - unit.b))
        value += unit.weight * p
    return value


def domain_derivative(theta, domain):
    value = 0.0
    for unit in domain.units:
        p = float(sigmoid(unit.a * (theta - unit.b)))
        value += unit.weight * unit.a * p * (1 - p)
    return value


def weighted_quantile(values, weights, probability):
    order = np.argsort(values)
    values = np.asarray(values)[order]
    weights = np.asarray(weights)[order]
    cdf = np.cumsum(weights)
    index = np.searchsorted(cdf, probability, side="left")
    return float(values[min(index, len(values) - 1)])


def posterior_on_grid(usable, bank, config, lower, upper):
    grid = np.linspace(
        lower,
        upper,
        round((upper - lower) / config.grid_step) + 1
    )

    sigma = config.prior_sd
    mu = config.prior_mean
    log_prior = -0.5 * ((grid - mu) / sigma) ** 2

    # Trapezoidal quadrature weights.
    quad = np.ones(len(grid)) * (grid[1] - grid[0])
    quad[0] *= 0.5
    quad[-1] *= 0.5
    log_weights = log_prior + np.log(quad)

    for response in usable:
        item = bank[response.item_id]
        q = category_probabilities(grid, item)[response.category]

        # Zero probability must remain zero likelihood.
        # Do not silently invent positive probability via clipping.
        with np.errstate(divide="ignore"):
            log_weights += np.log(q)

    if not np.any(np.isfinite(log_weights)):
        raise NumericalError("All posterior weights are zero")

    normalizer = logsumexp(log_weights)
    weights = np.exp(log_weights - normalizer)
    return grid, weights


def score_session(session, bank, domain, config):
    validate_versions(session, bank, domain, config)
    validate_bank_and_domain(bank, domain, config)

    normalized = normalize_and_validate_events(session, bank)
    quality = compute_quality_flags(normalized, config)

    usable = [
        response
        for response in normalized.responses
        if response.category in {
            "correct", "incorrect", "dont_know"
        }
        and response.integrity_valid
        and not response.rapid_flag
    ]

    reasons = pre_scoring_gates(
        normalized, usable, quality, config
    )
    if reasons:
        return insufficient_evidence(session, reasons, quality)

    lower = config.grid_min
    upper = config.grid_max

    for attempt in range(config.max_grid_expansions + 1):
        grid, weights = posterior_on_grid(
            usable, bank, config, lower, upper
        )

        left_mass = float(
            weights[grid <= lower + 0.2].sum()
        )
        right_mass = float(
            weights[grid >= upper - 0.2].sum()
        )

        if max(left_mass, right_mass) <= config.edge_mass_limit:
            break

        lower -= config.grid_expansion_size
        upper += config.grid_expansion_size
    else:
        raise NumericalError("Posterior grid boundary failure")

    theta_eap = float(np.sum(weights * grid))
    theta_sd = math.sqrt(
        float(np.sum(weights * (grid - theta_eap) ** 2))
    )

    theta_interval = [
        weighted_quantile(grid, weights, 0.025),
        weighted_quantile(grid, weights, 0.975),
    ]

    count_values = domain_count(grid, domain)
    count_eap = float(np.sum(weights * count_values))
    count_sd = math.sqrt(
        float(np.sum(weights * (count_values - count_eap) ** 2))
    )

    count_interval = [
        weighted_quantile(count_values, weights, 0.025),
        weighted_quantile(count_values, weights, 0.975),
    ]

    information = sum(
        item_information(theta_eap, bank[r.item_id])
        for r in usable
    )

    if information <= 0:
        return insufficient_evidence(
            session, ["low_test_information"], quality
        )

    csem_theta = 1 / math.sqrt(information)
    csem_count = (
        abs(domain_derivative(theta_eap, domain))
        * csem_theta
    )

    reasons = post_scoring_gates(
        information=information,
        count_interval=count_interval,
        domain_size=domain.size,
        config=config,
    )

    if reasons:
        return insufficient_evidence(session, reasons, quality)

    return build_scored_result(
        session=session,
        theta_eap=theta_eap,
        count_eap=count_eap,
        theta_interval=theta_interval,
        count_interval=count_interval,
        posterior_sd_theta=theta_sd,
        posterior_sd_count=count_sd,
        csem_theta=csem_theta,
        csem_count=csem_count,
        information=information,
        quality=quality,
        config=config,
    )
```

### 11.1. Yêu cầu triển khai bổ sung

- Dùng `float64`.
- Các lỗi xác suất/NaN MUST làm chấm thất bại rõ ràng.
- API MUST idempotent với cùng input và cùng phiên bản.
- Không đưa lời giải hoặc feedback trước khi phản hồi câu đó được khóa.
- Trong V0, một đơn vị từ không SHOULD được đo lặp như bằng chứng độc lập trong cùng phiên.
- Nếu cho phép đổi đáp án, manifest MUST quy định một lần khóa phản hồi duy nhất và cách đo thời gian tương ứng.
- Với CAT, MUST lưu lịch sử item selection và stopping rule. Likelihood chỉ bỏ qua cơ chế chọn câu khi cơ chế này là ignorable theo thiết kế đã phê duyệt.

---

## 12. Kiểm thử bắt buộc

### 12.1. Unit tests toán học

1. `p_i(theta)` tăng theo theta khi `a_i > 0`.
2. Tổng xác suất ba kết quả bằng 1 trong sai số số học.
3. Khi `dK = dU = 0`, mô hình trở về công thức nhị phân.
4. Khi `g = s = 0` và không có `Dont_Know`, `P(correct) = p`.
5. Giới hạn ở năng lực rất thấp/cao khớp với mô hình mixture.
6. Posterior weights có tổng bằng 1.
7. `0 ≤ V ≤ N`.
8. `V_eap` được tính từ toàn posterior, không từ riêng EAP theta.
9. CSEM dùng likelihood information, không cộng prior precision.
10. Không có chia cho 0 hoặc xuất JSON chứa `NaN`/`Infinity`.

### 12.2. Tests trạng thái

- Thêm câu `not_presented` không thay đổi posterior.
- Thêm timeout không làm posterior giảm trực tiếp, nhưng có thể làm gate thất bại.
- `Dont_Know` và incorrect có thể tạo posterior khác nhau.
- Rapid đúng và rapid sai đều bị loại bằng cùng quy tắc.
- Phiên toàn `Dont_Know` không tự động bị gắn “không nghiêm túc”.
- Phiên toàn đúng vẫn có điểm hữu hạn nhờ prior, nhưng có thể thiếu thông tin.
- Phiên bỏ dở có đủ bằng chứng được xuất điểm partial.
- Phiên bỏ dở không đủ bằng chứng không nhận điểm 0.
- Sự kiện trùng không được nhân đôi bằng chứng.

### 12.3. Numerical tests

So sánh lưới bước `0.01` với `0.005` trên tập fixture:

```text
abs(theta_eap_coarse − theta_eap_fine) < 0.005
abs(V_eap_coarse − V_eap_fine) < max(1, 0.0005 × N)
```

Quantile tests MUST tính đến sai số rời rạc của lưới.

### 12.4. Simulation và pilot

Trước phát hành điểm nghiên cứu:

- Mô phỏng theta thấp, trung bình, cao.
- Mô phỏng các mức đoán, bất cẩn và sử dụng `Dont_Know`.
- Đánh giá bias, RMSE và tỷ lệ từ chối xuất điểm.
- Đánh giá độ nhạy với prior và tham số hành vi.
- Kiểm tra timeout phụ thuộc năng lực.
- Kiểm tra rapid filtering và stopping rule.
- Kiểm tra item fit, dimensionality và local dependence.
- Kiểm tra fairness và measurement invariance trên các nhóm phù hợp.

Coverage thực nghiệm của credible interval MUST được mô tả là kết quả kiểm định, không mặc định bằng 95% tại mọi theta.

---

## 13. Hiển thị và diễn giải cho người dùng

Cách diễn đạt khuyến nghị:

> Ước lượng khả năng nhận biết của bạn là khoảng 8.400 đơn vị từ trong miền tham chiếu của bài kiểm tra. Khoảng khả tín Bayesian 95% là 6.900–10.200, theo mô hình và dữ liệu đã sử dụng.

Không dùng:

> Bạn chắc chắn biết 8.400 từ.

Không dùng:

> Điểm chính xác 95%.

Với `insufficient_evidence`:

> Chưa đủ dữ liệu đáng tin cậy để ước lượng. Bạn có thể tiếp tục hoặc làm lại bài kiểm tra.

Không hiển thị thông báo quy kết “bạn gian lận” chỉ từ rapid flags hoặc mẫu đáp án.

---

## 14. Versioning, audit và tái lập

Mỗi kết quả MUST gắn:

```text
scoring_spec_version
scoring_engine_version
scoring_config_version
item_bank_version
domain_version
test_blueprint_version
prior_version
quality_policy_version
```

Audit record MUST lưu hoặc tham chiếu bất biến tới:

- Phản hồi chuẩn hóa.
- Item đã hiển thị và thứ tự.
- Câu được dùng và bị loại.
- Lý do loại.
- Tham số chấm.
- Quy tắc dừng.
- Thông số grid và kiểm tra biên.
- Kết quả gates.
- Hash input và cấu hình.

Không ghi đè điểm cũ khi thay cấu hình. Re-scoring MUST tạo bản ghi mới có liên kết tới bản cũ.

---

## 15. Tiêu chí hoàn thành P0.3

P0.3 chỉ hoàn thành khi:

- [ ] Mô hình `p`, `g`, `s`, `dK`, `dU` được triển khai và kiểm thử.
- [ ] `Dont_Know`, timeout và abandonment có xử lý riêng.
- [ ] Có posterior theta xác định và ổn định số học.
- [ ] Có miền count hợp lệ, hoặc hệ thống từ chối xuất count rõ ràng.
- [ ] Điểm count là `E[V(theta) | responses]`.
- [ ] Credible interval, confidence interval và CSEM có tên gọi đúng.
- [ ] Quality gates chạy trước và sau suy luận.
- [ ] `insufficient_evidence` không rò rỉ điểm nội bộ ra UI.
- [ ] Các ngưỡng chính sách được version hóa.
- [ ] Có unit tests, numerical tests và simulation fixtures.
- [ ] Có audit trail và API idempotent.
- [ ] Tham số giả định không được trình bày như dữ liệu hiệu chuẩn.
- [ ] Có phê duyệt đo lường học trước khi dùng điểm count cho kết luận nghiên cứu.

---

## 16. Tóm tắt quyết định V0

| Chủ đề | Quyết định |
|---|---|
| Mô hình nhận biết | Logistic latent trait |
| Đoán mò | Thành phần riêng `g`, có điều kiện theo việc thử trả lời |
| Bất cẩn | Thành phần riêng `s`, cố định trong lần chấm |
| `Dont_Know` | Kết quả quan sát riêng trong likelihood phân loại |
| Timeout | Không chấm sai; loại khỏi likelihood và kiểm tra missingness |
| Bỏ dở | Có thể chấm partial nếu đủ bằng chứng |
| Ước lượng theta | Bayesian EAP bằng grid quadrature |
| Ước lượng số từ | Posterior mean của `V(theta)` |
| Khoảng chính thức | Equal-tailed Bayesian credible interval 95% |
| Confidence interval | Không xuất trong V0 mặc định |
| CSEM theta | `1 / sqrt(I_test(theta))` |
| CSEM count | Delta-method qua đạo hàm `V'(theta)` |
| Dữ liệu không đủ | `insufficient_evidence`, không phải điểm 0 |
| Cấu hình/miền không hợp lệ | `scoring_unavailable`, không quy lỗi cho người dùng |
| Nguyên tắc phát hành | Không đánh đổi tính hợp lệ đo lường để luôn có một con số |