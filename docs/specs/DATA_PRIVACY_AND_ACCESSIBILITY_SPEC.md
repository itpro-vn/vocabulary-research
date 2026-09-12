# DATA_PRIVACY_AND_ACCESSIBILITY_SPEC.md

> **Actual source handling:** [The provided snapshot](../data/LAZZYBEE_SNAPSHOT_AUDIT.md) includes columns for notes and learning progress. The audit used allowlisted content columns and aggregate schema/counts; no notes, progress values or system values were published. Keep raw content/mappings private, verify dictionary-content rights separately, and sanitize imported HTML before any frontend rendering. Content availability does not imply research consent or redistribution permission.

> **Dự án:** `vocabulary-research`  
> **Repository:** `itpro-vn/vocabulary-research`  
> **Mã đặc tả:** P0.7  
> **Phạm vi:** Privacy, Ethics & Accessibility Contract  
> **Trạng thái:** Đặc tả đề xuất — bắt buộc phê duyệt trước khi triển khai production  
> **Mức ưu tiên:** P0 — điều kiện chặn phát hành  
> **Phiên bản:** 1.0.0

---

## 1. Mục tiêu và hiệu lực

Tài liệu quy định hợp đồng kỹ thuật về:

1. Bảo vệ dữ liệu câu trả lời, sự kiện tương tác và telemetry nghiên cứu.
2. Đồng thuận có hiểu biết, giới hạn mục đích xử lý và quyền được xóa.
3. Bảo mật ngân hàng câu hỏi và hạn chế trích xuất tự động.
4. Khả năng tiếp cận công bằng cho người dùng có khuyết tật, thiết bị yếu hoặc kết nối không ổn định.
5. Kiểm soát thiên lệch nội dung, đo lường và hiệu chuẩn.
6. Bằng chứng kiểm thử bắt buộc trước khi phát hành.

Đây là hợp đồng thiết kế mục tiêu, không phải xác nhận rằng repository hiện tại đã triển khai các cơ chế được mô tả.

### 1.1. Ngôn ngữ quy phạm

| Từ khóa | Ý nghĩa |
|---|---|
| **MUST / MUST NOT** | Bắt buộc / tuyệt đối không được phép |
| **SHOULD / SHOULD NOT** | Khuyến nghị mạnh; ngoại lệ phải có lý do, người phê duyệt và hạn hết hiệu lực |
| **MAY** | Tùy chọn, sau khi đánh giá tác động |

Các yêu cầu MUST chưa đáp ứng là lỗi chặn phát hành trong phạm vi chức năng liên quan.

### 1.2. Giới hạn pháp lý

“GDPR-aligned” thể hiện định hướng thiết kế, không tự động cấu thành chứng nhận tuân thủ pháp luật.

Trước khi vận hành thực tế, đơn vị quản lý MUST xác định:

- Vai trò data controller và data processor.
- Căn cứ pháp lý cho từng mục đích xử lý.
- Khu vực lưu trữ và cơ chế chuyển dữ liệu xuyên biên giới.
- Nghĩa vụ áp dụng đối với trẻ em và nhóm dễ bị tổn thương.
- Nhu cầu thực hiện DPIA và thẩm định đạo đức nghiên cứu.
- Danh sách bên xử lý phụ và thỏa thuận xử lý dữ liệu.

---

## 2. Phạm vi và mô hình đe dọa

### 2.1. Tài sản cần bảo vệ

- Danh tính và trạng thái đồng thuận của người tham gia.
- Câu trả lời, điểm số, lịch sử đánh giá và dữ liệu thời gian.
- Ngân hàng câu hỏi, đáp án, lời giải và metadata hiệu chuẩn.
- Tham số mô hình, manifest dữ liệu và artifact calibration.
- Token phiên, khóa giả danh hóa và khóa mã hóa.
- Dữ liệu phục vụ phân tích fairness.

### 2.2. Đe dọa chính

| Đe dọa | Hậu quả |
|---|---|
| Ghép telemetry với danh tính | Tái nhận dạng người tham gia |
| Thu thập khi chưa đồng thuận | Vi phạm quyền riêng tư và đạo đức nghiên cứu |
| Dữ liệu đã xóa quay lại từ backup | Không thực hiện đầy đủ quyền được xóa |
| Scraping phân tán | Rò rỉ ngân hàng đề |
| Nội gián hoặc quyền truy cập quá rộng | Xuất dữ liệu trái phép |
| Timeout do mạng yếu bị coi là thiếu năng lực | Sai lệch điểm và calibration |
| Giao diện không dùng được bằng công nghệ hỗ trợ | Loại trừ người dùng |
| Câu hỏi thiên lệch văn hóa | Đo đặc quyền hoặc kiến thức nền thay vì vốn từ |
| Nhóm phân tích quá nhỏ | Tiết lộ thuộc tính nhạy cảm |

### 2.3. Ranh giới tin cậy

```text
Web / Mobile Client
        │
        ▼
API Gateway ── Security signals / rate limiting
        │
        ├── Identity & Consent Service
        │       └── Identity Vault
        │
        ├── Assessment Service
        │       ├── Restricted Item Bank
        │       └── Operational Response Store
        │
        └── Telemetry Ingestion
                ├── Consent enforcement
                ├── Schema allowlist
                └── Research Store
                        │
                        ▼
                Controlled Calibration Jobs
                        │
                        ▼
                Versioned Model Registry
```

Client MUST được coi là không đáng tin cậy. Kiểm tra quyền, đồng thuận, giới hạn truy cập và tính hợp lệ dữ liệu MUST được thực thi phía server.

---

## 3. Nguyên tắc bảo vệ dữ liệu

### 3.1. Giới hạn mục đích

Dữ liệu MUST được tách thành ít nhất ba mục đích:

1. **Vận hành đánh giá:** dữ liệu tối thiểu để tiếp nhận câu trả lời và trả kết quả.
2. **An toàn hệ thống:** dữ liệu tối thiểu để phát hiện lạm dụng và xử lý sự cố.
3. **Nghiên cứu và hiệu chuẩn:** dữ liệu tùy chọn, chỉ được thu thập theo đồng thuận hợp lệ.

Không đồng thuận nghiên cứu MUST NOT làm mất quyền sử dụng chức năng đánh giá cốt lõi.

Nếu một nghiên cứu có điều kiện tham gia riêng, điều kiện đó MUST được công bố trước và không được che giấu dưới quyền truy cập dịch vụ thông thường.

### 3.2. Cấm PII trong responses và telemetry

Bảng `responses`, `telemetry_events`, dataset nghiên cứu và export tương ứng MUST NOT chứa:

- Họ tên, email, số điện thoại.
- Địa chỉ, ngày sinh đầy đủ hoặc vị trí chính xác.
- ID tài khoản trực tiếp từ nhà cung cấp đăng nhập.
- Cookie, access token, refresh token hoặc authorization header.
- IP thô, full user-agent hoặc fingerprint thiết bị.
- URL đầy đủ có query chứa dữ liệu người dùng.
- Nội dung câu hỏi, đáp án đúng hoặc lời giải.

Nếu sản phẩm cần PII để quản lý tài khoản, PII MUST nằm trong Identity Vault tách biệt.

Câu trả lời tự do có thể vô tình chứa PII. Chức năng này MUST mặc định bị vô hiệu hóa trong telemetry nghiên cứu; nếu thật sự cần, phải có đánh giá riêng, cảnh báo người dùng, cơ chế phát hiện/redaction và quyền truy cập hạn chế.

### 3.3. Không thu thập “để dùng sau”

Mỗi trường dữ liệu MUST có:

- Mục đích xử lý.
- Chủ sở hữu.
- Căn cứ xử lý.
- Thời hạn lưu.
- Tập quyền truy cập.
- Kiểm thử xác nhận không thu thập ngoài phạm vi.

Telemetry MUST dùng schema allowlist. Không chấp nhận trường `metadata` hoặc `properties` tùy ý không có schema.

SDK bên thứ ba MUST NOT tự động thu thập session replay, nội dung màn hình, clipboard, bàn phím hoặc advertising ID.

---

## 4. Giả danh hóa và quản lý định danh

### 4.1. `subject_id` một chiều

Hệ thống MUST sử dụng `subject_id` giả danh hóa dựa trên hàm băm có khóa:

```text
internal_subject_uuid = CSPRNG-generated UUID

subject_id =
  "sid_v1_" +
  base64url(
    HMAC-SHA-256(
      K_subject_v1,
      tenant_scope || ":" || purpose_scope || ":" || internal_subject_uuid
    )
  )
```

Yêu cầu:

- `internal_subject_uuid` không được suy ra từ email, số điện thoại hoặc tên.
- Khóa HMAC MUST được lưu trong KMS/HSM hoặc dịch vụ quản lý bí mật tương đương.
- Khóa MUST NOT xuất hiện trong source code, log hoặc cấu hình client.
- Dữ liệu đầu vào MUST được mã hóa theo định dạng canonical, không gây nhập nhằng.
- Không sử dụng `SHA256(email)` hoặc hash không khóa của PII.
- Không sử dụng `subject_id` làm bằng chứng xác thực hoặc bí mật truy cập.
- Phạm vi giả danh hóa SHOULD được tách theo tenant, mục đích và nghiên cứu để giảm khả năng liên kết chéo.

HMAC một chiều không có nghĩa là dữ liệu đã được ẩn danh hoàn toàn. Khi vẫn có thể liên kết qua Identity Vault, `subject_id` và dữ liệu gắn với nó MUST được quản lý như dữ liệu cá nhân giả danh hóa.

### 4.2. Identity Vault

Identity Vault MAY lưu liên kết giữa tài khoản, UUID nội bộ và các bí danh cần thiết cho quyền dữ liệu.

Vault MUST:

- Tách schema hoặc database và quyền truy cập khỏi Research Store.
- Mã hóa dữ liệu lưu trữ.
- Ghi audit mọi truy cập đặc quyền.
- Chỉ cung cấp thao tác nghiệp vụ cần thiết, không cho truy vấn join tùy ý.
- Cho phép dịch vụ xóa xác định tất cả bí danh thuộc một chủ thể.

Research analyst MUST NOT có quyền truy cập Vault.

### 4.3. Luân chuyển khóa

Khóa MUST có phiên bản và quy trình xoay vòng.

Khi thay khóa:

- Các bí danh cũ MUST vẫn được truy vết phục vụ yêu cầu xóa trong thời gian dữ liệu còn tồn tại.
- Không đổi khóa theo cách làm mất khả năng thực thi quyền dữ liệu.
- Việc hợp nhất bí danh giữa các phiên bản MUST chỉ diễn ra trong dịch vụ đặc quyền.
- Hủy khóa MUST được phối hợp với thời hạn backup và quy trình phục hồi.

---

## 5. Đồng thuận có hiểu biết

### 5.1. Thông tin bắt buộc

Trước khi thu thập telemetry nghiên cứu, người dùng MUST được thông báo bằng ngôn ngữ dễ hiểu về:

- Ai quản lý dữ liệu và cách liên hệ.
- Dữ liệu nào được thu thập.
- Mục đích nghiên cứu và hiệu chuẩn.
- Thời hạn lưu.
- Ai có quyền truy cập và dữ liệu có được chia sẻ hay không.
- Quyền từ chối, rút lại và yêu cầu xóa.
- Giới hạn thực tế đối với kết quả tổng hợp hoặc mô hình đã công bố.
- Ảnh hưởng của lựa chọn đến trải nghiệm sản phẩm.

Không được hứa rằng mọi dữ liệu đều “hoàn toàn ẩn danh” nếu còn khả năng liên kết.

### 5.2. Luồng bắt buộc

```text
UNDECIDED
   ├── Explicit opt-in  → GRANTED
   └── Decline          → DENIED

GRANTED
   ├── Withdraw         → WITHDRAWN
   └── Material change  → RECONSENT_REQUIRED

DENIED / WITHDRAWN / RECONSENT_REQUIRED
   └── New explicit opt-in → GRANTED
```

Yêu cầu UX:

- Không tích sẵn checkbox.
- Nút từ chối dễ thấy và dễ thao tác như nút đồng ý.
- Không gộp nghiên cứu với marketing hoặc điều khoản không liên quan.
- Không dùng dark pattern, đếm ngược hoặc ép đồng ý.
- Có màn hình xem và thay đổi lựa chọn.
- Giao diện xin đồng thuận MUST đáp ứng cùng chuẩn accessibility với sản phẩm.

### 5.3. Bằng chứng đồng thuận

Consent Store MUST lưu tối thiểu:

```json
{
  "consent_record_id": "cr_random",
  "subject_reference": "vault_scoped_reference",
  "purpose": "research_calibration",
  "status": "GRANTED",
  "notice_version": "privacy-research-1.0",
  "notice_digest": "sha256:...",
  "locale": "vi",
  "effective_at": "2026-01-01T10:00:00Z",
  "withdrawn_at": null,
  "collection_channel": "web"
}
```

Không cần lưu IP để chứng minh đồng thuận theo mặc định.

### 5.4. Thực thi phía server

Telemetry ingestion MUST kiểm tra đồng thuận độc lập với giá trị client gửi lên.

Một sự kiện chỉ được nhận vào Research Store khi:

```text
consent_at_capture == GRANTED
AND consent_at_ingestion == GRANTED
AND event_purpose is covered
AND notice_version is acceptable
AND schema is valid
```

Khi dịch vụ đồng thuận không khả dụng:

- Thu thập nghiên cứu MUST fail closed.
- Đánh giá cốt lõi SHOULD tiếp tục nếu an toàn.
- Không tạo hàng đợi telemetry mới để “xin phép sau”.

Không được thu thập trước đồng thuận rồi hồi tố hợp thức hóa.

### 5.5. Rút lại đồng thuận

Rút lại đồng thuận MUST:

1. Có hiệu lực đối với mọi lần ghi nghiên cứu tiếp theo sau khi giao dịch rút lại thành công.
2. Chặn ingest và loại bỏ sự kiện đang chờ.
3. Ngăn dữ liệu liên quan tham gia job calibration mới.
4. Vô hiệu hóa cache đồng thuận hoặc sử dụng cơ chế kiểm tra revocation có tính nhất quán.
5. Hiển thị rõ việc rút lại đồng thuận khác với xóa tài khoản như thế nào.

Đối với nghiên cứu dựa trên consent, dữ liệu có thể liên kết MUST được lên lịch xóa khi rút consent, trừ khi có căn cứ giữ lại độc lập, hợp lệ và đã được thông báo. Tính hợp pháp của xử lý trước thời điểm rút lại không tự động cho phép lưu dữ liệu vô thời hạn.

### 5.6. Người chưa thành niên

Nếu phục vụ người chưa thành niên, hệ thống MUST có chính sách độ tuổi theo khu vực và cơ chế xác minh/đồng thuận của người đại diện khi cần.

Không thu ngày sinh đầy đủ chỉ để kiểm tra ngưỡng tuổi nếu có phương án ít xâm phạm hơn. Khi chưa có cơ chế phù hợp, MUST tắt telemetry nghiên cứu cho nhóm này.

---

## 6. Hợp đồng dữ liệu telemetry

### 6.1. Schema tối thiểu đề xuất

```json
{
  "schema_version": "1.0",
  "event_id": "random-uuid",
  "subject_id": "sid_v1_...",
  "session_id": "opaque-short-lived-id",
  "purpose": "research_calibration",
  "consent_record_id": "cr_random",
  "event_type": "response_submitted",
  "item_version_id": "restricted-opaque-reference",
  "response_code": "choice_2",
  "active_duration_ms": 8400,
  "timing_quality": "valid",
  "connectivity_class": "degraded",
  "presentation_profile": "standard",
  "client_release": "web-1.4.0",
  "server_received_at": "2026-01-01T10:05:00Z"
}
```

Schema này là hợp đồng đề xuất, không phải migration xác nhận hiện trạng.

### 6.2. Quy tắc trường dữ liệu

| Trường | Quy tắc |
|---|---|
| `event_id` | Ngẫu nhiên; dùng chống trùng lặp |
| `session_id` | Không tái sử dụng xuyên sản phẩm |
| `item_version_id` | Tham chiếu server quản lý; không mã hóa đáp án |
| `response_code` | Mã lựa chọn đã kiểm tra; không phải nội dung tự do |
| `active_duration_ms` | Có thể null khi đo không đáng tin |
| `timing_quality` | `valid`, `interrupted`, `unknown`, `suspect` |
| `connectivity_class` | Nhóm thô; không chứa SSID, IP hoặc nhà mạng cụ thể |
| `presentation_profile` | Mã cấu hình trình bày; không suy diễn chẩn đoán khuyết tật |
| `server_received_at` | Timestamp chính xác chỉ ở tầng cần thiết |

Research export SHOULD giảm độ chính xác timestamp và loại bỏ định danh không cần thiết.

Không tự động phát hiện rồi ghi nhận việc dùng screen reader. Dữ liệu accommodation có thể tiết lộ thông tin nhạy cảm; chỉ được đưa vào nghiên cứu khi có mục đích, thông báo và căn cứ phù hợp.

### 6.3. Dữ liệu không hợp lệ

Payload chứa trường cấm MUST bị từ chối hoặc loại bỏ theo chính sách đã định.

Log lỗi MUST chỉ ghi mã lỗi, tên trường vi phạm và request ID an toàn; MUST NOT ghi lại toàn bộ payload bị từ chối.

---

## 7. Lưu trữ, xóa và quyền dữ liệu

### 7.1. Chính sách lưu trữ mặc định

Các thời hạn dưới đây là baseline đề xuất. Mỗi thay đổi MUST được phê duyệt trước triển khai.

| Loại dữ liệu | Thời hạn tối đa mặc định |
|---|---|
| Bộ đệm telemetry trên client | 24 giờ |
| Câu trả lời vận hành chi tiết | 30 ngày, trừ tính năng lịch sử đã được thông báo |
| Telemetry nghiên cứu thô | 90 ngày từ lúc nhận |
| Dataset nghiên cứu có thể liên kết | 12 tháng từ lúc thu thập ban đầu |
| IP thô phục vụ an ninh | 7 ngày |
| Bộ đếm rate limit | Theo cửa sổ kiểm soát, tối đa 24 giờ |
| Backup dữ liệu có thể liên kết | 35 ngày |
| Audit log bảo mật đã giảm thiểu | 12 tháng |
| Consent receipt | Theo lịch lưu bằng chứng được phê duyệt riêng |
| Artifact calibration | Theo vòng đời mô hình, có đánh giá rủi ro |
| Thống kê thực sự vô danh | Theo nhu cầu nghiên cứu và đánh giá tái nhận dạng định kỳ |

Biến đổi, sao chép hoặc huấn luyện lại MUST NOT đặt lại thời điểm bắt đầu retention.

Audit và consent receipt không được giữ nguyên toàn bộ câu trả lời dưới danh nghĩa “bằng chứng”.

TTL MUST áp dụng cho database, object storage, cache, warehouse, export và notebook workspace.

### 7.2. Quyền truy cập và xuất dữ liệu

Người dùng MUST có kênh:

- Xem trạng thái đồng thuận.
- Yêu cầu bản sao dữ liệu thuộc về mình.
- Sửa dữ liệu hồ sơ có thể sửa.
- Rút lại đồng thuận.
- Yêu cầu xóa tài khoản và dữ liệu liên quan.

Export MUST được xác thực, có liên kết tải hết hạn ngắn, không chứa dữ liệu người khác hoặc bí mật ngân hàng đề.

Quy trình xác minh danh tính MUST tương xứng với rủi ro; không mặc định yêu cầu thêm giấy tờ nhận dạng khi tài khoản đã xác thực đủ.

### 7.3. Quy trình xóa

```text
REQUESTED
   → VERIFIED
   → PROCESSING_BLOCKED
   → ACTIVE_DATA_PURGED
   → DOWNSTREAM_PURGED
   → MODEL_IMPACT_REVIEWED
   → BACKUP_EXPIRY_PENDING
   → COMPLETED
```

Quy trình MUST:

1. Xác minh yêu cầu.
2. Chặn xử lý mới và thu hồi phiên liên quan.
3. Xác định mọi bí danh trước khi xóa liên kết trong Vault.
4. Xóa responses, telemetry, feature rows, cache và export.
5. Hủy hoặc tái tạo snapshot/job chưa hoàn tất có dữ liệu liên quan.
6. Yêu cầu bên xử lý phụ thực hiện xóa và ghi nhận kết quả.
7. Đánh giá artifact calibration bị ảnh hưởng.
8. Xử lý bản sao lưu và thông báo trạng thái thực tế.

SLO nội bộ:

- Chặn xử lý mới: ngay khi yêu cầu đã được xác minh và cam kết.
- Xóa khỏi hệ thống hoạt động: tối đa 7 ngày.
- Hoàn tất xử lý yêu cầu và thông báo: mục tiêu trong một tháng; ngoại lệ và gia hạn phải theo luật áp dụng.
- Backup: hết hạn tối đa 35 ngày theo baseline.

Không được thông báo “đã xóa hoàn toàn” khi backup còn tồn tại mà không giải thích rõ giới hạn.

### 7.4. Backup và chống phục hồi dữ liệu đã xóa

Backup MUST:

- Được mã hóa, cô lập và không dùng cho truy vấn nghiệp vụ.
- Có thời hạn cố định.
- Không được dùng để tái tạo dataset nghiên cứu thông thường.

Deletion ledger MUST lưu tối thiểu các mã cần để ngăn dữ liệu sống lại, có quyền truy cập đặc biệt và retention riêng.

Khi restore:

```text
Restore into isolated environment
    → Apply deletion ledger
    → Purge expired data
    → Verify consent revocations
    → Run privacy checks
    → Allow production traffic
```

Nếu không thể xóa chọn lọc trong backup bất biến, dữ liệu MUST bị đặt ngoài sử dụng cho đến khi hết hạn. Quy trình này không thay thế đánh giá nghĩa vụ pháp lý cụ thể.

---

## 8. Xóa dữ liệu và calibration đã đóng băng

### 8.1. Nguyên tắc

“Frozen” nghĩa là artifact không được sửa âm thầm; không có nghĩa dữ liệu nguồn được miễn quyền xóa.

Hệ thống MUST phân biệt:

| Thành phần | Xử lý |
|---|---|
| Response/telemetry gắn với người dùng | Xóa theo yêu cầu |
| Dataset, feature store, snapshot có thể liên kết | Xóa hoặc tái tạo không có chủ thể |
| Ước lượng năng lực từng người | Dữ liệu cá nhân; phải xử lý xóa |
| Tham số item hoặc mô hình tổng hợp | Đánh giá riêng; không mặc định vô danh |
| Chỉ số tổng hợp nhóm nhỏ | Kiểm tra nguy cơ tái nhận dạng |
| Báo cáo đã công bố | Đánh giá tính vô danh và khả năng thu hồi thực tế |

### 8.2. Điều kiện giữ artifact

Artifact calibration chỉ MAY được giữ sau yêu cầu xóa nếu đánh giá được phê duyệt xác nhận:

- Không chứa định danh, câu trả lời cá nhân hoặc latent score từng người.
- Không kèm membership manifest có thể liên kết.
- Không cho phép suy ra hợp lý dữ liệu của một cá nhân trong bối cảnh sử dụng.
- Rủi ro từ mẫu nhỏ, outlier, mô hình ghi nhớ và suy luận membership đã được xem xét.
- Việc giữ artifact có căn cứ pháp lý phù hợp.

Hash dataset hoặc hash bản ghi không tự động làm dữ liệu vô danh.

Differential privacy MAY được dùng cho thống kê hoặc mô hình phù hợp, nhưng MUST có threat model, privacy budget, kiểm toán composition và đánh giá tác động lên độ chính xác/fairness. Chỉ thêm nhiễu không đủ để tuyên bố differential privacy.

### 8.3. Artifact không đạt điều kiện giữ

Nếu artifact còn mang rủi ro dữ liệu cá nhân hoặc cần loại bỏ đóng góp theo nghĩa vụ áp dụng:

1. Đánh dấu phiên bản bị ảnh hưởng.
2. Ngừng phục vụ khi mức rủi ro yêu cầu.
3. Hiệu chuẩn lại trên dataset đã làm sạch.
4. Tạo phiên bản mới.
5. Kiểm tra linking, độ lệch thang đo và ảnh hưởng điểm số.
6. Phê duyệt và chuyển phiên bản triển khai.
7. Hủy artifact cũ nếu không có căn cứ giữ hợp lệ.

Machine unlearning chỉ MAY thay thế retraining khi có bằng chứng hiệu quả phù hợp với loại mô hình và rủi ro. Không mặc định rằng mọi mô hình IRT hoặc calibration đều hỗ trợ xóa đóng góp chính xác.

### 8.4. Toàn vẹn và tái lập

Mỗi phiên bản calibration MUST có manifest gồm:

```text
model_version
artifact_digest
calibration_code_commit
item_bank_version
data_window
consent_policy_version
privacy_filter_version
inclusion_exclusion_rules
sample_size_summary
fit_and_fairness_report
approved_at
approved_by
supersedes_model_version
```

Manifest thông thường MUST NOT chứa danh sách `subject_id`.

Dataset lineage có thể liên kết chỉ được giữ trong phạm vi đặc quyền, có TTL và cơ chế xóa.

Sau khi dữ liệu nguồn bị xóa, khả năng tái lập bit-for-bit có thể không còn. Hệ thống MUST ghi nhận trung thực giới hạn đó; không giữ dữ liệu trái chính sách để bảo toàn tái lập tuyệt đối.

---

## 9. Bảo mật ngân hàng câu hỏi

### 9.1. Phân lớp nội dung

| Lớp | Ví dụ | Chính sách |
|---|---|---|
| Public practice | Câu luyện tập công khai | Chấp nhận mức exposure cao |
| Operational assessment | Câu dùng đánh giá | Phân phối có kiểm soát |
| Calibration pilot | Câu thử nghiệm | Phân phối theo kế hoạch |
| Retired/compromised | Câu nghỉ hoặc nghi rò rỉ | Không đưa vào đánh giá đang hiệu lực |

Ngân hàng luyện tập SHOULD tách khỏi ngân hàng đánh giá bảo mật.

### 9.2. API serving

API MUST:

- Chỉ trả câu hỏi đang được cấp quyền cho phiên.
- Không có endpoint liệt kê toàn bộ item cho người dùng thông thường.
- Không trả đáp án, lời giải, tham số IRT hoặc trạng thái pilot không cần thiết.
- Dùng opaque ID, nhưng không coi tính khó đoán của ID là kiểm soát quyền.
- Kiểm tra object-level authorization cho mọi request.
- Ràng buộc item lease với phiên, item version, thời hạn và nonce.
- Chống replay và chấm điểm lặp bằng idempotency.
- Dùng `Cache-Control: no-store` cho nội dung đánh giá nhạy cảm.
- Không đóng gói ngân hàng đề trong JS bundle, source map hoặc ứng dụng mobile.
- Không ghi nội dung đề vào log, tracing hoặc công cụ phân tích bên thứ ba.

Câu đã hiển thị luôn có thể bị chụp màn hình hoặc sao chép. Không được tuyên bố chống trích xuất tuyệt đối.

Không dùng chặn copy, chặn zoom hoặc phá ngữ nghĩa accessibility như biện pháp bảo mật chính.

### 9.3. Rate limiting đa chiều

Rate limiting MUST được thực thi theo:

- IP hoặc nhóm mạng phù hợp.
- Phiên đánh giá.
- Tài khoản/subject khi có.
- Tenant và toàn hệ thống.
- Tốc độ tạo phiên, không chỉ tốc độ lấy item.

Baseline để load test và điều chỉnh:

| Hành vi | Giới hạn khởi điểm |
|---|---|
| Cấp item mới theo session | 6/phút, burst 3 |
| Số phiên đồng thời theo tài khoản | 2 |
| Tạo phiên theo tài khoản | 10/giờ |
| Request lấy item theo IP | 120/phút, ưu tiên cảnh báo/challenge |
| Request trùng cùng idempotency key | Không tính là exposure mới |

Các giá trị MUST được kiểm định với blueprint, tốc độ làm bài thực tế và mạng NAT dùng chung.

Không hard-block người dùng chỉ vì một IP trường học hoặc nhà mạng vượt ngưỡng, trừ tình huống bảo vệ hệ thống khẩn cấp đã được định nghĩa.

Phản hồi giới hạn MUST có:

```text
HTTP 429
Retry-After: <seconds>
error_code: RATE_LIMITED
```

Retry MUST NOT làm mất câu trả lời, tiêu hao lượt làm bài hoặc bị tính là gian lận.

IP cho bộ đếm SHOULD dùng HMAC khóa luân chuyển với TTL ngắn. Dữ liệu này vẫn không được coi là vô danh.

### 9.4. Phát hiện extraction

Tín hiệu MAY bao gồm:

- Tạo nhiều phiên để lấy câu mới.
- Bỏ câu hàng loạt.
- Truy cập song song bất thường.
- Nhịp request không phù hợp luồng hiển thị.
- Lặp lại hành vi phủ rộng item pool.

Không dùng riêng thời gian trả lời nhanh, thiết bị yếu, screen reader hoặc kết nối bất ổn làm bằng chứng lạm dụng.

Biện pháp tăng dần:

```text
Observe → Throttle → Accessible challenge → Temporary restrict → Human review
```

CAPTCHA, nếu dùng, MUST có phương án tiếp cận tương đương, không chỉ thử thách hình ảnh/âm thanh và không mặc định gửi dữ liệu nghiên cứu sang bên thứ ba.

---

## 10. Item Exposure Control

### 10.1. Chỉ số

Exposure MUST được theo dõi theo item version và cohort/blueprint phù hợp:

```text
item_exposure_rate =
  unique_eligible_sessions_issued_item
  / unique_eligible_sessions_in_window
```

“Issued” được tính khi nội dung đã được server cấp ra, không chờ người dùng gửi câu trả lời hoặc xác nhận hiển thị.

Ngoài tỷ lệ, MUST có giới hạn tuyệt đối theo cửa sổ ngắn để phát hiện đột biến.

### 10.2. Cơ chế cấp item

Scheduler MUST phối hợp:

- Điều kiện nội dung và blueprint.
- Mức phù hợp năng lực.
- Ràng buộc accessibility.
- Exposure budget.
- Điều kiện chống lặp trong phiên.
- Ngẫu nhiên hóa có kiểm soát.

MAY dùng randomesque selection, phương pháp tương tự Sympson–Hetter hoặc shadow testing có ràng buộc exposure.

Ngưỡng exposure MUST được khai báo theo cấu hình vận hành, không dùng một ngưỡng chung cho mọi pool.

### 10.3. Tính nhất quán

Exposure reservation MUST là thao tác atomic.

```text
Select eligible candidate
    → Atomically reserve exposure budget
    → Persist item lease
    → Issue item
```

Không rollback exposure chỉ vì client khai báo chưa nhận được: nội dung có thể đã bị lấy.

Retry cùng item lease không tính là lần cấp item mới. Nếu hết pool hợp lệ, hệ thống MUST chọn fallback đã phê duyệt hoặc kết thúc an toàn; không âm thầm vượt ngưỡng.

### 10.4. Xử lý nghi rò rỉ

Khi item bị nghi compromise:

- Chuyển trạng thái `QUARANTINED`.
- Ngừng cấp mới.
- Đánh giá cửa sổ ảnh hưởng.
- Kiểm tra drift, item fit và response pattern.
- Hiệu chuẩn lại hoặc thay item nếu cần.
- Không tự động hủy điểm của toàn bộ người đã gặp item.
- Ghi nhận quyết định chuyên môn và cơ chế khiếu nại.

---

## 11. Accessibility: WCAG 2.1 AA

### 11.1. Phạm vi tuân thủ

Toàn bộ luồng Web và mobile web MUST đáp ứng WCAG 2.1 AA, bao gồm:

- Đăng nhập và đồng thuận.
- Bài đánh giá.
- Kết quả và thông báo lỗi.
- Yêu cầu quyền dữ liệu.
- Challenge chống lạm dụng.

Ứng dụng native MUST ánh xạ yêu cầu tương đương sang accessibility API của iOS/Android và kiểm thử bằng VoiceOver/TalkBack.

### 11.2. Yêu cầu giao diện

| Hạng mục | Yêu cầu |
|---|---|
| Tương phản chữ | Tối thiểu 4.5:1 cho chữ thường, 3:1 cho chữ lớn theo định nghĩa WCAG |
| Thành phần phi văn bản | Tối thiểu 3:1 với màu liền kề khi tiêu chí áp dụng |
| Màu sắc | Không dùng màu làm tín hiệu duy nhất |
| Zoom | Hỗ trợ phóng chữ 200% không mất nội dung/chức năng |
| Reflow | Hỗ trợ chiều rộng tương đương 320 CSS px, trừ ngoại lệ hợp lệ |
| Bàn phím | Dùng được toàn bộ chức năng; không keyboard trap |
| Focus | Hiển thị rõ, thứ tự hợp lý, không bị modal che khuất |
| Screen reader | Có tên, role, value và trạng thái đúng |
| Lỗi biểu mẫu | Mô tả bằng văn bản và liên kết với trường tương ứng |
| Chuyển động | Hạn chế hiệu ứng; tôn trọng `prefers-reduced-motion` |
| Nhấp nháy | Không vi phạm ngưỡng gây co giật của WCAG |
| Vùng chạm | Baseline sản phẩm 44 × 44 CSS px hoặc tương đương native |

Kích thước vùng chạm 44 × 44 là yêu cầu sản phẩm bổ sung, không được mô tả nhầm là tiêu chí AA của WCAG 2.1.

### 11.3. Ngữ nghĩa và screen reader

- Dùng HTML semantic và native controls trước custom ARIA.
- Nhóm đáp án dùng `fieldset`/`legend` hoặc ngữ nghĩa tương đương.
- Khi chuyển câu, focus MUST được đưa tới vị trí hợp lý.
- Thông báo trạng thái dùng live region vừa đủ; không đọc đồng hồ mỗi giây.
- Khai báo `lang` cho trang và đoạn đổi ngôn ngữ.
- Không nhúng từ cần đọc vào ảnh nếu có thể dùng văn bản.
- Alternative text MUST truyền đạt nội dung tương đương, không vô tình gợi ý đáp án.
- Audio/video MUST có phương án tương đương phù hợp với mục tiêu đo.

### 11.4. Font và khả năng đọc

- Cỡ chữ nội dung mặc định SHOULD từ 16 CSS px.
- Line height SHOULD khoảng 1.5.
- Dùng font Unicode hỗ trợ đầy đủ dấu tiếng Việt.
- Không dùng font trang trí cho thân bài.
- Không vô hiệu hóa browser zoom hoặc text scaling của hệ điều hành.
- Không cắt nội dung khi người dùng tăng text spacing.
- Font MUST có fallback cục bộ; không chặn hiển thị vì CDN font lỗi.

Không tuyên bố một font cụ thể phù hợp với mọi người có dyslexia. SHOULD cung cấp tùy chỉnh cỡ chữ, khoảng cách và giao diện.

### 11.5. Thời gian và accommodation

Đánh giá vốn từ không chủ đích đo tốc độ SHOULD không có hard timer theo câu.

Nếu giới hạn thời gian là thiết yếu:

- Lý do đo lường MUST được tài liệu hóa.
- Áp dụng yêu cầu timing adjustable hoặc xác định rõ ngoại lệ WCAG hợp lệ.
- Cung cấp accommodation phù hợp.
- Xác thực tính tương đương điểm giữa các điều kiện.
- Không âm thầm trừ điểm vì người dùng bật tính năng tiếp cận.

---

## 12. Trung lập thiết bị và mạng

### 12.1. Mục tiêu đo

Hệ thống MUST đo năng lực ngôn ngữ theo định nghĩa sản phẩm, không đo tốc độ tải mạng, CPU hoặc mức thành thạo công nghệ ngoài chủ đích.

Các khoảng thời gian MUST được tách:

```text
network_delivery_time
render_and_accessibility_ready_time
user_active_response_time
submission_transport_time
```

Không sử dụng:

```text
server_received_at - server_issued_at
```

như thời gian suy nghĩ thuần túy.

### 12.2. Mô hình sự kiện thời gian

```text
ITEM_ISSUED
    → CONTENT_READY
    → PRESENTED
    → RESPONSE_COMMITTED
    → RESPONSE_ACCEPTED
```

- `CONTENT_READY`: nội dung cần thiết và control đã sẵn sàng.
- `PRESENTED`: item có thể tương tác trong giao diện hiển thị.
- `RESPONSE_COMMITTED`: người dùng xác nhận đáp án.
- `RESPONSE_ACCEPTED`: server tiếp nhận thành công.

Thời gian phản hồi SHOULD dùng monotonic clock phía client giữa `PRESENTED` và `RESPONSE_COMMITTED`.

Client timing là dữ liệu không hoàn toàn đáng tin. Server MUST kiểm tra giới hạn hợp lý, thứ tự sự kiện và gắn `timing_quality`; không dùng timing client làm cơ chế chống gian lận duy nhất.

### 12.3. Timeout và latency adjustment

- Timeout truyền tải MUST NOT tự động trở thành câu trả lời sai.
- Thời gian retry gửi đáp án MUST NOT cộng vào thời gian suy nghĩ.
- Dữ liệu thời gian bị gián đoạn MUST được đánh dấu thay vì “sửa” bằng hằng số tùy ý.
- Không trừ một RTT ước lượng duy nhất khỏi toàn bộ thời gian rồi coi kết quả là chính xác.
- Nếu cần ước lượng latency, thuật toán MUST được version hóa và kiểm định.
- Session expiration MUST phân biệt với item-response timeout.
- Resume MUST bảo toàn đáp án đã được xác nhận.

Mã trạng thái tối thiểu:

```text
ANSWERED
OMITTED_BY_USER
NOT_REACHED
TECHNICAL_INTERRUPTION
TIMING_UNRELIABLE
```

`TECHNICAL_INTERRUPTION` MUST NOT được mặc định ánh xạ sang `INCORRECT`.

Dữ liệu thiếu MUST được xử lý theo kế hoạch psychometrics đã phê duyệt; không mặc định thiếu ngẫu nhiên và không loại toàn bộ người dùng mạng yếu.

### 12.4. Offline và retry

- Request gửi đáp án MUST có idempotency key.
- UI MUST phân biệt “đã chọn”, “đang gửi” và “đã lưu”.
- Không tải trước toàn bộ ngân hàng đề để hỗ trợ offline.
- Nếu lưu tạm trên thiết bị, chỉ lưu dữ liệu tối thiểu và có TTL.
- Đăng xuất hoặc hoàn tất phiên MUST xóa hàng đợi cục bộ theo chính sách.
- Không coi local storage là kho bí mật chống XSS.
- Lưu cục bộ MUST không bao gồm đáp án đúng hoặc khóa ngân hàng đề.

### 12.5. Baseline hiệu năng

CI/staging MUST có bài kiểm thử tối thiểu với:

```text
Viewport: 320 CSS px
CPU throttling: 4×
Network: 400 kbps downstream / 200 kbps upstream
RTT: 400 ms
Packet loss: 2%
Connectivity loss: 30–120 seconds
Assistive technology: keyboard + screen reader
```

Đây là cấu hình stress test, không phải định nghĩa phổ quát của mạng 3G.

Mục tiêu:

- Payload item văn bản SHOULD ≤ 30 KB sau nén, không tính asset đặc biệt.
- Asset dùng cho construct MUST có ngân sách riêng và preload hợp lý.
- Không bắt đầu đo trước khi nội dung thiết yếu sẵn sàng.
- Không mất hoặc ghi trùng câu trả lời đã xác nhận.
- Không gắn cờ gian lận chỉ do cấu hình kiểm thử trên.

---

## 13. Fairness và nội dung trung lập văn hóa

### 13.1. Hướng dẫn biên soạn

Item MUST:

- Đo đúng construct vốn từ đã định nghĩa.
- Tránh kiến thức thương hiệu, giải trí, du lịch hoặc mức sống không cần thiết.
- Không giả định mọi người có cùng trải nghiệm đô thị, giáo dục hoặc nghề nghiệp.
- Không dùng định kiến giới, dân tộc, tôn giáo, vùng miền hoặc khuyết tật.
- Phân biệt nghĩa chuẩn đích đo với biến thể phương ngữ hợp lệ.
- Tránh distractor dựa trên sự chế giễu một cộng đồng.
- Có ngữ cảnh đủ để giảm nhập nhằng không liên quan đến vốn từ.

“Trung lập văn hóa” không có nghĩa xóa mọi yếu tố văn hóa khỏi ngôn ngữ. Mục tiêu là tránh yếu tố ngoài construct tạo lợi thế không hợp lý.

### 13.2. Quy trình duyệt

Mỗi item trước production MUST có:

1. Duyệt ngôn ngữ và độ chính xác.
2. Duyệt construct và blueprint.
3. Duyệt văn hóa/vùng miền.
4. Duyệt accessibility.
5. Pilot và phân tích psychometrics.
6. Quyết định chấp nhận, sửa, nghiên cứu tiếp hoặc loại.

Ít nhất hai reviewer SHOULD độc lập ở bước nội dung; đội reviewer SHOULD có đa dạng vùng miền và bối cảnh phù hợp quần thể mục tiêu.

### 13.3. Phân tích DIF và measurement invariance

Phân tích fairness SHOULD bao gồm:

- DIF đồng nhất và không đồng nhất.
- Nhóm vùng miền/ngôn ngữ được tự khai báo phù hợp.
- Thiết bị, chất lượng kết nối và presentation profile khi có căn cứ.
- Tác động tổng hợp lên điểm, không chỉ từng item.
- Độ bất định, effect size và multiple-testing correction.

MAY dùng logistic regression, Mantel–Haenszel hoặc multi-group IRT tùy dữ liệu và giả định.

Yêu cầu:

- Không kết luận bias chỉ từ chênh lệch tỷ lệ đúng thô.
- Không kết luận “không bias” chỉ vì kiểm định không có ý nghĩa thống kê.
- Cỡ mẫu tối thiểu MUST dựa trên power analysis hoặc mô phỏng.
- DIF là tín hiệu điều tra, không tự động chứng minh phân biệt đối xử.
- Không bỏ item chỉ để làm đẹp chỉ số nếu làm hỏng blueprint.

### 13.4. Dữ liệu nhóm và quyền riêng tư

Thuộc tính nhóm MUST:

- Là tự nguyện khi dùng cho nghiên cứu tùy chọn.
- Có lựa chọn không trả lời.
- Không suy diễn từ tên, IP hoặc giọng nói.
- Không dùng để thay đổi quyền truy cập hoặc phạt điểm.
- Được tách quyền truy cập khỏi telemetry thông thường.

Không công bố ô thống kê nhỏ hơn 20 người theo baseline. Phải có suppression bổ sung để tránh suy ngược từ tổng; ngưỡng 20 không phải bảo đảm vô danh.

### 13.5. Fairness của bộ lọc chất lượng

Quy tắc loại dữ liệu như “trả lời quá nhanh”, “nhiều lần gián đoạn” hoặc “phiên quá dài” MUST được đánh giá tác động theo nhóm.

Ưu tiên loại riêng trường timing không hợp lệ thay vì loại câu trả lời đúng/sai còn dùng được.

Không được coi thiếu dữ liệu accessibility hoặc demographic là bằng chứng chất lượng thấp.

---

## 14. Kiểm soát truy cập và bảo mật nền tảng

### 14.1. Least privilege

| Vai trò | Quyền cho phép | Quyền bị cấm mặc định |
|---|---|---|
| Assessment Runtime | Cấp item và ghi response trong phạm vi phiên | Export toàn bộ bank |
| Telemetry Ingestor | Ghi schema hợp lệ sau kiểm tra consent | Đọc PII |
| Calibration Worker | Đọc dataset được cấp riêng cho job | Truy cập Identity Vault |
| Research Analyst | Dữ liệu giảm thiểu/aggregate | Re-identification, bulk raw export |
| Item Author | Biên soạn item được phân công | Dữ liệu người tham gia |
| Privacy Operator | Điều phối quyền dữ liệu | Đọc nội dung đề nếu không cần |
| Security Operator | Log an ninh tối thiểu | Telemetry nghiên cứu mặc định |

Tài khoản người dùng nội bộ MUST dùng MFA. Quyền đặc biệt MUST có thời hạn và audit.

### 14.2. Bảo vệ hạ tầng

- TLS 1.2 trở lên; SHOULD ưu tiên TLS 1.3.
- Mã hóa dữ liệu lưu trữ và backup bằng KMS-managed keys.
- Service identity riêng; không dùng credential quản trị dùng chung.
- Kiểm soát tenant và object-level authorization ở server.
- Secret scanning, dependency scanning và kiểm thử authorization trong CI.
- CSP và phòng chống XSS phù hợp ứng dụng.
- Cookie phiên dùng `Secure`, `HttpOnly`, `SameSite` khi áp dụng.
- Production data MUST NOT được sao chép xuống máy phát triển.
- Dữ liệu test MUST là synthetic hoặc đã qua quy trình vô danh hóa được đánh giá.
- Export nhạy cảm MUST có phê duyệt, TTL và audit.

Không đưa dữ liệu người tham gia hoặc ngân hàng đề vào dịch vụ AI bên ngoài nếu chưa có đánh giá nhà cung cấp, thỏa thuận phù hợp và cấu hình giới hạn sử dụng/lưu trữ.

---

## 15. Audit, sự cố và trách nhiệm

### 15.1. Audit event bắt buộc

```text
CONSENT_GRANTED
CONSENT_WITHDRAWN
RESEARCH_INGEST_REJECTED
PRIVILEGED_ACCESS_GRANTED
RESEARCH_EXPORT_CREATED
ERASURE_REQUEST_VERIFIED
ERASURE_STAGE_COMPLETED
BACKUP_RESTORE_PRIVACY_CHECKED
MODEL_PRIVACY_REVIEW_COMPLETED
ITEM_QUARANTINED
ACCESSIBILITY_EXCEPTION_APPROVED
```

Audit MUST có tính toàn vẹn và kiểm soát sửa đổi. Không đưa PII, nội dung response hoặc toàn bộ payload vào audit.

### 15.2. Ứng phó sự cố

Runbook MUST bao gồm:

1. Phát hiện và phân loại.
2. Cô lập nguồn rò rỉ.
3. Thu hồi token/khóa khi cần.
4. Xác định dữ liệu và nhóm bị ảnh hưởng.
5. Bảo toàn bằng chứng tối thiểu.
6. Đánh giá nghĩa vụ thông báo.
7. Khắc phục và theo dõi.
8. Postmortem không đổ lỗi, có hành động cụ thể.

Nếu GDPR áp dụng, đánh giá nghĩa vụ thông báo cơ quan có thẩm quyền trong 72 giờ kể từ khi nhận biết vi phạm, trừ trường hợp ngoại lệ theo luật; thông báo chủ thể khi có rủi ro cao và điều kiện luật định.

### 15.3. Chủ sở hữu

| Lĩnh vực | Trách nhiệm phê duyệt |
|---|---|
| Privacy/retention/erasure | Privacy Lead hoặc người phụ trách được chỉ định |
| API/item security | Security Lead |
| Calibration và timing | Psychometrics Lead |
| WCAG và accommodation | Accessibility Lead |
| Triển khai và rollback | Engineering Lead |
| Nghiên cứu nhóm nhạy cảm | Ethics/Research Governance |

Một người có thể đảm nhiệm nhiều vai trò trong đội nhỏ, nhưng quyết định rủi ro cao SHOULD có người duyệt thứ hai độc lập.

---

## 16. Kiểm thử chấp nhận P0.7

### 16.1. Privacy và consent

| ID | Kịch bản | Điều kiện đạt |
|---|---|---|
| PRIV-01 | Payload có email/phone/field lạ | Bị từ chối; log không chứa giá trị |
| PRIV-02 | Người dùng chưa đồng thuận | Không có bản ghi trong Research Store |
| PRIV-03 | Client giả `consent=true` | Server vẫn từ chối |
| PRIV-04 | Rút consent khi có queue | Không ingest queue; không dùng cho job mới |
| PRIV-05 | Consent service lỗi | Nghiên cứu fail closed; core flow không bị ép opt-in |
| PRIV-06 | Analyst thử join Vault | Bị chặn và có audit |
| PRIV-07 | Xoay khóa subject | Vẫn xóa được toàn bộ bí danh còn dữ liệu |
| PRIV-08 | TTL hết hạn | Xóa ở mọi tầng, kể cả export và cache |

### 16.2. Erasure và model integrity

| ID | Kịch bản | Điều kiện đạt |
|---|---|---|
| ERASE-01 | Xóa tài khoản có nhiều phiên/bí danh | Không còn dữ liệu active thuộc phạm vi xóa |
| ERASE-02 | Job calibration đang chạy | Hủy hoặc tái tạo dataset sạch trước promote |
| ERASE-03 | Restore backup trước ngày xóa | Deletion ledger được áp dụng trước mở truy cập |
| ERASE-04 | Frozen artifact còn participant score | Không được giữ theo giả định “aggregate” |
| ERASE-05 | Artifact cần thay | Có version mới, lineage và quyết định chuyển đổi |
| ERASE-06 | Processor bên ngoài giữ export | Có xác nhận xử lý hoặc escalation theo SLA |

### 16.3. Item bank

| ID | Kịch bản | Điều kiện đạt |
|---|---|---|
| SEC-01 | Đổi item ID của phiên khác | Không truy cập được nội dung |
| SEC-02 | Replay item/response token | Không cấp/chấm trùng ngoài hợp đồng |
| SEC-03 | Scraping nhiều session | Kích hoạt kiểm soát đa chiều |
| SEC-04 | Nhiều người dùng chung NAT | Không phạt diện rộng chỉ theo IP |
| SEC-05 | Đồng thời chạm exposure cap | Reservation không vượt ngưỡng |
| SEC-06 | Kiểm tra bundle/log/cache | Không có đáp án hoặc bank dump |
| SEC-07 | Item đã quarantine | Không được cấp mới |

### 16.4. Accessibility và mạng

| ID | Kịch bản | Điều kiện đạt |
|---|---|---|
| A11Y-01 | Chỉ dùng bàn phím | Hoàn thành mọi luồng cốt lõi |
| A11Y-02 | NVDA/Firefox hoặc Chrome; VoiceOver/Safari | Đọc và thao tác đúng trên ma trận hỗ trợ |
| A11Y-03 | TalkBack/Android | Hoàn thành luồng mobile hỗ trợ |
| A11Y-04 | Zoom, reflow và text spacing | Không mất nội dung hoặc chức năng |
| A11Y-05 | Kiểm tra contrast thủ công/tự động | Đạt các tiêu chí AA áp dụng |
| A11Y-06 | Challenge chống bot | Có lựa chọn tiếp cận tương đương |
| NET-01 | RTT cao, mất mạng rồi retry | Không sai điểm hoặc ghi trùng |
| NET-02 | Render chậm trên CPU yếu | Không cộng render time vào response time |
| NET-03 | Background/resume | Timing được đánh dấu đúng; đáp án được bảo toàn |
| NET-04 | Client sửa clock | Không làm hỏng integrity hoặc bị tin tuyệt đối |

Công cụ tự động không đủ để chứng nhận WCAG. Release MUST có kiểm thử thủ công và kiểm thử với công nghệ hỗ trợ; SHOULD có người dùng khuyết tật tham gia đánh giá.

### 16.5. Fairness

| ID | Kịch bản | Điều kiện đạt |
|---|---|---|
| FAIR-01 | Item mới | Có checklist duyệt nội dung/văn hóa/accessibility |
| FAIR-02 | Nhóm mẫu nhỏ | Không kết luận công bằng thiếu căn cứ |
| FAIR-03 | Quy tắc rapid-response | Có đánh giá false positive và tác động nhóm |
| FAIR-04 | Báo cáo subgroup | Suppression và kiểm tra suy ngược hoạt động |
| FAIR-05 | Thay presentation/accommodation | Có đánh giá tương đương đo lường phù hợp |

---

## 17. Quan sát vận hành và chỉ số

Dashboard MUST theo dõi ở dạng tổng hợp, hạn chế chiều phân tách có nguy cơ tái nhận dạng:

- Số ingest bị từ chối vì thiếu consent.
- Số payload chứa trường cấm.
- Độ trễ thực thi rút consent và erasure.
- Số bản sao quá hạn retention.
- Số export đặc quyền và truy cập bất thường.
- Exposure theo pool và số item quarantine.
- Tỷ lệ `TECHNICAL_INTERRUPTION` và `TIMING_UNRELIABLE`.
- Tỷ lệ hoàn thành theo nhóm thiết bị/kết nối khi có căn cứ xử lý.
- Lỗi accessibility chưa khắc phục.
- Chỉ số DIF, độ bất định và trạng thái điều tra.

Không tối ưu tỷ lệ đồng ý nghiên cứu bằng dark pattern. Không đánh đổi quyền riêng tư để tăng độ phủ telemetry.

---

## 18. Release gate

P0.7 chỉ được đánh dấu hoàn tất khi có đủ:

- [ ] Data inventory và sơ đồ luồng dữ liệu đã duyệt.
- [ ] Identity Vault tách biệt và `subject_id` HMAC có quản lý khóa.
- [ ] Schema allowlist; không có PII trong responses/telemetry.
- [ ] Consent trước thu thập và enforcement phía server.
- [ ] Rút consent chặn cả queue và downstream jobs.
- [ ] Retention tự động và báo cáo kiểm chứng.
- [ ] Erasure end-to-end, gồm backup restore và processor bên ngoài.
- [ ] Chính sách frozen calibration không miễn trừ quyền dữ liệu.
- [ ] API authorization, rate limiting và exposure control đã kiểm thử.
- [ ] Không rò bank/đáp án qua bundle, log, cache hoặc export.
- [ ] Báo cáo WCAG 2.1 AA cho toàn bộ luồng trọng yếu.
- [ ] Kiểm thử thiết bị yếu, mạng bất ổn và công nghệ hỗ trợ.
- [ ] Chính sách timing/missingness được Psychometrics Lead phê duyệt.
- [ ] Checklist bias nội dung và kế hoạch DIF/fairness.
- [ ] Runbook sự cố và quyền dữ liệu đã diễn tập.
- [ ] Không còn lỗi P0/P1 về privacy, security hoặc accessibility trong phạm vi phát hành.

Ngoại lệ MUST có mô tả tác động, biện pháp giảm thiểu, người chịu trách nhiệm và ngày hết hiệu lực. Không được dùng ngoại lệ để hợp thức hóa thu thập thiếu căn cứ pháp lý, truy cập trái phép hoặc tuyên bố tuân thủ sai sự thật.

---

## 19. Nguyên tắc bất biến

```text
No research consent → No research telemetry.

Pseudonymous ≠ Anonymous.

Frozen calibration ≠ Permission to retain personal data forever.

Network delay ≠ Low vocabulary ability.

Assistive technology ≠ Suspicious behavior.

Item secrecy ≠ Justification for inaccessible UI.

Statistical non-significance ≠ Proof of fairness.

Reproducibility never overrides lawful erasure obligations.
```

**Kết luận hợp đồng:** `vocabulary-research` MUST bảo vệ đồng thời tính hợp lệ của phép đo, quyền kiểm soát dữ liệu của người tham gia và khả năng tiếp cận công bằng. Không thành phần nào được xem là phần bổ sung có thể trì hoãn sau khi hệ thống đã thu thập dữ liệu hoặc đưa ra kết quả đánh giá.