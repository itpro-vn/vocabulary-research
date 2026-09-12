# P0.6 — Pilot Calibration & Empirical Validation Protocol

**Dự án:** `vocabulary-research`  
**Repository:** `itpro-vn/vocabulary-research`  
**Tệp:** `PILOT_CALIBRATION_PROTOCOL.md`  
**Trạng thái:** Đặc tả đề xuất — cần phê duyệt trước khi tuyển mẫu  
**Mức ưu tiên:** P0.6 — bắt buộc trước khi công bố độ khó thực nghiệm hoặc triển khai chấm điểm IRT chính thức  
**Phiên bản giao thức:** `1.0.0`

---

## 1. Mục đích và phạm vi

Tài liệu quy định giao thức:

1. Thu thập dữ liệu pilot cho ngân hàng 1.200 câu hỏi.
2. Liên kết các booklet lên một thang năng lực chung.
3. Hiệu chuẩn độ khó thực nghiệm bằng Rasch/1PL, 2PL và, nếu dữ liệu hỗ trợ, 3PL.
4. Đánh giá chất lượng câu hỏi, phương án nhiễu và tính công bằng.
5. Xác thực điểm số trên mẫu độc lập bằng bài test tham chiếu dài.
6. Quyết định câu hỏi và mô hình nào đủ điều kiện phát hành.

**Nguyên tắc cốt lõi:** Độ khó do chuyên gia, CEFR, tần suất từ hoặc mô hình AI dự đoán chỉ là thông tin thiết kế ban đầu; không được công bố như độ khó IRT đã hiệu chuẩn.

Tài liệu này mô tả hợp đồng kỹ thuật cần triển khai, không xác nhận repository hiện đã có các module hoặc pipeline tương ứng.

### 1.1. Quy ước bắt buộc

- **MUST:** Điều kiện bắt buộc.
- **SHOULD:** Khuyến nghị mạnh; ngoại lệ phải được giải trình.
- **MAY:** Tùy chọn có kiểm soát.
- Mọi ngưỡng thống kê phải được đăng ký trước khi mở dữ liệu xác thực.
- Không được thay đổi tiêu chí nghiệm thu sau khi xem kết quả mà không tạo phiên bản giao thức mới.

### 1.2. Giả định thiết kế

Thiết kế mặc định áp dụng cho câu hỏi trắc nghiệm một đáp án đúng, chấm điểm nhị phân.

Nếu có câu hỏi đa mức điểm, nhiều đáp án hoặc định dạng khác, MUST có phụ lục mô hình riêng; không tự động áp dụng 3PL.

Thang đo mục tiêu mặc định là **năng lực từ vựng EFL tổng quát**. Nếu dữ liệu cho thấy nhiều chiều quan trọng, MUST đánh giá lại giả định này trước khi phát hành một điểm tổng duy nhất.

---

## 2. Các cổng nghiệm thu

| Cổng | Nội dung | Điều kiện qua cổng |
|---|---|---|
| G0 | Sẵn sàng nội dung và dữ liệu | Khóa phiên bản item, đáp án, blueprint và schema |
| G1 | Sẵn sàng vận hành | Soft pilot xác nhận UI, logging, thời lượng và phân phối booklet |
| G2 | Đủ dữ liệu | Đạt quota response, năng lực, liên kết và nhóm phân tích |
| G3 | Hiệu chuẩn hợp lệ | Mô hình hội tụ, thang đo liên kết ổn định, item đạt tiêu chuẩn |
| G4 | Công bằng và chất lượng | Hoàn tất distractor, DIF, rà soát nội dung và anchor purification |
| G5 | Xác thực độc lập | Đạt MAE, RMSE, coverage và các tiêu chí nhóm đã đăng ký |
| G6 | Phát hành | Snapshot bất biến, báo cáo kiểm toán và phê duyệt liên ngành |

Không được dùng kết quả pilot để tuyên bố độ chính xác sản phẩm khi chưa qua G5.

---

## 3. Thiết kế lấy mẫu pilot

### 3.1. Quy mô mặc định

Thiết kế dùng:

- 1.200 item.
- 72 booklet.
- 80 item/booklet.
- 150 người hợp lệ/booklet.
- Một người chỉ làm một booklet trong phân tích hiệu chuẩn chính.

```text
N_valid = 72 × 150 = 10.800 người

Tổng lượt trình bày mục tiêu:
10.800 × 80 = 864.000

Item không neo:
1.080 item × 600 lượt = 648.000

Item neo:
120 item × 1.800 lượt = 216.000

Tổng:
648.000 + 216.000 = 864.000
```

Đây là số lượt trình bày theo thiết kế. Số response chấm điểm được có thể thấp hơn vì bỏ trống hoặc dữ liệu không hợp lệ.

MUST theo dõi riêng:

- `n_presented`
- `n_answered_valid`
- `n_omitted`
- `n_not_reached`
- `n_excluded`

### 3.2. Số response/item

| Loại item | Mục tiêu response hợp lệ | Sàn xem xét hiệu chuẩn |
|---|---:|---:|
| Item không neo | 600 | 500 |
| Item neo | 1.800 | 1.500 |
| Item rất dễ/rất khó hoặc cần 3PL | 800–1.200 nếu bất định cao | Theo mô phỏng và thông tin thực tế |

**600 response/item không bảo đảm 3PL khả định tốt.** Phân bố năng lực, số trả lời đúng/sai và thông tin ở vùng năng lực thấp quan trọng hơn một ngưỡng cỡ mẫu đơn lẻ.

Nếu thiếu dữ liệu, MUST tuyển bổ sung theo booklet và dải năng lực còn thiếu; không chỉ tăng tổng số người.

### 3.3. Quy mô tuyển ban đầu

Với tỷ lệ loại, bỏ dở hoặc không hoàn thành dự kiến 15%:

```text
N_recruit = ceil(10.800 / 0,85)
          = 12.706 người
```

Ngân sách tuyển SHOULD dự phòng khoảng 13.000–14.000 người.

Tuyển bổ sung chỉ dựa trên quota, thiếu dữ liệu hoặc độ chính xác tham số đã đăng ký; không dựa trên việc “kết quả có đẹp hơn hay không”.

### 3.4. Phân tầng năng lực EFL

Phân bổ cân bằng sáu dải:

| Dải tuyển mẫu | Số người hợp lệ | Người/booklet |
|---|---:|---:|
| Pre-A1/A1 | 1.800 | 25 |
| A2 | 1.800 | 25 |
| B1 | 1.800 | 25 |
| B2 | 1.800 | 25 |
| C1 | 1.800 | 25 |
| C2 hoặc EFL nâng cao tương đương | 1.800 | 25 |
| **Tổng** | **10.800** | **150** |

Dải tuyển mẫu MUST dựa trên:

1. Bài sàng lọc độc lập, không dùng item pilot hoặc tham chiếu.
2. Chứng chỉ hoặc lịch sử học gần đây, nếu có.
3. Tự đánh giá chỉ là dữ liệu bổ trợ.

Các nhãn trên phục vụ tuyển mẫu, **không tự động chứng minh điểm IRT tương ứng với CEFR**.

Theo thiết kế, mỗi item không neo có khoảng 100 lượt trình bày/dải; mỗi item neo có khoảng 300 lượt/dải.

### 3.5. Mẫu hiệu chuẩn và quần thể triển khai

Mẫu cân bằng năng lực không đại diện tự nhiên cho mọi quần thể người dùng.

MUST phân biệt:

- **Calibration population:** Dùng để xác định tham số và đơn vị thang đo.
- **Deployment population:** Quần thể dự kiến sử dụng sản phẩm.
- **Validation population:** Mẫu độc lập dùng đánh giá khả năng tổng quát hóa.

Kết quả hiệu năng MUST báo cáo:

- Không trọng số theo thiết kế nghiên cứu.
- Có trọng số theo quần thể triển khai, nếu có căn cứ xác định trọng số.

### 3.6. Quota phục vụ DIF

Trước tuyển mẫu, MUST xác định các nhóm L1 và thiết bị ưu tiên.

Mục tiêu cho mỗi phép so sánh DIF quan trọng:

- Khoảng 200 response hợp lệ/item/nhóm cho các item thuộc phạm vi kết luận.
- Có đủ chồng lấn năng lực giữa hai nhóm.
- Không để nhóm L1 hoặc thiết bị chỉ xuất hiện trong một số booklet riêng biệt.

Không thể mặc định ngân sách 10.800 người đủ kiểm định mạnh cho mọi ngôn ngữ mẹ đẻ.

Nếu không đạt quota:

- Báo cáo “không đủ bằng chứng để đánh giá DIF”.
- Không được diễn giải thành “không có DIF”.
- Tuyển mẫu bổ sung có mục tiêu hoặc giới hạn phạm vi kết luận.

---

## 4. Thiết kế booklet và matrix sampling

### 4.1. Phân chia ngân hàng

```text
Ngân hàng: 1.200 item

Anchor candidates:
120 item = 12 panel × 10 item

Operational candidates:
1.080 item = 36 module × 30 item

Mỗi booklet:
2 module × 30 item + 2 anchor panel × 10 item
= 80 item
```

Anchor ở giai đoạn này là **ứng viên neo**, chưa phải item bất biến đã được chứng minh.

### 4.2. Xây dựng 72 booklet

Các điều kiện bắt buộc:

1. Mỗi module xuất hiện trong đúng 4 booklet.
2. Mỗi anchor panel xuất hiện trong đúng 12 booklet.
3. Không có item lặp lại trong cùng một booklet.
4. Đồ thị đồng xuất hiện giữa các module phải liên thông.
5. Đồ thị đồng xuất hiện giữa các anchor panel phải liên thông.
6. Toàn bộ đồ thị booklet–item phải liên thông và có nhiều đường liên kết dự phòng.
7. Không gán một panel riêng cho một nhóm năng lực, L1 hoặc thiết bị.

Một cách xây dựng module có thể tái lập:

```text
Đánh số module: 0..35

Tạo các cặp:
(i, (i + 1) mod 36)
(i, (i + 6) mod 36)

Với i = 0..35:
Tổng cộng 72 cặp module, tương ứng 72 booklet.

Mỗi module xuất hiện 4 lần.
Đồ thị liên thông nhờ các cạnh chênh lệch 1.
```

Việc gán hai anchor panel/booklet MUST dùng thuật toán cân bằng có seed cố định, thỏa các ràng buộc trên và tối đa hóa đa dạng cặp panel.

### 4.3. Chọn anchor candidates

120 anchor candidates MUST bao phủ:

- Toàn dải độ khó dự kiến.
- Các lĩnh vực nội dung trong blueprint.
- Các định dạng câu hỏi được phép.
- Nhiều vị trí trong booklet.
- Các mức tần suất từ và đặc điểm ngôn ngữ phù hợp.

Không chọn anchor chỉ vì item có vẻ “dễ, ổn định”.

Loại khỏi tập ứng viên neo trước pilot nếu:

- Nội dung phụ thuộc văn hóa mạnh.
- Có khả năng nhiều đáp án đúng.
- Hiển thị nhạy với thiết bị.
- Có gợi ý hình thức rõ ràng.
- Phụ thuộc đáp án hoặc ngữ cảnh của item khác.

### 4.4. Thứ tự và hiệu ứng vị trí

SHOULD dùng ít nhất bốn biến thể thứ tự/booklet:

- Rải anchor ở đầu, giữa và cuối.
- Cân bằng vị trí module.
- Tránh tập trung item khó ở cuối.
- Lưu `position_index` và `order_variant_id`.

Nếu đảo phương án, MUST ghi cả:

- ID phương án ngữ nghĩa ổn định.
- Thứ tự hiển thị thực tế.

Không đảo phương án với những item mà thứ tự có ý nghĩa nội dung.

### 4.5. Gán người tham gia

Gán ngẫu nhiên có phân tầng theo:

- Dải năng lực.
- L1 ưu tiên.
- Nhóm thiết bị.
- Nguồn tuyển mẫu hoặc địa điểm.

Bộ phân phối MUST ưu tiên ô quota thiếu nhưng không được dùng đáp án pilot đang diễn ra để chọn booklet.

Pilot hiệu chuẩn là thiết kế cố định theo booklet, không phải CAT.

---

## 5. Quy trình thu thập

### 5.1. Soft pilot

Thực hiện trước pilot chính với khoảng 150–250 người.

Mục tiêu:

- Kiểm tra UI và đáp án.
- Kiểm tra logging.
- Xác định thời lượng.
- Kiểm tra rendering trên mobile/desktop.
- Phát hiện item gây hiểu sai.

Không dùng soft pilot để quyết định mô hình IRT cuối cùng.

Dữ liệu soft pilot mặc định không gộp vào hiệu chuẩn chính, đặc biệt nếu nội dung hoặc giao diện đã thay đổi.

### 5.2. Phiên làm bài

- 80 item, mục tiêu khoảng 40–60 phút; điều chỉnh bằng soft pilot.
- Có nghỉ giữa các phần.
- Không hiển thị đúng/sai hoặc lời giải.
- Không ép tốc độ nếu mục tiêu đo là năng lực từ vựng, không phải xử lý nhanh.
- Ghi nhận mất kết nối, tab hidden và resume nhưng không tự động coi đó là gian lận.

### 5.3. Đồng thuận và bảo vệ dữ liệu

MUST:

- Có đồng thuận tham gia.
- Tách thông tin liên hệ khỏi response.
- Dùng ID giả danh.
- Hạn chế quyền truy cập L1, tuổi và metadata thiết bị.
- Công bố thời hạn lưu trữ và quy trình xóa dữ liệu.
- Có cơ chế phù hợp nếu tuyển người chưa thành niên.

Không thu nội dung bàn phím, định danh thiết bị xâm lấn hoặc dữ liệu ngoài mục tiêu nghiên cứu.

---

## 6. Hợp đồng dữ liệu

### 6.1. Bản ghi response tối thiểu

```json
{
  "study_id": "pilot_p06_v1",
  "participant_id": "pseudonymous-id",
  "session_id": "session-id",
  "booklet_id": "B001",
  "order_variant_id": "O2",
  "item_id": "I0001",
  "item_version": "1",
  "item_content_hash": "sha256:...",
  "position_index": 17,
  "option_order": ["o3", "o1", "o4", "o2"],
  "selected_option_id": "o1",
  "score": 1,
  "response_status": "answered",
  "response_time_ms": 14820,
  "device_class": "mobile",
  "delivery_version": "pilot-ui-v1",
  "assignment_seed": 47291
}
```

Thông tin năng lực sàng lọc, L1 và biến nền SHOULD lưu ở bảng participant riêng.

### 6.2. Phân biệt trạng thái thiếu dữ liệu

| Trạng thái | Ý nghĩa | Xử lý mặc định |
|---|---|---|
| `not_administered` | Không thuộc booklet | Missing theo thiết kế |
| `omitted` | Đã thấy nhưng không trả lời | Missing, phân tích độ nhạy |
| `not_reached` | Chưa tới item khi dừng | Missing, kiểm tra speededness |
| `technical_failure` | Lỗi hệ thống | Loại khỏi response hợp lệ |
| `answered` | Có đáp án hợp lệ | Chấm 0/1 |
| `invalidated` | Bị loại theo QC | Giữ audit, không dùng hiệu chuẩn chính |

**Không được chấm `not_administered` thành 0.**

Với `omitted` và `not_reached`, MUST so sánh ít nhất:

1. Phân tích chính coi là missing.
2. Phân tích độ nhạy coi là sai nếu chính sách sản phẩm chấm như vậy.
3. Phân tích ảnh hưởng của năng lực, vị trí và thời gian đến missingness.

Nếu missingness phụ thuộc mạnh vào năng lực hoặc tốc độ, giả định bỏ qua missing phải được xem xét lại.

### 6.3. Tính bất biến

Đổi stem, đáp án, distractor hoặc nội dung có khả năng ảnh hưởng đo lường MUST tạo `item_version` mới.

Không gộp response của các phiên bản khác nhau như cùng một item.

---

## 7. Kiểm soát chất lượng dữ liệu

### 7.1. Tiêu chí loại người tham gia

Có thể loại khi có bằng chứng:

- Trùng người hoặc trùng phiên ngoài thiết kế.
- Bot hoặc tự động hóa được xác minh.
- Không đáp ứng điều kiện tuyển mẫu.
- Lỗi hệ thống làm phần lớn phiên không sử dụng được.
- Nhiều chỉ báo kết hợp về trả lời không có nỗ lực.

Không loại chỉ vì:

- Điểm rất thấp hoặc rất cao.
- Person-fit bất thường.
- Trả lời nhanh.
- Dùng thiết bị di động.
- Thuộc một nhóm L1 cụ thể.

### 7.2. Rapid guessing và response time

Ngưỡng rapid guessing SHOULD được xác định từ soft pilot theo định dạng hoặc item family.

Nếu dùng mô hình mixture hoặc ngưỡng response time:

- Đăng ký thuật toán trước phân tích chính.
- Không chọn ngưỡng để tối đa hóa fit.
- Báo cáo kết quả có và không loại response bị gắn cờ.
- Xem xét bất bình đẳng giữa nhóm đọc nhanh, thiết bị và nhu cầu hỗ trợ tiếp cận.

### 7.3. Báo cáo QC bắt buộc

- Số người tuyển, bắt đầu, hoàn tất và hợp lệ.
- Tỷ lệ loại theo nguyên nhân.
- Tỷ lệ loại theo năng lực, L1 và thiết bị.
- Response hợp lệ/item.
- Mức hoàn thành quota.
- Phân bố thời gian và vị trí bỏ dở.
- Kiểm tra đồ thị liên kết sau QC.

---

## 8. Quy trình hiệu chuẩn IRT

### 8.1. Quy ước mô hình và thang đo

Dùng logistic với hệ số quy mô `D = 1`.

```text
logistic(x) = 1 / (1 + exp(−x))

Rasch:
P(correct | θ, b) = logistic(θ − b)

2PL:
P(correct | θ, a, b) = logistic(a × (θ − b))

3PL:
P(correct | θ, a, b, c)
= c + (1 − c) × logistic(a × (θ − b))
```

Trong đó:

- `θ`: Năng lực.
- `b`: Độ khó.
- `a`: Độ phân biệt, yêu cầu dương.
- `c`: Tiệm cận dưới của xác suất đúng.

`c` không phải phép đo trực tiếp “tỷ lệ đoán mò thực tế”, và không mặc định bằng `1 / số phương án`.

### 8.2. Bước 0 — Kiểm tra cấu trúc trước IRT

MUST kiểm tra:

- Đáp án và mã hóa.
- Tỷ lệ đúng, số đúng/sai.
- Tương quan item–rest trên người thực sự được gán item.
- Dimensionality trên các tập item có đồng quan sát.
- Local dependence, ví dụ residual Q3 đã điều chỉnh.
- Hiệu ứng testlet, nội dung lặp, vị trí và tốc độ.

Không được tạo tương quan item bằng cách điền 0 vào ô missing theo booklet.

Nếu có local dependence đáng kể, cân nhắc:

- Loại một item trong cụm trùng lặp.
- Mô hình testlet.
- Mô hình đa chiều.
- Thiết kế lại nội dung.

Không dùng tăng số tham số 2PL/3PL để che giấu cấu trúc đo lường sai.

### 8.3. Bước 1 — Rasch có regularization

Rasch là baseline bắt buộc.

Một cấu hình prior khởi đầu:

```text
b_i ~ Normal(0, 2²)
a_i = 1

Population ability:
μ = 0 để định vị thang đo
σ được ước lượng trong mô hình Rasch
```

Việc cố định `a = 1` đã xác định đơn vị logistic của Rasch; không tùy tiện đồng thời áp thêm chuẩn hóa khiến việc so sánh mô hình mất nhất quán.

MUST:

- Kiểm tra độ nhạy với prior yếu hơn.
- Lưu ước lượng bất định của `b`.
- Xác nhận item cực đoan không chỉ được “cứu” bằng prior.
- Dùng nhiều điểm khởi tạo hoặc kiểm tra hội tụ phù hợp với bộ ước lượng.

### 8.4. Bước 2 — 2PL

Cấu hình regularization tham khảo:

```text
θ ~ Normal(0, 1)
log(a_i) ~ Normal(0, 0,35²)
b_i ~ Normal(0, 2²)
```

Độ rộng prior phải được kiểm tra bằng mô phỏng trước khi khóa cấu hình.

2PL được ưu tiên hơn Rasch khi:

- Cải thiện dự đoán ngoài mẫu có ý nghĩa thực tiễn.
- Sự khác nhau của discrimination ổn định qua bootstrap.
- Item fit và residual được cải thiện.
- Không tạo nhiều ước lượng biên hoặc phụ thuộc prior quá mạnh.
- Điểm số và bất định tốt hơn trên vùng năng lực mục tiêu.

Trước so sánh tham số hoặc điểm giữa mô hình, MUST đưa về cùng đơn vị thang đo.

### 8.5. Bước 3 — 3PL

Chỉ thử 3PL khi:

- Định dạng trắc nghiệm phù hợp.
- Có đủ người năng lực thấp cho các item liên quan.
- 2PL có residual phù hợp với giả thuyết tiệm cận dưới.
- Mô phỏng phục hồi tham số cho thiết kế thực tế cho kết quả chấp nhận được.

Prior cho `c` MAY dùng phân bố Beta có trung bình gần xác suất chọn ngẫu nhiên, nhưng phải:

- Ghi rõ độ mạnh prior.
- Kiểm tra độ nhạy.
- Không diễn giải posterior hẹp do prior mạnh như bằng chứng dữ liệu mạnh.

Không chấp nhận 3PL nếu:

- `c` gần như không được dữ liệu cập nhật.
- Tương quan tham số quá cao hoặc Hessian bất ổn.
- Kết quả thay đổi mạnh theo khởi tạo.
- Cải thiện in-sample nhưng không cải thiện ngoài mẫu.
- `a`, `b`, `c` khó phục hồi trong mô phỏng.

Trong trường hợp đó, giữ 2PL hoặc Rasch và thu thập bổ sung nếu cần.

### 8.6. Phương pháp so sánh

MUST dùng kết hợp:

1. Predictive log loss trên dữ liệu giữ lại.
2. Kiểm định fit và residual.
3. AIC/BIC nếu phương pháp ước lượng cho phép so sánh hợp lệ.
4. Độ ổn định tham số.
5. Sai số đo theo năng lực.
6. Khả năng phục hồi tham số bằng mô phỏng.

Cross-validation SHOULD chia theo participant, phân tầng theo booklet và năng lực.

Khi chấm dự đoán người ở fold giữ lại, không được dùng chính response mục tiêu để ước lượng `θ` rồi coi dự đoán đó là ngoài mẫu. Phải dùng likelihood biên hoặc tách response dùng suy luận năng lực khỏi response dùng đánh giá.

Không dùng likelihood-ratio test thông thường như bằng chứng duy nhất cho 2PL so với 3PL vì `c = 0` là trường hợp biên.

---

## 9. Liên kết thang đo và anchor purification

### 9.1. Hiệu chuẩn chính

Ưu tiên **concurrent calibration** toàn bộ dữ liệu booklet với một tham số chung cho mỗi item version.

Thiết kế chồng lấn giúp đặt các item lên cùng thang đo; không cần hiệu chuẩn từng booklet rồi nối thủ công nếu concurrent calibration hoạt động tốt.

Từ “equating” chỉ được dùng khi đã chứng minh các form có cùng cấu trúc đo và có thể thay thế về điểm số. Nếu chưa, dùng “linking”.

### 9.2. Thanh lọc anchor

Quy trình:

1. Fit mô hình ban đầu.
2. Kiểm tra item fit, DIF, position effect và parameter drift của anchor.
3. Loại anchor không bất biến khỏi tập neo.
4. Ước lượng lại thang đo.
5. Lặp đến khi tập anchor ổn định hoặc đạt số vòng tối đa đã đăng ký, mặc định 3.

Loại khỏi tập neo không nhất thiết loại khỏi ngân hàng.

Tập anchor cuối MUST:

- Có ít nhất 60 item.
- Bao phủ các vùng năng lực mục tiêu.
- Mỗi booklet còn ít nhất 10 anchor được chấp nhận.
- Giữ đồ thị liên kết liên thông, có liên kết dự phòng.

Nếu không đạt, dừng G3 và thu thập bridging data.

### 9.3. Kiểm tra độ bền linking

MUST thực hiện:

- Leave-one-panel-out hoặc leave-one-block-out.
- Bootstrap theo participant, giữ cấu trúc booklet.
- So sánh tham số trên các nửa mẫu cân bằng.
- Ước lượng sai số linking.

Nếu hiệu chuẩn riêng để kiểm tra chéo, MAY dùng Stocking–Lord hoặc Haebara trên anchor đã thanh lọc.

Không dùng tập anchor có DIF chưa xử lý để định nghĩa thang đo tham chiếu.

---

## 10. Item fit và quy tắc xử lý câu hỏi hỏng

### 10.1. Ngưỡng sàng lọc mặc định

Các ngưỡng dưới đây là cờ rà soát, không phải máy loại item tự động.

| Chỉ báo | Ngưỡng rà soát | Diễn giải |
|---|---|---|
| Rasch Infit MNSQ | Ngoài 0,70–1,30 | Sai khác với kỳ vọng mô hình |
| Rasch Outfit MNSQ | Ngoài 0,70–1,30 | Nhạy với response bất thường |
| Infit/Outfit | Ngoài 0,50–1,50 | Cờ nghiêm trọng |
| Item–rest correlation | Âm | Kiểm tra đáp án/nội dung ngay |
| Discrimination `a` | Nhỏ hơn 0,35 hoặc lớn hơn 3,0 | Ít thông tin hoặc dependence |
| `SE(b)` | Lớn hơn 0,30 SD θ | Chưa đủ chính xác |
| Correct/incorrect counts | Ít hơn 50 ở một phía | Cảnh báo bất định, không tự động loại |
| Adjusted residual Q3 | Lớn hơn 0,20 | Rà soát dependence |
| S-X² hoặc item-fit tương đương | FDR-adjusted `q < 0,05` | Kết hợp effect size và đồ thị |

Infit/Outfit là tiêu chí chính trong Rasch; không áp máy móc cùng khoảng ngưỡng cho mọi triển khai 2PL/3PL.

### 10.2. M2 và fit toàn cục

M2 là kiểm định fit toàn cục, không phải chỉ báo xác định trực tiếp item cần xóa.

MUST báo cáo khi ước lượng hợp lệ:

- M2, bậc tự do và p-value.
- RMSEA và khoảng tin cậy.
- SRMSR.
- CFI/TLI nếu có mô hình baseline phù hợp.

Ngưỡng định hướng:

- RMSEA không quá 0,06: mong muốn.
- 0,06–0,08: cần giải trình.
- SRMSR không quá 0,08: mong muốn.
- CFI/TLI khoảng 0,95 trở lên: hỗ trợ, không thay thế kiểm tra nội dung.

Với matrix sampling thưa, không được giả định mọi phần mềm tính M2 hợp lệ. MUST kiểm tra hỗ trợ missing theo thiết kế và số cặp item đồng quan sát.

Nếu M2 toàn ngân hàng không khả dụng:

- Báo cáo rõ lý do.
- Dùng fit theo booklet hoặc các cụm có đủ đồng quan sát.
- Bổ sung posterior predictive checks hoặc parametric bootstrap.
- Không tính M2 bằng dữ liệu điền giả.

### 10.3. Trạng thái quyết định item

| Trạng thái | Ý nghĩa |
|---|---|
| `accepted` | Đủ dữ liệu, fit và nội dung đạt |
| `accepted_non_anchor` | Dùng chấm điểm được, không dùng neo |
| `needs_more_data` | Bất định cao hoặc thiếu nhóm cần thiết |
| `revise_and_repilot` | Cần sửa nội dung; phiên bản mới phải pilot lại |
| `quarantined` | Không được đưa vào chấm điểm |
| `retired` | Loại khỏi chu kỳ phát hành |

Lỗi đáp án, nhiều đáp án đúng hoặc rendering làm thay đổi nghĩa là lý do quarantine ngay, không chờ kiểm định thống kê.

Mỗi quyết định MUST có:

- Bằng chứng thống kê.
- Nhận xét chuyên gia nội dung.
- Người phê duyệt.
- Phiên bản và thời điểm.
- Hành động tiếp theo.

---

## 11. Distractor Functioning

### 11.1. Phân tích bắt buộc

Với từng phương án:

- Tỷ lệ chọn toàn mẫu.
- Tỷ lệ chọn theo năng lực.
- Tỷ lệ chọn theo L1 và thiết bị.
- Quan hệ với điểm item–rest hoặc năng lực ước lượng không dùng response của chính item.
- Thời gian trả lời.
- Option characteristic curves.

Đáp án đúng kỳ vọng được chọn nhiều hơn khi năng lực tăng. Distractor thường giảm ở năng lực cao, nhưng có thể đạt đỉnh ở vùng năng lực trung bình.

Không yêu cầu mọi distractor phải giảm đơn điệu trên toàn thang.

### 11.2. Cờ distractor không hoạt động

Gắn cờ khi:

- Được chọn dưới 5% toàn mẫu **và** rất ít trong nhóm có khả năng trả lời sai.
- Gần như không được chọn trong vùng năng lực thấp–trung bình.
- Thu hút người năng lực cao bất thường.
- Có quan hệ dương mạnh với năng lực sau khi kiểm tra sampling.
- Có dấu hiệu gợi ý độ dài, ngữ pháp hoặc vị trí.

Ngưỡng 5% chỉ là heuristic; với item rất dễ, tỷ lệ chọn distractor thấp có thể hoàn toàn hợp lý.

### 11.3. Mô hình bổ sung

MAY dùng nominal response model hoặc multinomial regression để:

- Mô tả khả năng chọn từng phương án.
- Phát hiện phương án cạnh tranh với đáp án đúng.
- Phân tích differential distractor functioning.

Sửa distractor MUST tạo item version mới và hiệu chuẩn lại. Không tái sử dụng nguyên tham số cũ.

---

## 12. DIF theo L1 và thiết bị

### 12.1. Phạm vi

MUST kiểm tra:

- DIF đồng nhất: Khác biệt xác suất đúng sau khi khống chế năng lực.
- DIF không đồng nhất: Khác biệt thay đổi theo năng lực.
- Differential distractor functioning khi đủ dữ liệu.

Khác biệt tỷ lệ đúng thô giữa nhóm không tự nó là DIF.

### 12.2. Phương pháp

Phân tích chính SHOULD dùng multi-group IRT với:

- Mean/variance năng lực được phép khác giữa nhóm.
- Anchor không DIF để định nghĩa thang chung.
- Kiểm định tham số item theo nhóm.

Phân tích đối chiếu:

```text
logit(P(correct))
= β0
+ β1 × ability
+ β2 × group
+ β3 × ability × group
+ covariates
```

Trong đó:

- `β2`: Thành phần DIF đồng nhất.
- `β3`: Thành phần DIF không đồng nhất.
- Covariates MAY gồm vị trí item, booklet và điều kiện thu thập.

Mantel–Haenszel MAY dùng như phân tích bổ trợ cho DIF đồng nhất.

### 12.3. Ngưỡng và multiplicity

Đăng ký trước các họ kiểm định; áp dụng Benjamini–Hochberg với FDR 0,05 trong từng họ.

Gắn cờ thực tiễn nếu có một hoặc nhiều dấu hiệu:

- Chênh lệch `b` sau linking từ 0,50 SD θ.
- Chênh lệch xác suất đúng từ 0,10 trên vùng năng lực có hỗ trợ dữ liệu.
- Tỷ số discrimination lớn hơn 1,5 hoặc nhỏ hơn khoảng 0,67, kèm bất định phù hợp.
- Differential test functioning đáng kể ở mức điểm tổng.

Ngưỡng phải được kiểm tra bằng mô phỏng công suất theo thiết kế thật.

### 12.4. Kiểm soát nhiễu thiết bị

Thiết bị thường tương quan với tuổi, vùng địa lý, L1 và năng lực.

MUST:

- Kiểm tra vùng chồng lấn covariates.
- Không suy luận quan hệ nhân quả từ so sánh quan sát đơn thuần.
- Có nghiên cứu con ngẫu nhiên thiết bị nếu muốn khẳng định hiệu ứng do thiết bị.
- Kiểm tra font, kích thước màn hình, cuộn trang và vị trí phương án.

### 12.5. Diễn giải và xử lý

DIF không đồng nghĩa tự động với thiên lệch không công bằng.

Hội đồng nội dung phải xác định khác biệt:

- Có thuộc cấu trúc năng lực cần đo không.
- Do yếu tố không liên quan như giao diện hoặc kiến thức văn hóa.
- Có gây hại thực tiễn ở cấp điểm tổng không.

Item có DIF nghiêm trọng chưa giải thích được không được làm anchor và phải quarantine hoặc giới hạn phạm vi sử dụng có công bố.

---

## 13. Nghiên cứu xác thực đối chuẩn độc lập

### 13.1. Mục tiêu

Đánh giá hệ thống đo sản xuất đã khóa, bao gồm:

- Ngân hàng và tham số.
- Thuật toán chọn item nếu dùng CAT.
- Prior chấm điểm.
- Điều kiện dừng.
- Cách tính khoảng bất định.
- Chính sách missing.

Không chỉ xác thực mô hình IRT trừu tượng.

### 13.2. Bài tham chiếu dài

Xây dựng **160 item độc lập**, ngoài 1.200 item pilot.

Bài tham chiếu MUST:

- Có blueprint tương thích với cấu trúc đo mục tiêu.
- Bao phủ toàn dải năng lực.
- Không trùng stem, target word hoặc item family gần tương đương với ngân hàng pilot.
- Không chia sẻ các mẹo hoặc dấu hiệu đáp án.
- Được chuyên gia rà soát độc lập.
- Có thông tin đo đủ ở cả hai đầu thang.

Chia thành bốn block 40 item, có nghỉ giữa block.

Độ dài 160 không tự bảo đảm độ chính xác. Mục tiêu:

```text
SE_ref ≤ 0,20 SD θ trên vùng trung tâm mục tiêu
SE_ref ≤ 0,30 SD θ ở các vùng biên đã đăng ký
```

Nếu không đạt, MUST tăng thông tin bài tham chiếu hoặc giới hạn phạm vi tuyên bố.

### 13.3. Hiệu chuẩn và linking bài tham chiếu

Dùng một mẫu bridging độc lập, mặc định:

- 2.400 người hợp lệ.
- Cân bằng sáu dải năng lực.
- Mỗi người làm 160 item tham chiếu.
- Mỗi người làm thêm một mini-form 30 anchor đã được chấp nhận từ pilot.
- Phân phối mini-form bảo đảm liên kết tốt.
- Tách phiên và cân bằng thứ tự.

Các anchor cầu nối không thuộc điểm bài tham chiếu.

Tham số pilot được giữ cố định trong quy trình linking chính; sai số từ hiệu chuẩn pilot và linking MUST được đưa vào phân tích bất định hoặc phân tích độ nhạy.

Mẫu bridging không được dùng làm mẫu xác thực cuối.

### 13.4. Mẫu xác thực cuối

Mặc định:

- 1.200 người hợp lệ mới.
- 200 người/dải năng lực.
- Không tham gia pilot hoặc bridging.
- Có quota cho các nhóm triển khai quan trọng.

Mỗi người làm:

1. Bài đánh giá mục tiêu: CAT hoặc short form sản xuất.
2. Bài tham chiếu 160 item.

Thiết kế crossover:

- 50% làm bài mục tiêu trước.
- 50% làm bài tham chiếu trước.
- Khoảng cách phiên mục tiêu 2–7 ngày.
- Không cung cấp phản hồi học tập giữa hai phiên.
- Ghi nhận học thêm hoặc thay đổi điều kiện.

Đây là concurrent validation trong khoảng thời gian gần; không được tuyên bố độ ổn định dài hạn từ thiết kế này.

### 13.5. Chống rò rỉ dữ liệu xác thực

Trước khi mở đáp án validation, MUST khóa:

- Snapshot tham số.
- Code scoring và dependency.
- CAT policy hoặc short-form definition.
- Seed hoặc chính sách ngẫu nhiên.
- Metric và ngưỡng nghiệm thu.
- Mapping thang đo.
- Kế hoạch phân tích nhóm.

Không fit phép biến đổi điểm để giảm MAE trực tiếp trên mẫu xác thực cuối.

Nếu dùng validation để chỉnh hệ thống, tập đó trở thành development data; cần một mẫu xác thực mới.

---

## 14. Chỉ số xác thực

### 14.1. Sai số điểm

Tất cả điểm phải ở cùng thang đo.

```text
e_j = theta_target_j − theta_reference_j

Bias = mean(e_j)

MAE = mean(abs(e_j))

RMSE = sqrt(mean(e_j²))
```

MUST báo cáo:

- Tổng thể.
- Theo dải năng lực sàng lọc độc lập.
- Theo L1.
- Theo thiết bị.
- Theo độ dài bài mục tiêu hoặc số item CAT.
- Theo điều kiện thứ tự làm bài.

Báo cáo thêm:

- Pearson correlation.
- Spearman correlation.
- Calibration intercept và slope.
- Đồ thị sai số theo năng lực.
- Floor/ceiling effects.

Tương quan cao không thay thế MAE, RMSE hoặc phân tích bias.

### 14.2. Độ bất định của metric

Dùng bootstrap theo participant, có phân tầng phù hợp, mặc định ít nhất 2.000 lần.

MUST xem xét thêm:

- Sai số tham số item.
- Sai số linking.
- Sai số bài tham chiếu.
- Cấu trúc cụm nếu tuyển theo trường hoặc lớp.

Bootstrap chỉ response người làm bài với tham số cố định không phản ánh toàn bộ bất định hiệu chuẩn.

### 14.3. Empirical Coverage: phân biệt đúng đại lượng

Năng lực thật không quan sát trực tiếp. Điểm tham chiếu dù dài vẫn có sai số.

Vì vậy MUST báo cáo ba đại lượng riêng biệt.

#### A. Reference-point inclusion

```text
Reference-point inclusion
= mean(L_target_j ≤ theta_reference_j ≤ U_target_j)
```

Đây là tỷ lệ khoảng mục tiêu chứa **ước lượng tham chiếu**, không phải coverage của năng lực thật.

Không được dùng nhãn “true empirical coverage” cho chỉ số này.

#### B. Khoảng chênh lệch có xét sai số hai phép đo

Với khoảng Wald và các giả định phù hợp:

```text
d_j = theta_target_j − theta_reference_j

SE_diff_j
= sqrt(
    Var_target_j
    + Var_reference_j
    − 2 × Cov_error_j
  )

Difference interval:
d_j ± 1,96 × SE_diff_j
```

Đánh giá tỷ lệ khoảng chênh lệch chứa 0.

Nếu không thể giả định sai số độc lập, MUST ước lượng covariance hoặc báo cáo phân tích độ nhạy. Sai số linking chung cũng có thể tạo tương quan.

Chỉ số này đánh giá sự nhất quán của hai phép đo cùng bất định đã khai báo; không đồng nhất với coverage của `θ` thật.

#### C. Coverage với năng lực biết trước trong mô phỏng

```text
Coverage_95
= mean(L_target_j ≤ theta_true_j ≤ U_target_j)
```

Mô phỏng MUST dùng:

- Thiết kế booklet/CAT thật.
- Phân bố năng lực đa dạng.
- Bộ tham số rút từ bất định hiệu chuẩn.
- Kịch bản lệch mô hình: dependence, DIF, guessing và missing.
- Không chỉ sinh và fit cùng một mô hình lý tưởng.

Ngoài ra MAY dùng joint latent-variable model trên dữ liệu thực, nhưng phải công bố coverage ước lượng này phụ thuộc giả định mô hình.

### 14.4. Khoảng tin cậy và khoảng credible

MUST ghi rõ khoảng báo cáo là:

- Confidence interval.
- Bayesian credible interval.
- Prediction interval.

Không gọi mọi khoảng `±1,96 × SE` là khoảng có coverage 95% nếu chưa đánh giá.

---

## 15. Tiêu chí nghiệm thu xác thực

Các ngưỡng dưới đây là mặc định cho điểm liên tục trên thang `θ` chuẩn hóa. Chủ sản phẩm và psychometrics lead MUST phê duyệt trước validation.

| Chỉ số | Mục tiêu |
|---|---:|
| Absolute bias tổng thể | Không quá 0,10 SD θ |
| MAE tổng thể | Không quá 0,30 SD θ |
| RMSE tổng thể | Không quá 0,40 SD θ |
| Absolute bias ở nhóm trọng yếu | Không quá 0,20 SD θ |
| RMSE ở nhóm đủ cỡ mẫu | Không quá 0,50 SD θ |
| Coverage mô phỏng của khoảng danh nghĩa 95% | Ước lượng điểm ít nhất 93%; cận dưới một phía 95% ít nhất 90% |
| Coverage mô phỏng ở nhóm trọng yếu | Không thấp hơn 90% với độ chính xác mô phỏng phù hợp |
| Tỷ lệ khoảng chênh lệch chứa 0 | Ít nhất 90%, cần điều tra nếu lệch mạnh khỏi 95% |

Với MAE/RMSE, cận trên một phía 95% SHOULD không vượt ngưỡng nghiệm thu. Nếu chưa đủ chính xác để kết luận, trạng thái là `inconclusive`, không phải `passed`.

Coverage cao không được đạt bằng cách trả về khoảng quá rộng. MUST báo cáo:

- Độ rộng khoảng trung vị và phân vị 90.
- Độ rộng theo năng lực.
- Số item cần dùng.
- Tỷ lệ không đạt điều kiện dừng.

`Reference-point inclusion` được báo cáo mô tả, không áp ngưỡng coverage thật.

Nếu sản phẩm xuất nhãn CEFR, cần nghiên cứu standard setting riêng; các ngưỡng trên không đủ để chứng nhận phân loại CEFR.

---

## 16. Mô phỏng trước thu thập

Trước G0, MUST chạy simulation study với tối thiểu:

1. Rasch đúng mô hình.
2. 2PL với discrimination phân tán.
3. 3PL với `c` khác nhau và prior khác nhau.
4. Năng lực lệch chuẩn hoặc mixture.
5. Thiếu mẫu ở hai đầu năng lực.
6. DIF theo L1 hoặc thiết bị.
7. Local dependence.
8. Rapid guessing và bỏ dở.
9. Mất một phần anchor.
10. Thất cân bằng nhóm/booklet.

Chỉ số đánh giá:

- Bias và RMSE của `a`, `b`, `c`.
- Coverage tham số.
- Tỷ lệ hội tụ.
- Độ ổn định linking.
- Công suất và false-positive rate của DIF.
- Sai số điểm.
- Coverage và chiều rộng khoảng điểm.
- Tác động của thiếu response.

Cỡ mẫu cuối MUST được xác nhận hoặc điều chỉnh bằng kết quả mô phỏng này, không chỉ bằng các quy tắc kinh nghiệm.

---

## 17. Pipeline kỹ thuật và artifacts

### 17.1. Pipeline logic

```text
freeze_item_bank
  → validate_booklet_design
  → run_soft_pilot
  → collect_main_pilot
  → validate_raw_data
  → apply_preregistered_qc
  → audit_sampling_and_connectivity
  → inspect_dimensionality
  → fit_regularized_rasch
  → fit_2pl
  → conditionally_fit_3pl
  → compare_models
  → analyze_item_fit
  → analyze_distractors
  → analyze_dif
  → purify_anchors
  → refit_and_quantify_uncertainty
  → freeze_calibration
  → calibrate_and_link_reference
  → freeze_validation_plan
  → run_independent_validation
  → approve_release
```

### 17.2. Artifacts bắt buộc

Các đường dẫn dưới đây là cấu trúc đề xuất:

```text
research/p06/
  protocol/
    PILOT_CALIBRATION_PROTOCOL.md
    preregistration.yaml
    deviations.md

  design/
    item_manifest.csv
    module_manifest.csv
    anchor_panel_manifest.csv
    booklet_manifest.csv
    assignment_policy.yaml

  reports/
    recruitment_and_qc.md
    dimensionality.md
    model_comparison.md
    item_fit.md
    distractor_analysis.md
    dif_analysis.md
    linking_stability.md
    concurrent_validation.md
    release_decision.md

  artifacts/
    item_parameters.parquet
    item_decisions.csv
    accepted_anchors.csv
    scale_definition.json
    validation_metrics.json
    calibration_manifest.json
```

Dữ liệu response cấp cá nhân MUST nằm trong kho có kiểm soát truy cập, không commit công khai.

### 17.3. Metadata tham số item

Mỗi item parameter record MUST chứa:

```text
item_id
item_version
model_family
a_estimate
b_estimate
c_estimate
parameter_uncertainty
n_answered_valid
n_correct
n_incorrect
fit_flags
dif_flags
anchor_status
decision_status
scale_version
calibration_run_id
```

Với tham số cố định, phải ghi rõ `fixed`; không giả vờ đó là tham số được ước lượng với SE bằng 0.

### 17.4. Khả năng tái lập

MUST lưu:

- Git commit.
- Phiên bản phần mềm và dependency.
- Hash dữ liệu đầu vào.
- Seed.
- Cấu hình prior và optimizer/sampler.
- Log hội tụ.
- Quy tắc lọc.
- Manifest đầu ra.
- Phiên bản định nghĩa thang đo.

Công cụ MAY là R, Python hoặc nền tảng thống kê khác, nhưng phải chứng minh hỗ trợ đúng mô hình, missing theo thiết kế và phương pháp fit được sử dụng.

---

## 18. Kiểm thử bắt buộc

### 18.1. Kiểm thử thiết kế

```text
assert unique_item_count == 1200
assert anchor_candidate_count == 120
assert non_anchor_count == 1080
assert booklet_count == 72
assert items_per_booklet == 80
assert each_module_occurs_in_4_booklets
assert each_anchor_panel_occurs_in_12_booklets
assert no_duplicate_item_within_booklet
assert booklet_item_graph_is_connected
assert assignment_is_not_confounded_with_group
```

### 18.2. Kiểm thử scoring và dữ liệu

- Chấm điểm bằng semantic option ID, không bằng vị trí hiển thị.
- Missing theo thiết kế không được chuyển thành sai.
- Item version mismatch phải gây lỗi.
- Response trùng phải được phát hiện.
- Tham số và scoring phải dùng cùng scale version.
- Validation participant không trùng pilot/bridging participant.
- Reference item không trùng hoặc gần trùng ngân hàng mục tiêu.

### 18.3. Kiểm thử phục hồi tham số

Pipeline MUST vượt qua dữ liệu tổng hợp có tham số biết trước.

Ngưỡng sai số và coverage của bài kiểm thử phải được cấu hình theo cỡ mẫu; không chỉ kiểm tra “chạy xong không lỗi”.

---

## 19. Quản trị quyết định và thay đổi

### 19.1. Trách nhiệm

| Vai trò | Trách nhiệm |
|---|---|
| Psychometrics lead | Mô hình, linking, fit, DIF và diễn giải |
| Content lead | Đáp án, cấu trúc nội dung, distractor và fairness |
| Engineering lead | Phân phối booklet, logging và tái lập |
| Data steward | Đồng thuận, quyền truy cập và vòng đời dữ liệu |
| Product/research owner | Quần thể mục tiêu và tiêu chí sử dụng |
| Independent reviewer | Rà soát kết luận và rủi ro phương pháp |

### 19.2. Điều kiện dừng phát hành

MUST dừng nếu:

- Đồ thị liên kết bị đứt.
- Anchor không đủ bất biến hoặc không đủ bao phủ.
- Mô hình không hội tụ đáng tin cậy.
- Thang đơn chiều không được hỗ trợ.
- Bất định tham số quá lớn ở phần quan trọng của ngân hàng.
- Có DIF nghiêm trọng chưa xử lý.
- Có rò rỉ dữ liệu validation.
- Bài tham chiếu quá thiếu chính xác.
- Khoảng bất định bị undercoverage nghiêm trọng.
- Quần thể được quảng bá nằm ngoài phạm vi mẫu được nghiên cứu.

### 19.3. Sau chỉnh sửa

- Đổi nội dung item: Pilot lại item version mới.
- Đổi mô hình chấm điểm: Hiệu chuẩn và xác thực lại theo mức ảnh hưởng.
- Đổi CAT policy hoặc stopping rule: Xác thực lại hệ thống đầu cuối.
- Đổi UI có khả năng ảnh hưởng nghĩa hoặc thao tác: Bridge study theo thiết bị.
- Mở rộng sang nhóm L1 mới: Thu thập dữ liệu và phân tích fairness bổ sung.

---

## 20. Checklist phê duyệt P0.6

### Trước tuyển mẫu

- [ ] Khóa 1.200 item và đáp án.
- [ ] Hoàn tất blueprint.
- [ ] Sinh và kiểm thử 72 booklet.
- [ ] Đăng ký quota năng lực, L1 và thiết bị.
- [ ] Hoàn tất mô phỏng cỡ mẫu.
- [ ] Khóa quy tắc QC, mô hình và metric.
- [ ] Có đồng thuận và kế hoạch bảo vệ dữ liệu.

### Trước hiệu chuẩn

- [ ] Đạt quota người và response/item.
- [ ] Kiểm tra missingness và speededness.
- [ ] Đồ thị liên kết còn hợp lệ.
- [ ] Hoàn tất audit dữ liệu.
- [ ] Xác nhận mã hóa và phiên bản item.

### Trước xác thực

- [ ] So sánh Rasch → 2PL → 3PL có lý do.
- [ ] Hoàn tất item fit, distractor và DIF.
- [ ] Anchor đã thanh lọc.
- [ ] Tham số, thang đo và scoring được khóa.
- [ ] Bài tham chiếu 160 item đã hiệu chuẩn độc lập.
- [ ] Kế hoạch validation và coverage được khóa.

### Trước phát hành

- [ ] MAE, RMSE và bias đạt yêu cầu.
- [ ] Báo cáo bất định và coverage đúng đại lượng.
- [ ] Công bố kết quả nhóm và hạn chế công suất.
- [ ] Không có lỗi công bằng nghiêm trọng chưa xử lý.
- [ ] Artifacts tái lập đầy đủ.
- [ ] Có phê duyệt psychometrics, nội dung và kỹ thuật.

---

## 21. Định nghĩa hoàn thành

P0.6 chỉ được coi là hoàn thành khi có **một phiên bản thang đo được hiệu chuẩn thực nghiệm, có liên kết kiểm chứng, có bất định định lượng, có bằng chứng chất lượng và fairness ở cấp item, và có xác thực độc lập ở cấp hệ thống**.

Một bảng tham số `a`, `b`, `c` xuất ra từ phần mềm chưa phải là bằng chứng ngân hàng đã sẵn sàng.

**Đầu ra cuối cùng phải trả lời được bốn câu hỏi:**

1. Item đo điều gì và hoạt động ổn định ở đâu?
2. Điểm số sai bao nhiêu trên người dùng chưa từng tham gia hiệu chuẩn?
3. Khoảng bất định có phản ánh đúng mức chưa biết không?
4. Kết luận nào được dữ liệu hỗ trợ, và kết luận nào chưa được phép công bố?