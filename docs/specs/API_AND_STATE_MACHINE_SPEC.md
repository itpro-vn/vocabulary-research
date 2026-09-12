# API_AND_STATE_MACHINE_SPEC.md

> **Data-integration constraint:** [The actual LazzyBee source](../data/LAZZYBEE_SNAPSHOT_AUDIT.md) is a dictionary/learning snapshot, not an assessment response dataset. Preserve source IDs through a reviewed crosswalk and serve separately authored ItemVersions. The offline CLI does not implement this API; Dont Know, no-score statuses, server-side answer authority and versioned release contracts still require joint validation with Scoring.

| Thuộc tính | Giá trị |
|---|---|
| Dự án | `vocabulary-research` |
| Repository | `itpro-vn/vocabulary-research` |
| Mốc đặc tả | **P0.4 — API Contracts & Session State Machine** |
| Phiên bản giao thức | `v1` |
| Trạng thái tài liệu | Đặc tả đề xuất để phê duyệt và triển khai |
| Đối tượng | Backend, frontend, mobile, psychometrics, QA, security, data engineering |
| Phạm vi | Vòng đời phiên đánh giá, phân phối item, nộp phản hồi, phục hồi phiên và trả kết quả |

> Tài liệu này định nghĩa hợp đồng đích của P0.4, không khẳng định repository hiện tại đã triển khai các hành vi bên dưới. Khi áp dụng, nhóm phát triển MUST đối chiếu với mã nguồn, mô hình dữ liệu và các quyết định kiến trúc đã được phê duyệt.

---

## 1. Mục tiêu và ngôn ngữ quy phạm

Các từ khóa:

- **MUST / MUST NOT**: yêu cầu bắt buộc.
- **SHOULD / SHOULD NOT**: khuyến nghị mạnh; ngoại lệ cần được ghi nhận.
- **MAY**: tùy chọn có kiểm soát.

Đặc tả phải bảo đảm:

1. Một phản hồi hợp lệ được ghi nhận **tối đa một lần**, kể cả khi client gửi lại.
2. Chỉ backend quyết định item tiếp theo, điều kiện dừng và kết quả.
3. Mất mạng hoặc retry không làm thay đổi câu trả lời đã chấp nhận.
4. Đồng hồ client không quyết định thời hạn hoặc trạng thái phiên.
5. Việc chuyển thiết bị có cơ chế chuyển quyền ghi rõ ràng.
6. Client không nhận dữ liệu có thể dùng để suy ra trực tiếp đáp án hoặc tham số chấm điểm.
7. Kết quả có thông tin bất định, phiên bản mô hình và giới hạn diễn giải.

### 1.1. Ngoài phạm vi

Tài liệu không định nghĩa:

- Thuật toán chọn item cụ thể.
- Cấu trúc item bank đầy đủ.
- Quy trình hiệu chuẩn tham số đo lường.
- Dashboard quản trị.
- Cơ chế xác thực người dùng cấp tổ chức.
- API xóa dữ liệu cá nhân.

Các thành phần này MUST tuân thủ những bất biến giao thức được quy định ở đây.

---

## 2. Các thực thể và bất biến

### 2.1. Thực thể chính

| Thực thể | Ý nghĩa |
|---|---|
| `AssessmentSession` | Một lần thực hiện đánh giá của một chủ thể |
| `ItemDelivery` | Một lần backend cấp một item cho một phiên |
| `AcceptedResponse` | Phản hồi bất biến đã được backend chấp nhận |
| `WriterLease` | Quyền ghi độc quyền của một thiết bị vào phiên |
| `IdempotencyRecord` | Ánh xạ khóa idempotency tới yêu cầu và kết quả đã commit |
| `AssessmentResult` | Kết quả cuối cùng bất biến của phiên |
| `AuditEvent` | Sự kiện phục vụ kiểm toán, xử lý sự cố và integrity |

### 2.2. Bất biến bắt buộc

1. Một phiên có tối đa một `ItemDelivery` chưa được xử lý.
2. Một `delivery_id` có tối đa một `AcceptedResponse`.
3. Một phiên có tối đa một writer lease đang hiệu lực.
4. Item đã được cấp MUST NOT bị thay thế chỉ vì refresh, retry hoặc đổi thiết bị.
5. Phản hồi đã chấp nhận MUST NOT bị sửa hoặc thay bằng phản hồi khác.
6. Phiên terminal MUST NOT nhận thêm phản hồi hoặc được mở lại.
7. Chỉ phiên `completed` có `AssessmentResult` được công bố.
8. `completed` MUST có đúng một kết quả cuối cùng.
9. Backend MUST cố định phiên bản assessment, item bank, scoring model và timing policy cho phiên.
10. Frontend MUST NOT tự tính hoặc tự công bố điểm chính thức.
11. Không có “exactly-once delivery” ở tầng mạng; hệ thống cung cấp **at-least-once transport, at-most-once acceptance và deterministic replay**.
12. `session_version` tăng đơn điệu khi có thay đổi nghiệp vụ; đọc hoặc replay không làm tăng phiên bản.

### 2.3. Nguồn sự thật

Backend là nguồn sự thật đối với:

- Trạng thái phiên.
- Thời hạn.
- Item hiện hành.
- Phản hồi đã chấp nhận.
- Điều kiện hoàn tất.
- Quyền ghi.
- Integrity decision.
- Kết quả và bất định.

Client chỉ cung cấp:

- Lựa chọn của người tham gia.
- Dấu thời gian cục bộ.
- Sự kiện vòng đời ứng dụng.
- Dữ liệu phục hồi có thể kiểm tra.

---

## 3. Session lifecycle state machine

### 3.1. Định nghĩa trạng thái

| Trạng thái | Ý nghĩa | Terminal |
|---|---|---|
| `created` | Phiên đã được tạo, chưa cấp item đầu tiên | Không |
| `in_progress` | Đã cấp ít nhất một item; có thể tiếp tục hoặc chờ hoàn tất | Không |
| `completed` | Đã chốt kết quả thành công | Có |
| `expired` | Đã vượt hard deadline | Có |
| `invalidated` | Phiên bị vô hiệu do vi phạm integrity, cấu hình hoặc quyết định quản trị | Có |
| `abandoned` | Phiên bị bỏ dở trước hard deadline | Có |

`ready_to_complete` không phải trạng thái lifecycle. Đây là thuộc tính của phiên `in_progress`.

### 3.2. Sơ đồ

```text
                     first item issued
         created --------------------------> in_progress
            |                                     |
            | hard deadline                       | valid complete request
            v                                     v
         expired                              completed

created / in_progress -- hard deadline ----------> expired
created / in_progress -- integrity/admin --------> invalidated
created / in_progress -- abandonment trigger ----> abandoned

completed / expired / invalidated / abandoned
    => terminal; không có chuyển trạng thái tiếp theo
```

### 3.3. Bảng chuyển trạng thái

| Từ | Đến | Trigger | Điều kiện và tác động |
|---|---|---|---|
| Không có | `created` | `start(action=create)` | Chủ thể hợp lệ; assessment khả dụng; cố định cấu hình |
| `created` | `in_progress` | `next-item` cấp item đầu tiên | Lease hợp lệ; chưa quá hạn; tạo delivery và chuyển trạng thái trong cùng transaction |
| `in_progress` | `in_progress` | Chấp nhận response | Ghi response; cập nhật estimator và điều kiện dừng |
| `in_progress` | `completed` | `complete` | Không còn pending delivery; đạt điều kiện dừng; kết quả được commit nguyên tử |
| `created` hoặc `in_progress` | `expired` | Hard deadline | `server_now >= expires_at` |
| `created` hoặc `in_progress` | `abandoned` | Hết inactivity deadline | Chưa vượt hard deadline; vượt ngưỡng bỏ dở do policy quy định |
| `created` hoặc `in_progress` | `abandoned` | Chủ thể hủy rõ ràng | Qua control-plane command được xác thực |
| `created` hoặc `in_progress` | `invalidated` | Quyết định integrity/quản trị | Có mã lý do và audit event; không chỉ dựa trên một tín hiệu timing yếu |

### 3.4. Terminality và hiệu lực kết quả

Một phiên đã `completed` MUST NOT chuyển sang `invalidated`.

Nếu phát hiện vấn đề sau hoàn tất:

- Kết quả gốc vẫn bất biến.
- Hệ thống dùng bản ghi thu hồi/đính chính riêng.
- API công bố kết quả sau này MUST kiểm tra trạng thái thu hồi.
- Không sửa lịch sử lifecycle để che giấu việc đã công bố kết quả.

### 3.5. Thời hạn và inactivity

Mỗi phiên có:

- `created_at`
- `expires_at`: hard deadline, không được gia hạn qua retry, polling hoặc takeover.
- `last_activity_at`
- `abandon_at`: inactivity deadline, không vượt `expires_at`.

Các hành động được tính là hoạt động:

- Tạo phiên.
- Cấp một delivery mới.
- Chấp nhận một response mới.
- Resume hoặc takeover được cấp lease mới, có rate limit.

Các hành động MUST NOT giữ phiên sống vô hạn:

- Replay cùng một request.
- Polling `next-item` khi item hiện hành không đổi.
- GET tự động do prefetch.
- Traffic lỗi hoặc không có quyền.

Inactivity policy SHOULD lớn hơn thời gian làm một item hợp lý. Backgrounding hoặc mất mạng ngắn hạn MUST NOT tự động làm phiên bị invalidated.

### 3.6. Ưu tiên khi có cạnh tranh

Backend MUST serialize thay đổi trên cùng một phiên bằng row lock, compare-and-swap hoặc cơ chế tương đương.

Trong transaction:

1. Nếu đã terminal, giữ nguyên.
2. Nếu `server_now >= expires_at`, chuyển `expired`.
3. Nếu `server_now >= abandon_at`, chuyển `abandoned`.
4. Nếu có quyết định invalidation đã được xác thực, áp dụng quyết định đó.
5. Kiểm tra lease, version và điều kiện nghiệp vụ.
6. Thực hiện thay đổi.

Thời điểm quyết định là thời điểm kiểm tra bằng đồng hồ backend trong transaction, không phải timestamp client gửi.

Worker hết hạn có thể chạy trễ, nhưng mọi API MUST tự kiểm tra deadline. Không được dựa hoàn toàn vào background worker.

### 3.7. Control plane

Bốn API công khai trong tài liệu không bao gồm endpoint hủy hoặc quản trị.

Các lệnh nội bộ tương ứng MUST tồn tại ở tầng service:

```text
AbandonSession(session_id, actor, reason)
InvalidateSession(session_id, actor, reason, evidence_reference)
ExpireSession(session_id, evaluated_at)
```

Nếu client cần nút “Hủy phiên”, endpoint riêng MUST được đặc tả trước khi phát hành tính năng. Không dùng `/complete` để biểu diễn abandonment.

---

## 4. State machine của một item

```text
not_issued
    |
    | backend selects and binds item
    v
issued
    |
    | first valid response accepted
    v
answered

issued -- session becomes terminal --> closed_unanswered
```

### 4.1. Quy tắc phân phối

- `delivery_id` là định danh ngẫu nhiên, opaque.
- `item_ref` là tham chiếu opaque trong phiên, không phải ID trực tiếp của item bank.
- Backend MUST lưu assignment trước hoặc đồng thời với việc trả payload.
- Retry `next-item` khi còn pending delivery MUST trả lại cùng `delivery_id`, nội dung và thứ tự lựa chọn.
- `delivery_token` MAY được cấp lại sau takeover, nhưng item không đổi.
- Không được dùng số lần gọi GET để chọn lại hoặc “reroll” item.
- Sau khi response được chấp nhận, chỉ một lần gọi `next-item` tiếp theo mới cấp delivery mới.

### 4.2. Ngữ nghĩa đặc biệt của GET

`GET /next-item` có thể materialize assignment hoặc cấp lại delivery token. Đây là ngoại lệ có chủ đích đối với tính “safe” thông thường của GET.

Để giảm rủi ro:

- Endpoint MUST có authentication và active writer lease.
- Client MUST NOT prefetch hoặc speculative-load.
- Response MUST có `Cache-Control: no-store`.
- Proxy/CDN MUST NOT cache.
- GET lặp lại không được tăng item sequence hoặc chấm điểm.
- Hai GET đồng thời MUST hội tụ về cùng một pending delivery.
- Quyền truy cập endpoint này không được cấp cho vai trò chỉ đọc.

Nếu kiến trúc yêu cầu GET hoàn toàn không có tác dụng phụ, assignment MUST được materialize trong transaction `start`/`submit-response`; không được âm thầm thay đổi ngữ nghĩa giữa các deployment.

---

## 5. Latency capture

### 5.1. Nguyên tắc

Latency là tín hiệu đo lường và integrity, không phải bằng chứng tuyệt đối về tính trung thực.

Backend MUST NOT:

- Tin tuyệt đối vào timestamp client.
- Hứa hẹn độ chính xác tuyệt đối 1 ms.
- So trực tiếp timestamp monotonic client với UTC server.
- Kết luận gian lận chỉ vì thời gian trả lời ngắn.
- Tự động quy response thành sai khi timing không khả dụng.

Trong trình duyệt không được quản lý, không thể chứng minh rằng telemetry không bị sửa. Cơ chế chống gian lận MUST kết hợp kiểm soát quyền ghi, token, replay protection, kiểm tra hợp lý và phân tích hành vi.

### 5.2. Đồng hồ

Client MUST dùng monotonic clock:

| Nền tảng | Ví dụ |
|---|---|
| Web | `performance.now()` |
| Android | `SystemClock.elapsedRealtimeNanos()` |
| iOS | API monotonic/continuous time phù hợp |
| Desktop | Monotonic clock của runtime |

Client MUST NOT dùng `Date.now()` hoặc wall clock để tính response latency.

Mỗi monotonic epoch có một `clock_context_id` mới. Reload trang, khởi động lại process hoặc thay đổi clock origin MUST tạo context mới.

Độ phân giải danh nghĩa của API không đồng nghĩa với độ chính xác thực tế. Browser throttling, rendering pipeline, scheduler và privacy rounding đều có thể làm giảm chất lượng đo.

### 5.3. Các timestamp bắt buộc về ngữ nghĩa

Các giá trị dưới đây là millisecond kể từ một monotonic origin, không phải Unix timestamp:

| Trường | Định nghĩa |
|---|---|
| `render_timestamp` | Khi nội dung item đã được commit vào giao diện và client quan sát được cơ hội hiển thị đầu tiên |
| `interaction_timestamp` | Tương tác có chủ đích đầu tiên với vùng trả lời |
| `submit_timestamp` | Khi client đóng băng response để gửi lần đầu |

`render_timestamp` không chứng minh pixel đã thực sự được người dùng nhìn thấy.

Trên web, client SHOULD dùng layout/paint lifecycle và `requestAnimationFrame` theo chính sách nền tảng; không ghi ngay lúc HTTP response về.

Tương tác hợp lệ bao gồm pointer, keyboard, assistive technology và thao tác chọn/nhập đáp án. Mouse move hoặc focus tự động không phải tương tác trả lời.

`interaction_timestamp` MAY là `null` nếu không quan sát được tương tác; backend gắn cờ timing thay vì tự suy diễn.

Retry MUST giữ nguyên `submit_timestamp` và toàn bộ payload.

### 5.4. Tính toán

Chỉ tính các đại lượng sau nếu timestamp cùng context và có thứ tự hợp lệ:

```text
first_interaction_latency_ms =
    interaction_timestamp - render_timestamp

response_latency_ms =
    submit_timestamp - render_timestamp

post_interaction_latency_ms =
    submit_timestamp - interaction_timestamp

foreground_latency_estimate_ms =
    response_latency_ms - union(background_intervals)
```

Các interval MUST được cắt vào phạm vi `[render_timestamp, submit_timestamp]` và tính hợp để không trừ hai lần.

Mỗi segment phải thỏa:

```text
render_timestamp >= 0
submit_timestamp >= render_timestamp

interaction_timestamp == null
OR
render_timestamp <= interaction_timestamp <= submit_timestamp
```

Giá trị âm, không hữu hạn hoặc thứ tự trái ngược MUST bị từ chối với `422 INVALID_TIMING`.

Timing thiếu do API không hỗ trợ hoặc reload có thể được chấp nhận nếu được biểu diễn bằng status rõ ràng.

### 5.5. Nhiều context và chuyển thiết bị

Một delivery có thể có nhiều exposure segment:

- Một segment trước reload.
- Một segment sau reload.
- Một segment ở thiết bị mới.

Backend MUST NOT lấy timestamp ở hai context khác nhau rồi trừ trực tiếp.

Có thể tổng hợp duration của từng segment hợp lệ, nhưng MUST gắn nhãn `partial` nếu có khoảng mất quan sát.

Sau chuyển thiết bị:

- Item vẫn giữ nguyên.
- Timing tổng thể tối thiểu mang cờ `cross_device`.
- Không được coi thời gian từ render trên thiết bị mới là toàn bộ response latency.
- Telemetry từ segment cũ không được khôi phục phải được đánh dấu thiếu.

### 5.6. Backgrounding

Client MUST ghi nhận các khoảng ứng dụng không ở foreground khi nền tảng cho phép:

```text
background interval:
  start_timestamp
  end_timestamp
```

Khi app quay lại foreground:

- Đóng interval đang mở.
- Kiểm tra context còn hợp lệ.
- Nếu process đã khởi động lại, mở exposure segment mới.

Monotonic clock của một số nền tảng có hành vi khác nhau trong sleep. Client MUST khai báo nguồn clock; backend MUST NOT giả định mọi elapsed time đều bao gồm suspend.

Background time không làm dừng hard deadline.

### 5.7. Đối chiếu client–server

Backend SHOULD lưu:

- `issued_at`
- `first_request_received_at`
- `accepted_at`
- Thời điểm cấp lại token và chuyển lease.
- Chất lượng đồng hồ của hạ tầng.

Backend có thể đối chiếu:

```text
server_observed_window_ms =
    first_request_received_at - issued_at
```

Đại lượng này bao gồm truyền mạng, thời gian chờ, rendering và thao tác. Nó không phải response latency thuần.

Giới hạn kiểm tra MUST có tolerance theo môi trường triển khai. Chênh lệch nhỏ MUST NOT bị xem là gian lận.

`server_time` trong API chỉ phục vụ hiển thị countdown và đồng bộ gần đúng. Khi client ước lượng offset từ RTT, offset đó MUST NOT được dùng để chứng minh tính chính xác của telemetry hoặc thay đổi quyền hết hạn.

### 5.8. Timing integrity flags

Ví dụ:

- `timing_unavailable`
- `partial_capture`
- `background_observed`
- `cross_context`
- `cross_device`
- `implausible_duration`
- `server_window_mismatch`

Ngưỡng phát hiện và trọng số integrity MUST nằm ở backend.

Latency không được dùng như proxy trực tiếp cho năng lực từ vựng nếu chưa có bằng chứng hiệu lực đo lường. Các hiệu ứng thiết bị, hỗ trợ tiếp cận và ngôn ngữ giao diện phải được xem xét.

---

## 6. Idempotency và safe replay

### 6.1. Phạm vi

Ba endpoint POST MUST yêu cầu header:

```http
Idempotency-Key: <random opaque key>
```

Đây là `idempotency_key` của giao thức. Client SHOULD dùng UUID v4 hoặc giá trị ngẫu nhiên có ít nhất 128 bit entropy.

Phạm vi duy nhất:

```text
authenticated_principal_id
+ HTTP method
+ normalized route, including session_id
+ idempotency_key
```

### 6.2. Fingerprint

Backend MUST tạo fingerprint từ:

- Method.
- Route.
- JSON body canonicalized.
- Device ID.
- Lease version nếu có.
- Phiên bản giao thức.

Không đưa access token, trace ID, `User-Agent` hoặc thời gian truyền lại vào fingerprint.

Có thể sử dụng RFC 8785 để canonicalize JSON.

Cùng khóa nhưng khác fingerprint:

```http
409 Conflict
```

```json
{
  "error": {
    "code": "IDEMPOTENCY_KEY_REUSED",
    "message": "Khóa đã được sử dụng cho một yêu cầu khác.",
    "retryable": false,
    "request_id": "req_01"
  }
}
```

### 6.3. Atomicity

Việc ghi:

1. Response nghiệp vụ.
2. Thay đổi session.
3. Cập nhật estimator.
4. Kết quả idempotency.

MUST commit trong cùng transaction, hoặc dùng thiết kế có bảo đảm tương đương.

Không được tồn tại trạng thái “đã chấm điểm nhưng chưa thể replay”.

Outbox MUST được dùng nếu phát audit/event sang hệ thống khác sau commit.

### 6.4. Thứ tự xử lý

1. Xác thực principal và quyền sở hữu phiên.
2. Parse, kiểm tra kích thước và fingerprint.
3. Tra idempotency record.
4. Nếu request đã commit và fingerprint khớp: trả replay.
5. Nếu chưa có: kiểm tra terminal state, deadline, lease, version và nghiệp vụ.
6. Commit kết quả cùng idempotency record.

Replay một response đã commit MAY thành công dù phiên hiện đã hết hạn hoặc lease cũ đã bị thu hồi. Đây là đọc lại kết quả cũ, không phải cấp quyền ghi mới.

Ngoại lệ này không bỏ qua việc xác thực chủ thể hoặc quyền truy cập hiện tại.

### 6.5. Response replay

Replay MUST trả:

- Cùng HTTP status nghiệp vụ.
- Cùng JSON body đã commit.
- Header `Idempotency-Replayed: true`.

`Date`, tracing header và rate-limit header MAY khác.

Body replay có thể chứa `server_time`, `session_version` và lease snapshot cũ. Client MUST NOT coi replay là snapshot trạng thái mới nhất.

Đối với start/takeover bị replay sau khi lease đã thay đổi, lease cũ trong body không được tự động trở thành hợp lệ.

### 6.6. Request đang xử lý

Hai request cùng khóa đến đồng thời:

- Backend MAY chờ request đầu hoàn tất trong một khoảng giới hạn.
- Nếu chưa có kết quả, trả `409 IDEMPOTENCY_IN_PROGRESS`.
- Trả `Retry-After`.
- Client retry cùng khóa và cùng payload.

Lỗi trước commit như `503` hoặc mất kết nối không chứng minh request chưa được chấp nhận.

### 6.7. Submit cùng delivery nhưng khác khóa

Backend MUST có unique constraint trên `delivery_id`.

Nếu delivery đã có response:

- Không tạo thêm response.
- Trả `409 RESPONSE_ALREADY_ACCEPTED`.
- Có thể trả `accepted_response_id` và `accepted_client_response_id`.
- MUST NOT thay câu trả lời dù response mới khác nội dung.

### 6.8. Thời hạn lưu khóa

P0.4 quy định:

- Lưu idempotency record ít nhất đến 30 ngày sau khi phiên terminal.
- Khi phiên còn active, không được xóa record.
- TTL này phải phù hợp chính sách bảo vệ dữ liệu.
- Sau cửa sổ bảo đảm replay, terminality và unique constraints vẫn ngăn chấp nhận thêm response.

Client SHOULD xóa retry queue đã được xác nhận sớm nhất có thể.

---

## 7. Disconnect, background và chuyển thiết bị

### 7.1. Retry queue phía client

Trước khi gửi response, client MUST lưu nguyên tử vào local queue:

```text
session_id
delivery_id
client_response_id
idempotency_key
device_id
lease_version
request_body
payload_fingerprint
local_status
```

Trạng thái client tham khảo:

```text
displayed
  -> response_frozen
  -> sending
  -> acknowledged

sending
  -> outcome_unknown
  -> retrying_same_payload
  -> acknowledged
```

Client MUST NOT đổi lựa chọn hoặc timing sau khi response đã được đóng băng.

Nếu người dùng cần sửa lựa chọn, thao tác đó chỉ được phép trước lần gửi đầu tiên.

### 7.2. Mất mạng

- Client MAY cho phép hoàn thành item đã được cấp.
- Client MUST NOT tự chọn item tiếp theo.
- Không được prefetch item bank để chạy adaptive assessment offline.
- Sau reconnect, retry nguyên payload.
- Nếu chưa commit và đã quá hạn, response bị từ chối; timestamp offline không giúp vượt deadline.
- Nếu đã commit trước khi mất mạng, replay vẫn trả kết quả cũ.

### 7.3. Resume cùng thiết bị

Gọi:

```http
POST /v1/assessment/session/start
```

với `action=resume`.

Backend:

- Kiểm tra quyền sở hữu.
- Nếu lease vẫn thuộc thiết bị này và còn hiệu lực: trả lease hiện tại.
- Nếu lease đã hết hạn và phiên còn active: cấp lease mới.
- Nếu thiết bị khác đang có lease: trả `409 DEVICE_LEASE_CONFLICT`.
- Nếu terminal: trả snapshot terminal và `writer_lease: null`.

Để giải quyết một submit có kết quả chưa biết, client SHOULD retry submit cũ trước khi tạo submit mới.

### 7.4. Takeover sang thiết bị khác

Gọi `start` với `action=takeover`.

Backend MUST:

1. Yêu cầu cùng principal.
2. Áp dụng xác thực tăng cường nếu policy yêu cầu.
3. Tăng `lease_version`.
4. Thu hồi quyền ghi của lease trước.
5. Giữ nguyên pending item.
6. Ghi audit event.
7. Gắn timing continuity flag thích hợp.

Nếu submit cũ và takeover cạnh tranh, thứ tự commit quyết định:

- Submit commit trước: response được chấp nhận, takeover nhìn thấy tiến độ mới.
- Takeover commit trước: submit chưa commit dùng lease cũ bị từ chối.

### 7.5. Writer lease

Lease gồm:

- `lease_id`
- `lease_version`
- `device_id`
- `lease_expires_at`

`X-Device-ID` không phải bằng chứng xác thực thiết bị. Đây là định danh cài đặt hoặc browser profile; không được dùng thay authentication.

Mọi thao tác cấp item, submit và complete MUST yêu cầu lease hiện hành.

Lease expiry không đồng nghĩa session expiry. Client có thể resume để xin lease mới nếu phiên vẫn active.

---

## 8. Quy ước HTTP

### 8.1. Headers

```http
Authorization: Bearer <access-token>
Content-Type: application/json
Accept: application/json
X-Device-ID: <opaque-installation-id>
X-Lease-Version: <positive-integer>
Idempotency-Key: <opaque-random-key>
```

- `X-Lease-Version` không bắt buộc cho `start`.
- `Idempotency-Key` chỉ bắt buộc cho POST.
- Response SHOULD có `X-Request-ID`.
- Response MUST có `Cache-Control: no-store`.
- Không đặt credential hoặc delivery token trong URL.

### 8.2. Optimistic concurrency

`submit-response` và `complete` MUST có `expected_session_version`.

Nếu phiên đã thay đổi:

```http
409 SESSION_VERSION_CONFLICT
```

Client đồng bộ lại bằng `start(action=resume)` hoặc `next-item`, rồi tạo request mới với khóa mới nếu payload cần thay đổi.

Idempotency replay MUST được xét trước version conflict.

### 8.3. Mã lỗi

| HTTP | Code tiêu biểu | Hành vi |
|---|---|---|
| 400 | `MALFORMED_REQUEST` | Sửa cấu trúc request |
| 401 | `UNAUTHENTICATED` | Xác thực lại |
| 403 | `DEVICE_LEASE_REVOKED`, `TAKEOVER_NOT_ALLOWED` | Không retry mù |
| 404 | `SESSION_NOT_FOUND` | Bao gồm phiên không thuộc principal để hạn chế enumeration |
| 409 | `SESSION_VERSION_CONFLICT` | Đồng bộ trạng thái |
| 409 | `DEVICE_LEASE_CONFLICT`, `DEVICE_LEASE_EXPIRED` | Resume hoặc takeover |
| 409 | `IDEMPOTENCY_KEY_REUSED` | Lỗi client |
| 409 | `IDEMPOTENCY_IN_PROGRESS` | Retry cùng khóa |
| 409 | `RESPONSE_ALREADY_ACCEPTED` | Không gửi đáp án thay thế |
| 409 | `COMPLETION_NOT_ALLOWED` | Tiếp tục assessment |
| 409 | `SESSION_COMPLETED` | Không còn nhận response |
| 410 | `SESSION_EXPIRED`, `SESSION_ABANDONED`, `SESSION_INVALIDATED` | Terminal |
| 422 | `INVALID_RESPONSE`, `INVALID_TIMING`, `INVALID_DELIVERY_TOKEN` | Sửa hoặc đồng bộ theo lỗi |
| 429 | `RATE_LIMITED` | Theo `Retry-After` |
| 503 | `TEMPORARILY_UNAVAILABLE` | Retry cùng khóa nếu chưa biết kết quả |

`retryable=true` nghĩa là có thể retry nguyên request. Nó không có nghĩa là đổi payload nhưng giữ nguyên khóa.

---

## 9. Hợp đồng nghiệp vụ của bốn API

### 9.1. `POST /v1/assessment/session/start`

#### Create

- Tạo `created`.
- Cố định toàn bộ phiên bản cấu hình.
- Cấp writer lease.
- Chưa trả item.
- Trả `201 Created`.

#### Resume

- Không tạo phiên mới.
- Không reset deadline.
- Không thay item.
- Trả `200 OK`.

#### Takeover

- Chuyển quyền ghi.
- Không thay đổi assessment state hoặc kết quả đã ghi.
- Trả `200 OK`.

Nếu assessment bị tắt sau khi phiên đã tạo, backend MUST có policy rõ ràng: tiếp tục với cấu hình cố định hoặc invalidation có audit; không âm thầm đổi mô hình.

### 9.2. `GET /v1/assessment/session/{id}/next-item`

Trả một trong hai outcome:

```text
outcome = item
outcome = ready_to_complete
```

Nếu pending item tồn tại, trả lại item đó.

Nếu không còn pending item:

- Nếu đã đạt stopping rule: trả `ready_to_complete`, `delivery: null`.
- Nếu chưa đạt: chọn và cấp item tiếp theo nguyên tử.

GET không tự hoàn tất phiên và không trả kết quả.

Với phiên terminal, trả lỗi terminal tương ứng.

### 9.3. `POST /v1/assessment/session/{id}/submit-response`

Backend MUST kiểm tra:

1. Quyền truy cập.
2. Idempotency.
3. Phiên active và deadline.
4. Lease.
5. `expected_session_version`.
6. Delivery thuộc phiên và đang pending.
7. Delivery token hợp lệ.
8. Option thuộc payload đã cấp.
9. Timing hợp lệ về cấu trúc.
10. Unique acceptance.

Transaction thành công:

- Ghi response bất biến.
- Ghi timing và integrity metadata.
- Cập nhật estimator bằng mô hình backend.
- Tính stopping rule.
- Tăng session version.
- Lưu response receipt và idempotency result.

API này MUST NOT trả:

- Đúng/sai.
- Đáp án đúng.
- Điểm theo item.
- Trọng số item.
- Tham số IRT.
- Item information.
- Ước lượng năng lực trung gian, trừ khi một contract riêng đã phê duyệt việc công bố.

### 9.4. `POST /v1/assessment/session/{id}/complete`

Điều kiện:

- `state=in_progress`.
- `ready_to_complete=true`.
- Không còn pending delivery.
- Đủ response hợp lệ theo policy.
- Không có integrity block.
- Chưa quá hạn.

Backend MUST lưu kết quả và chuyển `completed` trong cùng transaction.

Nếu đang tính kết quả mà transaction chưa commit, MUST NOT công bố `completed`. Nếu scoring tạm thời không khả dụng, trả `503`; không tạo kết quả giả.

Nếu đã `completed`:

- Cùng idempotency key: replay.
- Khóa mới, cùng principal và final lease được ghi nhận: trả cùng kết quả bất biến, không chấm lại.
- Lease của phiên completed không được gia hạn chỉ để đọc kết quả.
- Thiết bị không giữ final lease phải dùng API truy xuất kết quả riêng khi được đặc tả.

---

## 10. OpenAPI 3.1 contract

Đây là contract P0.4 cho item dạng `single_choice`. Loại item mới MUST có schema và versioning rõ ràng; không nhét dữ liệu không định kiểu vào trường tùy ý.

Các ràng buộc xuyên trường và transaction trong phần văn bản có hiệu lực bổ sung cho schema.

```yaml
openapi: 3.1.0
info:
  title: Vocabulary Research Assessment API
  version: 1.0.0
  description: P0.4 session, delivery, response and completion contracts

servers:
  - url: https://api.example.invalid

security:
  - bearerAuth: []

paths:
  /v1/assessment/session/start:
    post:
      operationId: startAssessmentSession
      parameters:
        - $ref: '#/components/parameters/DeviceId'
        - $ref: '#/components/parameters/IdempotencyKey'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StartRequest'
      responses:
        '200':
          description: Session resumed or writer lease transferred
          headers:
            Idempotency-Replayed:
              $ref: '#/components/headers/IdempotencyReplayed'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StartResponse'
        '201':
          description: Session created
          headers:
            Idempotency-Replayed:
              $ref: '#/components/headers/IdempotencyReplayed'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StartResponse'
        default:
          $ref: '#/components/responses/ApiError'

  /v1/assessment/session/{id}/next-item:
    get:
      operationId: getNextAssessmentItem
      parameters:
        - $ref: '#/components/parameters/SessionId'
        - $ref: '#/components/parameters/DeviceId'
        - $ref: '#/components/parameters/LeaseVersion'
      responses:
        '200':
          description: Existing or newly assigned item, or completion readiness
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NextItemResponse'
        default:
          $ref: '#/components/responses/ApiError'

  /v1/assessment/session/{id}/submit-response:
    post:
      operationId: submitAssessmentResponse
      parameters:
        - $ref: '#/components/parameters/SessionId'
        - $ref: '#/components/parameters/DeviceId'
        - $ref: '#/components/parameters/LeaseVersion'
        - $ref: '#/components/parameters/IdempotencyKey'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SubmitRequest'
      responses:
        '200':
          description: Response accepted or committed receipt replayed
          headers:
            Idempotency-Replayed:
              $ref: '#/components/headers/IdempotencyReplayed'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SubmitResponse'
        default:
          $ref: '#/components/responses/ApiError'

  /v1/assessment/session/{id}/complete:
    post:
      operationId: completeAssessmentSession
      parameters:
        - $ref: '#/components/parameters/SessionId'
        - $ref: '#/components/parameters/DeviceId'
        - $ref: '#/components/parameters/LeaseVersion'
        - $ref: '#/components/parameters/IdempotencyKey'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CompleteRequest'
      responses:
        '200':
          description: Immutable assessment result
          headers:
            Idempotency-Replayed:
              $ref: '#/components/headers/IdempotencyReplayed'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CompleteResponse'
        default:
          $ref: '#/components/responses/ApiError'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer

  parameters:
    SessionId:
      name: id
      in: path
      required: true
      schema:
        type: string
        format: uuid

    DeviceId:
      name: X-Device-ID
      in: header
      required: true
      schema:
        type: string
        minLength: 16
        maxLength: 128
        pattern: '^[A-Za-z0-9_-]+$'

    LeaseVersion:
      name: X-Lease-Version
      in: header
      required: true
      schema:
        type: integer
        minimum: 1

    IdempotencyKey:
      name: Idempotency-Key
      in: header
      required: true
      schema:
        type: string
        minLength: 16
        maxLength: 128
        pattern: '^[A-Za-z0-9_-]+$'

  headers:
    IdempotencyReplayed:
      description: True when returning a previously committed response
      schema:
        type: boolean

  responses:
    ApiError:
      description: Structured API error; status and code follow this specification
      headers:
        Retry-After:
          description: Retry delay in seconds when applicable
          schema:
            type: integer
            minimum: 1
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorEnvelope'

  schemas:
    SessionState:
      type: string
      enum:
        - created
        - in_progress
        - completed
        - expired
        - invalidated
        - abandoned

    StartRequest:
      oneOf:
        - $ref: '#/components/schemas/CreateSessionRequest'
        - $ref: '#/components/schemas/ResumeSessionRequest'
        - $ref: '#/components/schemas/TakeoverSessionRequest'
      discriminator:
        propertyName: action
        mapping:
          create: '#/components/schemas/CreateSessionRequest'
          resume: '#/components/schemas/ResumeSessionRequest'
          takeover: '#/components/schemas/TakeoverSessionRequest'

    CreateSessionRequest:
      type: object
      additionalProperties: false
      required:
        - action
        - assessment_id
        - locale
        - client_capabilities
      properties:
        action:
          const: create
        assessment_id:
          type: string
          minLength: 1
          maxLength: 128
        locale:
          type: string
          minLength: 2
          maxLength: 35
        client_capabilities:
          $ref: '#/components/schemas/ClientCapabilities'

    ResumeSessionRequest:
      type: object
      additionalProperties: false
      required:
        - action
        - session_id
        - client_capabilities
      properties:
        action:
          const: resume
        session_id:
          type: string
          format: uuid
        client_capabilities:
          $ref: '#/components/schemas/ClientCapabilities'

    TakeoverSessionRequest:
      type: object
      additionalProperties: false
      required:
        - action
        - session_id
        - confirm_takeover
        - client_capabilities
      properties:
        action:
          const: takeover
        session_id:
          type: string
          format: uuid
        confirm_takeover:
          const: true
        client_capabilities:
          $ref: '#/components/schemas/ClientCapabilities'

    ClientCapabilities:
      type: object
      additionalProperties: false
      required:
        - platform
        - sdk_version
        - monotonic_clock
        - lifecycle_capture
      properties:
        platform:
          type: string
          enum: [web, android, ios, desktop]
        sdk_version:
          type: string
          minLength: 1
          maxLength: 64
        monotonic_clock:
          type: boolean
        lifecycle_capture:
          type: boolean

    SessionSnapshot:
      type: object
      additionalProperties: false
      required:
        - id
        - state
        - session_version
        - assessment_version
        - created_at
        - expires_at
        - abandon_at
        - accepted_response_count
        - ready_to_complete
        - pending_delivery_id
      properties:
        id:
          type: string
          format: uuid
        state:
          $ref: '#/components/schemas/SessionState'
        session_version:
          type: integer
          minimum: 1
        assessment_version:
          type: string
          minLength: 1
        created_at:
          type: string
          format: date-time
        expires_at:
          type: string
          format: date-time
        abandon_at:
          type: string
          format: date-time
        accepted_response_count:
          type: integer
          minimum: 0
        ready_to_complete:
          type: boolean
        pending_delivery_id:
          type: [string, 'null']
          format: uuid

    WriterLease:
      type: object
      additionalProperties: false
      required:
        - lease_id
        - lease_version
        - device_id
        - lease_expires_at
      properties:
        lease_id:
          type: string
          format: uuid
        lease_version:
          type: integer
          minimum: 1
        device_id:
          type: string
        lease_expires_at:
          type: string
          format: date-time

    StartResponse:
      type: object
      additionalProperties: false
      required:
        - session
        - writer_lease
        - timing_policy_version
        - server_time
      properties:
        session:
          $ref: '#/components/schemas/SessionSnapshot'
        writer_lease:
          oneOf:
            - $ref: '#/components/schemas/WriterLease'
            - type: 'null'
        timing_policy_version:
          type: string
        server_time:
          type: string
          format: date-time

    ChoiceOption:
      type: object
      additionalProperties: false
      required: [id, text]
      properties:
        id:
          type: string
          minLength: 1
          maxLength: 128
        text:
          type: string
          minLength: 1
          maxLength: 10000

    ItemDelivery:
      type: object
      additionalProperties: false
      required:
        - delivery_id
        - delivery_token
        - item_ref
        - sequence
        - response_type
        - prompt
        - options
        - issued_at
      properties:
        delivery_id:
          type: string
          format: uuid
        delivery_token:
          type: string
          minLength: 32
          maxLength: 4096
        item_ref:
          type: string
          minLength: 16
          maxLength: 128
        sequence:
          type: integer
          minimum: 1
        response_type:
          const: single_choice
        prompt:
          type: string
          minLength: 1
          maxLength: 20000
        options:
          type: array
          minItems: 2
          maxItems: 20
          items:
            $ref: '#/components/schemas/ChoiceOption'
        issued_at:
          type: string
          format: date-time

    NextItemResponse:
      type: object
      additionalProperties: false
      required: [outcome, session, delivery, server_time]
      properties:
        outcome:
          type: string
          enum: [item, ready_to_complete]
        session:
          $ref: '#/components/schemas/SessionSnapshot'
        delivery:
          oneOf:
            - $ref: '#/components/schemas/ItemDelivery'
            - type: 'null'
        server_time:
          type: string
          format: date-time
      allOf:
        - if:
            properties:
              outcome:
                const: item
          then:
            properties:
              delivery:
                $ref: '#/components/schemas/ItemDelivery'
          else:
            properties:
              delivery:
                type: 'null'

    BackgroundInterval:
      type: object
      additionalProperties: false
      required: [start_timestamp, end_timestamp]
      properties:
        start_timestamp:
          type: number
          minimum: 0
        end_timestamp:
          type: number
          minimum: 0

    TimingSegment:
      type: object
      additionalProperties: false
      required:
        - segment_id
        - clock_context_id
        - device_id
        - clock_source
        - render_timestamp
        - interaction_timestamp
        - submit_timestamp
        - end_timestamp
        - end_reason
        - background_intervals
      properties:
        segment_id:
          type: string
          format: uuid
        clock_context_id:
          type: string
          format: uuid
        device_id:
          type: string
        clock_source:
          type: string
          enum:
            - performance_now
            - elapsed_realtime
            - continuous_time
            - other_monotonic
        resolution_ms:
          type: [number, 'null']
          exclusiveMinimum: 0
        render_timestamp:
          type: number
          minimum: 0
        interaction_timestamp:
          type: [number, 'null']
          minimum: 0
        submit_timestamp:
          type: [number, 'null']
          minimum: 0
        end_timestamp:
          type: number
          minimum: 0
        end_reason:
          type: string
          enum: [submitted, context_lost, handoff]
        background_intervals:
          type: array
          maxItems: 128
          items:
            $ref: '#/components/schemas/BackgroundInterval'

    TimingCapture:
      type: object
      additionalProperties: false
      required: [status, missing_reason, segments]
      properties:
        status:
          type: string
          enum: [captured, partial, unavailable]
        missing_reason:
          type: [string, 'null']
          enum:
            - null
            - unsupported_clock
            - context_lost
            - process_terminated
            - cross_device
            - lifecycle_unavailable
            - capture_limit_exceeded
        segments:
          type: array
          maxItems: 16
          items:
            $ref: '#/components/schemas/TimingSegment'
      allOf:
        - if:
            properties:
              status:
                const: captured
          then:
            properties:
              missing_reason:
                type: 'null'
              segments:
                minItems: 1
        - if:
            properties:
              status:
                const: unavailable
          then:
            properties:
              segments:
                maxItems: 0
              missing_reason:
                type: string
        - if:
            properties:
              status:
                const: partial
          then:
            properties:
              missing_reason:
                type: string

    ChoiceResponse:
      type: object
      additionalProperties: false
      required: [type, option_id]
      properties:
        type:
          const: single_choice
        option_id:
          type: string
          minLength: 1
          maxLength: 128

    SubmitRequest:
      type: object
      additionalProperties: false
      required:
        - expected_session_version
        - delivery_id
        - delivery_token
        - client_response_id
        - response
        - timing
      properties:
        expected_session_version:
          type: integer
          minimum: 1
        delivery_id:
          type: string
          format: uuid
        delivery_token:
          type: string
          minLength: 32
          maxLength: 4096
        client_response_id:
          type: string
          format: uuid
        response:
          $ref: '#/components/schemas/ChoiceResponse'
        timing:
          $ref: '#/components/schemas/TimingCapture'

    SubmitResponse:
      type: object
      additionalProperties: false
      required:
        - accepted
        - response_id
        - client_response_id
        - delivery_id
        - accepted_at
        - next_action
        - session
        - server_time
      properties:
        accepted:
          const: true
        response_id:
          type: string
          format: uuid
        client_response_id:
          type: string
          format: uuid
        delivery_id:
          type: string
          format: uuid
        accepted_at:
          type: string
          format: date-time
        next_action:
          type: string
          enum: [next_item, complete]
        session:
          $ref: '#/components/schemas/SessionSnapshot'
        server_time:
          type: string
          format: date-time

    CompleteRequest:
      type: object
      additionalProperties: false
      required: [expected_session_version]
      properties:
        expected_session_version:
          type: integer
          minimum: 1

    UncertaintyInterval:
      type: object
      additionalProperties: false
      required: [kind, level, lower, upper, method]
      properties:
        kind:
          type: string
          enum: [confidence_interval, credible_interval]
        level:
          type: number
          exclusiveMinimum: 0
          exclusiveMaximum: 1
        lower:
          type: number
        upper:
          type: number
        method:
          type: string
          minLength: 1
          maxLength: 128

    ScoreEstimate:
      type: object
      additionalProperties: false
      required:
        - scale_id
        - scale_version
        - unit
        - estimate
        - uncertainty
      properties:
        scale_id:
          type: string
        scale_version:
          type: string
        unit:
          type: string
        estimate:
          type: number
        uncertainty:
          $ref: '#/components/schemas/UncertaintyInterval'

    AssessmentResult:
      type: object
      additionalProperties: false
      required:
        - result_id
        - computed_at
        - scoring_model_version
        - calibration_version
        - response_count
        - stopping_reason
        - estimate
        - quality_status
        - warnings
      properties:
        result_id:
          type: string
          format: uuid
        computed_at:
          type: string
          format: date-time
        scoring_model_version:
          type: string
        calibration_version:
          type: string
        response_count:
          type: integer
          minimum: 1
        stopping_reason:
          type: string
          enum:
            - precision_target_reached
            - maximum_items_reached
            - fixed_form_finished
            - eligible_item_pool_exhausted
        estimate:
          $ref: '#/components/schemas/ScoreEstimate'
        quality_status:
          type: string
          enum: [reportable, reportable_with_caution]
        warnings:
          type: array
          uniqueItems: true
          maxItems: 32
          items:
            type: string
            maxLength: 128

    CompleteResponse:
      type: object
      additionalProperties: false
      required: [session, result, server_time]
      properties:
        session:
          $ref: '#/components/schemas/SessionSnapshot'
        result:
          $ref: '#/components/schemas/AssessmentResult'
        server_time:
          type: string
          format: date-time

    ErrorDetails:
      type: object
      additionalProperties: false
      properties:
        session_state:
          $ref: '#/components/schemas/SessionState'
        current_session_version:
          type: integer
          minimum: 1
        accepted_response_id:
          type: string
          format: uuid
        accepted_client_response_id:
          type: string
          format: uuid
        reason_code:
          type: string
          maxLength: 128

    ErrorEnvelope:
      type: object
      additionalProperties: false
      required: [error]
      properties:
        error:
          type: object
          additionalProperties: false
          required: [code, message, retryable, request_id]
          properties:
            code:
              type: string
            message:
              type: string
            retryable:
              type: boolean
            request_id:
              type: string
            details:
              $ref: '#/components/schemas/ErrorDetails'
```

### 10.1. Validation bổ sung

Backend MUST kiểm tra các điều kiện không thể biểu diễn đầy đủ bằng schema đơn giản:

- Option ID duy nhất trong một item.
- Option được chọn thuộc delivery.
- `end_timestamp >= render_timestamp`.
- `end_reason=submitted` yêu cầu `submit_timestamp` khác `null` và bằng `end_timestamp`.
- Segment không kết thúc bằng submit phải có `submit_timestamp=null`.
- Timing đầy đủ có đúng một segment cuối kết thúc bằng submit.
- `segment_id` không trùng; thứ tự segment là thứ tự quan sát.
- Không trừ timestamp khác context.
- `lower <= upper`.
- `ready_to_complete` chỉ có hiệu lực trong `in_progress`.
- `CompleteResponse.session.state=completed`.
- `outcome=item` yêu cầu pending ID khớp `delivery_id`.
- `outcome=ready_to_complete` yêu cầu không có pending delivery.
- JSON parser MUST từ chối duplicate object keys, `NaN`, `Infinity` và payload vượt giới hạn.
- Request body P0.4 MUST không vượt 256 KiB; vượt giới hạn trả `413`.

---

## 11. Kết quả và dải bất định

### 11.1. Yêu cầu đo lường học

Kết quả MUST khai báo:

- Thang đo.
- Phiên bản thang đo.
- Đơn vị.
- Point estimate.
- Loại interval.
- Mức interval.
- Phương pháp tính.
- Scoring model và calibration version.
- Lý do dừng.
- Chất lượng báo cáo.

Không được dùng lẫn:

- Confidence interval.
- Bayesian credible interval.
- Prediction interval.

Nếu mô hình dùng posterior interval thì MUST trả `credible_interval`, không đổi tên thành confidence interval để đơn giản hóa giao diện.

### 11.2. Giới hạn diễn giải

Dải bất định có thể chỉ phản ánh sai số theo mô hình đã cố định. Nó không tự động bao gồm:

- Sai số hiệu chuẩn item.
- Sampling bias của item bank.
- Domain coverage.
- Model misspecification.
- Hiệu ứng thiết bị hoặc điều kiện làm bài.

Các giới hạn này MUST được mô tả trong tài liệu thang đo mà `scale_id` tham chiếu.

Không được chuyển điểm sang “số từ biết” nếu chưa có mô hình ánh xạ và bằng chứng hiệu lực tương ứng.

### 11.3. Ví dụ kết quả

Ví dụ minh họa hình dạng payload, không phải khẳng định dự án đã có thang đo được hiệu chuẩn:

```json
{
  "result_id": "f0f5830e-46c2-4e70-bb4c-082a13b3ed25",
  "computed_at": "2026-06-01T10:15:00Z",
  "scoring_model_version": "example-model-v1",
  "calibration_version": "example-calibration-v1",
  "response_count": 28,
  "stopping_reason": "precision_target_reached",
  "estimate": {
    "scale_id": "example-vocabulary-ability",
    "scale_version": "1",
    "unit": "scale_score",
    "estimate": 61.4,
    "uncertainty": {
      "kind": "credible_interval",
      "level": 0.95,
      "lower": 55.2,
      "upper": 67.8,
      "method": "posterior_equal_tailed"
    }
  },
  "quality_status": "reportable_with_caution",
  "warnings": [
    "TIMING_PARTIALLY_UNAVAILABLE"
  ]
}
```

Backend MUST NOT thu hẹp interval chỉ để đáp ứng thiết kế UI.

Nếu chưa đủ dữ liệu để có kết quả reportable, `/complete` MUST trả lỗi nghiệp vụ, không trả estimate bằng `0` hoặc interval giả.

---

## 12. Bảo mật và chống rò rỉ

### 12.1. Dữ liệu tuyệt đối không trả xuống client

Bất kỳ response, error, token có thể giải mã, HTML, bundle hoặc log client nào cũng MUST NOT chứa:

- `answer_key`
- `correct_option_id`
- Cờ `is_correct` theo lựa chọn.
- Trọng số item.
- Tham số difficulty, discrimination, guessing.
- Scoring rubric bí mật.
- Posterior nội bộ hoặc candidate ranking.
- Random seed dùng cho chọn item.
- Nội dung item chưa được cấp.
- Ngưỡng và trọng số phát hiện gian lận.

Một JWT được ký nhưng không mã hóa vẫn đọc được payload. Không được đặt đáp án hoặc tham số item trong JWT rồi coi là bí mật.

### 12.2. DTO allowlist

Backend MUST serialize bằng public DTO allowlist.

Không được:

```text
return database_item_entity
return {...internal_item}
```

sau đó chỉ xóa vài trường nhạy cảm bằng denylist.

API contract tests MUST kiểm tra cả field name và semantic leakage.

### 12.3. Delivery token

Token MUST ràng buộc tối thiểu:

```text
session_id
delivery_id
principal_id
lease_version
content_revision
expiry
nonce
```

Token SHOULD là opaque random handle lưu server-side hoặc authenticated token không chứa bí mật chấm điểm.

Token không thay thế access token và không tự xác thực người dùng.

### 12.4. Các kiểm soát khác

- TLS bắt buộc.
- Kiểm tra object-level authorization ở mọi endpoint.
- Rate limit theo principal, session và nguồn truy cập.
- CORS allowlist.
- Nếu dùng cookie auth thay bearer, MUST có CSRF protection.
- CSP và encoding nội dung item để chống XSS.
- Không log Authorization hoặc delivery token.
- Hạn chế item exposure và automated harvesting.
- Không dùng ID tuần tự cho tài nguyên công khai.
- Error integrity SHOULD trả mã tổng quát; bằng chứng chi tiết chỉ ở audit nội bộ.
- Dữ liệu timing và device ID phải có retention, access control và mục đích sử dụng rõ ràng.

---

## 13. Lưu trữ và transaction

### 13.1. Ràng buộc dữ liệu tối thiểu

```text
assessment_sessions
  PRIMARY KEY (session_id)

item_deliveries
  PRIMARY KEY (delivery_id)
  UNIQUE (session_id, sequence)
  UNIQUE active pending delivery per session

accepted_responses
  PRIMARY KEY (response_id)
  UNIQUE (delivery_id)
  UNIQUE (session_id, client_response_id)

assessment_results
  PRIMARY KEY (result_id)
  UNIQUE (session_id)

idempotency_records
  UNIQUE (principal_id, method, normalized_route, idempotency_key)

writer_leases
  UNIQUE active lease per session
```

### 13.2. Submit transaction tham khảo

```text
authenticate and authorize
lookup committed idempotency result
if replay exists:
    return replay

begin transaction
    acquire idempotency ownership
    lock session

    evaluate terminal state and deadlines
    validate lease
    validate expected session version
    validate pending delivery and token
    validate selected option and timing

    insert immutable accepted response
    update scoring state using pinned model
    mark delivery answered
    evaluate stopping rule
    increment session version

    build public receipt
    persist idempotency receipt
    append audit outbox event
commit

return committed receipt
```

Nếu scoring không thể thực hiện trong transaction ngắn, triển khai MAY dùng kiến trúc staged processing, nhưng MUST đặc tả thêm trạng thái xử lý và API tương ứng. Không được để frontend hiểu “accepted” là estimator đã cập nhật trong khi backend thực tế chưa hoàn tất.

---

## 14. Observability và audit

Audit events tối thiểu:

```text
session.created
session.started
session.resumed
session.lease_transferred
item.issued
response.accepted
response.replay_served
response.rejected
session.ready_to_complete
session.completed
session.expired
session.abandoned
session.invalidated
```

Mỗi event SHOULD có:

- Event ID.
- Session ID.
- Actor/principal reference.
- Request ID.
- Server timestamp.
- Session version trước và sau.
- Lease version.
- Reason code.
- Idempotency key hash nếu cần đối chiếu.

Operational logs SHOULD NOT chứa đáp án người dùng hoặc item text mặc định. Dữ liệu nghiên cứu chi tiết phải nằm trong kho có kiểm soát riêng.

Metrics tối thiểu:

- Duplicate acceptance violations: phải bằng `0`.
- Idempotency replay rate.
- Session version conflict rate.
- Lease conflict rate.
- Unknown outcome recovery success rate.
- Timing missingness theo platform.
- Completion/abandonment/expiry rate.
- Scoring transaction failure rate.
- Item issuance collision rate.
- P50/P95/P99 API latency.

API latency không được trộn với response latency của người tham gia.

---

## 15. Kịch bản kiểm thử chấp nhận P0.4

| ID | Kịch bản | Kết quả bắt buộc |
|---|---|---|
| SM-01 | Tạo phiên | `created`, chưa có pending item |
| SM-02 | GET đầu tiên | Chuyển `in_progress`, cấp đúng một delivery |
| SM-03 | GET đồng thời | Cùng delivery, không tăng sequence hai lần |
| SM-04 | Complete khi còn pending item | `409 COMPLETION_NOT_ALLOWED` |
| SM-05 | Request đúng hard deadline | Không chấp nhận mutation |
| SM-06 | Terminal session | Không mở lại, không chấp nhận response mới |
| ID-01 | Submit cùng khóa hai lần | Một response; lần sau replay |
| ID-02 | Commit xong nhưng response mạng bị mất | Retry trả receipt gốc |
| ID-03 | Cùng khóa, đổi option | `409 IDEMPOTENCY_KEY_REUSED` |
| ID-04 | Cùng delivery, hai khóa | Tối đa một acceptance |
| ID-05 | Hai request cùng khóa đang chạy | Replay hoặc `IDEMPOTENCY_IN_PROGRESS` |
| ID-06 | Replay sau expiry | Trả receipt đã commit, không mutation |
| ID-07 | Replay start sau takeover | Snapshot cũ không phục hồi quyền lease cũ |
| TM-01 | Wall clock client đổi | Latency monotonic không bị tính lại bằng wall clock |
| TM-02 | Timestamp đảo thứ tự | `422 INVALID_TIMING` |
| TM-03 | Reload giữa item | Context mới, timing continuity không giả tạo |
| TM-04 | Background rồi foreground | Interval được ghi; hard deadline không dừng |
| TM-05 | Không có timing API | Response vẫn có thể được chấp nhận với quality flag |
| TM-06 | Retry sau mất mạng | `submit_timestamp` không đổi |
| DV-01 | Thiết bị khác resume | Conflict nếu lease đang hiệu lực |
| DV-02 | Takeover | Lease cũ không ghi được |
| DV-03 | Takeover cạnh tranh submit | Kết quả theo thứ tự commit, không double score |
| DV-04 | Takeover khi pending item | Cùng item và thứ tự option |
| RS-01 | Complete thành công | Kết quả và `completed` commit nguyên tử |
| RS-02 | Complete retry | Cùng result ID và số liệu |
| RS-03 | Model service lỗi | Không công bố completed hoặc điểm giả |
| SC-01 | Kiểm tra tất cả response | Không có answer key hoặc trọng số |
| SC-02 | Token bị giải mã | Không lộ bí mật item |
| SC-03 | Đọc session của chủ thể khác | Không rò rỉ nội dung hoặc sự tồn tại |
| SC-04 | CDN/proxy cache | Assessment payload không được cache |
| PS-01 | Báo interval Bayesian | Dùng `credible_interval`, không gắn nhãn sai |
| PS-02 | Timing thiếu | Không tự quy thành câu trả lời sai |
| PS-03 | Adaptive stop | Backend quyết định; client không ép complete |

Ngoài unit tests, P0.4 MUST có integration tests với transaction race, network fault injection và property-based tests cho bất biến state machine.

---

## 16. Definition of Done

P0.4 chỉ được xem là hoàn tất khi:

- [ ] State machine được thực thi tập trung trong backend service.
- [ ] Mọi transition có test và audit.
- [ ] Bốn endpoint tuân thủ OpenAPI và validation bổ sung.
- [ ] Có unique constraints ngăn double acceptance.
- [ ] Idempotency commit nguyên tử với nghiệp vụ.
- [ ] Replay không làm thay đổi state, estimator hoặc item exposure.
- [ ] SDK/client dùng monotonic clock và immutable retry queue.
- [ ] Có xử lý background, context loss và cross-device.
- [ ] Writer lease và takeover đã được kiểm thử cạnh tranh.
- [ ] Deadline được kiểm tra trong request path.
- [ ] Không trả answer key, item weight hoặc tham số chấm điểm.
- [ ] Complete trả kết quả bất biến cùng dải bất định đúng ngữ nghĩa.
- [ ] Có observability cho lỗi phục hồi và timing missingness.
- [ ] Có chính sách retention cho telemetry và idempotency.
- [ ] Backend, frontend, QA, security và psychometrics cùng phê duyệt contract.

**Nguyên tắc chốt:** mạng có thể gửi lại, client có thể mất trạng thái, đồng hồ có thể không đáng tin; nhưng một delivery chỉ được chấp nhận một phản hồi, một phiên chỉ có một lifecycle nhất quán, và mọi kết quả được công bố phải có nguồn gốc cùng bất định có thể kiểm toán.